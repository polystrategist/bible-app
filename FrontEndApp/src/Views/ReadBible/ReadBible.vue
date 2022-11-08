<script lang="ts" setup>
import { Splitpanes, Pane } from 'splitpanes';
import LeftSideBar from './LeftSideBar/LeftSideBar.vue';
import RightSideBar from './RightSideBar/RightSideBar.vue';
import ViewVerses from './ViewVerses/ViewVerses.vue';
</script>

<template>
    <Splitpanes vertical class="h-full w-full">
        <Pane size="25" min-size="15" max-size="50">
            <LeftSideBar />
        </Pane>
        <Pane class="bg-gray-100 dark:bg-dark-700 p-3">
            <ViewVerses />
        </Pane>
        <Pane size="25" min-size="15" max-size="50">
            <RightSideBar />
        </Pane>
    </Splitpanes>
</template>
