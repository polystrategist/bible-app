import { createRouter, createWebHashHistory, createWebHistory, RouteRecordRaw } from 'vue-router';
import PrayerList from './../Views/PrayerList/PrayerList.vue';
import ProfilePage from './../Views/UserProfile/Profile.vue';
import AboutPage from './../Views/About/About.vue';
import CreateSermon from './../Views/CreateSermon/CreateSermon.vue';
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
        path: '/profile',
        component: ProfilePage,
        children: [
            {
                path: '',
                name: 'ProfilePage',
                component: () => import('./../Views/UserProfile/Pages/Login.vue'),
            },
            {
                path: 'profile',
                component: () => import('./../Views/UserProfile/Pages/Profile/Profile.vue'),
            },
        ],
    },
    {
        name: 'AboutPage',
        path: '/about-page',
        component: AboutPage,
    },
    {
        name: 'CreateSermon',
        path: '/create-sermon',
        component: CreateSermon,
    },
];
const mode = import.meta.env.MODE == 'web' ? '/app/' : undefined;
const router = createRouter({
    history: createWebHashHistory(mode),
    routes,
});

export default router;
