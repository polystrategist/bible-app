import { bible } from '../../modules';

type AvailableBible = string | { file_name: string; title?: string | null };

/**
 * This will get the bibles and its details.
 * Enriches each installed module with metadata from the module JSON when available.
 * @returns
 */
export async function getDownloadedBible(): Promise<Array<any>> {
    const files = (await window.browserWindow.getAvailableBibles()) as AvailableBible[];

    return files.map((item) => {
        const fileName = typeof item === 'string' ? item : item.file_name;
        const titleOverride = typeof item === 'string' ? '' : (item.title ?? '').trim();
        const meta = bible.find((b) => b.file_name === fileName);

        return {
            file_name: fileName,
            title: titleOverride || meta?.title || fileName.replace('.SQLite3', '').replace('.db', ''),
            description: meta?.description ?? '',
            short_name: meta?.version_short_name_and_date ?? '',
            language: meta?.language_full ?? '',
            module_type: (meta as any)?.module_type ?? '',
            year: (meta as any)?.year ?? null,
        };
    });
}
