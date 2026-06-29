PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS bible_versions (
    id INTEGER PRIMARY KEY,
    uuid TEXT NOT NULL UNIQUE,
    abbreviation TEXT NOT NULL,
    name TEXT NOT NULL,
    language_code TEXT NOT NULL DEFAULT 'en',
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    sync_status TEXT NOT NULL DEFAULT 'local' CHECK (sync_status IN ('local', 'synced', 'pending', 'conflict')),
    server_id TEXT,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    deleted_at TEXT
);

CREATE TABLE IF NOT EXISTS commentary_authors (
    id INTEGER PRIMARY KEY,
    uuid TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL,
    author_type TEXT NOT NULL CHECK (author_type IN ('ai', 'human', 'organization', 'mixed')),
    biography TEXT,
    website_url TEXT,
    language_code TEXT,
    sync_status TEXT NOT NULL DEFAULT 'local' CHECK (sync_status IN ('local', 'synced', 'pending', 'conflict')),
    server_id TEXT,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    deleted_at TEXT
);

CREATE TABLE IF NOT EXISTS commentary_collections (
    id INTEGER PRIMARY KEY,
    uuid TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    slug TEXT NOT NULL,
    description TEXT,
    collection_type TEXT NOT NULL CHECK (collection_type IN ('ai_generated', 'human_written', 'mixed')),
    primary_author_id INTEGER,
    default_bible_version_id INTEGER,
    language_code TEXT NOT NULL DEFAULT 'en',
    theological_perspective TEXT,
    license TEXT,
    copyright_notice TEXT,
    is_offline_available INTEGER NOT NULL DEFAULT 1 CHECK (is_offline_available IN (0, 1)),
    sync_status TEXT NOT NULL DEFAULT 'local' CHECK (sync_status IN ('local', 'synced', 'pending', 'conflict')),
    server_id TEXT,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    deleted_at TEXT,
    FOREIGN KEY (primary_author_id) REFERENCES commentary_authors(id) ON DELETE SET NULL,
    FOREIGN KEY (default_bible_version_id) REFERENCES bible_versions(id) ON DELETE SET NULL,
    UNIQUE (slug, language_code)
);

