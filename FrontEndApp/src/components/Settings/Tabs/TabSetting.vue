<script setup lang="ts">
import { NCheckbox, NAlert, NCheckboxGroup } from 'naive-ui';
import { useMenuStore } from '../../../store/menu';

const menuStore = useMenuStore();
</script>
<template>
    <div>
        <NCheckboxGroup v-model:value="menuStore.enableTab">
            <div class="flex flex-col gap-1 mt-5">
                <NCheckbox :label="$t('Sermons')" value="sermons" />
                <NCheckbox :label="$t('Prayer List')" value="/prayer-list" />
            </div>
        </NCheckboxGroup>
    </div>
</template>
