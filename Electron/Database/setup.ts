import { app } from 'electron';
import fs from 'fs';
import Path from 'path';
import UPath from 'upath';

const isPackaged = app.isPackaged;
// const isNightly = 
// console.log(process.env.IS_NIGHTLY)
const dataPath = app.getPath('appData') + (isPackaged ? '\\believers-sword' : '\\believers-sword-nightly');

export function setupDefaults() {
    const filePath = dataPath + `\\modules\\bible\\KJV1769+.SQLite3`;
    if (fs.existsSync(filePath)) {
        // do nothing
        console.log('File Exist');
    } else {
        // copy default bible to the <appData>/modules/bible
        // const path = Path.join(__dirname, './index.html');

        const path =
            isPackaged || true
                ? UPath.toUnix(UPath.join(__dirname, 'defaults', 'Modules', 'Bible', 'KJV1769+.SQLite3')).replace('app.asar/', '')
                : './../../defaults/Modules/Bible/KJV1769+.SQLite3';

        // console.log(path);
        console.log('File Does Not Exist', path);
    }
}
