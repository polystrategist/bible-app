<script lang="ts" setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import {
    NButton, NInput, NInputNumber, NSelect, NDatePicker, NForm, NFormItem,
    NAlert, NDynamicTags, NTag, useMessage,
} from 'naive-ui';
import Editor from '../../components/Editor/Editor.vue';
import { useAuthStore } from '../../store/authStore';
import { useSermonStore, ScriptureRef } from '../../store/Sermons';
import { useMenuStore } from '../../store/menu';
import { Icon } from '@iconify/vue';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const sermonStore = useSermonStore();
const menuStore = useMenuStore();
const message = useMessage();

const editId = computed(() => route.query.edit ? Number(route.query.edit) : null);
const isEditing = computed(() => editId.value !== null);

const loading = ref(false);
const errors = ref<Record<string, string>>({});

// Form fields
const title = ref('');
const shortSummary = ref('');
const content = ref('');
const preacherName = ref('');
const categoryId = ref<number | null>(null);
const sermonDate = ref<number | null>(null); // NDatePicker uses timestamp
const statusValue = ref<'draft' | 'published'>('draft');
const visibility = ref<'public' | 'private' | 'unlisted'>('public');
const videoUrl = ref('');
const audioUrl = ref('');
const thumbnailUrl = ref('');
const durationSeconds = ref<number | null>(null);
const tags = ref<string[]>([]);

// Scripture refs
const mainScripture = ref<ScriptureRef[]>([]);
const newScriptureBook = ref<number | null>(null);
const newScriptureChapter = ref<number | null>(null);
const newScriptureVerses = ref(''); // "1,2,3-5" format

// ----- Options -----
const statusOptions = [
    { label: 'Draft (save without publishing)', value: 'draft' },
    { label: 'Published (visible to community)', value: 'published' },
];
const visibilityOptions = [
    { label: 'Public', value: 'public' },
    { label: 'Unlisted (only via link)', value: 'unlisted' },
    { label: 'Private (only you)', value: 'private' },
];
const selectScrollbarProps = { trigger: 'none' as const };
const categoryOptions = computed(() => [
    { label: '— No Category —', value: null as any },
    ...sermonStore.categories.map((c) => ({ label: c.name, value: c.id as any })),
]);

// Bible books for scripture picker (MyBible numbering: 10-step increments)
const BIBLE_BOOKS = [
    { label: 'Genesis', value: 10 },      { label: 'Exodus', value: 20 },
    { label: 'Leviticus', value: 30 },    { label: 'Numbers', value: 40 },
    { label: 'Deuteronomy', value: 50 },  { label: 'Joshua', value: 60 },
    { label: 'Judges', value: 70 },       { label: 'Ruth', value: 80 },
    { label: '1 Samuel', value: 90 },     { label: '2 Samuel', value: 100 },
    { label: '1 Kings', value: 110 },     { label: '2 Kings', value: 120 },
    { label: '1 Chronicles', value: 130 },{ label: '2 Chronicles', value: 140 },
    { label: 'Ezra', value: 150 },        { label: 'Nehemiah', value: 160 },
    { label: 'Esther', value: 180 },      { label: 'Job', value: 220 },
    { label: 'Psalms', value: 230 },      { label: 'Proverbs', value: 240 },
    { label: 'Ecclesiastes', value: 250 },{ label: 'Song of Solomon', value: 260 },
    { label: 'Isaiah', value: 290 },      { label: 'Jeremiah', value: 300 },
    { label: 'Lamentations', value: 310 },{ label: 'Ezekiel', value: 330 },
    { label: 'Daniel', value: 340 },      { label: 'Hosea', value: 350 },
    { label: 'Joel', value: 360 },        { label: 'Amos', value: 370 },
    { label: 'Obadiah', value: 380 },     { label: 'Jonah', value: 390 },
    { label: 'Micah', value: 400 },       { label: 'Nahum', value: 410 },
    { label: 'Habakkuk', value: 420 },    { label: 'Zephaniah', value: 430 },
    { label: 'Haggai', value: 440 },      { label: 'Zechariah', value: 450 },
    { label: 'Malachi', value: 460 },     { label: 'Matthew', value: 470 },
    { label: 'Mark', value: 480 },        { label: 'Luke', value: 490 },
    { label: 'John', value: 500 },        { label: 'Acts', value: 510 },
    { label: 'Romans', value: 520 },      { label: '1 Corinthians', value: 530 },
    { label: '2 Corinthians', value: 540 },{ label: 'Galatians', value: 550 },
    { label: 'Ephesians', value: 560 },   { label: 'Philippians', value: 570 },
    { label: 'Colossians', value: 580 },  { label: '1 Thessalonians', value: 590 },
    { label: '2 Thessalonians', value: 600 },{ label: '1 Timothy', value: 610 },
    { label: '2 Timothy', value: 620 },   { label: 'Titus', value: 630 },
    { label: 'Philemon', value: 640 },    { label: 'Hebrews', value: 650 },
    { label: 'James', value: 660 },       { label: '1 Peter', value: 670 },
    { label: '2 Peter', value: 680 },     { label: '1 John', value: 690 },
    { label: '2 John', value: 700 },      { label: '3 John', value: 710 },
    { label: 'Jude', value: 720 },        { label: 'Revelation', value: 730 },
];

