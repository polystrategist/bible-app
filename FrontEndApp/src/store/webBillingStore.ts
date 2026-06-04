import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import axios from 'axios';
import {
    Purchases,
    PurchasesError,
    ErrorCode,
    type Package,
} from '@revenuecat/purchases-js';
import { useAuthStore } from './authStore';

const WEB_KEY = import.meta.env.VITE_REVENUECAT_WEB_KEY as string | undefined;
const API_BASE_URL = `${import.meta.env.VITE_API_BASE_URL}/api`;

/** Outcome of an in-app Sync → Pro upgrade. */
export type UpgradeResult =
    /** Upgrade applied; tier is now (or will shortly be) Pro. */
    | { status: 'upgraded' }
    /** Plan lives on a mobile store and must be upgraded there. */
    | { status: 'managed-elsewhere'; store: string | null }
    /** Couldn't upgrade (API/config error) — `error` holds a user message. */
    | { status: 'error' };

export interface PlanOption {
    id: string;
    title: string;
    price: string;
    pkg: Package;
}

/** Outcome of trying to open subscription management. */
export type ManageResult =
    /** A web (Paddle) management page was opened in the browser. */
    | { status: 'opened' }
    /** The active subscription lives on another store (Play/App Store), which
     *  has no web management URL — the caller should tell the user where to go. */
    | { status: 'managed-elsewhere'; store: string }
    /** Nothing to manage / couldn't read customer info. */
    | { status: 'none' };

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

    /** The store backing the active entitlement ('play_store', 'app_store',
     *  'rc_billing'/'paddle', 'test_store', …), or null if none / not yet read. */
    const activeStore = ref<string | null>(null);

    /** Stores whose subscriptions are billed through the web (Paddle) and can
     *  therefore be managed here in the desktop/web app. Anything else (a mobile
     *  store) must be managed on the device where it was purchased. */
    const WEB_STORES = new Set(['rc_billing', 'paddle', 'stripe']);

    /** True when the user has an active subscription that was purchased on a
     *  mobile store, so the web app can't manage/upgrade it. */
    const managedOnMobile = computed(
        () => activeStore.value !== null && !WEB_STORES.has(activeStore.value),
    );

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

    /** Whether the account already has any active entitlement (from ANY store —
     *  RevenueCat merges mobile + web under the same app user id). */
    async function hasActiveSubscription(): Promise<boolean> {
        try {
            const info = await Purchases.getSharedInstance().getCustomerInfo();
            return Object.keys(info.entitlements.active ?? {}).length > 0;
        } catch {
            return false; // can't verify — don't hard-block
        }
    }

    /** Run the hosted checkout for a package, then refresh the verified tier. */
    async function purchase(plan: PlanOption): Promise<boolean> {
        if (!ensureConfigured()) return false;
        error.value = null;

        // Prevent duplicate/stacked subscriptions: if the account already has an
        // active entitlement (web OR mobile), don't create a second paid
        // subscription. Direct the user to "Manage subscription" to change it.
        if (await hasActiveSubscription()) {
            error.value =
                'You already have an active subscription. Use "Manage subscription" to change or cancel your plan.';
            return false;
        }

        purchasingId.value = plan.id;
        try {
            await Purchases.getSharedInstance().purchase({
                rcPackage: plan.pkg,
                customerEmail: authStore.user?.email,
            });
            // The RevenueCat webhook updates our backend; pull the new tier.
            await authStore.getUser(true);
            void refreshActiveStore();
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

    /** The store backing the currently active entitlement (e.g. 'play_store',
     *  'app_store', 'paddle'/'rc_billing'), or null if none. */
    function readActiveStore(info: {
        entitlements: { active?: Record<string, { store?: string }> };
    }): string | null {
        const active = Object.values(info.entitlements.active ?? {});
        return active.length ? (active[0].store ?? null) : null;
    }

    /** Pull CustomerInfo and cache which store the active subscription lives on,
     *  so the UI can disable web-only management for mobile-bought plans. */
    async function refreshActiveStore(): Promise<void> {
        if (!ensureConfigured()) {
            activeStore.value = null;
            return;
        }
        try {
            const info = await Purchases.getSharedInstance().getCustomerInfo();
            activeStore.value = readActiveStore(info);
        } catch {
            // leave the last known value
        }
    }

    /** Open the subscription management page so the user can cancel/upgrade.
     *
     *  Web Billing only exposes a `managementURL` for subscriptions purchased
     *  through the web (Paddle). A subscription bought on mobile (Google Play /
     *  App Store) has no web management URL — it must be managed on that store —
     *  so we report it back as 'managed-elsewhere' instead of silently no-op'ing.
     *  Uses the OS default browser (Electron shell.openExternal). */
    async function manageSubscription(): Promise<ManageResult> {
        if (!ensureConfigured()) return { status: 'none' };
        try {
            const info = await Purchases.getSharedInstance().getCustomerInfo();
            const url = (info as { managementURL?: string | null }).managementURL;
            if (url) {
                void window.browserWindow.openExternal(url);
                return { status: 'opened' };
            }
            const store = readActiveStore(info);
            if (store) return { status: 'managed-elsewhere', store };
            return { status: 'none' };
        } catch {
            return { status: 'none' };
        }
    }

    /**
     * Upgrade an existing web (Paddle) Sync subscription to Pro in place.
     *
     * RevenueCat can't drive Paddle plan changes, so the backend calls the
     * Paddle API directly (prorated immediately). The tier then flips when
     * RevenueCat's PRODUCT_CHANGE webhook lands — so we poll the user a few
     * times after the request to pick up the new tier without a restart.
     */
    async function upgradeToPro(): Promise<UpgradeResult> {
        error.value = null;
        const token = authStore.token;
        if (!token) return { status: 'error' };

        purchasingId.value = 'upgrade';
        try {
            await axios.post(
                `${API_BASE_URL}/subscription/upgrade-to-pro`,
                {},
                { headers: { Authorization: `Bearer ${token}` } },
            );
        } catch (e: unknown) {
            if (axios.isAxiosError(e) && e.response?.status === 409) {
                return { status: 'managed-elsewhere', store: e.response.data?.store ?? null };
            }
            error.value = axios.isAxiosError(e)
                ? (e.response?.data?.message ?? 'Upgrade failed. Please try again.')
                : 'Upgrade failed. Please try again.';
            return { status: 'error' };
        } finally {
            purchasingId.value = null;
        }

        // Pull the new tier (webhook → backend). Poll briefly; it's usually
        // quick. (Cast avoids TS narrowing the reactive getter to a constant.)
        for (let i = 0; i < 5; i++) {
            await authStore.getUser(true);
            if ((authStore.tier as string) === 'pro') break;
            await new Promise((r) => setTimeout(r, 2000));
        }
        return { status: 'upgraded' };
    }

    return {
        supported,
        plans,
        loading,
        purchasingId,
        error,
        activeStore,
        managedOnMobile,
        loadPlans,
        refreshActiveStore,
        purchase,
        manageSubscription,
        upgradeToPro,
    };
});
