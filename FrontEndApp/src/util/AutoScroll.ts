export const setScrollTopState = (containerID: string, selectedElementID: string, subtract: number = 80): void => {
    const ViewVerseElement = document.getElementById(containerID);
    const TheSelectedVerse = document.getElementById(selectedElementID);
    if (ViewVerseElement && TheSelectedVerse) {
        ViewVerseElement.scrollTop = TheSelectedVerse.offsetTop - subtract;
    }
};
