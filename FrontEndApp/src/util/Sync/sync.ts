export async function syncData() {
    // get all data
    const bookmarks = await window.browserWindow.getBookMarks();
    const highlights = await window.browserWindow.getHighlights(JSON.stringify({
        page: 1,
        search: null,
        limit: 9999999999
    }));
    const clipNotes = await window.browserWindow.getClipNotes(JSON.stringify({
        page: 1,
        search: null,
        limit: 9999999999
    }));


    // set data
    console.log('bookmarks', bookmarks);
    console.log('highlights', highlights);
    console.log('clipNotes', clipNotes);
}