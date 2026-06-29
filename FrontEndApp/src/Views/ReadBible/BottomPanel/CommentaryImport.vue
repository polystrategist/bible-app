<script setup lang="ts">
import { NButton, NInput, NIcon, NCheckbox, useMessage, NSpin } from 'naive-ui';
import { ref, computed, watch } from 'vue';
import { DocumentImport, Checkmark, Close } from '@vicons/carbon';

const emit = defineEmits<{ (e: 'imported', fileName: string): void; (e: 'cancel'): void }>();

const message = useMessage();

const name = ref('');
const selectedFilePath = ref<string | null>(null);
const selectedFileName = ref<string | null>(null);
const isValidating = ref(false);
const isImporting = ref(false);
const validationResult = ref<{ valid: boolean; error?: string; entryCount?: number } | null>(null);
const alreadyExists = ref(false);
const overwrite = ref(false);

const canImport = computed(
    () =>
        name.value.trim().length > 0 &&
        !!selectedFilePath.value &&
        validationResult.value?.valid &&
        (!alreadyExists.value || overwrite.value) &&
        !isImporting.value,
);

let duplicateTimeout: ReturnType<typeof setTimeout> | null = null;
watch(name, (newName) => {
    alreadyExists.value = false;
    overwrite.value = false;
    if (duplicateTimeout) clearTimeout(duplicateTimeout);
    if (!newName.trim()) return;

    duplicateTimeout = setTimeout(async () => {
        try {
            const result = await window.browserWindow.importCommentaryCheckDuplicate(newName.trim());
            alreadyExists.value = result.exists;
        } catch {
            /* non-fatal — duplicate check is best-effort */
        }
    }, 300);
});

async function selectFile() {
    let result: { canceled: boolean; filePath?: string };
    try {
        result = await window.browserWindow.importCommentarySelectFile();
    } catch (err: any) {
        message.error(`Could not open the file picker: ${err?.message ?? err}`);
        return;
    }
    if (result.canceled || !result.filePath) return;

    selectedFilePath.value = result.filePath;
    selectedFileName.value = result.filePath.split(/[\\/]/).pop() || result.filePath;

    // Default the name to the file's base name if the user hasn't typed one.
    if (!name.value.trim()) {
        name.value = (selectedFileName.value || '')
            .replace(/\.commentaries\.SQLite3$/i, '')
            .replace(/\.SQLite3$/i, '')
            .replace(/\.db$/i, '');
    }

    isValidating.value = true;
    validationResult.value = null;
    try {
        validationResult.value = await window.browserWindow.importCommentaryValidate({
            filePath: result.filePath,
        });
    } catch (err: any) {
        validationResult.value = { valid: false, error: `Validation failed: ${err?.message ?? err}` };
    } finally {
        isValidating.value = false;
    }
}

async function doImport() {
    if (!canImport.value || !selectedFilePath.value) return;

    isImporting.value = true;
    try {
        const result = await window.browserWindow.importCommentary({
            filePath: selectedFilePath.value,
            name: name.value.trim(),
            overwrite: overwrite.value,
        });

        if (result.success) {
            message.success(`Commentary imported (${result.entryCount?.toLocaleString()} entries)`);
            const fileName = result.fileName ?? '';
            resetForm();
            emit('imported', fileName);
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
    name.value = '';
    selectedFilePath.value = null;
    selectedFileName.value = null;
    validationResult.value = null;
    alreadyExists.value = false;
    overwrite.value = false;
}
</script>

<template>
    <div class="flex flex-col gap-3">
        <p class="text-xs opacity-70 m-0">
            Import a commentary SQLite file. It must contain a <code>commentaries</code> table with the
            standard columns. The imported commentary appears in the tab's selector for every translation.
        </p>

        <!-- File Selection -->
        <div>
            <label class="block text-xs font-600 mb-1 opacity-70">
                Commentary file <span class="text-red-500">*</span>
            </label>
            <div class="flex gap-2 items-center">
                <NButton size="small" :disabled="isImporting" @click="selectFile">
                    <template #icon>
                        <NIcon><DocumentImport /></NIcon>
                    </template>
                    Select File
                </NButton>
                <span v-if="selectedFileName" class="text-xs opacity-70 truncate max-w-250px">
                    {{ selectedFileName }}
                </span>
            </div>
        </div>

        <!-- Display name -->
        <div>
            <label class="block text-xs font-600 mb-1 opacity-70">
                Display name <span class="text-red-500">*</span>
            </label>
            <NInput
                v-model:value="name"
                placeholder="e.g. Matthew Henry Commentary"
                size="small"
                maxlength="80"
                :status="alreadyExists ? 'warning' : undefined"
            />
            <div v-if="alreadyExists" class="text-xs text-yellow-500 mt-1">
                A commentary named "{{ name.trim() }}" is already installed.
            </div>
        </div>

        <!-- Validation Status -->
        <div v-if="isValidating" class="flex items-center gap-2 text-xs opacity-70">
            <NSpin size="small" />
            Validating file...
        </div>
        <div v-else-if="validationResult" class="text-xs">
            <div v-if="validationResult.valid" class="flex items-center gap-1 text-green-500">
                <NIcon size="14"><Checkmark /></NIcon>
                Valid — {{ validationResult.entryCount?.toLocaleString() }} entries found
            </div>
            <div v-else class="flex items-center gap-1 text-red-500">
                <NIcon size="14"><Close /></NIcon>
                {{ validationResult.error }}
            </div>
        </div>

        <!-- Overwrite confirmation -->
        <NCheckbox v-if="alreadyExists" v-model:checked="overwrite" size="small">
            <span class="text-xs">Replace the existing commentary</span>
        </NCheckbox>

        <!-- Actions -->
        <div class="flex justify-end gap-2 mt-2">
            <NButton size="small" :disabled="isImporting" @click="emit('cancel')">Cancel</NButton>
            <NButton
                size="small"
                type="info"
                :disabled="!canImport"
                :loading="isImporting"
                @click="doImport"
            >
                <template #icon>
                    <NIcon><DocumentImport /></NIcon>
                </template>
                Import
            </NButton>
        </div>
    </div>
</template>
