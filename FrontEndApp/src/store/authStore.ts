import { defineStore } from 'pinia';
import { computed, ref, watch } from 'vue';
import axios from 'axios';
import { runSync, runPullSync, resetSyncBackoff } from '../util/Sync/sync';

const API_BASE_URL = `${import.meta.env.VITE_API_BASE_URL}/api`;

export interface UserInfo {
    id?: number;
    user_id?: number;
    denomination: string | null;
    profile_picture?: string | null;
}

export interface User {
    id: number;
    name: string;
    username?: string | null;
    email: string;
    pending_email?: string | null;
    sync_enabled: boolean;
    /** Server-verified subscription tier (RevenueCat webhook source of truth). */
    tier?: 'free' | 'sync' | 'pro';
    email_verified_at?: string;
    created_at?: string;
    updated_at?: string;
    info?: UserInfo | null;
}

export interface AuthTokens {
    token: string;
    refreshToken?: string;
}

export interface UserSettings {
    id?: number;
    selected_theme: string;
    is_dark: boolean;
    background_theme: string;
}

export const useAuthStore = defineStore('authStore', () => {
    const user = ref<User | null>(null);
    const token = ref<string | null>(null);
    const isAuthenticated = ref(false);
    const remoteSettings = ref<UserSettings | null>(null);

    // Server-verified subscription tier (authoritative; the backend also gates
    // every AI request). Drives entitlement gating in the AI views.
    const tier = computed<'free' | 'sync' | 'pro'>(() => user.value?.tier ?? 'free');
    const isAiEnabled = computed(() => tier.value !== 'free');

    // Local avatar cache — base64 data URL of the last uploaded custom picture.
    // Keyed by the profile_picture value so it auto-invalidates if the picture changes.
    const localAvatarKey  = ref<string | null>(localStorage.getItem('profile_avatar_key'));
    const localAvatarCache = ref<string | null>(localStorage.getItem('profile_avatar_data'));

    // Pending settings that failed to reach the server (e.g. offline).
    // Stored in localStorage so they survive app restarts.
    const pendingSettingsUpdate = ref<Partial<UserSettings> | null>(
        (() => {
            try { return JSON.parse(localStorage.getItem('pending_theme_settings') || 'null'); }
            catch { return null; }
        })()
    );

    // Pending sync_enabled preference (separate endpoint from theme settings).
    const pendingSyncEnabled = ref<boolean | null>(
        (() => {
            const v = localStorage.getItem('pending_sync_enabled');
            return v === null ? null : v === '1';
        })()
    );

    // Restore cached user from previous session so profile shows immediately offline.
    (() => {
        const savedUser = localStorage.getItem('cached_user');
        if (savedUser) {
            try { user.value = JSON.parse(savedUser); } catch {}
        }
    })();

    // Auto-persist user on every change so it's available offline on next launch.
    watch(user, (u) => {
        if (u) {
            localStorage.setItem('cached_user', JSON.stringify(u));
        } else {
            localStorage.removeItem('cached_user');
        }
    }, { deep: true });

    /**
     * Register a new user
     */
    async function register(
        name: string,
        username: string,
        email: string,
        password: string,
        passwordConfirmation: string,
        denomination?: string | null
    ): Promise<{ success: boolean; message: string; user?: User; token?: string }> {
        try {
            const response = await axios.post(`${API_BASE_URL}/auth/register`, {
                name,
                username,
                email,
                password,
                password_confirmation: passwordConfirmation,
                ...(denomination ? { denomination } : {}),
            });

            if (response.data.status === 'success') {
                return {
                    success: true,
                    message: response.data.message,
                };
            }

            return { success: false, message: 'Registration failed' };
        } catch (error: any) {
            console.error('Registration error:', error);
            return {
                success: false,
                message: error.response?.data?.message || error.message || 'Registration failed',
            };
        }
    }

    /**
     * Login user
     */
    async function login(
        email: string,
        password: string
    ): Promise<{ success: boolean; message: string; user?: User; token?: string }> {
        try {
            const response = await axios.post(`${API_BASE_URL}/auth/login`, {
                email,
                password,
            });

            if (response.data.status === 'success') {
                user.value = response.data.user;
                token.value = response.data.token;
                isAuthenticated.value = true;
                syncEnabled.value = response.data.user.sync_enabled === true;

                localStorage.setItem('auth_token', response.data.token);

                // Load remote settings after login (fire-and-forget)
                loadSettings();

                return {
                    success: true,
                    message: response.data.message,
                    user: response.data.user,
                    token: response.data.token,
                };
            }

            return { success: false, message: 'Login failed' };
        } catch (error: any) {
            console.error('Login error:', error);
            return {
                success: false,
                message: error.response?.data?.message || error.message || 'Invalid credentials',
            };
        }
    }

    /**
     * Delete the authenticated user's account.
     * Requires email confirmation matching the current user's email.
     */
    async function deleteAccount(email: string): Promise<{ success: boolean; message: string }> {
        const currentToken = token.value;
        if (!currentToken) return { success: false, message: 'Not authenticated' };

        try {
            const response = await axios.delete(`${API_BASE_URL}/auth/account`, {
                headers: { Authorization: `Bearer ${currentToken}` },
                data: { email },
            });

            if (response.data.status === 'success') {
                user.value = null;
                token.value = null;
                isAuthenticated.value = false;
                syncEnabled.value = false;
                remoteSettings.value = null;
                pendingSettingsUpdate.value = null;
                pendingSyncEnabled.value = null;
                localAvatarKey.value   = null;
                localAvatarCache.value = null;
                localStorage.removeItem('auth_token');
                localStorage.removeItem('pending_theme_settings');
                localStorage.removeItem('pending_sync_enabled');
                localStorage.removeItem('cached_user');
                localStorage.removeItem('profile_avatar_key');
                localStorage.removeItem('profile_avatar_data');
                return { success: true, message: response.data.message };
            }

            return { success: false, message: response.data.message || 'Failed to delete account' };
        } catch (error: any) {
            return {
                success: false,
                message: error.response?.data?.message || error.message || 'Failed to delete account',
            };
        }
    }

    /**
     * Logout user
     */
    async function logout(): Promise<{ success: boolean; message: string }> {
        const currentToken = token.value;

        // Always clear local state immediately
        user.value = null;
        token.value = null;
        isAuthenticated.value = false;
        syncEnabled.value = false;
        remoteSettings.value = null;
        pendingSettingsUpdate.value = null;
        pendingSyncEnabled.value = null;
        localAvatarKey.value   = null;
        localAvatarCache.value = null;
        localStorage.removeItem('auth_token');
        localStorage.removeItem('pending_theme_settings');
        localStorage.removeItem('pending_sync_enabled');
        localStorage.removeItem('cached_user');
        localStorage.removeItem('profile_avatar_key');
        localStorage.removeItem('profile_avatar_data');

        if (!currentToken) {
            return { success: false, message: 'No token to logout' };
        }

        try {
            await axios.post(`${API_BASE_URL}/auth/logout`, {}, {
                headers: { Authorization: `Bearer ${currentToken}` },
            });
            return { success: true, message: 'Logged out successfully' };
        } catch (error: any) {
            console.error('Logout error:', error);
            return {
                success: false,
                message: error.response?.data?.message || error.message || 'Logout failed',
            };
        }
    }

    let getUserPromise: Promise<User | null> | null = null;

    /**
     * Get current user info.
     * Only clears auth state on 401/403 — network errors keep existing state
     * so the user is not logged out when offline.
     */
    function getUser(forceRefresh = false): Promise<User | null> {
        if (!forceRefresh && user.value) return Promise.resolve(user.value);
        if (!token.value) return Promise.resolve(null);

        if (getUserPromise) return getUserPromise;

        getUserPromise = axios.get(`${API_BASE_URL}/auth/user`, {
            headers: { Authorization: `Bearer ${token.value}` },
        }).then((response) => {
            if (response.data.status === 'success') {
                user.value = response.data.user;
                syncEnabled.value = response.data.user.sync_enabled === true;
                return response.data.user as User;
            }
            return null;
        }).catch((error: any) => {
            console.error('Get user error:', error);
            const status = error?.response?.status;
            if (status === 401 || status === 403) {
                // Token invalid — clear auth
                user.value = null;
                token.value = null;
                isAuthenticated.value = false;
                localStorage.removeItem('auth_token');
            }
            // Network errors: keep existing auth state — user is just offline
            return null;
        }).finally(() => {
            getUserPromise = null;
        });

        return getUserPromise;
    }

    // Guard against concurrent flush calls (e.g. focus + online firing together)
    let isFlushing = false;

    /**
     * Flush any pending settings/preferences to the backend.
     * Called on reconnect, focus, and before loadSettings.
     */
    async function flushPendingSettings(): Promise<boolean> {
        if (isFlushing || !token.value) return false;
        if (!pendingSettingsUpdate.value && pendingSyncEnabled.value === null) return false;

        isFlushing = true;
        let allFlushed = true;

        try {
            // Flush theme settings
            if (pendingSettingsUpdate.value) {
                try {
                    const response = await axios.patch(`${API_BASE_URL}/settings`, pendingSettingsUpdate.value, {
                        headers: { Authorization: `Bearer ${token.value}` },
                    });
                    if (response.data.status === 'success') {
                        remoteSettings.value = response.data.settings;
                        pendingSettingsUpdate.value = null;
                        localStorage.removeItem('pending_theme_settings');
                    } else {
                        allFlushed = false;
                    }
                } catch {
                    allFlushed = false; // Still offline
                }
            }

            // Flush sync_enabled preference
            if (pendingSyncEnabled.value !== null) {
                try {
                    const response = await axios.patch(
                        `${API_BASE_URL}/auth/preferences`,
                        { sync_enabled: pendingSyncEnabled.value },
                        { headers: { Authorization: `Bearer ${token.value}` } }
                    );
                    if (response.data.status === 'success') {
                        user.value = response.data.user;
                        pendingSyncEnabled.value = null;
                        localStorage.removeItem('pending_sync_enabled');
                    } else {
                        allFlushed = false;
                    }
                } catch {
                    allFlushed = false; // Still offline
                }
            }
        } finally {
            isFlushing = false;
        }

        return allFlushed;
    }

    /**
     * Load user settings from the backend.
     * Flushes any pending local changes first — local always wins.
     */
    async function loadSettings(): Promise<UserSettings | null> {
        if (!token.value) return null;

        // Pending local changes take priority — flush before pulling server state
        if (pendingSettingsUpdate.value) {
            await flushPendingSettings();
            return remoteSettings.value;
        }

        try {
            const response = await axios.get(`${API_BASE_URL}/settings`, {
                headers: { Authorization: `Bearer ${token.value}` },
            });
            if (response.data.status === 'success') {
                remoteSettings.value = response.data.settings;
                return response.data.settings as UserSettings;
            }
        } catch {
            // Offline — keep using local settings, no change to remoteSettings
        }
        return null;
    }

    /**
     * Persist theme settings to the backend.
     * Queues the update locally so it survives offline scenarios.
     */
    async function updateSettings(data: Partial<UserSettings>): Promise<void> {
        if (!token.value) return;

        // Merge into pending so rapid changes collapse into one request
        const merged = { ...(pendingSettingsUpdate.value ?? {}), ...data };
        pendingSettingsUpdate.value = merged;
        localStorage.setItem('pending_theme_settings', JSON.stringify(merged));

        if (isFlushing) return; // A flush is already in progress — pending will be sent then

        try {
            const response = await axios.patch(`${API_BASE_URL}/settings`, merged, {
                headers: { Authorization: `Bearer ${token.value}` },
            });
            if (response.data.status === 'success') {
                remoteSettings.value = response.data.settings;
                pendingSettingsUpdate.value = null;
                localStorage.removeItem('pending_theme_settings');
            }
        } catch {
            // Offline — pending saved to localStorage, will flush on reconnect/focus
        }
    }

    /**
     * Initialize auth state from localStorage.
     */
    function initAuth() {
        const savedToken = localStorage.getItem('auth_token');
        if (savedToken) {
            token.value = savedToken;
            isAuthenticated.value = true;
            // Load sync preference from local IPC store so syncEnabled is correct
            // even if the network is down and getUser() fails.
            loadSyncEnabled();
            getUser(true).then((u) => {
                if (u) loadSettings();
            });
        }

        // On reconnect: flush pending changes then pull fresh settings
        window.addEventListener('online', onOnline);

        // On app quit: push any unsynced changes before closing
        window.browserWindow.onSyncBeforeQuit(async () => {
            try {
                await runSync();
            } finally {
                window.browserWindow.notifySyncBeforeQuitDone();
            }
        });
    }

    function cleanupListeners() {
        window.removeEventListener('online', onOnline);
    }

    async function onOnline() {
        if (!isAuthenticated.value) return;
        // If we were offline at startup, user may be null and syncEnabled may be stale.
        if (!user.value) {
            const u = await getUser();
            if (u) loadSettings();
        }
        await flushPendingSettings();
        if (!pendingSettingsUpdate.value) loadSettings();
        // Clear backoff so reconnect triggers an immediate sync rather than waiting
        // out a cooldown that was set during the offline period.
        if (syncEnabled.value) {
            resetSyncBackoff();
            runSync();
        }
    }

    /**
     * Whether syncing is enabled
     */
    const syncEnabled = ref(false);
    const lastSyncAt = ref<string | null>(null);
    let syncInterval: ReturnType<typeof setInterval> | null = null;
    let lastFocusPullAt = 0;

    function startSyncInterval() {
        if (syncInterval) return;
        // On login/startup: push any pending local changes, then pull remote state
        flushPendingSettings().then(() => runSync());
        // Periodic pull-only every 5 minutes — never auto-pushes without user action
        syncInterval = setInterval(runPullSync, 5 * 60 * 1_000);
        window.addEventListener('focus', onFocus);
    }

    async function onFocus() {
        // Throttle: don't pull more than once per minute on focus
        const now = Date.now();
        if (now - lastFocusPullAt < 60_000) return;
        lastFocusPullAt = now;
        await flushPendingSettings();
        runPullSync();
    }

    function stopSyncInterval() {
        if (syncInterval) {
            clearInterval(syncInterval);
            syncInterval = null;
        }
        window.removeEventListener('focus', onFocus);
    }

    async function loadLastSyncAt() {
        try {
            const ts = await window.browserWindow.getLastSyncTimestamp();
            lastSyncAt.value = ts && ts !== '0' ? ts : null;
        } catch {
            // best-effort
        }
    }

    async function loadSyncEnabled() {
        try {
            const value = await window.browserWindow.getSyncSetting('sync_enabled');
            syncEnabled.value = value === '1' || value === 1 || value === true;
        } catch {
            syncEnabled.value = false;
        }
    }

    /**
     * Toggle cloud sync on/off.
     * Queues the preference locally so it's not lost if offline.
     */
    async function setSyncEnabled(enabled: boolean) {
        syncEnabled.value = enabled;

        try {
            await window.browserWindow.setSyncSetting('sync_enabled', enabled ? '1' : '0');
        } catch {
            // best-effort
        }

        // Save to pending in case we're offline
        pendingSyncEnabled.value = enabled;
        localStorage.setItem('pending_sync_enabled', enabled ? '1' : '0');

        if (token.value) {
            try {
                const response = await axios.patch(
                    `${API_BASE_URL}/auth/preferences`,
                    { sync_enabled: enabled },
                    { headers: { Authorization: `Bearer ${token.value}` } }
                );
                if (response.data.status === 'success') {
                    user.value = response.data.user;
                    pendingSyncEnabled.value = null;
                    localStorage.removeItem('pending_sync_enabled');
                }
            } catch {
                // Offline — pending saved, will flush on reconnect
            }
        }
    }

    watch(syncEnabled, (enabled) => {
        if (enabled && isAuthenticated.value) {
            startSyncInterval();
        } else {
            stopSyncInterval();
        }
    });

    watch(isAuthenticated, (authenticated) => {
        if (!authenticated) {
            stopSyncInterval();
            cleanupListeners();
        } else if (syncEnabled.value) {
            startSyncInterval();
        }
    });

    async function forgotPassword(email: string): Promise<{ success: boolean; message: string }> {
        try {
            const response = await axios.post(`${API_BASE_URL}/auth/forgot-password`, { email });
            return {
                success: response.data.status === 'success',
                message: response.data.message ?? 'Failed to send reset link',
            };
        } catch (error: any) {
            return {
                success: false,
                message: error.response?.data?.message || error.message || 'Failed to send reset link',
            };
        }
    }

    async function updateProfile(
        data: { name?: string; username?: string; email?: string }
    ): Promise<{ success: boolean; message?: string; emailVerificationSent?: boolean }> {
        if (!token.value) return { success: false, message: 'Not authenticated' };
        try {
            const response = await axios.patch(`${API_BASE_URL}/auth/profile`, data, {
                headers: { Authorization: `Bearer ${token.value}` },
            });
            if (response.data.status === 'success') {
                user.value = response.data.user;
                return { success: true, emailVerificationSent: response.data.email_verification_sent === true };
            }
            return { success: false, message: 'Failed to update profile' };
        } catch (error: any) {
            const validationErrors = error.response?.data?.errors;
            const firstError = validationErrors
                ? Object.values(validationErrors).flat()[0] as string
                : null;
            return {
                success: false,
                message: firstError || error.response?.data?.message || error.message || 'Failed to update profile',
            };
        }
    }

    async function updateUserInfo(
        data: { denomination?: string | null }
    ): Promise<{ success: boolean; message?: string }> {
        if (!token.value) return { success: false, message: 'Not authenticated' };
        try {
            const response = await axios.patch(`${API_BASE_URL}/user-info`, data, {
                headers: { Authorization: `Bearer ${token.value}` },
            });
            if (response.data.status === 'success') {
                if (user.value) {
                    user.value = { ...user.value, info: response.data.info };
                }
                return { success: true };
            }
            return { success: false, message: 'Failed to update info' };
        } catch (error: any) {
            return {
                success: false,
                message: error.response?.data?.message || error.message || 'Failed to update info',
            };
        }
    }

    function fileToDataUrl(file: File): Promise<string> {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload  = (e) => resolve(e.target!.result as string);
            reader.onerror = () => reject(new Error('FileReader failed'));
            reader.readAsDataURL(file);
        });
    }

    /**
     * Set profile picture.
     * For default app pictures pass `{ type: 'default', name: 'app_profile1.png' }`.
     * For custom uploads pass `{ type: 'upload', file: File }` — the file must
     * already be compressed to < 60 KB by the caller.
     */
    async function updateProfilePicture(
        payload: { type: 'default'; name: string } | { type: 'upload'; files: Record<number, File> }
    ): Promise<{ success: boolean; message?: string; profile_picture?: string }> {
        if (!token.value) return { success: false, message: 'Not authenticated' };

        try {
            const form = new FormData();
            form.append('type', payload.type);
            if (payload.type === 'default') {
                form.append('name', payload.name);
            } else {
                for (const [size, file] of Object.entries(payload.files)) {
                    form.append(`image_${size}`, file);
                }
            }

            const response = await axios.post(`${API_BASE_URL}/user-info/profile-picture`, form, {
                headers: {
                    Authorization: `Bearer ${token.value}`,
                    'Content-Type': 'multipart/form-data',
                },
            });

            if (response.data.status === 'success') {
                if (user.value) {
                    user.value = { ...user.value, info: response.data.info };
                }

                if (payload.type === 'upload') {
                    // Cache the 400px version locally so it shows offline next launch.
                    try {
                        const file400 = payload.files[400];
                        if (file400) {
                            const dataUrl = await fileToDataUrl(file400);
                            localAvatarKey.value   = response.data.profile_picture;
                            localAvatarCache.value = dataUrl;
                            localStorage.setItem('profile_avatar_key',  response.data.profile_picture);
                            localStorage.setItem('profile_avatar_data', dataUrl);
                        }
                    } catch { /* non-critical */ }
                } else {
                    // Switched to a default avatar — clear any old custom cache.
                    localAvatarKey.value   = null;
                    localAvatarCache.value = null;
                    localStorage.removeItem('profile_avatar_key');
                    localStorage.removeItem('profile_avatar_data');
                }

                return { success: true, profile_picture: response.data.profile_picture };
            }
            return { success: false, message: 'Failed to update profile picture' };
        } catch (error: any) {
            return {
                success: false,
                message: error.response?.data?.message || error.message || 'Failed to update profile picture',
            };
        }
    }

    async function resendVerification(): Promise<{ success: boolean; message: string; alreadyVerified?: boolean }> {
        if (!token.value) return { success: false, message: 'Not authenticated' };
        try {
            const response = await axios.post(`${API_BASE_URL}/auth/resend-verification`, {}, {
                headers: { Authorization: `Bearer ${token.value}` },
            });
            return {
                success: response.data.status === 'success',
                message: response.data.message ?? 'Verification email sent.',
                alreadyVerified: response.data.already_verified === true,
            };
        } catch (error: any) {
            return {
                success: false,
                message: error.response?.data?.message || error.message || 'Failed to send verification email',
            };
        }
    }

    async function resetPassword(
        token: string,
        email: string,
        password: string,
        passwordConfirmation: string,
    ): Promise<{ success: boolean; message: string }> {
        try {
            const response = await axios.post(`${API_BASE_URL}/auth/reset-password`, {
                token,
                email,
                password,
                password_confirmation: passwordConfirmation,
            });
            return {
                success: response.data.status === 'success',
                message: response.data.message ?? 'Failed to reset password',
            };
        } catch (error: any) {
            return {
                success: false,
                message: error.response?.data?.message || error.message || 'Failed to reset password',
            };
        }
    }

    return {
        user,
        token,
        tier,
        isAiEnabled,
        isAuthenticated,
        syncEnabled,
        lastSyncAt,
        loadLastSyncAt,
        remoteSettings,
        pendingSettingsUpdate,
        pendingSyncEnabled,
        register,
        login,
        logout,
        deleteAccount,
        getUser,
        initAuth,
        loadSyncEnabled,
        setSyncEnabled,
        loadSettings,
        updateSettings,
        flushPendingSettings,
        localAvatarKey,
        localAvatarCache,
        forgotPassword,
        resetPassword,
        updateProfile,
        updateUserInfo,
        updateProfilePicture,
        resendVerification,
    };
});
