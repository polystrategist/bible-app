import { defineStore } from 'pinia';
import { computed, onBeforeMount, ref, watch } from 'vue';
import axios from 'axios';
import { useAuthStore } from './authStore';

const API_BASE_URL = `${import.meta.env.VITE_API_BASE_URL}/api`;

export type ScriptureRef = {
    book: number;
    chapter: number;
    verse: number[];
};

export type SermonCategory = {
    id: number;
    name: string;
    slug: string;
};

export type SermonSeries = {
    id: number;
    title: string;
    description?: string | null;
    thumbnail_url?: string | null;
};

export type SermonCreator = {
    id: number;
    name: string;
    username?: string | null;
    info?: { profile_picture?: string | null } | null;
};

export type SermonType = {
    id: number;
    title: string;
    slug: string;
    created_by: number;
    preacher_name: string | null;
    short_summary: string;
    content: string;
    main_scripture: ScriptureRef[] | null;
    scripture_references: ScriptureRef[] | null;
    sermon_date: string | null;
    sermon_series_id: number | null;
    category_id: number | null;
    status: 'draft' | 'published' | 'archived';
    visibility: 'public' | 'private' | 'unlisted';
    thumbnail_url: string | null;
    audio_url: string | null;
    video_url: string | null;
    duration_seconds: number | null;
    tags: string[] | null;
    view_count: number;
    published_at: string | null;
    created_at: string;
    updated_at: string;
    creator?: SermonCreator;
    category?: SermonCategory | null;
    series?: SermonSeries | null;
};

export type CreateSermonPayload = {
    title: string;
    short_summary: string;
    content: string;
    preacher_name?: string | null;
    main_scripture?: ScriptureRef[] | null;
    scripture_references?: ScriptureRef[] | null;
    sermon_date?: string | null;
    sermon_series_id?: number | null;
    category_id?: number | null;
    status?: 'draft' | 'published';
    visibility?: 'public' | 'private' | 'unlisted';
    thumbnail_url?: string | null;
    audio_url?: string | null;
    video_url?: string | null;
    duration_seconds?: number | null;
    tags?: string[] | null;
};

