export default defineNuxtConfig({
    modules: ["nuxt-windicss", "@nuxtjs/supabase"],
    css: [
        "primevue/resources/themes/saga-blue/theme.css",
        "primevue/resources/primevue.css",
        "primeicons/primeicons.css",
        "~/assets/style/main.scss",
        "vue3-carousel/dist/carousel.css",
    ],
});
