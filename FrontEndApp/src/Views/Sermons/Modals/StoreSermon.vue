<script lang='ts' setup>
import { NModal, NCard } from "naive-ui"
import { ref } from 'vue';

const showModal = ref(false)

</script>

<template>
    <NModal v-model:show='showModal'>
        <NCard>
            lorem
        </NCard>
    </NModal>
</template>