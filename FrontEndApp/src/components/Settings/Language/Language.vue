<script setup lang="ts">
import { Language } from '@vicons/carbon';
import { NIcon, NSelect } from 'naive-ui';
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import SESSION from '../../../util/session';

const savedLocaleKey = 'saveLanguageStorageKey';
const { locale, availableLocales } = useI18n();
const selectScrollbarProps = { trigger: 'none' as const };

const langOptions = computed(() =>
    availableLocales.map((lang) => ({ label: lang as string, value: lang as string })),
);

function onUpdateLocale(lang: string) {
    locale.value = lang;
    SESSION.set(savedLocaleKey, lang);
}
</script>

<template>
    <div>
        <div class="text-size-16px mb-1">
            <NIcon>
                <Language />
            </NIcon>
            {{ $t('Language') }}
        </div>
        <p class="text-xs opacity-50 mb-2">{{ $t('choose-display-language') }}</p>
        <NSelect
            :value="locale"
            :options="langOptions"
            size="small"
            style="width: 200px"
            to="body"
            :virtual-scroll="false"
            :scrollbar-props="selectScrollbarProps"
            @update:value="onUpdateLocale"
        />
    </div>
</template>
