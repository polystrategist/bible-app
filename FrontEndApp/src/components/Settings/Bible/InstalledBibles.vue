<script setup lang="ts">
import { NButton, NIcon, NPopconfirm, useMessage } from 'naive-ui';
import { ref } from 'vue';
import { useModuleStore } from '../../../store/moduleStore';
import { useBibleStore } from '../../../store/BibleStore';
import { TrashCan } from '@vicons/carbon';

const message = useMessage();
const moduleStore = useModuleStore();
const bibleStore = useBibleStore();
const deletingFile = ref<string | null>(null);

function formatDescription(description?: string) {
    if (!description) return '';
    return description
        .replace(/<br\s*\/?>/gi, ' ')
        .replace(/<[^>]+>/g, '')
        .replace(/\s+/g, ' ')
        .trim();
}

async function removeBible(fileName: string, title: string) {
    deletingFile.value = fileName;
    try {
        const result = await window.browserWindow.deleteBible(fileName);
        if (result.success) {
            message.success(`Removed "${title}"`);
            bibleStore.selectedBibleVersions = bibleStore.selectedBibleVersions.filter((v) => v !== fileName);
            if (!bibleStore.selectedBibleVersions.length) {
                await moduleStore.getBibleLists();
                if (moduleStore.bibleLists.length) {
                    bibleStore.selectedBibleVersions = [moduleStore.bibleLists[0].file_name];
                }
            } else {
                await moduleStore.getBibleLists();
            }
            bibleStore.getVerses();
        } else {
            message.error(result.error || 'Failed to remove Bible module.');
        }
    } catch (err: any) {
        message.error(`Error: ${err.message}`);
    } finally {
        deletingFile.value = null;
    }
}
</script>
<template>
    <div class="flex flex-col gap-1">
        <template v-for="bible in moduleStore.bibleLists">
            <div v-if="!bible.title.includes('commentaries')"
                class="py-2 px-3 rounded-2 flex items-start justify-between gap-3 hover:bg-black hover:bg-opacity-4 dark:hover:bg-white dark:hover:bg-opacity-4">
                <div class="min-w-0 flex-1">
                    <div class="font-600 leading-tight">{{ bible.title }}</div>
                    <div v-if="bible.short_name || bible.language" class="mt-1 flex items-center gap-2 text-xs opacity-50">
                        <span v-if="bible.short_name">{{ bible.short_name }}</span>
                        <span v-if="bible.short_name && bible.language">·</span>
                        <span v-if="bible.language" class="capitalize">{{ bible.language }}</span>
                    </div>
                    <div v-if="formatDescription(bible.description)" class="mt-1 text-xs opacity-40">
                        {{ formatDescription(bible.description) }}
                    </div>
                </div>
                <NPopconfirm @positive-click="removeBible(bible.file_name, bible.title)" positive-text="Remove" negative-text="Cancel">
                    <template #trigger>
                        <NButton quaternary size="tiny" type="error" :loading="deletingFile === bible.file_name" class="mt-0.5">
                            <template #icon>
                                <NIcon><TrashCan /></NIcon>
                            </template>
                        </NButton>
                    </template>
                    Remove "{{ bible.title }}"?
                </NPopconfirm>
            </div>
        </template>
        <div v-if="!moduleStore.bibleLists.length" class="text-xs opacity-50 text-center py-4">
            No Bible versions added. Switch to the Download tab to add versions.
        </div>
    </div>
</template>
