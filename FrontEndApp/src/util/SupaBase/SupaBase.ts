import { createClient } from '@supabase/supabase-js';

// Create a single supabase client for interacting with your database
export const supabase = createClient(
    'https://ufzycbyenppkgamvgcfy.supabase.co',
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmenljYnllbnBwa2dhbXZnY2Z5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NjIxODU4NDQsImV4cCI6MTk3Nzc2MTg0NH0.AH7HLZ2wPyubQa4mzAbGGPAeEGcUPmSsW0A6o6qv5RA'
);

export const getPagination = (page: number, limit: number) => {
    const from = page == 1 ? 0 : page * limit - limit;
    const to = from + limit - 1;

    return { from, to };
};
