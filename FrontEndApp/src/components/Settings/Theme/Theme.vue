<script setup lang="ts">
import { NSwitch, NIcon } from 'naive-ui';
import { Moon, Sun } from '@vicons/carbon';
import { useThemeStore } from '../../../store/theme';

const themeStore = useThemeStore();
</script>

<template>
    <div>
        <div>
            <NIcon>
                <Moon v-if="themeStore.isDark" />
                <Sun v-else />
            </NIcon>
            Theme
        </div>
        <NSwitch v-model:value="themeStore.isDark">
            <template #checked> Dark </template>
            <template #unchecked> Light </template>
        </NSwitch>
    </div>
</template>
