export async function installExt() {
    try {
        const { default: installExtension, VUEJS_DEVTOOLS } = await import('electron-devtools-installer');
        await installExtension(VUEJS_DEVTOOLS);
        console.log('Added Extension');
    } catch (err) {
        console.log('Extension Error: ', err);
    }
}
