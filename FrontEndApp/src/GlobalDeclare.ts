declare global {
    interface Window {
        versions: any;
        browserWindow: any;
        getAvailableBibles: Function;
        getVerses: Function;
    }
}
export {};
