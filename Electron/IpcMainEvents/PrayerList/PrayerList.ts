import { ipcMain } from 'electron';
import Log from 'electron-log';
import { StoreDB } from '../../DataBase/DataBase';
import { logSyncChange } from '../../DataBase/SyncDB';

const tableName = 'prayer_lists';

export default () => {
    ipcMain.handle('resetPrayerListItems', async (event, args: { status: 'ongoing' | 'done'; data: Array<any> }) => {
        try {
            if (args.status == 'ongoing') {
                // Log deletions for old items
                const oldItems = await StoreDB(tableName).where('status', '<>', 'done').select();
                for (const item of oldItems) {
                    await logSyncChange({
                        table_name: 'prayer_lists',
                        record_key: item.key,
                        action: 'deleted',
                        payload: item,
                        synced: 0,
                    });
                }
                
                await StoreDB(tableName).where('status', '<>', 'done').del();
                await StoreDB(tableName).insert(args.data);
                
                // Log new items
                for (const item of args.data) {
                    await logSyncChange({
                        table_name: 'prayer_lists',
                        record_key: item.key,
                        action: 'created',
                        payload: item,
                        synced: 0,
                    });
                }
            } else if (args.status == 'done') {
                // Log deletions for old items
                const oldItems = await StoreDB(tableName).where('status', '<>', 'ongoing').select();
                for (const item of oldItems) {
                    await logSyncChange({
                        table_name: 'prayer_lists',
                        record_key: item.key,
                        action: 'deleted',
                        payload: item,
                        synced: 0,
                    });
                }
                
                await StoreDB(tableName).where('status', '<>', 'ongoing').del();
                await StoreDB(tableName).insert(args.data);
                
                // Log new items
                for (const item of args.data) {
                    await logSyncChange({
                        table_name: 'prayer_lists',
                        record_key: item.key,
                        action: 'created',
                        payload: item,
                        synced: 0,
                    });
                }
            }
        } catch (e) {
            Log.error(e);
        }
    });

    ipcMain.handle('deletePrayerListItem', async (event, key: string | number) => {
        try {
            const existingItem = await StoreDB(tableName).where('key', String(key)).first();
            
            if (existingItem) {
                // Log sync change before deletion
                await logSyncChange({
                    table_name: 'prayer_lists',
                    record_key: String(key),
                    action: 'deleted',
                    payload: existingItem,
                    synced: 0,
                });
            }
            
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
                const existingItem = await StoreDB(tableName).where('key', args.key).first();
                
                const result = await StoreDB(tableName).insert(args).onConflict('key').merge();
                
                // Log sync change
                await logSyncChange({
                    table_name: 'prayer_lists',
                    record_key: args.key,
                    action: existingItem ? 'updated' : 'created',
                    payload: args,
                    synced: 0,
                });
                
                return result;
            } catch (e) {
                Log.error(e);
            }
        }
    );
};
