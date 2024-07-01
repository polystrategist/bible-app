import { h } from 'vue';
import { Icon } from '@iconify/vue';

export function renderIcon(icon: string) {
    return () => h(Icon, { icon: icon });
}
