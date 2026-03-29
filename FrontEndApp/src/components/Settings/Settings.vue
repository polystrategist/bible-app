<script setup lang="ts">
import { NCard, NIcon, NTabs, NTabPane } from 'naive-ui';
import { Settings, SettingsAdjust, DataBin } from '@vicons/carbon';
import LanguageSetting from './Language/Language.vue';
import PrimaryColor from './PrimaryColor/PrimaryColor.vue';
import Theme from './Theme/Theme.vue';
import TabSetting from './Tabs/TabSetting.vue';
import SyncData from './Sync/SyncData.vue';
import Deuterocanonical from './Deuterocanonical/Deuterocanonical.vue';
import Scale from './Scale/Scale.vue';
import VerseReaderSetting from './VerseReader/VerseReaderSetting.vue';
import Updates from './General/Updates.vue';
import { Icon } from '@iconify/vue';
import { useMainStore } from '../../store/main';
import { computed } from 'vue';

const mainStore = useMainStore();
const name = computed({
    get: () => mainStore.settingsTab,
    set: (v) => { mainStore.settingsTab = v; },
});
</script>
<template>
    <NCard size="small">
        <div class="w-full select-none">
            <div class="text-size-20px mb-3">
                <NIcon> <Settings /> </NIcon> {{ $t('Settings') }}
            </div>
            <NTabs v-model:value="name" type="card" size="small" class="h-[70vh] min-h-100px">
                <NTabPane class="h-full overflow-y-auto overflowing-div" name="General">
                    <template #tab>
                        <span>
                            <NIcon>
                                <SettingsAdjust />
                            </NIcon>
                            {{ $t('General') }}
                        </span>
                    </template>
                    <div class="flex flex-col gap-5 py-3">
                        <LanguageSetting />
                        <Scale />
                        <SyncData />
                        <Deuterocanonical />
                        <Updates />
                    </div>
                </NTabPane>
                <NTabPane class="flex flex-col gap-30px" name="Tab">
                    <template #tab>
                        <span>
                            <NIcon>
                                <DataBin />
                            </NIcon>
                            {{ $t('Tabs') }}
                        </span>
                    </template>
                    <TabSetting />
                </NTabPane>
                <NTabPane class="h-full overflow-y-auto overflowing-div" name="VerseReader">
                    <template #tab>
                        <span class="flex items-center gap-1">
                            <Icon icon="mdi:account-voice" style="font-size: 16px;" />
                            Verse Reader
                        </span>
                    </template>
                    <div class="py-3">
                        <p class="text-xs opacity-50 mb-4">Choose how Bible verses are read aloud. More options will be available in future updates.</p>
                        <VerseReaderSetting />
                    </div>
                </NTabPane>
            </NTabs>
        </div>
    </NCard>
</template>
