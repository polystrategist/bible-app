import { ipcMain } from 'electron';
import { StrongsDB } from '../../DataBase/DataBase';

export default () => {
    // Look up a single Strong's lexicon entry by its number (e.g. "G2424",
    // "H7225"). Returns the row or null when not found.
    ipcMain.handle('getStrongsDefinition', async (_event, strongNumber: string) => {
        const key = String(strongNumber ?? '').trim().toUpperCase();
        if (!key) return null;

        const row = await StrongsDB('strongs_dictionary')
            .where('strong_number', key)
            .first(
                'strong_number',
                'language',
                'lemma',
                'translit',
                'pronunciation',
                'derivation',
                'strongs_def',
                'kjv_def'
            );

        return row ?? null;
    });
};
