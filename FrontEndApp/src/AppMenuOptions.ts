import { Component, h } from 'vue';
import { NIcon } from 'naive-ui';
import { Book, MediaLibrary, UserProfile, Information } from '@vicons/carbon';

function renderIcon(icon: Component) {
    return () => h(NIcon, null, { default: () => h(icon) });
}

export const menuOptions = [
    {
        label: 'Read Bible',
        key: 'read-bible',
        icon: renderIcon(Book),
    },
    {
        label: 'Sermons',
        key: 'sermons',
        icon: renderIcon(MediaLibrary),
    },
    {
        label: 'Prayer List',
        key: '/prayer-list',
        icon: renderIcon(Book),
    },
];

export const bottomMenuOptions = [
    {
        label: 'Profile',
        key: '/profile',
        icon: renderIcon(UserProfile),
    },
    {
        label: 'About',
        key: '/about-page',
        icon: renderIcon(Information),
    },
];
