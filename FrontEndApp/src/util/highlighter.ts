const getSelectionParentElement = () => {
    let parentEl = null,
        sel;
    if (window.getSelection) {
        sel = window.getSelection();
        if (sel?.rangeCount) {
            parentEl = sel.getRangeAt(0).commonAncestorContainer;
            if (parentEl.nodeType != 1) {
                parentEl = parentEl.parentNode;
            }
        }
    }

    return parentEl;
};

export function isHighlightable(): boolean {
    const selected = window.getSelection();
    const selection = selected?.getRangeAt(0);
    let parentNode = selection?.startContainer.parentNode as HTMLElement;

    for (let x = 0; x <= 10; x++) {
        if (parentNode && parentNode.classList && parentNode.classList.contains('verse-select-text')) {
            return true;
        }

        parentNode = parentNode.parentNode as HTMLElement;
    }
    return false;
}

export const highlight = async (color: string) => {
    try {
        const selected = window.getSelection();
        const selection = selected?.getRangeAt(0);
        const selectedContent = selection?.extractContents().textContent;
        const span = document.createElement('span');
        span.style.backgroundColor = color;
        if (color != 'remove') span.style.color = '#111827';
        if (color != 'remove') span.className = 'imOnlyOne HasHighlightSpan';
        if (selectedContent) span.textContent = selectedContent;
        if (selection) selection.insertNode(span);

        const selectedParentElement: any = getSelectionParentElement();

        const Children = selectedParentElement.children;
        if (Children.length > 0) {
            for (const elem of Children) {
                if (elem.textContent === '') elem.remove();
            }
        }

        let key = selectedParentElement.getAttribute('data-key');
        let bibleVersion = selectedParentElement.getAttribute('data-bible-version');
        let bookNumber = selectedParentElement.getAttribute('data-book');
        let chapterNumber = selectedParentElement.getAttribute('data-chapter');
        let verseNumber = selectedParentElement.getAttribute('data-verse');
        let content = selectedParentElement.innerHTML;

        if (color === 'remove') {
            const parentElem = selectedParentElement;
            const classList = parentElem.classList.value;

            if (classList.includes('HasHighlightSpan')) {
                parentElem.className = '';
                parentElem.style.removeProperty('background-color');
                parentElem.style.removeProperty('color');
            }

            const rootParent = selectedParentElement.parentElement;
            const rootParentClassList = rootParent.classList.value;
            if (rootParentClassList.includes('verse-select-text cursor-text')) {
                key = rootParent.getAttribute('data-key');
                bibleVersion = rootParent.getAttribute('data-bible-version');
                bookNumber = rootParent.getAttribute('data-book');
                chapterNumber = rootParent.getAttribute('data-chapter');
                verseNumber = rootParent.getAttribute('data-verse');
                content = rootParent.innerHTML;
            }
        }

        await saveHighlight({
            key,
            book_number: bookNumber,
            chapter: chapterNumber,
            verse: verseNumber,
            content,
        });

        window.getSelection()?.empty();
    } catch (e) {
        console.log(e);
    }
};

export async function getChapterHighlights(args: { book_number: number; chapter: number }) {
    const highlights = await window.browserWindow.getChapterHighlights(JSON.stringify(args));
    return highlights;
}

export async function saveHighlight(args: { key: string; book_number: number; chapter: number; verse: number; content: string }) {
    const save = await window.browserWindow.saveHighlight(JSON.stringify(args));
    return save;
}

export const colors = [
    {
        color: '#FFD26A',
        name: 'orange',
    },
    {
        color: 'lightpink',
        name: 'lightpink',
    },
    {
        color: 'lightblue',
        name: 'lightblue',
    },
    {
        color: '#80ED99',
        name: 'green',
    },
    {
        color: '#C2B8A3',
        name: 'brown',
    },
];
