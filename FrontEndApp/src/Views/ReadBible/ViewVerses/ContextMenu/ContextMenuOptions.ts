import type { Component } from 'vue';
import { BookmarkAdd, Attachment } from '@vicons/carbon';
import { EraserSegment24Filled, TabDesktopMultiple20Regular, PaintBrush24Regular, Sparkle24Regular } from '@vicons/fluent';

interface ContextMenuOption {
    label: string;
    description?: string;
    icon: Component;
    key: string;
}

export const ContextMenuOptions: ContextMenuOption[] = [
    {
        label: 'AI Insight',
        description: 'Understand this verse more deeply',
        icon: Sparkle24Regular,
        key: 'ai-insight',
    },
    {
        label: 'Add to Bookmark',
        icon: BookmarkAdd,
        key: 'add-to-bookmark',
    },
    {
        label: 'Create Clip Note',
        icon: Attachment,
        key: 'create-clip-note',
    },
    {
        label: 'Highlight Verse',
        icon: PaintBrush24Regular,
        key: 'highlight-verse',
    },
    {
        label: 'Compare Verse',
        icon: TabDesktopMultiple20Regular,
        key: 'compare-verse',
    },
    {
        label: 'Clear Highlight',
        icon: EraserSegment24Filled,
        key: 'clear-highlight',
    },
];
