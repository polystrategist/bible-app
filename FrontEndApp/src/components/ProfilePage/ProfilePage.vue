<script lang="ts" setup>
import { supabase } from '../../util/SupaBase/SupaBase';
import { NButton, NCard, NForm, NFormItem, NInput, useMessage } from 'naive-ui';
import { onMounted, ref } from 'vue';
import SESSION from '../../util/session';
import { useUserStore } from '../../store/userStore';
import { Icon } from '@iconify/vue';

const loading = ref(false);
const userStore = useUserStore();
const message = useMessage();
const props = defineProps(['user_id']);

async function getProfileData() {
    if (userStore.profile_data) return;

    const { data, error } = await supabase.from('profile').select().eq('user_id', props.user_id).single();
    if (error) {
        if (error.code == 'PGRST116') {
            const createProfile = await supabase.from('profile').insert({ user_id: props.user_id }).select().single();
            if (createProfile.error) message.error(createProfile.error.message);
            userStore.profile_data = createProfile.data;
            SESSION.set('profile-data', JSON.parse(JSON.stringify(createProfile.data)));
            return;
        }
        message.error(error.message);
    }
    SESSION.set('profile-data', JSON.parse(JSON.stringify(data)));
    userStore.profile_data = data;
}

async function updateProfile() {
    loading.value = true;
    const { data, error } = await supabase
        .from('profile')
        .update(JSON.parse(JSON.stringify(userStore.profile_data)))
        .eq('user_id', props.user_id)
        .select()
        .single();
    loading.value = false;

    if (error) message.error(error.message);
    
    message.success('Profile Updated!');
    userStore.profile_data = data;
}

onMounted(() => getProfileData());
</script>
<template>
    <div>
        <NCard size="small">
            <NForm v-if="userStore.profile_data" :disabled="loading" @keypress.enter="updateProfile">
                <h3 class="text-lg flex gap-2 items-center mb-2 font-700">
                    <Icon icon="mdi:account-circle" />
                    <span>Profile</span>
                </h3>
                <NFormItem label="Username">
                    <NInput v-model:value="userStore.profile_data.username"  placeholder="ex. brojenuel" />
                </NFormItem>
                <NFormItem label="About">
                    <NInput v-model:value="userStore.profile_data.about" type="textarea" placeholder="Introduce yourself" />
                </NFormItem>
                <NFormItem label="First Name">
                    <NInput v-model:value="userStore.profile_data.first_name" placeholder="ex. John" />
                </NFormItem>
                <NFormItem label="Last Name">
                    <NInput v-model:value="userStore.profile_data.last_name" placeholder="ex. Delacruz" />
                </NFormItem>

                <h3 class="text-lg flex gap-2 items-center mb-2 font-700">
                    <Icon icon="mdi:account-group" />
                    <span>Social</span>
                </h3>
                <NFormItem label="Facebook Url">
                    <NInput
                        v-model:value="userStore.profile_data.facebook_url"
                        placeholder="ex. https://www.facebook.com/brojenuel"
                    />
                </NFormItem>
                <NFormItem label="Instagram Url">
                    <NInput
                        v-model:value="userStore.profile_data.instagram_url"
                        placeholder="ex. https://www.instagram.com/brojenuel"
                    />
                </NFormItem>
                <NFormItem label="Tiktok Url">
                    <NInput
                        v-model:value="userStore.profile_data.tiktok_url"
                        placeholder="ex. https://www.tiktok.com/@brojenuel"
                    />
                </NFormItem>
                <NFormItem label="Twitter Url">
                    <NInput
                        v-model:value="userStore.profile_data.twitter_url"
                        placeholder="ex. https://www.twitter.com/brojenuel"
                    />
                </NFormItem>
                <NButton type="primary" @click="updateProfile" :disabled="loading" :loading="loading">
                    <template #icon>
                        <Icon icon="mdi:content-save" />
                    </template>
                    Save
                </NButton>
            </NForm>
        </NCard>
    </div>
</template>
