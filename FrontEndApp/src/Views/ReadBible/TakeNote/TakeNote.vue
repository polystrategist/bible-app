<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { NButton, NCard, NDropdown, NEmpty, NIcon, NInput, NModal } from 'naive-ui';
import { Add, TrashCan } from '@vicons/carbon';
import Editor from '../../../components/Editor/Editor.vue';
import useNoteStore from '../../../store/useNoteStore';
import SpaceStudyStore from '../../../store/SpaceStudyStore';

const spaceStudyStore = SpaceStudyStore();
const EditorRef = ref<{
    setContent: Function;
}>();
const noteStore = useNoteStore();
const showRenameModal = ref(false);
const renamingNoteId = ref('');
const renameInput = ref('');

const showNoteContextMenu = ref(false);
const noteContextX = ref(0);
const noteContextY = ref(0);
const contextNoteId = ref('');
const contextNoteTitle = ref('');

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

function handleContextAction(actionKey: string, noteId: string, currentTitle: string) {
    noteStore.selectNote(noteId);

    if (actionKey === 'delete') {
        noteStore.deleteNote(noteId);
        return;
    }

    if (actionKey === 'rename') {
        renamingNoteId.value = noteId;
        renameInput.value = currentTitle || '';
        showRenameModal.value = true;
    }
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

function submitRename() {
    if (!renamingNoteId.value) {
        showRenameModal.value = false;
        return;
    }

    noteStore.renameNote(renamingNoteId.value, renameInput.value);
    showRenameModal.value = false;
}
</script>
<template>
    <div class="p-10px h-[calc(100%-20px)] relative dark:bg-dark-400 bg-gray-100 rounded-md">
        <div class="h-full flex gap-2">
            <div
                class="w-180px min-w-160px h-full border-r border-gray-200 dark:border-dark-300 pr-2 flex flex-col gap-2"
            >
                <NButton size="small" type="primary" secondary @click="noteStore.addNote()">
                    <template #icon>
                        <NIcon><Add /></NIcon>
                    </template>
                    New Note
                </NButton>

                <div class="overflow-y-auto overflowing-div h-full flex flex-col gap-1 pr-1">
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
                                @click.stop="noteStore.deleteNote(noteItem.id)"
                            >
                                <template #icon>
                                    <NIcon><TrashCan /></NIcon>
                                </template>
                            </NButton>
                        </div>
                    </div>
                </div>
            </div>

            <div class="flex-1 min-w-0 h-full">
                <Editor ref="EditorRef" v-model="noteStore.currentNoteContent" overflow />
            </div>
        </div>

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
                title="Rename Note"
                size="small"
                role="dialog"
                aria-modal="true"
                class="max-w-400px"
            >
                <div class="flex flex-col gap-3">
                    <NInput
                        v-model:value="renameInput"
                        placeholder="Set note name"
                        maxlength="60"
                        @keyup.enter="submitRename"
                    />
                    <div class="flex justify-end gap-2">
                        <NButton size="small" @click="showRenameModal = false">Cancel</NButton>
                        <NButton type="primary" size="small" @click="submitRename">Save</NButton>
                    </div>
                </div>
            </NCard>
        </NModal>
    </div>
</template>
