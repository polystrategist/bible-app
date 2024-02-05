<script lang="ts" setup>
import { ref } from 'vue';
import { NIcon, NButton, useMessage, NDropdown, useDialog } from 'naive-ui';
import EditPrayerItem from './EditPrayerItem.vue';
import { Edit, TrashCan, OverflowMenuVertical } from '@vicons/carbon';
import Draggable from 'vuedraggable';
import { usePrayerListStore } from '../../store/prayerListStore';
import NewPrayerItem from './CreateNewPrayerItem.vue';
import type { Component } from 'vue';
import { h } from 'vue';
import { useI18n } from 'vue-i18n';

const message = useMessage();
const prayerListStore = usePrayerListStore();
const editPrayerModal = ref<any>(null);
const dialog = useDialog();
const { t } = useI18n();

const renderIcon = (icon: Component) => {
    return () => {
        return h(NIcon, null, {
            default: () => h(icon),
        });
    };
};

const removePrayerItem = (key: string) => {
    try {
        prayerListStore.removePrayerItem(key);
    } catch (e) {
        if (e instanceof Error) message.error(e.message);
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

function selectItemFromMenuElement(key: any, element: any) {
    if (key === 'edit') editPrayerItem(element.key, element.content);
    else if (key === 'remove') {
        dialog.warning({
            title: t('Confirm'),
            content: t('Are You Sure You want to remove?'),
            positiveText: t('Yes'),
            negativeText: t('No'),
            onPositiveClick: () => {
                removePrayerItem(element.key);
            },
        });
    }
}
</script>
<template>
    <div
        class="prayer-list-page px-10px h-[100%] overflow-y-auto overflowing-div scroll-bar-sm flex gap-10px pl-30px bg-dark-800"
    >
        <div class="w-full max-w-250px h-[100%] flex flex-col">
            <div class="p-10px flex justify-between items-end select-none min-h-60px">
                <span class="font-700 capitalize">{{ $t('prayer list') }}</span>
                <NewPrayerItem />
            </div>
            <Draggable
                class="list-group h-[100%] overflow-y-auto overflowing-div bg-dark-900 p-2"
                :list="prayerListStore.prayerList"
                v-bind="dragOptions"
                group="prayer-list-items"
                itemKey="name"
                @change="changeInProgress"
            >
                <template #item="{ element }">
                    <div class="relative prayer-list-item group">
                        <div class="pb-0 duration-200">
                            <div
                                class="prayer-list-content cursor-move prose-mirror-render-html !pt-1 px-1"
                                v-html="element.content"
                            ></div>
                            <NDropdown
                                trigger="click"
                                :options="[
                                    {
                                        label: $t('edit'),
                                        key: 'edit',
                                        icon: renderIcon(Edit),
                                    },
                                    {
                                        label: $t('remove'),
                                        key: 'remove',
                                        icon: renderIcon(TrashCan),
                                    },
                                ]"
                                @select="(key: string) => selectItemFromMenuElement(key, element)"
                            >
                                <NButton type="primary" size="tiny" class="absolute top-1 right-1 invisible group-hover:visible">
                                    <template #icon>
                                        <NIcon>
                                            <OverflowMenuVertical />
                                        </NIcon>
                                    </template>
                                </NButton>
                            </NDropdown>
                        </div>
                    </div>
                </template>
            </Draggable>
        </div>
        <div class="w-full max-w-250px h-[100%] flex flex-col">
            <div class="p-10px flex justify-between items-end min-h-60px">
                <span class="font-700 select-none capitalize">{{ $t('done') }} </span>
            </div>
            <Draggable
                class="list-group list-group-done h-[100%] overflow-y-auto overflowing-div bg-dark-900 p-2"
                :list="prayerListStore.donePrayerList"
                v-bind="dragOptions"
                group="prayer-list-items"
                itemKey="name"
                @change="changeInDone"
            >
                <template #item="{ element }">
                    <div class="group relative prayer-list-item">
                        <div
                            class="prayer-list-content cursor-move prose-mirror-render-html !pt-1 px-1"
                            v-html="element.content"
                        ></div>
                        <NDropdown
                            trigger="click"
                            :options="[
                                {
                                    label: $t('edit'),
                                    key: 'edit',
                                    icon: renderIcon(Edit),
                                },
                                {
                                    label: $t('remove'),
                                    key: 'remove',
                                    icon: renderIcon(TrashCan),
                                },
                            ]"
                            @select="(key: string) => selectItemFromMenuElement(key, element)"
                        >
                            <NButton type="primary" size="tiny" class="absolute top-1 right-1 invisible group-hover:visible">
                                <template #icon>
                                    <NIcon>
                                        <OverflowMenuVertical />
                                    </NIcon>
                                </template>
                            </NButton>
                        </NDropdown>
                    </div>
                </template>
            </Draggable>
        </div>
    </div>
    <EditPrayerItem ref="editPrayerModal" />
</template>

<style lang="scss">
.prayer-list-item {
    @apply dark:bg-opacity-50 dark:bg-gray-800 dark:hover:bg-gray-800 bg-gray-300 hover:bg-gray-400 rounded-md relative overflow-hidden cursor-move mb-2 p-1;

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
</style>
