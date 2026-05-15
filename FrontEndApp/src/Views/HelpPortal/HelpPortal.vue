<script lang="ts" setup>
import { ref, computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { Icon } from '@iconify/vue';
import { NModal } from 'naive-ui';

const { t } = useI18n();

// ── Article definitions (slug-keyed, i18n-safe) ──────────────────────────────

interface StepDef { labelKey: string; detailKey: string }
interface ArticleDef {
    titleKey: string;
    introKey: string;
    steps: StepDef[];
    tipsKeys?: string[];
}

const articleDefs: Record<string, ArticleDef> = {
    'change-translation': {
        titleKey: 'help-portal.article.change-translation.title',
        introKey: 'help-portal.article.change-translation.intro',
        steps: [
            { labelKey: 'help-portal.article.change-translation.step1-label', detailKey: 'help-portal.article.change-translation.step1-detail' },
            { labelKey: 'help-portal.article.change-translation.step2-label', detailKey: 'help-portal.article.change-translation.step2-detail' },
            { labelKey: 'help-portal.article.change-translation.step3-label', detailKey: 'help-portal.article.change-translation.step3-detail' },
        ],
        tipsKeys: ['help-portal.article.change-translation.tip1'],
    },
    'navigate-books': {
        titleKey: 'help-portal.article.navigate-books.title',
        introKey: 'help-portal.article.navigate-books.intro',
        steps: [
            { labelKey: 'help-portal.article.navigate-books.step1-label', detailKey: 'help-portal.article.navigate-books.step1-detail' },
            { labelKey: 'help-portal.article.navigate-books.step2-label', detailKey: 'help-portal.article.navigate-books.step2-detail' },
            { labelKey: 'help-portal.article.navigate-books.step3-label', detailKey: 'help-portal.article.navigate-books.step3-detail' },
            { labelKey: 'help-portal.article.navigate-books.step4-label', detailKey: 'help-portal.article.navigate-books.step4-detail' },
        ],
        tipsKeys: ['help-portal.article.navigate-books.tip1'],
    },
    'font-size': {
        titleKey: 'help-portal.article.font-size.title',
        introKey: 'help-portal.article.font-size.intro',
        steps: [
            { labelKey: 'help-portal.article.font-size.step1-label', detailKey: 'help-portal.article.font-size.step1-detail' },
            { labelKey: 'help-portal.article.font-size.step2-label', detailKey: 'help-portal.article.font-size.step2-detail' },
            { labelKey: 'help-portal.article.font-size.step3-label', detailKey: 'help-portal.article.font-size.step3-detail' },
            { labelKey: 'help-portal.article.font-size.step4-label', detailKey: 'help-portal.article.font-size.step4-detail' },
            { labelKey: 'help-portal.article.font-size.step5-label', detailKey: 'help-portal.article.font-size.step5-detail' },
        ],
        tipsKeys: ['help-portal.article.font-size.tip1'],
    },
    'multiple-bibles': {
        titleKey: 'help-portal.article.multiple-bibles.title',
        introKey: 'help-portal.article.multiple-bibles.intro',
        steps: [
            { labelKey: 'help-portal.article.multiple-bibles.step1-label', detailKey: 'help-portal.article.multiple-bibles.step1-detail' },
            { labelKey: 'help-portal.article.multiple-bibles.step2-label', detailKey: 'help-portal.article.multiple-bibles.step2-detail' },
            { labelKey: 'help-portal.article.multiple-bibles.step3-label', detailKey: 'help-portal.article.multiple-bibles.step3-detail' },
            { labelKey: 'help-portal.article.multiple-bibles.step4-label', detailKey: 'help-portal.article.multiple-bibles.step4-detail' },
        ],
        tipsKeys: ['help-portal.article.multiple-bibles.tip1'],
    },
    'add-bookmark': {
        titleKey: 'help-portal.article.add-bookmark.title',
        introKey: 'help-portal.article.add-bookmark.intro',
        steps: [
            { labelKey: 'help-portal.article.add-bookmark.step1-label', detailKey: 'help-portal.article.add-bookmark.step1-detail' },
            { labelKey: 'help-portal.article.add-bookmark.step2-label', detailKey: 'help-portal.article.add-bookmark.step2-detail' },
            { labelKey: 'help-portal.article.add-bookmark.step3-label', detailKey: 'help-portal.article.add-bookmark.step3-detail' },
            { labelKey: 'help-portal.article.add-bookmark.step4-label', detailKey: 'help-portal.article.add-bookmark.step4-detail' },
        ],
        tipsKeys: ['help-portal.article.add-bookmark.tip1'],
    },
    'highlight-colors': {
        titleKey: 'help-portal.article.highlight-colors.title',
        introKey: 'help-portal.article.highlight-colors.intro',
        steps: [
            { labelKey: 'help-portal.article.highlight-colors.step1-label', detailKey: 'help-portal.article.highlight-colors.step1-detail' },
            { labelKey: 'help-portal.article.highlight-colors.step2-label', detailKey: 'help-portal.article.highlight-colors.step2-detail' },
            { labelKey: 'help-portal.article.highlight-colors.step3-label', detailKey: 'help-portal.article.highlight-colors.step3-detail' },
            { labelKey: 'help-portal.article.highlight-colors.step4-label', detailKey: 'help-portal.article.highlight-colors.step4-detail' },
        ],
        tipsKeys: ['help-portal.article.highlight-colors.tip1'],
    },
    'view-bookmarks': {
        titleKey: 'help-portal.article.view-bookmarks.title',
        introKey: 'help-portal.article.view-bookmarks.intro',
        steps: [
            { labelKey: 'help-portal.article.view-bookmarks.step1-label', detailKey: 'help-portal.article.view-bookmarks.step1-detail' },
            { labelKey: 'help-portal.article.view-bookmarks.step2-label', detailKey: 'help-portal.article.view-bookmarks.step2-detail' },
            { labelKey: 'help-portal.article.view-bookmarks.step3-label', detailKey: 'help-portal.article.view-bookmarks.step3-detail' },
        ],
        tipsKeys: ['help-portal.article.view-bookmarks.tip1'],
    },
    'delete-bookmark': {
        titleKey: 'help-portal.article.delete-bookmark.title',
        introKey: 'help-portal.article.delete-bookmark.intro',
        steps: [
            { labelKey: 'help-portal.article.delete-bookmark.step1-label', detailKey: 'help-portal.article.delete-bookmark.step1-detail' },
            { labelKey: 'help-portal.article.delete-bookmark.step2-label', detailKey: 'help-portal.article.delete-bookmark.step2-detail' },
        ],
    },
    'create-note': {
        titleKey: 'help-portal.article.create-note.title',
        introKey: 'help-portal.article.create-note.intro',
        steps: [
            { labelKey: 'help-portal.article.create-note.step1-label', detailKey: 'help-portal.article.create-note.step1-detail' },
            { labelKey: 'help-portal.article.create-note.step2-label', detailKey: 'help-portal.article.create-note.step2-detail' },
            { labelKey: 'help-portal.article.create-note.step3-label', detailKey: 'help-portal.article.create-note.step3-detail' },
            { labelKey: 'help-portal.article.create-note.step4-label', detailKey: 'help-portal.article.create-note.step4-detail' },
        ],
        tipsKeys: ['help-portal.article.create-note.tip1'],
    },
    'clip-note': {
        titleKey: 'help-portal.article.clip-note.title',
        introKey: 'help-portal.article.clip-note.intro',
        steps: [
            { labelKey: 'help-portal.article.clip-note.step1-label', detailKey: 'help-portal.article.clip-note.step1-detail' },
            { labelKey: 'help-portal.article.clip-note.step2-label', detailKey: 'help-portal.article.clip-note.step2-detail' },
            { labelKey: 'help-portal.article.clip-note.step3-label', detailKey: 'help-portal.article.clip-note.step3-detail' },
            { labelKey: 'help-portal.article.clip-note.step4-label', detailKey: 'help-portal.article.clip-note.step4-detail' },
        ],
    },
    'export-note': {
        titleKey: 'help-portal.article.export-note.title',
        introKey: 'help-portal.article.export-note.intro',
        steps: [
            { labelKey: 'help-portal.article.export-note.step1-label', detailKey: 'help-portal.article.export-note.step1-detail' },
            { labelKey: 'help-portal.article.export-note.step2-label', detailKey: 'help-portal.article.export-note.step2-detail' },
            { labelKey: 'help-portal.article.export-note.step3-label', detailKey: 'help-portal.article.export-note.step3-detail' },
            { labelKey: 'help-portal.article.export-note.step4-label', detailKey: 'help-portal.article.export-note.step4-detail' },
        ],
        tipsKeys: ['help-portal.article.export-note.tip1'],
    },
    'autosave': {
        titleKey: 'help-portal.article.autosave.title',
        introKey: 'help-portal.article.autosave.intro',
        steps: [
            { labelKey: 'help-portal.article.autosave.step1-label', detailKey: 'help-portal.article.autosave.step1-detail' },
            { labelKey: 'help-portal.article.autosave.step2-label', detailKey: 'help-portal.article.autosave.step2-detail' },
            { labelKey: 'help-portal.article.autosave.step3-label', detailKey: 'help-portal.article.autosave.step3-detail' },
            { labelKey: 'help-portal.article.autosave.step4-label', detailKey: 'help-portal.article.autosave.step4-detail' },
        ],
        tipsKeys: ['help-portal.article.autosave.tip1'],
    },
    'add-prayer': {
        titleKey: 'help-portal.article.add-prayer.title',
        introKey: 'help-portal.article.add-prayer.intro',
        steps: [
            { labelKey: 'help-portal.article.add-prayer.step1-label', detailKey: 'help-portal.article.add-prayer.step1-detail' },
            { labelKey: 'help-portal.article.add-prayer.step2-label', detailKey: 'help-portal.article.add-prayer.step2-detail' },
            { labelKey: 'help-portal.article.add-prayer.step3-label', detailKey: 'help-portal.article.add-prayer.step3-detail' },
        ],
        tipsKeys: ['help-portal.article.add-prayer.tip1'],
    },
    'mark-done': {
        titleKey: 'help-portal.article.mark-done.title',
        introKey: 'help-portal.article.mark-done.intro',
        steps: [
            { labelKey: 'help-portal.article.mark-done.step1-label', detailKey: 'help-portal.article.mark-done.step1-detail' },
            { labelKey: 'help-portal.article.mark-done.step2-label', detailKey: 'help-portal.article.mark-done.step2-detail' },
            { labelKey: 'help-portal.article.mark-done.step3-label', detailKey: 'help-portal.article.mark-done.step3-detail' },
        ],
        tipsKeys: ['help-portal.article.mark-done.tip1'],
    },
    'reorder-prayer': {
        titleKey: 'help-portal.article.reorder-prayer.title',
        introKey: 'help-portal.article.reorder-prayer.intro',
        steps: [
            { labelKey: 'help-portal.article.reorder-prayer.step1-label', detailKey: 'help-portal.article.reorder-prayer.step1-detail' },
            { labelKey: 'help-portal.article.reorder-prayer.step2-label', detailKey: 'help-portal.article.reorder-prayer.step2-detail' },
        ],
    },
    'edit-delete-prayer': {
        titleKey: 'help-portal.article.edit-delete-prayer.title',
        introKey: 'help-portal.article.edit-delete-prayer.intro',
        steps: [
            { labelKey: 'help-portal.article.edit-delete-prayer.step1-label', detailKey: 'help-portal.article.edit-delete-prayer.step1-detail' },
            { labelKey: 'help-portal.article.edit-delete-prayer.step2-label', detailKey: 'help-portal.article.edit-delete-prayer.step2-detail' },
        ],
    },
    'devo-five-steps': {
        titleKey: 'help-portal.article.devo-five-steps.title',
        introKey: 'help-portal.article.devo-five-steps.intro',
        steps: [
            { labelKey: 'help-portal.article.devo-five-steps.step1-label', detailKey: 'help-portal.article.devo-five-steps.step1-detail' },
            { labelKey: 'help-portal.article.devo-five-steps.step2-label', detailKey: 'help-portal.article.devo-five-steps.step2-detail' },
            { labelKey: 'help-portal.article.devo-five-steps.step3-label', detailKey: 'help-portal.article.devo-five-steps.step3-detail' },
            { labelKey: 'help-portal.article.devo-five-steps.step4-label', detailKey: 'help-portal.article.devo-five-steps.step4-detail' },
            { labelKey: 'help-portal.article.devo-five-steps.step5-label', detailKey: 'help-portal.article.devo-five-steps.step5-detail' },
        ],
        tipsKeys: ['help-portal.article.devo-five-steps.tip1'],
    },
    'devo-language': {
        titleKey: 'help-portal.article.devo-language.title',
        introKey: 'help-portal.article.devo-language.intro',
        steps: [
            { labelKey: 'help-portal.article.devo-language.step1-label', detailKey: 'help-portal.article.devo-language.step1-detail' },
            { labelKey: 'help-portal.article.devo-language.step2-label', detailKey: 'help-portal.article.devo-language.step2-detail' },
            { labelKey: 'help-portal.article.devo-language.step3-label', detailKey: 'help-portal.article.devo-language.step3-detail' },
        ],
    },
    'devo-verse-preview': {
        titleKey: 'help-portal.article.devo-verse-preview.title',
        introKey: 'help-portal.article.devo-verse-preview.intro',
        steps: [
            { labelKey: 'help-portal.article.devo-verse-preview.step1-label', detailKey: 'help-portal.article.devo-verse-preview.step1-detail' },
            { labelKey: 'help-portal.article.devo-verse-preview.step2-label', detailKey: 'help-portal.article.devo-verse-preview.step2-detail' },
            { labelKey: 'help-portal.article.devo-verse-preview.step3-label', detailKey: 'help-portal.article.devo-verse-preview.step3-detail' },
        ],
        tipsKeys: ['help-portal.article.devo-verse-preview.tip1'],
    },
    'create-sermon': {
        titleKey: 'help-portal.article.create-sermon.title',
        introKey: 'help-portal.article.create-sermon.intro',
        steps: [
            { labelKey: 'help-portal.article.create-sermon.step1-label', detailKey: 'help-portal.article.create-sermon.step1-detail' },
            { labelKey: 'help-portal.article.create-sermon.step2-label', detailKey: 'help-portal.article.create-sermon.step2-detail' },
            { labelKey: 'help-portal.article.create-sermon.step3-label', detailKey: 'help-portal.article.create-sermon.step3-detail' },
            { labelKey: 'help-portal.article.create-sermon.step4-label', detailKey: 'help-portal.article.create-sermon.step4-detail' },
            { labelKey: 'help-portal.article.create-sermon.step5-label', detailKey: 'help-portal.article.create-sermon.step5-detail' },
        ],
    },
    'rich-text-editor': {
        titleKey: 'help-portal.article.rich-text-editor.title',
        introKey: 'help-portal.article.rich-text-editor.intro',
        steps: [
            { labelKey: 'help-portal.article.rich-text-editor.step1-label', detailKey: 'help-portal.article.rich-text-editor.step1-detail' },
            { labelKey: 'help-portal.article.rich-text-editor.step2-label', detailKey: 'help-portal.article.rich-text-editor.step2-detail' },
            { labelKey: 'help-portal.article.rich-text-editor.step3-label', detailKey: 'help-portal.article.rich-text-editor.step3-detail' },
        ],
    },
    'view-sermons': {
        titleKey: 'help-portal.article.view-sermons.title',
        introKey: 'help-portal.article.view-sermons.intro',
        steps: [
            { labelKey: 'help-portal.article.view-sermons.step1-label', detailKey: 'help-portal.article.view-sermons.step1-detail' },
            { labelKey: 'help-portal.article.view-sermons.step2-label', detailKey: 'help-portal.article.view-sermons.step2-detail' },
            { labelKey: 'help-portal.article.view-sermons.step3-label', detailKey: 'help-portal.article.view-sermons.step3-detail' },
        ],
        tipsKeys: ['help-portal.article.view-sermons.tip1'],
    },
    'sign-in-sync': {
        titleKey: 'help-portal.article.sign-in-sync.title',
        introKey: 'help-portal.article.sign-in-sync.intro',
        steps: [
            { labelKey: 'help-portal.article.sign-in-sync.step1-label', detailKey: 'help-portal.article.sign-in-sync.step1-detail' },
            { labelKey: 'help-portal.article.sign-in-sync.step2-label', detailKey: 'help-portal.article.sign-in-sync.step2-detail' },
            { labelKey: 'help-portal.article.sign-in-sync.step3-label', detailKey: 'help-portal.article.sign-in-sync.step3-detail' },
        ],
        tipsKeys: ['help-portal.article.sign-in-sync.tip1'],
    },
    'push-pull-sync': {
        titleKey: 'help-portal.article.push-pull-sync.title',
        introKey: 'help-portal.article.push-pull-sync.intro',
        steps: [
            { labelKey: 'help-portal.article.push-pull-sync.step1-label', detailKey: 'help-portal.article.push-pull-sync.step1-detail' },
            { labelKey: 'help-portal.article.push-pull-sync.step2-label', detailKey: 'help-portal.article.push-pull-sync.step2-detail' },
            { labelKey: 'help-portal.article.push-pull-sync.step3-label', detailKey: 'help-portal.article.push-pull-sync.step3-detail' },
        ],
        tipsKeys: ['help-portal.article.push-pull-sync.tip1'],
    },
    'sync-conflicts': {
        titleKey: 'help-portal.article.sync-conflicts.title',
        introKey: 'help-portal.article.sync-conflicts.intro',
        steps: [
            { labelKey: 'help-portal.article.sync-conflicts.step1-label', detailKey: 'help-portal.article.sync-conflicts.step1-detail' },
            { labelKey: 'help-portal.article.sync-conflicts.step2-label', detailKey: 'help-portal.article.sync-conflicts.step2-detail' },
        ],
        tipsKeys: ['help-portal.article.sync-conflicts.tip1'],
    },
    'disable-sync': {
        titleKey: 'help-portal.article.disable-sync.title',
        introKey: 'help-portal.article.disable-sync.intro',
        steps: [
            { labelKey: 'help-portal.article.disable-sync.step1-label', detailKey: 'help-portal.article.disable-sync.step1-detail' },
            { labelKey: 'help-portal.article.disable-sync.step2-label', detailKey: 'help-portal.article.disable-sync.step2-detail' },
            { labelKey: 'help-portal.article.disable-sync.step3-label', detailKey: 'help-portal.article.disable-sync.step3-detail' },
        ],
    },
    'download-translation': {
        titleKey: 'help-portal.article.download-translation.title',
        introKey: 'help-portal.article.download-translation.intro',
        steps: [
            { labelKey: 'help-portal.article.download-translation.step1-label', detailKey: 'help-portal.article.download-translation.step1-detail' },
            { labelKey: 'help-portal.article.download-translation.step2-label', detailKey: 'help-portal.article.download-translation.step2-detail' },
            { labelKey: 'help-portal.article.download-translation.step3-label', detailKey: 'help-portal.article.download-translation.step3-detail' },
            { labelKey: 'help-portal.article.download-translation.step4-label', detailKey: 'help-portal.article.download-translation.step4-detail' },
            { labelKey: 'help-portal.article.download-translation.step5-label', detailKey: 'help-portal.article.download-translation.step5-detail' },
        ],
        tipsKeys: ['help-portal.article.download-translation.tip1'],
    },
    'import-bible': {
        titleKey: 'help-portal.article.import-bible.title',
        introKey: 'help-portal.article.import-bible.intro',
        steps: [
            { labelKey: 'help-portal.article.import-bible.step1-label', detailKey: 'help-portal.article.import-bible.step1-detail' },
            { labelKey: 'help-portal.article.import-bible.step2-label', detailKey: 'help-portal.article.import-bible.step2-detail' },
            { labelKey: 'help-portal.article.import-bible.step3-label', detailKey: 'help-portal.article.import-bible.step3-detail' },
            { labelKey: 'help-portal.article.import-bible.step4-label', detailKey: 'help-portal.article.import-bible.step4-detail' },
            { labelKey: 'help-portal.article.import-bible.step5-label', detailKey: 'help-portal.article.import-bible.step5-detail' },
        ],
        tipsKeys: ['help-portal.article.import-bible.tip1'],
    },
    'remove-translation': {
        titleKey: 'help-portal.article.remove-translation.title',
        introKey: 'help-portal.article.remove-translation.intro',
        steps: [
            { labelKey: 'help-portal.article.remove-translation.step1-label', detailKey: 'help-portal.article.remove-translation.step1-detail' },
            { labelKey: 'help-portal.article.remove-translation.step2-label', detailKey: 'help-portal.article.remove-translation.step2-detail' },
            { labelKey: 'help-portal.article.remove-translation.step3-label', detailKey: 'help-portal.article.remove-translation.step3-detail' },
        ],
        tipsKeys: ['help-portal.article.remove-translation.tip1'],
    },
    'file-formats': {
        titleKey: 'help-portal.article.file-formats.title',
        introKey: 'help-portal.article.file-formats.intro',
        steps: [
            { labelKey: 'help-portal.article.file-formats.step1-label', detailKey: 'help-portal.article.file-formats.step1-detail' },
            { labelKey: 'help-portal.article.file-formats.step2-label', detailKey: 'help-portal.article.file-formats.step2-detail' },
        ],
        tipsKeys: ['help-portal.article.file-formats.tip1'],
    },
    'setup-piper': {
        titleKey: 'help-portal.article.setup-piper.title',
        introKey: 'help-portal.article.setup-piper.intro',
        steps: [
            { labelKey: 'help-portal.article.setup-piper.step1-label', detailKey: 'help-portal.article.setup-piper.step1-detail' },
            { labelKey: 'help-portal.article.setup-piper.step2-label', detailKey: 'help-portal.article.setup-piper.step2-detail' },
            { labelKey: 'help-portal.article.setup-piper.step3-label', detailKey: 'help-portal.article.setup-piper.step3-detail' },
            { labelKey: 'help-portal.article.setup-piper.step4-label', detailKey: 'help-portal.article.setup-piper.step4-detail' },
        ],
        tipsKeys: ['help-portal.article.setup-piper.tip1'],
    },
    'choose-voice': {
        titleKey: 'help-portal.article.choose-voice.title',
        introKey: 'help-portal.article.choose-voice.intro',
        steps: [
            { labelKey: 'help-portal.article.choose-voice.step1-label', detailKey: 'help-portal.article.choose-voice.step1-detail' },
            { labelKey: 'help-portal.article.choose-voice.step2-label', detailKey: 'help-portal.article.choose-voice.step2-detail' },
            { labelKey: 'help-portal.article.choose-voice.step3-label', detailKey: 'help-portal.article.choose-voice.step3-detail' },
        ],
    },
    'playback-speed': {
        titleKey: 'help-portal.article.playback-speed.title',
        introKey: 'help-portal.article.playback-speed.intro',
        steps: [
            { labelKey: 'help-portal.article.playback-speed.step1-label', detailKey: 'help-portal.article.playback-speed.step1-detail' },
            { labelKey: 'help-portal.article.playback-speed.step2-label', detailKey: 'help-portal.article.playback-speed.step2-detail' },
            { labelKey: 'help-portal.article.playback-speed.step3-label', detailKey: 'help-portal.article.playback-speed.step3-detail' },
        ],
    },
};

// ── Category definitions ──────────────────────────────────────────────────────

interface CategoryDef {
    icon: string;
    titleKey: string;
    descKey: string;
    color: string;
    articleSlugs: string[];
}

const categoryDefs: CategoryDef[] = [
    {
        icon: 'mdi:book-open-page-variant',
        titleKey: 'help-portal.cat.reading-bible',
        descKey: 'help-portal.cat.reading-bible.desc',
        color: '#6366f1',
        articleSlugs: ['change-translation', 'navigate-books', 'font-size', 'multiple-bibles'],
    },
    {
        icon: 'mdi:bookmark-multiple',
        titleKey: 'help-portal.cat.bookmarks-highlights',
        descKey: 'help-portal.cat.bookmarks-highlights.desc',
        color: '#f59e0b',
        articleSlugs: ['add-bookmark', 'highlight-colors', 'view-bookmarks', 'delete-bookmark'],
    },
    {
        icon: 'mdi:note-text',
        titleKey: 'help-portal.cat.notes-clip-notes',
        descKey: 'help-portal.cat.notes-clip-notes.desc',
        color: '#10b981',
        articleSlugs: ['create-note', 'clip-note', 'export-note', 'autosave'],
    },
    {
        icon: 'mdi:hands-pray',
        titleKey: 'Prayer List',
        descKey: 'help-portal.cat.prayer-list.desc',
        color: '#8b5cf6',
        articleSlugs: ['add-prayer', 'mark-done', 'reorder-prayer', 'edit-delete-prayer'],
    },
    {
        icon: 'mdi:calendar-heart',
        titleKey: 'Daily Devotional',
        descKey: 'help-portal.cat.daily-devotional.desc',
        color: '#ec4899',
        articleSlugs: ['devo-five-steps', 'devo-language', 'devo-verse-preview'],
    },
    {
        icon: 'mdi:microphone-message',
        titleKey: 'Sermons',
        descKey: 'help-portal.cat.sermons.desc',
        color: '#0ea5e9',
        articleSlugs: ['create-sermon', 'rich-text-editor', 'view-sermons'],
    },
    {
        icon: 'mdi:cloud-sync',
        titleKey: 'help-portal.cat.cloud-sync',
        descKey: 'help-portal.cat.cloud-sync.desc',
        color: '#14b8a6',
        articleSlugs: ['sign-in-sync', 'push-pull-sync', 'sync-conflicts', 'disable-sync'],
    },
    {
        icon: 'mdi:book-search',
        titleKey: 'help-portal.cat.bible-modules',
        descKey: 'help-portal.cat.bible-modules.desc',
        color: '#f97316',
        articleSlugs: ['download-translation', 'import-bible', 'remove-translation', 'file-formats'],
    },
    {
        icon: 'mdi:volume-high',
        titleKey: 'help-portal.cat.tts',
        descKey: 'help-portal.cat.tts.desc',
        color: '#a855f7',
        articleSlugs: ['setup-piper', 'choose-voice', 'playback-speed'],
    },
];

// ── Shortcut definitions ──────────────────────────────────────────────────────

const shortcutDefs = [
    { keys: ['Ctrl', 'F'], descKey: 'help-portal.shortcut.search' },
    { keys: ['←', '→'], descKey: 'help-portal.shortcut.navigate' },
    { keys: ['Ctrl', '+'], descKey: 'help-portal.shortcut.font-plus' },
    { keys: ['Ctrl', '-'], descKey: 'help-portal.shortcut.font-minus' },
    { keys: ['Ctrl', 'B'], descKey: 'help-portal.shortcut.bookmark' },
    { keys: ['Ctrl', 'N'], descKey: 'help-portal.shortcut.new-note' },
    { keys: ['F11'], descKey: 'help-portal.shortcut.fullscreen' },
];

// ── FAQ definitions ───────────────────────────────────────────────────────────

const faqDefs = [
    { qKey: 'help-portal.faq1.q', aKey: 'help-portal.faq1.a' },
    { qKey: 'help-portal.faq2.q', aKey: 'help-portal.faq2.a' },
    { qKey: 'help-portal.faq3.q', aKey: 'help-portal.faq3.a' },
    { qKey: 'help-portal.faq4.q', aKey: 'help-portal.faq4.a' },
    { qKey: 'help-portal.faq5.q', aKey: 'help-portal.faq5.a' },
    { qKey: 'help-portal.faq6.q', aKey: 'help-portal.faq6.a' },
    { qKey: 'help-portal.faq7.q', aKey: 'help-portal.faq7.a' },
];

// ── Reactive state ────────────────────────────────────────────────────────────

const searchQuery = ref('');
const openFaq = ref<number | null>(null);
const selectedArticleSlug = ref<string | null>(null);
const showArticleModal = ref(false);

// ── Computed translated data ──────────────────────────────────────────────────

const categories = computed(() =>
    categoryDefs.map((def) => ({
        icon: def.icon,
        color: def.color,
        title: t(def.titleKey),
        description: t(def.descKey),
        articles: def.articleSlugs.map((slug) => ({
            slug,
            title: t(articleDefs[slug].titleKey),
        })),
    }))
);

const shortcuts = computed(() =>
    shortcutDefs.map((s) => ({ keys: s.keys, description: t(s.descKey) }))
);

const faqs = computed(() =>
    faqDefs.map((f) => ({ question: t(f.qKey), answer: t(f.aKey) }))
);

const selectedArticle = computed(() => {
    const slug = selectedArticleSlug.value;
    if (!slug) return null;
    const def = articleDefs[slug];
    if (!def) return null;
    return {
        title: t(def.titleKey),
        intro: t(def.introKey),
        steps: def.steps.map((s) => ({ label: t(s.labelKey), detail: t(s.detailKey) })),
        tips: def.tipsKeys?.map((k) => t(k)),
    };
});

const filteredCategories = computed(() => {
    if (!searchQuery.value.trim()) return categories.value;
    const q = searchQuery.value.toLowerCase();
    return categories.value.filter(
        (c) =>
            c.title.toLowerCase().includes(q) ||
            c.description.toLowerCase().includes(q) ||
            c.articles.some((a) => a.title.toLowerCase().includes(q))
    );
});

const filteredFaqs = computed(() => {
    if (!searchQuery.value.trim()) return faqs.value;
    const q = searchQuery.value.toLowerCase();
    return faqs.value.filter(
        (f) => f.question.toLowerCase().includes(q) || f.answer.toLowerCase().includes(q)
    );
});

// ── Actions ───────────────────────────────────────────────────────────────────

function openArticle(slug: string) {
    selectedArticleSlug.value = slug;
    showArticleModal.value = true;
}

function toggleFaq(i: number) {
    openFaq.value = openFaq.value === i ? null : i;
}
</script>

<template>
    <div class="help-portal">
        <!-- Hero -->
        <div class="help-hero">
            <div class="help-hero-icon">
                <Icon icon="mdi:lifebuoy" />
            </div>
            <h1 class="help-hero-title">{{ $t('Help Portal') }}</h1>
            <p class="help-hero-sub">{{ $t('help-portal.subtitle') }}</p>
            <div class="help-search-wrap">
                <Icon icon="mdi:magnify" class="help-search-icon" />
                <input
                    v-model="searchQuery"
                    class="help-search"
                    type="text"
                    :placeholder="$t('help-portal.search-placeholder')"
                />
                <button v-if="searchQuery" class="help-search-clear" @click="searchQuery = ''">
                    <Icon icon="mdi:close" />
                </button>
            </div>
        </div>

        <div class="help-body">
            <!-- Categories -->
            <section class="help-section">
                <h2 class="help-section-title">{{ $t('help-portal.browse-by-topic') }}</h2>
                <div v-if="filteredCategories.length === 0" class="help-empty">
                    <Icon icon="mdi:file-search-outline" class="help-empty-icon" />
                    <p>{{ $t('help-portal.no-topics', { query: searchQuery }) }}</p>
                </div>
                <div v-else class="help-grid">
                    <div v-for="cat in filteredCategories" :key="cat.title" class="help-card">
                        <div
                            class="help-card-icon-wrap"
                            :style="{ background: cat.color + '20', color: cat.color }"
                        >
                            <Icon :icon="cat.icon" />
                        </div>
                        <div class="help-card-body">
                            <div class="help-card-title">{{ cat.title }}</div>
                            <div class="help-card-desc">{{ cat.description }}</div>
                            <ul class="help-card-articles">
                                <li
                                    v-for="article in cat.articles"
                                    :key="article.slug"
                                    class="help-article-link"
                                    @click="openArticle(article.slug)"
                                >
                                    <Icon icon="mdi:chevron-right" class="help-article-chevron" />
                                    {{ article.title }}
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Keyboard Shortcuts -->
            <section v-if="!searchQuery" class="help-section">
                <h2 class="help-section-title">{{ $t('help-portal.keyboard-shortcuts') }}</h2>
                <div class="help-shortcuts-grid">
                    <div v-for="s in shortcuts" :key="s.description" class="help-shortcut-row">
                        <div class="help-keys">
                            <kbd v-for="k in s.keys" :key="k" class="help-kbd">{{ k }}</kbd>
                        </div>
                        <span class="help-shortcut-desc">{{ s.description }}</span>
                    </div>
                </div>
            </section>

            <!-- FAQ -->
            <section class="help-section">
                <h2 class="help-section-title">{{ $t('help-portal.faq-title') }}</h2>
                <div v-if="filteredFaqs.length === 0" class="help-empty">
                    <Icon icon="mdi:comment-question-outline" class="help-empty-icon" />
                    <p>{{ $t('help-portal.no-faqs', { query: searchQuery }) }}</p>
                </div>
                <div v-else class="help-faq-list">
                    <div
                        v-for="(faq, i) in filteredFaqs"
                        :key="i"
                        class="help-faq-item"
                        :class="{ 'is-open': openFaq === i }"
                    >
                        <button class="help-faq-q" @click="toggleFaq(i)">
                            <span>{{ faq.question }}</span>
                            <Icon
                                :icon="openFaq === i ? 'mdi:chevron-up' : 'mdi:chevron-down'"
                                class="help-faq-chevron"
                            />
                        </button>
                        <div v-if="openFaq === i" class="help-faq-a">{{ faq.answer }}</div>
                    </div>
                </div>
            </section>

            <!-- Footer note -->
            <div class="help-footer-note">
                <Icon icon="mdi:github" />
                {{ $t('help-portal.bug-note') }} &nbsp;
                <a href="https://github.com/Broskie/believers-sword/issues" target="_blank">{{
                    $t('help-portal.github-link')
                }}</a>
            </div>
        </div>

        <!-- Article Modal -->
        <NModal
            v-model:show="showArticleModal"
            preset="card"
            :style="{ maxWidth: '560px', width: '90vw' }"
            :bordered="false"
            :segmented="{ content: true }"
        >
            <template #header>
                <div class="article-modal-header">
                    <Icon icon="mdi:book-open-outline" class="article-modal-header-icon" />
                    {{ selectedArticle?.title }}
                </div>
            </template>

            <div v-if="selectedArticle" class="article-modal-body">
                <p class="article-intro">{{ selectedArticle.intro }}</p>

                <ol v-if="selectedArticle.steps?.length" class="article-steps">
                    <li v-for="step in selectedArticle.steps" :key="step.label" class="article-step">
                        <div class="article-step-label">{{ step.label }}</div>
                        <div class="article-step-detail">{{ step.detail }}</div>
                    </li>
                </ol>

                <div v-if="selectedArticle.tips?.length" class="article-tips">
                    <div v-for="tip in selectedArticle.tips" :key="tip" class="article-tip">
                        <Icon icon="mdi:lightbulb-outline" class="article-tip-icon" />
                        <span>{{ tip }}</span>
                    </div>
                </div>
            </div>
        </NModal>
    </div>
</template>

<style scoped>
.help-portal {
    height: 100%;
    overflow-y: auto;
    font-family: var(--bible-font-family, 'Poppins'), sans-serif;
}

/* ── Hero ── */
.help-hero {
    text-align: center;
    padding: 48px 24px 36px;
    border-bottom: 1px solid color-mix(in srgb, currentColor 8%, transparent);
}

.help-hero-icon {
    font-size: 48px;
    color: var(--primary-color);
    line-height: 1;
    margin-bottom: 14px;
}

.help-hero-title {
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 8px;
}

.help-hero-sub {
    font-size: 14px;
    opacity: 0.5;
    margin-bottom: 24px;
}

.help-search-wrap {
    position: relative;
    max-width: 440px;
    margin: 0 auto;
}

.help-search-icon {
    position: absolute;
    left: 14px;
    top: 50%;
    transform: translateY(-50%);
    opacity: 0.4;
    font-size: 18px;
    pointer-events: none;
}

.help-search {
    width: 100%;
    padding: 10px 40px 10px 42px;
    border-radius: 10px;
    border: 1px solid color-mix(in srgb, currentColor 15%, transparent);
    background: color-mix(in srgb, currentColor 5%, transparent);
    color: inherit;
    font-size: 14px;
    outline: none;
    transition: border-color 0.2s;
    box-sizing: border-box;
}

.help-search:focus {
    border-color: var(--primary-color);
}

.help-search-clear {
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    cursor: pointer;
    opacity: 0.4;
    color: inherit;
    font-size: 16px;
    display: flex;
    align-items: center;
    padding: 0;
}

.help-search-clear:hover {
    opacity: 0.8;
}

/* ── Body ── */
.help-body {
    max-width: 860px;
    margin: 0 auto;
    padding: 36px 24px 64px;
}

.help-section {
    margin-bottom: 48px;
}

.help-section-title {
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    opacity: 0.4;
    margin-bottom: 18px;
}

/* ── Category Grid ── */
.help-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 14px;
}

