export const setScrollTopState = (containerID: string, selectedElementID: string, subtract: number = 80): void => {
    const containerEl = document.getElementById(containerID);
    if (!containerEl) return;

    const selectedElements = new Set<HTMLElement>();
    const selectedById = document.getElementById(selectedElementID);
    if (selectedById && containerEl.contains(selectedById)) {
        selectedElements.add(selectedById);
    }
    containerEl
        .querySelectorAll<HTMLElement>(`.${selectedElementID}`)
        .forEach((selectedEl) => selectedElements.add(selectedEl));

    if (!selectedElements.size) return;

    selectedElements.forEach((selectedEl) => {
        // Support NScrollbar and split-pane scroll containers.
        let scrollEl = (containerEl.closest('.n-scrollbar-container') as HTMLElement) ?? containerEl;
        let parent = selectedEl.parentElement;

        while (parent && parent !== containerEl.parentElement) {
            const overflowY = window.getComputedStyle(parent).overflowY;
            const canScroll = parent.scrollHeight > parent.clientHeight;
            if (canScroll && ['auto', 'scroll', 'overlay'].includes(overflowY)) {
                scrollEl = parent;
                break;
            }
            parent = parent.parentElement;
        }

        const selectedTop = selectedEl.getBoundingClientRect().top - scrollEl.getBoundingClientRect().top + scrollEl.scrollTop;
        scrollEl.scrollTop = selectedTop - subtract;
    });
};
