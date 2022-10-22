<script setup lang="ts">
import { NConfigProvider, NDialogProvider, NNotificationProvider, NMessageProvider, darkTheme, NLayout } from "naive-ui";
import ReadBible from "./Views/ReadBible/ReadBible.vue";
import { useMenuStore } from "./store/menu";
import { onBeforeMount } from "vue";
import { useThemeStore } from "./store/theme";
import TitleBar from "./components/TitleBar/TitleBar.vue";
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
                        <div class="h-[calc(100%-25px)]">
                            <ReadBible v-show="menuStore.isRouter == false && menuStore.menuSelected == 'read-bible'" />
                            <div v-show="menuStore.isRouter == true">
                                <RouterView />
                            </div>
                        </div>
                    </NLayout>
                </NMessageProvider>
            </NNotificationProvider>
        </NDialogProvider>
    </NConfigProvider>
</template>
