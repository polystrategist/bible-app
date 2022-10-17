import { createRouter, createWebHashHistory } from 'vue-router';
import Bible from './../views/Bible/Bible.vue';
import About from './../views/About/About.vue';

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        {
            path: '/',
            name: 'Bible',
            component: Bible,
        },
        {
            path: '/about',
            name: 'About',
            component: About,
        },
    ],
});

export default router;
