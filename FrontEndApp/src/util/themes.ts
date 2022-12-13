type colorTypes = {
    primaryColor: string;
    primaryColorHover: string;
    primaryColorSuppl: string;
    primaryColorPressed: string;
};

type themeOptionsType = {
    default: {
        dark: colorTypes;
        light: colorTypes;
    };
    Nature: {
        dark: colorTypes;
        light: colorTypes;
    };
};

export const themesOptions: themeOptionsType = {
    default: {
        dark: {
            primaryColor: '#F2C423',
            primaryColorHover: 'rgba(238, 167, 24, 0.212)',
            primaryColorSuppl: '#E4BB2F',
            primaryColorPressed: '#E5BD1D',
        } as colorTypes,
        light: {
            primaryColor: '#F2AD23',
            primaryColorHover: '#E4A72F',
            primaryColorSuppl: '#D5A23A',
            primaryColorPressed: '#E5BD1D',
        } as colorTypes,
    },

    Nature: {
        dark: {
            primaryColor: '#A4BE7B',
            primaryColorHover: '#5F8D4E',
            primaryColorSuppl: '#A4BE7B',
            primaryColorPressed: '#E5D9B6',
        } as colorTypes,
        light: {
            primaryColor: '#A4BE7B',
            primaryColorHover: '#5F8D4E',
            primaryColorSuppl: '#A4BE7B',
            primaryColorPressed: '#E5D9B6',
        } as colorTypes,
    },
};

export type typeNameInterface = 'default' | 'Nature';

export function getTheme(name: typeNameInterface) {
    return themesOptions[name];
}
