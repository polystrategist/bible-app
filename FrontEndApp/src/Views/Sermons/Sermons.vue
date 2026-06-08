<script lang="ts" setup>
import {
    NButton, NInput, NSelect, NTag, NModal, NSpin, useDialog, useMessage,
} from 'naive-ui';
import { useSermonStore, SermonType } from '../../store/Sermons';
import { useBibleStore } from '../../store/BibleStore';
import { useModuleStore } from '../../store/moduleStore';
import { ref, onBeforeUnmount, onMounted, watch } from 'vue';
import { useInfiniteScroll } from '@vueuse/core';
import { DAYJS } from '../../util/dayjs';
import { useAuthStore } from '../../store/authStore';
import { Icon } from '@iconify/vue';
import { useMenuStore } from '../../store/menu';
import { bible } from '../../util/modules';
import { resolveAvatarUrl } from '../../util/avatar';

const menuStore = useMenuStore();
const authStore = useAuthStore();
const sermonStore = useSermonStore();
const bibleStore = useBibleStore();
const moduleStore = useModuleStore();
const dialog = useDialog();
const message = useMessage();

const browseEl = ref<HTMLElement | null>(null);
const myListEl = ref<HTMLElement | null>(null);
const activeTab = ref<'browse' | 'mine' | 'favorites'>('browse');
const selectedSermon = ref<SermonType | null>(null);
const showDetailModal = ref(false);
const viewDelayMs = 7000;
const viewTimer = ref<ReturnType<typeof setTimeout> | null>(null);
const scriptureLoading = ref(false);
type ScriptureVerseVersion = {
    version: string;
    versionCode: string;
    text: string;
};
type ScriptureVerseGroup = {
    key: string;
    refLabel: string;
    versions: ScriptureVerseVersion[];
};
const scriptureVerseGroups = ref<ScriptureVerseGroup[]>([]);
const scriptureVersionIndexes = ref<Record<string, number>>({});
let scriptureLoadToken = 0;

useInfiniteScroll(browseEl as any, () => {
    if (sermonStore.hasMoreFeed && !sermonStore.loading) sermonStore.page++;
}, { distance: 120 });

useInfiniteScroll(myListEl as any, () => {
    if (sermonStore.hasMoreMine && !sermonStore.myLoading) sermonStore.myPage++;
}, { distance: 120 });

onMounted(() => {
    // isAuthenticated may still be false here because App.vue calls initAuth()
    // in its own onMounted which fires AFTER children. The watcher below handles
    // the deferred case.
    if (authStore.isAuthenticated) sermonStore.getMySermons(true);
    document.addEventListener('visibilitychange', handleVisibilityChange);
});

watch(() => authStore.isAuthenticated, (authenticated) => {
    if (authenticated) sermonStore.getMySermons(true);
});

watch(() => sermonStore.requestedTab, (tab) => {
    if (tab) {
        activeTab.value = tab;
        sermonStore.requestedTab = null;
    }
});

function openDetail(sermon: SermonType) {
    selectedSermon.value = sermon;
    showDetailModal.value = true;
    scheduleSermonView(sermon);
    loadSermonScripture(sermon);
}

function clearSermonViewTimer() {
    if (!viewTimer.value) return;
    clearTimeout(viewTimer.value);
    viewTimer.value = null;
}

function scheduleSermonView(sermon: SermonType) {
    clearSermonViewTimer();
    if (document.hidden) return;

    viewTimer.value = setTimeout(async () => {
        viewTimer.value = null;
        if (document.hidden || !showDetailModal.value || selectedSermon.value?.id !== sermon.id) return;

        const result = await sermonStore.recordSermonView(sermon.id);
        if (result.sermon && selectedSermon.value?.id === result.sermon.id) {
            selectedSermon.value = result.sermon;
        }
    }, viewDelayMs);
}

function handleVisibilityChange() {
    if (document.hidden) {
        clearSermonViewTimer();
        return;
    }

    if (showDetailModal.value && selectedSermon.value) {
        scheduleSermonView(selectedSermon.value);
    }
}

function handleDelete(sermon: SermonType) {
    dialog.warning({
        title: 'Delete Sermon',
        content: `Delete "${sermon.title}"? This cannot be undone.`,
        positiveText: 'Delete',
        negativeText: 'Cancel',
        onPositiveClick: async () => {
            const result = await sermonStore.deleteSermon(sermon.id);
            if (result.success) message.success('Sermon deleted.');
            else message.error(result.message ?? 'Failed to delete.');
        },
    });
}

function handlePublish(sermon: SermonType) {
    dialog.warning({
        title: 'Publish Sermon',
        content: `Publish "${sermon.title}"? It will be visible to everyone.`,
        positiveText: 'Publish',
        negativeText: 'Cancel',
        onPositiveClick: async () => {
            const result = await sermonStore.updateSermon(sermon.id, { status: 'published' });
            if (result.success) message.success('Sermon published!');
            else message.error(result.message ?? 'Failed to publish.');
        },
    });
}

function selectCategory(id: number | null) {
    sermonStore.categoryFilter = id;
    sermonStore.getSermons(true);
}

const sortOptions = [
    { label: 'Most Recent', value: 'recent' },
    { label: 'Most Popular', value: 'popular' },
    { label: 'Oldest', value: 'oldest' },
];

const myStatusOptions = [
    { label: 'All Statuses', value: '' },
    { label: 'Draft', value: 'draft' },
    { label: 'Published', value: 'published' },
    { label: 'Archived', value: 'archived' },
];

function formatDate(d: string | null) {
    if (!d) return '';
    return DAYJS(d).format('MMM D, YYYY');
}

