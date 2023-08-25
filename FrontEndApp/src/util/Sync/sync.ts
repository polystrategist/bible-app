export async function syncData() {
    const bookmarks =  await window.browserWindow.getBookMarks();
    const highlights = await window.browserWindow.getHighlights();
    const clipNotes = await window.browserWindow.getClipNotes();
}