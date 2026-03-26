import { ipcMain } from 'electron';
import Log from 'electron-log';
import { StoreDB } from '../../DataBase/DataBase';
import { logSyncChange } from '../../DataBase/SyncDB';

const tableName = 'prayer_lists';

export default () => {
    ipcMain.handle('resetPrayerListItems', async (event, args: { status: 'ongoing' | 'done'; data: Array<any> }) => {
        try {
            // Snapshot old items before the transaction for sync logging
            const oldItems = args.status === 'ongoing'
                ? await StoreDB(tableName).where('status', 'ongoing').select()
                : await StoreDB(tableName).where('status', 'done').select();

            // Atomic replace: delete old items and insert new ones in a single transaction
            await StoreDB.transaction(async (trx) => {
                if (args.status === 'ongoing') {
                    await trx(tableName).where('status', 'ongoing').del();
                } else {
                    await trx(tableName).where('status', 'done').del();
                }
                if (args.data.length > 0) {
                    await trx(tableName).insert(args.data);
                }
            });

            // Log sync changes only after transaction commits successfully
            for (const item of oldItems) {
                try {
                    await logSyncChange({
                        table_name: 'prayer_lists',
                        record_key: item.key,
                        action: 'deleted',
                        payload: item,
                        synced: 0,
                    });
                } catch (e) {
                    Log.error('Failed to log sync change for prayer list item deletion:', e);
                }
            }
            for (const item of args.data) {
                try {
                    await logSyncChange({
                        table_name: 'prayer_lists',
                        record_key: item.key,
                        action: 'created',
                        payload: item,
                        synced: 0,
                    });
                } catch (e) {
                    Log.error('Failed to log sync change for prayer list item creation:', e);
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
                try {
                    await logSyncChange({
                        table_name: 'prayer_lists',
                        record_key: String(key),
                        action: 'deleted',
                        payload: existingItem,
                        synced: 0,
                    });
                } catch (e) {
                    Log.error('Failed to log sync change for prayer list item deletion:', e);
                }
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
                try {
                    await logSyncChange({
                        table_name: 'prayer_lists',
                        record_key: args.key,
                        action: existingItem ? 'updated' : 'created',
                        payload: args,
                        synced: 0,
                    });
                } catch (e) {
                    Log.error('Failed to log sync change for prayer list item:', e);
                }

                return result;
            } catch (e) {
                Log.error(e);
            }
        }
    );
};
