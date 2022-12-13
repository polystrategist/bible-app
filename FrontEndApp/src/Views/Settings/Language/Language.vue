<script setup lang="ts">
import { Language } from '@vicons/carbon';
import { NIcon, NSelect } from 'naive-ui';
import { watch } from 'vue';
import { useI18n } from 'vue-i18n';
import SESSION from '../../../util/session';
const savedLocaleKey = 'saveLanguageStorageKey';

const { locale } = useI18n();

watch(locale, (lang) => {
    SESSION.set(savedLocaleKey, lang);
});
</script>
<template>
    <div>
        <div class="text-size-16px mb-2">
            <NIcon>
                <Language />
            </NIcon>
            Language
        </div>
        <NSelect
            class="max-w-300px"
            size="small"
            v-model:value="$i18n.locale"
            :options="$i18n.availableLocales.map((l) => ({ label: l, value: l }))"
        />
    </div>
</template>
