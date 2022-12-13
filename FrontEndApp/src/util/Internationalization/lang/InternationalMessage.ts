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
}

type InternationalMessageTypeOptional<Type, Key extends keyof Type> = Omit<Type, Key> & Partial<Pick<Type, Key>>;

export type InternationalMessageType = InternationalMessageTypeOptional<InternationalMessageInterface, 'Sermons'>;
