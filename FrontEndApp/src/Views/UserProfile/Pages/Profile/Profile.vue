<script lang="ts" setup>
import { onMounted } from 'vue';
import { useAuthStore } from '../../../../store/authStore';
import { useRouter } from 'vue-router';
import ProfilePage from './../../../../components/ProfilePage/ProfilePage.vue';

const authStore = useAuthStore();
const router = useRouter();

onMounted(async () => {
    if (!authStore.isAuthenticated) {
        await router.push('/profile');
    } else if (!authStore.user) {
        await authStore.getUser();
        if (!authStore.user) {
            await router.push('/profile');
        }
    }
});
</script>

<template>
    <div class="h-full w-full">
        <div class="max-w-500px mx-auto py-3 px-3 mt-5">
            <ProfilePage v-if="authStore.user" />
        </div>
    </div>
</template>
