<script setup lang="ts">
import { Button } from "@/components/ui/button";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ref } from "vue";

const showModal = ref(false);

defineProps<{
    title: string;
    description?: string;
}>();

defineExpose({
    toggleModal: () => {
        showModal.value = !showModal.value;
    },
});
</script>

<template>
    <Dialog v-model:open="showModal">
        <DialogContent class="sm:max-w-[425px]">
            <DialogHeader>
                <DialogTitle>{{ title }}</DialogTitle>
                <DialogDescription v-if="description">
                    {{ description }}
                </DialogDescription>
            </DialogHeader>
            <slot name="dialog-content" />
            <DialogFooter>
                <slot name="dialog-footer" />
            </DialogFooter>
        </DialogContent>
    </Dialog>
</template>
