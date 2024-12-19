<script lang="ts" setup>
import type { Component } from 'vue';
import { h } from 'vue';
import { MessageReactive, NButton, NDropdown, NIcon, useDialog, useMessage } from 'naive-ui';
import { Edit as EditIcon, Login, Logout as LogoutIcon, UserProfile as UserIcon } from '@vicons/carbon';
import { useMenuStore } from '../../../store/menu';
import { supabase } from '../../../util/SupaBase/SupaBase';
import { useUserStore } from '../../../store/userStore';
import { useRouter } from 'vue-router';

const router = useRouter();
const dialog = useDialog();
const userStore = useUserStore();
const message = useMessage();
const menuStore = useMenuStore();
let loadingReactive: MessageReactive | null = null;
const renderIcon = (icon: Component) => {
    return () => {
        return h(NIcon, null, {
            default: () => h(icon),
        });
    };
};

const options = [
    {
        label: 'Profile',
        key: 'profile',
        icon: renderIcon(UserIcon),
    },
    // {
    //     label: 'Edit Profile',
    //     key: 'editProfile',
    //     icon: renderIcon(EditIcon),
    // },
    {
        label: 'Logout',
        key: 'logout',
        icon: renderIcon(LogoutIcon),
    },
];

async function logout() {
    dialog.warning({
        title: 'Confirm',
        content: 'Are you sure to logout?',
        positiveText: 'Yes',
        negativeText: 'No',
        onPositiveClick: async () => {
            if (!loadingReactive) {
                loadingReactive = message.loading('Signing Out...', {
                    duration: 0,
                });
            }
            const { error } = await supabase.auth.signOut();

            if (loadingReactive) {
                loadingReactive.destroy();
                loadingReactive = null;
            }

            if (error) {
                message.error(error.message);
                return;
            }

            message.success('Logged Out!');
            userStore.user = null;
            await menuStore.setMenu('/profile');
            router.push('/profile');
        },
    });
}

function handleSelect(key: string | number) {
    if (key == 'profile') menuStore.setMenu('/profile');
    if (key == 'logout') logout();
}
</script>

<template>
    <NDropdown v-if="userStore.user" :options="options" size="small" @select="handleSelect">
        <NButton round size="tiny" quaternary>
            <template #icon>
                <NIcon>
                    <UserIcon />
                </NIcon>
            </template>
            Account
        </NButton>
    </NDropdown>
    <NButton v-else round size="tiny" quaternary @click="menuStore.setMenu('/profile')">
        <template #icon>
            <NIcon>
                <Login />
            </NIcon>
        </template>
        Sign In
    </NButton>
</template>
