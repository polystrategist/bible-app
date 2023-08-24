<script lang='ts' setup>
import { NSwitch } from 'naive-ui';
import { useUserStore } from '../../../store/userStore';
import { Icon } from '@iconify/vue';

const userStore = useUserStore();
</script>

<template>
    <div>
        <div>
            <Icon class='text-size-16px' icon='fluent:save-sync-20-filled' />
            Sync Data <small>*if turned on, your data will be saved online. This way you can </small>
        </div>
        <div class='flex items-center'>
            <NSwitch v-model:value='userStore.syncData'>
                <template #checked> Sync</template>
                <template #unchecked> No</template>
            </NSwitch>
            <span v-show='userStore.syncData' class='ml-3 flex items-center gap-2'>
                Data Is Being Sync
                <Icon class='text-[var(--primary-color)]' icon='line-md:loading-alt-loop' />
            </span>
        </div>
    </div>
</template>
