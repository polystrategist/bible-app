import { createRouter, createWebHashHistory, createWebHistory, RouteRecordRaw } from 'vue-router';
import PrayerList from './../Views/PrayerList/PrayerList.vue';
import AboutPage from './../Views/About/About.vue';
import HelpPortal from './../Views/HelpPortal/HelpPortal.vue';
import CreateSermon from './../Views/CreateSermon/CreateSermon.vue';
import LoginPage from './../Views/UserProfile/Pages/Login.vue';
import ProfileAccountPage from './../Views/UserProfile/Pages/Profile/Profile.vue';
import TextBaseSermon from '../Views/CreateSermon/TextBaseSermon.vue';
import YoutubeShare from '../Views/CreateSermon/YoutubeShare.vue';
import UserProfileLayout from './../Views/UserProfile/Profile.vue';
import CompareVerse from '../Views/CompareVerse/CompareVerse.vue';
import DailyDevotional from '../Views/DailyDevotional/DailyDevotional.vue';
import DailyBelievers from '../Views/DailyBelievers/DailyBelievers.vue';
import AiAssistant from '../Views/AiAssistant/AiAssistant.vue';

export const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        redirect: 'prayer-list',
    },
    {
        name: 'Login',
        path: '/login',
        component: LoginPage,
        meta: { public: true },
    },
    {
        name: 'PrayerList',
        path: '/prayer-list',
        component: PrayerList,
    },
    {
        path: '/profile',
        component: UserProfileLayout,
        children: [
            {
                path: '',
                name: 'ProfilePage',
                redirect: () =>
                    localStorage.getItem('auth_token') ? '/profile/profile' : '/login',
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
        name: 'HelpPortal',
        path: '/help-portal',
        component: HelpPortal,
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
    },
    {
        name: 'CompareVerse',
        path: '/compare-verse',
        component: CompareVerse,
    },
    {
        name: 'DailyDevotional',
        path: '/daily-devotional',
        component: DailyDevotional,
    },
    {
        name: 'DailyBelievers',
        path: '/daily-believers',
        component: DailyBelievers,
    },
    {
        name: 'AiAssistant',
        path: '/ai-assistant',
        component: AiAssistant,
    },
];
const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

router.beforeEach((to) => {
    if (window.isElectron) return true;
    if (to.meta?.public) return true;
    if (!localStorage.getItem('auth_token')) return { name: 'Login' };
    return true;
});

export default router;
