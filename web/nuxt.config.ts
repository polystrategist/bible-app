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
                options: {
                    prefix: 'p',
                    darkModeSelector: '.my-app-dark',
                    cssLayer: false,
                },
            },
        },
    },
    vite: {
        css: {
            preprocessorOptions: {
                scss: {
                    api: 'modern-compiler', // or "modern"
                },
            },
        },
    },
});
