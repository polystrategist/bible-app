<script lang="ts" setup>
import { NAlert, NSwitch } from 'naive-ui';
import { useAuthStore } from '../../../store/authStore';
import { Icon } from '@iconify/vue';
import { useMenuStore } from '../../../store/menu';

const authStore = useAuthStore();
const menuStore = useMenuStore();
</script>

<template>
    <div v-show="false">
        <div>
            <Icon class="text-size-16px" icon="fluent:save-sync-20-filled" />
            Sync Data
        </div>
        <div class="flex flex-col items-start gap-3">
            <NSwitch :value="authStore.syncEnabled" :disabled="true">
                <template #checked> Sync</template>
                <template #unchecked> No</template>
            </NSwitch>
            <NAlert type="info" :show-icon="false">
                To sync your data, download the Believers Sword mobile app and enable sync in it.
            </NAlert>
            <span
                v-show="!authStore.user"
                class="ml-3 flex items-center gap-2 hover:text-[var(--primary-color)] cursor-pointer"
                @click="menuStore.setMenu('/profile')"
            >
                Login To Enable this Option
            </span>
            <span v-show="authStore.syncEnabled" class="ml-3 flex items-center gap-2">
                Data Is Being Sync
                <Icon class="text-[var(--primary-color)]" icon="line-md:loading-alt-loop" />
            </span>
        </div>
    </div>
</template>
