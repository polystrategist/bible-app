<script setup lang="ts">
import { computed, onBeforeMount, onMounted, ref, watch } from 'vue';
import { Splitpanes, Pane } from 'splitpanes';
import { NButton, NCard, NDropdown, NEmpty, NIcon, NInput, NModal, useDialog } from 'naive-ui';
import { Add, TrashCan } from '@vicons/carbon';
import Editor from '../../../components/Editor/Editor.vue';
import useNoteStore from '../../../store/useNoteStore';
import SpaceStudyStore from '../../../store/SpaceStudyStore';
import SESSION from '../../../util/session';

const spaceStudyStore = SpaceStudyStore();
const EditorRef = ref<{
    setContent: Function;
}>();
const noteStore = useNoteStore();
const dialog = useDialog();
const showRenameModal = ref(false);
const renamingNoteId = ref('');
const noteNameInput = ref('');
const noteModalMode = ref<'create' | 'rename'>('rename');

const showNoteContextMenu = ref(false);
const noteContextX = ref(0);
const noteContextY = ref(0);
const contextNoteId = ref('');
const contextNoteTitle = ref('');
const takeNotePaneStorageKey = 'take-note-pane-sizes';
const paneSizes = ref<Array<{ min: number; max: number; size: number }>>([
    { min: 15, max: 45, size: 28 },
    { min: 55, max: 85, size: 72 },
]);

const contextMenuOptions = [
    {
        label: 'Rename Note',
        key: 'rename',
    },
    {
        label: 'Delete Note',
        key: 'delete',
    },
];

async function setNoteWhenSelectingADifferentSpace() {
    await noteStore.loadNoteForSelectedSpace(spaceStudyStore.selectedSpaceStudy?.id as number);
}

watch(
    () => spaceStudyStore.selectedSpaceStudy,
    async () => {
        await setNoteWhenSelectingADifferentSpace();
    }
);

watch(
    () => noteStore.selectedNoteId,
    () => {
        EditorRef.value?.setContent(noteStore.currentNoteContent);
    }
);

onMounted(async () => {
    await setNoteWhenSelectingADifferentSpace();
});

onBeforeMount(() => {
    const savedPaneSizes = SESSION.get(takeNotePaneStorageKey);
    if (savedPaneSizes) {
        paneSizes.value = savedPaneSizes;
    }
});

function handleContextAction(actionKey: string, noteId: string, currentTitle: string) {
    noteStore.selectNote(noteId);

    if (actionKey === 'delete') {
        confirmDeleteNote(noteId, currentTitle);
        return;
    }

    if (actionKey === 'rename') {
        noteModalMode.value = 'rename';
        renamingNoteId.value = noteId;
        noteNameInput.value = currentTitle || '';
        showRenameModal.value = true;
    }
}

function confirmDeleteNote(noteId: string, title?: string) {
    dialog.warning({
        title: 'Delete Note?',
        content: `Are you sure you want to delete "${title || 'this note'}"? This action cannot be undone.`,
        positiveText: 'Delete',
        negativeText: 'Cancel',
        onPositiveClick: () => {
            noteStore.deleteNote(noteId);
        },
    });
}

function openCreateNoteDialog() {
    noteModalMode.value = 'create';
    renamingNoteId.value = '';
    noteNameInput.value = '';
    showRenameModal.value = true;
}

function openNoteContextMenu(event: MouseEvent, noteId: string, title: string) {
    event.preventDefault();
    noteStore.selectNote(noteId);
    contextNoteId.value = noteId;
    contextNoteTitle.value = title;
    noteContextX.value = event.clientX;
    noteContextY.value = event.clientY;
    showNoteContextMenu.value = true;
}

function closeContextMenu() {
    showNoteContextMenu.value = false;
}

function clickRenameFromContext() {
    if (!contextNoteId.value) {
        return;
    }

    handleContextAction('rename', contextNoteId.value, contextNoteTitle.value);
    closeContextMenu();
}

function clickDeleteFromContext() {
    if (!contextNoteId.value) {
        return;
    }

    handleContextAction('delete', contextNoteId.value, contextNoteTitle.value);
    closeContextMenu();
}

function handleDropdownSelect(key: string | number) {
    if (key === 'rename') {
        clickRenameFromContext();
        return;
    }

    if (key === 'delete') {
        clickDeleteFromContext();
    }
}

const noteModalTitle = computed(() => (noteModalMode.value === 'create' ? 'Create Note' : 'Rename Note'));

function submitRename() {
    if (noteModalMode.value === 'create') {
        noteStore.addNote(noteNameInput.value);
        showRenameModal.value = false;
        return;
    }

    if (!renamingNoteId.value) {
        showRenameModal.value = false;
        return;
    }

    noteStore.renameNote(renamingNoteId.value, noteNameInput.value);
    showRenameModal.value = false;
}

