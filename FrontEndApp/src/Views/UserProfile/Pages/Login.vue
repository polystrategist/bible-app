<script lang="ts" setup>
import { NButton, NInput, NSelect, useMessage } from 'naive-ui';
import { onMounted, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../../store/authStore';
import { DENOMINATION_OPTIONS } from '../../../util/denominations';

type View = 'login' | 'register' | 'forgot' | 'reset';

const view = ref<View>('login');
const loading = ref(false);
const successMessage = ref<string | null>(null);
const authStore = useAuthStore();
const router = useRouter();
const message = useMessage();

const selectScrollbarProps = { trigger: 'none' as const };

const form = reactive({
    email: null as string | null,
    password: null as string | null,
    retypePassword: null as string | null,
    name: null as string | null,
    username: null as string | null,
    denomination: null as string | null,
    resetToken: null as string | null,
    newPassword: null as string | null,
    newPasswordConfirm: null as string | null,
});

async function login() {
    if (!form.email || !form.password) {
        message.error('Cant Continue, some fields does not exist.');
        return;
    }
    loading.value = true;
    const result = await authStore.login(form.email, form.password);
    loading.value = false;
    if (!result.success) { message.error(result.message); return; }
    message.success('Logged In! Successfully.');
    await router.push(window.isElectron ? '/profile/profile' : '/');
}

async function register() {
    if (!form.email || !form.password || !form.name || !form.username) {
        message.error('Cant Continue, some fields does not exist.');
        return;
    }
    if (!/^[a-z0-9_]{3,30}$/.test(form.username)) {
        message.error('Username must be 3–30 characters: lowercase letters, numbers, and underscores only.');
        return;
    }
    if (form.password !== form.retypePassword) {
        message.error('Password and retype password should be the same.');
        return;
    }
    if (!form.denomination) {
        message.error('Please select your denomination.');
        return;
    }
    loading.value = true;
    const result = await authStore.register(form.name, form.username, form.email, form.password, form.retypePassword!, form.denomination);
    loading.value = false;
    if (!result.success) { message.error(result.message); return; }
    message.success('Registered! Successfully.');
    await router.push(window.isElectron ? '/profile/profile' : '/');
}

async function sendResetLink() {
    if (!form.email) {
        message.error('Please enter your email address.');
        return;
    }
    loading.value = true;
    const result = await authStore.forgotPassword(form.email);
    loading.value = false;
    if (!result.success) { message.error(result.message); return; }
    successMessage.value = 'Reset password link sent to your email.';
    view.value = 'login';
}

async function doResetPassword() {
    if (!form.email || !form.resetToken || !form.newPassword) {
        message.error('Please fill in all fields.');
        return;
    }
    if (form.newPassword !== form.newPasswordConfirm) {
        message.error('Passwords do not match.');
        return;
    }
    loading.value = true;
    const result = await authStore.resetPassword(
        form.resetToken,
        form.email,
        form.newPassword,
        form.newPasswordConfirm!,
    );
    loading.value = false;
    if (!result.success) { message.error(result.message); return; }
    message.success('Password reset! You can now sign in.');
    view.value = 'login';
    form.resetToken = null;
    form.newPassword = null;
    form.newPasswordConfirm = null;
}

async function submit() {
    if (view.value === 'register') await register();
    else if (view.value === 'forgot') await sendResetLink();
    else if (view.value === 'reset') await doResetPassword();
    else await login();
}

onMounted(async () => {
    if (authStore.isAuthenticated) {
        await router.push(window.isElectron ? '/profile/profile' : '/');
    }
});
</script>

<template>
    <div class="login-page">
        <div class="login-card">
            <!-- Branding -->
            <div class="login-brand">
                <img src="/logo.svg" alt="Believers Sword" class="login-logo" />
                <span class="login-app-name">Believers Sword</span>
            </div>

            <!-- Title -->
            <h2 class="login-title">
                <template v-if="view === 'login'">Sign In</template>
                <template v-else-if="view === 'register'">Create Account</template>
                <template v-else-if="view === 'forgot'">Forgot Password</template>
                <template v-else>Reset Password</template>
            </h2>
            <p class="login-desc">
                <template v-if="view === 'login'">{{ $t('sign-in-desc') }}</template>
                <template v-else-if="view === 'register'">{{ $t('sign-in-desc') }}</template>
                <template v-else-if="view === 'forgot'">Enter your email and we'll send you a reset link.</template>
                <template v-else>
                    Check your email for the reset link. Copy the token from the URL and paste it below.
                </template>
            </p>

            <div class="login-form">
                <!-- Success banner (e.g. after forgot password) -->
                <div v-if="successMessage && view === 'login'" class="login-success">
                    {{ successMessage }}
                </div>

                <!-- Register: name + username fields -->
                <template v-if="view === 'register'">
                    <label class="login-label">Full Name</label>
                    <NInput v-model:value="form.name" placeholder="Your name" size="large" @keydown.enter="submit" />
                    <label class="login-label">Username</label>
                    <NInput
                        v-model:value="form.username"
                        placeholder="e.g. john_doe"
                        size="large"
                        @keydown.enter="submit"
                        @input="form.username = (form.username ?? '').toLowerCase().replace(/[^a-z0-9_]/g, '')"
                    >
                        <template #prefix><span class="username-at">@</span></template>
                    </NInput>
                    <p class="login-hint">3–30 chars · lowercase letters, numbers, underscores only</p>
                </template>

                <!-- Email (all views) -->
                <label class="login-label">{{ $t('Email Address:') }}</label>
                <NInput v-model:value="form.email" :placeholder="$t('Email')" size="large" @keydown.enter="submit" />

                <!-- Login / Register: password -->
                <template v-if="view === 'login' || view === 'register'">
                    <label class="login-label">{{ $t('Password:') }}</label>
                    <NInput v-model:value="form.password" :placeholder="$t('Password')" type="password" show-password-on="click" size="large" @keydown.enter="submit" />
                </template>

                <!-- Register: confirm password + denomination -->
                <template v-if="view === 'register'">
                    <label class="login-label">Retype Password</label>
                    <NInput v-model:value="form.retypePassword" placeholder="Retype Password" type="password" show-password-on="click" size="large" @keydown.enter="submit" />
                    <label class="login-label">Denomination <span style="color: #fb923c; font-size: 11px; margin-left: 4px;">Required</span></label>
                    <NSelect
                        v-model:value="form.denomination"
                        :options="DENOMINATION_OPTIONS"
                        placeholder="Select your denomination..."
                        filterable
                        :virtual-scroll="false"
                        :scrollbar-props="selectScrollbarProps"
                        size="large"
                    />
                </template>

                <!-- Reset: token + new password -->
                <template v-if="view === 'reset'">
                    <label class="login-label">Reset Token</label>
                    <NInput v-model:value="form.resetToken" placeholder="Paste token from the reset email" size="large" @keydown.enter="submit" />
                    <label class="login-label">New Password</label>
                    <NInput v-model:value="form.newPassword" placeholder="New Password" type="password" show-password-on="click" size="large" @keydown.enter="submit" />
                    <label class="login-label">Confirm New Password</label>
                    <NInput v-model:value="form.newPasswordConfirm" placeholder="Confirm New Password" type="password" show-password-on="click" size="large" @keydown.enter="submit" />
                </template>

                <!-- Submit button -->
                <NButton
                    class="login-submit"
                    :disabled="loading"
                    :loading="loading"
                    type="primary"
                    size="large"
                    block
                    @click="submit"
                >
                    <template v-if="view === 'login'">Sign In</template>
                    <template v-else-if="view === 'register'">Sign Me Up</template>
                    <template v-else-if="view === 'forgot'">Send Reset Link</template>
                    <template v-else>Reset Password</template>
                </NButton>

                <!-- Forgot Password link (login view only) -->
                <NButton v-if="view === 'login'" text size="small" class="login-forgot" @click="view = 'forgot'; form.password = null; successMessage = null">
                    Forgot Password?
                </NButton>

                <!-- Toggle login / register -->
                <NButton v-if="view === 'login' || view === 'register'" size="large" block @click="view = view === 'login' ? 'register' : 'login'">
                    {{ view === 'login' ? $t('Create Account') : 'Already have an account? Sign In' }}
                </NButton>

                <!-- Back to Sign In (forgot / reset views) -->
                <NButton v-if="view === 'forgot' || view === 'reset'" size="large" block @click="view = 'login'">
                    Back to Sign In
                </NButton>

            </div>
        </div>
    </div>
</template>

<style scoped>
/* ── dark (default) ────────────────────────────────── */
.login-page {
    min-height: 100vh;
    width: 100%;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    padding: 24px;
    box-sizing: border-box;
    background: var(--theme-bg-main);
    overflow-y: auto;
}

.login-card {
    width: 100%;
    max-width: 420px;
    margin: auto 0;
    padding: 40px 36px;
    border-radius: 12px;
    border: 1px solid var(--theme-border);
    background: var(--theme-bg-elevated);
    backdrop-filter: blur(8px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
    color: var(--theme-text);
}

.login-brand {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    margin-bottom: 24px;
}

.login-logo {
    width: 36px;
    height: 36px;
    object-fit: contain;
}

.login-app-name {
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 0.02em;
    color: var(--theme-text);
}

.login-title {
    font-size: 24px;
    font-weight: 800;
    text-align: center;
    margin: 0 0 8px;
    color: var(--theme-text);
}

.login-desc {
    text-align: center;
    font-size: 13px;
    color: var(--theme-text-soft);
    margin: 0 0 28px;
    line-height: 1.5;
}

.login-form {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.login-label {
    font-size: 13px;
    color: var(--theme-text-soft);
    margin-bottom: -4px;
}

.login-submit {
    margin-top: 6px;
}

.login-forgot {
    align-self: center;
    opacity: 0.7;
}

.username-at {
    font-size: 15px;
    font-weight: 700;
    opacity: 0.6;
    margin-right: 2px;
}

.login-hint {
    margin: -4px 0 0;
    font-size: 11px;
    opacity: 0.45;
}

.login-success {
    padding: 10px 14px;
    border-radius: 8px;
    background: rgba(34, 197, 94, 0.12);
    border: 1px solid rgba(34, 197, 94, 0.35);
    color: #4ade80;
    font-size: 13px;
    text-align: center;
    line-height: 1.5;
}
</style>
