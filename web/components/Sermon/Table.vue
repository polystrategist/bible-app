<script setup lang="ts">
const supabase = useSupabaseClient();
const sermons = ref<Array<any>>([]);
const page = ref(1);
const limit = ref(10);

const getPagination = (p: number, size: number) => {
    const thePage = p - 1;
    const theLimit = size ? +size : 3;
    const from = thePage ? thePage * theLimit : 0;
    const to = thePage ? from + size : size;

    return { from, to: to - 1 };
};
async function getSermons() {
    const { from, to } = getPagination(page.value, limit.value);
    const { data, error } = await supabase.from("sermons").select().order("id", { ascending: false }).range(from, to);
    if (error) {
        alert(error.message);
        return;
    }
    sermons.value = data;
}

onMounted(() => {
    getSermons();
});

defineExpose({
    getSermons,
});
</script>
<template>
    <div>
        <div class="min-h-400px">
            <table class="w-full sermons-table">
                <thead>
                    <tr class="text-left">
                        <th>Title</th>
                        <th>Content</th>
                        <th>Created At</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="sermon in sermons" :key="sermon.id">
                        <td>{{ sermon.title }}</td>
                        <td>{{ sermon.description.slice(0, 100) }}...</td>
                        <td>{{ sermon.created_at }}</td>
                        <td>
                            <div class="flex gap-10px">
                                <PButton label="Edit" class="p-button-info p-button-sm" />
                                <PButton label="Delete" class="p-button-danger p-button-sm" />
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="flex gap-10px py-50px justify-center">
            <PButton
                label="Previous"
                v-show="page > 1"
                @click="
                    page--;
                    getSermons();
                "
            />
            <PButton
                label="Next"
                v-show="sermons.length == limit"
                @click="
                    page++;
                    getSermons();
                "
            />
        </div>
    </div>
</template>
<style lang="scss">
.sermons-table {
    thead {
        th {
            padding: 10px;
            border-bottom: 1px solid rgb(231, 231, 231);
        }
    }
    tbody {
        td {
            padding: 10px;
        }
    }
}
</style>
