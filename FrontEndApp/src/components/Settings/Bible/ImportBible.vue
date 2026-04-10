<script setup lang="ts">
import { NButton, NInput, NSelect, NIcon, useMessage, NSpin } from 'naive-ui';
import { ref, computed, watch } from 'vue';
import { useModuleStore } from '../../../store/moduleStore';
import { DocumentImport, Checkmark, Close } from '@vicons/carbon';

const message = useMessage();
const moduleStore = useModuleStore();

const importSource = ref<string>('ebible-sql');
const title = ref('');
const description = ref('');
const selectedFilePath = ref<string | null>(null);
const selectedFileName = ref<string | null>(null);
const isValidating = ref(false);
const isImporting = ref(false);
const validationResult = ref<{ valid: boolean; error?: string; verseCount?: number; warning?: string } | null>(null);
const duplicateError = ref<string | null>(null);

const sourceOptions = [
    { label: 'ebible.org SQL', value: 'ebible-sql' },
    { label: 'MyBible (.sqlite3)', value: 'mybible-sqlite3' },
];

watch(importSource, () => {
    selectedFilePath.value = null;
    selectedFileName.value = null;
    validationResult.value = null;
});

const canImport = computed(() => {
    return (
        title.value.trim().length > 0 &&
        selectedFilePath.value &&
        validationResult.value?.valid &&
        !duplicateError.value &&
        !isImporting.value
    );
});

let duplicateTimeout: ReturnType<typeof setTimeout> | null = null;
watch(title, (newTitle) => {
    duplicateError.value = null;
    if (duplicateTimeout) clearTimeout(duplicateTimeout);
    if (!newTitle.trim()) return;

    duplicateTimeout = setTimeout(async () => {
        const result = await window.browserWindow.importBibleCheckDuplicate(newTitle.trim());
        if (result.exists) {
            duplicateError.value = `A Bible module named "${newTitle.trim()}" already exists.`;
        }
    }, 300);
});

async function selectFile() {
    const result = await window.browserWindow.importBibleSelectFile(importSource.value);
    if (result.canceled || !result.filePath) return;

    selectedFilePath.value = result.filePath;
    selectedFileName.value = result.filePath.split(/[\\/]/).pop() || result.filePath;

    isValidating.value = true;
    validationResult.value = null;
    try {
        validationResult.value = await window.browserWindow.importBibleValidate({ filePath: result.filePath, source: importSource.value });
    } finally {
        isValidating.value = false;
    }
}

async function doImport() {
    if (!canImport.value || !selectedFilePath.value) return;

    isImporting.value = true;

    try {
        const result = await window.browserWindow.importBible({
            filePath: selectedFilePath.value,
            title: title.value.trim(),
            description: description.value.trim(),
            source: importSource.value,
        });

        if (result.success) {
            message.success(`Imported "${title.value.trim()}" successfully (${result.verseCount} verses)`);
            await moduleStore.getBibleLists();
            resetForm();
        } else {
            message.error(result.error || 'Import failed');
        }
    } catch (err: any) {
        message.error(`Import error: ${err.message}`);
    } finally {
        isImporting.value = false;
    }
}

function resetForm() {
    title.value = '';
    description.value = '';
    selectedFilePath.value = null;
    selectedFileName.value = null;
    validationResult.value = null;
    duplicateError.value = null;
}
</script>
<template>
    <div class="flex flex-col gap-3">
        <!-- Source Selection -->
        <div>
            <label class="block text-xs font-600 mb-1 opacity-70">Source Format</label>
            <NSelect v-model:value="importSource" :options="sourceOptions" size="small" />
        </div>

        <!-- Title -->
        <div>
            <label class="block text-xs font-600 mb-1 opacity-70">Title <span class="text-red-500">*</span></label>
            <NInput v-model:value="title" placeholder="e.g. King James Version 2006" size="small"
                :status="duplicateError ? 'error' : undefined" />
            <div v-if="duplicateError" class="text-xs text-red-500 mt-1">{{ duplicateError }}</div>
        </div>

        <!-- Description -->
        <div>
            <label class="block text-xs font-600 mb-1 opacity-70">Description</label>
            <NInput v-model:value="description" placeholder="Optional description" size="small" type="textarea"
                :rows="2" />
        </div>

        <!-- File Selection -->
        <div>
            <label class="block text-xs font-600 mb-1 opacity-70">
                {{ importSource === 'mybible-sqlite3' ? 'SQLite3 File' : 'SQL File' }}
                <span class="text-red-500">*</span>
            </label>
            <div class="flex gap-2 items-center">
                <NButton size="small" @click="selectFile" :disabled="isImporting">
                    <template #icon>
                        <NIcon><DocumentImport /></NIcon>
                    </template>
                    Select File
                </NButton>
                <span v-if="selectedFileName" class="text-xs opacity-70 truncate max-w-250px">{{ selectedFileName }}</span>
            </div>
        </div>

        <!-- Validation Status -->
        <div v-if="isValidating" class="flex items-center gap-2 text-xs opacity-70">
            <NSpin size="small" />
            Validating file...
        </div>
        <div v-else-if="validationResult" class="text-xs">
            <div v-if="validationResult.valid" class="flex flex-col gap-1">
                <div class="flex items-center gap-1 text-green-500">
                    <NIcon size="14"><Checkmark /></NIcon>
                    Valid — {{ validationResult.verseCount?.toLocaleString() }} verses found
                </div>
                <div v-if="validationResult.warning" class="text-yellow-500 opacity-80">
                    {{ validationResult.warning }}
                </div>
            </div>
            <div v-else class="text-red-500">
                <NIcon size="14"><Close /></NIcon>
                {{ validationResult.error }}
            </div>
        </div>

        <!-- Actions -->
        <div class="flex justify-end gap-2 mt-2">
            <NButton size="small" @click="resetForm" :disabled="isImporting">
                Reset
            </NButton>
            <NButton size="small" type="info" :disabled="!canImport" :loading="isImporting" @click="doImport">
                <template #icon>
                    <NIcon><DocumentImport /></NIcon>
                </template>
                Import
            </NButton>
        </div>
    </div>
</template>
