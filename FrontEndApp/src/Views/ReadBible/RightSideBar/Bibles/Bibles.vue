<script setup lang="ts">
import { onBeforeMount, ref } from 'vue';
import { getDownloadedBible } from '../../../../util/Modules/Controller/FeBibleController';
import { NCheckbox } from 'naive-ui';

const bibleLists = ref<Array<any>>([]);

async function getBibleLists() {
    bibleLists.value = await getDownloadedBible();
}

onBeforeMount(() => {
    getBibleLists();
});
</script>
<template>
    <div class="w-full overflowing-div">
        <h1 class="font-700">Bibles</h1>
        <NCheckbox v-for="bible in bibleLists" class="w-full">
            <span class="truncate">{{ bible.title }}</span>
        </NCheckbox>
    </div>
</template>
