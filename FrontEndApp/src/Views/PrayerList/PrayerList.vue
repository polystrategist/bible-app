<script lang="ts" setup>
import { ref } from 'vue';
import { NPopconfirm, NIcon, NButton } from 'naive-ui';
import EditPrayerItem from './EditPrayerItem.vue';
import { Edit, TrashCan } from '@vicons/carbon';
import Draggable from 'vuedraggable';
import { usePrayerListStore } from '../../store/prayerListStore';
import NewPrayerItem from './CreateNewPrayerItem.vue';

const prayerListStore = usePrayerListStore();
const editPrayerModal = ref<any>(null);

const removePrayerItem = (key: string) => {
    try {
        prayerListStore.removePrayerItem(key);
    } catch (e) {
        if (e instanceof Error) console.log(e.message);
    }
};

const editPrayerItem = (key: string, content: any): void => {
    editPrayerModal.value?.modalTrigger(content, key);
    editPrayerModal.value?.editor?.commands.setContent(content);
};

async function changeInProgress(item: any) {
    const theKeyAction = item.added ? 'added' : item.moved ? 'moved' : 'removed';
}

async function changeInDone(item: any) {
    const theKeyAction = item.added ? 'added' : item.moved ? 'moved' : 'removed';
    let theItem = JSON.parse(JSON.stringify(item[theKeyAction].element));

    if (item.added) theItem['status'] = 'done';
    else if (item.removed) theItem['status'] = 'ongoing';

    await prayerListStore.savePrayerItem(theItem, theItem.key);
}

const dragOptions = {
    animation: 200,
    group: 'description',
    disabled: false,
    ghostClass: 'ghost',
};
</script>
<template>
    <div class="prayer-list-page px-10px h-[100%] overflow-y-auto overflowing-div scroll-bar-sm flex gap-30px pl-30px">
        <div class="w-[100%] h-[100%] flex flex-col">
            <div class="p-10px flex justify-between items-center select-none min-h-60px">
                <span class="font-700 text-size-20px capitalize">{{ $t('prayer list') }}</span>
                <NewPrayerItem />
            </div>
            <Draggable
                class="list-group h-[100%] overflow-y-auto overflowing-div pr-10px"
                :list="prayerListStore.prayerList"
                v-bind="dragOptions"
                group="prayer-list-items"
                itemKey="name"
                @change="changeInProgress"
            >
                <template #item="{ element }">
                    <div class="relative prayer-list-item">
                        <div class="group pb-0 duration-200">
                            <div
                                class="prayer-list-content cursor-move px-3 prose-mirror-render-html"
                                v-html="element.content"
                            ></div>
                            <div class="bottom-10px text-size-17px flex gap-1 duration-300">
                                <NButton size="small" round secondary @click="editPrayerItem(element.key, element.content)">
                                    <template #icon>
                                        <NIcon>
                                            <Edit />
                                        </NIcon>
                                    </template>
                                    <span class="capitalize">{{ $t('edit') }}</span>
                                </NButton>
                                <div>
                                    <NPopconfirm @positive-click="removePrayerItem(element.key)">
                                        <template #trigger>
                                            <NButton size="small" round secondary type="error">
                                                <template #icon>
                                                    <NIcon>
                                                        <TrashCan />
                                                    </NIcon>
                                                </template>
                                                <span class="capitalize">{{ $t('remove') }}</span>
                                            </NButton>
                                        </template>
                                        <span class="capitalize">{{ $t('are you sure to remove this item') }}</span>
                                    </NPopconfirm>
                                </div>
                            </div>
                        </div>
                    </div>
                </template>
            </Draggable>
        </div>
        <div class="w-[100%] h-[100%] flex flex-col">
            <div class="p-10px flex justify-between items-center min-h-60px">
                <span class="font-700 text-size-20px select-none capitalize">{{ $t('done') }} </span>
            </div>
            <Draggable
                class="list-group list-group-done h-[100%] overflow-y-auto overflowing-div pr-10px"
                :list="prayerListStore.donePrayerList"
                v-bind="dragOptions"
                group="prayer-list-items"
                itemKey="name"
                @change="changeInDone"
            >
                <template #item="{ element }">
                    <div class="relative prayer-list-item">
                        <div class="absolute top-10px right-10px text-size-17px flex">
                            <NPopconfirm @positive-click="removePrayerItem(element.key)">
                                <template #trigger>
                                    <NButton size="small" circle type="error" secondary>
                                        <template #icon>
                                            <NIcon>
                                                <TrashCan />
                                            </NIcon>
                                        </template>
                                    </NButton>
                                </template>
                                <span class="capitalize">{{ $t('are you sure to remove this item') }}</span>
                            </NPopconfirm>
                        </div>
                        <div class="prayer-list-content cursor-move prose-mirror-render-html" v-html="element.content"></div>
                    </div>
                </template>
            </Draggable>
        </div>
    </div>
    <EditPrayerItem ref="editPrayerModal" />
</template>

<style lang="postcss">
.prayer-list-item {
    @apply my-10px dark:bg-opacity-50 dark:bg-gray-800 dark:hover:bg-gray-800 bg-gray-300 hover:bg-gray-400 p-10px rounded-md relative overflow-hidden cursor-move;

    .flip-list-move {
        transition: transform 0.5s;
    }
    .no-move {
        transition: transform 0s;
    }
    .ghost {
        opacity: 0.5;
    }
    .list-group {
        min-height: 20px;
    }
}
.prayer-list-page {
    .list-group-done {
        padding: 0 20px;
        opacity: 0.5;
    }
}
</style>
