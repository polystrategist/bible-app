import { createApp } from 'vue';
import { createPinia } from 'pinia';
import router from './routes/routes';
import App from './App.vue';
import 'virtual:windi.css';

createApp(App).use(createPinia()).use(router).mount('#app');
