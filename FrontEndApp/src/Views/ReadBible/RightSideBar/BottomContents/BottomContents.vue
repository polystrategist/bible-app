<script setup lang="ts">
import Dictionary from './Dictionary/Dictionary.vue';
import Reference from './Reference/Reference.vue';

const props = defineProps<{
    selectedMenuKey?: string | null;
}>();
</script>
<template>
    <div class="h-full">
        <Reference v-show="props.selectedMenuKey == 'references'" />
        <Dictionary v-show="props.selectedMenuKey == 'dictionary'" />
    </div>
</template>
