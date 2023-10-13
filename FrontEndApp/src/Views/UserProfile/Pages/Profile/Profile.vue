<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import { isSignedIn } from '../../../../util/SupaBase/Auth/Auth';
import { useUserStore } from '../../../../store/userStore';
import { useRouter } from 'vue-router';
import { supabase } from '../../../../util/SupaBase/SupaBase';
import ProfilePage from './../../../../components/ProfilePage/ProfilePage.vue';

const userStore = useUserStore();
const router = useRouter();

onMounted(async () => {
    if (!userStore.user) {
        const data = await isSignedIn();
        if (data) {
            userStore.user = data;

            if (userStore.profile_data) {
                let getProfile = await supabase.from('profile').select('*').eq('id', userStore.user.user.id).single();
                if (getProfile.data) userStore.profile_data = getProfile.data;
            }
        } else {
            await router.push('/profile');
        }
    }
});
</script>

<template>
    <div class="h-full w-full">
        <div class="max-w-500px mx-auto py-3 px-3 mt-5">
            <ProfilePage v-if="userStore.user" :user_id="userStore.user.user.id" />
        </div>
    </div>
</template>
