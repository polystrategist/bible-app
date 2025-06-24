import { app } from "electron";
import path from 'path';

export function setupPortableMode() {
    if (process.env.PORTABLE_EXECUTABLE_DIR) {
        const exeDir = process.env.PORTABLE_EXECUTABLE_DIR!;
        app.setPath('userData', path.join(exeDir, 'user-data'));
        console.log('Running in portable mode. Using userData path:', app.getPath('userData'));
    }
}