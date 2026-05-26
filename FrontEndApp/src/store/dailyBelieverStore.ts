import { defineStore } from 'pinia';
import { ref } from 'vue';
import axios from 'axios';
import { useAuthStore } from './authStore';

const API_BASE_URL = `${import.meta.env.VITE_API_BASE_URL}/api`;

export type DailyBelieverCreator = {
    id: number;
    name: string;
    username?: string | null;
    info?: { profile_picture?: string | null } | null;
};

export type DailyBelieverPost = {
    id: number;
    user_id: number;
    url: string;
    source_type: 'website' | 'youtube';
    source_domain: string | null;
    title: string;
    description: string | null;
    thumbnail_url: string | null;
    note: string | null;
    created_at: string;
    creator?: DailyBelieverCreator | null;
};

export type LinkMetadata = {
    url: string;
    sourceType: 'website' | 'youtube';
    sourceDomain: string;
    title: string;
    description: string | null;
    thumbnailUrl: string | null;
};

export const useDailyBelieverStore = defineStore('useDailyBelieverStore', () => {
    const authStore = useAuthStore();

    const posts = ref<DailyBelieverPost[]>([]);
    const loading = ref(false);
    const page = ref(1);
    const lastPage = ref(1);
    const search = ref('');
    const sourceTypeFilter = ref<'' | 'website' | 'youtube'>('');
    const feedStatus = ref<'loading' | 'fresh' | 'error' | 'empty'>('loading');

    async function fetchPosts(reset = false) {
        if (loading.value) return;
        if (reset) {
            page.value = 1;
            posts.value = [];
        }
        loading.value = true;
        if (reset) feedStatus.value = 'loading';

        try {
            const res = await axios.get(`${API_BASE_URL}/daily-believers`, {
                params: {
                    page: page.value,
                    search: search.value || undefined,
                    source_type: sourceTypeFilter.value || undefined,
                },
            });
            const data = res.data?.data;
            const items: DailyBelieverPost[] = data?.data ?? [];
            posts.value = reset ? items : [...posts.value, ...items];
            lastPage.value = data?.last_page ?? 1;
            feedStatus.value = posts.value.length ? 'fresh' : 'empty';
        } catch (err) {
            console.error('Failed to load daily believers feed', err);
            if (!posts.value.length) feedStatus.value = 'error';
        } finally {
            loading.value = false;
        }
    }

    async function loadMore() {
        if (loading.value || page.value >= lastPage.value) return;
        page.value += 1;
        await fetchPosts(false);
    }

    /**
     * Fetch OG/oEmbed metadata. In Electron we go through the main process
     * (`dailyBelieversExtractMetadata`) to bypass CORS. On the web build we
     * fall back to a direct fetch — websites without CORS headers will fail,
     * which is acceptable for the web fallback.
     */
    async function extractMetadata(rawUrl: string): Promise<LinkMetadata> {
        if (window.isElectron) {
            return await window.browserWindow.dailyBelieversExtractMetadata(rawUrl);
        }
        // Web fallback — best-effort. YouTube oEmbed works cross-origin.
        const url = rawUrl.startsWith('http') ? rawUrl : `https://${rawUrl}`;
        const host = new URL(url).host.toLowerCase().replace(/^www\./, '');
        if (host.includes('youtube.com') || host === 'youtu.be') {
            const res = await axios.get(
                `https://www.youtube.com/oembed?url=${encodeURIComponent(url)}&format=json`
            );
            return {
                url,
                sourceType: 'youtube',
                sourceDomain: 'youtube.com',
                title: res.data?.title ?? 'YouTube video',
                description: res.data?.author_name ? `By ${res.data.author_name}` : null,
                thumbnailUrl: res.data?.thumbnail_url ?? null,
            };
        }
        throw new Error('Link previews for non-YouTube URLs require the desktop app.');
    }

    async function createPost(metadata: LinkMetadata, note: string | null): Promise<DailyBelieverPost> {
        if (!authStore.token) throw new Error('You must be signed in to share a link.');
        const res = await axios.post(
            `${API_BASE_URL}/daily-believers`,
            {
                url: metadata.url,
                source_type: metadata.sourceType,
                source_domain: metadata.sourceDomain,
                title: metadata.title,
                description: metadata.description,
                thumbnail_url: metadata.thumbnailUrl,
                note: note || null,
            },
            { headers: { Authorization: `Bearer ${authStore.token}` } }
        );
        const post: DailyBelieverPost = res.data?.post;
        if (post) posts.value.unshift(post);
        return post;
    }

    async function deletePost(id: number): Promise<void> {
        if (!authStore.token) throw new Error('Sign-in required.');
        await axios.delete(`${API_BASE_URL}/daily-believers/${id}`, {
            headers: { Authorization: `Bearer ${authStore.token}` },
        });
        posts.value = posts.value.filter((p) => p.id !== id);
    }

    return {
        posts,
        loading,
        page,
        lastPage,
        search,
        sourceTypeFilter,
        feedStatus,
        fetchPosts,
        loadMore,
        extractMetadata,
        createPost,
        deletePost,
    };
});
