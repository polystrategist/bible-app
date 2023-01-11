<script setup lang="ts">
import { NCard, NModal } from 'naive-ui';
import { useMainStore } from '../../store/main';
import About from './About.vue';

const mainStore = useMainStore();
</script>
<template>
    <NModal v-model:show="mainStore.showAbout">
        <About class="max-w-500px my-30px" />
    </NModal>
</template>
