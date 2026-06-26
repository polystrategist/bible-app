<script lang="ts" setup>
import { NModal } from 'naive-ui';
import { computed } from 'vue';
import { useKeyboardShortcutsModalStore } from '../store/keyboardShortcutsModalStore';

// Global Keyboard Shortcuts dialog (mounted once in App.vue, opened from the Help menu).
const shortcutsModal = useKeyboardShortcutsModalStore();

const open = computed({
    get: () => shortcutsModal.open,
    set: (v: boolean) => (v ? shortcutsModal.show() : shortcutsModal.hide()),
});

// On macOS the dual-modifier shortcuts respond to ⌘; everywhere else it's Ctrl.
const isMac = /Mac|iPod|iPhone|iPad/.test(navigator.platform);
const mod = isMac ? '⌘' : 'Ctrl';

type Shortcut = { keys: string[]; label: string };
type Group = { title: string; items: Shortcut[] };

const groups = computed<Group[]>(() => [
    {
        title: 'Reading',
        items: [
            { keys: [mod, 'F'], label: 'Open the verse / chapter selector' },
            { keys: [mod, 'S'], label: 'Focus the search bar' },
            { keys: ['Ctrl', 'Scroll'], label: 'Increase or decrease font size' },
            { keys: ['Esc'], label: 'Clear the current verse selection' },
            { keys: [mod, 'Click'], label: 'Add or remove a verse from the selection' },
            { keys: ['Shift', 'Click'], label: 'Select a range of verses' },
        ],
    },
    {
        title: 'View',
        items: [
            { keys: ['Ctrl', 'Shift', 'N'], label: 'Toggle the Notes panel' },
            { keys: ['Ctrl', 'Shift', '+'], label: 'Increase app scale (zoom in)' },
            { keys: ['Ctrl', 'Shift', '−'], label: 'Decrease app scale (zoom out)' },
        ],
    },
    {
        title: 'Reading Mode (Flipbook)',
        items: [
            { keys: ['→', '↓'], label: 'Next page' },
            { keys: ['←', '↑'], label: 'Previous page' },
            { keys: ['Esc'], label: 'Close reading mode' },
        ],
    },
]);
</script>

<template>
    <NModal
        v-model:show="open"
        preset="card"
        title="Keyboard Shortcuts"
        :bordered="false"
        :auto-focus="false"
        style="max-width: 520px; width: 92vw;"
    >
        <div class="ks">
            <div v-for="group in groups" :key="group.title" class="ks__group">
                <div class="ks__group-title">{{ group.title }}</div>
                <div
                    v-for="(item, i) in group.items"
                    :key="i"
                    class="ks__row"
                >
                    <span class="ks__label">{{ item.label }}</span>
                    <span class="ks__keys">
                        <template v-for="(key, ki) in item.keys" :key="ki">
                            <span v-if="ki > 0" class="ks__plus">+</span>
                            <kbd class="ks__kbd">{{ key }}</kbd>
                        </template>
                    </span>
                </div>
            </div>
        </div>
    </NModal>
</template>

<style scoped>
.ks {
    display: flex;
    flex-direction: column;
    gap: 18px;
}
.ks__group {
    display: flex;
    flex-direction: column;
    gap: 4px;
}
.ks__group-title {
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    opacity: 0.55;
    margin-bottom: 4px;
}
.ks__row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding: 6px 0;
    border-bottom: 1px solid rgba(128, 128, 128, 0.12);
}
.ks__row:last-child {
    border-bottom: none;
}
.ks__label {
    font-size: 13px;
    line-height: 1.4;
}
.ks__keys {
    display: flex;
    align-items: center;
    gap: 4px;
    flex-shrink: 0;
}
.ks__plus {
    font-size: 11px;
    opacity: 0.5;
}
.ks__kbd {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 22px;
    height: 24px;
    padding: 0 7px;
    font-size: 12px;
    font-family: inherit;
    font-weight: 600;
    line-height: 1;
    border-radius: 6px;
    border: 1px solid rgba(128, 128, 128, 0.3);
    border-bottom-width: 2px;
    background: rgba(128, 128, 128, 0.08);
    white-space: nowrap;
}
:global(.dark) .ks__kbd {
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(255, 255, 255, 0.18);
}
</style>
