<script setup lang="ts">
import { NSwitch, NIcon, NButton } from 'naive-ui';
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
            {{ $t('themes') }}
        </div>
        <NSwitch v-model:value="themeStore.isDark">
            <template #checked> {{ $t('dark') }} </template>
            <template #unchecked> {{ $t('light') }} </template>
        </NSwitch>
        <NButton
            class="ml-2"
            size="small"
            secondary
            :type="themeStore.backgroundTheme === 'sepia' ? 'primary' : 'default'"
            @click="themeStore.isDark = false; themeStore.setBackgroundTheme(themeStore.backgroundTheme === 'sepia' ? 'default' : 'sepia')"
        >
            {{ $t('sepia') }}
        </NButton>
    </div>
</template>
