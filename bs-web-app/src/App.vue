<script setup lang="ts">
import { cn } from "@/lib/utils";
import { ResizableHandle, ResizablePanel, ResizablePanelGroup } from "@/components/ui/resizable";
import { onBeforeMount, ref } from "vue";
import { RouterView } from "vue-router";
import Nav, { type LinkProp } from "@/components/Nav/Nav.vue";
import TooltipProvider from "./components/ui/tooltip/TooltipProvider.vue";
import Separator from "./components/ui/separator/Separator.vue";
import SnapStorage from "snap-storage";
import { useColorMode } from "@vueuse/core";
import DialogComponent from "@/components/Dialog/index.vue";
import { Button } from "./components/ui/button";
import { Icon } from "@iconify/vue";

const DialogLogoutRef = ref();
const mode = useColorMode();
const isCollapsed = ref(false);
const menuBarMinSize = ref(15);
const menuBarMaxSize = ref(20);
const menuBarDefaultSize = ref(20);
const sideBarMaxSizeSnapKey = "sideBarMaxSize";

const links: LinkProp[] = [
    {
        title: "Bible",
        icon: "mdi:book-open-page-variant",
        variant: "default",
        path: "/",
        key: "read-bible",
    },
    {
        title: "Pray",
        icon: "mdi:hands-pray",
        variant: "ghost",
        path: "/prayer-list",
        key: "prayer-list",
    },
    {
        title: "Sermons",
        icon: "iconoir:media-video-folder",
        variant: "ghost",
        path: "/sermons",
        key: "sermons",
    },
];

const bottomLinks = ref<LinkProp[]>([
    {
        title: "Account",
        icon: "mdi:account",
        variant: "ghost",
        path: "/account",
        key: "account",
    },
    {
        title: "About",
        icon: "mdi:information-outline",
        variant: "ghost",
        path: "/about",
        key: "about",
    },
    {
        title: "Dark Mode",
        icon: "mdi:weather-night",
        variant: "ghost",
        key: "mode-toggle",
    },
    {
        title: "Logout",
        icon: "mdi:logout",
        variant: "ghost",
        key: "logout",
    },
]);

function onCollapse() {
    isCollapsed.value = true;
}

function onExpand() {
    isCollapsed.value = false;
}

function resize(number: any) {
    clearTimeout(window.sideBarTimeOut);

    window.sideBarTimeOut = setTimeout(() => {
        SnapStorage.set(sideBarMaxSizeSnapKey, number);
    }, 1000);
}

function onBottomMenuToggle(key: string) {
    if (key === "mode-toggle") {
        bottomLinks.value[2].title = mode.value === "dark" ? "Light Mode" : "Dark Mode";
        bottomLinks.value[2].icon =
            mode.value === "dark" ? "mdi:weather-sunny" : "mdi:weather-night";
        mode.value = mode.value === "dark" ? "light" : "dark";
    }

    if (key === "logout") {
        DialogLogoutRef.value.toggleModal();
    }
}

onBeforeMount(() => {
    window.addEventListener("resize", () => {
        if (window.innerWidth < 797) {
            if (!isCollapsed.value) {
                isCollapsed.value = true;
            }
        } else {
            isCollapsed.value = false;
        }
    });

    bottomLinks.value[2].title = mode.value === "dark" ? "Dark Mode" : "Light Mode";
    bottomLinks.value[2].icon = mode.value === "dark" ? "mdi:weather-night" : "mdi:weather-sunny";

    const sideBarMaxSize = SnapStorage.get(sideBarMaxSizeSnapKey);
    if (sideBarMaxSize) {
        menuBarDefaultSize.value = sideBarMaxSize;

        if (menuBarDefaultSize.value < menuBarMinSize.value) {
            isCollapsed.value = true;
            menuBarDefaultSize.value = 0;
        }
    }
});
</script>

<template>
    <DialogComponent
        ref="DialogLogoutRef"
        title="Logout"
        description="Are you sure you want to logout?"
    >
        <template #dialog-footer>
            <Button variant="destructive" type="submit"> Yes </Button>
            <Button variant="secondary" type="submit" @click="DialogLogoutRef.toggleModal()">
                No
            </Button>
        </template>
    </DialogComponent>
    <div class="h-[100lvh] w-[100%]">
        <TooltipProvider :delay-duration="0">
            <ResizablePanelGroup direction="horizontal">
                <ResizablePanel
                    collapsible
                    :default-size="menuBarDefaultSize"
                    :min-size="menuBarMinSize"
                    :max-size="menuBarMaxSize"
                    class="h-full flex flex-col"
                    :class="
                        cn(
                            isCollapsed &&
                                'min-w-[50px] !max-w-[50px] w-full transition-all duration-300 ease-in-out'
                        )
                    "
                    @expand="onExpand"
                    @collapse="onCollapse"
                    @resize="resize"
                >
                    <div
                        class="h-[50px] min-h-[50px] flex items-center justify-start px-4 gap-2"
                        :class="cn(isCollapsed && 'px-[5px] !justify-center')"
                    >
                        <Icon
                            icon="pepicons-pop:sword-shield-circle-filled"
                            class="size-5"
                            :class="cn(isCollapsed && '!size-8')"
                        />
                        <span class="font-bold" :class="cn(isCollapsed && 'hidden')">Believers Sword</span>
                    </div>
                    <Separator />
                    <div class="h-full overflow-y-auto">
                        <div>
                            <Nav :is-collapsed="isCollapsed" :links="links" />
                        </div>
                    </div>
                    <div>
                        <Separator />
                        <div>
                            <Nav
                                @toggle="onBottomMenuToggle"
                                :is-collapsed="isCollapsed"
                                :links="bottomLinks"
                            />
                        </div>
                    </div>
                </ResizablePanel>
                <ResizableHandle with-handle />
                <ResizablePanel>
                    <RouterView />
                </ResizablePanel>
            </ResizablePanelGroup>
        </TooltipProvider>
    </div>
</template>
