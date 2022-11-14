import installExtension, { VUEJS_DEVTOOLS } from 'electron-devtools-installer';

export async function installExt() {
    await installExtension(VUEJS_DEVTOOLS)
        .then(() => {
            console.log('Added Extension');
        })
        .catch((err) => {
            console.log('Extension Error: ', err);
        });
}
