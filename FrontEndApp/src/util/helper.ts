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
