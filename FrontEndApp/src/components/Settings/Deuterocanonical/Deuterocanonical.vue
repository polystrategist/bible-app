<script lang="ts" setup>
import { NSwitch } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { useSettingStore } from '../../../store/settingStore';

const settings = useSettingStore();
</script>

<template>
    <div>
        <div class="flex gap-1">
            <Icon class="text-size-16px" icon="fluent:save-sync-20-filled" />
            Deuterocanonical
        </div>
        <div class="flex items-center">
            <NSwitch v-model:value="settings.showDeuterocanonical">
                <template #checked> Yes</template>
                <template #unchecked> No</template>
            </NSwitch>
        </div>
    </div>
</template>
