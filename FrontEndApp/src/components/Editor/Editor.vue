<script setup lang="ts">
import { useEditor, EditorContent } from '@tiptap/vue-3';
import StarterKit from '@tiptap/starter-kit';
import { NIcon } from 'naive-ui';
import {
    Code,
    ListBulleted,
    ListNumbered,
    Paragraph,
    Quotes,
    Redo,
    TextBold,
    TextClearFormat,
    TextItalic,
    TextNewLine,
    TextStrikethrough,
    TextUnderline,
    Undo,
} from '@vicons/carbon';
import Underline from '@tiptap/extension-underline';
import Placeholder from '@tiptap/extension-placeholder';

const props = defineProps({
    modelValue: {
        type: [String],
        default: '',
    },
});
const emits = defineEmits(['update:modelValue']);

const editor: any = useEditor({
    content: props.modelValue,
    extensions: [
        StarterKit,
        Underline,
        Placeholder.configure({
            placeholder: 'Write Something Here 😁👍',
            emptyEditorClass:
                'cursor-text before:content-[attr(data-placeholder)] before:absolute before:top-3 before:left-5 before:text-mauve-11 before:opacity-50 before-pointer-events-none',
        }),
    ],
    onUpdate: ({ editor }) => {
        emits('update:modelValue', editor.getHTML());
    },
});
</script>

<template>
    <div>
        <div v-if="editor" class="editor-buttons">
            <button
                @click="editor.chain().focus().toggleBold().run()"
                :disabled="!editor.can().chain().focus().toggleBold().run()"
                :class="{ 'is-active': editor.isActive('bold') }"
            >
                <NIcon size="20">
                    <TextBold />
                </NIcon>
            </button>
            <button
                @click="editor.chain().focus().toggleUnderline().run()"
                :disabled="!editor.can().chain().focus().toggleUnderline().run()"
                :class="{ 'is-active': editor.isActive('underline') }"
            >
                <NIcon size="20">
                    <TextUnderline />
                </NIcon>
            </button>
            <button
                @click="editor.chain().focus().toggleItalic().run()"
                :disabled="!editor.can().chain().focus().toggleItalic().run()"
                :class="{ 'is-active': editor.isActive('italic') }"
            >
                <NIcon size="20">
                    <TextItalic />
                </NIcon>
            </button>
            <button
                @click="editor.chain().focus().toggleStrike().run()"
                :disabled="!editor.can().chain().focus().toggleStrike().run()"
                :class="{ 'is-active': editor.isActive('strike') }"
            >
                <NIcon size="20">
                    <TextStrikethrough />
                </NIcon>
            </button>
            <button
                @click="editor.chain().focus().toggleCode().run()"
                :disabled="!editor.can().chain().focus().toggleCode().run()"
                :class="{ 'is-active': editor.isActive('code') }"
            >
                <NIcon size="20">
                    <Code />
                </NIcon>
                Code
            </button>
            <button @click="editor.chain().focus().unsetAllMarks().run()">
                <NIcon size="20">
                    <TextClearFormat />
                </NIcon>
                Clear Mark
            </button>
            <button @click="editor.chain().focus().clearNodes().run()">
                <NIcon size="20">
                    <TextClearFormat />
                </NIcon>
                Clear Nodes
            </button>
            <button @click="editor.chain().focus().setParagraph().run()" :class="{ 'is-active': editor.isActive('paragraph') }">
                <NIcon size="20">
                    <Paragraph />
                </NIcon>
            </button>
            <button
                @click="editor.chain().focus().toggleHeading({ level: 1 }).run()"
                :class="{ 'is-active': editor.isActive('heading', { level: 1 }) }"
            >
                H1
            </button>
            <button
                @click="editor.chain().focus().toggleHeading({ level: 2 }).run()"
                :class="{ 'is-active': editor.isActive('heading', { level: 2 }) }"
            >
                H2
            </button>
            <button
                @click="editor.chain().focus().toggleHeading({ level: 3 }).run()"
                :class="{ 'is-active': editor.isActive('heading', { level: 3 }) }"
            >
                H3
            </button>
            <button
                @click="editor.chain().focus().toggleHeading({ level: 4 }).run()"
                :class="{ 'is-active': editor.isActive('heading', { level: 4 }) }"
            >
                H4
            </button>
            <button
                @click="editor.chain().focus().toggleHeading({ level: 5 }).run()"
                :class="{ 'is-active': editor.isActive('heading', { level: 5 }) }"
            >
                H5
            </button>
            <button
                @click="editor.chain().focus().toggleHeading({ level: 6 }).run()"
                :class="{ 'is-active': editor.isActive('heading', { level: 6 }) }"
            >
                H6
            </button>
            <button
                @click="editor.chain().focus().toggleBulletList().run()"
                :class="{ 'is-active': editor.isActive('bulletList') }"
            >
                <NIcon>
                    <ListBulleted />
                </NIcon>
            </button>
            <button
                @click="editor.chain().focus().toggleOrderedList().run()"
                :class="{ 'is-active': editor.isActive('orderedList') }"
            >
                <NIcon>
                    <ListNumbered />
                </NIcon>
            </button>
            <button
                @click="editor.chain().focus().toggleCodeBlock().run()"
                :class="{ 'is-active': editor.isActive('codeBlock') }"
            >
                <NIcon>
                    <Code />
                </NIcon>
                Code Block
            </button>
            <button
                @click="editor.chain().focus().toggleBlockquote().run()"
                :class="{ 'is-active': editor.isActive('blockquote') }"
            >
                <NIcon>
                    <Quotes />
                </NIcon>
                Qoute
            </button>
            <button @click="editor.chain().focus().setHorizontalRule().run()">Horizontal Rule</button>
            <button @click="editor.chain().focus().setHardBreak().run()">
                <NIcon><TextNewLine /></NIcon> Hard Break
            </button>
            <button @click="editor.chain().focus().undo().run()" :disabled="!editor.can().chain().focus().undo().run()">
                <NIcon>
                    <Undo />
                </NIcon>
                Undo
            </button>
            <button @click="editor.chain().focus().redo().run()" :disabled="!editor.can().chain().focus().redo().run()">
                <NIcon>
                    <Redo />
                </NIcon>
                Redo
            </button>
        </div>
        <editor-content :editor="editor" />
    </div>
</template>
