import { h } from 'vue';
import { Icon } from '@iconify/vue';
import { NIcon } from 'naive-ui';

export function renderIcon(icon: string) {
    return () => h(Icon, { icon: icon });
}

export function renderNIcon(icon: any, size?: number|null) {
    return () => h(NIcon, {
        ...(size && { size: size }),
    }, () => h(icon));
}

/**
 * Strip MyBible/HTML verse markup down to clean, readable plain text.
 *
 * Strong's numbers (<s>), footnotes (<f>) and anchors (<a>) are dropped
 * entirely — element and content — so they never leak into copied or previewed
 * text (e.g. "What1161 if1487 God2316"). Bracketed footnote markers like "[214]"
 * are stripped too. Mirrors getCleanVerseTextForCopy in ViewVerses, which is how
 * the reader pane keeps the same markup out of the on-screen text.
 */
export function stripVerseHtml(html: string): string {
    const tpl = document.createElement('template');
    tpl.innerHTML = html ?? '';
    tpl.content.querySelectorAll('a, s, f').forEach((el) => el.remove());
    return (tpl.content.textContent ?? '')
        .replace(/\[\d+\]/g, '')
        .replace(/\s+/g, ' ')
        .trim();
}
