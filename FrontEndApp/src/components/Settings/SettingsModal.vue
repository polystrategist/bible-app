<script setup lang="ts">
import { NModal } from 'naive-ui';
import { useMainStore } from '../../store/main';
import Settings from './Settings.vue';

const mainStore = useMainStore();
</script>
<template>
    <NModal v-model:show="mainStore.showSettings" class="my-30px">
        <Settings class="max-w-500px" />
    </NModal>
</template>
