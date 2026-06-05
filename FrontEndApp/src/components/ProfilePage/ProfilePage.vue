<script lang="ts" setup>
import { NAlert, NButton, NForm, NInput, NModal, NSelect, NSpin, useDialog, useMessage } from 'naive-ui';
import { computed, ref, watch, nextTick, onMounted, onBeforeUnmount } from 'vue';
import { useAuthStore } from '../../store/authStore';
import { useWebBillingStore, type PlanOption } from '../../store/webBillingStore';
import { Icon } from '@iconify/vue';
import { useRouter } from 'vue-router';
import { DENOMINATION_OPTIONS, normalizeDenominationCode } from '../../util/denominations';
import Cropper from 'cropperjs';
import 'cropperjs/dist/cropper.css';
import { DEFAULT_PROFILE_NAMES, getDefaultProfileUrl, useAvatarUrl } from '../../util/avatar';

const loading = ref(false);
const authStore = useAuthStore();
const webBilling = useWebBillingStore();
const message = useMessage();
const dialog = useDialog();
const router = useRouter();

// ─── Subscription card (mirrors the mobile SubscriptionCard) ─────────────────
const plansModalOpen = ref(false);
// Plan-management modal (subscribers: switch plan / open Paddle portal).
const manageModalOpen = ref(false);

const tierLabel = computed(
    () => ({ free: 'Free', sync: 'Sync', pro: 'Pro' })[authStore.tier],
);
const tierBlurb = computed(() => {
    switch (authStore.tier) {
        case 'pro':
            return 'Full access to AI study tools, plus everything in Sync.';
        case 'sync':
            return 'Your study data syncs across devices. Upgrade to Pro for AI study tools.';
        default:
            return 'Unlock cross-device sync and AI-powered Bible study tools.';
    }
});

// Live price from the current offering (never hard-coded, so a price change is
// reflected automatically).
const renewsLabel = computed(() => {
    const iso = authStore.user?.subscription_renews_at;
    if (!iso) return null;
    const d = new Date(iso);
    if (Number.isNaN(d.getTime())) return null;
    return d.toLocaleDateString(undefined, {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
    });
});

const syncPlan = computed(
    () =>
        webBilling.plans.find((p) => p.id === '$rc_monthly') ??
        webBilling.plans.find(
            (p) =>
                p.title.toLowerCase().includes('sync') &&
                !p.title.toLowerCase().includes('pro'),
        ),
);
const proPlan = computed(
    () =>
        webBilling.plans.find((p) => p.id === 'pro_monthly') ??
        webBilling.plans.find((p) => p.title.toLowerCase().includes('pro')),
);

// Live price from the current offering (never hard-coded, so a price change is
// reflected automatically). Null until plans load.
const subPrice = computed(() => {
    const plan =
        authStore.tier === 'pro'
            ? proPlan.value
            : authStore.tier === 'sync'
              ? syncPlan.value
              : undefined;
    return plan ? `${plan.price}/month` : null;
});

// Plan comparison cards — show the user exactly what each tier includes.
const planCards = computed(() => [
    {
        key: 'sync',
        name: 'Sync',
        tagline: 'Sync & back up your study',
        plan: syncPlan.value,
        highlight: false,
        badge: '',
        features: [
            'Cross-device sync — notes, highlights, bookmarks & prayer lists',
            'Cloud backup of your study data',
            'Web app access',
        ],
    },
    {
        key: 'pro',
        name: 'Pro',
        tagline: 'Everything in Sync, plus AI study tools',
        plan: proPlan.value,
        highlight: true,
        badge: 'Best for study & teaching',
        features: [
            'Everything in Sync',
            'AI verse insights — contextual insight on any passage',
            'AI Bible chat — Scripture-focused answers',
            'Sermon outlines, drafts & devotionals',
        ],
    },
]);

async function buyPlan(plan: PlanOption) {
    const ok = await webBilling.purchase(plan);
    if (ok) {
        plansModalOpen.value = false;
        message.success('Subscription activated.');
    }
}

async function viewPlans() {
    plansModalOpen.value = true;
    if (webBilling.plans.length === 0) await webBilling.loadPlans();
}

// Human-readable name + (optional) management deep link for a RevenueCat store.
function storeInfo(store: string): { where: string; url?: string } {
    switch (store) {
        case 'play_store':
            return {
                where: 'Google Play (your Android device)',
                url: 'https://play.google.com/store/account/subscriptions',
            };
        case 'app_store':
        case 'mac_app_store':
            return { where: 'the App Store (your iPhone, iPad, or Mac)' };
        case 'amazon':
            return { where: 'the Amazon Appstore' };
        case 'test_store':
            return { where: 'the mobile app (test purchase)' };
        default:
            return { where: 'the app where you subscribed' };
    }
}

// "Manage subscription" — opens the web (Paddle) management page if the plan was
// bought on the web; otherwise tells the user which store owns it.
async function manageSubscription() {
    const res = await webBilling.manageSubscription();
    if (res.status === 'managed-elsewhere') {
        const { where, url } = storeInfo(res.store);
        message.info(`Your subscription was purchased through ${where}. Manage or cancel it there.`);
        if (url) void window.browserWindow.openExternal(url);
    } else if (res.status === 'none') {
        message.error('Couldn’t open subscription management. Please try again.');
    }
}

// Format a Paddle minor-unit amount (e.g. "390") in its currency (e.g. "$3.90").
function formatAmount(minor: string, currency: string): string {
    const value = Number(minor) / 100;
    if (Number.isNaN(value)) return '';
    try {
        return new Intl.NumberFormat(undefined, { style: 'currency', currency }).format(value);
    } catch {
        return `${value.toFixed(2)} ${currency}`;
    }
}

// Route a plan-change result that came back 'managed-elsewhere' (the plan lives
// on a mobile store) — tell the user where to go and open that store if we can.
function notifyManagedElsewhere(store: string | null, verb: string) {
    const { where, url } = storeInfo(store ?? '');
    message.info(`Your subscription is billed through ${where}. ${verb} there to avoid being charged twice.`);
    if (url) void window.browserWindow.openExternal(url);
}

