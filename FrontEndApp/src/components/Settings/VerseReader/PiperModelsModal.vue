<script setup lang="ts">
import { NModal, NButton, NProgress, NScrollbar } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { ref, onMounted, computed } from 'vue';
import { useSettingStore } from '../../../store/settingStore';

interface PiperVoice {
    id: string;
    name: string;
    language: string;
    gender: string;
    quality: string;
    sizeMB: number;
    isDownloaded: boolean;
}

const props = defineProps<{ show: boolean }>();
const emit = defineEmits<{ 'update:show': [value: boolean] }>();

const settings = useSettingStore();

const voices = ref<PiperVoice[]>([]);
const downloading = ref<Record<string, number | null>>({});
const downloadError = ref<Record<string, string>>({});
const selectedLanguage = ref('All');

const languages = computed(() => {
    const langs = ['All', ...new Set(voices.value.map(v => v.language))];
    return langs;
});

const filteredVoices = computed(() =>
    selectedLanguage.value === 'All'
        ? voices.value
        : voices.value.filter(v => v.language === selectedLanguage.value)
);

async function loadVoices() {
    try {
        voices.value = await window.browserWindow.piperVoices();
    } catch {
        voices.value = [];
    }
}

onMounted(() => {
    loadVoices();
    window.browserWindow.piperOnModelProgress((data) => {
        downloading.value = { ...downloading.value, [data.voiceId]: data.percent };
    });
});

async function installVoice(voice: PiperVoice) {
    downloading.value = { ...downloading.value, [voice.id]: 0 };
    downloadError.value = { ...downloadError.value, [voice.id]: '' };

    const result = await window.browserWindow.piperInstallModel(voice.id);

    if (result.success) {
        settings.piperActiveModel = voice.id;
    } else {
        downloadError.value = { ...downloadError.value, [voice.id]: result.error ?? 'Download failed' };
    }

    const next = { ...downloading.value };
    delete next[voice.id];
    downloading.value = next;

    await loadVoices();
}

async function deleteVoice(voice: PiperVoice) {
    await window.browserWindow.piperDeleteModel(voice.id);
    if (settings.piperActiveModel === voice.id) {
        settings.piperActiveModel = 'en_US-ryan-high';
    }
    await loadVoices();
}

function qualityColor(quality: string) {
    if (quality === 'High') return 'text-purple-400';
    if (quality === 'Low') return 'text-gray-400';
    return 'text-blue-400';
}
</script>

<template>
    <NModal
        :show="props.show"
        @update:show="emit('update:show', $event)"
        preset="card"
        title="Voice Models"
        style="max-width: 540px; width: 95vw;"
        :bordered="false"
        size="small"
    >
        <template #header-extra>
            <span class="text-xs opacity-40">Powered by Piper TTS</span>
        </template>

        <!-- Language filter -->
        <div class="flex flex-wrap gap-1.5 mb-3">
            <button
                v-for="lang in languages"
                :key="lang"
                class="text-xs px-2.5 py-1 rounded-full border transition-colors cursor-pointer"
                :class="
                    selectedLanguage === lang
                        ? 'border-[var(--primary-color)] bg-[var(--primary-color)] text-white font-700'
                        : 'border-gray-500 border-opacity-30 opacity-60 hover:opacity-100 font-400'
                "
                @click="selectedLanguage = lang"
            >{{ lang }}</button>
        </div>

        <NScrollbar style="max-height: 380px;">
            <div class="flex flex-col gap-2 pr-1">
                <div
                    v-for="voice in filteredVoices"
                    :key="voice.id"
                    class="flex flex-col gap-2 p-3 rounded-lg border transition-colors"
                    :class="
                        settings.piperActiveModel === voice.id
                            ? 'border-[var(--primary-color)] bg-[var(--primary-color)] bg-opacity-5'
                            : 'border-gray-500 border-opacity-20'
                    "
                >
                    <!-- Voice info row -->
                    <div class="flex items-center gap-2">
                        <div class="flex-1">
                            <div class="flex items-center gap-2 flex-wrap">
                                <span class="font-600 text-sm">{{ voice.name }}</span>
                                <span class="text-xs opacity-50">{{ voice.language }}</span>
                                <span class="text-xs opacity-50 flex items-center gap-0.5">
                                    <Icon :icon="voice.gender === 'Male' ? 'mdi:gender-male' : 'mdi:gender-female'" class="text-xs" />
                                    {{ voice.gender }}
                                </span>
                                <span class="text-xs font-500" :class="qualityColor(voice.quality)">{{ voice.quality }}</span>
                                <span class="text-xs opacity-40">~{{ voice.sizeMB }} MB</span>
                            </div>
                        </div>
                        <span
                            v-if="settings.piperActiveModel === voice.id"
                            class="text-xs px-2 py-0.5 rounded-full bg-green-500 text-white font-600 flex-shrink-0 flex items-center gap-1"
                        >
                            <Icon icon="mdi:check-circle" class="text-xs" />
                            Active
                        </span>
                    </div>

                    <!-- Download progress -->
                    <div v-if="downloading[voice.id] != null" class="flex flex-col gap-1">
                        <span class="text-xs opacity-60">Downloading… {{ downloading[voice.id] }}%</span>
                        <NProgress
                            type="line"
                            :percentage="downloading[voice.id] ?? 0"
                            :show-indicator="false"
                        />
                    </div>

                    <!-- Error -->
                    <div v-else-if="downloadError[voice.id]" class="flex items-center gap-2">
                        <span class="text-xs text-red-400 flex-1">{{ downloadError[voice.id] }}</span>
                        <NButton size="tiny" type="error" secondary @click="installVoice(voice)">
                            <template #icon><Icon icon="mdi:refresh" /></template>
                            Retry
                        </NButton>
                    </div>

                    <!-- Actions -->
                    <div v-else class="flex items-center gap-2">
                        <template v-if="voice.isDownloaded">
                            <NButton
                                v-if="settings.piperActiveModel !== voice.id"
                                size="tiny"
                                type="primary"
                                secondary
                                @click="settings.piperActiveModel = voice.id"
                            >
                                <template #icon><Icon icon="mdi:check" /></template>
                                Use this voice
                            </NButton>
                            <NButton size="tiny" secondary @click="deleteVoice(voice)">
                                <template #icon><Icon icon="mdi:delete-outline" /></template>
                                Delete
                            </NButton>
                        </template>
                        <NButton v-else size="tiny" secondary @click="installVoice(voice)">
                            <template #icon><Icon icon="mdi:download" /></template>
                            Download (~{{ voice.sizeMB }} MB)
                        </NButton>
                    </div>
                </div>
            </div>
        </NScrollbar>
    </NModal>
</template>
