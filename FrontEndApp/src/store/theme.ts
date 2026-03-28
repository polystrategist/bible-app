import { defineStore } from 'pinia';
import { onBeforeMount, ref, watch } from 'vue';
import SESSION from '../util/session';
import { getTheme, themesOptions, typeNameInterface } from '../util/themes';
import { appearanceThemeOptions, backgroundThemeType } from '../util/appearanceThemes';
import { useAuthStore } from './authStore';

export const useThemeStore = defineStore('useThemeStore', () => {
    const showThemeChangerDrawer = ref(false);
    const saveThemeStorageKey = 'savedThemeStorage';
    const isDark = ref(true);
    const backgroundTheme = ref<backgroundThemeType>('default');
    const selectedTheme = ref<typeNameInterface>('default');
    const themeOverrides = ref<any>({
        common: {
            primaryColor: '#f2c423',
            primaryColorHover: 'rgba(238, 167, 24, 0.212)',
            primaryColorSuppl: '#E4BB2F',
            primaryColorPressed: '#E5BD1D',
        },
        Input: {
            color: 'var(--theme-bg-elevated)',
            textColor: 'var(--theme-text)',
            placeholderColor: 'var(--theme-text-soft)',
            colorFocus: 'var(--theme-bg-soft)',
            colorDisabled: 'var(--theme-bg-soft)',
            textColorDisabled: 'var(--theme-text-soft)',
            border: '1px solid var(--theme-border)',
            borderFocus: '1px solid var(--primary-color)',
            borderHover: '1px solid var(--theme-border)',
            boxShadowFocus: '0 0 8px 0 rgba(124, 131, 253, 0.3)',
        },
    });

    function applyBodyThemeClass() {
        document.body.classList.remove('dark', 'light');
        document.body.classList.add(isDark.value ? 'dark' : 'light');

        appearanceThemeOptions.forEach((theme) => {
            document.body.classList.remove(`theme-bg-${theme.backgroundTheme}`);
        });
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

        // Persist to backend if authenticated (best-effort)
        const authStore = useAuthStore();
        if (authStore.isAuthenticated) {
            authStore.updateSettings({
                selected_theme: selectedTheme.value,
                is_dark: itsDark,
                background_theme: backgroundTheme.value,
            });
        }
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

        // When remote settings load (after login/initAuth), apply them
        const authStore = useAuthStore();
        watch(() => authStore.remoteSettings, (settings) => {
            if (!settings) return;
            selectedTheme.value = settings.selected_theme as typeNameInterface;
            isDark.value = settings.is_dark;
            backgroundTheme.value = settings.background_theme as backgroundThemeType;
            themeOverrides.value.common = (themesOptions as any)[selectedTheme.value][isDark.value ? 'dark' : 'light'];
            applyBodyThemeClass();
            changeTheRootProperty();
            // Keep localStorage in sync
            SESSION.set(saveThemeStorageKey, {
                selectedTheme: selectedTheme.value,
                isDark: isDark.value,
                backgroundTheme: backgroundTheme.value,
            });
        });
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

    function applyAppearanceTheme(theme: { isDark: boolean; backgroundTheme: backgroundThemeType }) {
        isDark.value = theme.isDark;
        backgroundTheme.value = theme.backgroundTheme;
        saveThemeSelected(theme.isDark);
        changeTheRootProperty();
    }

    return {
        selectedTheme,
        themeOverrides,
        isDark,
        backgroundTheme,
        setBackgroundTheme,
        applyAppearanceTheme,
        appearanceThemeOptions,
        changePrimaryColor,
        showThemeChangerDrawer
    };
});
