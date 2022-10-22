const themesOptions = {
    default: {
        dark: {
            primaryColor: "#F2C423",
            primaryColorHover: "#D5B33A",
            primaryColorSuppl: "#E4BB2F",
            primaryColorPressed: "#E5BD1D",
        },
        light: {
            primaryColor: "#F2AD23",
            primaryColorHover: "#E4A72F",
            primaryColorSuppl: "#D5A23A",
            primaryColorPressed: "#E5BD1D",
        },
    },
};

export type typeNameInterface = "default";

export function getTheme(name: typeNameInterface) {
    return themesOptions[name];
}
