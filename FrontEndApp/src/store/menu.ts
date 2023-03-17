import { useMainStore } from './main';
import { routes } from './../router/router';
import { defineStore } from 'pinia';
import { useRouter } from 'vue-router';
import { onBeforeMount, ref, watch } from 'vue';
import session from './../util/session';
import { renderIcon } from '../util/helper';
import { Book, MediaLibrary, Settings, UserProfile } from '@vicons/carbon';
import { Pray } from '@vicons/fa';

type menuHasRoute = '/prayer-list' | '/profile';
type menuHasNoRoute = 'read-bible' | 'sermons';

export const useMenuStore = defineStore('useMenuStore', () => {
    const menuWithRoute: Array<menuHasRoute | string> = routes.map((route) => route.path);
    const menuWithNoRoute: Array<menuHasNoRoute> = ['read-bible', 'sermons'];
    const menuSelected = ref<menuHasRoute | menuHasNoRoute>('read-bible');
    const router = useRouter();
    const isRouter = ref<boolean>(false);
    const menuSessionKey = 'menu-session';
    const mainStore = useMainStore();

    // tabs
    const menuUpperTabs = ref([
        {
            label: 'read-bible',
            key: 'read-bible',
            icon: renderIcon(Book),
        },
        {
            label: 'Sermons',
            key: 'sermons',
            icon: renderIcon(MediaLibrary),
        },
        {
            label: 'Prayer List',
            key: '/prayer-list',
            icon: renderIcon(Pray),
        },
    ]);

    const bottomMenuTabs = ref([
        {
            label: 'Profile',
            key: '/profile',
            icon: renderIcon(UserProfile),
        },
        {
            label: 'Settings',
            key: '/settings-page',
            icon: renderIcon(Settings),
        },
    ]);

    const localSavedTabsKey = 'localSavedTabsKey';
    const enableTab = ref(['read-bible', 'sermons', '/prayer-list', '/profile', '/settings-page']);
    watch(
        () => enableTab.value,
        (val) => {
            setMenu('read-bible');
            session.set(localSavedTabsKey, val);
        },
        { deep: true }
    );

    function setMenuWithNoRoute(menu: menuHasNoRoute) {
        menuSelected.value = menu;
        isRouter.value = false;
        session.set(menuSessionKey, {
            isRouter: isRouter.value,
            menuSelected: menuSelected.value,
        });
    }

    function setMenuWithRoute(menu: menuHasRoute) {
        menuSelected.value = menu;
        isRouter.value = true;
        session.set(menuSessionKey, {
            isRouter: isRouter.value,
            menuSelected: menuSelected.value,
        });
        router.push(menu);
    }

    function setMenu(menu: string) {
        if (menu == '/settings-page') {
            mainStore.showSettings = true;
            return;
        }

        if (menu == menuSelected.value) return;
        else if (menuWithRoute.includes(menu)) setMenuWithRoute(menu as any);
        else if (menuWithNoRoute.includes(menu as any)) setMenuWithNoRoute(menu as any);
        else console.log(menu + ' was not found');
    }

    onBeforeMount(() => {
        const savedMenu: { isRouter: boolean; menuSelected: string } | undefined | null = session.get(menuSessionKey);
        if (savedMenu) setMenu(savedMenu.menuSelected);

        // for saved tabs
        if (session.get(localSavedTabsKey)) {
            enableTab.value = session.get(localSavedTabsKey);
        }
    });

    return {
        menuSelected,
        isRouter,
        menuWithRoute,
        menuWithNoRoute,
        setMenu,
        menuUpperTabs,
        bottomMenuTabs,
        enableTab,
    };
});
