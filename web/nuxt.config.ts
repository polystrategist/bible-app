import Aura from '@primevue/themes/aura';

export default defineNuxtConfig({
    ssr: true,
    compatibilityDate: '2024-04-03',
    devtools: { enabled: true },
    future: {
        compatibilityVersion: 4,
    },
    modules: ['@unocss/nuxt', '@nuxt/fonts', '@primevue/nuxt-module'],
    css: ['~/assets/style/main.scss'],
    primevue: {
        /* Configuration */
        options: {
            ripple: true,

            theme: {
                preset: Aura,
                darkModeSelector: '.my-app-dark',
            },
        },
    },
});
