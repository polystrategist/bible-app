<script lang='ts' setup>
import type { Component } from 'vue';
import { h } from 'vue';
import { NButton, NDropdown, NIcon, useDialog, useMessage } from 'naive-ui';
import { Edit as EditIcon, Login, Logout as LogoutIcon, UserProfile as UserIcon } from '@vicons/carbon';
import { useMenuStore } from '../../../store/menu';
import { supabase } from '../../../util/SupaBase/SupaBase';
import { useUserStore } from '../../../store/userStore';

const dialog = useDialog();
const userStore = useUserStore();
const message = useMessage();
const menuStore = useMenuStore();
const renderIcon = (icon: Component) => {
    return () => {
        return h(NIcon, null, {
            default: () => h(icon)
        });
    };
};

const options = [
    {
        label: 'Profile',
        key: 'profile',
        icon: renderIcon(UserIcon)
    },
    {
        label: 'Edit Profile',
        key: 'editProfile',
        icon: renderIcon(EditIcon)
    },
    {
        label: 'Logout',
        key: 'logout',
        icon: renderIcon(LogoutIcon)
    }
];

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
            await menuStore.setMenu('/profile');
        }
    });
}

function handleSelect(key: string | number) {
    if (key == 'profile') menuStore.setMenu('/profile');
    if (key == 'logout') logout();
}

</script>

<template>
    <NDropdown
        v-if='userStore.user'
        :options='options'
        size='small'
        @select='handleSelect'
    >
        <NButton round size='tiny' tertiary>
            <template #icon>
                <NIcon>
                    <UserIcon />
                </NIcon>
            </template>
            Account
        </NButton>
    </NDropdown>
    <NButton v-else round size='tiny' tertiary @click='menuStore.setMenu("/profile")'>
        <template #icon>
            <NIcon>
                <Login />
            </NIcon>
        </template>
        Sign In
    </NButton>
</template>