CREATE TABLE IF NOT EXISTS commentary_generation_batches (
    id INTEGER PRIMARY KEY,
    uuid TEXT NOT NULL UNIQUE,
    collection_id INTEGER,
    batch_name TEXT,
    generator_type TEXT NOT NULL DEFAULT 'ai' CHECK (generator_type IN ('ai', 'human', 'import', 'mixed')),
    model_name TEXT,
    model_provider TEXT,
    prompt_version TEXT,
    prompt_hash TEXT,
    generation_parameters TEXT,
    source_bible_version_id INTEGER,
    language_code TEXT NOT NULL DEFAULT 'en',
    started_at TEXT,
    completed_at TEXT,
    status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'reviewed', 'published', 'archived', 'rejected')),
    review_notes TEXT,
    sync_status TEXT NOT NULL DEFAULT 'local' CHECK (sync_status IN ('local', 'synced', 'pending', 'conflict')),
    server_id TEXT,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    deleted_at TEXT,
    FOREIGN KEY (collection_id) REFERENCES commentary_collections(id) ON DELETE SET NULL,
    FOREIGN KEY (source_bible_version_id) REFERENCES bible_versions(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS commentary_entries (
    id INTEGER PRIMARY KEY,
    uuid TEXT NOT NULL UNIQUE,
    collection_id INTEGER NOT NULL,
    author_id INTEGER,
    generation_batch_id INTEGER,
    bible_version_id INTEGER,
    book_id INTEGER NOT NULL CHECK (book_id BETWEEN 1 AND 66),
    chapter INTEGER CHECK (chapter IS NULL OR chapter >= 1),
    verse_start INTEGER CHECK (verse_start IS NULL OR verse_start >= 1),
    verse_end INTEGER CHECK (verse_end IS NULL OR verse_end >= 1),
    reference_scope TEXT NOT NULL CHECK (reference_scope IN ('book', 'chapter', 'verse_range', 'verse')),
    title TEXT,
    summary TEXT,
    content TEXT NOT NULL,
    application TEXT,
    prayer TEXT,
    key_points TEXT CHECK (key_points IS NULL OR json_valid(key_points)),
    study_questions TEXT CHECK (study_questions IS NULL OR json_valid(study_questions)),
    language_code TEXT NOT NULL DEFAULT 'en',
    theological_perspective TEXT,
    status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'reviewed', 'published', 'archived', 'rejected')),
    is_ai_generated INTEGER NOT NULL DEFAULT 0 CHECK (is_ai_generated IN (0, 1)),
    ai_model_name TEXT,
    ai_model_provider TEXT,
    ai_prompt_version TEXT,
    ai_generation_batch_uuid TEXT,
    ai_confidence REAL CHECK (ai_confidence IS NULL OR (ai_confidence >= 0.0 AND ai_confidence <= 1.0)),
    review_notes TEXT,
    word_count INTEGER CHECK (word_count IS NULL OR word_count >= 0),
    sync_status TEXT NOT NULL DEFAULT 'local' CHECK (sync_status IN ('local', 'synced', 'pending', 'conflict')),
    server_id TEXT,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    deleted_at TEXT,
    FOREIGN KEY (collection_id) REFERENCES commentary_collections(id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES commentary_authors(id) ON DELETE SET NULL,
    FOREIGN KEY (generation_batch_id) REFERENCES commentary_generation_batches(id) ON DELETE SET NULL,
    FOREIGN KEY (bible_version_id) REFERENCES bible_versions(id) ON DELETE SET NULL,
    CHECK (verse_end IS NULL OR verse_start IS NOT NULL),
    CHECK (verse_start IS NULL OR chapter IS NOT NULL),
    CHECK (verse_end IS NULL OR verse_end >= verse_start),
    CHECK (
        (reference_scope = 'book' AND chapter IS NULL AND verse_start IS NULL AND verse_end IS NULL) OR
        (reference_scope = 'chapter' AND chapter IS NOT NULL AND verse_start IS NULL AND verse_end IS NULL) OR
        (reference_scope = 'verse' AND chapter IS NOT NULL AND verse_start IS NOT NULL AND (verse_end IS NULL OR verse_end = verse_start)) OR
        (reference_scope = 'verse_range' AND chapter IS NOT NULL AND verse_start IS NOT NULL AND verse_end IS NOT NULL AND verse_end >= verse_start)
    )
);

