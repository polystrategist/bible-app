<script setup lang="ts">
useHead({
    title: "add sermon - admin",
});

const supabase = useSupabaseClient();
const sermonId = ref(null);
const selectedType = ref("youtube");
const youtubeId = ref(null);
const language = ref("english");
const source = ref(null);
const title = ref(null);
const scripture = ref(null);
const createdAt = ref(null);
const author = ref(null);
const denomination = ref(null);
const description = ref<string>("");
const content = ref("");
const loading = ref(false);

const denominationOptions = [
    { label: "Adventist" },
    { label: "Anglican" },
    { label: "Apostolic" },
    { label: "Assembly of God" },
    { label: "Baptist" },
    { label: "Bible Church" },
    { label: "Brethren" },
    { label: "Calvary Chapel" },
    { label: "Catholic" },
    { label: "Charismatic" },
    { label: "Christian Missionary Alliance" },
    { label: "Christian/Church of Christ" },
    { label: "Church of God" },
    { label: "Congregational" },
    { label: "Disciples of Christ" },
    { label: "Episcopal" },
    { label: "Evangelical Free" },
    { label: "Evangelical/Non-denominational" },
    { label: "Foursquare" },
    { label: "Free Methodist" },
    { label: "Friends" },
    { label: "Grace Brethren" },
    { label: "Holiness" },
    { label: "Independent/Bible" },
    { label: "Lutheran" },
    { label: "Mennonite" },
    { label: "Methodist" },
    { label: "Nazarene" },
    { label: "Orthodox" },
    { label: "Other" },
    { label: "Pentecostal" },
    { label: "Presbyterian/Reformed" },
    { label: "Salvation Army" },
    { label: "Seventh-Day Adventist" },
    { label: "United Methodist" },
    { label: "Vineyard" },
    { label: "Wesleyan" },
    { label: "Others" },
];

const getYoutubeVideoDetails = async (
    youtubeVideoId: string | number,
    key = "AIzaSyB6XTl8aX3Ro3lVKtPbx_2pHyTVU4GAyQM",
    part = "snippet,contentDetails,statistics,status"
) => {
    return await $fetch("https://www.googleapis.com/youtube/v3/videos", {
        params: {
            key,
            part,
            id: youtubeVideoId,
        },
    });
};

async function submitSermon() {
    loading.value = true;
    if (selectedType.value == "youtube") {
        // get data from api
        const youtubeData: any = await getYoutubeVideoDetails(youtubeId.value as any);

        if (!youtubeData || !youtubeData.items) {
            alert("Fetching Video Details Error");
            return;
        }
        const youtubeDetails = youtubeData.items[0];
        let dataToEnter = {
            type: "youtube",
            thumbnail: youtubeDetails.snippet.thumbnails.medium.url,
            // date_time: new Date(),
            description: youtubeDetails.snippet.description,
            title: youtubeDetails.snippet.title,
            youtube_embed: `https://www.youtube.com/embed/${youtubeDetails.id}`,
            youtube_video_id: youtubeDetails.id,
            language: language.value,
            source: source.value,
        };
        const { data, error } = sermonId.value
            ? await supabase.from("sermons").update(dataToEnter).match({ id: sermonId.value })
            : await supabase.from("sermons").insert(dataToEnter);

        if (error) {
            alert(error.message);
            return;
        }

        alert("Data Successfully Added!");
        useRouter().push({ path: "/admin/sermons" });
    } else if (selectedType.value == "text") {
        let dataToInsert = {
            type: "text",
            // date_time: new Date().toDateString(),
            description: description.value,
            title: title.value,
            content: content.value,
            scripture: scripture.value,
            // created_at: new Date(formValue.value.created_at),
            author: author.value,
            denomination: denomination.value,
            language: language.value,
            source: source.value,
        };
        const { data, error } = sermonId.value
            ? await supabase.from("sermons").update(dataToInsert).match({ id: sermonId.value })
            : await supabase.from("sermons").insert(dataToInsert);

        if (error) {
            alert(error.message);
            return;
        }

        alert("Data Successfully Added!");
        useRouter().push({ path: "/admin/sermons" });
    }

    loading.value = false;
}
</script>

<template>
    <NuxtLayout name="admin">
        <div>
            <h2 class="font-thin text-size-23px">Add New Sermon</h2>
            <div class="mt-10 flex flex-col gap-5">
                <div>
                    <label for="">Select Type:</label><br />
                    <select class="p-2 border rounded-md min-w-200px" v-model="selectedType" required>
                        <option value="youtube">youtube</option>
                        <option value="text">text</option>
                    </select>
                </div>
                <div v-if="selectedType == 'youtube'">
                    <label for="">Youtube ID:</label><br />
                    <input
                        class="p-2 border rounded-md min-w-250px"
                        type="text"
                        v-model="youtubeId"
                        placeholder="Enter Youtube Id..."
                        required
                    />
                </div>
                <div v-if="selectedType == 'text'">
                    <label for="">Title:</label><br />
                    <input
                        class="p-2 border rounded-md min-w-250px"
                        type="text"
                        v-model="title"
                        placeholder="enter title"
                        required
                    />
                </div>
                <div v-if="selectedType == 'text'">
                    <label for="">Scripture:</label><br />
                    <input
                        class="p-2 border rounded-md min-w-250px"
                        type="text"
                        v-model="scripture"
                        placeholder="enter scripture"
                        required
                    />
                </div>
                <div v-if="selectedType == 'text'">
                    <label for="">Created At:</label><br />
                    <input
                        class="p-2 border rounded-md min-w-250px"
                        type="date"
                        v-model="createdAt"
                        placeholder="enter created at"
                        required
                    />
                </div>
                <div v-if="selectedType == 'text'">
                    <label for="">Content Author:</label><br />
                    <input
                        class="p-2 border rounded-md min-w-250px"
                        type="text"
                        v-model="author"
                        placeholder="enter scripture"
                        required
                    />
                </div>
                <div v-if="selectedType == 'text'">
                    <label for="">Select Denomination:</label><br />
                    <select class="p-2 border rounded-md min-w-200px" v-model="denomination" required>
                        <option v-for="den in denominationOptions" :key="den.label" :value="den.label">
                            {{ den.label }}
                        </option>
                    </select>
                </div>
                <div v-if="selectedType == 'text'">
                    <label for="">Select Denomination:</label><br />
                    <textarea
                        v-model="description"
                        class="p-2 border rounded-md min-w-300px min-h-200px"
                        placeholder="Enter Description Here"
                        required
                    ></textarea>
                </div>
                <div>
                    <label for="">Select Language:</label><br />
                    <select class="p-2 border rounded-md min-w-200px" v-model="language" required>
                        <option value="english">English</option>
                        <option value="tagalog">Tagalog</option>
                    </select>
                </div>
                <div>
                    <label for="">Enter Source:</label><br />
                    <input
                        class="p-2 border rounded-md min-w-250px"
                        type="text"
                        v-model="source"
                        placeholder="enter URL"
                        required
                    />
                </div>
                <div v-if="selectedType == 'text'">
                    <label for="">Set Content:</label><br />
                    <Editor v-model="content" editorStyle="height: 320px" />
                </div>
                <div>
                    <PButton @click="submitSermon()" class="hover:underline" :loading="loading" :disabled="loading">
                        Create
                    </PButton>
                </div>
            </div>
        </div>
    </NuxtLayout>
</template>
