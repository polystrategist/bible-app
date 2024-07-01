import { createApp } from 'vue';
import { createPinia } from 'pinia';
import router from './router/router';
import App from './App.vue';
import Internationalization from './util/Internationalization';
import './GlobalDeclare';
import './assets/styles/main.scss';
import 'splitpanes/dist/splitpanes.css';
import '@unocss/reset/normalize.css';
import 'virtual:uno.css';

window.isElectron = true;

const userAgent = navigator.userAgent.toLowerCase();
if (userAgent.indexOf(' electron/') < 0) window.isElectron = false;

createApp(App).use(createPinia()).use(router).use(Internationalization).mount('#app');
