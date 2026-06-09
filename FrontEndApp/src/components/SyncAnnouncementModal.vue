<script lang="ts" setup>
import { NModal, NButton } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { onMounted, ref } from 'vue';
import SESSION from '../util/session';

// One-time announcement shown on app launch: free Sync is ending and Sync is
// now part of a small paid subscription. Bump the key suffix to re-show it after
// a future change. Mirrors the mobile app's announcement so the message is
// consistent everywhere.
const SEEN_KEY = 'sync-paid-announcement-seen-v1';

const show = ref(false);

onMounted(() => {
    if (!SESSION.get(SEEN_KEY)) show.value = true;
});

function acknowledge() {
    SESSION.set(SEEN_KEY, true);
    show.value = false;
}
</script>

<template>
    <NModal
        v-model:show="show"
        preset="card"
        title="A note about Sync"
        :bordered="false"
        :closable="false"
        :mask-closable="false"
        :auto-focus="false"
        style="max-width: 520px; width: 92vw;"
    >
        <div class="sync-note">
            <div class="sync-note__icon">
                <Icon icon="lucide:heart-handshake" />
            </div>
            <p>Grace and peace to you. 🙏</p>
            <p>
                Until now, syncing your notes, highlights, bookmarks, and prayer lists
                across your devices has been free. Keeping those servers running, though,
                carries a monthly cost that I — the developer — can no longer carry alone.
            </p>
            <p>
                So that Believers Sword can keep serving you faithfully, <strong>Sync is
                now part of a small paid subscription</strong>. Everything you do offline
                on this device stays completely free, always.
            </p>
            <p>
                Thank you for your understanding, your patience, and your prayers. May the
                Lord bless you richly as you continue in His Word.
            </p>
        </div>
        <template #footer>
            <div class="sync-note__footer">
                <NButton type="primary" @click="acknowledge">Amen, I understand</NButton>
            </div>
        </template>
    </NModal>
</template>

<style scoped>
.sync-note {
    display: flex;
    flex-direction: column;
    gap: 12px;
    font-size: 14px;
    line-height: 1.6;
}
.sync-note p {
    margin: 0;
}
.sync-note__icon {
    display: grid;
    place-items: center;
    width: 56px;
    height: 56px;
    margin: 0 auto 4px;
    border-radius: 16px;
    font-size: 28px;
    color: var(--primary-color);
    background: color-mix(in srgb, var(--primary-color) 16%, transparent);
}
.sync-note__footer {
    display: flex;
    justify-content: flex-end;
}
</style>
