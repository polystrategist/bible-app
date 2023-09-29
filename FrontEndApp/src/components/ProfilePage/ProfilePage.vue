<script lang='ts' setup>
import { supabase } from '../../util/SupaBase/SupaBase';
import { useMessage } from 'naive-ui';
import { onMounted, ref } from 'vue';
import SESSION from '../../util/session';
import { useUserStore } from '../../store/userStore';

const userStore = useUserStore();
const message = useMessage();
const props = defineProps(['user_id']);

async function getProfileData() {
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

onMounted(() => getProfileData());
</script>
<template>
    <div>
        <div class='flex gap-10px'>
            <img class='rounded-full h-100px w-100px'
                 height='100'
                 src='https://images.ctfassets.net/h6goo9gw1hh6/2sNZtFAWOdP1lmQ33VwRN3/24e953b920a9cd0ff2e1d587742a2472/1-intro-photo-final.jpg?w=1200&h=992&fl=progressive&q=70&fm=jpg' width='100' />
            <div class='profile-image'>
                <div>@Brian936</div>
                <div class='opacity-70'>"Life is all about this"</div>
                <div>lorem ipsom dolor sit amet lorem ipsom dolor sit amet lorem ipsom dolor sit amet lorem ipsom dolor sit amet</div>
            </div>
        </div>
    </div>
</template>