export const useSermonStore = defineStore('useSermonStore', () => {
    const authStore = useAuthStore();

    // Feed (public sermons)
    const sermons = ref<SermonType[]>([]);
    const loading = ref(false);
    const page = ref(1);
    const lastPage = ref(1);
    const search = ref('');
    const categoryFilter = ref<number | null>(null);
    const sort = ref<'recent' | 'popular' | 'oldest'>('recent');

    // My sermons (authenticated)
    const mySermons = ref<SermonType[]>([]);
    const myLoading = ref(false);
    const myPage = ref(1);
    const myLastPage = ref(1);
    const mySearch = ref('');
    const myStatusFilter = ref<string>('');

    // Categories
    const categories = ref<SermonCategory[]>([]);

    // Tab routing signal — set by CreateSermon to switch Sermons.vue to a specific tab
    const requestedTab = ref<'browse' | 'mine' | null>(null);

    // Sermon being edited — set before routing to /create-sermon?edit=X so the form
    // can populate immediately without a find-by-id race against mySermons loading.
    const editingSermon = ref<SermonType | null>(null);
    const viewedSermonIds = new Set<number>();
    const pendingViewSermonIds = new Set<number>();

    function authHeaders() {
        const token = authStore.token;
        return token ? { Authorization: `Bearer ${token}` } : {};
    }

    async function getSermons(fresh = false) {
        if (fresh) {
            page.value = 1;
            sermons.value = [];
        }
        if (loading.value || page.value > lastPage.value) return;
        loading.value = true;
        try {
            const params: Record<string, any> = { page: page.value };
            if (search.value) params.search = search.value;
            if (categoryFilter.value) params.category_id = categoryFilter.value;
            if (sort.value !== 'recent') params.sort = sort.value;

            const res = await axios.get(`${API_BASE_URL}/sermons`, { params });
            if (res.data.status === 'success') {
                const paged = res.data.data;
                sermons.value = fresh ? paged.data : [...sermons.value, ...paged.data];
                lastPage.value = paged.last_page ?? 1;
            }
        } catch (e) {
            console.error('getSermons error', e);
        } finally {
            loading.value = false;
        }
    }

    async function getMySermons(fresh = false) {
        if (!authStore.isAuthenticated) return;
        if (fresh) {
            myPage.value = 1;
            mySermons.value = [];
        }
        if (myLoading.value || myPage.value > myLastPage.value) return;
        myLoading.value = true;
        try {
            const params: Record<string, any> = { page: myPage.value };
            if (mySearch.value) params.search = mySearch.value;
            if (myStatusFilter.value) params.status = myStatusFilter.value;

            const res = await axios.get(`${API_BASE_URL}/my-sermons`, {
                params,
                headers: authHeaders(),
            });
            if (res.data.status === 'success') {
                const paged = res.data.data;
                mySermons.value = fresh ? paged.data : [...mySermons.value, ...paged.data];
                myLastPage.value = paged.last_page ?? 1;
            }
        } catch (e) {
            console.error('getMySermons error', e);
        } finally {
            myLoading.value = false;
        }
    }

    async function createSermon(
        payload: CreateSermonPayload
    ): Promise<{ success: boolean; sermon?: SermonType; message?: string }> {
        try {
            const res = await axios.post(`${API_BASE_URL}/sermons`, payload, {
                headers: authHeaders(),
            });
            if (res.data.status === 'success') {
                const created = res.data.sermon as SermonType;
                mySermons.value = [created, ...mySermons.value];
                return { success: true, sermon: created };
            }
            return { success: false, message: 'Failed to create sermon' };
        } catch (error: any) {
            return {
                success: false,
                message: error.response?.data?.message || error.message || 'Failed to create sermon',
            };
        }
    }

    async function updateSermon(
        id: number,
        payload: Partial<CreateSermonPayload>
    ): Promise<{ success: boolean; sermon?: SermonType; message?: string }> {
        try {
            const res = await axios.patch(`${API_BASE_URL}/sermons/${id}`, payload, {
                headers: authHeaders(),
            });
            if (res.data.status === 'success') {
                const updated = res.data.sermon as SermonType;
                const idx = mySermons.value.findIndex((s) => s.id === id);
                if (idx !== -1) mySermons.value[idx] = updated;
                return { success: true, sermon: updated };
            }
            return { success: false, message: 'Failed to update sermon' };
        } catch (error: any) {
            return {
                success: false,
                message: error.response?.data?.message || error.message || 'Failed to update sermon',
            };
        }
    }

    async function deleteSermon(id: number): Promise<{ success: boolean; message?: string }> {
        try {
            await axios.delete(`${API_BASE_URL}/sermons/${id}`, { headers: authHeaders() });
            mySermons.value = mySermons.value.filter((s) => s.id !== id);
            sermons.value = sermons.value.filter((s) => s.id !== id);
            return { success: true };
        } catch (error: any) {
            return {
                success: false,
                message: error.response?.data?.message || error.message || 'Failed to delete sermon',
            };
        }
    }

    function replaceSermonInLists(updated: SermonType) {
        const feedIdx = sermons.value.findIndex((s) => s.id === updated.id);
        if (feedIdx !== -1) sermons.value[feedIdx] = updated;

        const mineIdx = mySermons.value.findIndex((s) => s.id === updated.id);
        if (mineIdx !== -1) mySermons.value[mineIdx] = updated;
    }

    function incrementLocalViewCount(id: number) {
        const update = (sermon: SermonType) => {
            sermon.view_count += 1;
            return sermon;
        };

        const feedSermon = sermons.value.find((s) => s.id === id);
        if (feedSermon) update(feedSermon);

        const mySermon = mySermons.value.find((s) => s.id === id);
        if (mySermon && mySermon !== feedSermon) update(mySermon);
    }

    async function recordSermonView(id: number): Promise<{ success: boolean; sermon?: SermonType; message?: string }> {
        if (viewedSermonIds.has(id) || pendingViewSermonIds.has(id)) {
            return { success: true };
        }

        pendingViewSermonIds.add(id);

        try {
            const res = await axios.post(`${API_BASE_URL}/sermons/${id}/view`, null, {
                headers: authHeaders(),
            });

            const updated = (res.data.sermon ?? res.data.data) as SermonType | undefined;
            if (updated?.id) {
                replaceSermonInLists(updated);
            } else {
                incrementLocalViewCount(id);
            }

            viewedSermonIds.add(id);
            return { success: true, sermon: updated };
        } catch (error: any) {
            return {
                success: false,
                message: error.response?.data?.message || error.message || 'Failed to record sermon view',
            };
        } finally {
            pendingViewSermonIds.delete(id);
        }
    }

    async function fetchCategories() {
        if (categories.value.length) return;
        try {
            const res = await axios.get(`${API_BASE_URL}/sermon-categories`);
            if (res.data.status === 'success') {
                categories.value = res.data.categories;
            }
        } catch (e) {
            console.error('fetchCategories error', e);
        }
    }

    watch(() => page.value, () => getSermons());
    watch(() => myPage.value, () => getMySermons());

    onBeforeMount(async () => {
        await Promise.all([getSermons(), fetchCategories()]);
    });

    return {
        // Feed
        sermons,
        loading,
        page,
        lastPage,
        search,
        categoryFilter,
        sort,
        getSermons,
        // My sermons
        mySermons,
        myLoading,
        myPage,
        myLastPage,
        mySearch,
        myStatusFilter,
        getMySermons,
        // CRUD
        createSermon,
        updateSermon,
        deleteSermon,
        recordSermonView,
        // Categories
        categories,
        fetchCategories,
        // Tab routing
        requestedTab,
        editingSermon,
        // Computed
        hasMoreFeed: computed(() => page.value < lastPage.value),
        hasMoreMine: computed(() => myPage.value < myLastPage.value),
    };
});

// Keep legacy export name for existing imports
export const userSermonStore = useSermonStore;
export type { SermonType as SERMON_TYPE };
