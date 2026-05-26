<script lang="ts" setup>
import { NButton, NInput, NSelect, NModal, NSpin, useDialog, useMessage } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { ref, computed, onMounted, watch } from 'vue';
import { useInfiniteScroll } from '@vueuse/core';
import {
    useDailyBelieverStore,
    DailyBelieverPost,
    LinkMetadata,
} from '../../store/dailyBelieverStore';
import { useAuthStore } from '../../store/authStore';
import { useMenuStore } from '../../store/menu';
import { DAYJS } from '../../util/dayjs';
import { resolveAvatarUrl } from '../../util/avatar';

const store = useDailyBelieverStore();
const authStore = useAuthStore();
const menuStore = useMenuStore();
const dialog = useDialog();
const message = useMessage();

const scrollEl = ref<HTMLElement | null>(null);

const showShareModal = ref(false);
const shareUrl = ref('');
const shareNote = ref('');
const shareMetadata = ref<LinkMetadata | null>(null);
const shareMetaLoading = ref(false);
const shareMetaError = ref<string | null>(null);
const sharing = ref(false);

const selectedPost = ref<DailyBelieverPost | null>(null);
const showDetailModal = ref(false);
const failedAvatars = ref<Set<number>>(new Set());

function onAvatarError(post: DailyBelieverPost) {
    failedAvatars.value.add(post.id);
    failedAvatars.value = new Set(failedAvatars.value);
}

useInfiniteScroll(
    scrollEl as any,
    () => store.loadMore(),
    { distance: 200 }
);

onMounted(() => {
    if (!store.posts.length) store.fetchPosts(true);
});

const sourceOptions = [
    { label: 'All sources', value: '' },
    { label: 'YouTube', value: 'youtube' },
    { label: 'Websites', value: 'website' },
];

const isAuthed = computed(() => authStore.isAuthenticated);

function openShareModal() {
    if (!isAuthed.value) {
        dialog.warning({
            title: 'Sign in to share',
            content: 'You need an account to share a link with the community.',
            positiveText: 'Sign In',
            negativeText: 'Cancel',
            onPositiveClick: () => menuStore.setMenu('/profile'),
        });
        return;
    }
    shareUrl.value = '';
    shareNote.value = '';
    shareMetadata.value = null;
    shareMetaError.value = null;
    showShareModal.value = true;
}

async function fetchShareMetadata() {
    const url = shareUrl.value.trim();
    if (!url) return;
    shareMetadata.value = null;
    shareMetaError.value = null;
    shareMetaLoading.value = true;
    try {
        const meta = await store.extractMetadata(url);
        shareMetadata.value = meta;
    } catch (err: any) {
        shareMetaError.value = err?.message ?? 'Could not load that link.';
    } finally {
        shareMetaLoading.value = false;
    }
}

async function submitShare() {
    if (!shareMetadata.value) return;
    sharing.value = true;
    try {
        await store.createPost(shareMetadata.value, shareNote.value.trim() || null);
        message.success('Shared with the community!');
        showShareModal.value = false;
    } catch (err: any) {
        message.error(err?.response?.data?.message ?? err?.message ?? 'Failed to share.');
    } finally {
        sharing.value = false;
    }
}

function openDetail(post: DailyBelieverPost) {
    selectedPost.value = post;
    showDetailModal.value = true;
}

function openExternal(url: string) {
    window.open(url, '_blank', 'noopener,noreferrer');
}

function confirmDelete(post: DailyBelieverPost) {
    dialog.warning({
        title: 'Delete post',
        content: `Remove "${post.title}" from the community feed?`,
        positiveText: 'Delete',
        negativeText: 'Cancel',
        onPositiveClick: async () => {
            try {
                await store.deletePost(post.id);
                message.success('Post removed.');
                if (selectedPost.value?.id === post.id) showDetailModal.value = false;
            } catch (err: any) {
                message.error(err?.response?.data?.message ?? 'Failed to delete.');
            }
        },
    });
}

function timeAgo(d: string | null): string {
    if (!d) return '';
    return DAYJS(d).fromNow();
}

function creatorAvatar(post: DailyBelieverPost): string | null {
    if (failedAvatars.value.has(post.id)) return null;
    return resolveAvatarUrl(post.creator?.info?.profile_picture ?? null, 50);
}

