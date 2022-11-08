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
import { onBeforeMount } from 'vue';
import { useThemeStore } from './store/theme';
import { menuOptions } from './AppMenuOptions';
import TitleBar from './components/TitleBar/TitleBar.vue';
import Sermons from './Views/Sermons/Sermons.vue';

const menuStore = useMenuStore();
const themeStore = useThemeStore();
async function getVersions() {
    const versions = await window.browserWindow.versions();
    console.log(
        `This app is using Chrome (v${versions.chrome}), Node.js (v${versions.node}), and Electron (v${versions.electron})`
    );
}

onBeforeMount(() => {
    getVersions();
});
</script>
<template>
    <NConfigProvider :theme-overrides="themeStore.themeOverrides" :theme="themeStore.isDark ? darkTheme : null">
        <NDialogProvider>
            <NNotificationProvider>
                <NMessageProvider>
                    <NLayout class="h-[100vh]">
                        <TitleBar class="h-25px" />
                        <NLayout class="h-[calc(100%-25px)]" has-sider>
                            <NLayoutSider
                                bordered
                                show-trigger="bar"
                                collapse-mode="width"
                                :collapsed-width="50"
                                :width="180"
                                :native-scrollbar="false"
                                :inverted="false"
                                :default-collapsed="true"
                                class="side-bar-menu"
                            >
                                <NMenu
                                    :value="menuStore.menuSelected"
                                    :on-update:value="(key: string, item: MenuOption) => {
                                        menuStore.setMenu(key);
                                    }"
                                    :inverted="false"
                                    :collapsed-width="48"
                                    :collapsed-icon-size="25"
                                    :indent="15"
                                    :options="menuOptions"
                                />
                            </NLayoutSider>
                            <NLayout>
                                <ReadBible v-show="menuStore.isRouter == false && menuStore.menuSelected == 'read-bible'" />
                                <Sermons v-show="menuStore.isRouter == false && menuStore.menuSelected == 'sermons'" />
                                <div v-show="menuStore.isRouter == true">
                                    <RouterView />
                                </div>
                            </NLayout>
                        </NLayout>
                    </NLayout>
                </NMessageProvider>
            </NNotificationProvider>
        </NDialogProvider>
    </NConfigProvider>
</template>
<style lang="scss">
.side-bar-menu {
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
