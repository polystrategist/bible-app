<script setup lang="ts">
defineProps({
    title: {
        type: String,
    },
});
</script>
<template>
    <div class="w-full h-full">
        <h1 class="font-700 h-30px select-none">{{ $props.title }}</h1>
        <div class="w-full h-[calc(100%-30px)] overflow-auto overflowing-div">
            <slot />
        </div>
    </div>
</template>