// "Upgrade to Pro" — preview the exact prorated charge first, confirm with the
// user, then change the plan in place via the backend (prorated immediately)
// and poll for the tier to flip. A plan bought on mobile can't be upgraded here
// (it would create a second, stacked subscription and double-charge).
async function upgradeToPro() {
    const preview = await webBilling.previewUpgradeToPro();
    if (preview.status === 'managed-elsewhere') {
        notifyManagedElsewhere(preview.store, 'Upgrade to Pro');
        return;
    }
    if (preview.status !== 'ok') {
        message.error(webBilling.error ?? 'Couldn’t start the upgrade. Please try again.');
        return;
    }

    const due = formatAmount(preview.amount, preview.currency);
    const proPrice = proPlan.value?.price ?? '$5.99';
    const renews = renewsLabel.value;
    dialog.warning({
        title: 'Upgrade to Pro',
        content: `You’ll be charged ${due} today, prorated for the rest of this billing period, then ${proPrice}/month${renews ? ` from ${renews}` : ''}.`,
        positiveText: 'Upgrade',
        negativeText: 'Cancel',
        onPositiveClick: async () => {
            const res = await webBilling.upgradeToPro();
            if (res.status === 'upgraded') {
                manageModalOpen.value = false;
                message.success('You’re now on Pro. AI study tools are unlocked.');
            } else if (res.status === 'managed-elsewhere') {
                notifyManagedElsewhere(res.store, 'Upgrade to Pro');
            } else {
                message.error(webBilling.error ?? 'Upgrade failed. Please try again.');
            }
        },
    });
}

// "Switch to Sync" — schedule a downgrade for period end (keep Pro until the
// renewal date, then move to Sync; no charge or refund now).
function confirmDowngrade() {
    const renews = renewsLabel.value;
    dialog.warning({
        title: 'Switch to Sync?',
        content: `You’ll keep Pro${renews ? ` until ${renews}` : ' until your renewal date'}, then move to the Sync plan. No charge now, and AI tools stay on until then.`,
        positiveText: 'Switch to Sync',
        negativeText: 'Keep Pro',
        onPositiveClick: async () => {
            const res = await webBilling.downgradeToSync();
            if (res.status === 'scheduled') {
                manageModalOpen.value = false;
                message.success('Scheduled — you’ll switch to Sync at the end of this billing period.');
            } else if (res.status === 'managed-elsewhere') {
                notifyManagedElsewhere(res.store, 'Change your plan');
            } else {
                message.error(webBilling.error ?? 'Downgrade failed. Please try again.');
            }
        },
    });
}

// Cancel a scheduled downgrade — stay on Pro.
async function keepPro() {
    const ok = await webBilling.cancelDowngrade();
    if (ok) message.success('Got it — you’ll stay on Pro.');
    else message.error(webBilling.error ?? 'Couldn’t cancel the scheduled change. Please try again.');
}

// Open the in-app plan-management modal (subscribers), preloading plans.
async function openManage() {
    manageModalOpen.value = true;
    if (webBilling.plans.length === 0) await webBilling.loadPlans();
}

// ISO date a scheduled downgrade takes effect, formatted, or null when none.
const pendingDowngradeAt = computed(() => {
    const iso = authStore.user?.subscription_pending_change_at;
    if (!iso) return null;
    const d = new Date(iso);
    if (Number.isNaN(d.getTime())) return null;
    return d.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
});

onMounted(() => {
    // Preload plans so the live price shows for subscribers and "Upgrade to Pro"
    // / the plan modal are instant.
    if (webBilling.supported && authStore.user) {
        void webBilling.loadPlans();
        // Find out which store the active plan lives on, so we can disable
        // web-only management when it was bought on mobile.
        void webBilling.refreshActiveStore();
    }
});

// A subscription bought on mobile (Google Play / App Store) can't be managed
// or upgraded from the web app — it must be handled in the mobile app.
const subscribedOnMobile = computed(() => webBilling.managedOnMobile);
const mobileStoreLabel = computed(
    () => storeInfo(webBilling.activeStore ?? '').where,
);

// ─── Name / Username / Email editing ─────────────────────────────────────────
const profileName     = ref(authStore.user?.name ?? '');
const profileUsername = ref(authStore.user?.username ?? '');
const profileEmail    = ref(authStore.user?.email ?? '');
const profileSaving   = ref(false);
const usernameError   = ref('');

function validateUsername(val: string): string {
    if (!val) return 'Username is required';
    if (!/^[a-z0-9_]{3,30}$/.test(val)) return '3–30 chars: lowercase letters, numbers, underscores only';
    return '';
}

const profileDirty = computed(() =>
    profileName.value.trim()     !== (authStore.user?.name ?? '') ||
    profileUsername.value.trim() !== (authStore.user?.username ?? '') ||
    profileEmail.value.trim()    !== (authStore.user?.email ?? ''),
);

function resetProfile() {
    profileName.value     = authStore.user?.name ?? '';
    profileUsername.value = authStore.user?.username ?? '';
    profileEmail.value    = authStore.user?.email ?? '';
    usernameError.value   = '';
}

const profileRefreshing = ref(false);

// ─── Email Verification ──────────────────────────────────────────────────────
const isEmailVerified = computed(() => !!authStore.user?.email_verified_at);
const resendingVerification = ref(false);

async function resendVerification() {
    resendingVerification.value = true;
    const result = await authStore.resendVerification();
    resendingVerification.value = false;
    if (result.success) {
        if (result.alreadyVerified) {
            message.success('Your email is already verified.');
            await authStore.getUser(true);
        } else {
            message.success(result.message);
        }
    } else {
        message.error(result.message);
    }
}

async function refreshProfile() {
    profileRefreshing.value = true;
    await authStore.getUser(true);
    profileRefreshing.value = false;
    profileName.value     = authStore.user?.name     ?? profileName.value;
    profileUsername.value = authStore.user?.username ?? profileUsername.value;
    profileEmail.value    = authStore.user?.email    ?? profileEmail.value;
}

async function saveProfile() {
    const name     = profileName.value.trim();
    const username = profileUsername.value.trim();
    const email    = profileEmail.value.trim();
    if (!name || !email) return;

    const err = validateUsername(username);
    if (err) { usernameError.value = err; return; }
    usernameError.value = '';

    const payload: { name?: string; username?: string; email?: string } = {};
    if (name     !== authStore.user?.name)               payload.name     = name;
    if (username !== (authStore.user?.username ?? ''))   payload.username = username;
    if (email    !== authStore.user?.email)              payload.email    = email;
    if (!Object.keys(payload).length) return;

    profileSaving.value = true;
    const result = await authStore.updateProfile(payload);
    profileSaving.value = false;

    if (result.success) {
        profileName.value     = authStore.user?.name     ?? name;
        profileUsername.value = authStore.user?.username ?? username;
        profileEmail.value    = authStore.user?.email    ?? email;
        if (result.emailVerificationSent) {
            message.info(`Verification email sent to ${payload.email}. Check your inbox to confirm the change.`, { duration: 6000 });
        } else {
            message.success('Profile updated.');
        }
    } else {
        message.error(result.message ?? 'Failed to update profile.');
    }
}

