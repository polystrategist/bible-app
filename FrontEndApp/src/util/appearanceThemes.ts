export type backgroundThemeType =
    | 'default'
    | 'sepia'
    | 'forest'
    | 'dawn'
    | 'dusk'
    | 'nord'
    | 'midnight'
    | 'rosepaper'
    | 'oceanic'
    | 'graphite'
    | 'sandstone'
    | 'parchment'
    | 'cream'
    | 'arctic'
    | 'lavender'
    | 'moss'
    | 'abyss'
    | 'mocha'
    | 'emerald'
    | 'crimson'
    | 'amethyst';

export type appearanceThemeOption = {
    key: string;
    label: string;
    isDark: boolean;
    backgroundTheme: backgroundThemeType;
    swatch: string;
};

export const appearanceThemeOptions: appearanceThemeOption[] = [
    {
        key: 'light',
        label: 'light',
        isDark: false,
        backgroundTheme: 'default',
        swatch: '#e8e8e8',
    },
    {
        key: 'night',
        label: 'night',
        isDark: true,
        backgroundTheme: 'default',
        swatch: '#5f5f67',
    },
    {
        key: 'sepia',
        label: 'sepia',
        isDark: false,
        backgroundTheme: 'sepia',
        swatch: '#8b6b3f',
    },
    {
        key: 'forest',
        label: 'forest',
        isDark: false,
        backgroundTheme: 'forest',
        swatch: '#4f7a4a',
    },
    {
        key: 'dawn',
        label: 'dawn',
        isDark: false,
        backgroundTheme: 'dawn',
        swatch: '#e7a86e',
    },
    {
        key: 'dusk',
        label: 'dusk',
        isDark: true,
        backgroundTheme: 'dusk',
        swatch: '#6e6ea3',
    },
    {
        key: 'nord',
        label: 'nord',
        isDark: true,
        backgroundTheme: 'nord',
        swatch: '#88a7c8',
    },
    {
        key: 'midnight',
        label: 'midnight',
        isDark: true,
        backgroundTheme: 'midnight',
        swatch: '#3f5aa7',
    },
    {
        key: 'rosepaper',
        label: 'rosepaper',
        isDark: false,
        backgroundTheme: 'rosepaper',
        swatch: '#ce7e86',
    },
    {
        key: 'oceanic',
        label: 'oceanic',
        isDark: true,
        backgroundTheme: 'oceanic',
        swatch: '#3f8fa8',
    },
    {
        key: 'graphite',
        label: 'graphite',
        isDark: true,
        backgroundTheme: 'graphite',
        swatch: '#9095a1',
    },
    {
        key: 'sandstone',
        label: 'sandstone',
        isDark: false,
        backgroundTheme: 'sandstone',
        swatch: '#b68f5d',
    },
    {
        key: 'parchment',
        label: 'parchment',
        isDark: false,
        backgroundTheme: 'parchment',
        swatch: '#c4a96a',
    },
    {
        key: 'cream',
        label: 'cream',
        isDark: false,
        backgroundTheme: 'cream',
        swatch: '#d4cfc0',
    },
    {
        key: 'arctic',
        label: 'arctic',
        isDark: false,
        backgroundTheme: 'arctic',
        swatch: '#7aaec8',
    },
    {
        key: 'lavender',
        label: 'lavender',
        isDark: false,
        backgroundTheme: 'lavender',
        swatch: '#9b80d0',
    },
    {
        key: 'moss',
        label: 'moss',
        isDark: false,
        backgroundTheme: 'moss',
        swatch: '#6a9860',
    },
    {
        key: 'abyss',
        label: 'abyss',
        isDark: true,
        backgroundTheme: 'abyss',
        swatch: '#3d5a80',
    },
    {
        key: 'mocha',
        label: 'mocha',
        isDark: true,
        backgroundTheme: 'mocha',
        swatch: '#8c6040',
    },
    {
        key: 'emerald',
        label: 'emerald',
        isDark: true,
        backgroundTheme: 'emerald',
        swatch: '#2a7a50',
    },
    {
        key: 'crimson',
        label: 'crimson',
        isDark: true,
        backgroundTheme: 'crimson',
        swatch: '#8c2535',
    },
    {
        key: 'amethyst',
        label: 'amethyst',
        isDark: true,
        backgroundTheme: 'amethyst',
        swatch: '#6030a0',
    },
];
