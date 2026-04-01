export const setScrollTopState = (containerID: string, selectedElementID: string, subtract: number = 80): void => {
    const containerEl = document.getElementById(containerID);
    const selectedEl = document.getElementById(selectedElementID);
    if (!containerEl || !selectedEl) return;

    // Support NScrollbar: use its inner scrollable container if present
    const scrollEl = (containerEl.closest('.n-scrollbar-container') as HTMLElement) ?? containerEl;
    const selectedTop = selectedEl.getBoundingClientRect().top - scrollEl.getBoundingClientRect().top + scrollEl.scrollTop;
    scrollEl.scrollTop = selectedTop - subtract;
};