const selectScrollbarProps = { trigger: 'none' as const };

const denomination = ref<string | null>(null);
const denominationSaving = ref(false);
const denominationDirty = ref(false);

onMounted(() => {
    denomination.value = normalizeDenominationCode(authStore.user?.info?.denomination);
});

async function saveDenomination() {
    denominationSaving.value = true;
    const result = await authStore.updateUserInfo({
        denomination: normalizeDenominationCode(denomination.value),
    });
    denominationSaving.value = false;
    denominationDirty.value = false;
    if (result.success) message.success('Denomination saved.');
    else message.error(result.message ?? 'Failed to save.');
}

const initials = computed(() => {
    const name = authStore.user?.name ?? '';
    return name
        .split(' ')
        .map((part) => part[0])
        .filter(Boolean)
        .slice(0, 2)
        .join('')
        .toUpperCase();
});

async function logout() {
    loading.value = true;
    const result = await authStore.logout();
    loading.value = false;
    if (result.success) {
        message.success('Logged out successfully.');
    } else {
        message.warning('Logged out (offline).');
    }
    router.push('/profile');
}


// Danger Zone
const dangerZoneOpen = ref(false);
const showDeleteModal = ref(false);
const deleteEmail = ref('');
const deleteError = ref('');
const isDeleting = ref(false);

function openDeleteModal() {
    deleteEmail.value = '';
    deleteError.value = '';
    showDeleteModal.value = true;
}

async function confirmDeleteAccount() {
    deleteError.value = '';
    isDeleting.value = true;
    const result = await authStore.deleteAccount(deleteEmail.value.trim());
    isDeleting.value = false;
    if (result.success) {
        showDeleteModal.value = false;
        message.success('Account deleted.');
        router.push('/profile');
    } else {
        deleteError.value = result.message;
    }
}

// ─── Profile Picture ─────────────────────────────────────────────────────────

// Build picker list from the shared utility (one entry per default-profile folder).
// 100px version is used for the grid thumbnails.
const pickerProfiles = DEFAULT_PROFILE_NAMES.map((name) => ({
    name,
    previewUrl: getDefaultProfileUrl(name, 100) ?? '',
}));

// Full-size avatar for the header (400px, with offline cache fallback).
const avatarUrl = useAvatarUrl(400);

// ── Picker modal ──────────────────────────────────────────────────────────────
const showPicturePicker = ref(false);
const pictureLoading = ref(false);
const fileInputRef = ref<HTMLInputElement | null>(null);

function openPicturePicker() {
    showPicturePicker.value = true;
}

async function selectDefaultPicture(name: string) {
    pictureLoading.value = true;
    const result = await authStore.updateProfilePicture({ type: 'default', name });
    pictureLoading.value = false;
    if (result.success) {
        showPicturePicker.value = false;
        message.success('Profile picture updated.');
    } else {
        message.error(result.message ?? 'Failed to update picture.');
    }
}

function triggerFileInput() {
    fileInputRef.value?.click();
}

function handleFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) return;
    input.value = '';

    const reader = new FileReader();
    reader.onload = (e) => {
        cropSrc.value = e.target!.result as string;
        showPicturePicker.value = false;
        showCropModal.value = true;
    };
    reader.readAsDataURL(file);
}

// ── Crop modal ────────────────────────────────────────────────────────────────
const showCropModal = ref(false);
const cropSrc = ref('');
const cropImageRef = ref<HTMLImageElement | null>(null);
const cropUploading = ref(false);
let cropperInstance: Cropper | null = null;

watch(showCropModal, async (open) => {
    if (open) {
        await nextTick();
        if (cropImageRef.value) {
            cropperInstance = new Cropper(cropImageRef.value as HTMLImageElement, {
                aspectRatio: 1,
                viewMode: 1,
                dragMode: 'move',
                autoCropArea: 0.85,
                restore: false,
                guides: false,
                center: false,
                highlight: false,
                cropBoxMovable: true,
                cropBoxResizable: true,
                toggleDragModeOnDblclick: false,
            });
        }
    } else {
        destroyCropper();
    }
});

function destroyCropper() {
    if (cropperInstance) {
        cropperInstance.destroy();
        cropperInstance = null;
    }
}

function cancelCrop() {
    showCropModal.value = false;
    cropSrc.value = '';
    showPicturePicker.value = true;
}

// Sizes generated on every upload: [dimension, maxKb]
const AVATAR_SIZES: [number, number][] = [
    [400, 50],
    [300, 30],
    [100, 10],
    [50,   5],
    [25,   3],
];

async function confirmCrop() {
    if (!cropperInstance) return;
    cropUploading.value = true;

    try {
        // Crop at the largest size; all smaller sizes are downscaled from this canvas.
        const source = cropperInstance.getCroppedCanvas({ width: 400, height: 400 });
        const files = await generateAvatarSizes(source);

        const result = await authStore.updateProfilePicture({ type: 'upload', files });
        if (result.success) {
            showCropModal.value = false;
            cropSrc.value = '';
            message.success('Profile picture updated.');
        } else {
            message.error(result.message ?? 'Failed to upload picture.');
        }
    } catch {
        message.error('Failed to process image.');
    } finally {
        cropUploading.value = false;
    }
}

async function generateAvatarSizes(source: HTMLCanvasElement): Promise<Record<number, File>> {
    const files: Record<number, File> = {};
    for (const [size, maxKb] of AVATAR_SIZES) {
        const canvas = document.createElement('canvas');
        canvas.width  = size;
        canvas.height = size;
        canvas.getContext('2d')!.drawImage(source, 0, 0, size, size);
        const blob = await compressCanvasToTarget(canvas, maxKb);
        files[size] = new File([blob], `${size}.jpg`, { type: 'image/jpeg' });
    }
    return files;
}

async function compressCanvasToTarget(canvas: HTMLCanvasElement, maxKb: number): Promise<Blob> {
    for (let q = 0.9; q >= 0.1; q = Math.round((q - 0.05) * 100) / 100) {
        const blob = await canvasToJpegBlob(canvas, q);
        if (blob.size <= maxKb * 1024) return blob;
    }
    return canvasToJpegBlob(canvas, 0.1);
}

function canvasToJpegBlob(canvas: HTMLCanvasElement, quality: number): Promise<Blob> {
    return new Promise((resolve, reject) => {
        canvas.toBlob(
            (b) => (b ? resolve(b) : reject(new Error('toBlob failed'))),
            'image/jpeg',
            quality,
        );
    });
}

