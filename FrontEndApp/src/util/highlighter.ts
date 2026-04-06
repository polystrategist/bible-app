import { debouncedRunSync } from './Sync/sync';

const getSelectionParentElement = () => {
    let parentEl = null,
        sel;

    if (window.getSelection) {
        sel = window.getSelection();
        if (sel?.rangeCount) {
            parentEl = sel.anchorNode?.parentElement;

            let foundParent = false;
            while (!foundParent) {
                const hasKey = (parentEl as HTMLElement).getAttribute('data-key');
                if (hasKey) return parentEl;
                parentEl = parentEl?.parentNode;
            }

            if (parentEl?.nodeType != 1) {
                parentEl = parentEl?.parentNode;
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
        if (
            parentNode &&
            parentNode.classList &&
            parentNode.classList.contains('verse-select-text')
        ) {
            return true;
        }

        parentNode = parentNode.parentNode as HTMLElement;
    }
    return false;
}

export const highlight = async (color: string) => {
    try {
        const selectedParentElement: any = getSelectionParentElement();

        const bookNumber = selectedParentElement.getAttribute('data-book');
        const chapterNumber = selectedParentElement.getAttribute('data-chapter');
        const verseNumber = selectedParentElement.getAttribute('data-verse');

        if (!bookNumber || !chapterNumber || !verseNumber) {
            window.message.error('Error: Cant Save Highlight.');
            window.getSelection()?.empty();
            return;
        }

        // Version-independent key (matches mobile app format)
        const key = `${bookNumber}_${chapterNumber}_${verseNumber}`;

        // Save just the hex color, not HTML — keeps sync compatible across platforms
        await saveHighlight({
            key,
            book_number: bookNumber,
            chapter: chapterNumber,
            verse: verseNumber,
            content: color,
        });

        window.getSelection()?.empty();
    } catch (e) {
        window.message.error('Their is An Error Saving Highlight.');
    }
};

export async function getChapterHighlights(args: { book_number: number; chapter: number }) {
    return await window.browserWindow.getChapterHighlights(JSON.stringify(args));
}

export async function saveHighlight(args: {
    key: string;
    book_number: number;
    chapter: number;
    verse: number;
    content: string;
}) {
    const result = await window.browserWindow.saveHighlight(JSON.stringify(args));
    debouncedRunSync();
    return result;
}

export const colors = [
    {
        color: '#FFD26A',
        name: 'orange',
    },
    {
        color: '#FFB6C1',
        name: 'lightpink',
    },
    {
        color: '#ADD8E6',
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
    {
        color: '#F9A8D4',
        name: 'rose',
    },
    {
        color: '#C4B5FD',
        name: 'violet',
    },
    {
        color: '#7DD3FC',
        name: 'sky',
    },
    {
        color: '#A7F3D0',
        name: 'mint',
    },
    {
        color: '#FDE68A',
        name: 'amber',
    },
    {
        color: '#E9D5FF',
        name: 'lavender',
    },
    {
        color: '#FBCFE8',
        name: 'pink',
    },
];
