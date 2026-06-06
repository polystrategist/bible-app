import { createRouter, createWebHashHistory, createWebHistory, RouteRecordRaw } from 'vue-router';
import { useAuthStore } from '../store/authStore';
import PrayerList from './../Views/PrayerList/PrayerList.vue';
import WebSubscriptionGate from './../Views/UserProfile/Pages/WebSubscriptionGate.vue';
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
        // Web-only upsell shown to authenticated Free/lapsed accounts. The web
        // app is a paid feature (Sync or Pro); the guard below routes here.
        name: 'SubscriptionRequired',
        path: '/subscription-required',
        component: WebSubscriptionGate,
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
        name: 'AiAssistant',
        path: '/ai-assistant',
        component: AiAssistant,
    },
];
const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

router.beforeEach(async (to) => {
    // The desktop (Electron) build is the licensed app — no web subscription gate.
    if (window.isElectron) return true;
    if (to.meta?.public) return true;

    // Web requires a signed-in account…
    if (!localStorage.getItem('auth_token')) return { name: 'Login' };

    // …and a paid subscription. The web app is a Sync/Pro feature. Ensure the
    // verified tier is loaded (the guard can run before App.vue's initAuth on a
    // hard reload), then gate. The backend also enforces this on the data API.
    const auth = useAuthStore();
    await auth.ensureSession();
    if (!auth.token) return { name: 'Login' }; // token rejected (401) while loading

    if (!auth.isSyncEntitled) {
        return to.name === 'SubscriptionRequired' ? true : { name: 'SubscriptionRequired' };
    }
    // Entitled users shouldn't sit on the upsell page.
    if (to.name === 'SubscriptionRequired') return { name: 'PrayerList' };
    return true;
});

export default router;
