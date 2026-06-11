<script lang="ts" setup>
import { NModal, NInput, NIcon, NButton } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { computed, ref } from 'vue';
import { useModuleStore } from '../../../store/moduleStore';
import { useBibleStore } from '../../../store/BibleStore';
import { useMainStore } from '../../../store/main';

/**
 * Dialog for choosing the Bible version shown in a reading pane. Replaces the
 * inline dropdown with a richer, searchable card list — each version shows a
 * short-name avatar, title, source, short name, language and description.
 *
 * Metadata is read from the already-enriched installed list (moduleStore.bibleLists,
 * produced by getDownloadedBible, which merges the API record with the bundled
 * catalogue). When a version carries no short name we derive an abbreviation from
 * its title so every row stays consistent.
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

function cleanDescription(description?: string) {
    if (!description) return '';
    return description
        .replace(/<br\s*\/?>/gi, ' ')
        .replace(/<[^>]+>/g, '')
        .replace(/\s+/g, ' ')
        .trim();
}

function cap(s: string) {
    return s ? s.charAt(0).toUpperCase() + s.slice(1) : '';
}

// Build a versioned short name (e.g. "NIV", "ASD2015") from a title when the
// record has none. Uses the leading letter of each capitalised word plus any
// 4-digit year in the title, falling back to the year field.
function deriveShortName(title: string, year?: string | number) {
    const clean = title.replace(/^[★\s]+/, '').trim();
    const letters = clean
        .split(/[\s\-_]+/)
        .filter((w) => /^[A-Z]/.test(w))
        .map((w) => w[0])
        .join('');
    const yearMatch = clean.match(/\b(1\d{3}|20\d{2})\b/);
    const yr = yearMatch?.[1] ?? (year ? String(year) : '');
    return (letters + yr) || clean.slice(0, 6).toUpperCase();
}

// Compact token for the avatar — acronym letters only, capped to 4 chars.
function abbrOf(shortName: string) {
    const caps = shortName.match(/[A-Z]/g) ?? [];
    if (caps.length >= 2) return caps.join('').slice(0, 4);
    const letters = shortName.match(/[A-Za-z]/g) ?? [];
    return letters.join('').slice(0, 3).toUpperCase();
}

function avatarClass(moduleType: string) {
    if (moduleType === 'ebible') return 'bg-blue-100 text-blue-600 dark:bg-blue-900 dark:bg-opacity-40 dark:text-blue-300';
    if (moduleType === 'ph4_mybible') return 'bg-green-100 text-green-600 dark:bg-green-900 dark:bg-opacity-40 dark:text-green-300';
    return 'bg-indigo-100 text-indigo-600 dark:bg-indigo-900 dark:bg-opacity-40 dark:text-indigo-300';
}

const versions = computed(() => {
    const selected = new Set(bibleStore.selectedBibleVersions);
    const q = search.value.trim().toLowerCase();

    return moduleStore.bibleLists
        .filter((b: any) => !b.title?.includes('commentaries'))
        // Hide versions already open in a pane.
        .filter((b: any) => !selected.has(b.file_name))
        .map((b: any) => {
            const rawTitle = b.title || b.file_name;
            const starred = /^\s*★/.test(rawTitle);
            const title = rawTitle.replace(/^[★\s]+/, '').trim() || b.file_name;
            const year = b.year || '';
            const shortName = (b.short_name || '').trim() || deriveShortName(title, year);
            return {
                fileName: b.file_name,
                title,
                starred,
                shortName,
                abbr: abbrOf(shortName),
                description: cleanDescription(b.description),
                language: cap((b.language || '').trim()),
                moduleType: b.module_type || '',
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

        <div class="flex flex-col gap-2 overflowing-div pr-1" style="max-height: 60vh; overflow-y: auto">
            <button
                v-for="v in versions"
                :key="v.fileName"
                type="button"
                class="group flex items-start gap-3 text-left w-full rounded-lg border-none bg-transparent p-2.5 transition-colors hover:bg-gray-50 dark:hover:bg-dark-400 cursor-pointer"
                @click="choose(v.fileName)"
            >
                <!-- Short-name avatar -->
                <div
                    class="flex-shrink-0 w-11 h-11 rounded-lg flex items-center justify-center font-700 text-xs tracking-wide"
                    :class="avatarClass(v.moduleType)"
                >
                    {{ v.abbr }}
                </div>

                <!-- Body -->
                <div class="min-w-0 flex-1">
                    <div class="flex items-center gap-1.5 leading-tight">
                        <Icon
                            v-if="v.starred"
                            icon="lucide:star"
                            class="text-amber-400 fill-amber-400 flex-shrink-0"
                            width="14"
                            height="14"
                        />
                        <span class="text-sm font-600 truncate text-gray-900 dark:text-gray-100">{{ v.title }}</span>
                        <span
                            v-if="v.moduleType === 'ebible'"
                            class="flex-shrink-0 inline-flex items-center px-1.5 py-0.5 text-[10px] font-600 rounded bg-blue-100 text-blue-600 dark:bg-blue-900 dark:text-blue-300 cursor-pointer whitespace-nowrap"
                            @click.stop="openExternal('https://ebible.org/')"
                        >
                            eBible.org
                        </span>
                        <span
                            v-else-if="v.moduleType === 'ph4_mybible'"
                            class="flex-shrink-0 inline-flex items-center px-1.5 py-0.5 text-[10px] font-600 rounded bg-green-100 text-green-600 dark:bg-green-900 dark:text-green-300 cursor-pointer whitespace-nowrap"
                            @click.stop="openExternal('https://www.ph4.org/')"
                        >
                            PH4.org
                        </span>
                    </div>

                    <div class="mt-0.5 text-xs text-gray-600 dark:text-gray-300 truncate">
                        {{ [v.shortName, v.language].filter(Boolean).join(' · ') }}
                    </div>

                    <div v-if="v.description" class="mt-1 text-xs leading-snug text-gray-500 dark:text-gray-400 line-clamp-1">
                        {{ v.description }}
                    </div>
                </div>

                <NIcon
                    size="16"
                    class="flex-shrink-0 self-center opacity-0 group-hover:opacity-50 transition-opacity"
                >
                    <Icon icon="lucide:chevron-right" />
                </NIcon>
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
