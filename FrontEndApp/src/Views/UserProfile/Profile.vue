<script setup lang="ts">
import { Block } from 'notiflix';
import { NInput } from 'naive-ui';
import { ref, watch, onMounted } from 'vue';
import { isSignedIn } from './../../util/SupaBase/Auth/Auth';
import { useMenuStore } from '../../store/menu';
import Login from './Modal/Login.vue';

const loginModalRef = ref<{
    toggleModal: Function;
} | null>(null);
const menuStore = useMenuStore();
const user = ref<any>(null);
const loading = ref(false);
const fullName = ref<string | null>(null);
const aboutYourSelf = ref<string | null>(null);

async function isUserAlreadySignedIn() {
    loading.value = true;
    const userData = await isSignedIn();
    if (userData) user.value = userData;
    else {
        if (loginModalRef.value) loginModalRef.value.toggleModal();
    }
    loading.value = false;
}

onMounted(() => {
    if (menuStore.menuSelected === '/profile') isUserAlreadySignedIn();
});

watch(
    () => loading.value,
    (val) => {
        if (val) Block.standard('#profile-page');
        else Block.remove('#profile-page');
    }
);
</script>
<template>
    <Login ref="loginModalRef" />
    <div id="profile-page" class="w-full h-full p-5">
        <div class="max-w-400px flex flex-col gap-3">
            <div>
                <label>Your Full Name</label>
                <NInput v-model:value="fullName" />
            </div>
            <div>
                <label>About Your Self</label>
                <NInput v-model:value="aboutYourSelf" type="textarea" :autosize="false" />
            </div>
        </div>
    </div>
</template>
