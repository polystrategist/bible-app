<script setup lang="ts">
import { NTabs, NTabPane } from 'naive-ui';
import InstalledBibles from './InstalledBibles.vue';
import DownloadBibles from './DownloadBibles.vue';
import ImportBible from './ImportBible.vue';

const canManageLocalBibleFiles = window.isElectron;
</script>
<template>
    <NTabs type="line" size="small" default-value="Added">
        <NTabPane name="Added" :tab="$t('Added')">
            <InstalledBibles />
        </NTabPane>
        <NTabPane v-if="canManageLocalBibleFiles" name="Download" :tab="$t('Download')">
            <div class="py-2">
                <DownloadBibles />
            </div>
        </NTabPane>
        <NTabPane v-if="canManageLocalBibleFiles" name="Import" :tab="$t('Import')">
            <div class="py-2">
                <ImportBible />
            </div>
        </NTabPane>
    </NTabs>
</template>
