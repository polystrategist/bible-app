import { NIcon } from 'naive-ui';
import { Component, h } from 'vue';

export function renderIcon(icon: Component) {
    return () => h(NIcon, null, { default: () => h(icon) });
}
