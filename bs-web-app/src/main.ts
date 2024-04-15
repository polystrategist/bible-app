import "./assets/index.css";

import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";

const app = createApp(App);

declare global {
    interface Window {
        sideBarTimeOut: any;
    }
}

app.use(createPinia());
app.use(router);

app.mount("#app");
