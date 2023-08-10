<script setup lang="ts">
const route = useRoute();
const { $session } = useNuxtApp();
function changeTheme() {
    const theme = $session().get("theme");

    let newTheme = theme && theme == "dark" ? "light" : "dark";
    if (document.body.classList.contains("dark")) {
        newTheme = "light";
    }
    $session().set("theme", newTheme);
    document.body.className = newTheme;
}
</script>
<template>
    <div
        class="min-h-50px fixed top-0 left-0 w-full dark:bg-gray-800 dark:bg-opacity-25 bg-gray-300 p-7px bg-opacity-25 backdrop-filter backdrop-blur-md flex justify-center items-center dark:text-gray-300 shadow-md z-50"
    >
        <div class="flex flex-row gap-2 items-center header-nav">
            <NuxtLink to="/" class="mx-3px hover:underline" :class="{ 'nav-active': route.path == '/' }">
                Home
            </NuxtLink>
            <NuxtLink
                to="/how-to-download"
                class="mx-3px hover:underline"
                :class="{ 'nav-active': route.path == '/how-to-download' }"
            >
                How To Install
            </NuxtLink>
            <NuxtLink to="/donate" class="mx-3px hover:underline" :class="{ 'nav-active': route.path == '/donate' }">
                Donate
            </NuxtLink>
            <div class="text-24px ml-20px" title="Change Theme">
                <button @click="changeTheme()">
                    <svg
                        class="h-15px dark:hidden"
                        xmlns="http://www.w3.org/2000/svg"
                        xmlns:xlink="http://www.w3.org/1999/xlink"
                        viewBox="0 0 512 512"
                    >
                        <path
                            d="M279.135 512c78.756 0 150.982-35.804 198.844-94.775c28.27-34.831-2.558-85.722-46.249-77.401c-82.348 15.683-158.272-47.268-158.272-130.792c0-48.424 26.06-92.292 67.434-115.836c38.745-22.05 28.999-80.788-15.022-88.919A257.936 257.936 0 0 0 279.135 0c-141.36 0-256 114.575-256 256c0 141.36 114.576 256 256 256zm0-464c12.985 0 25.689 1.201 38.016 3.478c-54.76 31.163-91.693 90.042-91.693 157.554c0 113.848 103.641 199.2 215.252 177.944C402.574 433.964 344.366 464 279.135 464c-114.875 0-208-93.125-208-208s93.125-208 208-208z"
                            fill="currentColor"
                        ></path>
                    </svg>
                    <svg
                        class="h-20px light:hidden"
                        xmlns="http://www.w3.org/2000/svg"
                        xmlns:xlink="http://www.w3.org/1999/xlink"
                        viewBox="0 0 32 32"
                    >
                        <path
                            d="M16 12.005a4 4 0 1 1-4 4a4.005 4.005 0 0 1 4-4m0-2a6 6 0 1 0 6 6a6 6 0 0 0-6-6z"
                            fill="currentColor"
                        ></path>
                        <path d="M5.394 6.813l1.414-1.415l3.506 3.506L8.9 10.318z" fill="currentColor"></path>
                        <path d="M2 15.005h5v2H2z" fill="currentColor"></path>
                        <path d="M5.394 25.197L8.9 21.691l1.414 1.415l-3.506 3.505z" fill="currentColor"></path>
                        <path d="M15 25.005h2v5h-2z" fill="currentColor"></path>
                        <path d="M21.687 23.106l1.414-1.415l3.506 3.506l-1.414 1.414z" fill="currentColor"></path>
                        <path d="M25 15.005h5v2h-5z" fill="currentColor"></path>
                        <path d="M21.687 8.904l3.506-3.506l1.414 1.415l-3.506 3.505z" fill="currentColor"></path>
                        <path d="M15 2.005h2v5h-2z" fill="currentColor"></path>
                    </svg>
                </button>
            </div>
        </div>
    </div>
</template>
