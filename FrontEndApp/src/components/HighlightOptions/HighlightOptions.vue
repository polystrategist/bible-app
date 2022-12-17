<script setup lang="ts">
import { highlight, isHighlightable, colors } from './../../util/highlighter';
import { CircleSolid, Delete } from '@vicons/carbon';
import { NIcon, NButton } from 'naive-ui';
import { useBibleStore } from '../../store/BibleStore';

const bibleStore = useBibleStore();
const emit = defineEmits(['setHighlight']);

async function highlightSelection(color: string) {
    if (!isHighlightable()) return;
    await highlight(color);
    await bibleStore.getHighlights();
    emit('setHighlight', color);
}
</script>
<template>
    <span class="flex items-center whitespace-nowrap text-size-30px gap-7px">
        <button
            v-for="color in colors"
            :key="color.color"
            @click="highlightSelection(color.color)"
            :style="`color: ${color.color}`"
            class="border-1 border-opacity-0 border-light-50 hover:border-[var(--primaryColor)] rounded-1 flex items-center justify-center"
        >
            <NIcon>
                <CircleSolid />
            </NIcon>
        </button>
        <NButton size="small" @click="highlightSelection('remove')" round strong>
            <template #icon>
                <NIcon>
                    <Delete />
                </NIcon>
            </template>
            <span class="capitalize">{{ $t('remove') }}</span>
        </NButton>
    </span>
</template>
