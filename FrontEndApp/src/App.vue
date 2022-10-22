<script setup lang="ts">
import ReadBible from "./Views/ReadBible/ReadBible.vue";
import { useMenuStore } from "./store/menu";
const menuStore = useMenuStore();
</script>
<template>
    <div>
        <ul>
            <li @click="menuStore.setMenu('read-bible')">Read Bible</li>
            <li @click="menuStore.setMenu('/prayer-list')">Prayer List</li>
        </ul>
        <div>
            <pre>{{ menuStore.isRouter }}</pre>
            <ReadBible v-show="menuStore.isRouter == false && menuStore.menuSelected == 'read-bible'" />
            <div v-show="menuStore.isRouter == true">
                <RouterView />
            </div>
        </div>
    </div>
</template>
