<script lang="ts" setup>
import { ref, computed, h } from 'vue';
import { NButton, NModal, NIcon, NCard, NInput, NSelect, NCheckbox, useMessage } from 'naive-ui';
import { Save } from '@vicons/carbon';
import { Icon } from '@iconify/vue';
import Editor from '../../components/Editor/Editor.vue';
import { usePrayerListStore } from '../../store/prayerListStore';
import { PREDEFINED_GROUPS, groupStyle } from './prayerGroupStyle';
function renderGroupLabel(option: { label?: string; value?: string | number }) {
    const s = groupStyle(String(option.value ?? ''));
    return h('div', { style: 'display:flex;align-items:center;gap:8px;' }, [
        h(Icon, { icon: s.icon, style: `color:${s.color};font-size:16px;` }),
        h('span', String(option.label ?? '')),
    ]);
}

const keyOfItem = ref('');
const prayerTitle = ref('');
const prayerGroup = ref<string | null>('');
const prayerItemContent = ref('');
const isAnswered = ref(false);
const prayerListStore = usePrayerListStore();
const showModal = ref(false);
const message = useMessage();

// Include the current value when it's a custom group not in the presets, so it
// (and its icon) still renders in the select.
const groupOptions = computed(() => {
    const opts = PREDEFINED_GROUPS.map((g) => ({ label: g, value: g }));
    const cur = prayerGroup.value?.trim();
    if (cur && !PREDEFINED_GROUPS.some((g) => g.toLowerCase() === cur.toLowerCase())) {
        opts.unshift({ label: cur, value: cur });
    }
    return opts;
});

const SaveEditorContent = () => {
    try {
        prayerListStore.savePrayerItem(
            {
                title: prayerTitle.value.trim() || null,
                content: prayerItemContent.value,
                group: prayerGroup.value?.trim() || null,
                status: isAnswered.value ? 'done' : 'ongoing',
            },
            keyOfItem.value
        );
        showModal.value = false;
    } catch (e) {
        if (e instanceof Error) message.error(e.message);
    }
};

function modalTrigger(item: {
    key: string;
    title?: string | null;
    content?: string;
    group?: string | null;
    status?: string | null;
}) {
    keyOfItem.value = item.key;
    prayerTitle.value = item.title ?? '';
    prayerGroup.value = item.group ?? '';
    prayerItemContent.value = item.content ?? '';
    isAnswered.value = item.status === 'done';
    showModal.value = true;
}

defineExpose({ modalTrigger });
</script>

<template>
    <NModal v-model:show="showModal">
        <NCard class="max-w-500px my-20px" size="small">
            <template #header>
                <span class="capitalize">{{ $t('edit') }}</span>
            </template>

            <div class="flex flex-col gap-12px mb-16px">
                <div class="flex flex-col gap-4px">
                    <label class="text-12px font-600 opacity-70">Title</label>
                    <NInput v-model:value="prayerTitle" placeholder="Enter prayer title..." />
                </div>
                <div class="flex flex-col gap-4px">
                    <label class="text-12px font-600 opacity-70">Group</label>
                    <NSelect
                        v-model:value="prayerGroup"
                        :options="groupOptions"
                        :render-label="renderGroupLabel"
                        filterable
                        tag
                        clearable
                        placeholder="Select or type a group…"
                    />
                </div>
                <NCheckbox v-model:checked="isAnswered">
                    Mark as answered
                </NCheckbox>
                <div class="flex flex-col gap-4px">
                    <label class="text-12px font-600 opacity-70">Content</label>
                    <Editor
                        v-model="prayerItemContent"
                        :button-actions="['bold', 'italic', 'underline', 'strike', 'bulletList', 'orderedList', 'clearFormat']"
                    />
                </div>
            </div>

            <div class="p-10px flex flex-row justify-end gap-15px">
                <NButton class="flex-grow" type="info" @click="SaveEditorContent()">
                    <template #icon>
                        <NIcon><Save /></NIcon>
                    </template>
                    <span class="capitalize">{{ $t('save changes') }}</span>
                </NButton>
                <NButton ghost @click="showModal = false">
                    <span class="capitalize">{{ $t('cancel') }}</span>
                </NButton>
            </div>
        </NCard>
    </NModal>
</template>
