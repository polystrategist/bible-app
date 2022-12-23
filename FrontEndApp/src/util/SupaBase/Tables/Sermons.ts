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

    if (search) {
        query.ilike('title', `%${search}%`);
        query.ilike('content', `%${search}%`);
        query.ilike('description', `%${search}%`);
        query.ilike('author', `%${search}%`);
        query.ilike('denomination', `%${search}%`);
        query.ilike('scripture', `%${search}%`);
    }

    return await query;
}
