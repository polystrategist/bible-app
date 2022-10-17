<script setup lang="ts">
import Logo from './../../assets/logo.svg';
</script>
<template>
    <div id="title-bar" class="flex h-30px">
        <div class="flex items-center gap-9px h-[100%]">
            <div class="pl-10px w-28px">
                <img :src="Logo" class="h-35px w-30px" alt="Icon Logo" title="Believers Sword Logo" />
            </div>
            <div class="text-size-[12px] font-700 flex gap-5px items-center whitespace-nowrap">
                <span class="capitalize"> Believers Sword </span>
            </div>
        </div>
        <div id="drag-region" class="w-[100%] p-[10px]" style="cursor: move"></div>
        <div class="text-size-12px mr-10px h-[100%]">
            <div class="cursor-pointer h-[100%] px-10px flex justify-center items-center text-size-18px">
                <div>
                    <span class="capitalize"> dark</span>
                </div>
            </div>
        </div>
    </div>
</template>
<style lang="scss">
#drag-region {
    -webkit-app-region: drag;
    z-index: 999;
}

#minimizeButton,
#maximizeButton,
#closeButton {
    -webkit-app-region: no-drag;
    cursor: pointer !important;
}
</style>
