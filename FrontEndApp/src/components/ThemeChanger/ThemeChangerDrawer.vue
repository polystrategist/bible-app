<script setup lang="ts">
import { NButton, NIcon, NPopover } from 'naive-ui';
import { useThemeStore } from '../../store/theme';
import {
    Circle24Filled,
    PaintBucket24Filled,
    PaintBucket24Regular,
    WeatherMoon24Filled,
    WeatherMoon24Regular,
    WeatherSunny24Filled,
    WeatherSunny24Regular,
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
            <NButton round size="tiny" quaternary title="Change Theme">
                <NIcon size="17">
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
                <NButton
                    class="mr-1"
                    @click="themeStore.isDark = false; themeStore.setBackgroundTheme('default')"
                    secondary
                    round
                    size="small"
                    :type="!themeStore.isDark && themeStore.backgroundTheme === 'default' ? 'primary' : 'default'"
                >
                    <template #icon>
                        <NIcon>
                            <WeatherSunny24Filled v-if="themeStore.isDark" />
                            <WeatherSunny24Regular v-else />
                        </NIcon>
                    </template>
                    {{ $t('light') }}
                </NButton>
                <NButton
                    class="mr-1"
                    @click="themeStore.isDark = true; themeStore.setBackgroundTheme('default')"
                    secondary
                    round
                    size="small"
                    :type="themeStore.isDark && themeStore.backgroundTheme === 'default' ? 'primary' : 'default'"
                >
                    <template #icon>
                        <NIcon>
                            <WeatherMoon24Filled v-if="themeStore.isDark" />
                            <WeatherMoon24Regular v-else />
                        </NIcon>
                    </template>
                    <span class="capitalize">{{ $t('night') }}</span>
                </NButton>
                <NButton
                    @click="themeStore.isDark = false; themeStore.setBackgroundTheme('sepia')"
                    secondary
                    round
                    size="small"
                    :type="themeStore.backgroundTheme === 'sepia' ? 'primary' : 'default'"
                >
                    <template #icon>
                        <Circle24Filled color="#8b6b3f"></Circle24Filled>
                    </template>
                    <span class="capitalize">{{ $t('sepia') }}</span>
                </NButton>
            </div>
        </div>
    </NPopover>
</template>
