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
    MenuOption,
} from 'naive-ui';
import ReadBible from './Views/ReadBible/ReadBible.vue';
import { useMenuStore } from './store/menu';
import { onBeforeMount, onMounted, ref } from 'vue';
import { useThemeStore } from './store/theme';
import TitleBar from './components/TitleBar/TitleBar.vue';
import Sermons from './Views/Sermons/Sermons.vue';
import SESSION from './util/session';
import FooterComponent from './components/Footer/Footer.vue';
import DownloadBible from './components/DownloadBible/DownloadBible.vue';
import { useMainStore } from './store/main';
import { useI18n } from 'vue-i18n';
import AboutModal from './components/About/AboutModal.vue';
import SettingsModal from './components/Settings/SettingsModal.vue';
import { isSignedIn } from './util/SupaBase/Auth/Auth';
import { useUserStore } from './store/userStore';
import SelectStudySpaceModal from './components/StudySpace/SelectStudySpaceModal.vue';

const userStore = useUserStore();
const isMenuCollapse = 'is-menu-collapse';
const menuStore = useMenuStore();
const themeStore = useThemeStore();
const isSideBarCollapse = ref(true);
const savedLocaleKey = 'saveLanguageStorageKey';
const { locale } = useI18n();
useMainStore();

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
    const userData = await isSignedIn();
    if (userData) userStore.user = userData;
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
                    <NLayout class="h-[100vh]">
                        <TitleBar class="h-30px" />
                        <NLayout class="h-[calc(100%-60px)]" has-sider>
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
                                        :options="
                                            menuStore.menuUpperTabs
                                                .filter((item) =>
                                                    menuStore.enableTab.includes(item.key)
                                                )
                                                .map((item) => ({
                                                    label: $t(item.label),
                                                    key: item.key,
                                                    icon: themeStore.isDark
                                                        ? item.iconDark
                                                        : item.icon,
                                                }))
                                        "
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
                        <FooterComponent class="h-30px" size="tiny" />
                    </NLayout>
                    <DownloadBible />
                    <AboutModal />
                    <SettingsModal />
                    <SelectStudySpaceModal />
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
}
</style>
