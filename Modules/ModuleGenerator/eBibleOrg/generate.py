"""
eBible.org Bible Module Generator

Downloads a Bible translation from eBible.org, extracts the VPL SQL dump,
and converts it into a MyBible-format SQLite3 file for Believers Sword.

Usage:
    python generate.py <url>
    python generate.py https://ebible.org/find/details.php?id=tglulb

The generated .SQLite3 file will be placed in ./Generated/
"""

import sys
import re
import io
import sqlite3
import zipfile
import argparse
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

SCRIPT_DIR = Path(__file__).resolve().parent
GENERATED_DIR = SCRIPT_DIR / "Generated"

# ---------------------------------------------------------------------------
# MyBible 10-increment book number mapping (same as Electron/IpcMainEvents/importing)
# ---------------------------------------------------------------------------
EBIBLE_BOOK_MAP: dict[str, int] = {
    # Old Testament
    "GEN": 10, "EXO": 20, "LEV": 30, "NUM": 40, "DEU": 50,
    "JOS": 60, "JDG": 70, "RUT": 80,
    "1SA": 90, "2SA": 100, "1KI": 110, "2KI": 120,
    "1CH": 130, "2CH": 140, "EZR": 150, "NEH": 160,
    # Deuterocanonical
    "TOB": 170, "JDT": 180,
    "EST": 190,
    "JOB": 220, "PSA": 230, "PRO": 240, "ECC": 250, "SNG": 260,
    "WIS": 270, "SIR": 280,
    "ISA": 290, "JER": 300, "LAM": 310,
    "BAR": 320,
    "EZK": 330, "DAN": 340,
    "HOS": 350, "JOL": 360, "AMO": 370, "OBA": 380, "JON": 390,
    "MIC": 400, "NAM": 410, "HAB": 420, "ZEP": 430, "HAG": 440, "ZEC": 450, "MAL": 460,
    "1MA": 462, "2MA": 464,
    # New Testament
    "MAT": 470, "MRK": 480, "LUK": 490, "JHN": 500, "ACT": 510,
    "ROM": 520, "1CO": 530, "2CO": 540, "GAL": 550, "EPH": 560,
    "PHP": 570, "COL": 580, "1TH": 590, "2TH": 600,
    "1TI": 610, "2TI": 620, "TIT": 630, "PHM": 640, "HEB": 650,
    "JAS": 660, "1PE": 670, "2PE": 680,
    "1JN": 690, "2JN": 700, "3JN": 710, "JUD": 720, "REV": 730,
}

BOOK_LONG_NAMES: dict[int, str] = {
    10: "Genesis", 20: "Exodus", 30: "Leviticus", 40: "Numbers", 50: "Deuteronomy",
    60: "Joshua", 70: "Judges", 80: "Ruth",
    90: "1 Samuel", 100: "2 Samuel", 110: "1 Kings", 120: "2 Kings",
    130: "1 Chronicles", 140: "2 Chronicles", 150: "Ezra", 160: "Nehemiah",
    170: "Tobit", 180: "Judith",
    190: "Esther",
    220: "Job", 230: "Psalms", 240: "Proverbs", 250: "Ecclesiastes", 260: "Song of Solomon",
    270: "Wisdom", 280: "Sirach",
    290: "Isaiah", 300: "Jeremiah", 310: "Lamentations",
    320: "Baruch",
    330: "Ezekiel", 340: "Daniel",
    350: "Hosea", 360: "Joel", 370: "Amos", 380: "Obadiah", 390: "Jonah",
    400: "Micah", 410: "Nahum", 420: "Habakkuk", 430: "Zephaniah", 440: "Haggai", 450: "Zechariah", 460: "Malachi",
    462: "1 Maccabees", 464: "2 Maccabees",
    470: "Matthew", 480: "Mark", 490: "Luke", 500: "John", 510: "Acts",
    520: "Romans", 530: "1 Corinthians", 540: "2 Corinthians", 550: "Galatians", 560: "Ephesians",
    570: "Philippians", 580: "Colossians", 590: "1 Thessalonians", 600: "2 Thessalonians",
    610: "1 Timothy", 620: "2 Timothy", 630: "Titus", 640: "Philemon", 650: "Hebrews",
    660: "James", 670: "1 Peter", 680: "2 Peter",
    690: "1 John", 700: "2 John", 710: "3 John", 720: "Jude", 730: "Revelation",
}

INSERT_PATTERN = re.compile(
    r'INSERT INTO \S+ VALUES \("([^"]+)","([^"]+)","([A-Z0-9]+)","(\d+)","(\d+)","(\d+)","(.*)"\s*\);'
)


