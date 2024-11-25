type colorTypes = {
    primaryColor: string;
    primaryColorHover: string;
    primaryColorSuppl: string;
    primaryColorPressed: string;
    [key: string]: string;
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
    ocean: {
        dark: colorTypes;
        light: colorTypes;
    };
    reds: {
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
            primaryColorSuppl: '#59C1BD',
            primaryColorPressed: '#CFF5E7',
        } as colorTypes,
        light: {
            primaryColor: '#59C1BD',
            primaryColorHover: '#CFF5E7',
            primaryColorSuppl: '#A0E4CB',
            primaryColorPressed: '#CFF5E7',
        } as colorTypes,
    },

    ocean: {
        dark: {
            primaryColor: '#279EFF',
            primaryColorHover: '#40F8FF',
            primaryColorSuppl: '#40F8FF',
            primaryColorPressed: '#D5FFD0',
        },
        light: {
            primaryColor: '#279EFF',
            primaryColorHover: '#40F8FF',
            primaryColorSuppl: '#40F8FF',
            primaryColorPressed: '#D5FFD0',
        },
    },

    reds: {
        dark: {
            primaryColor: '#fd7264f2',
            primaryColorHover: '#e25e3e8f',
            primaryColorSuppl: '#FF9B50',
            primaryColorPressed: '#FFBB5C',
        },
        light: {
            primaryColor: '#f35b4b',
            primaryColorHover: '#e25e3e8f',
            primaryColorSuppl: '#FF9B50',
            primaryColorPressed: '#FFBB5C',
        },
    },
};

export type typeNameInterface = 'default' | 'Nature' | 'Sky' | 'ocean' | 'reds';

export function getTheme(name: typeNameInterface) {
    return themesOptions[name];
}
