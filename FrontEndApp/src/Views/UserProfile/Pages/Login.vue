<script lang="ts" setup>
import { NButton, NInput, useMessage } from 'naive-ui';
import { onMounted, reactive, ref } from 'vue';
import { supabase } from '../../../util/SupaBase/SupaBase';
import { useRouter } from 'vue-router';
import { useUserStore } from '../../../store/userStore';
import { isSignedIn } from '../../../util/SupaBase/Auth/Auth';

const isRegister = ref(false);
const loading = ref(false);
const userStore = useUserStore();
const router = useRouter();
const message = useMessage();
const form = reactive<{
    email: string | null;
    password: string | null;
    retypePassword: string | null;
    username: string | null;
}>({
    email: null,
    password: null,
    retypePassword: null,
    username: null,
});

async function login() {
    if (!form.email || !form.password) {
        message.error('Cant Continue, some fields does not exist.');
        return;
    }

    loading.value = true;
    const { data, error } = await supabase.auth.signInWithPassword({
        email: form.email,
        password: form.password,
    });
    loading.value = false;

    if (error) {
        message.error(error.message);
        return;
    }

    userStore.user = data;
    message.success('Logged In! Successfully.');
    await router.push('/profile/profile');
}

async function register() {
    loading.value = true;
    if (!form.email || !form.password) {
        message.error('Cant Continue, some fields does not exist.');
        loading.value = false;
        return;
    }

    if (form.password != form.retypePassword) {
        message.error('Password and retype password should be the same.');
        loading.value = false;
        return;
    }

    const { data, error } = await supabase.auth.signUp({
        email: form.email,
        password: form.password,
    });

    if (error) {
        message.error(error.message);
        loading.value = false;
        return;
    }

    const loginData = await supabase.auth.signInWithPassword({
        email: form.email,
        password: form.password,
    });

    if (loginData.error) {
        message.error(loginData.error.message);
        loading.value = false;
        return;
    }

    await supabase.from('profile').insert({
        user_id: loginData.data.user.id,
        username: form.username,
    });

    userStore.user = loginData.data.user;
    message.success('Registered! Successfully.');
    await router.push('/profile/profile');

    loading.value = false;
}

async function submit() {
    if (isRegister.value) await register();
    else await login();
}

onMounted(async () => {
    loading.value = true;

    const data = await isSignedIn();
    if (data) {
        userStore.user = data;
        await router.push('/profile/profile');
    }

    loading.value = false;
});
</script>
<template>
    <div class="h-full w-full">
        <div class="w-400px mx-auto mt-5 flex flex-col gap-2">
            <h5 class="text-center font-800 text-size-25px">
                {{ isRegister ? 'Sign Up' : 'Sign In' }}
            </h5>
            Email Address:
            <NInput v-model:value="form.email" placeholder="Email" />
            Password:
            <NInput v-model:value="form.password" placeholder="Password" type="password" />
            <span v-if="isRegister">Retype Password:</span>
            <NInput v-if="isRegister" v-model:value="form.retypePassword" placeholder="Retype Password" type="password" />

            <h3 v-if="isRegister">Additional Information</h3>
            <NInput v-if="isRegister" v-model:value="form.username" placeholder="Username" type="text" />
            <NButton :disabled="loading" :loading="loading" type="primary" @click="submit" @keydown.enter="submit">
                {{ isRegister ? 'Sign Me Up' : 'Sign In' }}
            </NButton>
            <NButton v-show="!isRegister" @click="isRegister = true">Create Account</NButton>
            <NButton v-show="isRegister" @click="isRegister = false">Already Have an Account?</NButton>
        </div>
    </div>
</template>
