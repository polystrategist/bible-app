<script lang="ts" setup>
import { NSwitch } from 'naive-ui';
import { useUserStore } from '../../../store/userStore';
import { Icon } from '@iconify/vue';
import { useMenuStore } from '../../../store/menu';

const userStore = useUserStore();
const menuStore = useMenuStore();
</script>

<template>
    <div v-show="false">
        <div>
            <Icon class="text-size-16px" icon="fluent:save-sync-20-filled" />
            Sync Data <small>*if turned on, your data will be saved online. This way you can </small>
        </div>
        <div class="flex items-center">
            <NSwitch v-model:value="userStore.syncData" :disabled="!userStore.user">
                <template #checked> Sync</template>
                <template #unchecked> No</template>
            </NSwitch>
            <span
                v-show="!userStore.user"
                class="ml-3 flex items-center gap-2 hover:text-[var(--primary-color)] cursor-pointer"
                @click="menuStore.setMenu('/profile')"
            >
                Login To Enable this Option
            </span>
            <span v-show="userStore.syncData" class="ml-3 flex items-center gap-2">
                Data Is Being Sync
                <Icon class="text-[var(--primary-color)]" icon="line-md:loading-alt-loop" />
            </span>
        </div>
    </div>
</template>
