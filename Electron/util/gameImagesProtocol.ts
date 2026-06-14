import { app, protocol } from 'electron';
import fs from 'fs';
import path from 'path';
import Log from 'electron-log';

/**
 * Custom `gameimg://` protocol that serves the 4 Pictures 1 Word images from
 * `userData/Games/fp_images`. A custom scheme is used instead of `file://`
 * because the renderer runs on an http(s)/app origin where `webSecurity`
 * blocks direct `file://` access. Usage from the renderer:
 *
 *     <img src="gameimg://img/lv1_img1.jpg" />
 */

const SCHEME = 'gameimg';

const MIME: Record<string, string> = {
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.webp': 'image/webp',
    '.gif': 'image/gif',
};

/** Must be called at module load, BEFORE app `ready`. */
export function registerGameImagesScheme(): void {
    protocol.registerSchemesAsPrivileged([
        {
            scheme: SCHEME,
            privileges: { standard: true, secure: true, supportFetchAPI: true, bypassCSP: true },
        },
    ]);
}

/** Must be called AFTER app `ready` (and after the images are seeded). */
export function registerGameImagesProtocol(): void {
    const baseDir = path.join(app.getPath('userData'), 'Games', 'fp_images');

    protocol.handle(SCHEME, async (request) => {
        try {
            const url = new URL(request.url);
            // Only the final path segment is honoured — guards against traversal.
            const requested = decodeURIComponent(url.pathname).replace(/^\/+/, '');
            const fileName = path.basename(requested);
            if (!fileName) return new Response('Not found', { status: 404 });

            const filePath = path.join(baseDir, fileName);
            if (!fs.existsSync(filePath)) {
                return new Response('Not found', { status: 404 });
            }

            const data = await fs.promises.readFile(filePath);
            const ext = path.extname(fileName).toLowerCase();
            return new Response(new Uint8Array(data), {
                status: 200,
                headers: { 'content-type': MIME[ext] ?? 'application/octet-stream' },
            });
        } catch (err) {
            Log.error('[gameimg] failed to serve image:', err);
            return new Response('Internal error', { status: 500 });
        }
    });
}
