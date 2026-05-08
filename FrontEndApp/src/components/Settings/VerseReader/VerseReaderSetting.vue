<script setup lang="ts">
import { NRadio, NIcon, NButton, NProgress, NTooltip, NSwitch } from 'naive-ui';
import { CheckmarkCircle24Filled } from '@vicons/fluent';
import { Icon } from '@iconify/vue';
import { useSettingStore } from '../../../store/settingStore';
import { usePiperTTSStore } from '../../../store/piperTTSStore';
import { useDialog } from 'naive-ui';
import { computed, onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import PiperModelsModal from './PiperModelsModal.vue';

const { t } = useI18n();
const dialog = useDialog();

const settings = useSettingStore();
const piperStore = usePiperTTSStore();
const showModelsModal = ref(false);
const canUsePiperTts = window.isElectron;

onMounted(() => {
    if (!canUsePiperTts && settings.verseReaderMode === 'piper-tts') {
        settings.verseReaderMode = 'browser-tts';
    }

    if (canUsePiperTts) {
        piperStore.checkInstalled();
    }
});

const options = computed(() => [
    {
        value: 'browser-tts',
        title: t('Browser Text to Speech'),
        description: t('browser-tts-desc'),
    },
    ...(canUsePiperTts
        ? [
              {
                  value: 'piper-tts',
                  title: 'Piper Neural TTS',
                  description: t('piper-tts-desc'),
              },
          ]
        : []),
]);

function installStepLabel(step: string, percent: number): string {
    if (step === 'binary') return `${t('Downloading Piper engine')}… ${percent}%`;
    if (step === 'model') return `${t('Downloading voice model')}… ${percent}%`;
    if (step === 'config') return `${t('Downloading model config')}…`;
    if (step === 'done') return t('Installation complete!');
    return `${t('Installing')}…`;
}
</script>

<template>
    <div class="flex flex-col gap-3">
        <div
            v-for="option in options"
            :key="option.value"
            class="flex flex-col p-3 rounded-lg border cursor-pointer transition-colors"
            :class="
                settings.verseReaderMode === option.value
                    ? 'border-[var(--primary-color)]'
                    : 'border-gray-500 border-opacity-30 hover:border-opacity-60'
            "
            :style="
                settings.verseReaderMode === option.value
                    ? 'background-color: color-mix(in srgb, var(--primary-color) 10%, transparent)'
                    : ''
            "
            @click="settings.verseReaderMode = option.value"
        >
            <!-- Top row: radio + title + check icon -->
            <div class="flex items-start gap-3">
                <NRadio
                    :checked="settings.verseReaderMode === option.value"
                    :value="option.value"
                    class="mt-0.5 flex-shrink-0"
                    @update:checked="settings.verseReaderMode = option.value"
                />
                <div class="flex-1">
                    <div class="font-600 text-sm flex items-center gap-2">
                        {{ option.title }}
                        <span
                            v-if="option.value === 'piper-tts' && piperStore.isInstalled"
                            class="text-xs px-1.5 py-0.5 rounded-full bg-green-500 bg-opacity-20 text-green-400"
                        >{{ $t('Installed') }}</span>
                    </div>
                    <div class="text-xs opacity-50 mt-0.5">{{ option.description }}</div>
                </div>
                <NIcon
                    v-if="settings.verseReaderMode === option.value"
                    size="20"
                    class="flex-shrink-0 mt-0.5"
                >
                    <CheckmarkCircle24Filled />
                </NIcon>
            </div>

            <!-- Piper: uninstall + models buttons shown when installed -->
            <div
                v-if="option.value === 'piper-tts' && piperStore.isInstalled"
                class="mt-2 ml-7 flex items-center gap-2"
                @click.stop
            >
                <NButton size="small" secondary @click="showModelsModal = true">
                    <template #icon><Icon icon="mdi:account-voice" /></template>
                    {{ $t('Voice Models') }}
                </NButton>
                <div class="flex-1" />
                <NTooltip trigger="hover">
                    <template #trigger>
                        <NButton
                            size="small"
                            type="error"
                            @click="dialog.warning({
                                title: t('Uninstall Piper?'),
                                content: t('uninstall-piper-content'),
                                positiveText: t('Uninstall'),
                                negativeText: t('Cancel'),
                                onPositiveClick: () => piperStore.uninstall(),
                            })"
                        >
                            <template #icon><Icon icon="mdi:delete-outline" /></template>
                        </NButton>
                    </template>
                    {{ $t('Uninstall Piper') }}
                </NTooltip>
            </div>

            <!-- Piper: install section shown when selected and not yet installed -->
            <div
                v-if="option.value === 'piper-tts' && settings.verseReaderMode === 'piper-tts' && !piperStore.isInstalled"
                class="mt-3 ml-7"
                @click.stop
            >
                <!-- Installing progress -->
                <div v-if="piperStore.isInstalling" class="flex flex-col gap-2">
                    <span class="text-xs opacity-70">
                        {{ installStepLabel(piperStore.installStep, piperStore.installPercent) }}
                    </span>
                    <NProgress
                        type="line"
                        :percentage="piperStore.installPercent"
                        :show-indicator="false"
                        class="max-w-300px"
                    />
                </div>

                <!-- Error state -->
                <div v-else-if="piperStore.installError" class="flex flex-col gap-2">
                    <span class="text-xs text-red-400">{{ piperStore.installError }}</span>
                    <NButton size="small" type="error" secondary @click="piperStore.install()">
                        <template #icon><Icon icon="mdi:refresh" /></template>
                        {{ $t('Retry') }}
                    </NButton>
                </div>

                <!-- Install prompt -->
                <div v-else class="flex items-center gap-3">
                    <NButton size="small" type="primary" @click="piperStore.install()">
                        <template #icon><Icon icon="mdi:download" /></template>
                        {{ $t('Download & Install (~67 MB)') }}
                    </NButton>
                    <span class="text-xs opacity-40">{{ $t('One-time download') }}</span>
                </div>
            </div>
        </div>
    </div>

    <!-- Read verse number toggle -->
    <div class="flex items-center justify-between p-3 rounded-lg border border-gray-500 border-opacity-30 mt-1">
        <div>
            <div class="font-600 text-sm">{{ $t('Read verse number') }}</div>
            <div class="text-xs opacity-50 mt-0.5">{{ $t('announce-verse-number-desc') }}</div>
        </div>
        <NSwitch v-model:value="settings.readVerseNumber" />
    </div>

    <PiperModelsModal v-if="canUsePiperTts" v-model:show="showModelsModal" />
</template>
