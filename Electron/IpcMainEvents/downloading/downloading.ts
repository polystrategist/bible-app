import { ipcMain, BrowserWindow } from 'electron';
import { app } from 'electron';
import { download } from 'electron-dl';
import Log from 'electron-log';
import { setupPortableMode } from '../../util/portable';
import { parseEbibleSql, createBibleModule } from '../../util/ebibleConverter';
import fs from 'fs';
import extract from 'extract-zip';
import path from 'path';

setupPortableMode();
const dataPath = app.getPath('userData');
const filePath = dataPath + `\\modules\\bible\\`;
const commentariesPath = dataPath + `\\modules\\commentaries\\`;

async function extractZip(zipPath: string, destPath: string, file_name: string): Promise<boolean> {
    try {
        const extractToPath = path.join(destPath, 'extracted');

        // Ensure extraction path exists
        if (!fs.existsSync(extractToPath)) {
            fs.mkdirSync(extractToPath, { recursive: true });
        }

        // Extract the zip
        await extract(zipPath, { dir: extractToPath });

        // Read all files in the extracted directory
        const files = fs.readdirSync(extractToPath);

        for (const file of files) {
            const fullExtractedPath = path.join(extractToPath, file);

            // Only process files (skip folders)
            const stat = fs.statSync(fullExtractedPath);
            if (!stat.isFile()) continue;

            const dotIndex = file.indexOf('.');
            if (dotIndex === -1) continue;

            // Replace prefix before first dot
            const newFileName = file.replace(/^.*?\./, file_name + '.');
            const newFilePath = path.join(destPath, newFileName);

            // Move and rename the file to the main destPath
            fs.renameSync(fullExtractedPath, newFilePath);
            Log.info(`Renamed & moved: ${file} → ${newFileName}`);
        }

        // Clean up extracted folder
        fs.rmSync(extractToPath, { recursive: true, force: true });
        Log.info(`Removed temporary folder: ${extractToPath}`);

        return true;
    } catch (err) {
        Log.error('extractZip error:', err);
        return false;
    }
}

/**
 * Handle an eBible VPL zip: extract the .sql file, parse verses, create SQLite3 module.
 */
async function convertEbibleZip(zipPath: string, destPath: string, fileName: string): Promise<boolean> {
    const tempDir = path.join(destPath, 'ebible_temp');
    try {
        // Extract zip to temp directory
        if (!fs.existsSync(tempDir)) {
            fs.mkdirSync(tempDir, { recursive: true });
        }
        await extract(zipPath, { dir: tempDir });

        // Find the .sql file
        const files = fs.readdirSync(tempDir);
        const sqlFile = files.find(f => f.endsWith('.sql'));
        if (!sqlFile) {
            Log.error('eBible zip: no .sql file found inside the archive');
            return false;
        }

        const sqlContent = fs.readFileSync(path.join(tempDir, sqlFile), 'utf-8');
        const verses = parseEbibleSql(sqlContent);

        if (verses.length === 0) {
            Log.error('eBible zip: no valid verses parsed from SQL');
            return false;
        }

        // Ensure destination directory exists
        if (!fs.existsSync(destPath)) {
            fs.mkdirSync(destPath, { recursive: true });
        }

        const dbPath = path.join(destPath, fileName);
        await createBibleModule(dbPath, verses);

        Log.info(`eBible module created: ${fileName} (${verses.length} verses)`);
        return true;
    } catch (err) {
        Log.error('convertEbibleZip error:', err);
        return false;
    } finally {
        // Clean up temp directory
        if (fs.existsSync(tempDir)) {
            fs.rmSync(tempDir, { recursive: true, force: true });
        }
    }
}

async function ensureDirectoryExists(dirPath: string) {
    if (!fs.existsSync(dirPath)) {
        await fs.promises.mkdir(dirPath, { recursive: true });
        Log.info('Created directory:', dirPath);
    }
}

function moveFilesWithCommentaries(dir: string) {
    fs.readdir(dir, (err, files) => {
        if (err) {
            Log.error('Failed to read directory:', err);
            return;
        }

        files.forEach(file => {
            const filePath = path.join(dir, file);
            fs.stat(filePath, (err, stat) => {
                if (err) {
                    Log.error('Error reading file stats:', err);
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
                            Log.error('Failed to move file:', filePath, err);
                        } else {
                            Log.info(`Moved: ${filePath} → ${destinationPath}`);
                        }
                    });
                }
            });
        });
    });
}


async function downloadModuleUrls(mainWindow: BrowserWindow, urls: Array<string>, moduleData: {
    title: string;
    description: string;
    is_zipped: boolean;
    file_name: string;
    module_type?: string;
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
                    const isEbible = moduleData?.module_type === 'ebible';
                    const isZipFile = moduleData?.is_zipped && downloadedFilePath.endsWith('.zip');

                    // Non-zip file — nothing to process
                    if (!isZipFile) {
                        mainWindow.webContents.send('download-module-done');
                        return;
                    }

                    if (isEbible) {
                        // eBible: extract SQL from zip, parse, and create SQLite3 module
                        const success = await convertEbibleZip(downloadedFilePath, filePath, moduleData.file_name);

                        // Clean up zip
                        fs.unlink(downloadedFilePath, (err) => {
                            if (err) Log.error('Failed to delete eBible zip:', err);
                        });

                        if (!success) {
                            mainWindow.webContents.send('download-module-cancel');
                            return;
                        }

                        mainWindow.webContents.send('download-module-done');
                    } else {
                        // MyBible: extract zip and rename files
                        const isExtracted = await extractZip(downloadedFilePath, filePath, moduleData?.title);

                        if (!isExtracted) {
                            mainWindow.webContents.send('download-module-done');
                            return;
                        }

                        // Remove zip after extraction
                        fs.unlink(downloadedFilePath, (err) => {
                            if (err) console.error('Failed to delete zip:', err);

                            // Move any commentary files
                            moveFilesWithCommentaries(filePath);

                            mainWindow.webContents.send('download-module-done');
                        });
                    }
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

    ipcMain.on('download-module', async (event, urls: Array<string>, moduleData: {
        title: string;
        description: string;
        is_zipped: boolean;
        file_name: string;
        module_type?: string;
    }) => {
        await downloadModuleUrls(mainWindow, urls, moduleData).catch((err) => {
            Log.error('Download module error:', err);
            mainWindow.webContents.send('download-module-error', err.message);
        });
    });
};
