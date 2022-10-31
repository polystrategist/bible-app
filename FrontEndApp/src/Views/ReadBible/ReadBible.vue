<script lang="ts" setup>
import { Splitpanes, Pane } from 'splitpanes';
</script>

<template>
    <Splitpanes vertical class="h-full w-full">
        <Pane size="25" min-size="15" max-size="50">
            <div>bible books</div>
            <div>
                <div>1</div>
                <div>2</div>
                <div>3</div>
                <div>4</div>
            </div>
        </Pane>
        <Pane>
            read bible here Lorem ipsum dolor sit amet consectetur adipisicing elit. Officia et esse mollitia quaerat est at odit
            labore similique ab, totam hic, iste quo distinctio soluta deleniti illo perferendis sapiente. Aliquam.
        </Pane>
        <Pane size="25" min-size="15" max-size="50">right side bar here</Pane>
    </Splitpanes>
</template>
