export interface InternationalMessageInterface {
    title: string;
    'read-bible': string;
    Sermons: string;
    'Prayer List': string;
    Profile: string;
    About: string;
    Settings: string;
    'Search Bible': string;
    'Bible List': string;
    Bookmarks: string;
    Search: string;
    'Are You sure?': string;
    Before: string;
    Next: string;
    'Bible Versions': string;
    Highlights: string;
    Nightly: string;
    copy: string;
    remove: string;
    'Clip Notes': string;
    note: string;
    close: string;
    'create new': string;
    'prayer list': string;
    new: string;
    done: string;
    edit: string;
    create: string;
    'save changes': string;
    cancel: string;
    'are you sure to remove this item': string;
    about: string;
    donate: string;
    dark: string;
    light: string;
}

type InternationalMessageTypeOptional<Type, Key extends keyof Type> = Omit<Type, Key> & Partial<Pick<Type, Key>>;

export type InternationalMessageType = InternationalMessageTypeOptional<InternationalMessageInterface, 'Sermons'>;