function changePaneSizes(sizes: Array<any>) {
    paneSizes.value = sizes;
    SESSION.set(takeNotePaneStorageKey, sizes);
}
</script>
<template>
    <div class="h-[calc(100%-1px)] relative bg-opacity-0 take-note-root">
        <Splitpanes vertical :dbl-click-splitter="false" class="h-full w-full take-note-split" @resized="changePaneSizes">
            <Pane
                :size="paneSizes[0].size"
                :min-size="paneSizes[0].min"
                :max-size="paneSizes[0].max"
                class="rounded-md"
            >
                <div
                    class="h-[calc(100%-20px)] border border-gray-200 dark:bg-dark-400 bg-gray-200/55 dark:bg-dark-400 p-10px flex flex-col gap-2 take-note-list-panel"
                >
                    <NButton size="small" type="primary" secondary @click="openCreateNoteDialog()">
                        <template #icon>
                            <NIcon><Add /></NIcon>
                        </template>
                        New Note
                    </NButton>

                    <div class="overflow-y-auto overflowing-div hide-note-list-scrollbar h-full flex flex-col gap-1 pr-1">
                        <NEmpty v-if="!noteStore.notes.length" description="No notes yet" size="small" />

                        <div
                            v-for="(noteItem, index) in noteStore.notes"
                            :key="noteItem.id"
                            class="rounded-md border border-gray-200 dark:border-dark-300 p-2 cursor-pointer transition-colors"
                            :class="{
                                'bg-[var(--primary-color)]/20 border-[var(--primary-color)]':
                                    noteStore.selectedNoteId === noteItem.id,
                                'hover:bg-gray-200/40 dark:hover:bg-dark-200':
                                    noteStore.selectedNoteId !== noteItem.id,
                            }"
                            @click="noteStore.selectNote(noteItem.id)"
                            @contextmenu="
                                openNoteContextMenu($event, noteItem.id, noteItem.title || `Note ${index + 1}`)
                            "
                        >
                            <div class="flex items-start justify-between gap-1">
                                <div class="text-xs font-700 truncate">
                                    {{ noteItem.title || `Note ${index + 1}` }}
                                </div>
                                <NButton
                                    quaternary
                                    size="tiny"
                                    title="Delete note"
                                    @click.stop="confirmDeleteNote(noteItem.id, noteItem.title || `Note ${index + 1}`)"
                                >
                                    <template #icon>
                                        <NIcon><TrashCan /></NIcon>
                                    </template>
                                </NButton>
                            </div>
                        </div>
                    </div>
                </div>
            </Pane>

            <Pane :size="paneSizes[1].size" :min-size="paneSizes[1].min" :max-size="paneSizes[1].max" class="rounded-md">
                <div
                    class="h-full min-w-0 rounded-r-md border border-gray-200 dark:border-dark-200 bg-gray-200/55 dark:bg-dark-400 take-note-editor-panel"
                >
                    <Editor ref="EditorRef" v-model="noteStore.currentNoteContent" overflow  />
                </div>
            </Pane>
        </Splitpanes>

        <NDropdown
            trigger="manual"
            :show="showNoteContextMenu"
            :x="noteContextX"
            :y="noteContextY"
            placement="bottom-start"
            :options="contextMenuOptions"
            :on-clickoutside="closeContextMenu"
            @select="handleDropdownSelect"
        />

        <NModal v-model:show="showRenameModal">
            <NCard
                :title="noteModalTitle"
                size="small"
                role="dialog"
                aria-modal="true"
                class="max-w-400px"
            >
                <div class="flex flex-col gap-3">
                    <NInput
                        v-model:value="noteNameInput"
                        placeholder="Set note name"
                        maxlength="60"
                        @keyup.enter="submitRename"
                    />
                    <div class="flex justify-end gap-2">
                        <NButton size="small" @click="showRenameModal = false">Cancel</NButton>
                        <NButton type="primary" size="small" @click="submitRename">
                            {{ noteModalMode === 'create' ? 'Create' : 'Save' }}
                        </NButton>
                    </div>
                </div>
            </NCard>
        </NModal>
    </div>
</template>

<style scoped>
:deep(.take-note-split .splitpanes__splitter) {
    min-width: 10px;
    background: transparent;
    position: relative;
}

:deep(.take-note-split .splitpanes__splitter::before) {
    content: '';
    position: absolute;
    top: 6px;
    bottom: 6px;
    left: 50%;
    transform: translateX(-50%);
    width: 1px;
    background: rgba(120, 120, 120, 0.45);
}

:deep(.take-note-split .splitpanes__splitter:hover::before) {
    width: 2px;
    background: var(--primary-color);
}

.hide-note-list-scrollbar {
    -ms-overflow-style: none;
    scrollbar-width: none;
}

.hide-note-list-scrollbar::-webkit-scrollbar {
    width: 0;
    height: 0;
    display: none;
}
</style>