.help-card {
    display: flex;
    gap: 14px;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid color-mix(in srgb, currentColor 10%, transparent);
    background: color-mix(in srgb, currentColor 3%, transparent);
    transition: background 0.15s, border-color 0.15s;
}

.help-card:hover {
    background: color-mix(in srgb, currentColor 6%, transparent);
    border-color: color-mix(in srgb, currentColor 18%, transparent);
}

.help-card-icon-wrap {
    flex-shrink: 0;
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
}

.help-card-body {
    flex: 1;
    min-width: 0;
}

.help-card-title {
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 4px;
}

.help-card-desc {
    font-size: 11px;
    opacity: 0.55;
    margin-bottom: 10px;
    line-height: 1.5;
}

.help-card-articles {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.help-article-link {
    font-size: 11px;
    display: flex;
    align-items: center;
    gap: 2px;
    cursor: pointer;
    color: var(--primary-color);
    opacity: 0.8;
    border-radius: 4px;
    padding: 2px 4px 2px 0;
    transition: opacity 0.15s;
}

.help-article-link:hover {
    opacity: 1;
    text-decoration: underline;
}

.help-article-chevron {
    font-size: 13px;
    flex-shrink: 0;
}

/* ── Shortcuts ── */
.help-shortcuts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 10px;
}

