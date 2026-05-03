import { defineStore } from 'pinia';
import { onBeforeMount, ref, watch } from 'vue';
import SESSION from '../util/session';
import { getTheme, themesOptions, typeNameInterface } from '../util/themes';
import { appearanceThemeOptions, backgroundThemeType } from '../util/appearanceThemes';
import { useAuthStore } from './authStore';

export const useThemeStore = defineStore('useThemeStore', () => {
    const showThemeChangerDrawer = ref(false);
    const saveThemeStorageKey = 'savedThemeStorage';
    let settingsDebounceTimer: ReturnType<typeof setTimeout> | null = null;
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
        // Select trigger (the closed button)
        InternalSelection: {
            color: 'var(--theme-bg-elevated)',
            colorActive: 'var(--theme-bg-elevated)',
            colorFocus: 'var(--theme-bg-soft)',
            colorDisabled: 'var(--theme-bg-soft)',
            textColor: 'var(--theme-text)',
            placeholderColor: 'var(--theme-text-soft)',
            border: '1px solid var(--theme-border)',
            borderHover: '1px solid var(--theme-border)',
            borderFocus: '1px solid var(--primary-color)',
            borderActive: '1px solid var(--primary-color)',
            caretColor: 'var(--primary-color)',
        },
        // Select dropdown popup
        InternalSelectMenu: {
            color: 'var(--theme-bg-elevated)',
            optionTextColor: 'var(--theme-text)',
            optionTextColorActive: 'var(--primary-color)',
            optionTextColorPressed: 'var(--primary-color)',
            optionColorPending: 'var(--theme-bg-soft)',
            optionColorActive: 'var(--theme-bg-soft)',
            groupHeaderTextColor: 'var(--theme-text-soft)',
        },
    });

    function resolveSelectedTheme(value: unknown): typeNameInterface {
        return typeof value === 'string' && value in themesOptions
            ? value as typeNameInterface
            : 'default';
    }

    function resolveBackgroundTheme(value: unknown): backgroundThemeType {
        return typeof value === 'string' && appearanceThemeOptions.some((theme) => theme.backgroundTheme === value)
            ? value as backgroundThemeType
            : 'default';
    }

    function resolveIsDark(value: unknown): boolean {
        return typeof value === 'boolean' ? value : true;
    }

    function applyPrimaryTheme() {
        const theme = getTheme(selectedTheme.value) ?? getTheme('default');
        themeOverrides.value.common = theme[isDark.value ? 'dark' : 'light'];
    }

    function applyBodyThemeClass() {
        document.body.classList.remove('dark', 'light');
        document.body.classList.add(isDark.value ? 'dark' : 'light');

        appearanceThemeOptions.forEach((theme) => {
            document.body.classList.remove(`theme-bg-${theme.backgroundTheme}`);
        });
        document.body.classList.add(`theme-bg-${backgroundTheme.value}`);
    }

    function saveThemeSelected(itsDark = isDark.value) {
        isDark.value = resolveIsDark(itsDark);
        selectedTheme.value = resolveSelectedTheme(selectedTheme.value);
        backgroundTheme.value = resolveBackgroundTheme(backgroundTheme.value);
        applyPrimaryTheme();

        applyBodyThemeClass();
        SESSION.set(saveThemeStorageKey, {
            selectedTheme: selectedTheme.value,
            isDark: itsDark,
            backgroundTheme: backgroundTheme.value,
        });

        // Persist to backend if authenticated — debounced to avoid a request
        // on every tap when the user is browsing through theme options.
        const authStore = useAuthStore();
        if (authStore.isAuthenticated) {
            if (settingsDebounceTimer) clearTimeout(settingsDebounceTimer);
            settingsDebounceTimer = setTimeout(() => {
                settingsDebounceTimer = null;
                authStore.updateSettings({
                    selected_theme: selectedTheme.value,
                    is_dark: itsDark,
                    background_theme: backgroundTheme.value,
                });
            }, 3000);
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
            selectedTheme.value = resolveSelectedTheme(savedTheme.selectedTheme);
            isDark.value = resolveIsDark(savedTheme.isDark);
            backgroundTheme.value = resolveBackgroundTheme(savedTheme.backgroundTheme);
            applyPrimaryTheme();
        }

        applyBodyThemeClass();
        changeTheRootProperty();

        // When remote settings load (after login/initAuth), apply them.
        // Skip if there are pending local changes — local always wins until flushed.
        const authStore = useAuthStore();
        watch(() => authStore.remoteSettings, (settings) => {
            if (!settings) return;
            if (authStore.pendingSettingsUpdate) return;
            selectedTheme.value = resolveSelectedTheme(settings.selected_theme);
            isDark.value = resolveIsDark(settings.is_dark);
            backgroundTheme.value = resolveBackgroundTheme(settings.background_theme);
            applyPrimaryTheme();
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
        selectedTheme.value = resolveSelectedTheme(key);
        applyPrimaryTheme();
        saveThemeSelected();
        changeTheRootProperty();
    }

    function setBackgroundTheme(theme: backgroundThemeType) {
        backgroundTheme.value = resolveBackgroundTheme(theme);
    }

    function applyAppearanceTheme(theme: { isDark: boolean; backgroundTheme: backgroundThemeType }) {
        isDark.value = resolveIsDark(theme.isDark);
        backgroundTheme.value = resolveBackgroundTheme(theme.backgroundTheme);
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
