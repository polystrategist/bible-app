<script setup lang="ts">
import { highlight, isHighlightable, colors } from './../../util/highlighter';
import { NButton } from 'naive-ui';
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
            :style="`background: ${color.color}`"
            class="border-1 border-opacity-0 rounded-full flex items-center justify-center cursor-pointer h-28px w-28px"
        ></button>
        <NButton secondary size="small" @click="highlightSelection('remove')" round strong>
            <span class="capitalize">{{ $t('clear') }}</span>
        </NButton>
    </span>
</template>