onBeforeUnmount(destroyCropper);
</script>

<template>
    <div class="profile-shell">
        <NForm v-if="authStore.user">
            <div class="flex items-start justify-between gap-4 mb-6">
                <div class="flex items-center gap-4">
                    <!-- Avatar with edit overlay -->
                    <button class="avatar-wrapper" @click="openPicturePicker" title="Change profile picture">
                        <img
                            v-if="avatarUrl"
                            :src="avatarUrl"
                            class="profile-avatar is-image"
                            alt="Profile"
                        />
                        <div v-else class="profile-avatar">
                            {{ initials }}
                        </div>
                        <div class="avatar-edit-overlay">
                            <Icon icon="mdi:camera" />
                        </div>
                    </button>
                    <div class="flex flex-col gap-1">
                        <h3 class="text-lg flex gap-2 items-center font-700 m-0">
                            <Icon icon="mdi:account-circle" />
                            <span>Profile</span>
                        </h3>
                        <span class="text-sm opacity-65">
                            Your account information and sync status.
                        </span>
                    </div>
                </div>
                <div class="profile-status-chip" :class="authStore.syncEnabled ? 'is-enabled' : 'is-disabled'">
                    <Icon :icon="authStore.syncEnabled ? 'mdi:cloud-check' : 'mdi:cloud-off-outline'" />
                    <span>{{ authStore.syncEnabled ? 'Sync On' : 'Desktop Only' }}</span>
                </div>
            </div>

            <!-- Unverified email warning -->
            <div v-if="!isEmailVerified" class="verify-warning mb-6">
                <Icon icon="mdi:email-alert-outline" class="verify-warning-icon" />
                <div class="flex-1">
                    <p class="verify-warning-title">Verify your email address</p>
                    <p class="verify-warning-text">
                        Your email is not yet verified. Please verify it before
                        <strong>June 30, 2026</strong>, or your account will stop working.
                    </p>
                </div>
                <NButton
                    size="small"
                    type="warning"
                    :loading="resendingVerification"
                    :disabled="resendingVerification"
                    @click="resendVerification"
                >
                    <template #icon><Icon icon="mdi:email-fast-outline" /></template>
                    Resend Email
                </NButton>
            </div>

            <!-- Row 1: Name | Username -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-3">
                <div class="profile-info-block">
                    <span class="profile-label">Name</span>
                    <NInput v-model:value="profileName" size="large" placeholder="Your name">
                        <template #prefix>
                            <Icon icon="mdi:account-outline" class="opacity-50 mr-1" />
                        </template>
                    </NInput>
                </div>
                <div class="profile-info-block">
                    <span class="profile-label">Username</span>
                    <NInput
                        v-model:value="profileUsername"
                        size="large"
                        placeholder="your_handle"
                        :status="usernameError ? 'error' : undefined"
                        @input="profileUsername = profileUsername.toLowerCase().replace(/[^a-z0-9_]/g, '')"
                    >
                        <template #prefix><span class="username-at-prefix">@</span></template>
                    </NInput>
                    <p v-if="usernameError" class="field-error">{{ usernameError }}</p>
                    <p v-else class="field-hint">Public handle · used in profile URLs</p>
                </div>
            </div>

            <!-- Row 2: Email (full width) -->
            <div class="mb-3">
                <div class="profile-info-block">
                    <div class="profile-label-row">
                        <span class="profile-label">Email</span>
                        <NButton size="tiny" quaternary :loading="profileRefreshing" title="Refresh profile" @click="refreshProfile">
                            <template #icon><Icon icon="mdi:refresh" /></template>
                        </NButton>
                    </div>
                    <NInput v-model:value="profileEmail" size="large" type="text" placeholder="your@email.com">
                        <template #prefix>
                            <Icon icon="mdi:email-outline" class="opacity-50 mr-1" />
                        </template>
                    </NInput>
                    <p v-if="authStore.user.pending_email" class="pending-email-hint">
                        <Icon icon="mdi:clock-outline" class="inline mr-1" />
                        Pending: <strong>{{ authStore.user.pending_email }}</strong> — check your inbox to confirm.
                    </p>
                </div>
            </div>

            <div class="flex gap-2 mb-6 justify-end">
                <NButton
                    v-if="profileDirty"
                    size="small"
                    @click="resetProfile"
                    :disabled="profileSaving"
                >
                    Cancel
                </NButton>
                <NButton
                    type="primary"
                    size="small"
                    :loading="profileSaving"
                    :disabled="profileSaving || !profileDirty"
                    @click="saveProfile"
                >
                    <template #icon><Icon icon="mdi:content-save-outline" /></template>
                    Save Changes
                </NButton>
            </div>

            <div class="sub-card">
                <!-- ── Subscription ───────────────────────────────────── -->
                <div class="sub-section">
                    <div class="sub-head">
                        <Icon icon="lucide:sparkles" class="sub-head__icon" />
                        <span class="sub-head__title">Subscription</span>
                        <span class="plan-pill" :class="`tier-${authStore.tier}`">{{ tierLabel }}</span>
                    </div>
                    <p class="sub-blurb">{{ tierBlurb }}</p>

                    <div
                        v-if="authStore.tier !== 'free' && (subPrice || renewsLabel)"
                        class="sub-billing"
                    >
                        <Icon icon="lucide:credit-card" />
                        <span>
                            <template v-if="subPrice">{{ subPrice }}</template>
                            <template v-if="subPrice && renewsLabel"> · </template>
                            <template v-if="renewsLabel">Renews {{ renewsLabel }}</template>
                        </span>
                    </div>

                    <!-- Free → open the plan comparison modal -->
                    <template v-if="authStore.tier === 'free'">
                        <NButton type="primary" block @click="viewPlans">
                            <template #icon><Icon icon="lucide:sparkles" /></template>
                            View plans
                        </NButton>
                    </template>

                    <!-- Subscribed → upgrade (Sync only) + manage -->
                    <template v-else>
                        <!-- Scheduled downgrade → keep the user informed. -->
                        <NAlert
                            v-if="pendingDowngradeAt"
                            type="warning"
                            :bordered="false"
                            class="mb-2 pending-downgrade"
                        >
                            Switching to Sync on {{ pendingDowngradeAt }}.
                            <NButton text type="primary" size="small" @click="keepPro">Keep Pro</NButton>
                        </NAlert>

                        <NButton
                            v-if="authStore.tier === 'sync'"
                            type="primary"
                            block
                            class="mb-2"
                            :disabled="subscribedOnMobile || webBilling.purchasingId === 'preview' || webBilling.purchasingId === 'upgrade'"
                            :loading="webBilling.purchasingId === 'preview' || webBilling.purchasingId === 'upgrade'"
                            @click="upgradeToPro"
                        >
                            <template #icon><Icon icon="lucide:arrow-up" /></template>
                            Upgrade to Pro
                        </NButton>
                        <NButton
                            block
                            :disabled="subscribedOnMobile"
                            @click="openManage"
                        >
                            <template #icon><Icon icon="lucide:settings" /></template>
                            Manage subscription
                        </NButton>

                        <!-- Plan bought on a mobile store → can't manage it here. -->
                        <div v-if="subscribedOnMobile" class="manage-elsewhere-note">
                            <Icon icon="mdi:cellphone-cog" />
                            <span>
                                You subscribed through {{ mobileStoreLabel }}. To
                                upgrade, change, or cancel your plan, please manage it
                                in the Believers Sword <strong>mobile app</strong>.
                            </span>
                        </div>
                    </template>
                </div>

                <div class="sub-divider" />

                <!-- ── Sync ───────────────────────────────────────────── -->
                <div class="sub-section">
                    <div class="sub-head">
                        <Icon icon="mdi:sync" class="sub-head__icon" />
                        <span class="sub-head__title">Sync</span>
                        <span class="onoff-chip" :class="authStore.syncEnabled ? 'is-on' : 'is-off'">
                            <span class="onoff-dot" /> {{ authStore.syncEnabled ? 'On' : 'Off' }}
                        </span>
                    </div>
                    <p class="sub-blurb">
                        Keep your bookmarks, highlights, notes, and prayer lists backed up and in sync across devices.
                    </p>
                    <div v-if="authStore.syncEnabled" class="sync-footer-item is-active">
                        <Icon icon="mdi:check-circle-outline" />
                        <span>Sync is included in your subscription and stays on automatically</span>
                    </div>
                    <div v-else class="sync-free-notice">
                        <Icon icon="mdi:lock-outline" />
                        <span>Cross-device sync is part of the Sync and Pro plans.</span>
                    </div>
                </div>

                <div class="sub-divider" />

                <!-- ── AI Assistant ───────────────────────────────────── -->
                <div class="sub-section">
                    <div class="sub-head">
                        <Icon icon="lucide:sparkles" class="sub-head__icon" />
                        <span class="sub-head__title">AI Assistant</span>
                        <span class="onoff-chip" :class="authStore.isAiEnabled ? 'is-on' : 'is-off'">
                            <span class="onoff-dot" /> {{ authStore.isAiEnabled ? 'On' : 'Off' }}
                        </span>
                    </div>
                    <p class="sub-blurb">
                        Verse insights, sermon outlines, devotionals, and Bible chat.
                    </p>
                    <div v-if="authStore.isAiEnabled" class="sync-footer-item is-active">
                        <Icon icon="mdi:check-circle-outline" />
                        <span>Included with Pro — an AI allowance that refreshes every few hours</span>
                    </div>
                    <div v-else class="sync-free-notice">
                        <Icon icon="mdi:lock-outline" />
                        <span>The AI Assistant is part of the Pro plan.</span>
                    </div>
                </div>
            </div>

            <!-- Denomination -->
            <div class="denomination-panel mt-4">
                <div class="flex items-center gap-2 font-700 mb-1">
                    <Icon icon="mdi:church" />
                    <span>Denomination</span>
                    <span class="required-badge">Required</span>
                </div>
                <p class="m-0 text-sm opacity-70 mb-3">
                    Select your church denomination. This helps connect you with your community.
                </p>
                <NAlert v-if="!denomination" type="warning" :show-icon="false" class="mb-3 text-sm">
                    Please set your denomination to participate in the Believers' Feed.
                </NAlert>
                <div class="flex gap-2 items-end">
                    <NSelect
                        v-model:value="denomination"
                        :options="DENOMINATION_OPTIONS"
                        placeholder="Select your denomination..."
                        filterable
                        clearable
                        :virtual-scroll="false"
                        :scrollbar-props="selectScrollbarProps"
                        class="flex-1"
                        @update:value="denominationDirty = true"
                    />
                    <NButton
                        type="primary"
                        :loading="denominationSaving"
                        :disabled="denominationSaving || !denominationDirty"
                        @click="saveDenomination"
                    >
                        Save
                    </NButton>
                </div>
            </div>

            <div class="mt-6 flex justify-end">
                <NButton type="error" secondary @click="logout" :disabled="loading" :loading="loading">
                    <template #icon>
                        <Icon icon="mdi:logout" />
                    </template>
                    Logout
                </NButton>
            </div>

            <!-- Danger Zone -->
            <div class="danger-zone mt-8">
                <button class="danger-zone-header" @click="dangerZoneOpen = !dangerZoneOpen">
                    <div class="flex items-center gap-2">
                        <Icon icon="mdi:alert-circle-outline" class="text-red-400" />
                        <span class="font-600 text-red-400">Danger Zone</span>
                    </div>
                    <Icon
                        :icon="dangerZoneOpen ? 'mdi:chevron-up' : 'mdi:chevron-down'"
                        class="text-red-400"
                    />
                </button>
                <div v-if="dangerZoneOpen" class="danger-zone-body">
                    <div class="flex items-start justify-between gap-4 flex-wrap">
                        <div>
                            <p class="font-600 m-0 mb-1">Delete Account</p>
                            <p class="m-0 text-sm opacity-70" style="max-width: 480px;">
                                Permanently deletes your account and all associated data, including bookmarks,
                                highlights, notes, and prayer lists. This action cannot be undone.
                            </p>
                        </div>
                        <NButton type="error" size="small" @click="openDeleteModal">
                            <template #icon>
                                <Icon icon="mdi:trash-can-outline" />
                            </template>
                            Delete My Account
                        </NButton>
                    </div>
                </div>
            </div>
        </NForm>

        <!-- Delete Account Confirmation Modal -->
        <NModal
            v-model:show="showDeleteModal"
            preset="dialog"
            type="error"
            title="Delete Account"
            :mask-closable="!isDeleting"
            :close-on-esc="!isDeleting"
        >
            <template #icon>
                <Icon icon="mdi:alert-circle-outline" />
            </template>
            <div class="flex flex-col gap-3">
                <p class="m-0 text-sm">
                    This will permanently delete your account and all data. This action <strong>cannot be undone</strong>.
                </p>
                <p class="m-0 text-sm font-600">Enter your email address to confirm:</p>
                <NInput
                    v-model:value="deleteEmail"
                    placeholder="your@email.com"
                    type="text"
                    :disabled="isDeleting"
                    @keyup.enter="confirmDeleteAccount"
                />
                <p v-if="deleteError" class="m-0 text-sm text-red-400">{{ deleteError }}</p>
            </div>
            <template #action>
                <NButton :disabled="isDeleting" @click="showDeleteModal = false">Cancel</NButton>
                <NButton
                    type="error"
                    :loading="isDeleting"
                    :disabled="isDeleting || !deleteEmail.trim()"
                    @click="confirmDeleteAccount"
                >
                    Delete Account
                </NButton>
            </template>
        </NModal>

        <!-- Profile Picture Picker Modal -->
        <NModal
            v-model:show="showPicturePicker"
            preset="card"
            title="Change Profile Picture"
            style="max-width: 480px;"
            :mask-closable="!pictureLoading"
            :close-on-esc="!pictureLoading"
        >
            <div v-if="pictureLoading" class="flex items-center justify-center py-8">
                <NSpin size="large" />
            </div>
            <template v-else>
                <p class="m-0 text-sm opacity-70 mb-4">Choose one of the app avatars or upload your own photo.</p>

                <!-- Default app avatars -->
                <div class="picker-section-label">App Avatars</div>
                <div class="default-avatars-grid">
                    <button
                        v-for="pic in pickerProfiles"
                        :key="pic.name"
                        class="default-avatar-btn"
                        :class="{ 'is-selected': authStore.user?.info?.profile_picture === `default:${pic.name}` }"
                        @click="selectDefaultPicture(pic.name)"
                    >
                        <img :src="pic.previewUrl" :alt="pic.name" />
                        <Icon
                            v-if="authStore.user?.info?.profile_picture === `default:${pic.name}`"
                            icon="mdi:check-circle"
                            class="avatar-check-icon"
                        />
                    </button>
                </div>

                <!-- Custom upload -->
                <div class="picker-section-label mt-4">Custom Photo</div>
                <p class="m-0 text-sm opacity-60 mb-3">
                    You'll be able to crop your photo before it's uploaded.
                </p>
                <NButton @click="triggerFileInput" secondary>
                    <template #icon>
                        <Icon icon="mdi:upload" />
                    </template>
                    Upload Photo
                </NButton>
                <input
                    ref="fileInputRef"
                    type="file"
                    accept="image/jpeg,image/png,image/webp"
                    style="display: none;"
                    @change="handleFileSelected"
                />
            </template>
        </NModal>

        <!-- Crop Modal -->
        <NModal
            v-model:show="showCropModal"
            preset="card"
            title="Crop Photo"
            style="max-width: 560px;"
            :mask-closable="false"
            :close-on-esc="!cropUploading"
            @after-leave="destroyCropper"
        >
            <div class="crop-container">
                <img ref="cropImageRef" :src="cropSrc" class="crop-source-img" alt="Crop preview" />
            </div>
            <template #footer>
                <div class="flex justify-end gap-2 mt-2">
                    <NButton :disabled="cropUploading" @click="cancelCrop">
                        Back
                    </NButton>
                    <NButton
                        type="primary"
                        :loading="cropUploading"
                        :disabled="cropUploading"
                        @click="confirmCrop"
                    >
                        <template #icon>
                            <Icon icon="mdi:crop" />
                        </template>
                        Crop &amp; Upload
                    </NButton>
                </div>
            </template>
        </NModal>

        <!-- Plan comparison modal -->
        <NModal
            v-model:show="plansModalOpen"
            preset="card"
            title="Choose your plan"
            :bordered="false"
            :auto-focus="false"
            style="max-width: 720px; width: 92vw;"
        >
            <div v-if="webBilling.loading" class="sub-plan-loading">
                <NSpin size="small" /> <span>Loading plans…</span>
            </div>
            <template v-else>
                <div class="plans-grid">
                    <div
                        v-for="card in planCards"
                        :key="card.key"
                        class="plan-card"
                        :class="{ 'is-highlight': card.highlight }"
                    >
                        <div v-if="card.badge" class="plan-card__badge">{{ card.badge }}</div>
                        <div class="plan-card__name">{{ card.name }}</div>
                        <div class="plan-card__price">
                            <template v-if="card.plan">
                                {{ card.plan.price }}<span class="plan-card__per">/month</span>
                            </template>
                            <template v-else>—</template>
                        </div>
                        <p class="plan-card__tagline">{{ card.tagline }}</p>
                        <ul class="plan-card__features">
                            <li v-for="f in card.features" :key="f">
                                <Icon icon="lucide:check" /> <span>{{ f }}</span>
                            </li>
                        </ul>
                        <NButton
                            :type="card.highlight ? 'primary' : 'default'"
                            block
                            :disabled="!card.plan || webBilling.purchasingId !== null"
                            :loading="!!card.plan && webBilling.purchasingId === card.plan.id"
                            @click="card.plan && buyPlan(card.plan)"
                        >
                            Choose {{ card.name }}
                        </NButton>
                    </div>
                </div>
                <p v-if="!webBilling.supported" class="sub-hint">
                    Subscribe in the Believers Sword mobile app — your plan works here automatically.
                </p>
                <p v-if="webBilling.error" class="sub-error">{{ webBilling.error }}</p>
            </template>
        </NModal>

        <!-- Manage plan modal (active subscribers): switch plan + Paddle portal -->
        <NModal
            v-model:show="manageModalOpen"
            preset="card"
            title="Manage plan"
            :bordered="false"
            :auto-focus="false"
            style="max-width: 720px; width: 92vw;"
        >
            <div v-if="webBilling.loading" class="sub-plan-loading">
                <NSpin size="small" /> <span>Loading plans…</span>
            </div>
            <template v-else>
                <NAlert
                    v-if="pendingDowngradeAt"
                    type="warning"
                    :bordered="false"
                    class="mb-3 pending-downgrade"
                >
                    Switching to Sync on {{ pendingDowngradeAt }}.
                    <NButton text type="primary" size="small" @click="keepPro">Keep Pro</NButton>
                </NAlert>

                <div class="plans-grid">
                    <div
                        v-for="card in planCards"
                        :key="card.key"
                        class="plan-card"
                        :class="{ 'is-highlight': card.highlight, 'is-current': card.key === authStore.tier }"
                    >
                        <div
                            v-if="card.key === authStore.tier"
                            class="plan-card__badge plan-card__badge--current"
                        >
                            Current plan
                        </div>
                        <div v-else-if="card.badge" class="plan-card__badge">{{ card.badge }}</div>
                        <div class="plan-card__name">{{ card.name }}</div>
                        <div class="plan-card__price">
                            <template v-if="card.plan">
                                {{ card.plan.price }}<span class="plan-card__per">/month</span>
                            </template>
                            <template v-else>—</template>
                        </div>
                        <p class="plan-card__tagline">{{ card.tagline }}</p>
                        <ul class="plan-card__features">
                            <li v-for="f in card.features" :key="f">
                                <Icon icon="lucide:check" /> <span>{{ f }}</span>
                            </li>
                        </ul>

                        <!-- Current plan → no action -->
                        <NButton v-if="card.key === authStore.tier" block disabled>
                            Current plan
                        </NButton>
                        <!-- Sync subscriber → upgrade to Pro -->
                        <NButton
                            v-else-if="card.key === 'pro'"
                            type="primary"
                            block
                            :disabled="webBilling.purchasingId !== null"
                            :loading="webBilling.purchasingId === 'preview' || webBilling.purchasingId === 'upgrade'"
                            @click="upgradeToPro"
                        >
                            Upgrade to Pro
                        </NButton>
                        <!-- Pro subscriber → downgrade to Sync (at period end) -->
                        <NButton
                            v-else
                            block
                            :disabled="webBilling.purchasingId !== null || !!pendingDowngradeAt"
                            :loading="webBilling.purchasingId === 'downgrade'"
                            @click="confirmDowngrade"
                        >
                            {{ pendingDowngradeAt ? 'Switch scheduled' : 'Switch to Sync' }}
                        </NButton>
                    </div>
                </div>

                <div class="manage-portal-row">
                    <NButton text type="primary" @click="manageSubscription">
                        <template #icon><Icon icon="lucide:external-link" /></template>
                        Payment method &amp; cancel
                    </NButton>
                </div>
                <p v-if="webBilling.error" class="sub-error">{{ webBilling.error }}</p>
            </template>
        </NModal>
    </div>
