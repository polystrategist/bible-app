import { defineStore } from 'pinia';
import { ref, watch } from 'vue';
import axios from 'axios';
import { runSync } from '../util/Sync/sync';

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

export const useAuthStore = defineStore('authStore', () => {
    const user = ref<User | null>(null);
    const token = ref<string | null>(null);
    const isAuthenticated = ref(false);

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
                
                // Store token in localStorage for persistence
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

                // Store token in localStorage
                localStorage.setItem('auth_token', response.data.token);

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
     * Logout user
     */
    async function logout(): Promise<{ success: boolean; message: string }> {
        const currentToken = token.value;

        // Always clear local state immediately
        user.value = null;
        token.value = null;
        isAuthenticated.value = false;
        syncEnabled.value = false;
        localStorage.removeItem('auth_token');

        if (!currentToken) {
            return { success: false, message: 'No token to logout' };
        }

        try {
            await axios.post(`${API_BASE_URL}/auth/logout`, {}, {
                headers: {
                    Authorization: `Bearer ${currentToken}`,
                },
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
     * Get current user info
     */
    function getUser(): Promise<User | null> {
        if (user.value) return Promise.resolve(user.value);
        if (!token.value) return Promise.resolve(null);

        // Deduplicate concurrent calls — return the in-flight promise if one exists
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
            user.value = null;
            token.value = null;
            isAuthenticated.value = false;
            localStorage.removeItem('auth_token');
            return null;
        }).finally(() => {
            getUserPromise = null;
        });

        return getUserPromise;
    }

    /**
     * Initialize auth state from localStorage
     */
    function initAuth() {
        const savedToken = localStorage.getItem('auth_token');
        if (savedToken) {
            token.value = savedToken;
            isAuthenticated.value = true;
            // Fetch user info
            getUser();
        }
    }

    /**
     * Whether syncing is enabled (persisted via sync_settings table)
     */
    const syncEnabled = ref(false);
    let syncInterval: ReturnType<typeof setInterval> | null = null;

    function startSyncInterval() {
        if (syncInterval) return;
        runSync(); // run immediately on enable
        syncInterval = setInterval(runSync, 30_000);
        window.addEventListener('focus', runSync);
    }

    function stopSyncInterval() {
        if (syncInterval) {
            clearInterval(syncInterval);
            syncInterval = null;
        }
        window.removeEventListener('focus', runSync);
    }

    async function loadSyncEnabled() {
        try {
            const value = await window.browserWindow.getSyncSetting('sync_enabled');
            syncEnabled.value = value === '1' || value === 1 || value === true;
        } catch {
            syncEnabled.value = false;
        }
    }

    async function setSyncEnabled(enabled: boolean) {
        syncEnabled.value = enabled;
        // Persist locally
        try {
            await window.browserWindow.setSyncSetting('sync_enabled', enabled ? '1' : '0');
        } catch {
            // best-effort
        }
        // Persist to backend (source of truth)
        if (token.value) {
            try {
                const response = await axios.patch(`${API_BASE_URL}/auth/preferences`, { sync_enabled: enabled }, {
                    headers: { Authorization: `Bearer ${token.value}` },
                });
                if (response.data.status === 'success') {
                    user.value = response.data.user;
                }
            } catch {
                // best-effort — local state is already updated
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
        if (!authenticated) stopSyncInterval();
        else if (syncEnabled.value) startSyncInterval();
    });

    return {
        user,
        token,
        isAuthenticated,
        syncEnabled,
        register,
        login,
        logout,
        getUser,
        initAuth,
        loadSyncEnabled,
        setSyncEnabled,
    };
});
