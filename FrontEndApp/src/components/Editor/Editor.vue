<script lang="ts" setup>
import { EditorContent, useEditor } from '@tiptap/vue-3';
import { NIcon, NButton, NPopselect } from 'naive-ui';
import { FileCodeRegular } from '@vicons/fa';
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
    Undo,
    ChevronDown,
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
import CodeBlock from '@tiptap/extension-code-block';
import { ref } from 'vue';

const props = defineProps({
    modelValue: {
        type: [String],
        default: '',
    },
    overflow: {
        type: Boolean,
        default: false,
    },
    buttonActions: {
        type: Array,
        default: [
            'bold',
            'italic',
            'underline',
            'strike',
            'code',
            'paragraph',
            'heading1',
            'heading2',
            'heading3',
            'heading4',
            'heading5',
            'heading6',
            'bulletList',
            'orderedList',
            'codeBlock',
            'blockQuote',
            'horizontalRule',
            'hardBreak',
            'undo',
            'redo',
        ],
    },
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
                'cursor-text before:content-[attr(data-placeholder)] before:absolute before:text-mauve-11 before:opacity-50 before-pointer-events-none p-0',
        }),
    ],
    onUpdate: ({ editor }) => {
        emits('update:modelValue', editor.getHTML());
    },
});

function toggleHeading(level: number | any) {
    editor?.value?.chain().focus().toggleHeading({ level: level }).run();
}
</script>

