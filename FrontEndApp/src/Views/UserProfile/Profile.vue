<script setup lang="ts">
import { useAuthStore } from './../../store/authStore';

const authStore = useAuthStore();
</script>
<template>
    <div class="h-100% w-100% p-2">
        <RouterView />
    </div>
</template>
