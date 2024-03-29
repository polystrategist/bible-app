<script setup lang="ts">
import ListItem from './ListItem.vue';
import {
    NavigationMenu,
    NavigationMenuContent,
    NavigationMenuItem,
    NavigationMenuLink,
    NavigationMenuList,
    NavigationMenuTrigger,
    navigationMenuTriggerStyle,
} from './../../ui/navigation-menu';

const colorMode = useColorMode();

const components: { title: string; href: string; description: string }[] = [
    {
        title: 'Alert Dialog',
        href: '/docs/primitives/alert-dialog',
        description: 'A modal dialog that interrupts the user with important content and expects a response.',
    },
    {
        title: 'Hover Card',
        href: '/docs/primitives/hover-card',
        description: 'For sighted users to preview content available behind a link.',
    },
    {
        title: 'Progress',
        href: '/docs/primitives/progress',
        description: 'Displays an indicator showing the completion progress of a task, typically displayed as a progress bar.',
    },
    {
        title: 'Scroll-area',
        href: '/docs/primitives/scroll-area',
        description: 'Visually or semantically separates content.',
    },
    {
        title: 'Tabs',
        href: '/docs/primitives/tabs',
        description: 'A set of layered sections of content—known as tab panels—that are displayed one at a time.',
    },
    {
        title: 'Tooltip',
        href: '/docs/primitives/tooltip',
        description:
            'A popup that displays information related to an element when the element receives keyboard focus or the mouse hovers over it.',
    },
];
</script>

<template>
    <div class="hidden items-center justify-between px-10 h-[70px] md:flex">
        <div>
            <NuxtLink to="/">
                <Icon size="40" name="pepicons-pop:sword-shield-circle-filled" />
            </NuxtLink>
        </div>
        <NavigationMenu>
            <NavigationMenuList>
                <NavigationMenuItem>
                    <NuxtLink to="/" :class="navigationMenuTriggerStyle()"> Home </NuxtLink>
                </NavigationMenuItem>
                <NavigationMenuItem>
                    <NavigationMenuTrigger>Getting started</NavigationMenuTrigger>
                    <NavigationMenuContent>
                        <ul class="grid gap-3 p-6 md:w-[400px] lg:w-[500px] lg:grid-cols-[minmax(0,.75fr)_minmax(0,1fr)]">
                            <li class="row-span-3">
                                <NavigationMenuLink as-child>
                                    <a
                                        class="flex h-full w-full select-none flex-col justify-end rounded-md bg-gradient-to-b from-muted/50 to-muted p-6 no-underline outline-none focus:shadow-md"
                                        href="/"
                                    >
                                        <img src="https://www.radix-vue.com/logo.svg" class="h-6 w-6" />
                                        <div class="mb-2 mt-4 text-lg font-medium">shadcn/ui</div>
                                        <p class="text-sm leading-tight text-muted-foreground">
                                            Beautifully designed components built with Radix UI and Tailwind CSS.
                                        </p>
                                    </a>
                                </NavigationMenuLink>
                            </li>
                            <ListItem href="/docs" title="Introduction">
                                Re-usable components built using Radix UI and Tailwind CSS.
                            </ListItem>
                            <ListItem href="/docs/installation" title="Installation">
                                How to install dependencies and structure your app.
                            </ListItem>
                            <ListItem href="/docs/primitives/typography" title="Typography">
                                Styles for headings, paragraphs, lists...etc
                            </ListItem>
                        </ul>
                    </NavigationMenuContent>
                </NavigationMenuItem>
                <NavigationMenuItem>
                    <NavigationMenuTrigger>Components</NavigationMenuTrigger>
                    <NavigationMenuContent>
                        <ul class="grid w-[400px] gap-3 p-4 md:w-[500px] md:grid-cols-2 lg:w-[600px]">
                            <ListItem
                                v-for="component in components"
                                :key="component.title"
                                :title="component.title"
                                :href="component.href"
                            >
                                {{ component.description }}
                            </ListItem>
                        </ul>
                    </NavigationMenuContent>
                </NavigationMenuItem>
                <NavigationMenuItem>
                    <NuxtLink to="/sermons" :class="navigationMenuTriggerStyle()"> Sermons </NuxtLink>
                </NavigationMenuItem>
            </NavigationMenuList>
        </NavigationMenu>
        <div class="flex items-center gap-5">
            <Button size="sm">Login</Button>
            <div
                @click="colorMode.preference = colorMode.preference === 'dark' ? 'light' : 'dark'"
                class="cursor-pointer flex items-center justify-center"
            >
                <Icon
                    name="radix-icons:moon"
                    class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0"
                />
                <Icon
                    name="radix-icons:sun"
                    class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100"
                />
            </div>
        </div>
    </div>
</template>

<style lang="scss">
.router-link-exact-active {
    @apply bg-accent/50;
}
</style>