function bookLabel(bookNum: number) {
    return BIBLE_BOOKS.find((b) => b.value === bookNum)?.label ?? `Book ${bookNum}`;
}

function parseVerses(raw: string): number[] {
    const verses: number[] = [];
    raw.split(',').forEach((part) => {
        const trimmed = part.trim();
        const range = trimmed.match(/^(\d+)-(\d+)$/);
        if (range) {
            const from = parseInt(range[1]);
            const to = parseInt(range[2]);
            for (let v = from; v <= to; v++) verses.push(v);
        } else if (/^\d+$/.test(trimmed)) {
            verses.push(parseInt(trimmed));
        }
    });
    return [...new Set(verses)].sort((a, b) => a - b);
}

function addScripture() {
    if (!newScriptureBook.value || !newScriptureChapter.value) return;
    const verses = newScriptureVerses.value.trim()
        ? parseVerses(newScriptureVerses.value)
        : [];
    mainScripture.value.push({
        book: newScriptureBook.value,
        chapter: newScriptureChapter.value,
        verse: verses,
    });
    newScriptureBook.value = null;
    newScriptureChapter.value = null;
    newScriptureVerses.value = '';
}

function removeScripture(index: number) {
    mainScripture.value.splice(index, 1);
}

function validate(): boolean {
    errors.value = {};
    if (!title.value.trim()) errors.value.title = 'Title is required';
    if (!shortSummary.value.trim()) errors.value.shortSummary = 'Short summary is required';
    if (!content.value.trim()) errors.value.content = 'Content is required';
    return Object.keys(errors.value).length === 0;
}

async function submit() {
    if (!validate()) return;
    loading.value = true;

    const payload = {
        title: title.value.trim(),
        short_summary: shortSummary.value.trim(),
        content: content.value,
        preacher_name: preacherName.value.trim() || null,
        category_id: categoryId.value,
        sermon_date: sermonDate.value ? new Date(sermonDate.value).toISOString().slice(0, 10) : null,
        status: statusValue.value,
        visibility: visibility.value,
        video_url: videoUrl.value.trim() || null,
        audio_url: audioUrl.value.trim() || null,
        thumbnail_url: thumbnailUrl.value.trim() || null,
        duration_seconds: durationSeconds.value || null,
        tags: tags.value.length ? tags.value : null,
        main_scripture: mainScripture.value.length ? mainScripture.value : null,
    };

    let result;
    if (isEditing.value && editId.value) {
        result = await sermonStore.updateSermon(editId.value, payload);
    } else {
        result = await sermonStore.createSermon(payload);
    }

    loading.value = false;

    if (result.success) {
        message.success(isEditing.value ? 'Sermon updated!' : 'Sermon created!');
        sermonStore.requestedTab = 'mine';
        await goBackToSermons();
    } else {
        message.error(result.message ?? 'Something went wrong');
    }
}