function creatorInitials(post: DailyBelieverPost): string {
    const name = (post.creator?.name || post.creator?.username || '?').trim();
    const initials = name
        .split(/\s+/)
        .map((w) => w[0])
        .filter(Boolean)
        .slice(0, 2)
        .join('');
    return (initials || '?').toUpperCase();
}

function sourceIcon(post: DailyBelieverPost): string {
    return post.source_type === 'youtube' ? 'mdi:youtube' : 'mdi:link-variant';
}

function ownerOf(post: DailyBelieverPost): boolean {
    return isAuthed.value && authStore.user?.id === post.user_id;
}

watch(() => store.sourceTypeFilter, () => store.fetchPosts(true));
</script>

<template>
    <div class="db-root">

        <!-- ═══ HEADER ═══ -->
        <div class="page-header">
            <div>
                <h1 class="page-title">Daily Believers</h1>
                <p class="page-subtitle">A community feed of sermons, articles, and videos shared by other believers.</p>
            </div>
            <NButton type="primary" size="small" @click="openShareModal">
                <template #icon><Icon icon="mdi:plus" /></template>
                Share a Link
            </NButton>
        </div>

        <!-- ═══ TOOLBAR ═══ -->
        <div class="toolbar">
            <NInput
                v-model:value="store.search"
                placeholder="Search shared links…"
                size="small"
                clearable
                class="search-input"
                @keydown.enter="store.fetchPosts(true)"
            >
                <template #prefix><Icon icon="mdi:magnify" class="opacity-50" /></template>
            </NInput>
            <NButton size="small" type="primary" ghost :loading="store.loading" @click="store.fetchPosts(true)">
                Search
            </NButton>
            <NSelect
                v-model:value="store.sourceTypeFilter"
                :options="sourceOptions"
                size="small"
                class="!w-150px"
            />
            <NButton size="small" secondary :loading="store.loading" @click="store.fetchPosts(true)">
                <template #icon><Icon icon="mdi:refresh" /></template>
            </NButton>
        </div>

        <!-- ═══ FEED ═══ -->
        <div ref="scrollEl" class="feed-scroll">
            <!-- Initial loading -->
            <div v-if="store.loading && !store.posts.length" class="empty-state">
                <NSpin size="large" />
            </div>

            <!-- Error -->
            <div v-else-if="store.feedStatus === 'error' && !store.posts.length" class="empty-state">
                <Icon icon="mdi:cloud-off-outline" class="empty-icon" />
                <p class="empty-title">Could not load feed</p>
                <p class="empty-sub">Check your connection and try again.</p>
                <NButton size="small" @click="store.fetchPosts(true)">Retry</NButton>
            </div>

            <!-- Empty -->
            <div v-else-if="!store.loading && !store.posts.length" class="empty-state">
                <Icon icon="mdi:link-variant-plus" class="empty-icon" />
                <p class="empty-title">No links shared yet</p>
                <p class="empty-sub">Be the first to share a sermon or YouTube video with the community.</p>
                <NButton type="primary" size="small" @click="openShareModal">Share a Link</NButton>
            </div>

            <!-- Card grid -->
            <div v-else class="feed-grid">
                <article
                    v-for="post in store.posts"
                    :key="post.id"
                    class="feed-card"
                    @click="openDetail(post)"
                >
                    <div class="card-thumb">
                        <img v-if="post.thumbnail_url" :src="post.thumbnail_url" :alt="post.title" loading="lazy" />
                        <div v-else class="card-thumb-placeholder">
                            <Icon :icon="sourceIcon(post)" class="text-4xl opacity-30" />
                        </div>
                        <div class="card-source-badge">
                            <Icon :icon="sourceIcon(post)" />
                            <span>{{ post.source_domain || post.source_type }}</span>
                        </div>
                    </div>

                    <div class="card-body">
                        <h3 class="card-title">{{ post.title }}</h3>
                        <p v-if="post.description" class="card-desc">{{ post.description }}</p>
                        <p v-if="post.note" class="card-note">"{{ post.note }}"</p>

                        <div class="card-footer">
                            <span v-if="isAuthed && post.creator" class="creator-meta">
                                <span class="creator-avatar">
                                    <img
                                        v-if="creatorAvatar(post)"
                                        :src="creatorAvatar(post) ?? undefined"
                                        :alt="post.creator.name || ''"
                                        @error="onAvatarError(post)"
                                    />
                                    <span v-else>{{ creatorInitials(post) }}</span>
                                </span>
                                <span class="creator-name">
                                    <span v-if="post.creator.username">@{{ post.creator.username }}</span>
                                    <span v-else>{{ post.creator.name }}</span>
                                </span>
                            </span>
                            <span class="card-time">{{ timeAgo(post.created_at) }}</span>
                        </div>
                    </div>
                </article>

                <div v-if="store.loading" class="load-more-row">
                    <NSpin size="small" />
                </div>
            </div>
        </div>

        <!-- ═══ SHARE MODAL ═══ -->
        <NModal
            v-model:show="showShareModal"
            preset="card"
            title="Share a Link"
            class="db-modal !max-w-560px !w-[94vw]"
            :bordered="false"
        >
            <div class="share-form">
                <label class="share-label">Link URL</label>
                <NInput
                    v-model:value="shareUrl"
                    placeholder="https://youtube.com/watch?v=… or a sermon article URL"
                    size="medium"
                    clearable
                    @blur="fetchShareMetadata"
                    @keydown.enter.prevent="fetchShareMetadata"
                />
                <p class="share-hint">Paste a YouTube video, sermon page, or article — we'll fetch a preview automatically.</p>

                <!-- Preview -->
                <div v-if="shareMetaLoading" class="share-preview share-preview-loading">
                    <NSpin size="small" />
                    <span>Loading preview…</span>
                </div>
                <div v-else-if="shareMetaError" class="share-preview share-preview-error">
                    <Icon icon="mdi:alert-circle-outline" />
                    <span>{{ shareMetaError }}</span>
                </div>
                <div v-else-if="shareMetadata" class="share-preview">
                    <img
                        v-if="shareMetadata.thumbnailUrl"
                        :src="shareMetadata.thumbnailUrl"
                        :alt="shareMetadata.title"
                        class="share-preview-thumb"
                    />
                    <div class="share-preview-body">
                        <div class="share-preview-domain">
                            <Icon :icon="shareMetadata.sourceType === 'youtube' ? 'mdi:youtube' : 'mdi:link-variant'" />
                            {{ shareMetadata.sourceDomain }}
                        </div>
                        <div class="share-preview-title">{{ shareMetadata.title }}</div>
                        <div v-if="shareMetadata.description" class="share-preview-desc">{{ shareMetadata.description }}</div>
                    </div>
                </div>

                <label class="share-label mt-3">Note (optional)</label>
                <NInput
                    v-model:value="shareNote"
                    type="textarea"
                    placeholder="Why are you sharing this? A short message for the community…"
                    :autosize="{ minRows: 2, maxRows: 5 }"
                    maxlength="2000"
                    show-count
                />

                <div class="share-actions">
                    <NButton size="small" @click="showShareModal = false">Cancel</NButton>
                    <NButton
                        size="small"
                        type="primary"
                        :loading="sharing"
                        :disabled="!shareMetadata || shareMetaLoading"
                        @click="submitShare"
                    >
                        Share
                    </NButton>
                </div>
            </div>
        </NModal>

        <!-- ═══ DETAIL MODAL ═══ -->
        <NModal
            v-model:show="showDetailModal"
            preset="card"
            :title="selectedPost?.title ?? ''"
            class="db-modal !max-w-640px !w-[94vw]"
            :bordered="false"
        >
            <div v-if="selectedPost" class="detail-body">
                <img
                    v-if="selectedPost.thumbnail_url"
                    :src="selectedPost.thumbnail_url"
                    :alt="selectedPost.title"
                    class="detail-thumb"
                />

                <div class="detail-meta">
                    <Icon :icon="sourceIcon(selectedPost)" />
                    <span>{{ selectedPost.source_domain || selectedPost.source_type }}</span>
                    <span class="detail-time">· {{ timeAgo(selectedPost.created_at) }}</span>
                </div>

                <p v-if="selectedPost.description" class="detail-desc">{{ selectedPost.description }}</p>

                <div v-if="selectedPost.note" class="detail-note">
                    <Icon icon="mdi:format-quote-open" class="detail-note-quote" />
                    {{ selectedPost.note }}
                </div>

                <div v-if="isAuthed && selectedPost.creator" class="detail-creator">
                    <span class="creator-avatar lg">
                        <img
                            v-if="creatorAvatar(selectedPost)"
                            :src="creatorAvatar(selectedPost) ?? undefined"
                            :alt="selectedPost.creator.name || ''"
                            @error="onAvatarError(selectedPost)"
                        />
                        <span v-else>{{ creatorInitials(selectedPost) }}</span>
                    </span>
                    <span>
                        Shared by
                        <strong v-if="selectedPost.creator.username">@{{ selectedPost.creator.username }}</strong>
                        <strong v-else>{{ selectedPost.creator.name }}</strong>
                    </span>
                </div>

                <div class="detail-actions">
                    <NButton type="primary" size="small" @click="openExternal(selectedPost.url)">
                        <template #icon><Icon icon="mdi:open-in-new" /></template>
                        Open Link
                    </NButton>
                    <NButton
                        v-if="ownerOf(selectedPost)"
                        size="small"
                        type="error"
                        secondary
                        @click="confirmDelete(selectedPost)"
                    >
                        <template #icon><Icon icon="mdi:trash-can-outline" /></template>
                        Delete
                    </NButton>
                </div>
            </div>
        </NModal>
    </div>