@dataclass
class ModuleMetadata:
    """Metadata scraped from the eBible.org details page."""
    module_id: str = ""
    language: str = ""          # ISO 639-3 code (e.g. "tgl")
    language_name: str = ""     # Full name (e.g. "Tagalog")
    title: str = ""             # Native-language title
    description: str = ""       # English title or fallback to native title
    copyright: str = ""
    download_url: str = ""


def extract_module_id(url: str) -> str:
    """Extract the module ID from an eBible.org details URL."""
    match = re.search(r'[?&]id=([^&#]+)', url)
    if match:
        return match.group(1)
    raise ValueError(f"Could not extract module ID from URL: {url}")


def _find_td_after_label(soup: BeautifulSoup, label: str) -> str | None:
    """Find a <td> containing the label text and return the next <td>'s text."""
    td = soup.find("td", string=re.compile(re.escape(label), re.IGNORECASE))
    if not td:
        return None
    next_td = td.find_next_sibling("td")
    return next_td.get_text(strip=True) if next_td else None


def scrape_details_page(url: str) -> tuple[BeautifulSoup, ModuleMetadata]:
    """Scrape the eBible.org details page for metadata and the VPL download link."""
    print(f"Fetching details page: {url}")
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    meta = ModuleMetadata()

    # Module ID from URL
    meta.module_id = extract_module_id(url)

    # Title from <h1>
    h1 = soup.find("h1")
    if h1:
        meta.title = h1.get_text(strip=True)

    # Description from <h2> (English title) or fallback to <h1>
    h2 = soup.find("h2")
    if h2:
        meta.description = h2.get_text(strip=True)
    else:
        meta.description = meta.title

    # Language — page uses: <td>Language: <a>[tgl]</a></td><td>Tagalog</td>
    # soup.find('td', string=...) won't match because the td has child elements,
    # so we iterate all tds and check get_text()
    for td in soup.find_all("td"):
        td_text = td.get_text(strip=True)
        if td_text.startswith("Language"):
            # Extract [xxx] code from this td
            code_match = re.search(r"\[(\w{2,3})\]", td_text)
            if code_match:
                meta.language = code_match.group(1)
            # Language name is in the next sibling td
            next_td = td.find_next_sibling("td")
            if next_td:
                meta.language_name = next_td.get_text(strip=True)
            break

    # Copyright — extract from the about.htm content embedded in the page
    # The pattern is: "copyright © YYYY <holder>" ending before "Language:" or newline
    body_text = soup.get_text(separator="\n")
    copyright_match = re.search(
        r"((?:[Cc]opyright|©)\s*©?\s*\d{4}\s+[^\n]+?)(?=\s*Language:|\s*Translation|\s*Contributor|\n|$)",
        body_text,
    )
    if copyright_match:
        meta.copyright = copyright_match.group(1).strip()

    # VPL download link
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if "_vpl.zip" in href:
            meta.download_url = urljoin(url, href)
            break

    if not meta.download_url:
        raise RuntimeError(
            "Could not find a _vpl.zip download link on the page. "
            "The page structure may have changed, or this translation may not have a VPL export."
        )

    print(f"  Title:       {meta.title}")
    print(f"  Description: {meta.description}")
    print(f"  Language:    [{meta.language}] {meta.language_name}")
    print(f"  Copyright:   {meta.copyright}")
    print(f"  Download:    {meta.download_url}")

    return soup, meta


def download_zip(download_url: str) -> bytes:
    """Download the zip file and return its content as bytes."""
    print(f"Downloading: {download_url}")
    resp = requests.get(download_url, timeout=120)
    resp.raise_for_status()
    size_mb = len(resp.content) / (1024 * 1024)
    print(f"Downloaded {size_mb:.1f} MB")
    return resp.content


def extract_from_zip(zip_bytes: bytes, module_id: str) -> tuple[str, str | None]:
    """
    Extract the SQL content and the about.htm content from the zip.
    Returns (sql_content, about_html_or_None).
    """
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        names = zf.namelist()
        print(f"Zip contains {len(names)} file(s): {names}")

        # Find the SQL file
        sql_file = None
        for name in names:
            if name.endswith(".sql"):
                sql_file = name
                break

        if not sql_file:
            raise RuntimeError(f"No .sql file found in the zip. Files: {names}")

        print(f"Extracting SQL: {sql_file}")
        sql_content = zf.read(sql_file).decode("utf-8")

        # Find the about.htm file
        about_html = None
        for name in names:
            if name.endswith("_about.htm") or name.endswith("_about.html"):
                print(f"Extracting about file: {name}")
                about_html = zf.read(name).decode("utf-8")
                break

        return sql_content, about_html


