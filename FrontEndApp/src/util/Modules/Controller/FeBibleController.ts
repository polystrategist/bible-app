import { bible } from '../../modules';

type AvailableBible =
    | string
    | {
          file_name: string;
          title?: string | null;
          short_name?: string | null;
          description?: string | null;
          year?: number | null;
          language?: string | null;
      };

export async function getDownloadedBible(): Promise<Array<any>> {
    const files = (await window.browserWindow.getAvailableBibles()) as AvailableBible[];

    return files.map((item) => {
        const fileName = typeof item === 'string' ? item : item.file_name;
        const api = typeof item === 'string' ? null : item;
        const meta = bible.find((b) => b.file_name === fileName);

        return {
            file_name: fileName,
            title:
                (api?.title ?? '').trim() ||
                meta?.title ||
                fileName.replace('.SQLite3', '').replace('.db', ''),
            description: ((api?.description ?? '').trim() || meta?.description) ?? '',
            short_name: ((api?.short_name ?? '').trim() || meta?.version_short_name_and_date) ?? '',
            language: ((api?.language ?? '').trim() || meta?.language_full) ?? '',
            module_type: (meta as any)?.module_type ?? '',
            year: api?.year ?? (meta as any)?.year ?? null,
            has_strongs: (meta as any)?.has_strongs ?? false,
            has_red_letters: (meta as any)?.has_red_letters ?? false,
        };
    });
}
