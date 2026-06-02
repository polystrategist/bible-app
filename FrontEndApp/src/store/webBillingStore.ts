import { defineStore } from 'pinia';
import { ref } from 'vue';
import {
    Purchases,
    PurchasesError,
    ErrorCode,
    type Package,
} from '@revenuecat/purchases-js';
import { useAuthStore } from './authStore';

const WEB_KEY = import.meta.env.VITE_REVENUECAT_WEB_KEY as string | undefined;

export interface PlanOption {
    id: string;
    title: string;
    price: string;
    pkg: Package;
}

/**
 * RevenueCat Web Billing (Paddle) purchasing for the desktop/web app.
 *
 * Purchasing is enabled only when VITE_REVENUECAT_WEB_KEY is set; otherwise the
 * UI falls back to "subscribe on mobile". The SDK is configured with the
 * backend user id as the app user id (same identity the mobile app uses via
 * Purchases.logIn), so a purchase here flows through the same RevenueCat
 * webhook → user_subscriptions → tier. After a purchase we just re-fetch the
 * user to pick up the new server-verified tier.
 */
export const useWebBillingStore = defineStore('webBillingStore', () => {
    const authStore = useAuthStore();

    /** Whether web purchasing is configured at all. */
    const supported = !!WEB_KEY;

    const plans = ref<PlanOption[]>([]);
    const loading = ref(false);
    const purchasingId = ref<string | null>(null);
    const error = ref<string | null>(null);

    let configuredFor: string | null = null;

    /** Configure (or re-point) the SDK to the current signed-in user. */
    function ensureConfigured(): boolean {
        if (!WEB_KEY) return false;
        const appUserId = authStore.user?.id ? String(authStore.user.id) : null;
        if (!appUserId) return false;

        if (!Purchases.isConfigured()) {
            Purchases.configure({ apiKey: WEB_KEY, appUserId });
            configuredFor = appUserId;
        } else if (configuredFor !== appUserId) {
            void Purchases.getSharedInstance().changeUser(appUserId);
            configuredFor = appUserId;
        }
        return true;
    }

    /** Load the current offering's packages for display. */
    async function loadPlans(): Promise<void> {
        error.value = null;
        if (!ensureConfigured()) {
            plans.value = [];
            return;
        }
        loading.value = true;
        try {
            const offerings = await Purchases.getSharedInstance().getOfferings();
            const pkgs = offerings.current?.availablePackages ?? [];
            plans.value = pkgs.map((pkg) => {
                const product = pkg.webBillingProduct;
                return {
                    id: pkg.identifier,
                    title: product.title,
                    price: product.price?.formattedPrice ?? '',
                    pkg,
                };
            });
        } catch {
            error.value = 'Could not load plans. Please try again.';
            plans.value = [];
        } finally {
            loading.value = false;
        }
    }

    /** Run the hosted checkout for a package, then refresh the verified tier. */
    async function purchase(plan: PlanOption): Promise<boolean> {
        if (!ensureConfigured()) return false;
        error.value = null;
        purchasingId.value = plan.id;
        try {
            await Purchases.getSharedInstance().purchase({
                rcPackage: plan.pkg,
                customerEmail: authStore.user?.email,
            });
            // The RevenueCat webhook updates our backend; pull the new tier.
            await authStore.getUser(true);
            return true;
        } catch (e) {
            if (e instanceof PurchasesError && e.errorCode === ErrorCode.UserCancelledError) {
                return false; // user closed the checkout — not an error
            }
            error.value = 'Purchase could not be completed. Please try again.';
            return false;
        } finally {
            purchasingId.value = null;
        }
    }

    return { supported, plans, loading, purchasingId, error, loadPlans, purchase };
});
