<script setup lang="ts">
const { $session } = useNuxtApp();
onBeforeMount(() => {
    const theme = $session().get("theme");
    if (!theme) {
        document.body.className = "dark";
        return;
    }
    const newTheme = theme && theme == "dark" ? "dark" : "light";
    document.body.className = newTheme;
});
</script>
<template>
    <div>
        <HomeNav />
        <div class="pt-15 max-w-1200px px-20px mx-auto">
            <slot />
        </div>
        <Footer />
    </div>
</template>
