"""
Scraper for ph4.org MyBible module index.
Extracts only complete Bible entries (bgcolor="#ffffff" + <b>BIBLE</b> label)
and outputs ph4_mybible.module.json to FrontEndApp/src/assets/json/.

Usage:
    .venv/Scripts/python generate.py
"""

import json
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

INDEX_URL = "https://www.ph4.org/b4_index.php?hd=b"
OUTPUT_PATH = (
    Path(__file__).resolve().parents[3]
    / "FrontEndApp"
    / "src"
    / "assets"
    / "json"
    / "ph4_mybible.module.json"
)


def fetch_html(url):
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    resp.raise_for_status()
    return resp.text


def strip_tags(element):
    """Return plain text from a BS4 element."""
    return element.get_text(separator=" ", strip=True)


def parse_language_header(row):
    """
    Extract (language_code, language_full) from a bgcolor="#272727" header row.
    Example href: b4_1.php?l=es&q=mybible  →  language_code = "es"
    Example text: <b>español</b> - Spanish  →  language_full = "spanish"
    """
    a_tag = row.find("a", href=re.compile(r"[?&]l="))
    if not a_tag:
        return "", ""

    # language code from ?l=xx
    code_m = re.search(r"[?&]l=([^&]+)", a_tag["href"])
    language_code = code_m.group(1).lower() if code_m else ""

    # native name from <b>...</b>, English name after " - "
    full_text = strip_tags(a_tag)   # e.g. "español - Spanish" (img stripped)
    # strip leading number from <sub> if it bled in
    full_text = re.sub(r"^\d+\s*", "", full_text).strip()

    # Take the part after " - " as the English name, lower-cased
    if " - " in full_text:
        language_full = full_text.split(" - ", 1)[1].strip().lower()
    else:
        # fallback: use the bold native name
        bold = a_tag.find("b")
        language_full = bold.get_text(strip=True).lower() if bold else full_text.lower()

    return language_code, language_full


def extract_modules(html):
    soup = BeautifulSoup(html, "html.parser")
    modules = []

    # Collect all <tr> rows that share the same top-level table
    all_rows = soup.find_all("tr", bgcolor=True)

    current_language = ""
    current_language_full = ""

    for row in all_rows:
        bg = row.get("bgcolor", "").upper()

        # Language header row — update current language context
        if bg == "#272727":
            current_language, current_language_full = parse_language_header(row)
            continue

        # Only process complete-Bible rows
        if bg != "#FFFFFF":
            continue

        # Must have <b>BIBLE</b>
        if not row.find("b", string=re.compile(r"^BIBLE$")):
            continue

        # --- download link & module_id ---
        dl_tag = row.find("a", href=re.compile(r"_dl\.php.*b=mybible"))
        if not dl_tag:
            continue

        href = dl_tag["href"]
        m = re.search(r"back=([^&]+)&(?:amp;)?a=([^&]+)&(?:amp;)?b=mybible", href)
        if not m:
            continue

        back = m.group(1)
        module_id = m.group(2)
        download_link = (
            f"https://www.ph4.org/_dl.php?back={back}&a={module_id}&b=mybible&c"
        )

        # --- short name + year ---
        first_td = row.find("td", align="right")
        short_name = module_id
        year = None
        if first_td:
            td_text = strip_tags(first_td)
            year_m = re.search(r"\b(\d{4})\b", td_text)
            if year_m:
                year = int(year_m.group(1))
            bold = first_td.find("b")
            if bold:
                short_name = bold.get_text(strip=True)

        # --- title (div.btl, strip leading star) ---
        btl = row.find("div", class_="btl")
        title = strip_tags(btl).lstrip("★").strip() if btl else short_name

        # --- description: first non-empty .gray div ---
        description = ""
        for gray in row.find_all("div", class_="gray"):
            text = strip_tags(gray)
            if text:
                description = text
                break

        version_short_name_and_date = f"{short_name}{year}" if year else short_name

        modules.append(
            {
                "title": title,
                "download_link": download_link,
                "file_name": f"ph4_mybible_{module_id}_{year}.SQLite3" if year else f"ph4_mybible_{module_id}.SQLite3",
                "is_zipped": True,
                "language": current_language,
                "language_full": current_language_full,
                "module_type": "ph4_mybible",
                "module_id": module_id,
                "description": description,
                "copyright": "",
                "testament": "full",
                "version_short_name_and_date": version_short_name_and_date,
                "year": year,
            }
        )

    return modules


def main():
    print(f"Fetching {INDEX_URL} ...")
    html = fetch_html(INDEX_URL)
    print(f"Downloaded {len(html):,} bytes")

    modules = extract_modules(html)
    print(f"Found {len(modules)} complete-Bible modules")

    if not modules:
        print("ERROR: no modules extracted — check the page structure.", file=sys.stderr)
        sys.exit(1)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(modules, f, ensure_ascii=False, indent=4)

    print(f"Written -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
