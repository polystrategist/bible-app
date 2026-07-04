import { Extension } from '@tiptap/core';

export interface IndentOptions {
    /** Node types that can carry a block indent. */
    types: string[];
    /** Minimum indent level. */
    minLevel: number;
    /**
     * Maximum indent level. Kept at 8 to match Quill's conventional range; note
     * the mobile HTML->Delta parser clamps a re-imported indent at level 5.
     */
    maxLevel: number;
}

declare module '@tiptap/core' {
    interface Commands<ReturnType> {
        indent: {
            /** Increase the block indent of the selected paragraph(s)/heading(s). */
            indent: () => ReturnType;
            /** Decrease the block indent of the selected paragraph(s)/heading(s). */
            outdent: () => ReturnType;
        };
    }
}

const EM_RE = /([\d.]+)\s*em/;

/**
 * Block-indentation for TipTap, kept format-compatible with the Flutter (Quill)
 * mobile app so indentation survives sync in both directions.
 *
 * Indent is stored on the block node as `indent` (an integer level) and
 * serialized to an inline `padding-left: {level}em` style — the exact
 * representation the mobile editor writes (`vsc_quill_delta_to_html`) and reads
 * (`flutter_quill_delta_from_html`, which recovers indent only from an inline
 * `padding-left`/`padding-right` at 1em = 1 level). Using a class such as
 * `ql-indent-N` would not round-trip on mobile and would be stripped by
 * ProseMirror here.
 *
 * Tab / Shift-Tab increase / decrease the indent. Inside a list the keys defer
 * to list nesting (sink / lift the list item) instead, matching common editor
 * behavior.
 */
export const Indent = Extension.create<IndentOptions>({
    name: 'indent',

    addOptions() {
        return {
            types: ['paragraph', 'heading'],
            minLevel: 0,
            maxLevel: 8,
        };
    },

    addGlobalAttributes() {
        return [
            {
                types: this.options.types,
                attributes: {
                    indent: {
                        default: 0,
                        parseHTML: (element) => {
                            const padding =
                                element.style.paddingLeft || element.style.paddingRight;
                            if (!padding) return 0;
                            const match = EM_RE.exec(padding);
                            if (!match) return 0;
                            const level = Math.round(parseFloat(match[1]));
                            if (!Number.isFinite(level) || level <= 0) return 0;
                            return Math.min(level, this.options.maxLevel);
                        },
                        renderHTML: (attributes) => {
                            const level = attributes.indent || 0;
                            if (!level) return {};
                            return { style: `padding-left: ${level}em` };
                        },
                    },
                },
            },
        ];
    },

    addCommands() {
        const shiftIndent =
            (delta: number) =>
            ({ state, dispatch }: any) => {
                const { from, to } = state.selection;
                let tr = state.tr;
                let changed = false;

                state.doc.nodesBetween(from, to, (node: any, pos: number) => {
                    if (!this.options.types.includes(node.type.name)) return;
                    const current = node.attrs.indent || 0;
                    const next = Math.min(
                        Math.max(current + delta, this.options.minLevel),
                        this.options.maxLevel
                    );
                    if (next !== current) {
                        tr = tr.setNodeMarkup(pos, undefined, {
                            ...node.attrs,
                            indent: next,
                        });
                        changed = true;
                    }
                });

                if (changed && dispatch) dispatch(tr);
                return changed;
            };

        return {
            indent: () => shiftIndent(1),
            outdent: () => shiftIndent(-1),
        };
    },

    addKeyboardShortcuts() {
        return {
            Tab: () => {
                // Inside a list, Tab nests the item rather than indenting the block.
                if (this.editor.isActive('listItem')) {
                    this.editor.commands.sinkListItem('listItem');
                    return true;
                }
                this.editor.commands.indent();
                return true;
            },
            'Shift-Tab': () => {
                if (this.editor.isActive('listItem')) {
                    this.editor.commands.liftListItem('listItem');
                    return true;
                }
                this.editor.commands.outdent();
                return true;
            },
        };
    },
});

export default Indent;