function editSermon(sermon: SermonType) {
    sermonStore.editingSermon = sermon;
    menuStore.setMenu(`/create-sermon?edit=${sermon.id}`);
}

const BOOK_NAMES: Record<number, string> = {
    10:'Genesis',20:'Exodus',30:'Leviticus',40:'Numbers',50:'Deuteronomy',
    60:'Joshua',70:'Judges',80:'Ruth',90:'1 Samuel',100:'2 Samuel',
    110:'1 Kings',120:'2 Kings',130:'1 Chronicles',140:'2 Chronicles',
    150:'Ezra',160:'Nehemiah',180:'Esther',220:'Job',230:'Psalms',
    240:'Proverbs',250:'Ecclesiastes',260:'Song of Solomon',290:'Isaiah',
    300:'Jeremiah',310:'Lamentations',330:'Ezekiel',340:'Daniel',
    350:'Hosea',360:'Joel',370:'Amos',380:'Obadiah',390:'Jonah',
    400:'Micah',410:'Nahum',420:'Habakkuk',430:'Zephaniah',440:'Haggai',
    450:'Zechariah',460:'Malachi',470:'Matthew',480:'Mark',490:'Luke',
    500:'John',510:'Acts',520:'Romans',530:'1 Corinthians',540:'2 Corinthians',
    550:'Galatians',560:'Ephesians',570:'Philippians',580:'Colossians',
    590:'1 Thessalonians',600:'2 Thessalonians',610:'1 Timothy',620:'2 Timothy',
    630:'Titus',640:'Philemon',650:'Hebrews',660:'James',670:'1 Peter',
    680:'2 Peter',690:'1 John',700:'2 John',710:'3 John',720:'Jude',730:'Revelation',
};
function bookName(n: number) { return BOOK_NAMES[n] ?? `Book ${n}`; }

function scriptureRefLabel(book: number, chapter: number, verse: number) {
    return `${bookName(book)} ${chapter}:${verse}`;
}

function hasVisibleText(html: string) {
    return html.replace(/<[^>]*>/g, '').trim().length > 0;
}

// Strip MyBible code-style markup (Strong's numbers, morphology, footnotes,
// annotations) so the sermon dialog shows clean prose. Keeps formatting tags
// like <J>, <i>, <e>, <br/>.
function cleanScriptureHtml(html: string) {
    return html
        .replace(/<(S|m|n|f)\b[^>]*>[\s\S]*?<\/\1>/gi, '')
        .replace(/<(S|m|n|f)\b[^>]*\/>/gi, '')
        .replace(/\s+([,.;:!?])/g, '$1')
        .replace(/\s{2,}/g, ' ')
        .trim();
}

function versionShortCode(fileName: string) {
    const installed = moduleStore.bibleLists.find((item: any) => item.file_name === fileName);
    const meta = bible.find((item) => item.file_name === fileName);
    const shortCode = installed?.short_name || meta?.version_short_name_and_date;

    if (shortCode) return shortCode;

    return fileName
        .replace(/\.(SQLite3|sqlite3|db)$/i, '')
        .replace(/^ph4_mybible_/i, '')
        .replace(/^ebible-/i, '')
        .split(/[\s_-]+/)
        .map((part) => part[0])
        .join('')
        .slice(0, 10)
        .toUpperCase();
}

async function loadSermonScripture(sermon: SermonType) {
    const refs = sermon.main_scripture ?? [];
    const versions = [...bibleStore.selectedBibleVersions];
    const token = ++scriptureLoadToken;
    scriptureVerseGroups.value = [];
    scriptureVersionIndexes.value = {};

    if (!refs.length || !versions.length) return;

    scriptureLoading.value = true;
    try {
        const verseRequests = refs.flatMap((ref) =>
            (ref.verse ?? []).map((verse) => ({
                book: ref.book,
                chapter: ref.chapter,
                verse,
                refLabel: scriptureRefLabel(ref.book, ref.chapter, verse),
            }))
        );

        const rows = await Promise.all(
            verseRequests.map(async (request) => {
                try {
                    const results = await window.browserWindow.getVerseText({
                        bible_versions: versions,
                        book_number: request.book,
                        chapter: request.chapter,
                        verse: request.verse,
                    });

                    const versionRows = results
                        .map((item) => ({
                            version: item.version,
                            versionCode: versionShortCode(item.version),
                            text: cleanScriptureHtml(item.text ?? ''),
                        }))
                        .filter((row) => hasVisibleText(row.text));

                    return {
                        key: `${request.book}-${request.chapter}-${request.verse}`,
                        refLabel: request.refLabel,
                        versions: versionRows,
                    };
                } catch (error) {
                    console.error('getVerseText failed:', error);
                    return null;
                }
            })
        );

        if (token === scriptureLoadToken) {
            scriptureVerseGroups.value = rows.filter(
                (row): row is ScriptureVerseGroup => !!row && row.versions.length > 0
            );
        }
    } finally {
        if (token === scriptureLoadToken) scriptureLoading.value = false;
    }
}

function scriptureVersionIndex(group: ScriptureVerseGroup) {
    const index = scriptureVersionIndexes.value[group.key] ?? 0;
    return Math.min(index, Math.max(group.versions.length - 1, 0));
}

function activeScriptureVersion(group: ScriptureVerseGroup) {
    return group.versions[scriptureVersionIndex(group)];
}

function shiftScriptureVersion(group: ScriptureVerseGroup, direction: -1 | 1) {
    if (group.versions.length < 2) return;

    const current = scriptureVersionIndex(group);
    const next = (current + direction + group.versions.length) % group.versions.length;
    scriptureVersionIndexes.value = {
        ...scriptureVersionIndexes.value,
        [group.key]: next,
    };
}

