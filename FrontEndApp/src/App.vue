<script setup lang="ts">
import {
    NConfigProvider,
    NDialogProvider,
    NNotificationProvider,
    NMessageProvider,
    darkTheme,
    NLayout,
    NLayoutSider,
    NMenu,
    NBadge,
    MenuOption,
} from 'naive-ui';
import ReadBible from './Views/ReadBible/ReadBible.vue';
import { useMenuStore } from './store/menu';
import { usePrayerStreakStore } from './store/prayerStreakStore';
import { useDevotionStreakStore } from './store/devotionStreakStore';
import { useNavBadgesStore } from './store/navBadgesStore';
import { onBeforeMount, onMounted, ref, watch, h } from 'vue';
import { useThemeStore } from './store/theme';
import TitleBar from './components/TitleBar/TitleBar.vue';
import Sermons from './Views/Sermons/Sermons.vue';
import SESSION from './util/session';
import FooterComponent from './components/Footer/Footer.vue';
import { useMainStore } from './store/main';
import { useI18n } from 'vue-i18n';
import AboutModal from './components/About/AboutModal.vue';
import SettingsModal from './components/Settings/SettingsModal.vue';
import SyncAnnouncementModal from './components/SyncAnnouncementModal.vue';
import PlanModal from './components/PlanModal.vue';
import FeedbackModal from './components/FeedbackModal.vue';
import { useAuthStore } from './store/authStore';
import FlipBook from './Views/ReadBible/FlipBook/FlipBook.vue';
import VersionSelectModal from './Views/ReadBible/FlipBook/VersionSelectModal.vue';
import { useRoute, useRouter } from 'vue-router';
import { computed } from 'vue';

const route = useRoute();
const router = useRouter();
const isPopupWindow = computed(() => route.name === 'CompareVerse' || (!window.isElectron && (route.name === 'Login' || route.name === 'SubscriptionRequired')));

const isMounted = ref(false);
const authStore = useAuthStore();

// On web: redirect to /login when the token is invalidated (e.g. 401 response)
watch(() => authStore.isAuthenticated, (authenticated) => {
    if (!authenticated && !window.isElectron) {
        router.push('/login');
    }
});
const isMenuCollapse = 'is-menu-collapse';
const menuStore = useMenuStore();
const themeStore = useThemeStore();
const prayerStreak = usePrayerStreakStore();
const devotionStreak = useDevotionStreakStore();
const navBadges = useNavBadgesStore();
const isSideBarCollapse = ref(true);
const savedLocaleKey = 'saveLanguageStorageKey';
const { locale, t } = useI18n();
useMainStore();

// Which sidebar entries should show a daily "attention" red dot.
function dotForKey(key: string): boolean {
    if (key === '/prayer-list') return !prayerStreak.prayedToday;
    if (key === '/daily-devotional') return !devotionStreak.completedToday;
    if (key === '/games') return navBadges.showGamesDot;
    return false;
}

// Upper sidebar menu options, with the icon wrapped in an NBadge dot when the
// matching daily activity is pending. Mirrors the inline map previously in the
// template; moved here so the badge render lives in TS.
const upperMenuOptions = computed<MenuOption[]>(() =>
    menuStore.menuUpperTabs
        .filter((item) => menuStore.enableTab.includes(item.key))
        .map((item) => {
            const iconRender = themeStore.isDark ? item.iconDark : item.icon;
            return {
                label: t(item.label),
                key: item.key,
                icon: () =>
                    h(
                        NBadge,
                        { dot: true, show: dotForKey(item.key) },
                        { default: iconRender }
                    ),
            };
        })
);

function triggerSideBarCollapse(collapse: boolean) {
    isSideBarCollapse.value = collapse;
    SESSION.set(isMenuCollapse, collapse);
}

onBeforeMount(async () => {
    const savedLocale = SESSION.get(savedLocaleKey);
    if (savedLocale) locale.value = savedLocale;

    const isCollapseSideMenu = SESSION.get(isMenuCollapse);
    isSideBarCollapse.value =
        isCollapseSideMenu || typeof isCollapseSideMenu == 'boolean' ? isCollapseSideMenu : true;
});