function resetForm() {
    title.value = '';
    shortSummary.value = '';
    content.value = '';
    preacherName.value = '';
    categoryId.value = null;
    sermonDate.value = null;
    statusValue.value = 'draft';
    visibility.value = 'public';
    videoUrl.value = '';
    audioUrl.value = '';
    thumbnailUrl.value = '';
    durationSeconds.value = null;
    tags.value = [];
    mainScripture.value = [];
    errors.value = {};
}

function populateForm(sermon: import('../../store/Sermons').SermonType) {
    title.value = sermon.title;
    shortSummary.value = sermon.short_summary;
    content.value = sermon.content;
    preacherName.value = sermon.preacher_name ?? '';
    categoryId.value = sermon.category_id;
    sermonDate.value = sermon.sermon_date ? new Date(sermon.sermon_date).getTime() : null;
    statusValue.value = sermon.status === 'draft' ? 'draft' : 'published';
    visibility.value = sermon.visibility;
    videoUrl.value = sermon.video_url ?? '';
    audioUrl.value = sermon.audio_url ?? '';
    thumbnailUrl.value = sermon.thumbnail_url ?? '';
    durationSeconds.value = sermon.duration_seconds;
    tags.value = sermon.tags ?? [];
    mainScripture.value = sermon.main_scripture ?? [];
}

async function goBackToSermons() {
    if (isEditing.value) sermonStore.requestedTab = 'mine';
    menuStore.setMenuWithNoRoute('sermons');

    if (route.name === 'CreateSermon') {
        await router.replace('/');
    }
}

onMounted(async () => {
    await sermonStore.fetchCategories();
    if (sermonStore.editingSermon) {
        populateForm(sermonStore.editingSermon);
    }
});

// Handles the case where the component was already mounted (router reuse)
watch(() => sermonStore.editingSermon, (sermon) => {
    if (sermon) populateForm(sermon);
});

onUnmounted(() => {
    sermonStore.editingSermon = null;
});
</script>

