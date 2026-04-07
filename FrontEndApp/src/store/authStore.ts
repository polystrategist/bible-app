import { defineStore } from 'pinia';
import { ref, watch } from 'vue';
import axios from 'axios';
import { runSync, runPullSync } from '../util/Sync/sync';

const API_BASE_URL = `${import.meta.env.VITE_API_BASE_URL}/api`;

export interface User {
    id: number;
    name: string;
    email: string;
    sync_enabled: boolean;
    email_verified_at?: string;
    created_at?: string;
    updated_at?: string;
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

    /**
     * Register a new user
     */
    async function register(
        name: string,
        email: string,
        password: string,
        passwordConfirmation: string
    ): Promise<{ success: boolean; message: string; user?: User; token?: string }> {
        try {
            const response = await axios.post(`${API_BASE_URL}/auth/register`, {
                name,
                email,
                password,
                password_confirmation: passwordConfirmation,
            });

            if (response.data.status === 'success') {
                user.value = response.data.user;
                token.value = response.data.token;
                isAuthenticated.value = true;

                localStorage.setItem('auth_token', response.data.token);

                return {
                    success: true,
                    message: response.data.message,
                    user: response.data.user,
                    token: response.data.token,
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
                localStorage.removeItem('auth_token');
                localStorage.removeItem('pending_theme_settings');
                localStorage.removeItem('pending_sync_enabled');
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
        localStorage.removeItem('auth_token');
        localStorage.removeItem('pending_theme_settings');
        localStorage.removeItem('pending_sync_enabled');

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
    function getUser(): Promise<User | null> {
        if (user.value) return Promise.resolve(user.value);
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
            getUser().then((u) => {
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
        await flushPendingSettings();
        if (!pendingSettingsUpdate.value) loadSettings();
        // Push all accumulated offline changes and pull any remote changes.
        if (syncEnabled.value) runSync();
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
        if (enabled) {
            return;
        }

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

    return {
        user,
        token,
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
    };
});