</template>

<style scoped>
.db-root {
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: hidden;
    padding-left: 15px;
}

.page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 20px 0;
    flex-shrink: 0;
    gap: 12px;
}
.page-title { font-size: 22px; font-weight: 800; margin: 0 0 2px; line-height: 1.2; }
.page-subtitle { font-size: 12px; opacity: 0.55; margin: 0; max-width: 540px; }

.toolbar {
    display: flex;
    gap: 8px;
    align-items: center;
    padding: 12px 20px 4px;
    flex-wrap: wrap;
    flex-shrink: 0;
}
.search-input { flex: 1; min-width: 180px; max-width: 360px; }

.feed-scroll {
    flex: 1;
    overflow-y: auto;
    padding: 8px 20px 24px;
}
.feed-scroll::-webkit-scrollbar { width: 4px; }
.feed-scroll::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 4px; }

/* Grid layout — matches Sermons */
.feed-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 14px;
}

.feed-card {
    border-radius: 14px;
    overflow: hidden;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    cursor: pointer;
    transition: transform 0.15s, box-shadow 0.15s, background 0.15s;
    display: flex;
    flex-direction: column;
}
.feed-card:hover {
    transform: translateY(-2px);
    background: rgba(255,255,255,0.07);
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}

.card-thumb {
    position: relative;
    width: 100%;
    aspect-ratio: 16 / 9;
    overflow: hidden;
    background: rgba(255,255,255,0.05);
    flex-shrink: 0;
}
.card-thumb img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    transition: transform 0.2s;
}
.feed-card:hover .card-thumb img { transform: scale(1.04); }
.card-thumb-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, rgba(111,132,255,0.1), rgba(95,176,255,0.06));
}
.card-source-badge {
    position: absolute;
    top: 8px;
    left: 8px;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 3px 8px;
    border-radius: 999px;
    background: rgba(0,0,0,0.6);
    color: #fff;
    font-size: 10.5px;
    font-weight: 700;
    backdrop-filter: blur(4px);
}

