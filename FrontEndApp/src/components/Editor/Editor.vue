<script lang='ts' setup>
import { EditorContent, useEditor } from '@tiptap/vue-3';
import { NIcon } from 'naive-ui';
import {
    Code as CodeIcon,
    ListBulleted,
    ListNumbered,
    Paragraph as ParagraphIcon,
    Quotes,
    Redo,
    TextBold,
    TextClearFormat,
    TextItalic,
    TextNewLine,
    TextStrikethrough,
    TextUnderline,
    Undo
} from '@vicons/carbon';
import Underline from '@tiptap/extension-underline';
import Placeholder from '@tiptap/extension-placeholder';
import Bold from '@tiptap/extension-bold';
import Document from '@tiptap/extension-document';
import Paragraph from '@tiptap/extension-paragraph';
import Text from '@tiptap/extension-text';
import Italic from '@tiptap/extension-italic';
import Strike from '@tiptap/extension-strike';
import Code from '@tiptap/extension-code';
import Heading from '@tiptap/extension-heading';
import BulletList from '@tiptap/extension-bullet-list';
import ListItem from '@tiptap/extension-list-item';
import OrderedList from '@tiptap/extension-ordered-list';
import Blockquote from '@tiptap/extension-blockquote';
import HardBreak from '@tiptap/extension-hard-break';
import HorizontalRule from '@tiptap/extension-horizontal-rule';
import History from '@tiptap/extension-history';
import Youtube from '@tiptap/extension-youtube';
import Image from '@tiptap/extension-image';
import Link from '@tiptap/extension-link';
import CodeBlock from '@tiptap/extension-code-block'

const props = defineProps({
    modelValue: {
        type: [String],
        default: ''
    }
});
const emits = defineEmits(['update:modelValue']);

const editor = useEditor({
    content: props.modelValue,
    extensions: [
        Text,
        Bold,
        Italic,
        Strike,
        Code,
        Heading,
        BulletList,
        ListItem,
        OrderedList,
        Blockquote,
        HardBreak,
        HorizontalRule,
        History,
        Document,
        Paragraph,
        Underline,
        Youtube,
        Image,
        Link,
        CodeBlock,
        Placeholder.configure({
            placeholder: 'Write Something Here 😁👍',
            emptyEditorClass:
                'cursor-text before:content-[attr(data-placeholder)] before:absolute before:top-5 before:left-5 before:text-mauve-11 before:opacity-50 before-pointer-events-none'
        })
    ],
    onUpdate: ({ editor }) => {
        emits('update:modelValue', editor.getHTML());
    }
});
</script>

