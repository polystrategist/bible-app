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
    olive: {
        dark: colorTypes;
        light: colorTypes;
    };
    ember: {
        dark: colorTypes;
        light: colorTypes;
    };
    lavender: {
        dark: colorTypes;
        light: colorTypes;
    };
    mint: {
        dark: colorTypes;
        light: colorTypes;
    };
    rose: {
        dark: colorTypes;
        light: colorTypes;
    };
    slate: {
        dark: colorTypes;
        light: colorTypes;
    };
    amber: {
        dark: colorTypes;
        light: colorTypes;
    };
    indigo: {
        dark: colorTypes;
        light: colorTypes;
    };
    teal: {
        dark: colorTypes;
        light: colorTypes;
    };
    cobalt: {
        dark: colorTypes;
        light: colorTypes;
    };
    orchid: {
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

    olive: {
        dark: {
            primaryColor: '#98C379',
            primaryColorHover: '#6FA956',
            primaryColorSuppl: '#7CB369',
            primaryColorPressed: '#B7D89A',
        },
        light: {
            primaryColor: '#5E8C3B',
            primaryColorHover: '#7CB369',
            primaryColorSuppl: '#98C379',
            primaryColorPressed: '#B7D89A',
        },
    },

    ember: {
        dark: {
            primaryColor: '#E76F51',
            primaryColorHover: '#F4A261',
            primaryColorSuppl: '#E9C46A',
            primaryColorPressed: '#F4A261',
        },
        light: {
            primaryColor: '#D65A3A',
            primaryColorHover: '#E76F51',
            primaryColorSuppl: '#F4A261',
            primaryColorPressed: '#E9C46A',
        },
    },

    lavender: {
        dark: {
            primaryColor: '#B388FF',
            primaryColorHover: '#D1B3FF',
            primaryColorSuppl: '#9D7BFF',
            primaryColorPressed: '#E0CCFF',
        },
        light: {
            primaryColor: '#9B6DFF',
            primaryColorHover: '#B388FF',
            primaryColorSuppl: '#C4A2FF',
            primaryColorPressed: '#DCC8FF',
        },
    },

    mint: {
        dark: {
            primaryColor: '#4CD4A8',
            primaryColorHover: '#73E8C1',
            primaryColorSuppl: '#39C99D',
            primaryColorPressed: '#A3F2D8',
        },
        light: {
            primaryColor: '#2CBF90',
            primaryColorHover: '#4CD4A8',
            primaryColorSuppl: '#73E8C1',
            primaryColorPressed: '#9CEFD3',
        },
    },

    rose: {
        dark: {
            primaryColor: '#F06292',
            primaryColorHover: '#F48FB1',
            primaryColorSuppl: '#EC407A',
            primaryColorPressed: '#F8BBD0',
        },
        light: {
            primaryColor: '#E64980',
            primaryColorHover: '#F06292',
            primaryColorSuppl: '#F48FB1',
            primaryColorPressed: '#F8BBD0',
        },
    },

    slate: {
        dark: {
            primaryColor: '#8FA3BF',
            primaryColorHover: '#B0BDD1',
            primaryColorSuppl: '#7D93B2',
            primaryColorPressed: '#C7D1DF',
        },
        light: {
            primaryColor: '#6B819E',
            primaryColorHover: '#8FA3BF',
            primaryColorSuppl: '#A5B4C7',
            primaryColorPressed: '#C7D1DF',
        },
    },

    amber: {
        dark: {
            primaryColor: '#FFB020',
            primaryColorHover: '#FFC857',
            primaryColorSuppl: '#F59F00',
            primaryColorPressed: '#FFD98A',
        },
        light: {
            primaryColor: '#E09100',
            primaryColorHover: '#FFB020',
            primaryColorSuppl: '#FFC857',
            primaryColorPressed: '#FFD98A',
        },
    },

    indigo: {
        dark: {
            primaryColor: '#7C83FD',
            primaryColorHover: '#A0A6FF',
            primaryColorSuppl: '#6C73F3',
            primaryColorPressed: '#C5C9FF',
        },
        light: {
            primaryColor: '#5F67E8',
            primaryColorHover: '#7C83FD',
            primaryColorSuppl: '#A0A6FF',
            primaryColorPressed: '#C5C9FF',
        },
    },

    teal: {
        dark: {
            primaryColor: '#2EC4B6',
            primaryColorHover: '#5ED3C8',
            primaryColorSuppl: '#21B5A7',
            primaryColorPressed: '#9BE7DF',
        },
        light: {
            primaryColor: '#1FA89B',
            primaryColorHover: '#2EC4B6',
            primaryColorSuppl: '#5ED3C8',
            primaryColorPressed: '#9BE7DF',
        },
    },

    cobalt: {
        dark: {
            primaryColor: '#3A86FF',
            primaryColorHover: '#6AA4FF',
            primaryColorSuppl: '#2F74E6',
            primaryColorPressed: '#A9CAFF',
        },
        light: {
            primaryColor: '#2469D9',
            primaryColorHover: '#3A86FF',
            primaryColorSuppl: '#6AA4FF',
            primaryColorPressed: '#A9CAFF',
        },
    },

    orchid: {
        dark: {
            primaryColor: '#C77DFF',
            primaryColorHover: '#D8A4FF',
            primaryColorSuppl: '#B968F5',
            primaryColorPressed: '#E6C7FF',
        },
        light: {
            primaryColor: '#B35EEA',
            primaryColorHover: '#C77DFF',
            primaryColorSuppl: '#D8A4FF',
            primaryColorPressed: '#E6C7FF',
        },
    },
};

export type typeNameInterface =
    | 'default'
    | 'Nature'
    | 'Sky'
    | 'ocean'
    | 'reds'
    | 'olive'
    | 'ember'
    | 'lavender'
    | 'mint'
    | 'rose'
    | 'slate'
    | 'amber'
    | 'indigo'
    | 'teal'
    | 'cobalt'
    | 'orchid';

export function getTheme(name: typeNameInterface) {
    return themesOptions[name];
}
