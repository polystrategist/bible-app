export const getSelectionParentElement = (elementClass: string) => {
    let parentEl = null,
        sel;

    if (window.getSelection) {
        sel = window.getSelection();
        if (sel?.rangeCount) {
            parentEl = sel.anchorNode?.parentElement;

            let foundParent = false;
            try {
                while (!foundParent) {
                    const hasKey = (parentEl as HTMLElement).classList.contains(elementClass);
                    if (hasKey) return parentEl;
                    parentEl = parentEl?.parentNode;
                }
            } catch (e) {
                return null;
            }
        }
    }

    return parentEl;
};
