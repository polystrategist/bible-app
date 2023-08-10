<script setup lang="ts">
useHead({
    title: "Donate - Believers Sword",
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
            <div class="max-w-[1200px] w-[100%] mx-auto text-center pb-[50px]">
                <h1 class="font-thin text-[3em]">How To Download/Install</h1>
            </div>
            <div class="max-w-[700px] w-[100%] mx-auto text-[18px] leading-normal">
                <div>
                    <h1 class="text-[17px] font-bold">Step 1 - Download The Installer</h1>
                    <div class="pl-[20px]">
                        To Download the Installer, go to
                        <NuxtLink class="text-blue-500 hover:underline font-medium" to="/" target="_blank">
                            Home Page
                        </NuxtLink>
                        and download the Installer.
                        <img class="border my-[10px] rounded-md" src="~/assets/images/how/step1.png" />
                    </div>
                </div>
                <div class="mt-[30px]">
                    <h1 class="text-[17px] font-bold">Step 2 - Save The Installer</h1>
                    <div class="pl-[20px]">
                        Save The File by clicking save button.
                        <img class="border my-[10px] rounded-md" src="~/assets/images/how/step2.png" />
                    </div>
                </div>
                <div class="mt-[30px]">
                    <h1 class="text-[17px] font-bold">Step 3 - Keep The Installer</h1>
                    <div class="pl-[20px]">
                        Click the keep to tell the computer to keep the installer, the reason this is showing is because
                        its not yet commonly downloaded and the application is not Code Signed yet. Dont worry this
                        <b>installer is <span class="font-extrabold italic">100%</span> Safe</b>.

                        <div class="bg-yellow-200 my-[10px] text-gray-800 p-[10px] rounded-lg">
                            <h1 class="font-bold underline">This Installer is Totally Safe</h1>
                            Code sign is a certificate for the app. Code Signing is very expensive, and This application
                            is Free. You can
                            <a class="text-blue-500 hover:underline font-medium" target="_blank" href="/donate"
                                >Donate</a
                            >
                            to help me get a Code Sign for this application.
                        </div>

                        <img class="border my-[10px] rounded-md" src="~/assets/images/how/step3.png" />
                    </div>
                </div>
                <div class="mt-[30px]">
                    <h1 class="text-[17px] font-bold">Step 4 - Open The Installer</h1>
                    <div class="pl-[20px]">
                        Open the installer by clicking the installer.
                        <img class="border my-[10px] rounded-md" src="~/assets/images/how/step4.png" />
                    </div>
                </div>
                <div class="mt-[30px]">
                    <h1 class="text-[17px] font-bold">Step 5 - If this warning shows up, click "More info"</h1>
                    <div class="pl-[20px]">
                        If this shows up, click "More Info". The reason this is showing is because its not yet commonly
                        downloaded and the application is not Code Signed yet.. Dont worry this
                        <b>installer is <span class="font-extrabold italic">100%</span> Safe</b>.

                        <div class="bg-yellow-200 my-[10px] text-gray-800 p-[10px] rounded-lg">
                            <h1 class="font-bold underline">This Installer is Totally Safe</h1>
                            Code sign is a certificate for the app. Code Signing is very expensive, and This application
                            is Free. You can
                            <NuxtLink class="text-blue-500 hover:underline font-medium" target="_blank" to="/donate">
                                Donate
                            </NuxtLink>
                            to help me get a Code Sign for this application.
                        </div>
                        <img class="border my-[10px] rounded-md" src="~/assets/images/how/step5.png" />
                    </div>
                </div>
                <div class="mt-[30px]">
                    <h1 class="text-[17px] font-bold">Step 6 - Run The Installer"</h1>
                    <div class="pl-[20px]">
                        Run the installer
                        <img class="border my-[10px] rounded-md" src="~/assets/images/how/step6.png" />
                    </div>
                </div>
                <div class="mt-[30px]">
                    <h1 class="text-[17px] font-bold">Step 7 - Click Next"</h1>
                    <div class="pl-[20px]">
                        It is recommended to choose Only for me Option
                        <img class="border my-[10px] rounded-md" src="~/assets/images/how/step7.png" />
                    </div>
                </div>
                <div class="mt-[30px]">
                    <h1 class="text-[17px] font-bold">Step 8 - Click Install"</h1>
                    <div class="pl-[20px]">
                        Click Install, to install the app on your computer.
                        <img class="border my-[10px] rounded-md" src="~/assets/images/how/step8.png" />
                    </div>
                </div>
                <div class="mt-[30px]">
                    <h1 class="text-[17px] font-bold">Step 9 - Click Finished"</h1>
                    <div class="pl-[20px]">
                        Once, the installer is done click finish. Then the app will automatically be opened after
                        clicking the finish button.
                        <img class="border my-[10px] rounded-md" src="~/assets/images/how/step9.png" />
                    </div>
                </div>
            </div>
        </section>
    </NuxtLayout>
</template>
