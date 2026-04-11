<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { NSpin } from 'naive-ui';
import { useThemeStore } from '../../store/theme';

const route = useRoute();
const themeStore = useThemeStore();
const loading = ref(true);
const results = ref<{ version: string; text: string }[]>([]);

const book_number = Number(route.query.book);
const chapter = Number(route.query.chapter);
const verse = Number(route.query.verse);
const bookName = String(route.query.bookName || `Book ${book_number}`);

const verseRef = computed(() => `${bookName} ${chapter}:${verse}`);
const versionCount = computed(() => results.value.length);

onMounted(async () => {
    results.value = await (window as any).browserWindow.compareVerseGetVerse({
        book_number,
        chapter,
        verse,
    });
    loading.value = false;
});

function close() {
    (window as any).browserWindow.closeCurrentWindow();
}
</script>

<template>
    <div
        class="compare-verse-root h-[100vh] flex flex-col overflow-hidden"
        :class="{ dark: themeStore.isDark }"
    >
        <!-- Title bar / drag region -->
        <div
            class="title-bar flex items-center justify-between px-3 select-none shrink-0"
            style="-webkit-app-region: drag;"
        >
            <span class="text-xs font-semibold opacity-50 tracking-wide uppercase">{{ $t('Compare Verse') }}</span>
            <button
                class="close-btn flex items-center justify-center rounded-full text-lg leading-none"
                style="-webkit-app-region: no-drag;"
                title="Close"
                @click="close"
            >
                ✕
            </button>
        </div>

        <!-- Verse reference header -->
        <div class="verse-header px-4 py-3 shrink-0">
            <h2 class="text-xl font-bold text-[var(--primary-color)] leading-tight">{{ verseRef }}</h2>
            <p class="text-xs opacity-40 mt-0.5">
                {{ loading ? 'Loading…' : `${versionCount} version${versionCount !== 1 ? 's' : ''}` }} · Based on your installed Bible versions
            </p>
        </div>

        <!-- Results list -->
        <div class="flex-1 min-h-0 overflow-y-auto px-3 pb-4 flex flex-col gap-2">
            <!-- Loading -->
            <div v-if="loading" class="flex justify-center items-center h-full">
                <NSpin size="medium" />
            </div>

            <!-- Empty state -->
            <div
                v-else-if="results.length === 0"
                class="flex flex-col items-center justify-center h-full opacity-40 text-sm gap-2"
            >
                <span style="font-size: 2rem;">📖</span>
                <span>{{ $t('no-bible-versions-found') }}</span>
            </div>

            <!-- Version cards -->
            <template v-else>
                <div
                    v-for="item in results"
                    :key="item.version"
                    class="version-card rounded-lg p-3"
                >
                    <div class="text-[10px] font-bold text-[var(--primary-color)] uppercase tracking-widest mb-1.5 opacity-80">
                        {{ item.version }}
                    </div>
                    <div class="text-sm leading-relaxed verse-text" v-html="item.text" />
                </div>
            </template>
        </div>
    </div>
</template>

<style scoped>
.compare-verse-root {
    background: #ffffff;
    color: #1a1a1a;
    font-family: system-ui, sans-serif;
}

.title-bar {
    height: 36px;
    background: rgba(0, 0, 0, 0.04);
    border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.close-btn {
    width: 22px;
    height: 22px;
    background: transparent;
    border: none;
    cursor: pointer;
    font-size: 13px;
    color: inherit;
    opacity: 0.45;
    transition: opacity 0.15s, background 0.15s, color 0.15s;
}

.close-btn:hover {
    opacity: 1;
    background: rgba(220, 38, 38, 0.12);
    color: #dc2626;
}

.verse-header {
    border-bottom: 1px solid rgba(0, 0, 0, 0.07);
}

.version-card {
    background: rgba(0, 0, 0, 0.03);
    border: 1px solid rgba(0, 0, 0, 0.07);
    transition: border-color 0.15s;
}

.version-card:hover {
    border-color: var(--primary-color, #6366f1);
}

/* Dark mode */
.dark.compare-verse-root {
    background: #1e1e2e;
    color: #e0e0e0;
}

.dark .title-bar {
    background: rgba(255, 255, 255, 0.04);
    border-bottom-color: rgba(255, 255, 255, 0.08);
}

.dark .verse-header {
    border-bottom-color: rgba(255, 255, 255, 0.07);
}

.dark .version-card {
    background: rgba(255, 255, 255, 0.04);
    border-color: rgba(255, 255, 255, 0.08);
}

.dark .version-card:hover {
    border-color: var(--primary-color, #818cf8);
}

/* Strip any HTML formatting from verse text (e.g. <s> strong tags from some modules) */
.verse-text :deep(a) { display: none; }
.verse-text :deep(s) {
    text-decoration: none;
    font-size: 9px;
    border: 1px solid rgba(128, 128, 128, 0.4);
    border-radius: 3px;
    padding: 0 2px;
    margin: 0 2px;
}
</style>
