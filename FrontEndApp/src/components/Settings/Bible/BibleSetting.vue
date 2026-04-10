<script setup lang="ts">
import { NTabs, NTabPane } from 'naive-ui';
import InstalledBibles from './InstalledBibles.vue';
import DownloadBibles from './DownloadBibles.vue';
import ImportBible from './ImportBible.vue';
</script>
<template>
    <NTabs type="line" size="small" default-value="Added">
        <NTabPane name="Added" :tab="$t('Added')">
            <div class="py-2">
                <InstalledBibles />
            </div>
        </NTabPane>
        <NTabPane name="Download" :tab="$t('Download')">
            <div class="py-2">
                <DownloadBibles />
            </div>
        </NTabPane>
        <NTabPane name="Import" :tab="$t('Import')">
            <div class="py-2">
                <ImportBible />
            </div>
        </NTabPane>
    </NTabs>
</template>
