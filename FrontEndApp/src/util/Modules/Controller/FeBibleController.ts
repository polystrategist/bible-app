import { bible } from '../../modules';

/**
 * This will get the bibles and its details.
 * @returns
 */
export async function getDownloadedBible(): Promise<Array<any>> {
    const files = await window.browserWindow.getAvailableBibles();
    const listOfBibleModules = bible;
    return listOfBibleModules.filter((file) => files.includes(file.file_name));
}
