import json
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BOOKS_JSON = os.path.join(SCRIPT_DIR, "books.json")
INPUT_DIR = os.path.join(SCRIPT_DIR, "cross_references")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "generated")

with open(BOOKS_JSON, "r", encoding="utf-8") as f:
    books = json.load(f)

# Build a mapping from title string to book_number int
title_to_number = {book["title"]: book["book_number"] for book in books}

# Build a regex that matches any quoted book title, e.g. 'Genesis' or "Genesis"
# Sorted by length descending to avoid partial matches (e.g. "Mark" inside "Remark")
sorted_titles = sorted(title_to_number.keys(), key=len, reverse=True)
pattern = re.compile(
    r"(['\"])(" + "|".join(re.escape(t) for t in sorted_titles) + r")\1"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

for filename in os.listdir(INPUT_DIR):
    if not filename.endswith(".sql"):
        continue

    input_path = os.path.join(INPUT_DIR, filename)
    output_path = os.path.join(OUTPUT_DIR, filename)

    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace 'BookTitle' / "BookTitle" with the integer book_number
    updated = pattern.sub(lambda m: str(title_to_number[m.group(2)]), content)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(updated)

    print(f"Written: {output_path}")

print("Done.")
