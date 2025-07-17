import BibleModules from "./Modules/Bible";
import CommentariesModules from './Modules/Commentaries';

export type MODULE_BIBLE_TYPE = {
    file_name: string;
    language: string;
    language_full: string;
    title: string;
    description: string;
    download_link: string;
    is_zipped?: boolean | undefined | null;
};

export const bible: MODULE_BIBLE_TYPE[] = BibleModules;

const fileNames = bible.map(entry => entry.file_name).filter(Boolean);
const duplicates = fileNames.filter((name, index, self) => self.indexOf(name) !== index);

if (duplicates.length > 0) {
    throw new Error("Duplicate file_name(s) found: " + [...new Set(duplicates)].join(", "));
}

export const commentaries = CommentariesModules;