function creatorAvatarUrl(creator?: SermonType['creator']): string | null {
    return resolveAvatarUrl(creator?.info?.profile_picture ?? null, 25);
}

function creatorInitials(creator?: SermonType['creator']): string {
    if (!creator?.name) return '?';
    return creator.name.split(' ').map((w) => w[0]).slice(0, 2).join('').toUpperCase();
}

function viewLabel(count: number | null | undefined) {
    const n = count ?? 0;
    return `${n.toLocaleString()} ${n === 1 ? 'view' : 'views'}`;
}

watch(showDetailModal, (showing) => {
    if (showing) return;
    clearSermonViewTimer();
    scriptureLoadToken++;
    scriptureLoading.value = false;
    scriptureVerseGroups.value = [];
    scriptureVersionIndexes.value = {};
});

watch(() => [...bibleStore.selectedBibleVersions], () => {
    if (showDetailModal.value && selectedSermon.value) {
        loadSermonScripture(selectedSermon.value);
    }
});

onBeforeUnmount(() => {
    clearSermonViewTimer();
    document.removeEventListener('visibilitychange', handleVisibilityChange);
});
</script>

<template>
    <div class="sermons-root">

        <!-- ═══ PAGE HEADER ═══ -->
        <div class="page-header">
            <div>
                <h1 class="page-title">{{ $t('Sermons') }}</h1>
                <p class="page-subtitle">Browse and share messages from the community</p>
            </div>
            <NButton
                v-if="authStore.isAuthenticated"
                type="primary"
                size="small"
                @click="menuStore.setMenu('/create-sermon')"
            >
                <template #icon><Icon icon="mdi:plus" /></template>
                Share a Sermon
            </NButton>
            <NButton v-else size="small" @click="menuStore.setMenu('/profile')">
                <template #icon><Icon icon="mdi:login" /></template>
                Sign In
            </NButton>
        </div>

        <!-- ═══ TAB BAR ═══ -->
        <div class="tab-bar">
            <button
                class="tab-btn"
                :class="{ active: activeTab === 'browse' }"
                @click="activeTab = 'browse'"
            >
                <Icon icon="mdi:earth" class="mr-1" />Browse
            </button>
            <button
                class="tab-btn"
                :class="{ active: activeTab === 'mine' }"
                @click="activeTab = 'mine'"
            >
                <Icon icon="mdi:account-edit" class="mr-1" />My Sermons
                <span v-if="authStore.isAuthenticated && sermonStore.mySermons.length"
                      class="tab-count">{{ sermonStore.mySermons.length }}</span>
            </button>
            <button
                class="tab-btn"
                :class="{ active: activeTab === 'favorites' }"
                @click="activeTab = 'favorites'"
            >
                <Icon icon="mdi:star" class="mr-1" />Favorites
                <span v-if="sermonStore.favorites.length" class="tab-count">{{ sermonStore.favorites.length }}</span>
            </button>
        </div>

        <!-- Offline / stale banner — visible above all tabs when feed is stale. -->
        <div
            v-if="activeTab === 'browse' && (sermonStore.feedStatus === 'staleOffline' || sermonStore.feedStatus === 'staleError')"
            class="stale-banner"
        >
            <Icon :icon="sermonStore.feedStatus === 'staleOffline' ? 'mdi:wifi-off' : 'mdi:cloud-off-outline'" />
            <span>
                {{ sermonStore.feedStatus === 'staleOffline'
                    ? "You're offline — showing saved sermons."
                    : "Couldn't reach the server — showing saved sermons." }}
            </span>
        </div>

        <!-- ═══════════════ BROWSE TAB ═══════════════ -->
        <div v-show="activeTab === 'browse'" class="tab-content">

            <!-- Toolbar -->
            <div class="browse-toolbar">
                <NInput
                    v-model:value="sermonStore.search"
                    placeholder="Search sermons…"
                    size="small"
                    clearable
                    class="browse-search"
                    @keydown.enter="sermonStore.getSermons(true)"
                >
                    <template #prefix><Icon icon="mdi:magnify" class="opacity-50" /></template>
                </NInput>
                <NButton size="small" type="primary" ghost @click="sermonStore.getSermons(true)" :loading="sermonStore.loading">
                    Search
                </NButton>
                <NSelect
                    v-model:value="sermonStore.sort"
                    :options="sortOptions"
                    size="small"
                    class="!w-150px"
                    @update:value="sermonStore.getSermons(true)"
                />
                <NButton
                    size="small"
                    secondary
                    :loading="sermonStore.loading"
                    @click="sermonStore.getSermons(true)"
                >
                    <template #icon><Icon icon="mdi:refresh" /></template>
                </NButton>
            </div>

            <!-- Category pills -->
            <div class="category-pills" v-if="sermonStore.categories.length">
                <button
                    class="cat-pill"
                    :class="{ active: sermonStore.categoryFilter === null }"
                    @click="selectCategory(null)"
                >All</button>
                <button
                    v-for="cat in sermonStore.categories"
                    :key="cat.id"
                    class="cat-pill"
                    :class="{ active: sermonStore.categoryFilter === cat.id }"
                    @click="selectCategory(cat.id)"
                >{{ cat.name }}</button>
            </div>

            <!-- Sermon grid -->
            <div ref="browseEl" class="sermon-grid-scroll">

                <!-- Initial loading -->
                <div v-if="sermonStore.loading && !sermonStore.sermons.length" class="empty-state">
                    <NSpin size="large" />
                </div>

                <!-- Empty -->
                <div v-else-if="!sermonStore.loading && !sermonStore.sermons.length" class="empty-state">
                    <Icon icon="mdi:book-open-blank-variant-outline" class="empty-icon" />
                    <p class="empty-title">No sermons yet</p>
                    <p class="empty-sub">Be the first to share a sermon with the community!</p>
                    <NButton v-if="authStore.isAuthenticated" type="primary" size="small"
                             @click="menuStore.setMenu('/create-sermon')">
                        Share a Sermon
                    </NButton>
                </div>

                <!-- Cards -->
                <div v-else class="sermon-grid">
                    <div
                        v-for="sermon in sermonStore.sermons"
                        :key="sermon.id"
                        class="sermon-card"
                        @click="openDetail(sermon)"
                    >
                        <!-- Thumbnail -->
                        <div class="card-thumb">
                            <img v-if="sermon.thumbnail_url" :src="sermon.thumbnail_url" :alt="sermon.title" />
                            <div v-else class="card-thumb-placeholder">
                                <Icon icon="mdi:book-cross" class="text-4xl opacity-30" />
                            </div>
                            <NTag v-if="sermon.category" class="card-cat-badge" size="tiny" :bordered="false" type="info">
                                {{ sermon.category.name }}
                            </NTag>
                            <div v-if="sermon.video_url" class="card-media-badge">
                                <Icon icon="mdi:play-circle" />
                            </div>
                            <button
                                type="button"
                                class="card-fav-btn"
                                :class="{ active: sermonStore.isFavorite(sermon.id) }"
                                :title="sermonStore.isFavorite(sermon.id) ? 'Remove from favorites' : 'Add to favorites'"
                                @click.stop="sermonStore.toggleFavorite(sermon)"
                            >
                                <Icon :icon="sermonStore.isFavorite(sermon.id) ? 'mdi:star' : 'mdi:star-outline'" />
                            </button>
                        </div>

                        <!-- Body -->
                        <div class="card-body">
                            <h3 class="card-title">{{ sermon.title }}</h3>
                            <p class="card-summary">{{ sermon.short_summary }}</p>
                            <div class="card-meta">
                                <span v-if="sermon.preacher_name || sermon.creator" class="creator-meta">
                                    <span class="creator-avatar">
                                        <img v-if="creatorAvatarUrl(sermon.creator)" :src="creatorAvatarUrl(sermon.creator) ?? undefined" />
                                        <span v-else>{{ creatorInitials(sermon.creator) }}</span>
                                    </span>
                                    <span v-if="sermon.creator?.username">@{{ sermon.creator.username }}</span>
                                    <span v-else>{{ sermon.preacher_name || sermon.creator?.name }}</span>
                                </span>
                                <span v-if="sermon.sermon_date">
                                    <Icon icon="mdi:calendar-blank-outline" class="inline mr-0.5" />
                                    {{ formatDate(sermon.sermon_date) }}
                                </span>
                                <span>
                                    <Icon icon="mdi:eye-outline" class="inline mr-0.5" />
                                    {{ sermon.view_count }}
                                </span>
                            </div>
                            <div v-if="sermon.tags?.length" class="card-tags">
                                <span v-for="tag in sermon.tags.slice(0, 3)" :key="tag" class="card-tag">#{{ tag }}</span>
                            </div>
                        </div>
                    </div>

                    <!-- Load-more spinner -->
                    <div v-if="sermonStore.loading" class="col-span-full flex justify-center py-4">
                        <NSpin size="small" />
                    </div>
                </div>
            </div>
        </div>

        <!-- ═══════════════ MY SERMONS TAB ═══════════════ -->
        <div v-show="activeTab === 'mine'" class="tab-content">

            <!-- Not signed in -->
            <div v-if="!authStore.isAuthenticated" class="empty-state">
                <Icon icon="mdi:lock-outline" class="empty-icon" />
                <p class="empty-title">Sign in to manage your sermons</p>
                <NButton type="primary" @click="menuStore.setMenu('/profile')">Sign In</NButton>
            </div>

            <template v-else>
                <!-- Toolbar -->
                <div class="browse-toolbar">
                    <NInput
                        v-model:value="sermonStore.mySearch"
                        placeholder="Search my sermons…"
                        size="small"
                        clearable
                        class="browse-search"
                        @keydown.enter="sermonStore.getMySermons(true)"
                    >
                        <template #prefix><Icon icon="mdi:magnify" class="opacity-50" /></template>
                    </NInput>
                    <NSelect
                        v-model:value="sermonStore.myStatusFilter"
                        :options="myStatusOptions"
                        size="small"
                        class="!w-150px"
                        @update:value="sermonStore.getMySermons(true)"
                    />
                    <NButton size="small" type="primary" @click="menuStore.setMenu('/create-sermon')">
                        <template #icon><Icon icon="mdi:plus" /></template>
                        New Sermon
                    </NButton>
                </div>

                <div ref="myListEl" class="sermon-grid-scroll">
                    <div v-if="sermonStore.myLoading && !sermonStore.mySermons.length" class="empty-state">
                        <NSpin size="large" />
                    </div>
                    <div v-else-if="!sermonStore.myLoading && !sermonStore.mySermons.length" class="empty-state">
                        <Icon icon="mdi:pencil-plus-outline" class="empty-icon" />
                        <p class="empty-title">No sermons yet</p>
                        <NButton type="primary" size="small" @click="menuStore.setMenu('/create-sermon')">
                            Write your first sermon
                        </NButton>
                    </div>

                    <div v-else class="sermon-grid">
                        <div
                            v-for="sermon in sermonStore.mySermons"
                            :key="sermon.id"
                            class="sermon-card"
                            @click="openDetail(sermon)"
                        >
                            <!-- Thumbnail -->
                            <div class="card-thumb">
                                <img v-if="sermon.thumbnail_url" :src="sermon.thumbnail_url" :alt="sermon.title" />
                                <div v-else class="card-thumb-placeholder">
                                    <Icon icon="mdi:book-cross" class="text-4xl opacity-30" />
                                </div>
                                <NTag
                                    class="card-cat-badge"
                                    size="tiny"
                                    :bordered="false"
                                    :type="sermon.status === 'published' ? 'success' : sermon.status === 'draft' ? 'warning' : 'default'"
                                >
                                    {{ sermon.status }}
                                </NTag>
                                <NTag v-if="sermon.category" class="card-cat-badge-right" size="tiny" :bordered="false" type="info">
                                    {{ sermon.category.name }}
                                </NTag>
                            </div>
                            <!-- Body -->
                            <div class="card-body">
                                <h3 class="card-title">{{ sermon.title }}</h3>
                                <p class="card-summary">{{ sermon.short_summary }}</p>
                                <div class="card-meta">
                                    <span v-if="sermon.sermon_date">
                                        <Icon icon="mdi:calendar-blank-outline" class="inline mr-0.5" />
                                        {{ formatDate(sermon.sermon_date) }}
                                    </span>
                                    <span>
                                        <Icon icon="mdi:eye-outline" class="inline mr-0.5" />
                                        {{ sermon.view_count }}
                                    </span>
                                </div>
                            </div>
                            <!-- Actions -->
                            <div class="my-card-actions" @click.stop>
                                <NButton size="tiny" secondary @click="editSermon(sermon)">
                                    <template #icon><Icon icon="mdi:pencil-outline" /></template>
                                    Edit
                                </NButton>
                                <NButton
                                    v-if="sermon.status === 'draft'"
                                    size="tiny"
                                    type="success"
                                    secondary
                                    @click="handlePublish(sermon)"
                                >
                                    <template #icon><Icon icon="mdi:publish" /></template>
                                    Publish
                                </NButton>
                                <NButton size="tiny" type="error" secondary @click="handleDelete(sermon)">
                                    <template #icon><Icon icon="mdi:trash-can-outline" /></template>
                                    Delete
                                </NButton>
                            </div>
                        </div>
                        <div v-if="sermonStore.myLoading" class="col-span-full flex justify-center py-4">
                            <NSpin size="small" />
                        </div>
                    </div>
                </div>
            </template>
        </div>

        <!-- ═══════════════ FAVORITES TAB ═══════════════ -->
        <div v-show="activeTab === 'favorites'" class="tab-content">
            <div v-if="!sermonStore.favorites.length" class="empty-state">
                <Icon icon="mdi:star-outline" class="empty-icon" />
                <p class="empty-title">No favorites yet</p>
                <p class="empty-sub">Tap the star on a sermon to save it here for offline reading.</p>
            </div>
            <div v-else class="sermon-grid-scroll">
                <div class="sermon-grid">
                    <div
                        v-for="sermon in sermonStore.favorites"
                        :key="sermon.id"
                        class="sermon-card"
                        @click="openDetail(sermon)"
                    >
                        <div class="card-thumb">
                            <img v-if="sermon.thumbnail_url" :src="sermon.thumbnail_url" :alt="sermon.title" />
                            <div v-else class="card-thumb-placeholder">
                                <Icon icon="mdi:book-cross" class="text-4xl opacity-30" />
                            </div>
                            <button
                                type="button"
                                class="absolute top-1 right-1 w-32px h-32px rounded-full bg-black/55 flex items-center justify-center text-yellow-400 hover:bg-black/75"
                                title="Remove from favorites"
                                @click.stop="sermonStore.toggleFavorite(sermon)"
                            >
                                <Icon icon="mdi:star" width="20" />
                            </button>
                        </div>
                        <div class="card-body">
                            <h3 class="card-title">{{ sermon.title }}</h3>
                            <p class="card-summary">{{ sermon.short_summary }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ═══════════════ DETAIL MODAL ═══════════════ -->
        <NModal
            v-model:show="showDetailModal"
            preset="card"
            :title="selectedSermon?.title ?? ''"
            class="sermon-detail-modal !max-w-1120px !w-[94vw]"
            :bordered="false"
        >
            <div v-if="selectedSermon" class="detail-body">
                <img
                    v-if="selectedSermon.thumbnail_url"
                    :src="selectedSermon.thumbnail_url"
                    :alt="selectedSermon.title"
                    class="detail-hero"
                />

                <div class="detail-layout">
                    <div class="detail-main">
                        <div v-if="selectedSermon.video_url || selectedSermon.audio_url" class="detail-actions">
                            <a v-if="selectedSermon.video_url" :href="selectedSermon.video_url" target="_blank" rel="noopener">
                                <NButton size="small" type="info">
                                    <template #icon><Icon icon="mdi:play-circle-outline" /></template>
                                    Watch Video
                                </NButton>
                            </a>
                            <a v-if="selectedSermon.audio_url" :href="selectedSermon.audio_url" target="_blank" rel="noopener">
                                <NButton size="small">
                                    <template #icon><Icon icon="mdi:headphones" /></template>
                                    Listen
                                </NButton>
                            </a>
                        </div>

                        <div class="detail-content" v-html="selectedSermon.content" />

                        <div v-if="selectedSermon.tags?.length" class="detail-tags">
                            <span v-for="tag in selectedSermon.tags" :key="tag" class="detail-tag">#{{ tag }}</span>
                        </div>
                    </div>

                    <aside class="detail-sidebar">
                        <div class="detail-header">
                            <div class="detail-meta">
                                <span v-if="selectedSermon.preacher_name || selectedSermon.creator" class="detail-meta-item">
                                    <Icon icon="mdi:account-tie" />
                                    {{ selectedSermon.preacher_name || selectedSermon.creator?.name }}
                                </span>
                                <span v-if="selectedSermon.sermon_date" class="detail-meta-item">
                                    <Icon icon="mdi:calendar-blank-outline" />
                                    {{ formatDate(selectedSermon.sermon_date) }}
                                </span>
                                <span class="detail-meta-item detail-view-count">
                                    <Icon icon="mdi:eye-outline" />
                                    {{ viewLabel(selectedSermon.view_count) }}
                                </span>
                            </div>

                            <div class="detail-badges">
                                <NTag v-if="selectedSermon.category" size="small" :bordered="false" type="info">
                                    {{ selectedSermon.category.name }}
                                </NTag>
                                <NTag v-if="selectedSermon.series" size="small" :bordered="false">
                                    <template #icon><Icon icon="mdi:playlist-play" /></template>
                                    {{ selectedSermon.series.title }}
                                </NTag>
                            </div>

                            <p class="detail-summary">{{ selectedSermon.short_summary }}</p>

                            <div v-if="selectedSermon.main_scripture?.length" class="detail-scripture">
                                <Icon icon="mdi:book-open-variant" class="detail-scripture-icon" />
                                <span class="detail-scripture-label">Scripture</span>
                                <span v-for="(s, i) in selectedSermon.main_scripture" :key="i">
                                    {{ bookName(s.book) }} {{ s.chapter }}<span v-if="s.verse.length">:{{ s.verse.join(', ') }}</span>
                                    <span v-if="i < selectedSermon.main_scripture!.length - 1"> · </span>
                                </span>
                            </div>

                            <div v-if="selectedSermon.main_scripture?.length" class="detail-verse-preview">
                                <div v-if="scriptureLoading" class="detail-verse-loading">
                                    <NSpin size="small" />
                                </div>

                                <div v-else-if="scriptureVerseGroups.length" class="detail-verse-list">
                                    <div
                                        v-for="group in scriptureVerseGroups"
                                        :key="group.key"
                                        class="detail-verse-row"
                                    >
                                        <div class="detail-verse-line">
                                            <span class="detail-version-code">{{ activeScriptureVersion(group).versionCode }}</span>
                                            <span class="detail-verse-ref">{{ group.refLabel }}</span>
                                            <div v-if="group.versions.length > 1" class="detail-verse-pager">
                                                <button
                                                    type="button"
                                                    class="detail-verse-pager-btn"
                                                    @click="shiftScriptureVersion(group, -1)"
                                                >
                                                    <Icon icon="mdi:chevron-left" />
                                                </button>
                                                <span class="detail-verse-pager-count">
                                                    {{ scriptureVersionIndex(group) + 1 }}/{{ group.versions.length }}
                                                </span>
                                                <button
                                                    type="button"
                                                    class="detail-verse-pager-btn"
                                                    @click="shiftScriptureVersion(group, 1)"
                                                >
                                                    <Icon icon="mdi:chevron-right" />
                                                </button>
                                            </div>
                                        </div>
                                        <div class="detail-verse-text" v-html="activeScriptureVersion(group).text" />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </aside>
                </div>
            </div>
        </NModal>
    </div>
</template>

<style scoped>
/* ── Root ── */
.sermons-root {
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: hidden;
    padding-left: 15px;
}

/* ── Header ── */
.page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 20px 0;
    flex-shrink: 0;
}
.page-title {
    font-size: 22px;
    font-weight: 800;
    margin: 0 0 2px;
    line-height: 1.2;
}
.page-subtitle {
    font-size: 12px;
    opacity: 0.5;
    margin: 0;
}

