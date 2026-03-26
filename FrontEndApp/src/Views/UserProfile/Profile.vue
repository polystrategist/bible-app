<script setup lang="ts">
import { onMounted } from 'vue';
import { useAuthStore } from './../../store/authStore';

const authStore = useAuthStore();

onMounted(() => {
    authStore.initAuth();
});
</script>
<template>
    <div class="h-100% w-100% p-2">
        <RouterView />
    </div>
</template>
