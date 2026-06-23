import type { typeNameInterface } from './themes';

/** One curated theme preset = an appearance key + an accent key. Identical to mobile. */
export interface ThemePreset {
    name: string;
    appearance: string; // appearanceThemeOption.key
    accent: typeNameInterface;
}

export const themePresets: ThemePreset[] = [
    // Brand default
    { name: 'Default', appearance: 'light', accent: 'default' },
    { name: 'Default Dark', appearance: 'irisdark', accent: 'default' },
    // Light
    { name: 'Candlelight', appearance: 'parchment', accent: 'ochre' },
    { name: 'Morning Sepia', appearance: 'sepia', accent: 'ember' },
    { name: 'Soft Day', appearance: 'cream', accent: 'gold' },
    { name: 'Dawnlight', appearance: 'dawn', accent: 'rose' },
    { name: 'Forest Walk', appearance: 'forest', accent: 'sage' },
    { name: 'Arctic Focus', appearance: 'arctic', accent: 'cobalt' },
    { name: 'Clear Sky', appearance: 'light', accent: 'ocean' },
    { name: 'Coral Blush', appearance: 'rosepaper', accent: 'reds' },
    { name: 'Desert Sand', appearance: 'sandstone', accent: 'amber' },
    { name: 'Lavender Fields', appearance: 'lavender', accent: 'indigo' },
    { name: 'Meadow', appearance: 'moss', accent: 'olive' },
    { name: 'Warm Cocoa', appearance: 'cream', accent: 'mocha' },
    { name: 'Cathedral', appearance: 'parchment', accent: 'garnet' },
    { name: 'Rosewood', appearance: 'rosepaper', accent: 'plum' },
    { name: 'Sapphire Day', appearance: 'arctic', accent: 'sapphire' },
    { name: 'Pine Grove', appearance: 'forest', accent: 'pine' },
    { name: 'Royal Violet', appearance: 'lavender', accent: 'grape' },
    { name: 'White & Dark', appearance: 'light', accent: 'mono' },
    // Dark
    { name: 'Nordic Night', appearance: 'nord', accent: 'sky' },
    { name: 'Midnight Gold', appearance: 'midnight', accent: 'gold' },
    { name: 'Obsidian Mint', appearance: 'abyss', accent: 'mint' },
    { name: 'Amethyst Dreams', appearance: 'amethyst', accent: 'orchid' },
    { name: 'Deep Ocean', appearance: 'oceanic', accent: 'teal' },
    { name: 'Emerald Night', appearance: 'emerald', accent: 'nature' },
    { name: 'Twilight', appearance: 'dusk', accent: 'lavender' },
    { name: 'Slate', appearance: 'graphite', accent: 'slate' },
    { name: 'Crimson', appearance: 'crimson', accent: 'reds' },
    { name: 'Garnet Night', appearance: 'night', accent: 'garnet' },
    { name: 'Sapphire Night', appearance: 'midnight', accent: 'sapphire' },
    { name: 'Royal Grape', appearance: 'amethyst', accent: 'grape' },
    { name: 'Deep Pine', appearance: 'emerald', accent: 'pine' },
    { name: 'Espresso', appearance: 'mocha', accent: 'gold' },
    { name: 'Wine Cellar', appearance: 'crimson', accent: 'plum' },
    { name: 'Dark & White', appearance: 'night', accent: 'mono' },
];
