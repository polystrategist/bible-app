<script setup lang="ts">
import { NCheckbox, NAlert, NCheckboxGroup } from 'naive-ui';
import { useMenuStore } from '../../../store/menu';

const menuStore = useMenuStore();
</script>
<template>
    <div>
        <NAlert title="Tab Disable/Enable" type="info">
            You can disable or enable tab by checking or unchecking a tab option.
        </NAlert>
        <NCheckboxGroup v-model:value="menuStore.enableTab">
            <div class="flex flex-col gap-1 mt-5">
                <NCheckbox label="Sermons" value="sermons" />
                <NCheckbox label="Prayer List" value="/prayer-list" />
            </div>
        </NCheckboxGroup>
    </div>
</template>
