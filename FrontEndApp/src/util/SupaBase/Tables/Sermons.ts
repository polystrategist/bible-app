import { getPagination, supabase } from '../SupaBase';

/**
 * Get sermons
 * @param search
 * @param limit
 * @returns Array<array>
 * @throws error
 */
export async function fetchSermons(search: string | null = null, limit: number = 30, page: number = 1) {
    const { from, to } = getPagination(page, limit);
    let query = supabase.from('sermons').select().range(from, to);

    if (search && search != '') {
        query.or(
            `title.ilike.*${search}*,content.ilike.*${search}*,description.ilike.*${search}*,author.ilike.*${search}*,denomination.ilike.*${search}*,scripture.ilike.*${search}*`
        );
    }

    return await query;
}
