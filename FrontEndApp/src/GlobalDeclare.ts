declare global {
    interface Window {
        versions: any;
        browserWindow: any;
        getAvailableBibles: Function;
        getVerses: Function;
        searchBible: Function;
        download: Function;
        downloadModule: Function;
    }
}
export {};
