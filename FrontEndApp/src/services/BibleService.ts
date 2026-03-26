// BibleService.ts
// Abstracts Bible data access for both Electron and Web

export interface BibleService {
  getVerses(args: any): Promise<any[]>;
  getChapterHighlights(args: any): Promise<any[]>;
}

// Electron implementation
export const electronBibleService: BibleService = {
  async getVerses(args) {
    return window.browserWindow.getVerses(JSON.stringify(args));
  },
  async getChapterHighlights(args) {
    return window.browserWindow.getChapterHighlights(JSON.stringify(args));
  },
};

// Web (backend) implementation
export const webBibleService: BibleService = {
  async getVerses(args) {
    const res = await fetch('/api/bible/verses', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(args),
    });
    return res.json();
  },
  async getChapterHighlights(args) {
    const res = await fetch('/api/bible/chapter-highlights', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(args),
    });
    return res.json();
  },
};

// Auto-select implementation
export function getBibleService(): BibleService {
  if (window.isElectron) return electronBibleService;
  return webBibleService;
}
