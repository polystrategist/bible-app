<script lang="ts" setup>
import { ref } from 'vue';
import { useMenuStore } from '../../store/menu';
import Editor from '../../components/Editor/Editor.vue';
import { NAlert, NButton, NIcon, NInput, NSelect } from 'naive-ui';
import { DAYJS } from '../../util/dayjs';
import { useUserStore } from '../../store/userStore';
import { useRouter } from 'vue-router';
import { Close } from '@vicons/carbon';

const router = useRouter();
const userStore = useUserStore();
const menuStore = useMenuStore();
const sermonId = ref(null);
const selectedType = ref('youtube');
const youtubeId = ref(null);
const language = ref('english');
const source = ref(null);
const title = ref(null);
const scripture = ref(null);
const author = ref(null);
const denomination = ref(null);
const description = ref<string>('');
const content = ref('');
const loading = ref(false);
const isPublished = ref(false);

const denominationOptions = [
    { label: 'Adventist' },
    { label: 'Anglican' },
    { label: 'Apostolic' },
    { label: 'Assembly of God' },
    { label: 'Baptist' },
    { label: 'Bible Church' },
    { label: 'Brethren' },
    { label: 'Calvary Chapel' },
    { label: 'Catholic' },
    { label: 'Charismatic' },
    { label: 'Christian Missionary Alliance' },
    { label: 'Christian/Church of Christ' },
    { label: 'Church of God' },
    { label: 'Congregational' },
    { label: 'Disciples of Christ' },
    { label: 'Episcopal' },
    { label: 'Evangelical Free' },
    { label: 'Evangelical/Non-denominational' },
    { label: 'Foursquare' },
    { label: 'Free Methodist' },
    { label: 'Friends' },
    { label: 'Grace Brethren' },
    { label: 'Holiness' },
    { label: 'Independent/Bible' },
    { label: 'Lutheran' },
    { label: 'Mennonite' },
    { label: 'Methodist' },
    { label: 'Nazarene' },
    { label: 'Orthodox' },
    { label: 'Other' },
    { label: 'Pentecostal' },
    { label: 'Presbyterian/Reformed' },
    { label: 'Salvation Army' },
    { label: 'Seventh-Day Adventist' },
    { label: 'United Methodist' },
    { label: 'Vineyard' },
    { label: 'Wesleyan' },
    { label: 'Others' },
];

const getYoutubeVideoDetails = async (
    youtubeVideoId: string | number,
    key = 'AIzaSyB6XTl8aX3Ro3lVKtPbx_2pHyTVU4GAyQM',
    part = 'snippet,contentDetails,statistics,status'
) => {
    return await axios.get('https://www.googleapis.com/youtube/v3/videos', {
        params: {
            key,
            part,
            id: youtubeVideoId,
        },
    });
};

async function submitSermon() {
    alert('Sermon submission is not yet available.');
}

const selectTypeOptions = [
    {
        value: 'youtube',
        label: 'Youtube',
    },
    {
        value: 'text',
        label: 'Text',
    },
];

function resetForm() {
    sermonId.value = null;
    selectedType.value = 'youtube';
    youtubeId.value = null;
    language.value = 'english';
    source.value = null;
    title.value = null;
    scripture.value = null;
    author.value = null;
    denomination.value = null;
    description.value = '';
    content.value = '';
    loading.value = false;
    isPublished.value = false;
}
</script>
<template>
    <div class="h-[100%] w-[100%]">
        <div class="absolute top-5 right-5">
            <NButton size="large" @click="menuStore.setMenu('sermons')" circle secondary>
                <template #icon>
                    <NIcon>
                        <Close />
                    </NIcon>
                </template>
            </NButton>
        </div>
        <div class="w-full mx-auto h-[100%] overflow-auto">
            <div class="w-full max-w-700px mx-auto">
                <div>
                    <h2 class="font-thin text-size-23px mb-0 font-800">Share A Youtube Sermon</h2>
                    <div>
                        Submit your sermon here so that other people can also watch or listen to your sermon.
                    </div>
                </div>
                <div class="mt-10 flex flex-col gap-5">
                    <div>
                        <label for="">Youtube Video ID:</label><br />
                        <NInput v-model:value="youtubeId" placeholder="Enter Youtube Video ID ..." required type="text"
                            class="mb-2" size="large" />
                        <NAlert type="info">
                            The video ID will be located in the URL of the video page, right after the v= URL parameter.
                            In
                            this case, the URL of the video is: https://www.youtube.com/watch?v=aqz-KE-bpKQ. Therefore,
                            the
                            ID of the video is aqz-KE-bpKQ .
                        </NAlert>
                    </div>
                    <div>
                        <label for=""> Select Language: </label><br />
                        <NSelect v-model:value="language" :options="[
                            {
                                label: 'English',
                                value: 'english',
                            },
                            {
                                label: 'Tagalog',
                                value: 'tagalog',
                            },
                        ]" size="large" />
                    </div>
                    <div>
                        <label for="">Enter Source (Optional):</label><br />
                        <NInput v-model="source" placeholder="enter URL" type="text" size="large" />
                    </div>
                    <div>
                        <label class="select-none">
                            <input v-model="isPublished" placeholder="enter URL" type="checkbox" />
                            Is Published?
                        </label>
                    </div>
                    <div class="mb-10">
                        <NButton v-if="userStore.user" :disabled="loading" :loading="loading" type="primary"
                            @click="submitSermon()">
                            Create
                        </NButton>
                        <!-- <NButton v-else :disabled="loading" :loading="loading" type="primary"
                            @click="router.push('/profile')">
                            Login First
                        </NButton> -->
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
