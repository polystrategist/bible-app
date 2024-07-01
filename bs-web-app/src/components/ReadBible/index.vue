<script setup lang="ts">
import { Separator } from "@/components/ui/separator";
import { ResizableHandle, ResizablePanel, ResizablePanelGroup } from "@/components/ui/resizable";
import { ScrollArea } from "@/components/ui/scroll-area";
</script>
<template>
    <div class="w-full h-full">
        <div class="h-[50px] min-h-[50px] flex items-center px-3">
            <h1 class="text-xl font-bold">Bible</h1>
        </div>
        <Separator />
        <div class="h-[calc(100%-50px)]">
            <ResizablePanelGroup direction="horizontal">
                <ResizablePanel>
                    <ScrollArea class="overflow-y-auto h-full p-5">
                        <div v-for="index in 500" :key="index">
                            Lorem ipsum, dolor sit amet consectetur adipisicing elit. Veniam
                            dolores, velit, officiis cum mollitia fuga eos voluptas illum,
                            cupiditate incidunt aspernatur. Modi vel quis delectus, commodi nostrum
                            expedita voluptatibus perspiciatis!
                        </div>
                    </ScrollArea>
                </ResizablePanel>
                <ResizableHandle with-handle />
                <ResizablePanel :default-size="30" :max-size="50" :min-size="15">
                    <div class="overflow-y-auto h-full p-5">
                        Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quidem iste
                        excepturi, vitae dolorum accusantium beatae nulla eos magnam laudantium,
                        ipsam autem deserunt consequatur deleniti soluta blanditiis doloremque
                        maxime repellendus laborum!
                    </div>
                </ResizablePanel>
            </ResizablePanelGroup>
        </div>
    </div>
</template>
