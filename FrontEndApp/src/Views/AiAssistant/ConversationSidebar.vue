<script lang="ts" setup>
import { ref, nextTick, h } from 'vue';
import { NButton, NDropdown, NInput, NTooltip, useDialog } from 'naive-ui';
import { Icon } from '@iconify/vue';
import type { ConversationMeta } from '../../store/conversationStore';

defineProps<{
    conversations: ConversationMeta[];
    activeId: string | null;
}>();

const emit = defineEmits<{
    (e: 'new'): void;
    (e: 'select', id: string): void;
    (e: 'rename', payload: { id: string; title: string }): void;
    (e: 'delete', id: string): void;
    (e: 'collapse'): void;
}>();

const dialog = useDialog();
const editingId = ref<string | null>(null);
const editText = ref('');
const editInput = ref<InstanceType<typeof NInput> | null>(null);

const rowMenu = [
    { key: 'rename', label: 'Rename', icon: () => iconNode('lucide:pencil') },
    { key: 'delete', label: 'Delete', icon: () => iconNode('lucide:trash-2') },
];

function iconNode(icon: string) {
    return h(Icon, { icon });
}

function startRename(c: ConversationMeta) {
    editingId.value = c.id;
    editText.value = c.title;
    nextTick(() => editInput.value?.focus());
}

function commitRename(c: ConversationMeta) {
    const title = editText.value.trim();
    if (title && title !== c.title) emit('rename', { id: c.id, title });
    editingId.value = null;
}

function confirmDelete(c: ConversationMeta) {
    dialog.warning({
        title: 'Delete conversation',
        content: `Delete “${c.title}”? This can't be undone.`,
        positiveText: 'Delete',
        negativeText: 'Cancel',
        onPositiveClick: () => emit('delete', c.id),
    });
}

function onMenu(key: string, c: ConversationMeta) {
    if (key === 'rename') startRename(c);
    else if (key === 'delete') confirmDelete(c);
}

function relativeTime(iso: string): string {
    const then = new Date(iso).getTime();
    if (Number.isNaN(then)) return '';
    const mins = Math.round((Date.now() - then) / 60000);
    if (mins < 1) return 'just now';
    if (mins < 60) return `${mins}m ago`;
    const hrs = Math.round(mins / 60);
    if (hrs < 24) return `${hrs}h ago`;
    const days = Math.round(hrs / 24);
    if (days < 7) return `${days}d ago`;
    return new Date(iso).toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
}
</script>

<template>
    <aside class="sidebar">
        <div class="sidebar__top">
            <NTooltip trigger="hover">
                <template #trigger>
                    <NButton quaternary circle size="small" @click="emit('collapse')">
                        <template #icon><Icon icon="lucide:panel-left-close" /></template>
                    </NButton>
                </template>
                Hide conversations
            </NTooltip>
            <NButton class="new-btn" secondary @click="emit('new')">
                <template #icon><Icon icon="lucide:plus" /></template>
                New chat
            </NButton>
        </div>

        <div class="sidebar__list">
            <p v-if="conversations.length === 0" class="sidebar__empty">
                No saved conversations yet.
            </p>

            <div
                v-for="c in conversations"
                :key="c.id"
                class="convo"
                :class="{ 'convo--active': c.id === activeId }"
                @click="editingId === c.id ? null : emit('select', c.id)"
            >
                <Icon icon="lucide:message-square" class="convo__icon" />

                <NInput
                    v-if="editingId === c.id"
                    ref="editInput"
                    v-model:value="editText"
                    size="tiny"
                    class="convo__edit"
                    @blur="commitRename(c)"
                    @keyup.enter="commitRename(c)"
                    @click.stop
                />
                <template v-else>
                    <div class="convo__meta">
                        <div class="convo__title">{{ c.title }}</div>
                        <div class="convo__time">{{ relativeTime(c.updated_at) }}</div>
                    </div>
                    <NDropdown
                        trigger="click"
                        :options="rowMenu"
                        @select="(k: string) => onMenu(k, c)"
                    >
                        <button class="convo__more" @click.stop>
                            <Icon icon="lucide:more-horizontal" />
                        </button>
                    </NDropdown>
                </template>
            </div>
        </div>
    </aside>
</template>

<style scoped>
.sidebar {
    width: 260px;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    border-right: 1px solid var(--theme-border);
    background: var(--theme-bg-soft);
    height: 100%;
}
.sidebar__top {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px;
}
.new-btn { flex: 1; justify-content: center; }

.sidebar__list {
    flex: 1;
    overflow-y: auto;
    padding: 4px 8px;
}
.sidebar__empty {
    text-align: center;
    font-size: 12.5px;
    opacity: 0.55;
    margin-top: 24px;
}

.convo {
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 9px 10px;
    border-radius: 10px;
    cursor: pointer;
    transition: background 0.12s;
}
.convo:hover { background: var(--theme-bg-elevated); }
.convo--active { background: color-mix(in srgb, var(--primary-color) 16%, transparent); }
.convo__icon { flex-shrink: 0; font-size: 16px; opacity: 0.7; }
.convo__meta { flex: 1; min-width: 0; }
.convo__title {
    font-size: 13.5px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.convo__time { font-size: 11px; opacity: 0.5; margin-top: 1px; }
.convo__edit { flex: 1; }
.convo__more {
    flex-shrink: 0;
    display: grid;
    place-items: center;
    width: 24px; height: 24px;
    border: none;
    background: transparent;
    color: inherit;
    border-radius: 6px;
    cursor: pointer;
    opacity: 0;
    transition: opacity 0.12s, background 0.12s;
}
.convo:hover .convo__more { opacity: 0.7; }
.convo__more:hover { background: var(--theme-bg-soft); opacity: 1; }
</style>