onMounted(async () => {
    // Initialize auth (token + user + sync state) on every app launch
    authStore.initAuth();

    // Drop AI insight/sermon cache entries older than 3 days (best-effort).
    void window.browserWindow?.pruneAiInsights?.();

    // Load streak days so the Prayer/Devotion nav dots are accurate from launch.
    void prayerStreak.loadDays();
    void devotionStreak.loadDays();

    isMounted.value = true;
});
</script>
<template>
    <NConfigProvider
        :theme-overrides="themeStore.themeOverrides"
        :theme="themeStore.isDark ? darkTheme : null"
    >
        <NDialogProvider>
            <NNotificationProvider>
                <NMessageProvider>
                    <!-- Popup windows (e.g. Compare Verse) — no sidebar/titlebar/footer -->
                    <RouterView v-if="isPopupWindow" />

                    <NLayout v-else class="h-[100vh] opacity-0 transition-all transform scale-50" :class="{'!opacity-100 !scale-100': isMounted}">
                        <TitleBar class="h-[var(--header-height)]" />
                        <NLayout class="h-[calc(100%-(var(--header-height)+var(--footer-height)))]" has-sider>
                            <NLayoutSider
                                bordered
                                :collapsed="isSideBarCollapse"
                                show-trigger="bar"
                                collapse-mode="width"
                                :collapsed-width="50"
                                :width="180"
                                :native-scrollbar="false"
                                :inverted="false"
                                :default-collapsed="true"
                                class="side-bar-menu h-full"
                                :on-update:collapsed="triggerSideBarCollapse"
                            >
                                <div class="flex flex-col justify-between h-full">
                                    <NMenu
                                        :value="menuStore.menuSelected"
                                        :on-update:value="(key: string, item: MenuOption) => {
                                        menuStore.setMenu(key);
                                    }"
                                        :inverted="false"
                                        :collapsed-icon-size="20"
                                        :indent="15"
                                        :options="upperMenuOptions"
                                    />
                                    <NMenu
                                        :value="menuStore.menuSelected"
                                        :on-update:value="
                                        (key: string, item: MenuOption) => {
                                            menuStore.setMenu(key);
                                        }"
                                        :inverted="false"
                                        :collapsed-icon-size="20"
                                        :indent="15"
                                        :options="
                                            menuStore.bottomMenuTabs.map((item) => ({
                                                label: $t(item.label),
                                                key: item.key,
                                                icon: item.icon,
                                            }))
                                        "
                                    />
                                </div>
                            </NLayoutSider>
                            <NLayout class="h-full">
                                <ReadBible
                                    v-show="
                                        menuStore.isRouter == false &&
                                        menuStore.menuSelected == 'read-bible'
                                    "
                                />
                                <Sermons
                                    v-show="
                                        menuStore.isRouter == false &&
                                        menuStore.menuSelected == 'sermons'
                                    "
                                />
                                <div class="h-[100%]" v-show="menuStore.isRouter == true">
                                    <RouterView />
                                </div>
                            </NLayout>
                        </NLayout>
                        <FooterComponent class="h-[var(--footer-height)]" size="tiny" />
                    </NLayout>
                    <AboutModal />
                    <SettingsModal />
                    <VersionSelectModal />
                    <FlipBook />
                    <SyncAnnouncementModal />
                    <PlanModal />
                    <FeedbackModal />
                </NMessageProvider>
            </NNotificationProvider>
        </NDialogProvider>
    </NConfigProvider>
</template>
<style lang="scss">
.side-bar-menu {
    .n-scrollbar-content {
        height: 100%;
    }
    .n-menu-item {
        height: 40px;
        transition: height 0.3s;
    }
    .n-menu--collapsed {
        .n-menu-item {
            height: 30px;
        }
    }
    .n-layout-toggle-bar {
        // background-color: var(--theme-bg-main, transparent) !important;
        // border-color: var(--theme-border, transparent) !important;
        
        // &:hover {
        //     background-color: var(--theme-bg-soft, transparent) !important;
        // }
        
        .n-layout-toggle-bar__top,
        .n-layout-toggle-bar__bottom {
            background-color: var(--theme-text, currentColor) !important;
        }
    }
}
</style>
