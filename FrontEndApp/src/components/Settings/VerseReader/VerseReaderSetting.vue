<script setup lang="ts">
import { NRadio, NIcon, NButton, NProgress, NTooltip, NSwitch } from 'naive-ui';
import { CheckmarkCircle24Filled } from '@vicons/fluent';
import { Icon } from '@iconify/vue';
import { useSettingStore } from '../../../store/settingStore';
import { usePiperTTSStore } from '../../../store/piperTTSStore';
import { useDialog } from 'naive-ui';
import { onMounted, ref } from 'vue';
import PiperModelsModal from './PiperModelsModal.vue';

const dialog = useDialog();

const settings = useSettingStore();
const piperStore = usePiperTTSStore();
const showModelsModal = ref(false);

onMounted(() => piperStore.checkInstalled());

const options = [
    {
        value: 'browser-tts',
        title: 'Browser Text to Speech',
        description: "Uses your device's built-in speech engine to read Bible verses aloud. Works fully offline — no internet or external service required.",
    },
    {
        value: 'piper-tts',
        title: 'Piper Neural TTS',
        description: 'High-quality AI voice that runs fully offline using a neural network model. Sounds significantly more natural than browser speech. Requires a one-time download (~67 MB).',
    },
];

function installStepLabel(step: string, percent: number): string {
    if (step === 'binary') return `Downloading Piper engine… ${percent}%`;
    if (step === 'model') return `Downloading voice model… ${percent}%`;
    if (step === 'config') return 'Downloading model config…';
    if (step === 'done') return 'Installation complete!';
    return 'Installing…';
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
                    ? 'border-[var(--primary-color)] bg-[var(--primary-color)] bg-opacity-5'
                    : 'border-gray-500 border-opacity-30 hover:border-opacity-60'
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
                        >Installed</span>
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
                    Voice Models
                </NButton>
                <div class="flex-1" />
                <NTooltip trigger="hover">
                    <template #trigger>
                        <NButton
                            size="small"
                            type="error"
                            @click="dialog.warning({
                                title: 'Uninstall Piper?',
                                content: 'This will delete the Piper engine and all voice models. You can re-download anytime.',
                                positiveText: 'Uninstall',
                                negativeText: 'Cancel',
                                onPositiveClick: () => piperStore.uninstall(),
                            })"
                        >
                            <template #icon><Icon icon="mdi:delete-outline" /></template>
                        </NButton>
                    </template>
                    Uninstall Piper
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
                        Retry
                    </NButton>
                </div>

                <!-- Install prompt -->
                <div v-else class="flex items-center gap-3">
                    <NButton size="small" type="primary" @click="piperStore.install()">
                        <template #icon><Icon icon="mdi:download" /></template>
                        Download & Install (~67 MB)
                    </NButton>
                    <span class="text-xs opacity-40">One-time download</span>
                </div>
            </div>
        </div>
    </div>

    <!-- Read verse number toggle -->
    <div class="flex items-center justify-between p-3 rounded-lg border border-gray-500 border-opacity-30 mt-1">
        <div>
            <div class="font-600 text-sm">Read verse number</div>
            <div class="text-xs opacity-50 mt-0.5">Announce the verse number before reading each verse</div>
        </div>
        <NSwitch v-model:value="settings.readVerseNumber" />
    </div>

    <PiperModelsModal v-model:show="showModelsModal" />
</template>
