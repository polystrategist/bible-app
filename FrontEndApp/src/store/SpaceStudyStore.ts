import { defineStore } from 'pinia';
import { onBeforeMount, onMounted, ref, watch } from 'vue';
import { useDialog, useMessage } from 'naive-ui';
import { useClipNoteStore } from './ClipNotes';
import { useBibleStore } from './BibleStore';
import { useBookmarkStore } from './bookmark';
import useNoteStore from './useNoteStore';

export type SPACE_STUDY_SCHEMA = {
    id: number | string | 0;
    title: string;
    description: string;
    created_at?: string;
    updated_at?: string;
};

export default defineStore('useSpaceStudyStore', () => {
    const noteStore = useNoteStore();
    const bookmarkStore = useBookmarkStore();
    const bibleStore = useBibleStore();
    const clipNoteStore = useClipNoteStore();
    const dialog = useDialog();
    const message = useMessage();
    const showSpaceStudy = ref(false);
    const lists = ref<Array<SPACE_STUDY_SCHEMA>>([]);
    const selectedSpaceStudy = ref<SPACE_STUDY_SCHEMA | null>(null);

    async function getLists(search?: string | null | undefined) {
        lists.value = await window.browserWindow.getSpaceStudyList(search);
    }

    async function store(args: SPACE_STUDY_SCHEMA) {
        const { data, error } = await window.browserWindow.storeSpaceStudy(JSON.stringify(args));

        if (error) {
            alert(error.message);
            return;
        }

        await getLists();

        selectStudySpace(data as any);

        return data;
    }

    async function selectStudySpace(args: SPACE_STUDY_SCHEMA) {
        const id = args.id;

        // update the database
        await window.browserWindow.selectStudySpace(id);

        // refresh the clip notes
        await clipNoteStore.getClipNotes();

        // refresh the highlights
        await bibleStore.getHighlights();

        // refresh bookmarks
        await bookmarkStore.getBookmarks();

        selectedSpaceStudy.value = args;

        message.success('Study Space Selected');
        showSpaceStudy.value = false;
    }

    async function deleteStudySpace(id: number) {
        dialog.error({
            title: 'Delete Study Space?',
            content:
                'Are you sure you want to delete this study space? Any bookmarks, clip notes, and any other data associated with this study space will also be deleted. This action cannot be undone.',
            positiveText: 'Yes, Remove',
            negativeText: 'Cancel',
            onPositiveClick: async () => {
                const data = await window.browserWindow.deleteSpaceStudy(id);

                if (data.error) {
                    dialog.error({
                        title: 'Unable To Delete',
                        content: data.error.message,
                        positiveText: 'OK',
                    });
                    return;
                }

                message.success('Deleted Study Space');
                await getLists();

                afterDeleteIfDeletedSelectedSelectTheFirstItemOnTheListAsDefault(id);
            },
        });
    }

    function afterDeleteIfDeletedSelectedSelectTheFirstItemOnTheListAsDefault(id: any) {
        selectStudySpace(lists.value[0]);
    }

    async function getSelectedSpaceStudy() {
        const { data, error } = await window.browserWindow.getSelectedSpaceStudy();
        return data;
    }

    onBeforeMount(async () => {
        await getLists();

        const savedSelectedSpace = await getSelectedSpaceStudy();
        selectedSpaceStudy.value = savedSelectedSpace;
    });

    return {
        showSpaceStudy,
        lists,
        getLists,
        store,
        selectedSpaceStudy,
        selectStudySpace,
        deleteStudySpace,
    };
});
