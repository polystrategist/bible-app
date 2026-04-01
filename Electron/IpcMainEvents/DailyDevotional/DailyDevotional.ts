import { ipcMain } from 'electron';
import { StoreDB } from '../../DataBase/DataBase';

function getDayOfYear(): number {
    const now = new Date();
    const start = new Date(now.getFullYear(), 0, 0);
    const diff = now.getTime() - start.getTime();
    const oneDay = 1000 * 60 * 60 * 24;
    return Math.floor(diff / oneDay);
}

export default () => {
    ipcMain.handle('getTodayDevotional', async () => {
        const dayOfYear = getDayOfYear();
        const day = Math.min(Math.max(dayOfYear, 1), 365);

        const row = await StoreDB('daily_devotionals')
            .where('day_number', day)
            .first();

        if (!row) return null;

        return {
            ...row,
            verses: JSON.parse(row.verses || '[]'),
        };
    });

    ipcMain.handle('getDevotionalByDay', async (_event, day: number) => {
        const row = await StoreDB('daily_devotionals')
            .where('day_number', day)
            .first();

        if (!row) return null;

        return {
            ...row,
            verses: JSON.parse(row.verses || '[]'),
        };
    });
};