.help-shortcut-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 14px;
    border-radius: 8px;
    background: color-mix(in srgb, currentColor 4%, transparent);
    border: 1px solid color-mix(in srgb, currentColor 8%, transparent);
}

.help-keys {
    display: flex;
    gap: 4px;
    flex-shrink: 0;
}

.help-kbd {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 2px 7px;
    border-radius: 5px;
    font-size: 11px;
    font-weight: 600;
    font-family: monospace;
    background: color-mix(in srgb, var(--primary-color) 12%, transparent);
    color: var(--primary-color);
    border: 1px solid color-mix(in srgb, var(--primary-color) 30%, transparent);
    white-space: nowrap;
}

.help-shortcut-desc {
    font-size: 12px;
    opacity: 0.75;
}

/* ── FAQ ── */
.help-faq-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.help-faq-item {
    border-radius: 10px;
    border: 1px solid color-mix(in srgb, currentColor 10%, transparent);
    overflow: hidden;
    transition: border-color 0.15s;
}

.help-faq-item.is-open {
    border-color: color-mix(in srgb, var(--primary-color) 40%, transparent);
}

.help-faq-q {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 14px 16px;
    background: none;
    border: none;
    cursor: pointer;
    color: inherit;
    font-size: 13px;
    font-weight: 600;
    text-align: left;
    transition: background 0.15s;
}

