"""
eBible.org JSON Module Generator

Scrapes https://ebible.org/find.php for all available Bible translations,
visits each details page to collect metadata and the VPL download link,
and generates a JSON module list compatible with believers-sword.module.json.

Usage:
    python generate-json-module.py
    python generate-json-module.py -o output.json
    python generate-json-module.py --delay 2.0
    python generate-json-module.py --random --limit 5
    python generate-json-module.py --reset
"""

from __future__ import annotations

import json
import random
import re
import sys
import time
import argparse
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

FIND_URL = "https://ebible.org/find.php"
DETAILS_BASE = "https://ebible.org/find/"
SCRIPT_DIR = Path(__file__).resolve().parent

# Default output path — same directory as believers-sword.module.json
DEFAULT_OUTPUT = (
    SCRIPT_DIR.parent.parent.parent
    / "FrontEndApp"
    / "src"
    / "assets"
    / "json"
    / "eBible.module.json"
)


def scrape_find_page() -> list[dict]:
    """
    Scrape https://ebible.org/find.php and return a list of translation entries.
    Each entry has: details_url, vernacular_title, english_title, language_local, language_english.
    """
    print(f"Fetching listing page: {FIND_URL}")
    resp = requests.get(FIND_URL, timeout=60)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    entries = []
    seen_ids = set()

    # Find all details links — each translation has one or more links to details.php?id=xxx
    for a_tag in soup.find_all("a", href=re.compile(r"details\.php\?id=")):
        href = a_tag["href"]
        match = re.search(r"id=([^&#]+)", href)
        if not match:
            continue

        module_id = match.group(1)
        if module_id in seen_ids:
            continue
        seen_ids.add(module_id)

        details_url = urljoin(DETAILS_BASE, href)
        title = a_tag.get_text(strip=True)

        entries.append({
            "module_id": module_id,
            "details_url": details_url,
            "title_from_list": title,
        })

    print(f"Found {len(entries)} unique translations on listing page")
    return entries


def scrape_details_page(url: str, module_id: str) -> dict | None:
    """
    Scrape a single eBible.org details page and return module metadata.
    Returns None if the page is restricted, not found, or has no VPL download.
    """
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    page_text = soup.get_text(separator="\n")

    # Check for "not found" error pages
    if "not found" in page_text.lower() and soup.find("h1") is None:
        return None

    # Check for restricted access indicators
    restricted_patterns = [
        r"restricted",
        r"not available for download",
        r"permission.+required",
        r"no.+download.+available",
    ]
    for pattern in restricted_patterns:
        if re.search(pattern, page_text, re.IGNORECASE):
            print(f"    SKIPPED (restricted)")
            return None

    # Title from <h1>
    title = ""
    h1 = soup.find("h1")
    if h1:
        title = h1.get_text(strip=True)

    # Description from <h2> (English title) or fallback to <h1>
    description = ""
    h2 = soup.find("h2")
    if h2:
        description = h2.get_text(strip=True)
    else:
        description = title

    # Language code and name
    language_code = ""
    language_name = ""
    for td in soup.find_all("td"):
        td_text = td.get_text(strip=True)
        if td_text.startswith("Language"):
            code_match = re.search(r"\[(\w{2,3})\]", td_text)
            if code_match:
                language_code = code_match.group(1)
            next_td = td.find_next_sibling("td")
            if next_td:
                language_name = next_td.get_text(strip=True)
            break

    # Abbreviation
    abbreviation = ""
    for td in soup.find_all("td"):
        td_text = td.get_text(strip=True)
        if td_text.startswith("Abbreviation"):
            next_td = td.find_next_sibling("td")
            if next_td:
                abbreviation = next_td.get_text(strip=True)
            break

    # Copyright
    copyright_text = ""
    copyright_match = re.search(
        r"((?:[Cc]opyright|©)\s*©?\s*\d{4}\s+[^\n]+?)(?=\s*Language:|\s*Translation|\s*Contributor|\n|$)",
        page_text,
    )
    if copyright_match:
        copyright_text = copyright_match.group(1).strip()

    # Determine license from page text
    license_type = "unknown"
    lower_text = page_text.lower()
    if "public domain" in lower_text or "not copyrighted" in lower_text:
        license_type = "public_domain"
    elif "creative commons" in lower_text:
        if "share-alike" in lower_text or "sa" in lower_text:
            license_type = "cc_by_sa"
        elif "attribution" in lower_text:
            license_type = "cc_by"
        else:
            license_type = "creative_commons"
    elif "open" in lower_text and "license" in lower_text:
        license_type = "open_attribution_required"

    # Year — try to extract from copyright or page text
    year = None
    year_match = re.search(r"(?:copyright|©)\s*©?\s*(\d{4})", page_text, re.IGNORECASE)
    if year_match:
        year = int(year_match.group(1))

    # Last updated date
    update_match = re.search(r"Last updated\s*(\d{4}-\d{2}-\d{2})", page_text)
    update_date = update_match.group(1) if update_match else ""

    # VPL download link
    vpl_url = ""
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if "_vpl.zip" in href:
            vpl_url = urljoin(url, href)
            break

    if not vpl_url:
        print(f"    SKIPPED (no VPL download)")
        return None

    # Determine testament coverage from the "Contents" table row and title/description
    contents_text = ""
    for td in soup.find_all("td"):
        td_text = td.get_text(strip=True)
        if td_text.startswith("Contents"):
            next_td = td.find_next_sibling("td")
            if next_td:
                contents_text = next_td.get_text(strip=True).lower()
            break

    combined_text = f"{title} {description} {contents_text}".lower()

    # Match full phrases and common abbreviations (word-boundary check for NT/OT)
    has_nt = "new testament" in combined_text or bool(re.search(r'\bnt\b', combined_text))
    has_ot = "old testament" in combined_text or bool(re.search(r'\bot\b', combined_text))
    has_bible = "bible" in combined_text

    # Skip portions, gospels-only, psalms-only, selections — these are too partial
    partial_patterns = [r"\bportions?\b", r"\bgospels?\b", r"\bpsalms?\s+only\b", r"\bselections?\b"]
    for pat in partial_patterns:
        if re.search(pat, contents_text):
            print(f"    SKIPPED (partial: {contents_text})")
            return None

    # Determine testament field
    if has_nt and not has_ot and not has_bible:
        testament = "nt"
    elif has_ot and not has_nt and not has_bible:
        testament = "ot"
    else:
        testament = "full"

    # Build file_name from module_id
    file_name = f"ebible-{module_id}.SQLite3"

    module = {
        "title": description if description else title,
        "download_link": vpl_url,
        "file_name": file_name,
        "is_zipped": True,
        "license": license_type,
        "language": language_code,
        "language_full": language_name.lower(),
        "module_type": "ebible",
        "module_id": module_id,
        "description": title if description and title != description else "",
        "copyright": copyright_text,
        "testament": testament,
    }

    short_name = abbreviation if abbreviation else module_id
    if year:
        module["version_short_name_and_date"] = f"{short_name}{year}"
    else:
        module["version_short_name_and_date"] = short_name

    if year:
        module["year"] = year

    return module


