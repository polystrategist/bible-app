<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import { useAuthStore } from '../../../../store/authStore';
import { useRouter } from 'vue-router';
import ProfilePage from './../../../../components/ProfilePage/ProfilePage.vue';
import { NButton } from 'naive-ui';

const authStore = useAuthStore();
const router = useRouter();
const loading = ref(false);
const offline = ref(false);

onMounted(async () => {
    if (!authStore.isAuthenticated) {
        await router.push('/profile');
    } else if (!authStore.user) {
        loading.value = true;
        await authStore.getUser();
        loading.value = false;
        // Only redirect if the token was invalidated (401/403); network errors
        // leave isAuthenticated true so we stay on the page without looping.
        if (!authStore.isAuthenticated) {
            await router.push('/profile');
        } else if (!authStore.user) {
            offline.value = true;
        }
    }
});

async function retry() {
    offline.value = false;
    loading.value = true;
    await authStore.getUser();
    loading.value = false;
    if (!authStore.isAuthenticated) {
        await router.push('/profile');
    } else if (!authStore.user) {
        offline.value = true;
    }
}
</script>

<template>
    <div class="h-full w-full">
        <div class="max-w-500px mx-auto py-3 px-3 mt-5">
            <ProfilePage v-if="authStore.user" />

            <div v-else-if="loading" class="flex flex-col items-center gap-3 mt-10 opacity-60">
                <div class="i-carbon-circle-dash animate-spin text-4xl" />
                <p class="text-sm">Loading profile...</p>
            </div>

            <div v-else-if="offline" class="flex flex-col items-center gap-4 mt-10 text-center">
                <div class="i-carbon-wifi-off text-5xl opacity-40" />
                <p class="font-600">Unable to reach server</p>
                <p class="text-sm opacity-60">Your account data could not be loaded. Check your connection and try again.</p>
                <NButton type="primary" @click="retry">Retry</NButton>
            </div>
        </div>
    </div>
</template>
