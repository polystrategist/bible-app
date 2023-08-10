<script setup lang="ts">
const emailAddress = ref(null);
const password = ref(null);
const supabase = useSupabaseClient();
const loading = ref(false);
const { $session } = useNuxtApp();
const router = useRouter();

onBeforeMount(() => {
    if ($session().get("session")) {
        router.push({ path: "/admin" });
    }
});

async function loginUser() {
    const data = {
        email: emailAddress.value,
        password: password.value,
    };
    loading.value = true;
    const { user, session, error } = await supabase.auth.signIn(data as any);
    if (error) {
        alert("Their is an Error");
        loading.value = false;
        return false;
    }

    if (session) $session().set("session", session);
    router.push("/admin");
    loading.value = false;
}
</script>
<template>
    <NuxtLayout>
        <div class="min-h-[100vh]">
            <form @submit.prevent="loginUser" class="w-500px mt-4 mx-auto p-4 border shadow flex flex-col gap-5">
                <div>
                    <label for="email-address">Email</label><br />
                    <input
                        class="border-b w-full px-2 py-1"
                        v-model="emailAddress"
                        id="email-address"
                        type="text"
                        placeholder="Email Address"
                    />
                </div>
                <div>
                    <label for="password">Password</label><br />
                    <input
                        class="border-b w-full px-2 py-1"
                        v-model="password"
                        id="password"
                        type="password"
                        placeholder="Password"
                    />
                </div>
                <div>
                    <PButton class="border px-2 py-1" type="submit" label="Login" :loading="loading" />
                </div>
            </form>
        </div>
    </NuxtLayout>
</template>
