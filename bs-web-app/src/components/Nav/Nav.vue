<script lang="ts" setup>
import { Icon } from "@iconify/vue";
import { cn } from "@/lib/utils";
import { buttonVariants } from "@/components/ui/button";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

export interface LinkProp {
    title: string;
    label?: string;
    icon: string;
    variant: "default" | "ghost";
    path?: string;
    key: string;
}

interface NavProps {
    isCollapsed: boolean;
    links: LinkProp[];
}

defineProps<NavProps>();
const emit = defineEmits(["toggle"]);

function menuClicked(link: LinkProp) {
    emit("toggle", link.key);
    if (link.path) router.push(link.path);
}
</script>

<template>
    <div
        :data-collapsed="isCollapsed"
        class="group flex flex-col gap-4 py-2 data-[collapsed=true]:py-2"
    >
        <nav
            class="grid gap-1 px-2 group-[[data-collapsed=true]]:justify-center group-[[data-collapsed=true]]:px-2"
        >
            <template v-for="(link, index) of links">
                <Tooltip v-if="isCollapsed" :key="`1-${index}`" :delay-duration="0">
                    <TooltipTrigger as-child>
                        <div
                            @click="menuClicked(link)"
                            class="cursor-pointer"
                            :class="
                                cn(
                                    buttonVariants({
                                        variant: route.path === link.path ? 'default' : 'ghost',
                                        size: 'icon',
                                    }),
                                    'h-9 w-9'
                                )
                            "
                        >
                            <Icon :icon="link.icon" class="size-4" />
                            <span class="sr-only">{{ link.title }}</span>
                        </div>
                    </TooltipTrigger>
                    <TooltipContent side="right" class="flex items-center gap-4">
                        {{ link.title }}
                        <span v-if="link.label" class="ml-auto text-muted-foreground">
                            {{ link.label }}
                        </span>
                    </TooltipContent>
                </Tooltip>

                <div
                    v-else
                    :key="`2-${index}`"
                    @click="menuClicked(link)"
                    class="cursor-pointer h-[28px]"
                    :class="
                        cn(
                            buttonVariants({
                                variant: route.path === link.path ? 'default' : 'ghost',
                                size: 'sm',
                            }),
                            'justify-start'
                        )
                    "
                >
                    <Icon :icon="link.icon" class="mr-2 size-4" />
                    {{ link.title }}
                    <span
                        v-if="link.label"
                        :class="
                            cn(
                                'ml-auto',
                                link.variant === 'default' && 'text-background dark:text-white'
                            )
                        "
                    >
                        {{ link.label }}
                    </span>
                </div>
            </template>
        </nav>
    </div>
</template>