</template>

<style scoped>
.profile-shell {
    max-width: 900px;
    margin: 0 auto;
    padding: 4px 4px 0;
    background:
        radial-gradient(circle at top right, rgba(111, 132, 255, 0.18), transparent 26%),
        linear-gradient(180deg, rgba(255, 255, 255, 0.02), rgba(255, 255, 255, 0));
    border-radius: 24px;
}

/* Avatar with camera overlay */
.avatar-wrapper {
    position: relative;
    background: none;
    border: none;
    padding: 0;
    cursor: pointer;
    border-radius: 18px;
    flex-shrink: 0;
}

.avatar-wrapper:focus-visible {
    outline: 2px solid rgba(111, 132, 255, 0.7);
    outline-offset: 2px;
}

.profile-avatar {
    width: 56px;
    height: 56px;
    border-radius: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    font-weight: 700;
    color: #fff;
    background: linear-gradient(135deg, #6f84ff 0%, #5fb0ff 100%);
    box-shadow: 0 10px 30px rgba(95, 176, 255, 0.25);
}

.profile-avatar.is-image {
    object-fit: cover;
    background: transparent;
}

.avatar-edit-overlay {
    position: absolute;
    inset: 0;
    border-radius: 18px;
    background: rgba(0, 0, 0, 0.45);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    color: #fff;
    opacity: 0;
    transition: opacity 0.15s;
}

.avatar-wrapper:hover .avatar-edit-overlay {
    opacity: 1;
}

.profile-status-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
    white-space: nowrap;
}

