<script lang="ts" setup>
useHead({
    title: "Believers Sword",
    script: [
        {
            type: "text/javascript",
            src: "https://platform-api.sharethis.com/js/sharethis.js#property=614ca36b13073f0019a43593&product=inline-share-buttons",
            async: true,
        },
    ],
});

onMounted(() => {
    setDownloadPath();
});

async function setDownloadPath() {
    console.log("getting data");
    await fetch("https://api.github.com/repos/Bible-Projects/believers-sword-next/releases/latest", {
        method: "GET",
        headers: {
            Accept: "application/vnd.github.v3+json",
        },
    })
        .then((response) => response.json())
        .then((data) => {
            const linkDownloadAppElement = document.getElementById("link-download-app");
            if (linkDownloadAppElement) linkDownloadAppElement.style.display = "block";
            if (linkDownloadAppElement)
                linkDownloadAppElement.setAttribute(
                    "href",
                    `https://github.com/Bible-Projects/believers-sword-app/releases/download/v${data.name}/Believers-Sword-Setup-${data.name}.exe`
                );

            const loadingButton = document.getElementById("loading-button");
            const downloadButton = document.getElementById("download-button");
            if (loadingButton) loadingButton.style.display = "none";
            if (downloadButton) downloadButton.innerHTML = `Download For Windows v.${data.name}`;
        })
        .catch((e) => {
            console.log(e);
        });
}
</script>
<template>
    <NuxtLayout>
        <section class="w-[100%] min-h-[100vh] dark:text-gray-100 py-[50px] duration-300">
            <div class="flex justify-center mb-5">
                <img
                    alt="Application Logo Image"
                    class="w-180px"
                    src="~/assets/images/believers-sword.svg"
                    width="180"
                />
            </div>
            <div
                class="w-[100%] max-w-[1000px] mx-auto flex flex-col justify-center items-center px-[15px] text-center"
            >
                <h1 class="md:text-48px text-38px font-medium">Believers Sword</h1>
                <p class="text-center md:text-18px text-16px font-thin max-w-700px !leading-normal mt-20px">
                    To God be the glory, We want to introduce this amazing bible studying app called "Believers Sword".
                    Whether you're new to this app or a seasoned user, Believers Sword App is a simple application that
                    helps you study bible with extra features.
                </p>
                <div class="my-30px flex flex-col gap-10px items-center justify-center">
                    <a
                        id="link-download-app"
                        class="my-[30px]"
                        href="https://github.com/Bible-Projects/believers-sword-app/releases/download/v1.2.6/Believers-Sword-Setup-1.2.6.exe"
                        style="display: none"
                    >
                        <button
                            id="download-button"
                            class="bg-yellow-600 dark:bg-yellow-500 px-[15px] py-[5px] rounded-md hover:bg-yellow-700 duration-300 active:bg-yellow-900 text-dark-900 inline-flex text-white border-0 py-2 px-6 focus:outline-none rounded text-lg"
                        >
                            Download For Windows v.1.2.6
                        </button>
                        <br />
                        <small class="font-bold dark:text-yellow-400 text-yellow-600">
                            Installer is <span>100%</span> Safe
                        </small>
                    </a>

                    <div id="loading-button" class="spin-icon" style="display: block">
                        <svg
                            height="24"
                            style="fill: rgba(255, 255, 255, 1)"
                            viewBox="0 0 24 24"
                            width="24"
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <path
                                d="M2 11h5v2H2zm15 0h5v2h-5zm-6 6h2v5h-2zm0-15h2v5h-2zM4.222 5.636l1.414-1.414 3.536 3.536-1.414 1.414zm15.556 12.728-1.414 1.414-3.536-3.536 1.414-1.414zm-12.02-3.536 1.414 1.414-3.536 3.536-1.414-1.414zm7.07-7.071 3.536-3.535 1.414 1.415-3.536 3.535z"
                            ></path>
                        </svg>
                    </div>
                </div>

                <small>
                    This is only available for <span class="text-blue-500 font-medium">Windows</span>, Coming soon for
                    MAC and Linux
                </small>
                <small>By downloading, you agree to use it to study the bible heartily.</small>
                <div class="mt-2">
                    If you like to download the legacy app/old version, you can download it by clicking
                    <a
                        class="text-blue-500 font-medium hover:underline"
                        href="https://github.com/Bible-Projects/believers-sword-app/releases/download/v1.3.4/Believers-Sword-Setup-1.3.4.exe"
                    >
                        Download Legacy.
                    </a>
                </div>
            </div>
            <div class="px-[15px] mx-auto flex flex-col justify-center pt-[50px] items-center">
                <div class="max-w-[1200px] w-[100%] mx-auto relative md:px-20px">
                    <a class="dark:hidden block" href="~/assets/images/screen-light.png">
                        <img
                            alt="Application Preview Image"
                            class="rounded-md"
                            src="~/assets/images/screen-light.png"
                        />
                    </a>
                    <a class="dark:block hidden" href="~/assets/images/screen-dark.png">
                        <img alt="Application Preview Image" class="rounded-md" src="~/assets/images/screen-dark.png" />
                    </a>
                </div>
            </div>
            <Sponsors />
        </section>
    </NuxtLayout>
</template>
