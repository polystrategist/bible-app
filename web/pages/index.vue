<script lang="ts" setup>
useHead({
    title: 'Believers Sword',
});
</script>

<template>
    <section
        class="mx-auto flex max-w-[980px] flex-col items-center gap-2 py-8 md:py-12 md:pb-8 lg:py-24 lg:pb-20 page-header pb-8 page-header"
    >
        <a href="/blocks" class="inline-flex items-center rounded-lg bg-muted px-3 py-1 text-sm font-medium"
            >✨ <span class="hidden sm:inline">Download App Now!</span
            ><svg viewBox="0 0 15 15" width="1.2em" height="1.2em" class="ml-1 h-4 w-4">
                <path
                    fill="currentColor"
                    fill-rule="evenodd"
                    d="M8.146 3.146a.5.5 0 0 1 .708 0l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L11.293 8H2.5a.5.5 0 0 1 0-1h8.793L8.146 3.854a.5.5 0 0 1 0-.708"
                    clip-rule="evenodd"
                ></path></svg
        ></a>
        <div class="relative w-full max-w-sm items-center">
            <Input id="search" type="text" placeholder="Search..." class="pl-10" />
            <span class="absolute start-0 inset-y-0 flex items-center justify-center px-2">
                <Icon name="ic:baseline-search" class="size-6 text-muted-foreground" />
            </span>
        </div>
        <h1 class="text-center text-3xl font-bold leading-tight tracking-tighter md:text-6xl lg:leading-[1.1]">
            Sharpen Your Faith with <br />Believers Sword
        </h1>
        <span
            data-br="8InUq"
            class="max-w-[750px] text-center text-lg text-muted-foreground sm:text-xl"
            data-brr="1"
            style="display: inline-block; vertical-align: top; text-decoration: inherit; text-wrap: initial; max-width: 568px"
        >
            Praise be to God! Welcome to 'Believers Sword,' a haven for refining the faith of believers. Sharing and Learning from
            different believers.</span
        >
        <section class="flex w-full items-center justify-center space-x-4 py-4 md:pb-10">
            <Button size="sm">Create Account</Button>
            <NuxtLink href="https://github.com/Bible-Projects/believers-sword-next" target="_blank">
                <Button size="sm">
                    <Icon class="mr-2" name="mdi:github" size="20" />
                    Github
                </Button>
            </NuxtLink>
        </section>
    </section>
</template>
