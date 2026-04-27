# eBible.org Module Generator

Scripts for scraping [ebible.org](https://ebible.org/) Bible translations and generating module files for Believers Sword.

## Scripts

| Script | Purpose |
|---|---|
| `generate-json-module.py` | Scrapes the eBible.org listing, collects metadata, and generates `eBible.module.json` |
| `generate.py` | Downloads a single translation and converts it to a `.SQLite3` module file |

## Setup

```bash
pip install -r requirements.txt
```

Requires Python 3.10+.

## generate-json-module.py

Scrapes https://ebible.org/find.php for all available Bible translations, visits each details page to collect metadata and the VPL download link, and outputs a JSON module list used by the app's download UI.

Only full Bibles are included — New Testament-only and Old Testament-only translations are skipped.

### Output

By default, outputs to `FrontEndApp/src/assets/json/eBible.module.json`.

### Basic usage

```bash
# Run full scrape — merges results into existing JSON file
python generate-json-module.py

# Output to a custom file
python generate-json-module.py -o output.json
```

### Merging behavior (default)

By default the script **merges** into the existing output file:

- If a module with the same `module_id` already exists, its fields are **updated** with the new data.
- If a module is new, it is **appended** to the list.
- Existing modules not found in the current scrape are left untouched.

This means you can run the script incrementally (e.g. with `--limit`) and build up the JSON over multiple runs.

### Reset mode

```bash
# Overwrite the file completely, starting fresh
python generate-json-module.py --reset
```

### Testing with a subset

```bash
# Scrape only 5 random translations (useful for checking output)
python generate-json-module.py --random --limit 5

# Scrape the first 10 translations (in page order)
python generate-json-module.py --limit 10
```

### Adjusting request delay

```bash
# Be extra polite — 2 seconds between requests
python generate-json-module.py --delay 2.0
```

### All arguments

| Argument | Default | Description |
|---|---|---|
| `-o`, `--output` | `FrontEndApp/src/assets/json/eBible.module.json` | Output JSON file path |
| `--delay` | `1.0` | Seconds between requests to avoid hammering the server |
| `--limit` | None | Only process N translations |
| `--random` | off | Shuffle entries before applying `--limit` |
| `--reset` | off | Overwrite output file instead of merging |

### Output format

Each entry in the JSON array:

```json
{
    "title": "English Standard Version",
    "download_link": "https://ebible.org/Scriptures/eng-ESV_vpl.zip",
    "file_name": "ebible-engESV.SQLite3",
    "is_zipped": true,
    "license": "public_domain",
    "language": "eng",
    "language_full": "english",
    "module_type": "ebible",
    "module_id": "engESV",
    "description": "",
    "copyright": "Copyright 2001 Crossway Bibles",
    "version_short_name_and_date": "ESV2001",
    "year": 2001
}
```

## generate.py

Downloads a single eBible.org translation by its details page URL and converts the VPL SQL dump into a MyBible-format `.SQLite3` file.

### Usage

```bash
# Convert a specific translation
python generate.py https://ebible.org/find/details.php?id=tglulb

# Custom output name
python generate.py https://ebible.org/find/details.php?id=tglulb -o tagalog-ulb
```

Output is saved to `./Generated/`.
