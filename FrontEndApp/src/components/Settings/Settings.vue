<script setup lang="ts">
import { NCard, NIcon, NTabs, NTabPane } from 'naive-ui';
import { Settings, SettingsAdjust, DataBin } from '@vicons/carbon';
import LanguageSetting from './Language/Language.vue';
import PrimaryColor from './PrimaryColor/PrimaryColor.vue';
import Theme from './Theme/Theme.vue';
import TabSetting from './Tabs/TabSetting.vue';
import { ref } from 'vue';

const name = ref('General');
</script>
<template>
    <NCard size="small">
        <div class="w-full h-[80vh] select-none">
            <div class="text-size-20px mb-8">
                <NIcon> <Settings /> </NIcon> Settings
            </div>
            <NTabs v-model:value="name" type="card" size="small">
                <NTabPane class="flex flex-col gap-30px" name="General">
                    <template #tab>
                        <span>
                            <NIcon>
                                <SettingsAdjust />
                            </NIcon>
                            General
                        </span>
                    </template>
                    <PrimaryColor />
                    <Theme />
                    <LanguageSetting />
                </NTabPane>
                <NTabPane class="flex flex-col gap-30px" name="Tab">
                    <template #tab>
                        <span>
                            <NIcon>
                                <DataBin />
                            </NIcon>
                            Tabs
                        </span>
                    </template>
                    <TabSetting />
                </NTabPane>
            </NTabs>
        </div>
    </NCard>
</template>
