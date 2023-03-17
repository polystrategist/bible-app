<script lang="ts" setup>
import { NModal, NCard } from 'naive-ui';
import { ref } from 'vue';

// const props = defineEmits(['logged']);
const showModal = ref(false);

function toggleModal() {
    showModal.value = !showModal.value;
}

defineExpose({
    toggleModal,
});
</script>
<template>
    <NModal v-model:show="showModal">
        <NCard class="max-w-500px">
            Lorem ipsum dolor sit, amet consectetur adipisicing elit. Aut tenetur aspernatur iusto recusandae, pariatur
            praesentium alias in magnam sed. Itaque ducimus doloribus fugit sit ab est inventore corporis voluptates incidunt!
        </NCard>
    </NModal>
</template>
