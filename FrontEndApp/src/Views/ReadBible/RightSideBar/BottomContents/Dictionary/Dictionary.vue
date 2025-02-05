<script setup lang="ts">
import { BookLetter24Filled, BookLetter24Regular } from '@vicons/fluent';
import { NIcon, NInput, NSelect } from 'naive-ui';
import { useThemeStore } from '../../../../../store/theme';
import { ref, watch } from 'vue';

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
        >
            <template #prefix>
                <NIcon>
                    <BookLetter24Filled v-if="themeStore.isDark" />
                    <BookLetter24Regular v-else />
                </NIcon>
            </template>
        </NSelect>
        <div class="overflowing-div overflow-y-auto h-full flex flex-col gap-3 py-2">
            <div v-for="definition in definitions">
                {{ definition.wordtype ?? '' }} {{ definition.definition }}
            </div>
        </div>
    </div>
</template>
