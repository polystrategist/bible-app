<script setup lang="ts">
import { NButton, NIcon, useMessage, NInput, NSelect, NModal, NCard } from 'naive-ui';
import { useVirtualList } from '@vueuse/core';
import { computed, ref, watch } from 'vue';
import { useBibleDownloadStore } from '../../../store/downloadBible';
import { useModuleStore } from '../../../store/moduleStore';
import { bible, type MODULE_BIBLE_TYPE } from '../../../util/modules';
import { Download } from '@vicons/carbon';

const searchBible = ref<string | null>(null);
const selectedLanguage = ref<string | null>(null);
const selectedModuleType = ref<string | null>(null);

watch(selectedModuleType, () => {
    selectedLanguage.value = null;
});

const moduleTypeOptions = computed(() => {
    const types = new Set<string>();
    for (const version of bible) {
        if (version.title.includes('commentaries')) continue;
        const type = version.module_type?.trim();
        if (type) types.add(type);
    }
    const labels: Record<string, string> = {
        'believers_sword': "Believer's Sword",
        'ebible': 'eBible.org',
        'ph4_mybible': 'PH4.org MyBible',
    };
    return [
        { label: 'All sources', value: null as unknown as string },
        ...Array.from(types)
            .sort((a, b) => a.localeCompare(b))
            .map((type) => ({ label: labels[type] || type, value: type })),
    ];
});

const languageOptions = computed(() => {
    const typeFilter = selectedModuleType.value;
    const langs = new Set<string>();
    for (const version of bible) {
        if (version.title.includes('commentaries')) continue;
        if (typeFilter && version.module_type !== typeFilter) continue;
        const lang = version.language_full?.trim();
        if (lang) langs.add(lang);
    }
    return [
        { label: 'All languages', value: null as unknown as string },
        ...Array.from(langs)
            .sort((a, b) => a.localeCompare(b))
            .map((lang) => ({ label: lang.charAt(0).toUpperCase() + lang.slice(1), value: lang })),
    ];
});