.profile-status-chip.is-enabled {
    background: rgba(74, 222, 128, 0.14);
    color: #16a34a;
}

.profile-status-chip.is-disabled {
    background: rgba(148, 163, 184, 0.14);
    color: var(--theme-text-soft);
}

body.dark .profile-status-chip.is-enabled {
    color: #86efac;
}

.profile-info-block {
    padding: 16px;
    border-radius: 16px;
    background: var(--theme-bg-elevated);
    border: 1px solid var(--theme-border);
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.profile-label-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.profile-label {
    font-size: 12px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    opacity: 0.55;
}

.pending-email-hint {
    margin: 0;
    font-size: 12px;
    opacity: 0.7;
    color: #fbbf24;
}

.verify-warning {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 14px 16px;
    border-radius: 14px;
    background: rgba(251, 146, 60, 0.1);
    border: 1px solid rgba(251, 146, 60, 0.32);
}

.verify-warning-icon {
    font-size: 22px;
    color: #fb923c;
    flex-shrink: 0;
    margin-top: 1px;
}

.verify-warning-title {
    margin: 0 0 2px;
    font-size: 14px;
    font-weight: 700;
    color: #fb923c;
}

.verify-warning-text {
    margin: 0;
    font-size: 13px;
    line-height: 1.4;
    opacity: 0.85;
}

.username-at-prefix {
    font-size: 15px;
    font-weight: 700;
    opacity: 0.55;
    margin-right: 2px;
}

.field-hint {
    margin: 0;
    font-size: 11px;
    opacity: 0.45;
}

.field-error {
    margin: 0;
    font-size: 12px;
    color: #f87171;
}

.sync-panel {
    padding: 18px;
    border-radius: 18px;
    background: rgba(67, 97, 176, 0.16);
    border: 1px solid rgba(107, 145, 255, 0.22);
}

.sync-footer {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 14px;
}

.sync-footer-item {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    border-radius: 999px;
    background: var(--theme-bg-soft);
    font-size: 12px;
    opacity: 0.82;
}

.sync-footer-item.is-active {
    background: rgba(74, 222, 128, 0.14);
    color: #15803d;
}

body.dark .sync-footer-item.is-active {
    color: #bbf7d0;
}

.sync-free-notice {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    margin-top: 12px;
    padding: 10px 12px;
    border-radius: 10px;
    background: rgba(216, 162, 58, 0.10);
    border: 1px solid rgba(216, 162, 58, 0.35);
    font-size: 12px;
    line-height: 1.4;
    color: #8a6314;
}

.sync-free-notice .iconify {
    flex-shrink: 0;
    margin-top: 1px;
    font-size: 15px;
}

body.dark .sync-free-notice {
    color: #e6b45a;
    background: rgba(216, 162, 58, 0.14);
}

/* ── Subscription card (Subscription / Sync / AI Assistant) ─────────────── */
.sub-card {
    border-radius: 18px;
    background: rgba(67, 97, 176, 0.10);
    border: 1px solid rgba(107, 145, 255, 0.20);
    overflow: hidden;
}

.sub-section {
    padding: 18px;
}

.sub-divider {
    height: 1px;
    background: rgba(107, 145, 255, 0.16);
}

.sub-head {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
}

.sub-head__icon {
    font-size: 18px;
    color: #d8a23a;
}

.sub-head__title {
    font-weight: 800;
}

.sub-blurb {
    margin: 0 0 14px;
    font-size: 13px;
    line-height: 1.4;
    opacity: 0.75;
}

.sub-billing {
    display: flex;
    align-items: center;
    gap: 7px;
    margin: -6px 0 14px;
    font-size: 12.5px;
    font-weight: 500;
    opacity: 0.85;
}

.sub-billing .iconify {
    font-size: 15px;
    opacity: 0.7;
}

.manage-elsewhere-note {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    margin-top: 12px;
    padding: 10px 12px;
    border-radius: 10px;
    background: rgba(216, 162, 58, 0.1);
    border: 1px solid rgba(216, 162, 58, 0.35);
    font-size: 12px;
    line-height: 1.4;
    color: #8a6314;
}

.manage-elsewhere-note .iconify {
    flex-shrink: 0;
    margin-top: 1px;
    font-size: 15px;
}

body.dark .manage-elsewhere-note {
    color: #e6b45a;
    background: rgba(216, 162, 58, 0.14);
}

.plan-pill {
    margin-left: auto;
    padding: 3px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 800;
    border: 1px solid transparent;
}

.plan-pill.tier-free {
    color: #94a3b8;
    background: rgba(148, 163, 184, 0.14);
    border-color: rgba(148, 163, 184, 0.30);
}

.plan-pill.tier-sync {
    color: #2e8b68;
    background: rgba(46, 139, 104, 0.16);
    border-color: rgba(46, 139, 104, 0.30);
}

.plan-pill.tier-pro {
    color: #8b5cf6;
    background: rgba(139, 92, 246, 0.16);
    border-color: rgba(139, 92, 246, 0.30);
}

.onoff-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 2px 9px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
    border: 1px solid transparent;
}

