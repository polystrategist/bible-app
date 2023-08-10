import PrimeVue from "primevue/config";
import Button from "primevue/button";
import Editor from "primevue/editor";

export default defineNuxtPlugin((nuxtApp) => {
    nuxtApp.vueApp.use(PrimeVue, { ripple: true });
    nuxtApp.vueApp.component("PButton", Button);
    nuxtApp.vueApp.component("Editor", Editor);
});
