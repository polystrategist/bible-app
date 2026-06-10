<script lang="ts" setup>
import { NModal, NInput, NIcon, NButton } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { computed, ref } from 'vue';
import { useModuleStore } from '../../../store/moduleStore';
import { useBibleStore } from '../../../store/BibleStore';
import { useMainStore } from '../../../store/main';
import { bible } from '../../../util/modules';

/**
 * Dialog for choosing the Bible version shown in a reading pane. Replaces the
 * inline dropdown with a richer, searchable card list (title, source, year,
 * short name, description) — enriched from the bundled module catalogue.
 *
 * Versions already open in any pane are hidden, so the list only offers
 * versions the user can actually switch to.
 */
const props = defineProps<{ show: boolean; paneIndex: number }>();
const emit = defineEmits<{
    'update:show': [boolean];
    select: [fileName: string];
}>();

const moduleStore = useModuleStore();
const bibleStore = useBibleStore();
const mainStore = useMainStore();
const search = ref('');

const open = computed({
    get: () => props.show,
    set: (v: boolean) => emit('update:show', v),
});

// Bundled catalogue keyed by file, used to enrich the installed list with
// metadata (language, short name, year, description) the DB record may lack.
const catalogByFile = new Map(bible.map((b) => [b.file_name, b]));

function cleanDescription(description?: string) {
    if (!description) return '';
    return description
        .replace(/<br\s*\/?>/gi, ' ')
        .replace(/<[^>]+>/g, '')
        .replace(/\s+/g, ' ')
        .trim();
}

const versions = computed(() => {
    const selected = new Set(bibleStore.selectedBibleVersions);
    const q = search.value.trim().toLowerCase();

    return moduleStore.bibleLists
        .filter((b: any) => !b.title?.includes('commentaries'))
        // Hide versions already open in a pane.
        .filter((b: any) => !selected.has(b.file_name))
        .map((b: any) => {
            const meta: any = catalogByFile.get(b.file_name) ?? {};
            return {
                fileName: b.file_name,
                title: b.title || meta.title || b.file_name,
                description: cleanDescription(b.description || meta.description),
                shortName: meta.version_short_name_and_date || '',
                language: meta.language_full || b.language_full || '',
                moduleType: meta.module_type || b.module_type || '',
                year: meta.year || b.year || '',
            };
        })
        .filter((v) => {
            if (!q) return true;
            return `${v.title} ${v.shortName} ${v.language} ${v.description}`
                .toLowerCase()
                .includes(q);
        })
        .sort((a, b) => a.title.localeCompare(b.title));
});

function choose(fileName: string) {
    emit('select', fileName);
    open.value = false;
    search.value = '';
}

function openExternal(url: string) {
    window.browserWindow.openExternal(url);
}

// Jump to Settings → Bible → Download so the user can install more versions.
function openDownloadBibles() {
    open.value = false;
    mainStore.settingsTab = 'Bible';
    mainStore.bibleSettingsTab = 'Download';
    mainStore.showSettings = true;
}
</script>

<template>
    <NModal
        v-model:show="open"
        preset="card"
        :bordered="false"
        title="Select Bible Version"
        class="max-w-560px"
        style="width: 92vw"
        :z-index="9000"
    >
        <NInput
            v-model:value="search"
            :placeholder="$t('Search versions...')"
            size="small"
            clearable
            class="mb-3"
        >
            <template #prefix>
                <NIcon><Icon icon="lucide:search" /></NIcon>
            </template>
        </NInput>

        <div class="flex flex-col gap-1 overflowing-div pr-1" style="max-height: 60vh; overflow-y: auto">
            <button
                v-for="v in versions"
                :key="v.fileName"
                type="button"
                class="text-left rounded-3 p-2 transition-colors hover:bg-black hover:bg-opacity-4 dark:hover:bg-white dark:hover:bg-opacity-6 cursor-pointer bg-transparent border-none w-full"
                @click="choose(v.fileName)"
            >
                <div class="text-base font-600 leading-tight flex items-center gap-2 flex-wrap">
                    <span>{{ v.title }}</span>
                    <span
                        v-if="v.moduleType === 'ebible'"
                        class="inline-flex items-center px-1.5 py-0.5 text-[10px] font-600 rounded bg-blue-100 text-blue-600 dark:bg-blue-900 dark:text-blue-300 cursor-pointer whitespace-nowrap"
                        @click.stop="openExternal('https://ebible.org/')"
                    >
                        eBible.org
                    </span>
                    <span
                        v-else-if="v.moduleType === 'ph4_mybible'"
                        class="inline-flex items-center px-1.5 py-0.5 text-[10px] font-600 rounded bg-green-100 text-green-600 dark:bg-green-900 dark:text-green-300 cursor-pointer whitespace-nowrap"
                        @click.stop="openExternal('https://www.ph4.org/')"
                    >
                        PH4.org
                    </span>
                    <span
                        v-if="v.year"
                        class="inline-flex items-center px-1.5 py-0.5 text-[10px] font-600 rounded bg-gray-100 text-gray-500 dark:bg-dark-300 dark:text-gray-400 whitespace-nowrap"
                    >
                        {{ v.year }}
                    </span>
                </div>
                <div v-if="v.shortName || v.language" class="mt-1 text-xs opacity-60">
                    {{ [v.shortName, v.language && (v.language.charAt(0).toUpperCase() + v.language.slice(1))].filter(Boolean).join(' · ') }}
                </div>
                <div v-if="v.description" class="mt-1 text-sm leading-snug opacity-70 line-clamp-2">
                    {{ v.description }}
                </div>
            </button>

            <div v-if="versions.length === 0" class="flex flex-col items-center justify-center gap-2 py-10 text-center">
                <NIcon size="26" class="opacity-55"><Icon icon="lucide:book-open" /></NIcon>
                <p class="m-0 text-sm opacity-55">
                    {{ search ? 'No versions matched your search.' : 'No other installed versions to switch to.' }}
                </p>
                <NButton v-if="!search" size="small" type="primary" secondary class="mt-1" @click="openDownloadBibles">
                    <template #icon><NIcon><Icon icon="lucide:download" /></NIcon></template>
                    Download Bible versions
                </NButton>
            </div>
        </div>

        <template #footer>
            <div class="flex justify-end">
                <NButton size="small" quaternary @click="openDownloadBibles">
                    <template #icon><NIcon><Icon icon="lucide:download" /></NIcon></template>
                    Download more versions
                </NButton>
            </div>
        </template>
    </NModal>
</template>
