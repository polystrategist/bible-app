<script setup lang="ts">
import { highlight, isHighlightable } from './../../util/highlighter';
import { CircleSolid, Delete } from '@vicons/carbon';
import { NIcon, NButton } from 'naive-ui';

const emit = defineEmits(['setHighlight']);

function highlightSelection(color: string) {
    console.log(color);
    if (!isHighlightable()) return;
    highlight(color);
    emit('setHighlight', color);
}
</script>
<template>
    <span class="flex items-center whitespace-nowrap text-size-30px gap-7px">
        <button
            @click="highlightSelection('#FFD26A')"
            style="color: #ffd26a"
            class="border-1 border-opacity-0 border-light-50 hover:border-[var(--primaryColor)] rounded-1 flex items-center justify-center"
        >
            <NIcon>
                <CircleSolid />
            </NIcon>
        </button>
        <button
            @click="highlightSelection('lightpink')"
            style="color: lightpink"
            class="border-1 border-opacity-0 border-light-50 hover:border-[var(--primaryColor)] rounded-1 flex items-center justify-center"
        >
            <NIcon>
                <CircleSolid />
            </NIcon>
        </button>
        <button
            @click="highlightSelection('lightblue')"
            style="color: lightblue"
            class="border-1 border-opacity-0 border-light-50 hover:border-[var(--primaryColor)] rounded-1 flex items-center justify-center"
        >
            <NIcon>
                <CircleSolid />
            </NIcon>
        </button>
        <button
            @click="highlightSelection('#80ED99')"
            style="color: #80ed99"
            class="border-1 border-opacity-0 border-light-50 hover:border-[var(--primaryColor)] rounded-1 flex items-center justify-center"
        >
            <NIcon>
                <CircleSolid />
            </NIcon>
        </button>
        <button
            @click="highlightSelection('#C2B8A3')"
            style="color: #c2b8a3"
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
