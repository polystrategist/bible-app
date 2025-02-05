import {
    NotebookSubsection24Filled,
    Bookmark24Filled,
    Highlight24Filled,
    Attach24Filled,
    NotebookSubsection24Regular,
    Bookmark24Regular,
    Highlight24Regular,
    Attach24Regular,
    BookLetter24Regular,
    BookLetter24Filled,
} from '@vicons/fluent';

type RightSideBarMenu = {
    title: string;
    key: string;
    icon: any;
    iconDark: any;
    show?: boolean;
};

export const rightSideBarMenus: RightSideBarMenu[] = [
    {
        title: 'Bible Versions',
        key: 'bible-lists',
        icon: NotebookSubsection24Regular,
        iconDark: NotebookSubsection24Filled,
    },
    {
        title: 'Bookmarks',
        key: 'bible-bookmarks',
        icon: Bookmark24Regular,
        iconDark: Bookmark24Filled,
    },
    {
        title: 'Highlights',
        key: 'bible-highlights',
        icon: Highlight24Regular,
        iconDark: Highlight24Filled,
    },
    {
        title: 'Clip Notes',
        key: 'bible-clip-notes',
        icon: Attach24Regular,
        iconDark: Attach24Filled,
    },
];

export const rightSideBarBottomMenu: RightSideBarMenu[] = [
    {
        title: 'dictionary',
        key: 'dictionary',
        icon: BookLetter24Regular,
        iconDark: BookLetter24Filled,
    },
    {
        title: 'references',
        key: 'references',
        icon: BookLetter24Regular,
        iconDark: BookLetter24Filled,
        show: false
    }
];
