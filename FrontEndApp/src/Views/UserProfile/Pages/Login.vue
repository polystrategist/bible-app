<script setup lang="ts">
import { NInput, NButton } from 'naive-ui';
</script>
<template>
    <div class="h-full w-full">
        <div class="w-400px mx-auto mt-5 flex flex-col gap-2">
            <h5 class="text-center font-800 text-size-25px">User Login</h5>
            Email Address:
            <NInput placeholder="Email" />
            Password:
            <NInput placeholder="Password" type="password" />
            <NButton>Login</NButton>
        </div>
    </div>
</template>
