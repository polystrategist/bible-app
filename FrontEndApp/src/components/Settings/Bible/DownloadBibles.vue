<script setup lang="ts">
import { NButton, NIcon, useMessage, NInput } from 'naive-ui';
import { computed, ref } from 'vue';
import { useBibleDownloadStore } from '../../../store/downloadBible';
import { useModuleStore } from '../../../store/moduleStore';
import { bible, type MODULE_BIBLE_TYPE } from '../../../util/modules';
import { Download } from '@vicons/carbon';

const searchBible = ref<string | null>(null);
const message = useMessage();
const bibleDownloadStore = useBibleDownloadStore();
const moduleStore = useModuleStore();
const downloadPercentage = ref<number>(0);

type BibleLanguageGroup = {
    language: string;
    versions: MODULE_BIBLE_TYPE[];
};

function normalizeTitle(title: string) {
    return title.replace(/^[^a-z0-9]+/i, '').trim();
}

function formatDescription(description?: string) {
    if (!description) return 'No description available.';

    return description
        .replace(/<br\s*\/?>/gi, ' ')
        .replace(/<[^>]+>/g, '')
        .replace(/\s+/g, ' ')
        .trim();
}

function matchesSearch(version: MODULE_BIBLE_TYPE, query: string) {
    const normalizedQuery = query.trim().toLowerCase();

    if (!normalizedQuery) return true;

    return [
        normalizeTitle(version.title),
        formatDescription(version.description),
        version.version_short_name_and_date,
        version.language_full,
    ]
        .filter(Boolean)
        .some((value) => value!.toLowerCase().includes(normalizedQuery));
}

const bibleLanguageGroups = computed<BibleLanguageGroup[]>(() => {
    const query = searchBible.value?.trim() ?? '';
    const groupedVersions = new Map<string, MODULE_BIBLE_TYPE[]>();

    for (const version of bible) {
        if (version.title.includes('commentaries')) continue;
        if (!matchesSearch(version, query)) continue;

        const language = version.language_full?.trim() || 'unknown';
        const versions = groupedVersions.get(language) ?? [];
        versions.push(version);
        groupedVersions.set(language, versions);
    }

    return Array.from(groupedVersions.entries())
        .map(([language, versions]) => ({
            language,
            versions: [...versions].sort((a, b) => normalizeTitle(a.title).localeCompare(normalizeTitle(b.title))),
        }))
        .sort((a, b) => a.language.localeCompare(b.language));
});

function isAlreadyDownloaded(file_name: string) {
    for (const item of moduleStore.bibleLists) {
        if (file_name == item.file_name) return false;
    }
    return true;
}

const downloadLoading = ref(false);
const selectedDownloadLink = ref<string | null>(null);
function clickDownload(downloadLink: string, version: any) {
    selectedDownloadLink.value = downloadLink;

    bibleDownloadStore.isDownloading = true;
    downloadLoading.value = true;
    window.browserWindow.downloadModule({
        urls: [downloadLink],
        percentage: (percentage: number) => {
            downloadPercentage.value = percentage;
        },
        done: async () => {
            downloadLoading.value = false;
            await moduleStore.getBibleLists();
            bibleDownloadStore.isDownloading = false;
        },
        cancel: () => {
            downloadLoading.value = false;
            bibleDownloadStore.isDownloading = false;
            message.error('Download Cancelled');
        },
    }, version);
}
</script>
<template>
    <div>
        <div class="mb-3">
            <NInput v-model:value="searchBible" :placeholder="$t('Search versions...')" size="small" clearable />
        </div>
        <div v-if="bibleLanguageGroups.length" class="select-none h-[55vh] overflow-y-auto overflowing-div pr-2">
            <section v-for="group in bibleLanguageGroups" :key="group.language" class="mb-5">
                <div class="sticky top-0 z-1 bg-gray-200 dark:bg-dark-400 py-2 rounded-1">
                    <h2 class="m-0 text-sm font-700 capitalize tracking-[0.08em] px-2 opacity-80">
                        {{ group.language }}
                        <span class="text-xs font-500 normal-case opacity-60">({{ group.versions.length }})</span>
                    </h2>
                </div>

                <div
                    v-for="version in group.versions"
                    :key="version.file_name"
                    :disabled="bibleDownloadStore.isDownloading"
                    class="my-2 flex items-start gap-3 rounded-3 p-2 hover:bg-black hover:bg-opacity-4 dark:hover:bg-white dark:hover:bg-opacity-4"
                >
                    <NButton
                        size="tiny"
                        :disabled="!isAlreadyDownloaded(version.file_name) || downloadLoading"
                        :type="!isAlreadyDownloaded(version.file_name) ? 'default' : 'info'"
                        @click="clickDownload(version.download_link, version)"
                        secondary
                        rounded
                        :loading="version.download_link === selectedDownloadLink && downloadLoading"
                    >
                        <NIcon>
                            <Download />
                        </NIcon>
                        <span class="capitalize">{{ isAlreadyDownloaded(version.file_name) ? $t('add') : $t('added') }}</span>
                        <span v-if="version.download_link === selectedDownloadLink && downloadLoading" class="px-2">
                            {{ downloadPercentage }}%
                        </span>
                    </NButton>

                    <div class="min-w-0 flex-1">
                        <div class="text-base font-600 leading-tight">
                            {{ version.title }}
                        </div>
                        <div class="mt-1 text-xs opacity-60">
                            <span class="font-700">Short name:</span>
                            {{ version.version_short_name_and_date || 'N/A' }}
                        </div>
                        <div class="mt-1 text-sm leading-snug opacity-70">
                            {{ formatDescription(version.description) }}
                        </div>
                    </div>
                </div>
            </section>
        </div>
        <div v-else class="flex items-center justify-center h-200px text-center opacity-50">
            No Bible versions matched your search.
        </div>
    </div>
</template>
