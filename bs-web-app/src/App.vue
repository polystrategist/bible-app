<script setup lang="ts">
import { cn } from '@/lib/utils';
import { ResizableHandle, ResizablePanel, ResizablePanelGroup } from '@/components/ui/resizable';
import { ref } from 'vue';
import { RouterView } from 'vue-router';

const isCollapsed = ref(false);

function onCollapse() {
    isCollapsed.value = true;
}

function onExpand() {
    isCollapsed.value = false;
}
</script>

<template>
    <div class="h-[100vh] w-[100vw]">
        <ResizablePanelGroup direction="horizontal">
            <ResizablePanel
                collapsible
                :min-size="15"
                :max-size="20"
                :class="cn(isCollapsed && 'min-w-[50px] transition-all duration-300 ease-in-out')"
                @expand="onExpand"
                @collapse="onCollapse"
            >
                One
            </ResizablePanel>
            <ResizableHandle with-handle />
            <ResizablePanel>
                <RouterView />
            </ResizablePanel>
        </ResizablePanelGroup>
    </div>
</template>
