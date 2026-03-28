<script setup lang="ts">
import { NCheckbox, NAlert, NCheckboxGroup } from 'naive-ui';
import { useMenuStore } from '../../../store/menu';

const menuStore = useMenuStore();
</script>
<template>
    <div>
        <p class="text-xs opacity-50 mb-3">Choose which tabs are visible in the navigation bar.</p>
        <NCheckboxGroup v-model:value="menuStore.enableTab">
            <div class="flex flex-col gap-3">
                <div>
                    <NCheckbox :label="$t('Sermons')" value="sermons" />
                    <p class="text-xs opacity-50 mt-0.5 ml-6">Manage and view your sermon notes and outlines.</p>
                </div>
                <div>
                    <NCheckbox :label="$t('Prayer List')" value="/prayer-list" />
                    <p class="text-xs opacity-50 mt-0.5 ml-6">Track and organize your personal prayer requests.</p>
                </div>
            </div>
        </NCheckboxGroup>
    </div>
</template>
