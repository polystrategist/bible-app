<script setup lang="ts">
defineProps({
    title: {
        type: String,
    },
});
</script>
<template>
    <div class="w-full h-full">
        <div class="h-30px select-none flex justify-between">
            <h1 class="font-700">{{ $props.title }}</h1>
            <slot name="rightSide">
                <div></div>
            </slot>
        </div>
        <div class="w-full h-[calc(100%-30px)] overflow-auto overflowing-div">
            <slot />
        </div>
    </div>
</template>
