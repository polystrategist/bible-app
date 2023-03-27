<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { isSignedIn } from './../../util/SupaBase/Auth/Auth';
import { useMenuStore } from '../../store/menu';

const loginModalRef = ref<{
    toggleModal: Function;
} | null>(null);
const menuStore = useMenuStore();
const user = ref<any>(null);
const loading = ref(false);

async function isUserAlreadySignedIn() {
    loading.value = true;
    const userData = await isSignedIn();
    if (userData) user.value = userData;
    else {
        if (loginModalRef.value) loginModalRef.value.toggleModal();
    }
    loading.value = false;
}

watch(
    () => menuStore.menuSelected,
    (selectedMenu) => {
        console.log(selectedMenu);
        if (selectedMenu === '/profile') isUserAlreadySignedIn();
    }
);
</script>
<template>
    <div class="h-100% w-100% p-2">
        <RouterView />
    </div>
</template>
