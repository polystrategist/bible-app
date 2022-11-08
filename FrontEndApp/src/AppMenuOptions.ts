import { Component, h } from 'vue';
import { NIcon } from 'naive-ui';
import { Book, Person, WindPower, MediaLibrary } from '@vicons/carbon';

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
    // {
    //     label: "Dance Dance Dance",
    //     key: "Dance Dance Dance",
    //     icon: renderIcon(Book),
    //     children: [
    //         {
    //             type: "group",
    //             label: "People",
    //             key: "people",
    //             children: [
    //                 {
    //                     label: "Narrator",
    //                     key: "narrator",
    //                     icon: renderIcon(Person),
    //                 },
    //                 {
    //                     label: "Sheep Man",
    //                     key: "sheep-man",
    //                     icon: renderIcon(Person),
    //                 },
    //             ],
    //         },
    //         {
    //             label: "Beverage",
    //             key: "beverage",
    //             icon: renderIcon(WindPower),
    //             children: [
    //                 {
    //                     label: "Whisky",
    //                     key: "whisky",
    //                 },
    //             ],
    //         },
    //         {
    //             label: "Food",
    //             key: "food",
    //             children: [
    //                 {
    //                     label: "Sandwich",
    //                     key: "sandwich",
    //                 },
    //             ],
    //         },
    //         {
    //             label: "The past increases. The future recedes.",
    //             key: "the-past-increases-the-future-recedes",
    //         },
    //     ],
    // },
];