.card-body {
    padding: 12px 14px 14px;
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 6px;
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
.card-desc {
    font-size: 12px;
    opacity: 0.65;
    margin: 0;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.card-note {
    font-size: 12px;
    font-style: italic;
    margin: 0;
    padding: 6px 8px;
    border-left: 2px solid color-mix(in srgb, var(--primary-color, #6f84ff) 60%, transparent);
    background: color-mix(in srgb, var(--primary-color, #6f84ff) 7%, transparent);
    border-radius: 0 6px 6px 0;
    color: var(--theme-text-soft, rgba(255,255,255,0.78));
}

.card-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 4px;
    font-size: 11px;
    opacity: 0.55;
    gap: 8px;
}
.creator-meta {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    min-width: 0;
}
.creator-avatar {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: #7c6af7;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    font-weight: 700;
    color: white;
    overflow: hidden;
    flex-shrink: 0;
}
.creator-avatar.lg { width: 32px; height: 32px; font-size: 12px; }
.creator-avatar img {
    width: 100%; height: 100%;
    object-fit: cover; display: block;
}
.creator-name {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.card-time { flex-shrink: 0; }

.load-more-row {
    grid-column: 1 / -1;
    display: flex;
    justify-content: center;
    padding: 12px 0 16px;
}

.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 80px 20px;
    opacity: 0.7;
}
.empty-icon { font-size: 52px; opacity: 0.5; }
.empty-title { font-size: 16px; font-weight: 700; margin: 0; }
.empty-sub { font-size: 13px; margin: 0; text-align: center; max-width: 320px; opacity: 0.7; }

/* ── Modals ── */
.db-modal :deep(.n-card) {
    background: var(--theme-bg-elevated, #30304f);
    border: 1px solid var(--theme-border, rgba(255,255,255,0.12));
    box-shadow: 0 24px 60px rgba(0,0,0,0.36);
}
.db-modal :deep(.n-card-header) {
    padding: 18px 22px 14px;
    border-bottom: 1px solid var(--theme-border, rgba(255,255,255,0.08));
}
.db-modal :deep(.n-card-header__main) {
    color: var(--theme-text, inherit);
    font-size: 17px;
    font-weight: 800;
}

/* Share form */
.share-form { display: flex; flex-direction: column; padding: 4px 4px 0; }
.share-label { font-size: 12px; font-weight: 700; opacity: 0.7; margin-bottom: 6px; }
.share-hint { font-size: 11px; opacity: 0.5; margin: 6px 0 12px; }

.share-preview {
    display: flex;
    gap: 12px;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid var(--theme-border, rgba(255,255,255,0.1));
    background: color-mix(in srgb, var(--theme-bg-elevated, #30304f) 60%, transparent);
    margin-top: 4px;
}
.share-preview-loading,
.share-preview-error {
    align-items: center;
    justify-content: flex-start;
    font-size: 12px;
    opacity: 0.8;
}
.share-preview-error { color: #ef4444; }
.share-preview-thumb {
    width: 110px;
    height: 70px;
    object-fit: cover;
    border-radius: 6px;
    flex-shrink: 0;
}
.share-preview-body { display: flex; flex-direction: column; gap: 4px; min-width: 0; flex: 1; }
.share-preview-domain {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 11px;
    font-weight: 700;
    opacity: 0.6;
}
.share-preview-title {
    font-size: 13px;
    font-weight: 700;
    line-height: 1.35;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.share-preview-desc {
    font-size: 11px;
    opacity: 0.55;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.share-actions {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
    margin-top: 16px;
    padding-bottom: 4px;
}

/* Detail modal */
.detail-body { display: flex; flex-direction: column; gap: 12px; padding: 4px 4px 0; }
.detail-thumb {
    width: 100%;
    max-height: 320px;
    object-fit: cover;
    border-radius: 10px;
    border: 1px solid var(--theme-border, rgba(255,255,255,0.08));
}
.detail-meta {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    font-weight: 700;
    opacity: 0.65;
}
.detail-time { font-weight: 500; opacity: 0.7; }
.detail-desc { font-size: 14px; line-height: 1.55; margin: 0; }
.detail-note {
    position: relative;
    padding: 12px 14px 12px 36px;
    border-radius: 8px;
    background: color-mix(in srgb, var(--primary-color, #6f84ff) 10%, transparent);
    border-left: 3px solid var(--primary-color, #6f84ff);
    font-size: 13px;
    font-style: italic;
    line-height: 1.55;
}
.detail-note-quote {
    position: absolute;
    left: 10px;
    top: 10px;
    font-size: 18px;
    opacity: 0.55;
    color: var(--primary-color, #6f84ff);
}
.detail-creator {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    font-size: 12.5px;
    opacity: 0.85;
}
.detail-actions {
    display: flex;
    gap: 8px;
    margin-top: 4px;
    flex-wrap: wrap;
}
</style>
