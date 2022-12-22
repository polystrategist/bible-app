import { ipcMain } from 'electron';
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
            console.log(e);
        }
    });

    ipcMain.handle('deletePrayerListItem', async (event, key: string | number) => {
        try {
            return await StoreDB(tableName).where('key', key).del();
        } catch (e) {
            console.log(e);
        }
    });

    ipcMain.handle(
        'getPrayerLists',
        async (event, args: { status: string | null; search: null | string } = { search: null, status: null }) => {
            try {
                return await StoreDB(tableName)
                    .select()
                    .where(function (query) {
                        if (args.status) query.where('status', args.status);
                        if (args.search) query.whereLike('content', `%${args.search}%`);
                    })
                    .then((row) => {
                        return row;
                    });
            } catch (e) {
                console.log(e);
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
                console.log(e);
            }
        }
    );
};
