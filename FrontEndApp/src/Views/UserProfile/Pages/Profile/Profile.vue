<script lang='ts' setup>
import { onMounted, ref } from 'vue';
import { isSignedIn } from '../../../../util/SupaBase/Auth/Auth';
import { useUserStore } from '../../../../store/userStore';
import { useRouter } from 'vue-router';
import { supabase } from '../../../../util/SupaBase/SupaBase';
import { NButton, useDialog, useMessage } from 'naive-ui';

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
        }
    });
}
</script>

<template>
    <div class='flex justify-center items-center h-[80vh]'>
        <div class='flex flex-col items-center gap-3'>
            <div>You are Logged.</div>
            <div>{{ userStore.user ? userStore.user.user.email : '--' }}</div>
            <div>
                <NButton :disabled='loading' :loading='loading' secondary strong type='warning' @click='logout'>
                    Logout
                </NButton>
            </div>
        </div>
    </div>
</template>