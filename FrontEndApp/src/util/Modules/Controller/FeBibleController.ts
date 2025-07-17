import { bible } from '../../modules';

/**
 * This will get the bibles and its details.
 * @returns
 */
export async function getDownloadedBible(): Promise<Array<any>> {
    const files = await window.browserWindow.getAvailableBibles();

    return files.map((fileName: string) => {
        return {
            file_name: fileName,
            title: fileName.replace('.SQLite3', '').replace('.db', '')
        }
    })
}