.help-faq-q:hover {
    background: color-mix(in srgb, currentColor 4%, transparent);
}

.help-faq-chevron {
    flex-shrink: 0;
    font-size: 18px;
    opacity: 0.5;
}

.help-faq-a {
    padding: 12px 16px 14px;
    font-size: 13px;
    line-height: 1.7;
    opacity: 0.75;
    border-top: 1px solid color-mix(in srgb, currentColor 8%, transparent);
}

/* ── Empty state ── */
.help-empty {
    text-align: center;
    padding: 32px 0;
    opacity: 0.4;
}

.help-empty-icon {
    font-size: 40px;
    margin-bottom: 10px;
}

.help-empty p {
    font-size: 13px;
}

/* ── Footer note ── */
.help-footer-note {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    font-size: 12px;
    opacity: 0.45;
    padding-top: 8px;
}

.help-footer-note a {
    color: var(--primary-color);
    text-decoration: none;
    opacity: 1;
}

.help-footer-note a:hover {
    text-decoration: underline;
}

/* ── Article Modal ── */
.article-modal-header {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 15px;
    font-weight: 700;
}

.article-modal-header-icon {
    color: var(--primary-color);
    font-size: 20px;
    flex-shrink: 0;
}

.article-modal-body {
    padding: 4px 0 8px;
}

