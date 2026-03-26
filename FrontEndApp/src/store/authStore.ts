import { defineStore } from 'pinia';
import { ref } from 'vue';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export interface User {
    id: number;
    name: string;
    email: string;
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
        if (!token.value) {
            return { success: false, message: 'No token to logout' };
        }

        try {
            await axios.post(`${API_BASE_URL}/auth/logout`, {}, {
                headers: {
                    Authorization: `Bearer ${token.value}`,
                },
            });

            user.value = null;
            token.value = null;
            isAuthenticated.value = false;
            localStorage.removeItem('auth_token');
            
            return { success: true, message: 'Logged out successfully' };
        } catch (error: any) {
            console.error('Logout error:', error);
            // Clear local state even if API call fails
            user.value = null;
            token.value = null;
            isAuthenticated.value = false;
            localStorage.removeItem('auth_token');
            
            return {
                success: false,
                message: error.response?.data?.message || error.message || 'Logout failed',
            };
        }
    }

    /**
     * Get current user info
     */
    async function getUser(): Promise<User | null> {
        if (!token.value) {
            return null;
        }

        try {
            const response = await axios.get(`${API_BASE_URL}/auth/user`, {
                headers: {
                    Authorization: `Bearer ${token.value}`,
                },
            });

            if (response.data.status === 'success') {
                user.value = response.data.user;
                return response.data.user;
            }
            
            return null;
        } catch (error: any) {
            console.error('Get user error:', error);
            // Token might be invalid
            user.value = null;
            token.value = null;
            isAuthenticated.value = false;
            localStorage.removeItem('auth_token');
            return null;
        }
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
     * Check if user is synced
     */
    const syncData = ref(false);

    function toggleSync() {
        syncData.value = !syncData.value;
    }

    return {
        user,
        token,
        isAuthenticated,
        syncData,
        register,
        login,
        logout,
        getUser,
        initAuth,
        toggleSync,
    };
});
