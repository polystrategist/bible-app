<script setup lang="ts">
const router = useRouter();
const supabase = useSupabaseClient();
const { $session } = useNuxtApp();
const pageRoutes = [
    {
        label: "Home",
        path: "/admin",
    },
    {
        label: "Sermons",
        path: "/admin/sermons",
    },
    {
        label: "Logout",
        path: "logout",
    },
];

async function changePage(path: string) {
    if (path === "logout" && confirm("Are you sure you want to logout")) {
        const { error } = await supabase.auth.signOut();
        if (error) {
            alert(error.message);
            return;
        }
        $session().remove("session");
        router.push("/login");
        return;
    }
    router.push({ path });
}

onBeforeMount(() => {
    document.body.className = "light";
});
</script>
<template>
    <div class="h-full w-full px-20px">
        <div class="p-3">Believers Sword Admin</div>
        <div class="flex">
            <div class="w-250px p-3 flex flex-col gap-2">
                <div
                    class="hover:font-600 cursor-pointer"
                    v-for="pageRoute in pageRoutes"
                    :key="pageRoute.path"
                    @click="changePage(pageRoute.path)"
                >
                    {{ pageRoute.label }}
                </div>
            </div>
            <div class="w-full p-3 bg-light-50 border rounded-md">
                <slot />
            </div>
        </div>
    </div>
</template>
