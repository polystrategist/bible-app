import data from './devotionals-data.json';

// Bump this number whenever you add OR edit any devotional entry
// (also update the "version" field in devotionals-data.json)
export const DEVOTIONALS_DATA_VERSION: number = data.version;

export const devotionalsData: Array<{
    day_number: number;
    title: string;
    pause: string;
    listen: string;
    think: string;
    pray: string;
    go_action: string;
    verses: string;
}> = data.devotionals;
