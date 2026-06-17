<script setup lang="ts">
import { ref } from 'vue';
import { NButton, NIcon, NPopover } from 'naive-ui';
import { useThemeStore } from '../../store/theme';
import {
    Circle24Filled,
    PaintBucket24Filled,
    PaintBucket24Regular,
    ChevronDown24Filled,
} from '@vicons/fluent';
import { themesOptions } from '../../util/themes';
import { appearanceThemeOptions } from '../../util/appearanceThemes';
import { themePresets, type ThemePreset } from '../../util/themePresets';

const themeStore = useThemeStore();

defineProps({
    placement: {
        type: String,
        default: 'bottom-end',
    },
});

const showCustom = ref(false);

// Preview background/foreground per appearance (mirrors mobile kAppearanceThemes),
// used to render the preset tiles like the mobile app.
const APPEARANCE_PREVIEW: Record<string, { bg: string; fg: string }> = {
    light: { bg: '#E8E8E8', fg: '#1A1A1A' },
    night: { bg: '#5F5F67', fg: '#FFFFFF' },
    sepia: { bg: '#F4EDDD', fg: '#3F2F1E' },
    forest: { bg: '#E7F1E5', fg: '#24351F' },
    dawn: { bg: '#FFF2E6', fg: '#4A2D18' },
    dusk: { bg: '#2B2B42', fg: '#ECECFF' },
    nord: { bg: '#2D3748', fg: '#E6EEF7' },
    midnight: { bg: '#141B2D', fg: '#E8EFFF' },
    rosepaper: { bg: '#FDF0F2', fg: '#4B2530' },
    oceanic: { bg: '#132B33', fg: '#E0F4F8' },
    graphite: { bg: '#2A2D34', fg: '#F1F3F7' },
    sandstone: { bg: '#F5EADF', fg: '#3F2F20' },
    parchment: { bg: '#F2E8D0', fg: '#2D1F0E' },
    cream: { bg: '#FAF8F3', fg: '#2A2520' },
    arctic: { bg: '#EEF4F8', fg: '#1A2D3A' },
    lavender: { bg: '#F3F0FA', fg: '#2D2040' },
    moss: { bg: '#EEF3EC', fg: '#1E2E1A' },
    abyss: { bg: '#0D1117', fg: '#E0E6F0' },
    mocha: { bg: '#1E1610', fg: '#F0E6D8' },
    emerald: { bg: '#0D1F18', fg: '#D0F0E0' },
    crimson: { bg: '#1A0D0F', fg: '#F5E0E2' },
    amethyst: { bg: '#150D1F', fg: '#E8D8F8' },
};

function appearanceFor(key: string) {
    return appearanceThemeOptions.find((a) => a.key === key);
}

function applyPreset(preset: ThemePreset) {
    const ap = appearanceFor(preset.appearance);
    if (ap) themeStore.applyAppearanceTheme(ap);
    themeStore.changePrimaryColor(preset.accent);
}

function isPresetActive(preset: ThemePreset): boolean {
    const ap = appearanceFor(preset.appearance);
    return (
        !!ap &&
        themeStore.isDark === ap.isDark &&
        themeStore.backgroundTheme === ap.backgroundTheme &&
        themeStore.selectedTheme === preset.accent
    );
}

function presetAccentColor(preset: ThemePreset): string {
    const c = themesOptions[preset.accent];
    if (!c) return 'var(--primary-color)';
    return themeStore.isDark ? c.dark.primaryColor : c.light.primaryColor;
}

function presetBg(preset: ThemePreset): string {
    return APPEARANCE_PREVIEW[preset.appearance]?.bg ?? 'var(--theme-bg-soft)';
}

function presetBarColor(preset: ThemePreset): string {
    return APPEARANCE_PREVIEW[preset.appearance]?.fg ?? 'var(--theme-text)';
}
</script>
<template>
    <NPopover trigger="click" :placement="placement as any">
        <template #trigger>
            <NButton round size="small" quaternary :title="$t('Change Theme')">
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
                <div class="capitalize mb-2">{{ $t('Presets') }}</div>
                <div class="preset-row">
                    <button
                        v-for="preset in themePresets"
                        :key="preset.name"
                        class="preset-tile"
                        :class="{ 'preset-tile--active': isPresetActive(preset) }"
                        :title="preset.name"
                        @click="applyPreset(preset)"
                    >
                        <div class="preset-swatch" :style="{ background: presetBg(preset) }">
                            <span class="preset-dot" :style="{ background: presetAccentColor(preset) }" />
                            <span class="preset-bar" :style="{ background: presetBarColor(preset) }" />
                        </div>
                        <span class="preset-name">{{ preset.name }}</span>
                    </button>
                </div>
            </div>
            <div>
                <button class="custom-toggle" @click="showCustom = !showCustom">
                    <span class="capitalize">{{ $t('customColors') }}</span>
                    <NIcon size="16" class="custom-chevron" :class="{ 'custom-chevron--open': showCustom }">
                        <ChevronDown24Filled />
                    </NIcon>
                </button>
                <div v-show="showCustom">
                    <div class="mb-5 mt-2">
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
            </div>
        </div>
    </NPopover>
</template>

<style scoped>
.preset-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}
.preset-tile {
    flex: 0 0 auto;
    width: 64px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 5px;
    padding: 0;
    background: none;
    border: none;
    cursor: pointer;
}
.preset-swatch {
    width: 64px;
    height: 48px;
    box-sizing: border-box;
    border-radius: 10px;
    border: 1.5px solid var(--theme-border);
    display: flex;
    align-items: flex-end;
    gap: 4px;
    padding: 8px;
}
.preset-tile--active .preset-swatch {
    border: 2.5px solid var(--primary-color);
}
.preset-dot {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    flex: 0 0 auto;
}
.preset-bar {
    width: 18px;
    height: 4px;
    border-radius: 2px;
    opacity: 0.5;
}
.preset-name {
    font-size: 10px;
    line-height: 1.2;
    max-width: 64px;
    text-align: center;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    color: var(--theme-text);
}
.custom-toggle {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    padding: 6px 0;
    background: none;
    border: none;
    cursor: pointer;
    color: var(--theme-text);
    font-size: 14px;
}
.custom-chevron {
    transition: transform 0.15s;
}
.custom-chevron--open {
    transform: rotate(180deg);
}
</style>
