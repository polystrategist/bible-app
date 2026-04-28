<script lang="ts" setup>
import { NButton, NInput, useMessage } from 'naive-ui';
import { onMounted, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../../store/authStore';

const isRegister = ref(false);
const loading = ref(false);
const authStore = useAuthStore();
const router = useRouter();
const message = useMessage();
const form = reactive<{
    email: string | null;
    password: string | null;
    retypePassword: string | null;
    name: string | null;
}>({
    email: null,
    password: null,
    retypePassword: null,
    name: null,
});

async function login() {
    if (!form.email || !form.password) {
        message.error('Cant Continue, some fields does not exist.');
        return;
    }

    loading.value = true;
    const result = await authStore.login(form.email, form.password);
    loading.value = false;

    if (!result.success) {
        message.error(result.message);
        return;
    }

    message.success('Logged In! Successfully.');
    await router.push(window.isElectron ? '/profile/profile' : '/');
}

async function register() {
    if (!form.email || !form.password || !form.name) {
        message.error('Cant Continue, some fields does not exist.');
        return;
    }

    if (form.password != form.retypePassword) {
        message.error('Password and retype password should be the same.');
        return;
    }

    loading.value = true;
    const result = await authStore.register(
        form.name,
        form.email,
        form.password,
        form.retypePassword!,
    );
    loading.value = false;

    if (!result.success) {
        message.error(result.message);
        return;
    }

    message.success('Registered! Successfully.');
    await router.push(window.isElectron ? '/profile/profile' : '/');
}

async function submit() {
    if (isRegister.value) await register();
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

            <h2 class="login-title">{{ isRegister ? 'Create Account' : 'Sign In' }}</h2>
            <p class="login-desc">{{ $t('sign-in-desc') }}</p>

            <div class="login-form">
                <template v-if="isRegister">
                    <label class="login-label">Full Name</label>
                    <NInput v-model:value="form.name" placeholder="Your name" size="large" @keydown.enter="submit" />
                </template>

                <label class="login-label">{{ $t('Email Address:') }}</label>
                <NInput v-model:value="form.email" :placeholder="$t('Email')" size="large" @keydown.enter="submit" />

                <label class="login-label">{{ $t('Password:') }}</label>
                <NInput v-model:value="form.password" :placeholder="$t('Password')" type="password" size="large" @keydown.enter="submit" />

                <template v-if="isRegister">
                    <label class="login-label">Retype Password</label>
                    <NInput v-model:value="form.retypePassword" placeholder="Retype Password" type="password" size="large" @keydown.enter="submit" />
                </template>

                <NButton
                    class="login-submit"
                    :disabled="loading"
                    :loading="loading"
                    type="primary"
                    size="large"
                    block
                    @click="submit"
                >
                    {{ isRegister ? 'Sign Me Up' : 'Sign In' }}
                </NButton>

                <NButton size="large" block @click="isRegister = !isRegister">
                    {{ isRegister ? 'Already have an account? Sign In' : $t('Create Account') }}
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
    align-items: center;
    justify-content: center;
    padding: 24px;
    box-sizing: border-box;
    background: #111;
}

.login-card {
    width: 100%;
    max-width: 420px;
    padding: 40px 36px;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: rgba(255, 255, 255, 0.04);
    backdrop-filter: blur(8px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    color: #ffffff;
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
    filter: brightness(0) invert(1);
}

.login-app-name {
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 0.02em;
    color: rgba(255, 255, 255, 0.9);
}

.login-title {
    font-size: 24px;
    font-weight: 800;
    text-align: center;
    margin: 0 0 8px;
    color: #ffffff;
}

.login-desc {
    text-align: center;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.5);
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
    color: rgba(255, 255, 255, 0.65);
    margin-bottom: -4px;
}

.login-submit {
    margin-top: 6px;
}

/* ── light theme overrides ─────────────────────────── */
:global(body.light) .login-page {
    background: #f0f0f0;
}

:global(body.light) .login-card {
    background: rgba(255, 255, 255, 0.8);
    border-color: rgba(0, 0, 0, 0.08);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    color: #111111;
}

:global(body.light) .login-logo {
    filter: brightness(0);
}

:global(body.light) .login-app-name { color: rgba(0, 0, 0, 0.85); }
:global(body.light) .login-title    { color: #111111; }
:global(body.light) .login-desc     { color: rgba(0, 0, 0, 0.5); }
:global(body.light) .login-label    { color: rgba(0, 0, 0, 0.65); }
</style>
