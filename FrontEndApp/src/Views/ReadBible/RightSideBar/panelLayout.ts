export interface PanelSectionState {
    key: string;
    expanded: boolean;
    /** px-scaled weight; relative size used to split height among open sections */
    size: number;
}

export const HEADER_HEIGHT = 32; // collapsed section / header bar height (px)
export const DIVIDER_HEIGHT = 4; // draggable divider between two open sections (px)
export const MIN_BODY_HEIGHT = 64; // minimum body height for an open section (px)
export const MIN_OPEN_HEIGHT = HEADER_HEIGHT + MIN_BODY_HEIGHT; // 96

/** Number of places where two consecutive sections in the stack are both open. */
function countOpenAdjacencies(sections: PanelSectionState[]): number {
    let count = 0;
    for (let i = 1; i < sections.length; i++) {
        if (sections[i].expanded && sections[i - 1].expanded) count++;
    }
    return count;
}

/**
 * Compute the pixel height for every section.
 * - Collapsed sections take exactly HEADER_HEIGHT.
 * - Open sections split the remaining height proportional to their `size`
 *   weights, each at least MIN_OPEN_HEIGHT. Open heights always sum to the
 *   available space when there is room above the per-section minimum.
 * Pure — no DOM — so it can be reasoned about directly.
 */
export function computeLayout(
    containerHeight: number,
    sections: PanelSectionState[]
): Record<string, number> {
    const result: Record<string, number> = {};
    const open = sections.filter((s) => s.expanded);

    for (const s of sections) {
        if (!s.expanded) result[s.key] = HEADER_HEIGHT;
    }
    if (open.length === 0) return result;

    const collapsedCount = sections.length - open.length;
    const reserved =
        collapsedCount * HEADER_HEIGHT + countOpenAdjacencies(sections) * DIVIDER_HEIGHT;
    const available = Math.max(open.length * MIN_OPEN_HEIGHT, containerHeight - reserved);

    // Distribute `available` among open sections proportional to their `size`
    // weights, clamping each up to MIN_OPEN_HEIGHT. Sections that hit the floor
    // are pinned and the rest re-share the remaining pool, so open heights always
    // sum to `available`. When nothing needs clamping, h_i = size_i/totalWeight *
    // available exactly — so pixel sizes committed during a divider drag round-trip
    // back to the same heights (the divider tracks the cursor).
    const remaining = new Set(open.map((s) => s.key));
    let pool = available;

    let changed = true;
    while (changed) {
        changed = false;
        let weightSum = 0;
        for (const s of open) {
            if (remaining.has(s.key)) weightSum += Math.max(s.size, 1);
        }
        for (const s of open) {
            if (!remaining.has(s.key)) continue;
            const share = (Math.max(s.size, 1) / weightSum) * pool;
            if (share < MIN_OPEN_HEIGHT) {
                result[s.key] = MIN_OPEN_HEIGHT;
                remaining.delete(s.key);
                pool -= MIN_OPEN_HEIGHT;
                changed = true;
            }
        }
    }

    const remOpen = open.filter((s) => remaining.has(s.key));
    const weightSum = remOpen.reduce((sum, s) => sum + Math.max(s.size, 1), 0);
    let used = 0;
    remOpen.forEach((s, i) => {
        if (i === remOpen.length - 1) {
            result[s.key] = Math.round(pool - used);
        } else {
            const h = Math.round((Math.max(s.size, 1) / weightSum) * pool);
            result[s.key] = h;
            used += h;
        }
    });

    return result;
}
