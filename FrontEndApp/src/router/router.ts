import { createRouter, createWebHashHistory, createWebHistory, RouteRecordRaw } from 'vue-router';
import PrayerList from './../Views/PrayerList/PrayerList.vue';
import ProfilePage from './../Views/UserProfile/Profile.vue';
import AboutPage from './../Views/About/About.vue';
import CreateSermon from './../Views/CreateSermon/CreateSermon.vue';
import LoginPage from './../Views/UserProfile/Pages/Login.vue';
import ProfileAccountPage from './../Views/UserProfile/Pages/Profile/Profile.vue';
import TextBaseSermon from '../Views/CreateSermon/TextBaseSermon.vue';
import YoutubeShare from '../Views/CreateSermon/YoutubeShare.vue';

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
                component: LoginPage,
            },
            {
                path: 'profile',
                component: ProfileAccountPage,
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
    {
        name: "CreateTextBaseSermon",
        path: "/create-text-base-sermon",
        component: TextBaseSermon
    },
    {
        name: "CreateSermonYoutubeShare",
        path: "/create-sermon-youtube-share",
        component: YoutubeShare
    }
];
const mode = import.meta.env.MODE == 'web' ? '/app/' : undefined;
const router = createRouter({
    history: createWebHashHistory(mode),
    routes,
});

export default router;