.onoff-chip .onoff-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: currentColor;
}

.onoff-chip.is-on {
    color: #2e8b68;
    background: rgba(46, 139, 104, 0.16);
    border-color: rgba(46, 139, 104, 0.30);
}

.onoff-chip.is-off {
    color: #b45353;
    background: rgba(180, 83, 83, 0.16);
    border-color: rgba(180, 83, 83, 0.30);
}

.sub-plan-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.sub-plan-loading {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    opacity: 0.8;
}

.sub-hint {
    margin: 4px 0 0;
    font-size: 12px;
    opacity: 0.7;
}

.sub-error {
    margin: 4px 0 0;
    font-size: 12px;
    color: #f87171;
}

.mb-2 {
    margin-bottom: 8px;
}

.mb-3 {
    margin-bottom: 12px;
}

.manage-portal-row {
    margin-top: 16px;
    text-align: center;
}

.pending-downgrade :deep(.n-button) {
    margin-left: 8px;
}

/* ── Plan comparison modal ─────────────────────────────────────────────── */
.plans-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
}

@media (max-width: 560px) {
    .plans-grid {
        grid-template-columns: 1fr;
    }
}

.plan-card {
    position: relative;
    display: flex;
    flex-direction: column;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid var(--theme-border, rgba(120, 130, 160, 0.3));
    background: var(--theme-bg-soft, rgba(120, 130, 160, 0.06));
}

