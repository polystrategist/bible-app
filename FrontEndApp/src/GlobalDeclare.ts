declare global {
    interface Window {
        versions: any;
        browserWindow: any;
        getAvailableBibles: Function;
        getVerses: Function;
        searchBible: Function;
        download: Function;
        downloadModule: Function;
        saveBookMark: Function;
        getBookMarks: Function;
        deleteBookmark: Function;
    }
}
export {};
