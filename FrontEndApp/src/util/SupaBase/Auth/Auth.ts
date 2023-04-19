import { supabase } from '../SupaBase';

/**
 * check if user is signed in
 */
export async function isSignedIn() {
    const { data, error } = await supabase.auth.getUser();
    if (error) return false;
    return data;
}

/**
 * This is used for logging in. Return false if error, and return user if successful.
 * @param email
 * @param password
 */
export async function signInWithEmailAndPassword(email: string, password: string) {
    const { data, error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) {
        alert(error.message);
        return false;
    }
    return data;
}
