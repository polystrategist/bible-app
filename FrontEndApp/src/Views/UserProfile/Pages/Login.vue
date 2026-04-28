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
    <div class="h-full w-full">
        <div class="w-400px mx-auto mt-5 flex flex-col gap-2">
            <h5 class="text-center font-800 text-size-25px">
                {{ isRegister ? 'Sign Up' : $t('Sign In') }}
            </h5>
            <p class="text-center text-sm opacity-60 mt-1 mb-2">
                {{ $t('sign-in-desc') }}
            </p>
            {{ $t('Email Address:') }}
            <NInput v-model:value="form.email" :placeholder="$t('Email')" />
            {{ $t('Password:') }}
            <NInput v-model:value="form.password" :placeholder="$t('Password')" type="password" />
            <span v-if="isRegister">Retype Password:</span>
            <NInput
                v-if="isRegister"
                v-model:value="form.retypePassword"
                placeholder="Retype Password"
                type="password"
            />

            <template v-if="isRegister">
                <span>Full Name:</span>
                <NInput v-model:value="form.name" placeholder="Your name" type="text" />
            </template>
            <NButton
                :disabled="loading"
                :loading="loading"
                type="primary"
                @click="submit"
                @keydown.enter="submit"
            >
                {{ isRegister ? 'Sign Me Up' : 'Sign In' }}
            </NButton>
            <NButton v-show="!isRegister" @click="isRegister = true">{{ $t('Create Account') }}</NButton>
            <NButton v-show="isRegister" @click="isRegister = false"
                >Already Have an Account?</NButton
            >
        </div>
    </div>
</template>