def main():
    parser = argparse.ArgumentParser(
        description="Scrape eBible.org and generate a JSON module list for Believers Sword."
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output JSON file path (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay in seconds between requests to be polite to the server (default: 1.0)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Stop after collecting N valid modules (useful for testing)",
    )
    parser.add_argument(
        "--random",
        action="store_true",
        help="Randomly shuffle entries before applying --limit",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Overwrite the output file instead of merging into existing data",
    )
    args = parser.parse_args()

    # 1. Scrape the listing page
    entries = scrape_find_page()
    if not entries:
        print("ERROR: No translations found on the listing page.")
        sys.exit(1)

    # 1b. Optionally shuffle
    if args.random:
        random.shuffle(entries)

    if args.limit:
        print(f"Will collect up to {args.limit} valid modules{' (randomized)' if args.random else ''}")

    # 2. Visit each details page and collect metadata
    modules = []
    skipped = 0
    errors = 0

    for i, entry in enumerate(entries, 1):
        # Stop once we have enough valid modules
        if args.limit and len(modules) >= args.limit:
            break

        module_id = entry["module_id"]
        url = entry["details_url"]
        print(f"[{i}/{len(entries)}] {module_id} — {entry['title_from_list']}")

        try:
            module = scrape_details_page(url, module_id)
            if module:
                modules.append(module)
                print(f"    OK: {module['title']} [{module['language']}]")
            else:
                skipped += 1
        except requests.RequestException as e:
            print(f"    ERROR: {e}")
            errors += 1
        except Exception as e:
            print(f"    ERROR (unexpected): {e}")
            errors += 1

        # Be polite — don't hammer the server
        if i < len(entries):
            time.sleep(args.delay)

    # 3. Merge with existing JSON or reset
    args.output.parent.mkdir(parents=True, exist_ok=True)

    if args.reset or not args.output.exists():
        final_modules = modules
        added = len(modules)
        updated = 0
    else:
        # Load existing data and merge
        with open(args.output, "r", encoding="utf-8") as f:
            existing = json.load(f)

        # Index existing modules by module_id (or file_name as fallback)
        existing_by_id = {}
        for mod in existing:
            key = mod.get("module_id") or mod.get("file_name")
            if key:
                existing_by_id[key] = mod

        added = 0
        updated = 0
        for mod in modules:
            key = mod.get("module_id") or mod.get("file_name")
            if key in existing_by_id:
                existing_by_id[key].update(mod)
                updated += 1
            else:
                existing.append(mod)
                existing_by_id[key] = mod
                added += 1

        final_modules = existing

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(final_modules, f, indent=4, ensure_ascii=False)

    print(f"\nDone!")
    print(f"  Total found:   {len(entries)}")
    print(f"  Scraped:       {len(modules)}")
    print(f"  Added (new):   {added}")
    print(f"  Updated:       {updated}")
    print(f"  Skipped:       {skipped}")
    print(f"  Errors:        {errors}")
    print(f"  Output:        {args.output}")


if __name__ == "__main__":
    main()
