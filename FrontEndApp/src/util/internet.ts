export async function hasInternetConnection() {
    try {
        const response = await fetch("https://www.google.com/favicon.ico", {
            method: "HEAD",
            mode: "no-cors"
        });
        return true;
    } catch (error) {
        return false;
    }
}