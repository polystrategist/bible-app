export interface BibleService {
  getVerses(args: any): Promise<any[]>;
  getChapterHighlights(args: any): Promise<any>;
}

export const bibleService: BibleService = {
  async getVerses(args) {
    return window.browserWindow.getVerses(JSON.stringify(args));
  },
  async getChapterHighlights(args) {
    return window.browserWindow.getChapterHighlights(JSON.stringify(args));
  },
};

export function getBibleService(): BibleService {
  return bibleService;
}