.plan-card.is-highlight {
    border-color: rgba(216, 162, 58, 0.55);
    background: rgba(216, 162, 58, 0.08);
}

.plan-card__badge {
    position: absolute;
    top: -10px;
    left: 14px;
    padding: 2px 10px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
    color: #fff;
    background: #d8a23a;
}

.plan-card.is-current {
    border-color: rgba(99, 179, 117, 0.55);
    background: rgba(99, 179, 117, 0.08);
}

.plan-card__badge--current {
    background: #63b375;
}

.plan-card__name {
    font-size: 16px;
    font-weight: 800;
}

.plan-card__price {
    margin-top: 4px;
    font-size: 24px;
    font-weight: 800;
}

.plan-card__per {
    font-size: 13px;
    font-weight: 500;
    opacity: 0.6;
}

.plan-card__tagline {
    margin: 4px 0 12px;
    font-size: 12.5px;
    opacity: 0.7;
}

.plan-card__features {
    list-style: none;
    margin: 0 0 16px;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 9px;
    flex: 1;
}

.plan-card__features li {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    font-size: 13px;
    line-height: 1.35;
}

.plan-card__features li .iconify {
    flex-shrink: 0;
    margin-top: 2px;
    font-size: 15px;
    color: #2e8b68;
}

.danger-zone {
    border: 1px solid rgba(239, 68, 68, 0.4);
    border-radius: 16px;
    overflow: hidden;
}

.danger-zone-header {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 18px;
    background: rgba(239, 68, 68, 0.06);
    border: none;
    cursor: pointer;
    color: inherit;
    font-size: 14px;
    transition: background 0.15s;
}

.danger-zone-header:hover {
    background: rgba(239, 68, 68, 0.1);
}

.danger-zone-body {
    padding: 18px;
    border-top: 1px solid rgba(239, 68, 68, 0.2);
}

.denomination-panel {
    padding: 18px;
    border-radius: 18px;
    background: rgba(111, 132, 255, 0.08);
    border: 1px solid rgba(111, 132, 255, 0.2);
}

.required-badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 600;
    padding: 2px 7px;
    border-radius: 999px;
    background: rgba(251, 146, 60, 0.2);
    color: #fb923c;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Picture picker */
.picker-section-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    opacity: 0.55;
    margin-bottom: 10px;
}

.default-avatars-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 10px;
    margin-bottom: 4px;
}

.default-avatar-btn {
    position: relative;
    background: none;
    border: 2px solid transparent;
    border-radius: 14px;
    padding: 0;
    cursor: pointer;
    overflow: hidden;
    transition: border-color 0.15s, transform 0.1s;
    aspect-ratio: 1;
}

.default-avatar-btn img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 12px;
    display: block;
}

.default-avatar-btn:hover {
    border-color: rgba(111, 132, 255, 0.6);
    transform: scale(1.04);
}

.default-avatar-btn.is-selected {
    border-color: #6f84ff;
}

.avatar-check-icon {
    position: absolute;
    bottom: 4px;
    right: 4px;
    font-size: 18px;
    color: #6f84ff;
    background: rgba(0, 0, 0, 0.55);
    border-radius: 999px;
    padding: 1px;
}

/* Crop modal */
.crop-container {
    width: 100%;
    max-height: 400px;
    overflow: hidden;
    border-radius: 12px;
    background: #000;
}

.crop-source-img {
    display: block;
    max-width: 100%;
}
</style>
