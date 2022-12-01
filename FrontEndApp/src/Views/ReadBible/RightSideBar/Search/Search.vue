<script lang="ts" setup>
import RightSideBarContainer from './../../../../components/ReadBible/RightSideBarContainer.vue';
import { NInput, NForm, NButton, NPopselect, useMessage } from 'naive-ui';
import { ref, computed } from 'vue';
import { useBibleStore } from '../../../../store/BibleStore';
import { bibleBooks } from '../../books';

const bibleStore = useBibleStore();
const page = ref<number>(1);
const search = ref<null | string>(null);
const searchedVerses: any = ref([]);
const limit = ref(20);
const selectedBookNumber = ref<null | number>(null);
const message = useMessage();

async function submitSearch() {
    if (!search.value || search.value.replace(/^\s+|\s+$/gm, '') == '') {
        message.warning('Please Enter What your looking for 😁');
        return;
    }

    const arg = {
        search: search.value,
        bible_versions: bibleStore.selectedBibleVersions,
        page: page.value,
        limit: limit.value,
        book_number: selectedBookNumber.value,
    };
    const data = await window.browserWindow.searchBible(JSON.stringify(arg));
    searchedVerses.value = data;
}

function getBookShortName(book_number: number) {
    return bibleBooks[bibleBooks.findIndex((book) => book.book_number == book_number)];
}

const selectBookOptions = computed(() => {
    let books = bibleBooks.map((b) => ({
        label: b.title,
        value: b.book_number,
    }));
    books.unshift({
        label: 'All',
        value: 0,
    });
    return books;
});
</script>
<template>
    <RightSideBarContainer title="Search Bible">
        <div class="h-full flex flex-col">
            <div class="h-65px">
                <NForm @submit.prevent="submitSearch">
                    <NInput v-model:value="search" size="small" clearable />
                    <NPopselect
                        size="small"
                        v-model:value="selectedBookNumber"
                        :options="selectBookOptions"
                        scrollable
                        :on-update:value="
                            (value) => {
                                selectedBookNumber = value;
                                if (search) {
                                    submitSearch();
                                }
                            }
                        "
                    >
                        <NButton class="w-full mt-1" size="small">{{
                            [null, 0].includes(selectedBookNumber)
                                ? 'All'
                                : selectBookOptions[selectBookOptions.findIndex(({ value }) => value == selectedBookNumber)].label
                        }}</NButton>
                    </NPopselect>
                </NForm>
            </div>
            <div class="h-[calc(100%-85px)] overflow-y-auto overflowing-div flex flex-col gap-15px show-chapter-verses">
                <div
                    v-for="verse in searchedVerses"
                    class="p-1 hover:bg-light-100 hover:bg-opacity-5 rounded-sm"
                    @click="bibleStore.selectVerse(verse.book_number, verse.chapter, verse.verse)"
                >
                    <div class="font-700">
                        {{ getBookShortName(verse.book_number).short_name }} {{ verse.chapter }}:{{ verse.verse }}
                    </div>
                    <div>
                        <div v-for="version in verse.version">
                            <span class="mr-7px text-[var(--primary-color)] italic">{{ version.version }}</span>
                            <div v-html="version.text"></div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="flex justify-between px-10px select-none">
                <div>
                    <span
                        v-show="page > 1"
                        class="cursor-pointer hover:text-[var(--primary-color)]"
                        @click="
                            page--;
                            submitSearch();
                        "
                    >
                        Before
                    </span>
                </div>
                <div>
                    <span
                        v-show="searchedVerses.length == limit"
                        class="cursor-pointer hover:text-[var(--primary-color)]"
                        @click="
                            page++;
                            submitSearch();
                        "
                    >
                        Next
                    </span>
                </div>
            </div>
        </div>
    </RightSideBarContainer>
</template>
