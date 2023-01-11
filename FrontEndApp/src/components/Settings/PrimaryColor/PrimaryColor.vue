<script setup lang="ts">
import { NIcon } from 'naive-ui';
import { ColorPalette } from '@vicons/carbon';
import { useThemeStore } from '../../../store/theme';
import { themesOptions } from '../../../util/themes';

const themeStore = useThemeStore();
</script>

<template>
    <div>
        <div>
            <NIcon>
                <ColorPalette />
            </NIcon>
            Primary Colors
        </div>
        <div class="flex gap-5">
            <div
                v-for="(colors, nameKey) in themesOptions"
                :key="nameKey"
                @click="themeStore.changePrimaryColor(nameKey)"
                class="p-2 dark:hover:bg-gray-50 dark:hover:bg-opacity-20 hover:bg-gray-500 hover:bg-opacity-20 cursor-pointer rounded-md"
                :class="{ 'dark:bg-gray-50 dark:bg-opacity-20 bg-gray-500 bg-opacity-20': themeStore.selectedTheme == nameKey }"
            >
                <div>
                    <span class="capitalize">{{ nameKey }}</span>
                    <div class="flex gap-1" v-if="themeStore.isDark">
                        <div
                            v-for="common in colors.dark"
                            :key="common"
                            class="w-20px h-20px rounded-md"
                            :style="`background-color:${common}`"
                        ></div>
                    </div>
                    <div class="flex gap-1" v-else>
                        <div
                            v-for="common in colors.light"
                            :key="common"
                            class="w-20px h-20px rounded-md"
                            :style="`background-color:${common}`"
                        ></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
