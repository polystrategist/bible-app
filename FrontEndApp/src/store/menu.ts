import { useMainStore } from './main';
import { defineStore } from 'pinia';
import { useRouter } from 'vue-router';
import { onBeforeMount, ref, watch } from 'vue';
import session from './../util/session';
import { renderNIcon } from '../util/helper';
import {
    Book24Filled,
    DocumentQueueMultiple24Filled,
    Person24Filled,
    Settings24Filled,
    HeartCircle24Filled,
    Book24Regular,
    DocumentQueueMultiple24Regular,
    Person24Regular,
    HeartCircle24Regular,
    Settings24Regular,
    BookStar24Regular,
    BookStar24Filled,
    Sparkle24Regular,
    Sparkle24Filled,
} from '@vicons/fluent';
import { PrayingHands } from '@vicons/fa';

export const useMenuStore = defineStore('useMenuStore', () => {
    const menuSelected = ref<string>('read-bible');
    const router = useRouter();
    const isRouter = ref<boolean>(false);
    const menuSessionKey = 'menu-session';
    const mainStore = useMainStore();

    // tabs
    const menuUpperTabs = ref([
        {
            label: 'read-bible',
            key: 'read-bible',
            icon: renderNIcon(Book24Regular),
            iconDark: renderNIcon(Book24Filled),
        },
        {
            label: 'Sermons',
            key: 'sermons',
            icon: renderNIcon(DocumentQueueMultiple24Regular),
            iconDark: renderNIcon(DocumentQueueMultiple24Filled),
        },
        {
            label: 'Prayer List',
            key: '/prayer-list',
            icon: renderNIcon(PrayingHands),
            iconDark: renderNIcon(PrayingHands),
        },
        {
            label: 'Daily Devotional',
            key: '/daily-devotional',
            icon: renderNIcon(BookStar24Regular),
            iconDark: renderNIcon(BookStar24Filled),
        },
        {
            label: 'AI Assistant',
            key: '/ai-assistant',
            icon: renderNIcon(Sparkle24Regular),
            iconDark: renderNIcon(Sparkle24Filled),
        },
    ]);

    const bottomMenuTabs = ref([
        // {
        //     label: 'Profile',
        //     key: '/profile',
        //     icon: renderNIcon(Person24Regular),
        //     iconDark: renderNIcon(Person24Filled),
        // },
        // {
        //     label: 'Donate',
        //     key: 'donate-modal',
        //     icon: renderNIcon(HeartCircle24Regular),
        //     iconDark: renderNIcon(HeartCircle24Filled),
        // },
        {
            label: 'Settings',
            key: '/settings-page',
            icon: renderNIcon(Settings24Regular),
            iconDark: renderNIcon(Settings24Filled),
        },
    ]);

    const localSavedTabsKey = 'localSavedTabsKey';
    const enableTab = ref([
        'read-bible',
        'sermons',
        '/prayer-list',
        '/daily-devotional',
        '/ai-assistant',
        // '/profile',
        '/settings-page',
        '/create-sermon',
        '/donate-page',
    ]);
    watch(
        () => enableTab.value,
        async (val) => {
            if (!val.includes(menuSelected.value)) await setMenu('read-bible');
            session.set(localSavedTabsKey, val);
        },
        { deep: true }
    );

    function setMenuWithNoRoute(menu: string) {
        menuSelected.value = menu;
        isRouter.value = false;
        session.set(menuSessionKey, {
            isRouter: isRouter.value,
            menuSelected: menuSelected.value,
        });
    }

    async function setMenuWithRoute(menu: string) {
        menuSelected.value = menu;
        isRouter.value = true;
        session.set(menuSessionKey, {
            isRouter: isRouter.value,
            menuSelected: menuSelected.value,
        });
        await router.push(menu);
    }

    async function setMenu(menu: string) {
        if (menu == '/settings-page') {
            mainStore.settingsTab = 'General';
            mainStore.showSettings = true;
            return;
        }

        if (menu == 'donate-modal') {
            window.browserWindow.openDonateWindow();
            return;
        }

        // Skip only when both the key and the router-mode are already correct.
        // If isRouter is true but we're navigating to a v-show key, we still need
        // setMenuWithNoRoute to flip isRouter back to false.
        if (menu == menuSelected.value && !isRouter.value) return;
        else if (menu.includes('/')) await setMenuWithRoute(menu as any);
        else if (!menu.includes('/')) setMenuWithNoRoute(menu as any);
    }

    onBeforeMount(async () => {
        // for saved tabs
        let savedLocalTabsKey = session.get(localSavedTabsKey);
        if (savedLocalTabsKey) {
            if (!savedLocalTabsKey.includes('/create-sermon')) {
                savedLocalTabsKey.push('/create-sermon');
                session.set(localSavedTabsKey, savedLocalTabsKey);
            }
            if (!savedLocalTabsKey.includes('/ai-assistant')) {
                savedLocalTabsKey.push('/ai-assistant');
                session.set(localSavedTabsKey, savedLocalTabsKey);
            }

            enableTab.value = session.get(localSavedTabsKey);
        }

        const savedMenu: { isRouter: boolean; menuSelected: string } | undefined | null = session.get(menuSessionKey);

        if (savedMenu) {
            await setMenu(savedMenu.menuSelected);
            return;
        }
    });

    return {
        menuSelected,
        isRouter,
        setMenu,
        setMenuWithNoRoute,
        menuUpperTabs,
        bottomMenuTabs,
        enableTab,
    };
});
