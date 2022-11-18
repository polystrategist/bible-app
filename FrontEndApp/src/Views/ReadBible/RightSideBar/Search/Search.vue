<script lang="ts" setup>
import RightSideBarContainer from './../../../../components/ReadBible/RightSideBarContainer.vue';
import { NInput, NForm } from 'naive-ui';
import { ref } from 'vue';
import { useBibleStore } from '../../../../store/BibleStore';
import { bibleBooks } from '../../books';

const bibleStore = useBibleStore();
const page = ref<number>(1);
const search = ref(null);
const searchedVerses: any = ref([]);

async function submitSearch() {
    const arg = {
        search: search.value,
        bible_versions: bibleStore.selectedBibleVersions,
        page: page.value,
        limit: 99,
    };
    const data = await window.browserWindow.searchBible(JSON.stringify(arg));
    searchedVerses.value = data;
    console.log(searchedVerses.value);
}

function getBookShortName(book_number: number) {
    return bibleBooks[bibleBooks.findIndex((book) => book.book_number == book_number)];
}
</script>
<template>
    <RightSideBarContainer title="Search Bible">
        <div class="h-35px">
            <NForm @submit.prevent="submitSearch">
                <NInput v-model:value="search" size="small" />
            </NForm>
        </div>
        <div class="h-[calc(100%-55px)] overflow-y-auto overflowing-div flex flex-col gap-10px show-chapter-verses">
            <div v-for="verse in searchedVerses">
                <div>{{ getBookShortName(verse.book_number).short_name }} {{ verse.chapter }}:{{ verse.verse }}</div>
                <div>
                    <div v-for="version in verse.version">
                        <span class="mr-7px">{{ version.version }}</span>
                        <div v-html="version.text"></div>
                    </div>
                </div>
            </div>
        </div>
        <div class="flex justify-between h-[20px] px-10px select-none">
            <div class="cursor-pointer hover:text-[var(--primary-color)]">Before</div>
            <div class="cursor-pointer hover:text-[var(--primary-color)]">Next</div>
        </div>
    </RightSideBarContainer>
</template>