<template>
    <div :class="{'flex flex-col h-full': overflow}">
        <div v-if="editor" class="editor-buttons">
            <NPopselect
                trigger="click"
                @update:value="toggleHeading"
                :options="
                    [1, 2, 3, 4, 5, 6].map((level) => {
                        const isActive = editor?.isActive('heading', { level: level });

                        return {
                            label: ` ${isActive ? '✅' : ''} Heading ${level}`,
                            value: level,
                            disabled: isActive,
                        };
                    })
                "
            >
                <NButton
                    quaternary
                    icon-placement="right"
                    :class="{
                        'is-active': [1, 2, 3, 4, 5, 6].some((level) => editor?.isActive('heading', { level })),
                    }"
                    size="small"
                >
                    <template #icon>
                        <NIcon>
                            <ChevronDown />
                        </NIcon>
                    </template>
                    <span class="!font-900">H</span>
                </NButton>
            </NPopselect>
            <NButton
                v-if="buttonActions.includes('bold')"
                :class="{ 'is-active': editor.isActive('bold') }"
                :disabled="!editor.can().chain().focus().toggleBold().run()"
                @click="editor?.chain().focus().toggleBold().run()"
                quaternary
                size="small"
            >
                <template #icon>
                    <NIcon size="20">
                        <TextBold />
                    </NIcon>
                </template>
            </NButton>
            <NButton
                v-if="buttonActions.includes('underline')"
                :class="{ 'is-active': editor.isActive('underline') }"
                :disabled="!editor.can().chain().focus().toggleUnderline().run()"
                @click="editor?.chain().focus().toggleUnderline().run()"
                quaternary
                size="small"
            >
                <template #icon>
                    <NIcon size="20">
                        <TextUnderline />
                    </NIcon>
                </template>
            </NButton>
            <NButton
                v-if="buttonActions.includes('italic')"
                :class="{ 'is-active': editor.isActive('italic') }"
                :disabled="!editor.can().chain().focus().toggleItalic().run()"
                @click="editor?.chain().focus().toggleItalic().run()"
                quaternary
                size="small"
            >
                <template #icon>
                    <NIcon size="20">
                        <TextItalic />
                    </NIcon>
                </template>
            </NButton>
            <NButton
                v-if="buttonActions.includes('strike')"
                :class="{ 'is-active': editor.isActive('strike') }"
                :disabled="!editor.can().chain().focus().toggleStrike().run()"
                @click="editor?.chain().focus().toggleStrike().run()"
                quaternary
                size="small"
            >
                <template #icon>
                    <NIcon size="20">
                        <TextStrikethrough />
                    </NIcon>
                </template>
            </NButton>
            <NButton
                v-if="buttonActions.includes('code')"
                :class="{ 'is-active': editor.isActive('code') }"
                :disabled="!editor.can().chain().focus().toggleCode().run()"
                @click="editor?.chain().focus().toggleCode().run()"
                quaternary
                size="small"
            >
                <NIcon size="20">
                    <CodeIcon />
                </NIcon>
                Code
            </NButton>
            <NButton
                v-if="buttonActions.includes('clearFormat')"
                @click="editor?.chain().focus().unsetAllMarks().run()"
                quaternary
                size="small"
            >
                <NIcon size="20">
                    <TextClearFormat />
                </NIcon>
                Clear Mark
            </NButton>
            <NButton
                v-if="buttonActions.includes('clearNodes')"
                @click="editor?.chain().focus().clearNodes().run()"
                quaternary
                size="small"
            >
                <NIcon size="20">
                    <TextClearFormat />
                </NIcon>
                Clear Nodes
            </NButton>
            <NButton
                v-if="buttonActions.includes('paragraph')"
                :class="{ 'is-active': editor.isActive('paragraph') }"
                @click="editor?.chain().focus().setParagraph().run()"
                quaternary
                size="small"
            >
                <NIcon size="20">
                    <ParagraphIcon />
                </NIcon>
            </NButton>
            <NButton
                v-if="buttonActions.includes('bulletList')"
                :class="{ 'is-active': editor.isActive('bulletList') }"
                @click="editor?.chain().focus().toggleBulletList().run()"
                quaternary
                size="small"
            >
                <NIcon>
                    <ListBulleted />
                </NIcon>
            </NButton>
            <NButton
                v-if="buttonActions.includes('orderedList')"
                :class="{ 'is-active': editor.isActive('orderedList') }"
                @click="editor?.chain().focus().toggleOrderedList().run()"
                quaternary
                size="small"
            >
                <NIcon>
                    <ListNumbered />
                </NIcon>
            </NButton>
            <NButton
                v-if="buttonActions.includes('hardBreak')"
                @click="editor?.chain().focus().setHardBreak().run()"
                quaternary
                size="small"
            >
                <NIcon>
                    <TextNewLine />
                </NIcon>
            </NButton>
            <NButton
                v-if="buttonActions.includes('codeBlock')"
                :class="{ 'is-active': editor.isActive('codeBlock') }"
                @click="editor?.chain().focus().toggleCodeBlock().run()"
                quaternary
                size="small"
            >
                <NIcon>
                    <FileCodeRegular />
                </NIcon>
                Code Block
            </NButton>
            <NButton
                v-if="buttonActions.includes('blockquote')"
                :class="{ 'is-active': editor.isActive('blockquote') }"
                @click="editor?.chain().focus().toggleBlockquote().run()"
                quaternary
                size="small"
            >
                <NIcon>
                    <Quotes />
                </NIcon>
                Quote
            </NButton>
            <NButton
                v-if="buttonActions.includes('horizontalRule')"
                @click="editor?.chain().focus().setHorizontalRule().run()"
                quaternary
                size="small"
            >
                Line Break
            </NButton>

            <NButton
                v-if="buttonActions.includes('undo')"
                :disabled="!editor.can().chain().focus().undo().run()"
                @click="editor?.chain().focus().undo().run()"
                quaternary
                size="small"
            >
                <NIcon>
                    <Undo />
                </NIcon>
            </NButton>
            <NButton
                v-if="buttonActions.includes('redo')"
                :disabled="!editor.can().chain().focus().redo().run()"
                @click="editor?.chain().focus().redo().run()"
                quaternary
                size="small"
            >
                <NIcon>
                    <Redo />
                </NIcon>
            </NButton>
        </div>
        <EditorContent :class="{'overflow-auto overflowing-div': overflow}" v-if="editor" :editor="editor" />
    </div>
</template>
