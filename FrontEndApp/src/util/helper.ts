import { NIcon } from 'naive-ui';
import { Component, h } from 'vue';
import { Icon } from '@iconify/vue';

export function renderIcon(icon: Component) {
    return () => h(NIcon, null, { default: () => h(icon) });
}