<template>
    <div class="h-full min-h-0 w-full overflow-y-auto scroll-bar-md overflowing-div">
        <div class="w-full max-w-720px mx-auto px-5 py-8">
            <!-- Header -->
            <div class="mb-8">
                <div class="flex items-center gap-2 mb-1">
                    <NButton text @click="goBackToSermons">
                        <template #icon><Icon icon="mdi:arrow-left" /></template>
                    </NButton>
                    <h2 class="font-800 text-2xl m-0">
                        {{ isEditing ? 'Edit Sermon' : 'Submit a Sermon' }}
                    </h2>
                </div>
                <p class="text-sm opacity-60 ml-8">
                    {{ isEditing ? 'Update your sermon details below.' : 'Share your message with the Believers Sword community.' }}
                </p>
            </div>

            <!-- Not signed in -->
            <NAlert v-if="!authStore.isAuthenticated" type="warning" class="mb-6">
                You must be signed in to submit a sermon.
                <NButton text type="warning" @click="menuStore.setMenu('/profile')">Sign in →</NButton>
            </NAlert>

            <NForm v-else label-placement="top" label-width="auto" require-mark-placement="right-hanging">

                <!-- Title -->
                <NFormItem label="Title *" :feedback="errors.title" :validation-status="errors.title ? 'error' : undefined">
                    <NInput v-model:value="title" placeholder="Sermon title..." maxlength="255" show-count />
                </NFormItem>

                <!-- Short Summary -->
                <NFormItem label="Short Summary *" :feedback="errors.shortSummary" :validation-status="errors.shortSummary ? 'error' : undefined">
                    <NInput
                        v-model:value="shortSummary"
                        type="textarea"
                        placeholder="A brief description of this sermon (max 1000 characters)..."
                        :autosize="{ minRows: 2, maxRows: 5 }"
                        maxlength="1000"
                        show-count
                    />
                </NFormItem>

                <!-- Preacher Name -->
                <NFormItem label="Preacher Name">
                    <NInput v-model:value="preacherName" placeholder="Name of the preacher (optional)" maxlength="255" />
                </NFormItem>

                <!-- Category + Date (side by side) -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-4">
                    <NFormItem label="Category">
                        <NSelect
                            v-model:value="categoryId"
                            :options="categoryOptions"
                            placeholder="Select category..."
                            clearable
                            :virtual-scroll="false"
                            :scrollbar-props="selectScrollbarProps"
                        />
                    </NFormItem>
                    <NFormItem label="Sermon Date">
                        <NDatePicker v-model:value="sermonDate" type="date" clearable class="w-full" />
                    </NFormItem>
                </div>

                <!-- Main Scripture Picker -->
                <NFormItem label="Main Scripture">
                    <div class="w-full">
                        <!-- Existing entries -->
                        <div v-if="mainScripture.length" class="flex flex-wrap gap-2 mb-2">
                            <NTag
                                v-for="(s, i) in mainScripture"
                                :key="i"
                                closable
                                @close="removeScripture(i)"
                            >
                                {{ bookLabel(s.book) }} {{ s.chapter }}<span v-if="s.verse.length">:{{ s.verse.join(',') }}</span>
                            </NTag>
                        </div>
                        <!-- Add new entry -->
                        <div class="flex gap-2 flex-wrap items-end">
                            <NSelect
                                v-model:value="newScriptureBook"
                                :options="BIBLE_BOOKS"
                                placeholder="Book"
                                filterable
                                class="!w-180px"
                                :virtual-scroll="false"
                                :scrollbar-props="selectScrollbarProps"
                            />
                            <NInputNumber
                                v-model:value="newScriptureChapter"
                                placeholder="Ch."
                                :min="1"
                                :show-button="false"
                                class="!w-90px"
                            />
                            <NInput
                                v-model:value="newScriptureVerses"
                                placeholder="Verses (e.g. 1,3-5)"
                                class="!w-160px"
                            />
                            <NButton size="small" :disabled="!newScriptureBook || !newScriptureChapter" @click="addScripture">
                                Add
                            </NButton>
                        </div>
                    </div>
                </NFormItem>

                <!-- Tags -->
                <NFormItem label="Tags">
                    <NDynamicTags v-model:value="tags" :max="10" />
                </NFormItem>

                <!-- Content editor -->
                <NFormItem label="Content *" :feedback="errors.content" :validation-status="errors.content ? 'error' : undefined">
                    <div class="w-full bg-white bg-opacity-5 rounded-lg p-2">
                        <Editor v-model="content" overflow editorContentStyle="min-height: 200px; max-height: 500px;" />
                    </div>
                </NFormItem>

                <!-- Media URLs -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-4">
                    <NFormItem label="Video URL">
                        <NInput v-model:value="videoUrl" placeholder="https://..." clearable />
                    </NFormItem>
                    <NFormItem label="Audio URL">
                        <NInput v-model:value="audioUrl" placeholder="https://..." clearable />
                    </NFormItem>
                    <NFormItem label="Thumbnail URL">
                        <NInput v-model:value="thumbnailUrl" placeholder="https://..." clearable />
                    </NFormItem>
                    <NFormItem label="Duration (seconds)">
                        <NInputNumber
                            v-model:value="durationSeconds"
                            placeholder="e.g. 3600 for 1 hour"
                            :min="0"
                            :show-button="false"
                            class="w-full"
                        />
                    </NFormItem>
                </div>

                <!-- Status + Visibility -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-4">
                    <NFormItem label="Status">
                        <NSelect
                            v-model:value="statusValue"
                            :options="statusOptions"
                            :virtual-scroll="false"
                            :scrollbar-props="selectScrollbarProps"
                        />
                    </NFormItem>
                    <NFormItem label="Visibility">
                        <NSelect
                            v-model:value="visibility"
                            :options="visibilityOptions"
                            :virtual-scroll="false"
                            :scrollbar-props="selectScrollbarProps"
                        />
                    </NFormItem>
                </div>

                <!-- Actions -->
                <div class="flex gap-3 mt-4 mb-10">
                    <NButton type="primary" :loading="loading" :disabled="loading" @click="submit">
                        <template #icon><Icon icon="mdi:check" /></template>
                        {{ isEditing ? 'Save Changes' : statusValue === 'published' ? 'Publish Sermon' : 'Save as Draft' }}
                    </NButton>
                    <NButton :disabled="loading" @click="resetForm">
                        Reset
                    </NButton>
                    <NButton text @click="goBackToSermons">
                        Cancel
                    </NButton>
                </div>

            </NForm>
        </div>
    </div>
</template>
