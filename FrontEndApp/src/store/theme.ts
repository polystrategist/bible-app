import { defineStore } from "pinia";
import { onBeforeMount, ref, watch } from "vue";
import SESSION from "../util/session";
import { getTheme, typeNameInterface } from "../util/themes";

export const useThemeStore = defineStore("useThemeStore", () => {
    const saveThemeStorageKey = "savedThemeStorage";
    const isDark = ref(true);
    const selectedTheme = ref<typeNameInterface>("default");
    const themeOverrides = ref<any>({
        common: {
            primaryColor: "#F2C423",
            primaryColorHover: "#D5B33A",
            primaryColorSuppl: "#E4BB2F",
            primaryColorPressed: "#E5BD1D",
        },
    });

    watch(
        () => isDark.value,
        (itsDark) => {
            if (themeOverrides.value.common)
                themeOverrides.value.common = itsDark ? getTheme(selectedTheme.value).dark : getTheme(selectedTheme.value).light;

            document.body.className = itsDark ? "dark" : "light";

            SESSION.set(saveThemeStorageKey, {
                selectedTheme: selectedTheme.value,
                isDark: itsDark,
            });
        }
    );

    onBeforeMount(() => {
        const savedTheme = SESSION.get(saveThemeStorageKey);
        if (savedTheme) {
            selectedTheme.value = savedTheme.selectedTheme;
            isDark.value = savedTheme.isDark;
            document.body.classList.add(isDark.value ? "dark" : "light");
        }
    });

    return {
        themeOverrides,
        isDark,
    };
});