CREATE TABLE IF NOT EXISTS commentary_entry_verses (
    id INTEGER PRIMARY KEY,
    uuid TEXT NOT NULL UNIQUE,
    commentary_entry_id INTEGER NOT NULL,
    bible_version_id INTEGER,
    book_id INTEGER NOT NULL CHECK (book_id BETWEEN 1 AND 66),
    chapter INTEGER NOT NULL CHECK (chapter >= 1),
    verse_start INTEGER NOT NULL CHECK (verse_start >= 1),
    verse_end INTEGER NOT NULL CHECK (verse_end >= verse_start),
    verse_commentary TEXT,
    status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'reviewed', 'published', 'archived', 'rejected')),
    sync_status TEXT NOT NULL DEFAULT 'local' CHECK (sync_status IN ('local', 'synced', 'pending', 'conflict')),
    server_id TEXT,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    deleted_at TEXT,
    FOREIGN KEY (commentary_entry_id) REFERENCES commentary_entries(id) ON DELETE CASCADE,
    FOREIGN KEY (bible_version_id) REFERENCES bible_versions(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS commentary_tags (
    id INTEGER PRIMARY KEY,
    uuid TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    description TEXT,
    sync_status TEXT NOT NULL DEFAULT 'local' CHECK (sync_status IN ('local', 'synced', 'pending', 'conflict')),
    server_id TEXT,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    deleted_at TEXT
);

CREATE TABLE IF NOT EXISTS commentary_entry_tags (
    commentary_entry_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    PRIMARY KEY (commentary_entry_id, tag_id),
    FOREIGN KEY (commentary_entry_id) REFERENCES commentary_entries(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES commentary_tags(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS commentary_sources (
    id INTEGER PRIMARY KEY,
    uuid TEXT NOT NULL UNIQUE,
    source_type TEXT NOT NULL CHECK (source_type IN ('book', 'article', 'website', 'journal', 'lexicon', 'bible', 'manuscript', 'sermon', 'other')),
    title TEXT NOT NULL,
    author TEXT,
    publisher TEXT,
    publication_date TEXT,
    url TEXT,
    isbn TEXT,
    doi TEXT,
    language_code TEXT,
    sync_status TEXT NOT NULL DEFAULT 'local' CHECK (sync_status IN ('local', 'synced', 'pending', 'conflict')),
    server_id TEXT,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    deleted_at TEXT
);

CREATE TABLE IF NOT EXISTS commentary_entry_sources (
    id INTEGER PRIMARY KEY,
    commentary_entry_id INTEGER NOT NULL,
    source_id INTEGER NOT NULL,
    citation_text TEXT,
    citation_location TEXT,
    source_url TEXT,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    FOREIGN KEY (commentary_entry_id) REFERENCES commentary_entries(id) ON DELETE CASCADE,
    FOREIGN KEY (source_id) REFERENCES commentary_sources(id) ON DELETE CASCADE,
    UNIQUE (commentary_entry_id, source_id, citation_location)
);

CREATE TABLE IF NOT EXISTS commentary_revisions (
    id INTEGER PRIMARY KEY,
    uuid TEXT NOT NULL UNIQUE,
    commentary_entry_id INTEGER NOT NULL,
    revision_number INTEGER NOT NULL CHECK (revision_number >= 1),
    revised_by_author_id INTEGER,
    revision_type TEXT NOT NULL DEFAULT 'edit' CHECK (revision_type IN ('create', 'edit', 'review', 'publish', 'archive', 'reject', 'restore')),
    title TEXT,
    summary TEXT,
    content TEXT,
    application TEXT,
    prayer TEXT,
    key_points TEXT CHECK (key_points IS NULL OR json_valid(key_points)),
    study_questions TEXT CHECK (study_questions IS NULL OR json_valid(study_questions)),
    status TEXT NOT NULL CHECK (status IN ('draft', 'reviewed', 'published', 'archived', 'rejected')),
    change_notes TEXT,
    sync_status TEXT NOT NULL DEFAULT 'local' CHECK (sync_status IN ('local', 'synced', 'pending', 'conflict')),
    server_id TEXT,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    deleted_at TEXT,
    FOREIGN KEY (commentary_entry_id) REFERENCES commentary_entries(id) ON DELETE CASCADE,
    FOREIGN KEY (revised_by_author_id) REFERENCES commentary_authors(id) ON DELETE SET NULL,
    UNIQUE (commentary_entry_id, revision_number)
);

CREATE TABLE IF NOT EXISTS commentary_generation_progress (
    id INTEGER PRIMARY KEY,
    uuid TEXT NOT NULL UNIQUE,
    collection_id INTEGER NOT NULL,
    language_code TEXT NOT NULL DEFAULT 'en',
    current_book_id INTEGER NOT NULL DEFAULT 1 CHECK (current_book_id BETWEEN 1 AND 66),
    current_chapter INTEGER NOT NULL DEFAULT 1 CHECK (current_chapter >= 1),
    last_completed_book_id INTEGER CHECK (last_completed_book_id IS NULL OR last_completed_book_id BETWEEN 1 AND 66),
    last_completed_chapter INTEGER CHECK (last_completed_chapter IS NULL OR last_completed_chapter >= 1),
    target_book_id INTEGER NOT NULL DEFAULT 66 CHECK (target_book_id BETWEEN 1 AND 66),
    target_chapter INTEGER,
    chapters_per_batch INTEGER NOT NULL DEFAULT 5 CHECK (chapters_per_batch >= 1),
    status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'reviewed', 'published', 'archived', 'rejected')),
    generation_batch_id INTEGER,
    sync_status TEXT NOT NULL DEFAULT 'local' CHECK (sync_status IN ('local', 'synced', 'pending', 'conflict')),
    server_id TEXT,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    deleted_at TEXT,
    FOREIGN KEY (collection_id) REFERENCES commentary_collections(id) ON DELETE CASCADE,
    FOREIGN KEY (generation_batch_id) REFERENCES commentary_generation_batches(id) ON DELETE SET NULL,
    UNIQUE (collection_id, language_code)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_commentary_entries_unique_active_reference
ON commentary_entries (
    collection_id,
    book_id,
    COALESCE(chapter, 0),
    COALESCE(verse_start, 0),
    COALESCE(verse_end, 0),
    COALESCE(bible_version_id, 0),
    language_code
)
WHERE deleted_at IS NULL;

CREATE UNIQUE INDEX IF NOT EXISTS idx_commentary_entry_verses_unique_active_reference
ON commentary_entry_verses (
    commentary_entry_id,
    book_id,
    chapter,
    verse_start,
    verse_end,
    COALESCE(bible_version_id, 0)
)
WHERE deleted_at IS NULL;

CREATE INDEX IF NOT EXISTS idx_commentary_entries_reference
ON commentary_entries (book_id, chapter, verse_start, verse_end)
WHERE deleted_at IS NULL;

CREATE INDEX IF NOT EXISTS idx_commentary_entries_collection_status
ON commentary_entries (collection_id, status, language_code)
WHERE deleted_at IS NULL;

CREATE INDEX IF NOT EXISTS idx_commentary_entries_author
ON commentary_entries (author_id)
WHERE deleted_at IS NULL;

CREATE INDEX IF NOT EXISTS idx_commentary_entries_generation_batch
ON commentary_entries (generation_batch_id)
WHERE deleted_at IS NULL;

CREATE INDEX IF NOT EXISTS idx_commentary_entries_sync_status
ON commentary_entries (sync_status)
WHERE deleted_at IS NULL;

CREATE INDEX IF NOT EXISTS idx_commentary_entries_updated_at
ON commentary_entries (updated_at);

CREATE INDEX IF NOT EXISTS idx_commentary_entry_verses_reference
ON commentary_entry_verses (book_id, chapter, verse_start, verse_end)
WHERE deleted_at IS NULL;

CREATE INDEX IF NOT EXISTS idx_commentary_tags_slug
ON commentary_tags (slug)
WHERE deleted_at IS NULL;

CREATE INDEX IF NOT EXISTS idx_commentary_entry_tags_tag
ON commentary_entry_tags (tag_id);

CREATE INDEX IF NOT EXISTS idx_commentary_sources_type
ON commentary_sources (source_type)
WHERE deleted_at IS NULL;

CREATE INDEX IF NOT EXISTS idx_commentary_entry_sources_entry
ON commentary_entry_sources (commentary_entry_id);

CREATE INDEX IF NOT EXISTS idx_commentary_revisions_entry_revision
ON commentary_revisions (commentary_entry_id, revision_number DESC)
WHERE deleted_at IS NULL;

CREATE INDEX IF NOT EXISTS idx_commentary_generation_batches_status
ON commentary_generation_batches (status, created_at)
WHERE deleted_at IS NULL;

CREATE INDEX IF NOT EXISTS idx_commentary_generation_progress_next
ON commentary_generation_progress (collection_id, current_book_id, current_chapter)
WHERE deleted_at IS NULL;
