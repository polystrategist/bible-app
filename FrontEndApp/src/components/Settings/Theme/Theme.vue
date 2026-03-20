<script setup lang="ts">
import { NIcon, NButton } from 'naive-ui';
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
        <div class="mt-2 flex flex-wrap gap-1">
            <NButton
                v-for="appearance in themeStore.appearanceThemeOptions"
                :key="appearance.key"
                size="small"
                secondary
                :type="
                    themeStore.isDark === appearance.isDark &&
                    themeStore.backgroundTheme === appearance.backgroundTheme
                        ? 'primary'
                        : 'default'
                "
                @click="themeStore.applyAppearanceTheme(appearance)"
            >
                {{ $t(appearance.label) }}
            </NButton>
        </div>
    </div>
</template>
