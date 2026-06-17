import type { typeNameInterface } from './themes';

/** One curated theme preset = an appearance key + an accent key. Identical to mobile. */
export interface ThemePreset {
    name: string;
    appearance: string; // appearanceThemeOption.key
    accent: typeNameInterface;
}

export const themePresets: ThemePreset[] = [
    { name: 'Candlelight', appearance: 'parchment', accent: 'ochre' },
    { name: 'Morning Sepia', appearance: 'sepia', accent: 'ember' },
    { name: 'Soft Day', appearance: 'cream', accent: 'default' },
    { name: 'Dawnlight', appearance: 'dawn', accent: 'rose' },
    { name: 'Forest Walk', appearance: 'forest', accent: 'sage' },
    { name: 'Arctic Focus', appearance: 'arctic', accent: 'cobalt' },
    { name: 'Nordic Night', appearance: 'nord', accent: 'sky' },
    { name: 'Midnight Gold', appearance: 'midnight', accent: 'default' },
    { name: 'Obsidian Mint', appearance: 'abyss', accent: 'mint' },
    { name: 'Amethyst Dreams', appearance: 'amethyst', accent: 'orchid' },
];
