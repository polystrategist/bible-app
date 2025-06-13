<script setup lang="ts">
import { BookLetter24Filled, BookLetter24Regular } from '@vicons/fluent';
import { NBadge, NIcon, NInput, NSelect, NTag } from 'naive-ui';
import { useThemeStore } from '../../../../../store/theme';
import { onMounted, ref, watch } from 'vue';

const displayFont = ref(false);
const fontSize = ref(14);
const themeStore = useThemeStore();
const selected = ref<string | null>(null);
const loading = ref(false);
const options = ref([]);
const definitions = ref<
    Array<{
        word: string;
        wordtype: string;
        definition: string;
    }>
>([]);

async function handleSearch(value: string) {
    const data = await window.browserWindow.searchDictionary(value);
    options.value = data;
}

watch(
    () => selected.value,
    async (val) => {
        if (val) definitions.value = await window.browserWindow.getDefinitions(val);
    }
);

function handleDictionaryScroll(deltaY: number) {
    if (deltaY < 0) {
        fontSize.value++;
    } else {
        fontSize.value--;
    }

    if (!displayFont.value) displayFont.value = true;

    // @ts-ignore
    clearTimeout(window.displayFontSizeDictionaryTimeout);
    // @ts-ignore
    window.displayFontSizeDictionaryTimeout = setTimeout(() => {
        displayFont.value = false;
    }, 2000);
}

onMounted(() => {
    document.addEventListener(
        'wheel',
        (event) => {
            if (event.ctrlKey) {
                // Ensure Ctrl key is pressed
                const dictionaryElement = document.getElementById('show-dictionary-definitions');

                if (dictionaryElement && dictionaryElement.contains(event.target as Node)) {
                    event.preventDefault(); // Prevent browser zoom
                    handleDictionaryScroll(event.deltaY);
                }
            }
        },
        { passive: false }
    );
});
</script>

<template>
    <div class="flex flex-col h-full">
        <NSelect
            v-model:value="selected"
            placeholder="Search..."
            clearable
            filterable
            :loading="loading"
            :options="options"
            label-field="word"
            value-field="word"
            remote
            :clear-filter-after-select="false"
            @search="handleSearch"
            :on-clear="() => (definitions = [])"
        >
            <template #prefix>
                <NIcon>
                    <BookLetter24Filled v-if="themeStore.isDark" />
                    <BookLetter24Regular v-else />
                </NIcon>
            </template>
        </NSelect>
        <div
            id="show-dictionary-definitions"
            class="py-2 relative h-[calc(100%-50px)]"
            :style="`font-size:${fontSize}px`"
        >
            <NTag
                :bordered="false"
                class="absolute bottom-4 right-0 opacity-0"
                :class="{ '!opacity-100': displayFont }"
            >
                {{ fontSize }}px
            </NTag>
            <div
                v-if="definitions.length"
                class="overflowing-div overflow-y-auto h-full flex flex-col gap-3"
            >
                <div v-for="definition in definitions">
                    <span class="italic text-[var(--primary-color)]">{{
                        definition.wordtype ?? ''
                    }}</span>
                    {{ definition.definition }}
                </div>
            </div>
            <div class="h-full flex flex-col items-center justify-center">
                <div class="text-3xl">🔎</div>
                <div>Empty</div>
                <small>Search for a word</small>
            </div>
        </div>
    </div>
</template>
