export type searchBibleType = Array<{
    book_number: number;
    chapter: number;
    verse: number;
    version: Array<{
        text: string;
        version: string;
    }>
}>;

export type bookmarksType = {
    [key: string]: {
        book_number: number;
        chapter: number;
        verse: number;
    }
}

export type SAVED_CLIP_NOTE_TYPE = {
    [key: string] : {
        book_number: number;
        chapter: number;
        color: string;
        content: string;
        created_at: number | string;
        id: number;
        key: string;
        updated_at: string | number;
        verse: number;
    }
}