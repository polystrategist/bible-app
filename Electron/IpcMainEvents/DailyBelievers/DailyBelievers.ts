import { ipcMain, net } from 'electron';

type LinkMetadata = {
    url: string;
    sourceType: 'website' | 'youtube';
    sourceDomain: string;
    title: string;
    description: string | null;
    thumbnailUrl: string | null;
};

function isYoutubeHost(host: string): boolean {
    const h = host.toLowerCase();
    return (
        h === 'youtube.com' ||
        h === 'www.youtube.com' ||
        h === 'm.youtube.com' ||
        h === 'youtu.be' ||
        h === 'music.youtube.com'
    );
}

function normalizeUrl(input: string): string {
    const trimmed = input.trim();
    if (trimmed.startsWith('http://') || trimmed.startsWith('https://')) return trimmed;
    return `https://${trimmed}`;
}

function fetchText(url: string, headers: Record<string, string>, timeoutMs = 12000): Promise<{ statusCode: number; body: string }> {
    return new Promise((resolve, reject) => {
        const request = net.request({ method: 'GET', url, redirect: 'follow' });
        for (const [k, v] of Object.entries(headers)) request.setHeader(k, v);

        const chunks: Buffer[] = [];
        const timer = setTimeout(() => {
            try { request.abort(); } catch { /* ignore */ }
            reject(new Error('Request timed out'));
        }, timeoutMs);

        request.on('response', (response) => {
            response.on('data', (c: Buffer) => chunks.push(c));
            response.on('end', () => {
                clearTimeout(timer);
                resolve({
                    statusCode: response.statusCode ?? 0,
                    body: Buffer.concat(chunks).toString('utf-8'),
                });
            });
            response.on('error', (err: Error) => {
                clearTimeout(timer);
                reject(err);
            });
        });
        request.on('error', (err) => {
            clearTimeout(timer);
            reject(err);
        });
        request.end();
    });
}

function metaContent(html: string, selectorAttr: 'property' | 'name', value: string): string | null {
    const re = new RegExp(
        `<meta[^>]*${selectorAttr}=["']${value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}["'][^>]*>`,
        'i'
    );
    const tag = html.match(re)?.[0];
    if (!tag) return null;
    const content = tag.match(/content=["']([^"']*)["']/i)?.[1];
    return content ? content.trim() : null;
}

function htmlTitleTag(html: string): string | null {
    const m = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
    return m ? m[1].replace(/\s+/g, ' ').trim() : null;
}

async function extractYoutube(url: string): Promise<LinkMetadata> {
    const oembed = `https://www.youtube.com/oembed?url=${encodeURIComponent(url)}&format=json`;
    const { statusCode, body } = await fetchText(oembed, {});
    if (statusCode !== 200) {
        throw new Error(`Could not load YouTube metadata (${statusCode}). Make sure the link is a public video.`);
    }
    const data = JSON.parse(body) as { title?: string; author_name?: string; thumbnail_url?: string };
    return {
        url,
        sourceType: 'youtube',
        sourceDomain: 'youtube.com',
        title: data.title ?? 'YouTube video',
        description: data.author_name ? `By ${data.author_name}` : null,
        thumbnailUrl: data.thumbnail_url ?? null,
    };
}

async function extractWebsite(url: string, domain: string): Promise<LinkMetadata> {
    const { statusCode, body } = await fetchText(url, {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) BelieversSwordBot/1.0',
        Accept: 'text/html,application/xhtml+xml',
    });
    if (statusCode >= 400) {
        throw new Error(`Could not load that page (${statusCode}). Check the link and try again.`);
    }

    const title =
        metaContent(body, 'property', 'og:title') ||
        metaContent(body, 'name', 'twitter:title') ||
        htmlTitleTag(body) ||
        domain;

    const description =
        metaContent(body, 'property', 'og:description') ||
        metaContent(body, 'name', 'twitter:description') ||
        metaContent(body, 'name', 'description');

    let image =
        metaContent(body, 'property', 'og:image') ||
        metaContent(body, 'name', 'twitter:image');
    if (image?.startsWith('//')) image = `https:${image}`;
    if (image?.startsWith('/')) {
        const parsed = new URL(url);
        image = `${parsed.protocol}//${parsed.host}${image}`;
    }

    return {
        url,
        sourceType: 'website',
        sourceDomain: domain,
        title,
        description,
        thumbnailUrl: image ?? null,
    };
}

export default () => {
    ipcMain.handle('dailyBelievers:extractMetadata', async (_event, rawUrl: string): Promise<LinkMetadata> => {
        const url = normalizeUrl(rawUrl);
        const parsed = new URL(url);
        const domain = parsed.host.replace(/^www\./, '');
        if (isYoutubeHost(parsed.host)) return extractYoutube(url);
        return extractWebsite(url, domain);
    });
};
