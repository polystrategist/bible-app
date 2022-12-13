<script setup lang="ts">
import { NCard, NForm, NIcon } from 'naive-ui';
import { Settings } from '@vicons/carbon';
import LanguageSetting from './Language/Language.vue';
import PrimaryColor from './PrimaryColor/PrimaryColor.vue';
import Theme from './Theme/Theme.vue';
</script>
<template>
    <NForm class="w-full h-full p-5 pl-8 select-none">
        <NCard size="small">
            <div class="text-size-20px mb-8">
                <NIcon> <Settings /> </NIcon> Settings
            </div>
            <div class="flex flex-col gap-30px">
                <PrimaryColor />
                <Theme />
                <LanguageSetting />
            </div>
        </NCard>
    </NForm>
</template>
