<script setup lang="ts">
import { NButton, NIcon, NPopover } from 'naive-ui';
import { useThemeStore } from '../../store/theme';
import {
    Circle24Filled,
    PaintBucket24Filled,
    PaintBucket24Regular,
} from '@vicons/fluent';
import { themesOptions } from '../../util/themes';

const themeStore = useThemeStore();

defineProps({
    placement: {
        type: String,
        default: 'bottom-end',
    },
});
</script>
<template>
    <NPopover trigger="click" :placement="placement as any">
        <template #trigger>
            <NButton round size="small" quaternary title="Change Theme">
                <NIcon size="20">
                    <PaintBucket24Filled v-if="themeStore.isDark" />
                    <PaintBucket24Regular v-else />
                </NIcon>
            </NButton>
        </template>
        <div class="max-w-500px">
            <div class="mb-5">
                <div class="capitalize">{{ $t('customize') }}</div>
                <small> {{ $t('Pick a style and color for you') }} </small>
            </div>
            <div class="mb-5">
                <div class="capitalize">{{ $t('color') }}</div>
                <div class="grid grid-cols-3 gap-1">
                    <NButton
                        v-for="(colors, nameKey) in themesOptions"
                        :key="nameKey"
                        @click="themeStore.changePrimaryColor(nameKey)"
                        :type="themeStore.selectedTheme == nameKey ? 'primary' : 'default'"
                        secondary
                        round
                        size="small"
                        class="px-2"
                    >
                        <template #icon>
                            <Circle24Filled v-if="themeStore.isDark" :color="colors.dark.primaryColor"></Circle24Filled>
                            <Circle24Filled v-else :color="colors.light.primaryColor"></Circle24Filled>
                        </template>
                        <span class="capitalize">{{ $t(nameKey) }}</span>
                    </NButton>
                </div>
            </div>
            <div>
                <div class="capitalize">{{ $t('theme') }}</div>
                <div class="grid grid-cols-3 gap-1">
                    <NButton
                        v-for="appearance in themeStore.appearanceThemeOptions"
                        :key="appearance.key"
                        @click="themeStore.applyAppearanceTheme(appearance)"
                        secondary
                        round
                        size="small"
                        :type="
                            themeStore.isDark === appearance.isDark &&
                            themeStore.backgroundTheme === appearance.backgroundTheme
                                ? 'primary'
                                : 'default'
                        "
                    >
                        <template #icon>
                            <Circle24Filled :color="appearance.swatch"></Circle24Filled>
                        </template>
                        <span class="capitalize">{{ $t(appearance.label) }}</span>
                    </NButton>
                </div>
            </div>
        </div>
    </NPopover>
</template>
