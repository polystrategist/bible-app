export const setScrollTopState = (containerID: string, selectedElementID: string): void => {
    const ViewVerseElement = document.getElementById(containerID);
    const TheSelectedVerse = document.getElementById(selectedElementID);
    if (ViewVerseElement && TheSelectedVerse) {
        const selectedVerseOffset = TheSelectedVerse.offsetTop - 80;
        ViewVerseElement.scrollTop = selectedVerseOffset;
    }
};
