import { ipcMain } from 'electron';
import Log from 'electron-log';
import { StoreDB } from '../../DataBase/DataBase';
const tableName = 'prayer_lists';
export default () => {
    ipcMain.handle('resetPrayerListItems', async (event, args: { status: 'ongoing' | 'done'; data: Array<any> }) => {
        try {
            if (args.status == 'ongoing') {
                await StoreDB(tableName).where('status', '<>', 'done').del();
                await StoreDB(tableName).insert(args.data);
            } else if (args.status == 'done') {
                await StoreDB(tableName).where('status', '<>', 'ongoing').del();
                await StoreDB(tableName).insert(args.data);
            }
        } catch (e) {
            Log.error(e);
        }
    });

    ipcMain.handle('deletePrayerListItem', async (event, key: string | number) => {
        try {
            return await StoreDB(tableName).where('key', key).del();
        } catch (e) {
            Log.error(e);
        }
    });

    ipcMain.handle(
        'getPrayerLists',
        async (event, args: { status: string | null; search: null | string } = { search: null, status: null }) => {
            try {
                const query = StoreDB(tableName).select();
                
                if (args.status) query.where('status', args.status);
                if (args.search) query.whereLike('content', `%${args.search}%`);
                
                return await query;
            } catch (e) {
                Log.error(e);
                return [];
            }
        }
    );

    ipcMain.handle(
        'savePrayerItem',
        async (
            event,
            args: { title: string | null; content: string; group: string | null; key: string; status: null | 'done' | 'ongoing' }
        ) => {
            try {
                return await StoreDB(tableName).insert(args).onConflict('key').merge();
            } catch (e) {
                Log.error(e);
            }
        }
    );
};
