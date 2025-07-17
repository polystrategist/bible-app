import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

url = "https://www.ph4.org/b4_1.php?l=en"
base_url = "https://www.ph4.org/"
headers = {'User-Agent': 'Mozilla/5.0'}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

results = []

for tr in soup.find_all("tr"):
    tds = tr.find_all("td", recursive=False)

    if len(tds) == 1:
        text = tds[0].get_text(strip=True)
        if text == "SUBHEADINGS":
            break  # Stop when reaching the 'SUBHEADINGS' section

    if len(tds) == 3:
        # Get <a> inside the first td and extract the href
        link_tag = tds[0].find("a", href=True, attrs={"class": "circle_dl"})
        href = urljoin(base_url, link_tag["href"]) if link_tag else None

        # Get text from second td
        second_td_text = tds[1].get_text(strip=True)

        # Get the title from third td
        title = tds[2].find("div", class_="btl")
        title_text = title.get_text(strip=True) if title else None

        if title_text:
            results.append({
                "title": title_text,
                "download_link": href,
                "version_short_name_and_date": second_td_text,
                "description": title_text,
                "file_name": f"{title_text}.SQLite3",
                "is_zipped": True
            })

# Write to JSON
with open("GenerateMyBibleModules/MyBible.module.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

    # Write to JSON
with open("FrontEndApp/src/assets/json/MyBible.module.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

print(f"✅ Saved {len(results)} items to MyBible.module.json")
