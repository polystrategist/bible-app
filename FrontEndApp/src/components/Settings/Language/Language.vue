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
        <div class="text-size-16px mb-1">
            <NIcon>
                <Language />
            </NIcon>
            {{ $t('Language') }}
        </div>
        <p class="text-xs opacity-50 mb-2">Choose the display language for the app interface.</p>
        <NSelect
            class="max-w-300px"
            size="small"
            v-model:value="$i18n.locale"
            :options="$i18n.availableLocales.map((l) => ({ label: l, value: l }))"
        />
    </div>
</template>