<template>
    <div>
        <div v-if='editor' class='editor-buttons'>
            <button
                :class="{ 'is-active': editor.isActive('bold') }"
                :disabled='!editor.can().chain().focus().toggleBold().run()'
                @click='editor?.chain().focus().toggleBold().run()'
            >
                <NIcon size='20'>
                    <TextBold />
                </NIcon>
            </button>
            <button
                :class="{ 'is-active': editor.isActive('underline') }"
                :disabled='!editor.can().chain().focus().toggleUnderline().run()'
                @click='editor?.chain().focus().toggleUnderline().run()'
            >
                <NIcon size='20'>
                    <TextUnderline />
                </NIcon>
            </button>
            <button
                :class="{ 'is-active': editor.isActive('italic') }"
                :disabled='!editor.can().chain().focus().toggleItalic().run()'
                @click='editor?.chain().focus().toggleItalic().run()'
            >
                <NIcon size='20'>
                    <TextItalic />
                </NIcon>
            </button>
            <button
                :class="{ 'is-active': editor.isActive('strike') }"
                :disabled='!editor.can().chain().focus().toggleStrike().run()'
                @click='editor?.chain().focus().toggleStrike().run()'
            >
                <NIcon size='20'>
                    <TextStrikethrough />
                </NIcon>
            </button>
            <button
                :class="{ 'is-active': editor.isActive('code') }"
                :disabled='!editor.can().chain().focus().toggleCode().run()'
                @click='editor?.chain().focus().toggleCode().run()'
            >
                <NIcon size='20'>
                    <CodeIcon />
                </NIcon>
                Code
            </button>
            <button @click='editor?.chain().focus().unsetAllMarks().run()'>
                <NIcon size='20'>
                    <TextClearFormat />
                </NIcon>
                Clear Mark
            </button>
            <button @click='editor?.chain().focus().clearNodes().run()'>
                <NIcon size='20'>
                    <TextClearFormat />
                </NIcon>
                Clear Nodes
            </button>
            <button :class="{ 'is-active': editor.isActive('paragraph') }"
                    @click='editor?.chain().focus().setParagraph().run()'>
                <NIcon size='20'>
                    <ParagraphIcon />
                </NIcon>
            </button>
            <button
                :class="{ 'is-active': editor.isActive('heading', { level: 1 }) }"
                @click='editor?.chain().focus().toggleHeading({ level: 1 }).run()'
            >
                H1
            </button>
            <button
                :class="{ 'is-active': editor.isActive('heading', { level: 2 }) }"
                @click='editor?.chain().focus().toggleHeading({ level: 2 }).run()'
            >
                H2
            </button>
            <button
                :class="{ 'is-active': editor.isActive('heading', { level: 3 }) }"
                @click='editor?.chain().focus().toggleHeading({ level: 3 }).run()'
            >
                H3
            </button>
            <button
                :class="{ 'is-active': editor.isActive('heading', { level: 4 }) }"
                @click='editor?.chain().focus().toggleHeading({ level: 4 }).run()'
            >
                H4
            </button>
            <button
                :class="{ 'is-active': editor.isActive('heading', { level: 5 }) }"
                @click='editor?.chain().focus().toggleHeading({ level: 5 }).run()'
            >
                H5
            </button>
            <button
                :class="{ 'is-active': editor.isActive('heading', { level: 6 }) }"
                @click='editor?.chain().focus().toggleHeading({ level: 6 }).run()'
            >
                H6
            </button>
            <button
                :class="{ 'is-active': editor.isActive('bulletList') }"
                @click='editor?.chain().focus().toggleBulletList().run()'
            >
                <NIcon>
                    <ListBulleted />
                </NIcon>
            </button>
            <button
                :class="{ 'is-active': editor.isActive('orderedList') }"
                @click='editor?.chain().focus().toggleOrderedList().run()'
            >
                <NIcon>
                    <ListNumbered />
                </NIcon>
            </button>
            <button
                :class="{ 'is-active': editor.isActive('codeBlock') }"
                @click='editor?.chain().focus().toggleCodeBlock().run()'
            >
                <NIcon>
                    <CodeIcon />
                </NIcon>
                Code Block
            </button>
            <button
                :class="{ 'is-active': editor.isActive('blockquote') }"
                @click='editor?.chain().focus().toggleBlockquote().run()'
            >
                <NIcon>
                    <Quotes />
                </NIcon>
                Quote
            </button>
            <button @click='editor?.chain().focus().setHorizontalRule().run()'>Horizontal Rule</button>
            <button @click='editor?.chain().focus().setHardBreak().run()'>
                <NIcon>
                    <TextNewLine />
                </NIcon>
                Hard Break
            </button>
            <button :disabled='!editor.can().chain().focus().undo().run()'
                    @click='editor?.chain().focus().undo().run()'>
                <NIcon>
                    <Undo />
                </NIcon>
                Undo
            </button>
            <button :disabled='!editor.can().chain().focus().redo().run()'
                    @click='editor?.chain().focus().redo().run()'>
                <NIcon>
                    <Redo />
                </NIcon>
                Redo
            </button>
        </div>
        <editor-content v-if='editor' :editor='editor' />
    </div>
</template>
