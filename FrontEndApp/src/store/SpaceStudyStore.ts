import { defineStore } from 'pinia';
import { onBeforeMount, onMounted, ref } from 'vue';
import SESSION from '../util/session';
import { useDialog, useMessage } from 'naive-ui';

export type SPACE_STUDY_SCHEMA = {
    id: number | string | 0;
    title: string;
    description: string;
    created_at?: string;
    updated_at?: string;
};

const selectedStudySpaceStorageKey = 'selectedStudySpaceStorageKey';

export default defineStore('useSpaceStudyStore', () => {
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
        return data;
    }

    function selectStudySpace(args: SPACE_STUDY_SCHEMA) {
        selectedSpaceStudy.value = args;

        SESSION.set(selectedStudySpaceStorageKey, args);

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
                await window.browserWindow.deleteSpaceStudy(id);
                message.success('Deleted Study Space');
                await getLists();
            },
        });
    }

    onBeforeMount(async () => {
        await getLists();
        selectedSpaceStudy.value = SESSION.get(selectedStudySpaceStorageKey) as SPACE_STUDY_SCHEMA;

        if (!selectedSpaceStudy.value && lists.value.length === 1) {
            selectedSpaceStudy.value = lists.value[0];
        }
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
