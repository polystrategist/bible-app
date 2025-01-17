import { BookmarkAdd, Attachment } from '@vicons/carbon';
import { EraserSegment24Filled } from '@vicons/fluent';

export const ContextMenuOptions = [
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
        label: "Clear Highlight",
        icon: EraserSegment24Filled,
        key: 'clear-highlight',
    }
];
