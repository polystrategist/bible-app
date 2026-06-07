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
    /** Upgrade applied and the verified tier is now Pro. */
    | { status: 'upgraded' }
    /** Charged & changed on Paddle, but the tier hasn't propagated yet (the
     *  webhook is slow); the UI will catch up via a background refresh. */
    | { status: 'pending' }
    /** Plan lives on a mobile store and must be upgraded there. */
    | { status: 'managed-elsewhere'; store: string | null }
    /** Couldn't upgrade (API/config error) — `error` holds a user message. */
    | { status: 'error' };

/** Preview of an upgrade's immediate charge, for the confirm dialog. */
export type PreviewResult =
    /** `amount` is in the currency's smallest unit (e.g. "390" = $3.90). */
    | { status: 'ok'; amount: string; currency: string; nextBilledAt: string | null }
    | { status: 'managed-elsewhere'; store: string | null }
    | { status: 'error' };

/** Outcome of scheduling a Pro → Sync downgrade. */
export type DowngradeResult =
    /** Scheduled for period end; `effectiveAt` is when Sync takes over. */
    | { status: 'scheduled'; effectiveAt: string | null }
    | { status: 'managed-elsewhere'; store: string | null }
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

    /** Configure (or re-point) the SDK to the current signed-in user.
     *
     *  The user switch is awaited: until `changeUser` resolves the SDK still
     *  reports the *previous* user's CustomerInfo, which would make a brand-new
     *  account look like it already has an active subscription. */
    async function ensureConfigured(): Promise<boolean> {
        if (!WEB_KEY) return false;
        const appUserId = authStore.user?.id ? String(authStore.user.id) : null;
        if (!appUserId) return false;

        if (!Purchases.isConfigured()) {
            Purchases.configure({ apiKey: WEB_KEY, appUserId });
            configuredFor = appUserId;
        } else if (configuredFor !== appUserId) {
            configuredFor = appUserId;
            await Purchases.getSharedInstance().changeUser(appUserId);
        }
        return true;
    }

    /** Load the current offering's packages for display. */
    async function loadPlans(): Promise<void> {
        error.value = null;
        if (!(await ensureConfigured())) {
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
        error.value = null;

        // Require a verified email before taking payment — the subscription and
        // its receipts are tied to the account email, so it must be confirmed.
        if (!authStore.user?.email_verified_at) {
            error.value =
                'Please verify your email address before subscribing. Check your inbox for the verification link.';
            return false;
        }

        if (!(await ensureConfigured())) return false;

        // Prevent duplicate/stacked subscriptions. The server-verified tier is the
        // source of truth — the RevenueCat webhook sets it for web AND mobile
        // purchases alike — so a paid tier means there's already a plan to manage.
        // (We avoid the client getCustomerInfo() here: its cached entitlements can
        // lag or report a phantom active sub on a freshly switched account.)
        await authStore.getUser(true);
        if (authStore.tier !== 'free') {
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
        if (!(await ensureConfigured())) {
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
        if (!(await ensureConfigured())) return { status: 'none' };
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
        // Keep the loading state on through the whole flow (request + the poll
        // below), so the button stays busy until the tier actually flips — the
        // poll is the slow part, so resetting before it left no feedback.
        try {
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
            }

            // The charge/plan change already succeeded. The tier flips when
            // RevenueCat's PRODUCT_CHANGE webhook reaches our backend, so poll the
            // user until it lands. (Cast avoids TS narrowing the reactive getter.)
            for (let i = 0; i < 8; i++) {
                await authStore.getUser(true);
                if ((authStore.tier as string) === 'pro') return { status: 'upgraded' };
                await new Promise((r) => setTimeout(r, 2000));
            }
            // Slower than we want to block for — keep refreshing in the background
            // so the UI catches up once the webhook lands.
            scheduleTierCatchUp();
            return { status: 'pending' };
        } finally {
            purchasingId.value = null;
        }
    }

    /** After an in-place plan change, refresh the user a few more times so the
     *  tier flips in the UI once the (async) webhook reaches the backend, even
     *  if it lands after we stop blocking the button. */
    function scheduleTierCatchUp(): void {
        for (const ms of [5000, 15000, 30000]) {
            setTimeout(() => void authStore.getUser(true), ms);
        }
    }

    /**
     * Preview the immediate prorated charge of upgrading to Pro, so the caller
     * can confirm the exact amount before billing. No charge is made.
     */
    async function previewUpgradeToPro(): Promise<PreviewResult> {
        error.value = null;
        const token = authStore.token;
        if (!token) return { status: 'error' };

        purchasingId.value = 'preview';
        try {
            const res = await axios.post(
                `${API_BASE_URL}/subscription/preview`,
                {},
                { headers: { Authorization: `Bearer ${token}` } },
            );
            return {
                status: 'ok',
                amount: String(res.data?.amount ?? '0'),
                currency: res.data?.currency ?? 'USD',
                nextBilledAt: res.data?.next_billed_at ?? null,
            };
        } catch (e: unknown) {
            if (axios.isAxiosError(e) && e.response?.status === 409) {
                return { status: 'managed-elsewhere', store: e.response.data?.store ?? null };
            }
            error.value = axios.isAxiosError(e)
                ? (e.response?.data?.message ?? 'Couldn’t preview the upgrade. Please try again.')
                : 'Couldn’t preview the upgrade. Please try again.';
            return { status: 'error' };
        } finally {
            purchasingId.value = null;
        }
    }

    /**
     * Schedule a Pro → Sync downgrade for the end of the current billing period.
     * The user keeps Pro until then — no charge or refund now. Polls the user so
     * the pending-downgrade banner appears without a restart.
     */
    async function downgradeToSync(): Promise<DowngradeResult> {
        error.value = null;
        const token = authStore.token;
        if (!token) return { status: 'error' };

        purchasingId.value = 'downgrade';
        let effectiveAt: string | null = null;
        try {
            const res = await axios.post(
                `${API_BASE_URL}/subscription/downgrade-to-sync`,
                {},
                { headers: { Authorization: `Bearer ${token}` } },
            );
            effectiveAt = res.data?.effective_at ?? null;
        } catch (e: unknown) {
            if (axios.isAxiosError(e) && e.response?.status === 409) {
                return { status: 'managed-elsewhere', store: e.response.data?.store ?? null };
            }
            error.value = axios.isAxiosError(e)
                ? (e.response?.data?.message ?? 'Downgrade failed. Please try again.')
                : 'Downgrade failed. Please try again.';
            return { status: 'error' };
        } finally {
            purchasingId.value = null;
        }

        // Refresh so the scheduled-change state (subscription_pending_change_at)
        // is reflected in the UI.
        await authStore.getUser(true);
        return { status: 'scheduled', effectiveAt };
    }

    /** Cancel a scheduled downgrade — the subscription stays on its current plan. */
    async function cancelDowngrade(): Promise<boolean> {
        error.value = null;
        const token = authStore.token;
        if (!token) return false;

        purchasingId.value = 'cancel-downgrade';
        try {
            await axios.post(
                `${API_BASE_URL}/subscription/cancel-downgrade`,
                {},
                { headers: { Authorization: `Bearer ${token}` } },
            );
        } catch {
            error.value = 'Couldn’t cancel the scheduled change. Please try again.';
            return false;
        } finally {
            purchasingId.value = null;
        }

        await authStore.getUser(true);
        return true;
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
        previewUpgradeToPro,
        downgradeToSync,
        cancelDowngrade,
    };
});
