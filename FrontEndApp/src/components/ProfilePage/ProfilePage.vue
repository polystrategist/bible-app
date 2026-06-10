<script lang="ts" setup>
import { NAlert, NButton, NForm, NInput, NModal, NSelect, NSpin, useMessage } from 'naive-ui';
import { computed, ref, watch, nextTick, onMounted, onBeforeUnmount } from 'vue';
import { useAuthStore } from '../../store/authStore';
import { useMainStore } from '../../store/main';
import { useWebBillingStore } from '../../store/webBillingStore';
import { usePlanModalStore } from '../../store/planModalStore';
import { useSubscriptionPlans } from '../../composables/useSubscriptionPlans';
import SubscriptionSections from '../SubscriptionSections.vue';
import { Icon } from '@iconify/vue';
import { useRouter } from 'vue-router';
import { DENOMINATION_OPTIONS, normalizeDenominationCode } from '../../util/denominations';
import Cropper from 'cropperjs';
import 'cropperjs/dist/cropper.css';
import { DEFAULT_PROFILE_NAMES, getDefaultProfileUrl, useAvatarUrl } from '../../util/avatar';

const loading = ref(false);
const authStore = useAuthStore();
const mainStore = useMainStore();
const webBilling = useWebBillingStore();
const planModal = usePlanModalStore();
const message = useMessage();
const router = useRouter();

// ─── Subscription card (mirrors the mobile SubscriptionCard) ─────────────────
// "Choose your plan" is the global PlanModal (App.vue), opened via planModal.
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

// Plan cards + prices come from the shared composable (single source of truth,
// with fallback prices so a price always shows even when offerings aren't loaded).
const { syncPrice, proPrice } = useSubscriptionPlans();

const subPrice = computed(() => {
    if (authStore.tier === 'pro') return `${proPrice.value}/month`;
    if (authStore.tier === 'sync') return `${syncPrice.value}/month`;
    return null;
});

// "View plans" opens the global Choose-your-plan dialog (PlanModal in App.vue).
function viewPlans() {
    planModal.show();
}

// Open the in-app plan-management modal (subscribers), preloading plans.
async function openManage() {
    manageModalOpen.value = true;
    if (webBilling.plans.length === 0) await webBilling.loadPlans();
}

// Open the subscription manager when the dropdown's "Manage subscription" asks
// for it (subscribers → manage modal; Free → plan picker). `immediate` covers
// the case where this page mounts after the flag was set during navigation.
watch(
    () => mainStore.openSubscriptionRequested,
    (requested) => {
        if (!requested) return;
        mainStore.openSubscriptionRequested = false;
        if (authStore.tier === 'free') void viewPlans();
        else void openManage();
    },
    { immediate: true },
);

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
const checkingVerification = ref(false);

// Re-fetch the account so a just-completed verification (done in the browser)
// is picked up without restarting the app.
async function checkVerification() {
    checkingVerification.value = true;
    await authStore.getUser(true);
    checkingVerification.value = false;
    if (isEmailVerified.value) {
        message.success('Your email is now verified.');
    } else {
        message.info('Still not verified. Click the link in the email, then refresh.');
    }
}

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
                <div class="verify-warning-actions">
                    <NButton
                        size="small"
                        :loading="checkingVerification"
                        :disabled="checkingVerification"
                        @click="checkVerification"
                    >
                        <template #icon><Icon icon="mdi:refresh" /></template>
                        Refresh
                    </NButton>
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

                </div>

                <div class="sub-divider" />

                <SubscriptionSections />
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

        <!-- "Choose your plan" is the global PlanModal, mounted in App.vue. -->

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
            <div v-else class="sub-card">
                <SubscriptionSections @purchased="manageModalOpen = false" />
            </div>
            <p v-if="webBilling.error" class="sub-error">{{ webBilling.error }}</p>
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
    flex-wrap: wrap;
    gap: 12px;
    padding: 14px 16px;
    border-radius: 14px;
    background: rgba(251, 146, 60, 0.1);
    border: 1px solid rgba(251, 146, 60, 0.32);
}

/* Keep the message readable; when it can't fit alongside the buttons the
   actions wrap to their own row instead of squeezing the text. */
.verify-warning .flex-1 {
    min-width: 220px;
}

.verify-warning-icon {
    font-size: 22px;
    color: #fb923c;
    flex-shrink: 0;
    margin-top: 1px;
}

.verify-warning-actions {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
    margin-left: auto;
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

.sub-features {
    list-style: none;
    padding: 0;
    margin: 0 0 14px;
    display: flex;
    flex-direction: column;
    gap: 7px;
}
.sub-features li {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    font-size: 13px;
    line-height: 1.35;
    opacity: 0.9;
}
.sub-features li .iconify {
    margin-top: 2px;
    color: #2e8b68;
    flex-shrink: 0;
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
