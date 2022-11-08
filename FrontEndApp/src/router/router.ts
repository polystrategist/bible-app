import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import PrayerList from './../Views/PrayerList/PrayerList.vue';

export const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        redirect: 'prayer-list',
    },
    {
        name: 'PrayerList',
        path: '/prayer-list',
        component: PrayerList,
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
