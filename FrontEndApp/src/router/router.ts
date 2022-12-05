import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import PrayerList from './../Views/PrayerList/PrayerList.vue';
import ProfilePage from './../Views/UserProfile/Profile.vue';
import AboutPage from './../Views/About/About.vue';
import SettingPage from './../Views/Settings/Settings.vue';

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
    {
        name: 'ProfilePage',
        path: '/profile',
        component: ProfilePage,
    },
    {
        name: 'AboutPage',
        path: '/about-page',
        component: AboutPage,
    },
    {
        name: 'SettingsPage',
        path: '/settings-page',
        component: SettingPage,
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
