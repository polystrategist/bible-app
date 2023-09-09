<script setup lang="ts">
import { NCard, NIcon, NTabs, NTabPane } from 'naive-ui';
import { Settings, SettingsAdjust, DataBin } from '@vicons/carbon';
import LanguageSetting from './Language/Language.vue';
import PrimaryColor from './PrimaryColor/PrimaryColor.vue';
import Theme from './Theme/Theme.vue';
import TabSetting from './Tabs/TabSetting.vue';
import { ref } from 'vue';
import SyncData from './Sync/SyncData.vue';
import Deuterocanonical from './Deuterocanonical/Deuterocanonical.vue';

const name = ref('General');
</script>
<template>
    <NCard size="small">
        <div class="w-full select-none">
            <div class="text-size-20px mb-3">
                <NIcon> <Settings /> </NIcon> Settings
            </div>
            <NTabs v-model:value="name" type="card" size="small" class="h-[70vh] min-h-100px">
                <NTabPane class="h-full overflow-y-auto overflowing-div" name="General">
                    <template #tab>
                        <span>
                            <NIcon>
                                <SettingsAdjust />
                            </NIcon>
                            General
                        </span>
                    </template>
                    <div class="flex flex-col gap-5 py-3">
                        <PrimaryColor />
                        <Theme />
                        <LanguageSetting />
                        <SyncData />
                        <Deuterocanonical />
                    </div>
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
