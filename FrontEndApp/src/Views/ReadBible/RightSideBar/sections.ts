import type { Component } from 'vue';
import {
    Bookmark24Regular,
    Highlight24Regular,
    Attach24Regular,
    BookLetter24Regular,
} from '@vicons/fluent';
import Bookmarks from './Bookmarks/Bookmarks.vue';
import Highlights from './Highlights/Highlights.vue';
import ClipNotes from './ClipNotes/ClipNotes.vue';
import Dictionary from './BottomContents/Dictionary/Dictionary.vue';
import Reference from './BottomContents/Reference/Reference.vue';

export interface RightPanelSection {
    key: string;
    title: string; // i18n key
    icon: Component;
    component: Component;
    defaultExpanded: boolean;
    defaultSize: number;
    show: boolean;
}

export const rightPanelSections: RightPanelSection[] = [
    { key: 'bible-bookmarks', title: 'Bookmarks', icon: Bookmark24Regular, component: Bookmarks, defaultExpanded: true, defaultSize: 200, show: true },
    { key: 'bible-highlights', title: 'Highlights', icon: Highlight24Regular, component: Highlights, defaultExpanded: false, defaultSize: 200, show: true },
    { key: 'bible-clip-notes', title: 'Clip Notes', icon: Attach24Regular, component: ClipNotes, defaultExpanded: false, defaultSize: 200, show: true },
    { key: 'dictionary', title: 'dictionary', icon: BookLetter24Regular, component: Dictionary, defaultExpanded: false, defaultSize: 200, show: true },
    { key: 'references', title: 'references', icon: BookLetter24Regular, component: Reference, defaultExpanded: false, defaultSize: 200, show: false },
];

export const visibleRightPanelSections = (): RightPanelSection[] =>
    rightPanelSections.filter((s) => s.show);
