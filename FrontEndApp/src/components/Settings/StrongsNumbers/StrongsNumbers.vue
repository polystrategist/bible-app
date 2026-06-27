<script lang="ts" setup>
import { NSwitch } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { useSettingStore } from '../../../store/settingStore';

const settings = useSettingStore();
</script>

<template>
    <div>
        <div class="flex gap-1">
            <Icon class="text-size-16px" icon="mdi:book-alphabet" />
            {{ $t('strongs-numbers') }}
        </div>
        <p class="text-xs opacity-50 my-1">{{ $t('strongs-numbers-desc') }}</p>
        <div class="flex items-center">
            <NSwitch v-model:value="settings.showStrongsNumbers">
                <template #checked> {{ $t('Yes') }}</template>
                <template #unchecked> {{ $t('No') }}</template>
            </NSwitch>
        </div>
    </div>
</template>
