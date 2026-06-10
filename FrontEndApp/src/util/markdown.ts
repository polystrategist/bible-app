// Minimal, safe Markdown → HTML renderer for AI assistant output.
//
// Supports the subset the assistant produces: ATX headings (#…######),
// **bold** / *italic*, `inline code`, ordered/unordered lists, blockquotes and
// paragraphs. Raw HTML in the source is escaped first, so the result is safe to
// pass to v-html (no third-party dependency / sanitizer needed).

function escapeHtml(s: string): string {
    return s
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
}

// Inline spans. Operates on already-escaped text, so it only ever introduces
// the tags we generate here.
function inline(s: string): string {
    return s
        .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
        .replace(/__([^_]+)__/g, '<strong>$1</strong>')
        .replace(/(^|[^*])\*([^*\n]+)\*/g, '$1<em>$2</em>')
        .replace(/`([^`]+)`/g, '<code>$1</code>');
}

/** Render a Markdown string to a safe HTML string. */
export function renderMarkdown(src: string): string {
    const lines = escapeHtml(src.replace(/\r\n/g, '\n')).split('\n');
    const out: string[] = [];
    let listType: 'ul' | 'ol' | null = null;
    let para: string[] = [];
    let inQuote = false;

    const flushPara = () => {
        if (para.length) {
            out.push(`<p>${inline(para.join(' '))}</p>`);
            para = [];
        }
    };
    const closeList = () => {
        if (listType) {
            out.push(`</${listType}>`);
            listType = null;
        }
    };
    const closeQuote = () => {
        if (inQuote) {
            out.push('</blockquote>');
            inQuote = false;
        }
    };

    for (const raw of lines) {
        const line = raw.trim();

        if (!line) {
            flushPara();
            closeList();
            closeQuote();
            continue;
        }

        const heading = line.match(/^(#{1,6})\s+(.*)$/);
        if (heading) {
            flushPara();
            closeList();
            closeQuote();
            // Shift down one level (# → h2) so headings sit under the page title.
            const level = Math.min(heading[1].length + 1, 6);
            out.push(`<h${level}>${inline(heading[2])}</h${level}>`);
            continue;
        }

        const quote = line.match(/^>\s?(.*)$/);
        if (quote) {
            flushPara();
            closeList();
            if (!inQuote) {
                out.push('<blockquote>');
                inQuote = true;
            }
            out.push(`<p>${inline(quote[1])}</p>`);
            continue;
        }

        const ul = line.match(/^[*\-]\s+(.*)$/);
        if (ul) {
            flushPara();
            closeQuote();
            if (listType !== 'ul') {
                closeList();
                out.push('<ul>');
                listType = 'ul';
            }
            out.push(`<li>${inline(ul[1])}</li>`);
            continue;
        }

        const ol = line.match(/^\d+\.\s+(.*)$/);
        if (ol) {
            flushPara();
            closeQuote();
            if (listType !== 'ol') {
                closeList();
                out.push('<ol>');
                listType = 'ol';
            }
            out.push(`<li>${inline(ol[1])}</li>`);
            continue;
        }

        // Plain prose → accumulate into the current paragraph.
        closeList();
        closeQuote();
        para.push(line);
    }

    flushPara();
    closeList();
    closeQuote();
    return out.join('\n');
}
