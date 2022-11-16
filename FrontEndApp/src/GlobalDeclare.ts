declare global {
    interface Window {
        versions: Function;
        browserWindow: Function;
        getAvailableBibles: Function;
        getVerses: Function;
    }
}
export {};
