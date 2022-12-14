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
    Sky: {
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
            primaryColor: '#5F8D4E',
            primaryColorHover: '#A4BE7B',
            primaryColorSuppl: '#A4BE7B',
            primaryColorPressed: '#E5D9B6',
        } as colorTypes,
    },

    Sky: {
        dark: {
            primaryColor: '#59C1BD',
            primaryColorHover: '#A0E4CB',
            primaryColorSuppl: '#0D4C92',
            primaryColorPressed: '#CFF5E7',
        } as colorTypes,
        light: {
            primaryColor: '#59C1BD',
            primaryColorHover: '#CFF5E7',
            primaryColorSuppl: '#A0E4CB',
            primaryColorPressed: '#CFF5E7',
        } as colorTypes,
    },
};

export type typeNameInterface = 'default' | 'Nature' | 'Sky';

export function getTheme(name: typeNameInterface) {
    return themesOptions[name];
}
