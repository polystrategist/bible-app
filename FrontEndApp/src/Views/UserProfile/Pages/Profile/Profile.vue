<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import { isSignedIn } from '../../../../util/SupaBase/Auth/Auth';
import { useUserStore } from '../../../../store/userStore';
import { useRouter } from 'vue-router';
import { supabase } from '../../../../util/SupaBase/SupaBase';
import { NButton, useDialog, useMessage } from 'naive-ui';
import ProfilePage from './../../../../components/ProfilePage/ProfilePage.vue';

const loading = ref(false);
const userStore = useUserStore();
const router = useRouter();
const message = useMessage();
const dialog = useDialog();

onMounted(async () => {
    if (!userStore.user) {
        const data = await isSignedIn();
        if (data) {
            userStore.user = data;

            if (userStore.profile_data) {
                let getProfile = await supabase.from('profile').select('*').eq('id', userStore.user.user.id).single();
                if (getProfile.data) userStore.profile_data = getProfile.data;
            }

            await router.push('/profile/profile');
        } else {
            await router.push('/profile');
        }
    }
});

async function logout() {
    dialog.warning({
        title: 'Confirm',
        content: 'Are you sure to logout?',
        positiveText: 'Yes',
        negativeText: 'No',
        onPositiveClick: async () => {
            const { error } = await supabase.auth.signOut();

            if (error) {
                message.error(error.message);
                return;
            }

            userStore.user = null;
            await router.push('/profile');
        },
    });
}
</script>

<template>
    <div class="h-full w-full">
        <div class="max-w-700px mx-auto py-3 px-3 mt-5">
            <ProfilePage v-if='userStore.user' :user_id="userStore.user.user.id" />
        </div>
    </div>
</template>