def parse_sql(sql_content: str) -> list[tuple[int, int, int, str]]:
    """
    Parse eBible.org VPL SQL INSERT statements into verse tuples.
    Returns list of (book_number, chapter, verse, text).
    """
    verses = []
    for line in sql_content.splitlines():
        line = line.strip()
        if not line.startswith("INSERT INTO"):
            continue

        match = INSERT_PATTERN.match(line)
        if not match:
            continue

        book_code = match.group(3)
        chapter = int(match.group(4))
        verse = int(match.group(5))
        text = match.group(7)

        book_number = EBIBLE_BOOK_MAP.get(book_code)
        if book_number is None:
            continue

        # Clean up pilcrow paragraph markers
        text = re.sub(r"¶\s*", "", text).strip()
        verses.append((book_number, chapter, verse, text))

    return verses


def _detect_contains_accents(verses: list[tuple[int, int, int, str]]) -> bool:
    """Check if the verse text contains accented/non-ASCII characters."""
    sample = verses[:500]
    for _, _, _, text in sample:
        for ch in text:
            if ord(ch) > 127 and ch not in "''""—–…¶":
                return True
    return False


def create_sqlite_module(
    output_path: Path,
    verses: list[tuple[int, int, int, str]],
    about_html: str | None,
    meta: ModuleMetadata,
) -> None:
    """Create the MyBible-format SQLite3 database file."""
    if output_path.exists():
        output_path.unlink()

    conn = sqlite3.connect(str(output_path))
    cur = conn.cursor()

    # -- verses table --
    cur.execute("""
        CREATE TABLE verses (
            book_number INTEGER,
            chapter     INTEGER,
            verse       INTEGER,
            text        TEXT
        )
    """)

    cur.executemany(
        "INSERT INTO verses (book_number, chapter, verse, text) VALUES (?, ?, ?, ?)",
        verses,
    )

    cur.execute(
        "CREATE INDEX idx_verses_book_chapter ON verses (book_number, chapter)"
    )

    # -- books table --
    book_numbers = sorted({v[0] for v in verses})
    cur.execute("""
        CREATE TABLE books (
            book_number INTEGER PRIMARY KEY,
            long_name   TEXT
        )
    """)
    cur.executemany(
        "INSERT INTO books (book_number, long_name) VALUES (?, ?)",
        [(bn, BOOK_LONG_NAMES.get(bn, f"Book {bn}")) for bn in book_numbers],
    )

    # -- info table (MyBible standard rows) --
    cur.execute("""
        CREATE TABLE info (
            name  TEXT,
            value TEXT
        )
    """)

    info_rows = [
        ("language", meta.language),
        ("description", meta.description),
        ("detailed_info", about_html or f"{meta.title} — {meta.copyright}"),
        ("chapter_string", "Chapter"),
        ("contains_accents", str(_detect_contains_accents(verses)).lower()),
        ("add_space_before_footnote_marker", "true"),
    ]

    cur.executemany(
        "INSERT INTO info (name, value) VALUES (?, ?)",
        info_rows,
    )

    conn.commit()
    conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="Download an eBible.org translation and convert it to a MyBible SQLite3 module."
    )
    parser.add_argument(
        "url",
        help="eBible.org details page URL, e.g. https://ebible.org/find/details.php?id=tglulb",
    )
    parser.add_argument(
        "-o", "--output",
        help="Custom output filename (without extension). Defaults to the module ID.",
    )
    args = parser.parse_args()

    # 1. Scrape the details page for metadata and download link
    soup, meta = scrape_details_page(args.url)

    # 2. Download the zip
    zip_bytes = download_zip(meta.download_url)

    # 3. Extract SQL and about.htm from the zip
    sql_content, about_html = extract_from_zip(zip_bytes, meta.module_id)

    # 4. Parse the SQL into verses
    verses = parse_sql(sql_content)
    if not verses:
        print("ERROR: No valid verses could be parsed from the SQL file.")
        sys.exit(1)

    book_numbers = sorted({v[0] for v in verses})
    book_names = [BOOK_LONG_NAMES.get(bn, f"Book {bn}") for bn in book_numbers]
    print(f"Parsed {len(verses)} verses across {len(book_numbers)} books")
    print(f"Books: {', '.join(book_names)}")

    # 5. Create the SQLite3 module
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    output_name = args.output or meta.module_id
    output_path = GENERATED_DIR / f"{output_name}.SQLite3"

    create_sqlite_module(output_path, verses, about_html, meta)

    print(f"\nDone! Module saved to: {output_path}")
    print(f"  Verses: {len(verses)}")
    print(f"  Books:  {len(book_numbers)}")
    print(f"  Info:   language={meta.language}, description={meta.description}")


if __name__ == "__main__":
    main()