function openExternal(url: string) {
    window.browserWindow.openExternal(url);
}
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
    const langFilter = selectedLanguage.value;
    const typeFilter = selectedModuleType.value;
    const groupedVersions = new Map<string, MODULE_BIBLE_TYPE[]>();

    for (const version of bible) {
        if (version.title.includes('commentaries')) continue;
        if (!matchesSearch(version, query)) continue;

        const language = version.language_full?.trim() || 'unknown';
        if (langFilter && language !== langFilter) continue;
        if (typeFilter && version.module_type !== typeFilter) continue;

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

// PH4.org confirmation dialog
const showPh4Dialog = ref(false);
const pendingPh4Version = ref<any>(null);

// eBible.org confirmation dialog
const showEbibleDialog = ref(false);
const pendingEbibleVersion = ref<any>(null);

function clickDownload(downloadLink: string, version: any) {
    if (version.module_type === 'ph4_mybible') {
        pendingPh4Version.value = version;
        showPh4Dialog.value = true;
        return;
    }
    if (version.module_type === 'ebible') {
        pendingEbibleVersion.value = version;
        showEbibleDialog.value = true;
        return;
    }
    startDownload(downloadLink, version);
}

function confirmPh4Download() {
    showPh4Dialog.value = false;
    if (pendingPh4Version.value) {
        startDownload(pendingPh4Version.value.download_link, pendingPh4Version.value);
        pendingPh4Version.value = null;
    }
}

function cancelPh4Download() {
    showPh4Dialog.value = false;
    pendingPh4Version.value = null;
}

function confirmEbibleDownload() {
    showEbibleDialog.value = false;
    if (pendingEbibleVersion.value) {
        startDownload(pendingEbibleVersion.value.download_link, pendingEbibleVersion.value);
        pendingEbibleVersion.value = null;
    }
}

function cancelEbibleDownload() {
    showEbibleDialog.value = false;
    pendingEbibleVersion.value = null;
}

function startDownload(downloadLink: string, version: any) {
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
    }, {
        title: version.title,
        description: version.description,
        is_zipped: !!version.is_zipped,
        file_name: version.file_name,
        module_type: version.module_type,
    });
}
</script>
<template>
    <div>
        <!-- PH4.org confirmation dialog -->
        <NModal v-model:show="showPh4Dialog" :mask-closable="false" preset="card" style="max-width: 420px">
            <template #header>
                <div class="flex items-center gap-2">
                    <span class="inline-flex items-center px-1.5 py-0.5 text-[10px] font-700 rounded bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300">
                        PH4.org
                    </span>
                    <span class="font-600">External Module Source</span>
                </div>
            </template>

            <div class="space-y-3 text-sm">
                <p class="opacity-80 leading-relaxed">
                    This module is hosted by
                    <span
                        class="text-green-600 dark:text-green-400 font-600 cursor-pointer hover:underline"
                        @click="openExternal('https://www.ph4.org/')"
                    >PH4.org</span>,
                    a third-party website. Believers Sword does not own, control, or verify the content of externally hosted modules.
                </p>
                <p class="opacity-80 leading-relaxed">
                    By continuing, you confirm that you have the right to download and use this content, and you accept full responsibility for its use.
                </p>
                <div v-if="pendingPh4Version" class="rounded-2 bg-gray-100 dark:bg-dark-400 px-3 py-2 text-xs opacity-70">
                    <span class="font-700">Module:</span> {{ pendingPh4Version.title }}
                </div>
            </div>

            <template #footer>
                <div class="flex justify-end gap-2">
                    <NButton size="small" @click="cancelPh4Download">Cancel</NButton>
                    <NButton size="small" type="primary" @click="confirmPh4Download">
                        Continue
                    </NButton>
                </div>
            </template>
        </NModal>

        <!-- eBible.org confirmation dialog -->
        <NModal v-model:show="showEbibleDialog" :mask-closable="false" preset="card" style="max-width: 420px">
            <template #header>
                <div class="flex items-center gap-2">
                    <span class="inline-flex items-center px-1.5 py-0.5 text-[10px] font-700 rounded bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300">
                        eBible.org
                    </span>
                    <span class="font-600">External Module Source</span>
                </div>
            </template>

            <div class="space-y-3 text-sm">
                <p class="opacity-80 leading-relaxed">
                    This module is hosted by
                    <span
                        class="text-blue-600 dark:text-blue-400 font-600 cursor-pointer hover:underline"
                        @click="openExternal('https://ebible.org/')"
                    >eBible.org</span>,
                    a third-party website. Believers Sword does not own, control, or verify the content of externally hosted modules.
                </p>
                <p class="opacity-80 leading-relaxed">
                    By continuing, you confirm that you have the right to download and use this content, and you accept full responsibility for its use.
                </p>
                <div v-if="pendingEbibleVersion" class="rounded-2 bg-gray-100 dark:bg-dark-400 px-3 py-2 text-xs opacity-70">
                    <span class="font-700">Module:</span> {{ pendingEbibleVersion.title }}
                </div>
            </div>

            <template #footer>
                <div class="flex justify-end gap-2">
                    <NButton size="small" @click="cancelEbibleDownload">Cancel</NButton>
                    <NButton size="small" type="primary" @click="confirmEbibleDownload">
                        Continue
                    </NButton>
                </div>
            </template>
        </NModal>

        <div class="mb-3 rounded-2 border border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-950 px-3 py-2 text-xs text-amber-800 dark:text-amber-300 leading-relaxed">
            Believer's Sword does not own or distribute Bible modules.
            Modules are provided by third-party sources such as
            <span class="font-600 cursor-pointer hover:underline" @click="openExternal('https://www.ph4.org/')">PH4.org</span>.
            Users are responsible for verifying usage rights.
        </div>

        <div class="mb-3 flex gap-2">
            <NInput v-model:value="searchBible" :placeholder="$t('Search versions...')" size="small" clearable class="flex-1" />
            <NSelect
                v-model:value="selectedModuleType"
                :options="moduleTypeOptions"
                size="small"
                to="body"
                style="width: 160px"
                :virtual-scroll="false"
            />
            <NSelect
                v-model:value="selectedLanguage"
                :options="languageOptions"
                size="small"
                filterable
                to="body"
                style="width: 180px"
                :virtual-scroll="false"
            />
        </div>
        <div
            v-if="flatItems.length"
            v-bind="containerProps"
            class="select-none h-[calc(70vh-240px)] overflowing-div pr-2"
        >
            <div v-bind="wrapperProps">
                <template v-for="{ data: item, index } in list" :key="item.key">
                    <!-- Language group header -->
                    <div
                        v-if="item.type === 'header'"
                        :style="{ height: `${HEADER_HEIGHT}px` }"
                        class="bg-gray-100 dark:bg-dark-500 border-b border-gray-200 dark:border-dark-300 flex items-center justify-between px-3 rounded-1"
                    >
                        <h2 class="m-0 text-xs font-700 uppercase tracking-[0.12em] opacity-70">
                            {{ item.language }}
                        </h2>
                        <span class="text-[10px] font-600 opacity-50 bg-gray-200 dark:bg-dark-300 px-1.5 py-0.5 rounded-full">
                            {{ item.count }}
                        </span>
                    </div>

                    <!-- Version card -->
                    <div
                        v-else
                        :style="{ height: `${VERSION_HEIGHT}px` }"
                        :disabled="bibleDownloadStore.isDownloading"
                        class="relative rounded-3 p-2 pr-20 hover:bg-black hover:bg-opacity-4 dark:hover:bg-white dark:hover:bg-opacity-4"
                    >
                        <NButton
                            size="tiny"
                            :disabled="!isAlreadyDownloaded(item.version.file_name) || downloadLoading"
                            :type="!isAlreadyDownloaded(item.version.file_name) ? 'default' : 'info'"
                            @click="clickDownload(item.version.download_link, item.version)"
                            secondary
                            rounded
                            :loading="item.version.download_link === selectedDownloadLink && downloadLoading"
                            class="absolute top-2 right-2"
                        >
                            <NIcon>
                                <Download />
                            </NIcon>
                            <span class="capitalize">{{ isAlreadyDownloaded(item.version.file_name) ? $t('add') : $t('added') }}</span>
                            <span v-if="item.version.download_link === selectedDownloadLink && downloadLoading" class="px-2">
                                {{ downloadPercentage }}%
                            </span>
                        </NButton>

                        <div class="min-w-0">
                            <div class="text-base font-600 leading-tight flex items-center gap-2">
                                <span>{{ item.version.title }}</span>
                                <span
                                    v-if="item.version.module_type === 'ebible'"
                                    class="inline-flex items-center px-1.5 py-0.5 text-[10px] font-600 rounded bg-blue-100 text-blue-600 dark:bg-blue-900 dark:text-blue-300 hover:bg-blue-200 dark:hover:bg-blue-800 cursor-pointer whitespace-nowrap"
                                    @click.stop="openExternal('https://ebible.org/')"
                                >
                                    eBible.org
                                </span>
                                <span
                                    v-else-if="item.version.module_type === 'ph4_mybible'"
                                    class="inline-flex items-center px-1.5 py-0.5 text-[10px] font-600 rounded bg-green-100 text-green-600 dark:bg-green-900 dark:text-green-300 hover:bg-green-200 dark:hover:bg-green-800 cursor-pointer whitespace-nowrap"
                                    @click.stop="openExternal('https://www.ph4.org/')"
                                >
                                    PH4.org
                                </span>
                                <span
                                    v-if="(item.version as any).year"
                                    class="inline-flex items-center px-1.5 py-0.5 text-[10px] font-600 rounded bg-gray-100 text-gray-500 dark:bg-dark-300 dark:text-gray-400 whitespace-nowrap"
                                >
                                    {{ (item.version as any).year }}
                                </span>
                            </div>
                            <div class="mt-1 text-xs opacity-60">
                                <span class="font-700">Short name:</span>
                                {{ item.version.version_short_name_and_date || 'N/A' }}
                            </div>
                            <div class="mt-1 text-sm leading-snug opacity-70 line-clamp-2">
                                {{ formatDescription(item.version.description) }}
                            </div>
                            <div v-if="item.version.copyright" class="mt-1 text-xs opacity-50 line-clamp-1">
                                {{ item.version.copyright }}
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