.article-intro {
    font-size: 13px;
    line-height: 1.7;
    opacity: 0.75;
    margin-bottom: 20px;
}

.article-steps {
    list-style: none;
    padding: 0;
    margin: 0 0 20px;
    display: flex;
    flex-direction: column;
    gap: 14px;
    counter-reset: steps;
}

.article-step {
    display: flex;
    gap: 14px;
    counter-increment: steps;
}

.article-step::before {
    content: counter(steps);
    flex-shrink: 0;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: color-mix(in srgb, var(--primary-color) 15%, transparent);
    color: var(--primary-color);
    font-size: 11px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 1px;
}

.article-step-label {
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 3px;
}

.article-step-detail {
    font-size: 12px;
    line-height: 1.6;
    opacity: 0.7;
}

.article-tips {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.article-tip {
    display: flex;
    gap: 8px;
    align-items: flex-start;
    padding: 10px 12px;
    border-radius: 8px;
    background: color-mix(in srgb, var(--primary-color) 8%, transparent);
    border: 1px solid color-mix(in srgb, var(--primary-color) 20%, transparent);
    font-size: 12px;
    line-height: 1.6;
}

.article-tip-icon {
    color: var(--primary-color);
    font-size: 16px;
    flex-shrink: 0;
    margin-top: 1px;
}
</style>
