<script setup lang="ts">
import { NButton, NSlider } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { computed } from 'vue';
import { useSettingStore } from '../../../store/settingStore';

const settings = useSettingStore();

const scalePercent = computed({
    get: () => Math.round(settings.appScale * 100),
    set: (value: number) => {
        settings.appScale = Number((value / 100).toFixed(2));
    },
});

function resetScale() {
    settings.appScale = 1;
}
</script>

<template>
    <div>
        <div class="flex items-center gap-1 flex-wrap">
            <Icon class="text-size-16px" icon="carbon:zoom-in-area" />
            {{ $t('Scale') }}
            <span class="text-xs opacity-70">({{ scalePercent }}%)</span>
            <span class="text-xs opacity-50 ml-1">
                <kbd class="font-mono">Ctrl+Shift+-</kbd> / <kbd class="font-mono">Ctrl+Shift++</kbd>
            </span>
        </div>
        <p class="text-xs opacity-50 mt-1">{{ $t('adjust-zoom-desc') }}</p>
        <div class="mt-2 flex items-center gap-3">
            <NSlider
                v-model:value="scalePercent"
                :min="75"
                :max="150"
                :step="5"
                class="flex-1"
            />
            <NButton size="small" secondary @click="resetScale">Reset</NButton>
        </div>
    </div>
</template>
