import { ipcMain, BrowserWindow } from 'electron';
import { app } from 'electron';
import { download } from 'electron-dl';
import { setupPortableMode } from '../../util/portable';
import fs from 'fs';
import extract from 'extract-zip';
import path from 'path';

setupPortableMode();
const dataPath = app.getPath('userData');
const filePath = dataPath + `\\modules\\bible\\`;
const commentariesPath = dataPath + `\\modules\\commentaries\\`;

async function extractZip(zipPath: string, destPath: string) {
    try {
        await extract(zipPath, { dir: destPath });
        return true;
    } catch (err) {
        return false;
    }
}

function ensureDirectoryExists(dirPath: string) {
    if (!fs.existsSync(dirPath)) {
        fs.mkdirSync(dirPath, { recursive: true });
        console.log('Created directory:', dirPath);
    }
}

function moveFilesWithCommentaries(dir: string) {
    fs.readdir(dir, (err, files) => {
        if (err) {
            console.error('Failed to read directory:', err);
            return;
        }

        files.forEach(file => {
            const filePath = path.join(dir, file);
            fs.stat(filePath, (err, stat) => {
                if (err) {
                    console.error('Error reading file stats:', err);
                    return;
                }

                if (stat.isDirectory() && file !== 'commentaries') {
                    moveFilesWithCommentaries(filePath); // Recurse into subdirectories
                } else if (stat.isFile() && file.toLowerCase().includes('commentaries')) {
                    // Ensure destination path exists before moving
                    ensureDirectoryExists(commentariesPath);

                    const destinationPath = path.join(commentariesPath, file);

                    fs.rename(filePath, destinationPath, (err) => {
                        if (err) {
                            console.error('Failed to move file:', filePath, err);
                        } else {
                            console.log(`Moved: ${filePath} → ${destinationPath}`);
                        }
                    });
                }
            });
        });
    });
}


async function downloadModuleUrls(mainWindow: BrowserWindow, urls: Array<string>, moduleData?: {
    title: string;
    description: string;
    is_zipped: boolean;
}) {
    await Promise.all(
        urls.map(async (url) => {
            await download(mainWindow, url, {
                directory: filePath,
                onProgress: (progressObj) => {
                    // Calculate the download progress percentage
                    const downloadPercentage = Math.floor(progressObj.percent);

                    // Update UI with progress percentage
                    mainWindow.webContents.send('download-module-progress', downloadPercentage);
                },
                onCompleted: async (item) => {
                    const downloadedFilePath = item.path;
                    console.log(downloadedFilePath);
                    console.log(moduleData);
                    const isZipFile = moduleData?.is_zipped && downloadedFilePath.endsWith('.zip');

                    if (!isZipFile) {
                        mainWindow.webContents.send('download-module-done');
                        return
                    }

                    // extract if its a zip file
                    const extractTo = filePath;

                    const isExtracted = await extractZip(downloadedFilePath, extractTo);

                    if (!isExtracted) {
                        mainWindow.webContents.send('download-module-done');
                        alert('Failed to extract zip file');
                        return
                    }

                    // Optionally remove zip after extraction
                    fs.unlink(downloadedFilePath, (err) => {
                        if (err) console.error('Failed to delete zip:', err);
                    });

                    // remove any file with commentaries in the file names
                    moveFilesWithCommentaries(filePath);

                    mainWindow.webContents.send('download-module-done');
                },
                onCancel: () => {
                    mainWindow.webContents.send('download-module-cancel');
                },
                overwrite: true,
                saveAs: false,
            });
        })
    );
}

export default (mainWindow: BrowserWindow) => {
    ipcMain.on('download', async (event, args) => {
        // console.log(args);
    });

    ipcMain.on('download-module', async (event, urls: Array<string>, moduleData?: {
        title: string;
        description: string;
        is_zipped: boolean;
    }) => {
        await downloadModuleUrls(mainWindow, urls, moduleData);
    });
};
