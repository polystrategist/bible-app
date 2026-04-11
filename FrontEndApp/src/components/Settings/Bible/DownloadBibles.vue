<script setup lang="ts">
import { NButton, NIcon, useMessage, NInput } from 'naive-ui';
import { useVirtualList } from '@vueuse/core';
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

type FlatItem =
    | { type: 'header'; language: string; count: number; key: string }
    | { type: 'version'; version: MODULE_BIBLE_TYPE; key: string };

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

const flatItems = computed<FlatItem[]>(() => {
    const items: FlatItem[] = [];
    for (const group of bibleLanguageGroups.value) {
        items.push({
            type: 'header',
            language: group.language,
            count: group.versions.length,
            key: `header-${group.language}`,
        });
        for (const version of group.versions) {
            items.push({
                type: 'version',
                version,
                key: `version-${version.file_name}`,
            });
        }
    }
    return items;
});

const HEADER_HEIGHT = 40;
const VERSION_HEIGHT = 100;

const { list, containerProps, wrapperProps } = useVirtualList(flatItems, {
    itemHeight: (index) => flatItems.value[index]?.type === 'header' ? HEADER_HEIGHT : VERSION_HEIGHT,
    overscan: 5,
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
        <div
            v-if="flatItems.length"
            v-bind="containerProps"
            class="select-none h-[calc(70vh-180px)] overflowing-div pr-2"
        >
            <div v-bind="wrapperProps">
                <template v-for="{ data: item, index } in list" :key="item.key">
                    <!-- Language group header -->
                    <div
                        v-if="item.type === 'header'"
                        :style="{ height: `${HEADER_HEIGHT}px` }"
                        class="bg-gray-200 dark:bg-dark-400 py-2 rounded-1 flex items-center"
                    >
                        <h2 class="m-0 text-sm font-700 capitalize tracking-[0.08em] px-2 opacity-80">
                            {{ item.language }}
                            <span class="text-xs font-500 normal-case opacity-60">({{ item.count }})</span>
                        </h2>
                    </div>

                    <!-- Version card -->
                    <div
                        v-else
                        :style="{ height: `${VERSION_HEIGHT}px` }"
                        :disabled="bibleDownloadStore.isDownloading"
                        class="flex items-start gap-3 rounded-3 p-2 hover:bg-black hover:bg-opacity-4 dark:hover:bg-white dark:hover:bg-opacity-4"
                    >
                        <NButton
                            size="tiny"
                            :disabled="!isAlreadyDownloaded(item.version.file_name) || downloadLoading"
                            :type="!isAlreadyDownloaded(item.version.file_name) ? 'default' : 'info'"
                            @click="clickDownload(item.version.download_link, item.version)"
                            secondary
                            rounded
                            :loading="item.version.download_link === selectedDownloadLink && downloadLoading"
                        >
                            <NIcon>
                                <Download />
                            </NIcon>
                            <span class="capitalize">{{ isAlreadyDownloaded(item.version.file_name) ? $t('add') : $t('added') }}</span>
                            <span v-if="item.version.download_link === selectedDownloadLink && downloadLoading" class="px-2">
                                {{ downloadPercentage }}%
                            </span>
                        </NButton>

                        <div class="min-w-0 flex-1">
                            <div class="text-base font-600 leading-tight">
                                {{ item.version.title }}
                            </div>
                            <div class="mt-1 text-xs opacity-60">
                                <span class="font-700">Short name:</span>
                                {{ item.version.version_short_name_and_date || 'N/A' }}
                            </div>
                            <div class="mt-1 text-sm leading-snug opacity-70 line-clamp-2">
                                {{ formatDescription(item.version.description) }}
                            </div>
                        </div>
                    </div>
                </template>
            </div>
        </div>
        <div v-else class="flex items-center justify-center h-200px text-center opacity-50">
            No Bible versions matched your search.
        </div>
    </div>
</template>
