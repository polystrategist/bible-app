<script setup lang="ts">
import { Language } from '@vicons/carbon';
import { NIcon, NPopover, NScrollbar, NButton } from 'naive-ui';
import { ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import SESSION from '../../../util/session';
const savedLocaleKey = 'saveLanguageStorageKey';

const { locale } = useI18n();
const showPicker = ref(false);

watch(locale, (lang) => {
    SESSION.set(savedLocaleKey, lang);
});

function selectLocale(lang: string) {
    locale.value = lang;
    showPicker.value = false;
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
        <NPopover v-model:show="showPicker" trigger="click" placement="bottom-start" :show-arrow="false">
            <template #trigger>
                <NButton size="small" style="min-width: 180px; justify-content: space-between;">
                    {{ locale }}
                    <template #icon>
                        <NIcon>
                            <svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 11L2 5h12z"/></svg>
                        </NIcon>
                    </template>
                </NButton>
            </template>
            <NScrollbar style="max-height: 240px; min-width: 180px;">
                <div
                    v-for="lang in $i18n.availableLocales"
                    :key="lang"
                    class="lang-option"
                    :class="{ 'lang-option--active': lang === locale }"
                    @click="selectLocale(lang)"
                >
                    {{ lang }}
                </div>
            </NScrollbar>
        </NPopover>
    </div>
</template>

<style scoped>
.lang-option {
    padding: 6px 14px;
    cursor: pointer;
    font-size: 13px;
    border-radius: 4px;
    transition: background 0.12s;
}
.lang-option:hover {
    background: var(--n-item-color-hover, rgba(128, 128, 128, 0.12));
}
.lang-option--active {
    color: var(--primary-color);
    font-weight: 600;
}
</style>
