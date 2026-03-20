import { defineStore } from 'pinia';
import { onBeforeMount, ref, watch } from 'vue';
import SESSION from '../util/session';
import { getTheme, themesOptions, typeNameInterface } from '../util/themes';

type backgroundThemeType = 'default' | 'sepia';

export const useThemeStore = defineStore('useThemeStore', () => {
    const showThemeChangerDrawer = ref(false);
    const saveThemeStorageKey = 'savedThemeStorage';
    const isDark = ref(true);
    const backgroundTheme = ref<backgroundThemeType>('default');
    const selectedTheme = ref<typeNameInterface>('default');
    const themeOverrides = ref<{
        common: {
            primaryColor: string;
            primaryColorHover: string;
            primaryColorSuppl: string;
            primaryColorPressed: string;
        };
    }>({
        common: {
            primaryColor: '#f2c423',
            primaryColorHover: 'rgba(238, 167, 24, 0.212)',
            primaryColorSuppl: '#E4BB2F',
            primaryColorPressed: '#E5BD1D',
        },
    });

    function applyBodyThemeClass() {
        document.body.classList.remove('dark', 'light');
        document.body.classList.add(isDark.value ? 'dark' : 'light');

        document.body.classList.remove('theme-bg-default', 'theme-bg-sepia');
        document.body.classList.add(`theme-bg-${backgroundTheme.value}`);
    }

    function saveThemeSelected(itsDark = isDark.value) {
        if (themeOverrides.value.common)
            themeOverrides.value.common = itsDark ? getTheme(selectedTheme.value).dark : getTheme(selectedTheme.value).light;

        applyBodyThemeClass();
        SESSION.set(saveThemeStorageKey, {
            selectedTheme: selectedTheme.value,
            isDark: itsDark,
            backgroundTheme: backgroundTheme.value,
        });
    }

    watch(
        () => isDark.value,
        (itsDark) => {
            saveThemeSelected(itsDark);
            changeTheRootProperty();
        }
    );

    watch(
        () => backgroundTheme.value,
        () => {
            saveThemeSelected();
        }
    );

    onBeforeMount(() => {
        const savedTheme = SESSION.get(saveThemeStorageKey);
        if (savedTheme) {
            selectedTheme.value = savedTheme.selectedTheme;
            isDark.value = savedTheme.isDark;
            backgroundTheme.value = savedTheme.backgroundTheme || 'default';
            themeOverrides.value.common = (themesOptions as any)[selectedTheme.value][isDark.value ? 'dark' : 'light'];
        }

        applyBodyThemeClass();

        changeTheRootProperty();
    });

    function changeTheRootProperty() {
        document.documentElement.style.setProperty('--primary-color', themeOverrides.value.common.primaryColor);
        document.documentElement.style.setProperty('--primary-color-light', themeOverrides.value.common.primaryColorHover);
    }

    function changePrimaryColor(key: typeNameInterface) {
        selectedTheme.value = key;
        themeOverrides.value.common = (themesOptions as any)[key][isDark.value ? 'dark' : 'light'];
        saveThemeSelected();
        changeTheRootProperty();
    }

    function setBackgroundTheme(theme: backgroundThemeType) {
        backgroundTheme.value = theme;
    }

    return {
        selectedTheme,
        themeOverrides,
        isDark,
        backgroundTheme,
        setBackgroundTheme,
        changePrimaryColor,
        showThemeChangerDrawer
    };
});
