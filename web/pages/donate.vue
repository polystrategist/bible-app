<script setup lang="ts">
useHead({
    title: "Believers Sword - Donate",
    script: [
        {
            type: "text/javascript",
            src: "https://platform-api.sharethis.com/js/sharethis.js#property=614ca36b13073f0019a43593&product=inline-share-buttons",
            async: true,
        },
    ],
});
</script>
<template>
    <NuxtLayout>
        <section class="w-[100%] min-h-[100vh] dark:text-gray-100 py-[50px] duration-300">
            <div class="max-w-[1200px] w-[100%] mx-auto text-center py-[50px]">
                <h1 class="font-thin text-[3em]">Donate</h1>
            </div>
            <div class="max-w-[700px] w-[100%] mx-auto text-[18px] leading-normal">
                <div class="bg-yellow-200 my-[10px] text-gray-800 p-[10px] rounded-lg">
                    <h1 class="font-bold underline">This App Absolutely Free</h1>
                    I am sharing this application with you for <b>FREE</b>. That means selling a copy of this
                    application is forbidden. The word of God is free, so I am forbidding anyone from selling a copy.
                </div>
                If this ministry blesses you, and like to join me. You can Support this application financially by
                selecting any of the choices below. Donate or Not, this application is always free on the internet.
            </div>
            <div class="max-w-[1200px] w-[100%] mx-auto flex flex-wrap justify-center mt-[50px] gap-[30px]">
                <button
                    class="rounded-xl overflow-hidden flex items-center flex-col opacity-70 hover:opacity-100"
                    onclick="window.open('https://www.paypal.com/donate?hosted_button_id=DCZYF7KWPUVB4','popup','width=700,height=700'); return false;"
                >
                    <span class="text-size-24px font-600">Debit/Credit</span>
                    <img src="~/assets/images/paypal.png" alt="" width="400" />
                </button>
                <button
                    class="rounded-xl overflow-hidden opacity-70 hover:opacity-100"
                    onclick="window.open('https://i.ibb.co/kJGg32y/GCash-My-QR-06102021230745.png','popup','width=700,height=700'); return false;"
                >
                    <img src="~/assets/images/gcash.jpg" alt="" width="325" />
                </button>
                <button
                    class="rounded-xl overflow-hidden opacity-70 hover:opacity-100"
                    onclick="window.open('https://www.buymeacoffee.com/BroJenuel','popup','width=700,height=700'); return false;"
                >
                    <img class="rounded-xl" src="~/assets/images/buymecoffee.png" alt="" width="325" />
                </button>
                <button
                    class="rounded-xl overflow-hidden opacity-70 hover:opacity-100"
                    onclick="window.open('https://ko-fi.com/brojenuel','popup','width=700,height=700'); return false;"
                >
                    <img class="rounded-xl" src="~/assets/images/kofi.gif" alt="" width="325" />
                </button>
            </div>
        </section>
    </NuxtLayout>
</template>
