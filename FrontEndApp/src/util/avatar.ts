import { computed } from 'vue';
import { useAuthStore } from '../store/authStore';

export type AvatarSize = 400 | 300 | 100 | 50 | 25;

const STORAGE_BASE = `${import.meta.env.VITE_API_BASE_URL}/storage`;

// Load every default profile image eagerly.
// Keys are paths relative to this file, e.g.
//   '../assets/default_profile_pictures/image1/400x400.jpg'
const defaultProfileImages = import.meta.glob(
    '../assets/default_profile_pictures/**/*.jpg',
    { eager: true, import: 'default' },
) as Record<string, string>;

// Derive unique folder names from the glob keys (image1, image2, …)
// so the picker automatically reflects whatever folders are in the assets dir.
export const DEFAULT_PROFILE_NAMES: string[] = [...new Set(
    Object.keys(defaultProfileImages)
        .map((k) => k.match(/default_profile_pictures\/([^/]+)\//)?.[1])
        .filter((n): n is string => !!n),
)].sort();

/** Bundled asset URL for a default profile at the given size, or null if not found. */
export function getDefaultProfileUrl(name: string, size: AvatarSize): string | null {
    return defaultProfileImages[
        `../assets/default_profile_pictures/${name}/${size}x${size}.jpg`
    ] ?? null;
}

/**
 * Resolve the display URL for a profile_picture value at the requested size.
 * Pass localAvatarKey/Cache from authStore for offline support on uploaded images.
 */
export function resolveAvatarUrl(
    profilePicture: string | null | undefined,
    size: AvatarSize,
    localAvatarKey?: string | null,
    localAvatarCache?: string | null,
): string | null {
    if (!profilePicture) return null;

    if (profilePicture.startsWith('default:')) {
        return getDefaultProfileUrl(profilePicture.slice('default:'.length), size);
    }

    if (profilePicture.startsWith('upload:')) {
        const path = profilePicture.slice('upload:'.length);
        // 400px has a local base64 cache for offline display
        if (size === 400 && localAvatarKey === profilePicture && localAvatarCache) {
            return localAvatarCache;
        }
        return `${STORAGE_BASE}/${path}/${size}.jpg`;
    }

    return null;
}

/**
 * Composable — returns a computed avatar URL for the current user at the given size.
 * Drop in anywhere a reactive avatar URL is needed.
 */
export function useAvatarUrl(size: AvatarSize = 400) {
    const authStore = useAuthStore();
    return computed(() =>
        resolveAvatarUrl(
            authStore.user?.info?.profile_picture,
            size,
            authStore.localAvatarKey,
            authStore.localAvatarCache,
        ),
    );
}
