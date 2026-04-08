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
local_modules = [
    {
        "title": "Biblia del Siglo de Oro",
        "download_link": "https://github.com/JenuelDev/Believers-Sword/raw/main/Modules/zipped/BSO%272009.zip",
        "version_short_name_and_date": "BSO2009",
        "description": "Biblia del Siglo de Oro",
        "file_name": "Biblia del Siglo de Oro.SQLite3",
        "is_zipped": True,
        "language": "es",
        "language_full": "spanish"
    },
    {
        "title": "Bíblia Sagrada Pe. Matos Soares 1956",
        "download_link": "https://github.com/JenuelDev/Believers-Sword/raw/main/Modules/zipped/PMS%271956.zip",
        "version_short_name_and_date": "PMS1956",
        "description": "Bíblia Sagrada segundo os textos originais Pe. Matos Soares 1956",
        "file_name": "Bíblia Sagrada Pe. Matos Soares 1956.SQLite3",
        "is_zipped": True,
        "language": "pt",
        "language_full": "portuguese"
    },
    {
        "title": "Biblia del Oso 1569",
        "download_link": "https://github.com/JenuelDev/Believers-Sword/raw/main/Modules/zipped/Reina%271569.zip",
        "version_short_name_and_date": "Reina1569",
        "description": "Biblia de Casiodoro de Reina, llamada Biblia del Oso, de 1569",
        "file_name": "Biblia del Oso 1569.SQLite3",
        "is_zipped": True,
        "language": "es",
        "language_full": "spanish"
    },
    {
        "title": "Biblia del Oso 1573",
        "download_link": "https://github.com/JenuelDev/Believers-Sword/raw/main/Modules/zipped/ReinaValera%271573.zip",
        "version_short_name_and_date": "BDO1573",
        "description": "Biblia del Oso 1573",
        "file_name": "Biblia del Oso 1573.SQLite3",
        "is_zipped": True,
        "language": "es",
        "language_full": "spanish"
    }
]

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

results.extend(local_modules)

# Write to JSON
with open("GenerateMyBibleModules/MyBible.module.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

    # Write to JSON
with open("FrontEndApp/src/assets/json/MyBible.module.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

print(f"✅ Saved {len(results)} items to MyBible.module.json")
