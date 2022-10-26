import { routes } from "./../router/router";
import { defineStore } from "pinia";
import { useRouter } from "vue-router";
import { onBeforeMount, ref } from "vue";
import session from "./../util/session";

type menuHasRoute = "/prayer-list";
type menuHasNoRoute = "read-bible";

export const useMenuStore = defineStore("useMenuStore", () => {
    const menuWithRoute: Array<menuHasRoute | string> = routes.map((route) => route.path);
    const menuWithNoRoute: Array<menuHasNoRoute> = ["read-bible"];
    const menuSelected = ref<menuHasRoute | menuHasNoRoute>("read-bible");
    const router = useRouter();
    const isRouter = ref<boolean>(false);
    const menuSessionKey = "menu-session";

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
        if (menu == menuSelected.value) return;
        else if (menuWithRoute.includes(menu)) setMenuWithRoute(menu as any);
        else if (menuWithNoRoute.includes(menu as any)) setMenuWithNoRoute(menu as any);
        else console.log(menu + " was not found");
    }

    onBeforeMount(() => {
        const savedMenu: { isRouter: boolean; menuSelected: string } | undefined | null = session.get(menuSessionKey);
        if (savedMenu) setMenu(savedMenu.menuSelected);
    });

    return {
        menuSelected,
        isRouter,
        menuWithRoute,
        menuWithNoRoute,
        setMenu,
    };
});
