<script lang='ts' setup>
import { ref } from 'vue';
import axios from 'axios';
import { supabase } from '../../util/SupaBase/SupaBase';
import { useMenuStore } from '../../store/menu';
import Editor from '../../components/Editor/Editor.vue';
import { NButton, NInput, NSelect } from 'naive-ui';
import { DAYJS } from '../../util/dayjs';
import { useUserStore } from '../../store/userStore';
import { useRouter } from 'vue-router';

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
    { label: 'Others' }
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
            id: youtubeVideoId
        }
    });
};

async function submitSermon() {
    loading.value = true;
    const session = await supabase.auth.getSession();
    if (selectedType.value == 'youtube') {
        if (!youtubeId.value || !source.value) {
            alert('please check fields!');
            loading.value = false;
            return;
        }
        // get data from api
        getYoutubeVideoDetails(youtubeId.value as any)
            .then(async ({ data }) => {
                if (!data || !data.items) {
                    alert('Fetching Video Details Error');
                    loading.value = false;
                    return;
                }


                const youtubeDetails = data.items[0];
                let dataToEnter = {
                    type: 'youtube',
                    thumbnail: youtubeDetails.snippet.thumbnails.medium.url,
                    // date_time: new Date(),
                    description: youtubeDetails.snippet.description,
                    title: youtubeDetails.snippet.title,
                    youtube_embed: `https://www.youtube.com/embed/${youtubeDetails.id}`,
                    youtube_video_id: youtubeDetails.id,
                    language: language.value,
                    source: source.value,
                    added_by: session.data.session?.user.id,
                    is_published: isPublished.value
                };
                const { error } = sermonId.value
                    ? await supabase.from('sermons').update(dataToEnter).match({ id: sermonId.value })
                    : await supabase.from('sermons').insert(dataToEnter);

                if (error) {
                    alert(error.message);
                    loading.value = false;
                    return;
                }

                resetForm();
                alert('Data Successfully Added!');
                await menuStore.setMenu('sermons');
            })
            .catch((e) => {
                let message =
                    e.response && e.response.data && e.response.data.error && e.response.data.error.message
                        ? e.response.data.error.message
                        : 'Their is an Error Getting Youtube Details!';
                alert(message);
            });
    } else if (selectedType.value == 'text') {
        let dataToInsert = {
            type: 'text',
            // date_time: new Date().toDateString(),
            description: description.value,
            title: title.value,
            content: content.value,
            scripture: scripture.value,
            created_at: DAYJS(),
            author: author.value,
            denomination: denomination.value,
            language: language.value,
            source: source.value,
            added_by: session.data.session?.user.id,
            is_published: isPublished.value
        };
        const { error } = sermonId.value
            ? await supabase.from('sermons').update(dataToInsert).match({ id: sermonId.value })
            : await supabase.from('sermons').insert(dataToInsert);

        if (error) {
            alert(error.message);
            loading.value = false;
            return;
        }
        resetForm();
        alert('Data Successfully Added!');
        await menuStore.setMenu('sermons');
    }

    loading.value = false;
}

const selectTypeOptions = [
    {
        value: 'youtube',
        label: 'Youtube'
    },
    {
        value: 'text',
        label: 'Text'
    }
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
    <div class='h-[100%] w-[100%] p-5 pl-10 overflow-y-auto overflowing-div'>
        <div class='w-full max-w-700px mx-auto'>
            <h2 class='font-thin text-size-23px'>Add New Sermon</h2>
            <div class='mt-10 flex flex-col gap-5'>
                <div>
                    <label for=''>Select Type:</label><br />
                    <NSelect v-model:value='selectedType' :options='selectTypeOptions' />
                </div>
                <div v-if="selectedType == 'youtube'">
                    <label for=''>Youtube ID:</label><br />
                    <NInput v-model:value='youtubeId' placeholder='Enter Youtube Id...' required type='text' />
                </div>
                <div v-if="selectedType == 'text'">
                    <label for=''>Title:</label><br />
                    <NInput v-model:value='title' placeholder='enter title' required type='text' />
                </div>
                <div v-if="selectedType == 'text'">
                    <label for=''>Scripture:</label><br />
                    <NInput v-model:value='scripture' placeholder='enter scripture' required type='text' />
                </div>
                <div v-if="selectedType == 'text'">
                    <label for=''>Content Author:</label><br />
                    <NInput v-model:value='author' placeholder='enter scripture' required type='text' />
                </div>
                <div v-if="selectedType == 'text'">
                    <label for=''>Select Denomination:</label><br />
                    <select v-model='denomination' class='p-2 rounded-md !dark:bg-dark-300 outline-none w-full'
                            required>
                        <option :value='null'>-- Select Denomination --</option>
                        <option v-for='den in denominationOptions' :key='den.label' :value='den.label'>
                            {{ den.label }}
                        </option>
                    </select>
                </div>
                <div v-if="selectedType == 'text'">
                    <label for=''>A Short Summary/Description:</label><br />
                    <textarea
                        v-model='description'
                        class='p-2 rounded-md min-h-200px w-full !dark:bg-dark-300 outline-none'
                        placeholder='Enter Description Here'
                        required
                    ></textarea>
                </div>
                <div>
                    <label for=''>Select Language:</label><br />
                    <select v-model='language' class='p-2 rounded-md min-w-200px w-full !dark:bg-dark-300 outline-none'
                            required>
                        <option value='english'>English</option>
                        <option value='tagalog'>Tagalog</option>
                    </select>
                </div>
                <div>
                    <label for=''>Enter Source:</label><br />
                    <input
                        v-model='source'
                        class='p-2 rounded-md min-w-250px w-full !dark:bg-dark-300 outline-none'
                        placeholder='enter URL'
                        required
                        type='text'
                    />
                </div>
                <div>
                    <label class='select-none'>
                        <input v-model='isPublished' placeholder='enter URL' type='checkbox' />
                        Is Published?
                    </label>
                </div>
                <div v-if="selectedType == 'text'">
                    <label for=''>Set Content:</label><br />
                    <Editor v-model='content' editorStyle='height: 320px' />
                </div>
                <div>
                    <NButton v-if='userStore.user' :disabled='loading' :loading='loading' type='primary'
                             @click='submitSermon()'>
                        Create
                    </NButton>
                    <NButton
                        v-else
                        :disabled='loading'
                        :loading='loading' type='primary'
                        @click='router.push("/profile")'
                    >
                        Login First
                    </NButton>
                </div>
            </div>
        </div>
    </div>
</template>
