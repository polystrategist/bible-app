export const GITHUB_REPO_OWNER = 'polystrategist';
export const GITHUB_REPO_NAME = 'bible-app';

export const GITHUB_REPO_URL = `https://github.com/${GITHUB_REPO_OWNER}/${GITHUB_REPO_NAME}`;
export const GITHUB_RELEASES_URL = `${GITHUB_REPO_URL}/releases`;
export const GITHUB_LATEST_RELEASE_URL = `${GITHUB_RELEASES_URL}/latest`;
export const GITHUB_ISSUES_URL = `${GITHUB_REPO_URL}/issues`;
export const GITHUB_SPONSORS_URL = 'https://github.com/sponsors/JenuelDev';

export const LICENSE_NAME = 'PolyForm Noncommercial License 1.0.0';

/** Build a raw GitHub content URL for a file on the default branch. */
export function githubRawUrl(filePath: string): string {
    const normalized = filePath.replace(/^\/+/, '');
    return `${GITHUB_REPO_URL}/raw/main/${normalized}`;
}