/* ── Tabs ── */
.tab-bar {
    display: flex;
    gap: 2px;
    padding: 10px 20px 0;
    border-bottom: 1px solid var(--theme-border, rgba(255,255,255,0.07));
    flex-shrink: 0;
}
.tab-btn {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 6px 14px 10px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    background: none;
    border: none;
    color: inherit;
    opacity: 0.5;
    border-bottom: 2px solid transparent;
    margin-bottom: -1px;
    transition: opacity 0.15s, border-color 0.15s;
}
.tab-btn:hover { opacity: 0.8; }
.tab-btn.active {
    opacity: 1;
    border-bottom-color: var(--primary-color, #6f84ff);
    color: var(--primary-color, #6f84ff);
}
.tab-count {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 18px;
    height: 18px;
    padding: 0 5px;
    border-radius: 999px;
    background: color-mix(in srgb, var(--primary-color, #6f84ff) 18%, transparent);
    color: var(--primary-color, #6f84ff);
    font-size: 10px;
    font-weight: 700;
}

/* ── Tab content wrapper ── */
.tab-content {
    display: flex;
    flex-direction: column;
    flex: 1;
    min-height: 0;
    padding: 12px 16px 0;
}

/* ── Toolbar ── */
.browse-toolbar {
    display: flex;
    gap: 8px;
    align-items: center;
    margin-bottom: 10px;
    flex-wrap: wrap;
}
.browse-search { flex: 1; min-width: 180px; max-width: 320px; }

/* ── Category pills ── */
.category-pills {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    margin-bottom: 12px;
}
.cat-pill {
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    background: var(--theme-bg-soft, rgba(255,255,255,0.06));
    border: 1px solid var(--theme-border, rgba(255,255,255,0.1));
    color: inherit;
    transition: background 0.15s, border-color 0.15s;
    white-space: nowrap;
}
.cat-pill:hover { background: var(--theme-bg-elevated, rgba(255,255,255,0.1)); }
.cat-pill.active {
    background: color-mix(in srgb, var(--primary-color, #6f84ff) 20%, transparent);
    border-color: color-mix(in srgb, var(--primary-color, #6f84ff) 60%, transparent);
    color: var(--primary-color, #6f84ff);
}

/* ── Scrollable area ── */
.sermon-grid-scroll {
    flex: 1;
    overflow-y: auto;
    /* Breathing room so the cards' hover lift + shadow aren't clipped by the
       scroll container's edges (overflow-y:auto also clips the x-axis). */
    padding: 4px 4px 16px;
}
.sermon-grid-scroll::-webkit-scrollbar { width: 4px; }
.sermon-grid-scroll::-webkit-scrollbar-thumb { background: var(--scrollbar-thumb, rgba(255,255,255,0.16)); border-radius: 4px; }

/* ── Sermon grid ── */
.sermon-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 14px;
}

/* ── Sermon card ── */
.sermon-card {
    border-radius: 14px;
    overflow: hidden;
    background: var(--theme-bg-soft, rgba(255,255,255,0.04));
    border: 1px solid var(--theme-border, rgba(255,255,255,0.07));
    cursor: pointer;
    transition: transform 0.15s, box-shadow 0.15s, background 0.15s;
    display: flex;
    flex-direction: column;
}
.sermon-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.18);
    background: var(--theme-bg-elevated, rgba(255,255,255,0.07));
}
.card-thumb {
    width: 100%;
    aspect-ratio: 16 / 9;
    position: relative;
    overflow: hidden;
    background: var(--theme-bg-elevated, rgba(255,255,255,0.05));
    flex-shrink: 0;
}
.card-thumb img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.2s;
}
.sermon-card:hover .card-thumb img { transform: scale(1.04); }
.card-thumb-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, rgba(111,132,255,0.1), rgba(95,176,255,0.06));
}
.card-cat-badge {
    position: absolute;
    top: 8px;
    left: 8px;
}
.card-media-badge {
    position: absolute;
    bottom: 8px;
    right: 8px;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: rgba(0,0,0,0.55);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    color: #fff;
}
.card-body {
    padding: 12px;
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 4px;
}
.card-title {
    font-size: 14px;
    font-weight: 700;
    margin: 0;
    line-height: 1.35;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.card-summary {
    font-size: 12px;
    opacity: 0.65;
    margin: 0;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    flex: 1;
}
.card-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    font-size: 11px;
    opacity: 0.55;
    margin-top: 4px;
}
.card-tags { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 4px; }
.card-tag {
    font-size: 11px;
    opacity: 0.55;
}
.creator-meta {
    display: inline-flex;
    align-items: center;
    gap: 5px;
}
.creator-avatar {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #7c6af7;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 9px;
    font-weight: 700;
    color: white;
    overflow: hidden;
    flex-shrink: 0;
}
.creator-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

/* ── My Sermons card actions ── */
.my-card-actions {
    display: flex;
    gap: 6px;
    padding: 0 10px 10px;
    flex-wrap: wrap;
}
.card-cat-badge-right {
    position: absolute;
    top: 8px;
    right: 8px;
}

/* ── Empty state ── */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 60px 20px;
    opacity: 0.6;
}
.empty-icon { font-size: 52px; opacity: 0.5; }
.empty-title { font-size: 16px; font-weight: 700; margin: 0; }
.empty-sub { font-size: 13px; margin: 0; text-align: center; max-width: 280px; opacity: 0.7; }

/* ── Detail modal ── */
.sermon-detail-modal :deep(.n-card) {
    background: var(--theme-bg-elevated, #30304f);
    border: 1px solid var(--theme-border, rgba(255,255,255,0.12));
    box-shadow: 0 24px 60px rgba(0,0,0,0.36);
    overflow: hidden;
}
.sermon-detail-modal :deep(.n-card-header) {
    padding: 20px 24px 16px;
    border-bottom: 1px solid var(--theme-border, rgba(255,255,255,0.08));
}
.sermon-detail-modal :deep(.n-card-header__main) {
    color: var(--theme-text, inherit);
    font-size: 19px;
    font-weight: 800;
    line-height: 1.35;
}
.sermon-detail-modal :deep(.n-card__content) {
    padding: 0;
}
.detail-body {
    display: flex;
    flex-direction: column;
    max-height: min(78vh, 760px);
    color: var(--theme-text, inherit);
    overflow: hidden;
}
.detail-hero {
    width: 100%;
    max-height: 240px;
    object-fit: cover;
    border-bottom: 1px solid var(--theme-border, rgba(255,255,255,0.08));
}
.detail-layout {
    display: flex;
    flex: 1;
    min-height: 0;
}
.detail-main {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    min-height: 0;
}
.detail-sidebar {
    width: min(380px, 38%);
    flex-shrink: 0;
    overflow-y: auto;
    border-left: 1px solid var(--theme-border, rgba(255,255,255,0.08));
    background: color-mix(in srgb, var(--theme-bg-soft, #282846) 42%, transparent);
}
.detail-sidebar::-webkit-scrollbar { width: 4px; }
.detail-sidebar::-webkit-scrollbar-thumb { background: var(--scrollbar-thumb, rgba(255,255,255,0.16)); border-radius: 4px; }
.detail-header {
    padding: 18px;
}
.detail-meta {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px 14px;
    font-size: 12px;
    color: var(--theme-text-soft, rgba(255,255,255,0.62));
}
.detail-meta-item {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    min-width: 0;
}
.detail-meta-item svg {
    flex-shrink: 0;
    font-size: 14px;
}
.detail-view-count {
    margin-left: auto;
    font-weight: 700;
    color: var(--theme-text, inherit);
}
.detail-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 12px;
}
.detail-summary {
    font-size: 14px;
    font-style: italic;
    color: var(--theme-text-soft, rgba(255,255,255,0.68));
    line-height: 1.65;
    margin: 12px 0 0;
}
.detail-scripture {
    font-size: 13px;
    padding: 10px 12px;
    border-radius: 8px;
    background: color-mix(in srgb, var(--theme-bg-elevated, #30304f) 78%, transparent);
    border: 1px solid var(--theme-border, rgba(255,255,255,0.1));
    margin-top: 12px;
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 6px;
}
.detail-scripture-icon {
    color: var(--primary-color, #6f84ff);
    opacity: 0.9;
}
.detail-scripture-label {
    font-weight: 800;
}
.detail-verse-preview {
    margin-top: 8px;
}
.detail-verse-loading {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 58px;
    border-radius: 8px;
    background: color-mix(in srgb, var(--theme-bg-elevated, #30304f) 56%, transparent);
    border: 1px solid var(--theme-border, rgba(255,255,255,0.08));
}
.detail-verse-list {
    display: grid;
    gap: 8px;
}
.detail-verse-row {
    padding: 10px 12px;
    border-radius: 8px;
    background: color-mix(in srgb, var(--theme-bg-elevated, #30304f) 64%, transparent);
    border: 1px solid var(--theme-border, rgba(255,255,255,0.08));
}
.detail-verse-line {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 5px;
    min-width: 0;
}
.detail-version-code {
    flex-shrink: 0;
    padding: 2px 6px;
    border-radius: 5px;
    color: var(--primary-color, #6f84ff);
    background: color-mix(in srgb, var(--primary-color, #6f84ff) 17%, transparent);
    border: 1px solid color-mix(in srgb, var(--primary-color, #6f84ff) 35%, transparent);
    font-size: 10px;
    font-weight: 800;
    line-height: 1.2;
}
.detail-verse-ref {
    color: var(--theme-text-soft, rgba(255,255,255,0.62));
    font-size: 11px;
    font-weight: 700;
}
.detail-verse-pager {
    margin-left: auto;
    display: inline-flex;
    align-items: center;
    gap: 3px;
    color: var(--theme-text-soft, rgba(255,255,255,0.62));
    font-size: 11px;
    font-weight: 800;
}
.detail-verse-pager-btn {
    width: 20px;
    height: 20px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border: 0;
    border-radius: 5px;
    background: transparent;
    color: inherit;
    cursor: pointer;
    font-size: 17px;
    line-height: 1;
}
.detail-verse-pager-btn:hover {
    color: var(--theme-text, inherit);
    background: rgba(255,255,255,0.07);
}
.detail-verse-pager-count {
    min-width: 28px;
    text-align: center;
}
.detail-verse-text {
    color: var(--theme-text, inherit);
    font-size: 13px;
    line-height: 1.55;
}
.detail-verse-text :deep(a) {
    display: none;
}
.detail-verse-text :deep(s) {
    color: var(--theme-text-soft, rgba(255,255,255,0.62));
    text-decoration: none;
}
.detail-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    padding: 14px 24px 0;
}
.detail-content {
    font-size: 15px;
    line-height: 1.78;
    margin: 16px 24px 0;
    padding: 0 16px 18px 0;
    flex: 1;
    min-height: 220px;
    overflow-y: auto;
    color: var(--theme-text, inherit);
}
.detail-content::-webkit-scrollbar { width: 4px; }
.detail-content::-webkit-scrollbar-thumb { background: var(--scrollbar-thumb, rgba(255,255,255,0.16)); border-radius: 4px; }
.detail-content :deep(p) { margin: 0 0 0.75em; }
.detail-content :deep(h1),
.detail-content :deep(h2),
.detail-content :deep(h3) { font-weight: 700; margin: 1em 0 0.4em; }
.detail-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    padding: 0 24px 20px;
}
.detail-tag {
    color: var(--theme-text-soft, rgba(255,255,255,0.58));
    font-size: 12px;
    font-weight: 700;
}

@media (max-width: 640px) {
    .sermon-detail-modal :deep(.n-card-header) {
        padding: 16px 18px 12px;
    }
    .detail-header,
    .detail-actions {
        padding-left: 18px;
        padding-right: 18px;
    }
    .detail-content {
        margin-left: 18px;
        margin-right: 18px;
    }
    .detail-view-count {
        margin-left: 0;
    }
}

@media (max-width: 900px) {
    .detail-layout {
        flex-direction: column;
    }
    .detail-sidebar {
        order: -1;
        width: auto;
        max-height: 44vh;
        border-left: 0;
        border-bottom: 1px solid var(--theme-border, rgba(255,255,255,0.08));
    }
}

.stale-banner {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 10px 16px 0;
    padding: 8px 12px;
    border-radius: 10px;
    border: 1px solid var(--theme-border, rgba(255, 255, 255, 0.08));
    background: rgba(120, 120, 120, 0.12);
    font-size: 12px;
    color: var(--theme-muted-foreground, #9ca3af);
}

.card-fav-btn {
    position: absolute;
    top: 8px;
    right: 8px;
    width: 30px;
    height: 30px;
    border-radius: 999px;
    background: rgba(0, 0, 0, 0.55);
    color: #ffffff;
    border: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 16px;
    transition: background 0.15s ease, transform 0.15s ease;
    z-index: 2;
}
.card-fav-btn:hover {
    background: rgba(0, 0, 0, 0.78);
    transform: scale(1.05);
}
.card-fav-btn.active {
    color: #fbbf24;
}
</style>
