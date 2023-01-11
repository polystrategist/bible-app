<script setup lang="ts">
import { NCard, NForm, NIcon } from 'naive-ui';
import { Settings } from '@vicons/carbon';
import LanguageSetting from './Language/Language.vue';
import PrimaryColor from './PrimaryColor/PrimaryColor.vue';
import Theme from './Theme/Theme.vue';
</script>
<template>
    <NCard size="small">
        <NForm class="w-full h-full select-none">
            <div class="text-size-20px mb-8">
                <NIcon> <Settings /> </NIcon> Settings
            </div>
            <div class="flex flex-col gap-30px">
                <PrimaryColor />
                <Theme />
                <LanguageSetting />
            </div>
        </NForm>
    </NCard>
</template>
