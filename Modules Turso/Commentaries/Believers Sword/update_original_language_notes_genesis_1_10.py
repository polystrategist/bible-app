import json
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

BASE = Path('/mnt/d/Projects/Personal/Believers-Sword/Modules Turso/Commentaries/Believers Sword')
GEN_DIR = BASE / 'generated' / '01-genesis'
DB = BASE / 'believers_sword_commentaries.db'

def now():
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

notes = {
  1: [
    {'term':'bārāʾ','language':'Hebrew','verse':'Genesis 1:1','words_used':'בָּרָא (bārāʾ) — “created”','meaning':'to create; used with God as the subject, emphasizing divine creative action that depends on no rival power.'},
    {'term':'tōhû wābōhû','language':'Hebrew phrase','verse':'Genesis 1:2','words_used':'תֹהוּ וָבֹהוּ (tōhû wābōhû) — “formless and empty”','meaning':'formless and empty; the unshaped condition that God orders by His word.'},
    {'term':'ṣelem','language':'Hebrew','verse':'Genesis 1:26-27','words_used':'צֶלֶם (ṣelem) — “image”','meaning':'image; humanity is made to represent God’s rule and character within creation.'},
  ],
  2: [
    {'term':'yāṣar','language':'Hebrew','verse':'Genesis 2:7','words_used':'וַיִּיצֶר (wayyîṣer) from יָצַר (yāṣar) — “formed”','meaning':'to form or fashion, like a potter shaping clay; it portrays God’s personal care in making man.'},
    {'term':'ʿēzer kĕnegdô','language':'Hebrew phrase','verse':'Genesis 2:18','words_used':'עֵזֶר כְּנֶגְדּוֹ (ʿēzer kĕnegdô) — “helper corresponding to him”','meaning':'a helper corresponding to him; not inferiority, but a strong companion suited to him.'},
    {'term':'šāmar','language':'Hebrew','verse':'Genesis 2:15','words_used':'לְשָׁמְרָהּ (ləšāmrāh) from שָׁמַר (šāmar) — “to keep/guard it”','meaning':'to keep, guard, or watch; humanity is called to protect and steward what God entrusts.'},
  ],
  3: [
    {'term':'nāḥāš','language':'Hebrew','verse':'Genesis 3:1','words_used':'הַנָּחָשׁ (hannāḥāš) — “the serpent”','meaning':'serpent; the deceiver who twists God’s word and invites suspicion against God.'},
    {'term':'ʿārûm / ʿărummîm','language':'Hebrew wordplay','verse':'Genesis 2:25; 3:1','words_used':'עֲרוּמִּים (ʿărummîm) — “naked”; עָרוּם (ʿārûm) — “crafty”','meaning':'crafty / naked; the chapter contrasts the serpent’s craftiness with humanity’s exposed shame.'},
    {'term':'zéraʿ','language':'Hebrew','verse':'Genesis 3:15','words_used':'זֶרַע (zéraʿ) — “seed/offspring”','meaning':'seed or offspring; in Genesis 3:15 it becomes a promise of conflict and final victory.'},
  ],
  4: [
    {'term':'ḥaṭṭāʾt','language':'Hebrew','verse':'Genesis 4:7','words_used':'חַטָּאת (ḥaṭṭāʾt) — “sin”','meaning':'sin; pictured as crouching at the door, ready to dominate if not resisted.'},
    {'term':'minḥâ','language':'Hebrew','verse':'Genesis 4:3-5','words_used':'מִנְחָה (minḥâ) — “offering/tribute”','meaning':'offering or tribute; worship is not merely the object offered but the heart before God.'},
    {'term':'qārāʾ bĕšēm YHWH','language':'Hebrew phrase','verse':'Genesis 4:26','words_used':'לִקְרֹא בְּשֵׁם יְהוָה (liqroʾ bĕšēm YHWH) — “to call on the name of the LORD”','meaning':'to call on the name of the LORD; public dependence and worship.'},
  ],
  5: [
    {'term':'tôlĕdōt','language':'Hebrew','verse':'Genesis 5:1','words_used':'תּוֹלְדֹת (tôlĕdōt) — “generations/account”','meaning':'generations or account; a structuring word in Genesis that traces God’s purposes through family lines.'},
    {'term':'hālak','language':'Hebrew','verse':'Genesis 5:22, 24','words_used':'וַיִּתְהַלֵּךְ (wayyithallēḵ) from הָלַךְ (hālak) — “walked”','meaning':'to walk; Enoch’s life is described as ongoing fellowship with God.'},
    {'term':'nāḥam','language':'Hebrew','verse':'Genesis 5:29','words_used':'יְנַחֲמֵנוּ (yənaḥămēnû) from נָחַם (nāḥam) — “comfort/relief”','meaning':'to comfort or give relief; connected to Noah’s name and the longing for rest from curse.'},
  ],
  6: [
    {'term':'ḥāmās','language':'Hebrew','verse':'Genesis 6:11, 13','words_used':'חָמָס (ḥāmās) — “violence”','meaning':'violence; the earth is filled with destructive injustice.'},
    {'term':'ḥēn','language':'Hebrew','verse':'Genesis 6:8','words_used':'חֵן (ḥēn) — “favor/grace”','meaning':'grace or favor; Noah finds grace before the LORD, not because the world is safe but because God is merciful.'},
    {'term':'tāmîm','language':'Hebrew','verse':'Genesis 6:9','words_used':'תָּמִים (tāmîm) — “blameless/whole”','meaning':'blameless or whole; Noah’s integrity contrasts with the corruption around him.'},
  ],
  7: [
    {'term':'mabbûl','language':'Hebrew','verse':'Genesis 7:6-7, 10, 17','words_used':'מַבּוּל (mabbûl) — “flood/deluge”','meaning':'flood or deluge; used for the catastrophic judgment in Noah’s day.'},
    {'term':'sāgar','language':'Hebrew','verse':'Genesis 7:16','words_used':'וַיִּסְגֹּר (wayyisgōr) from סָגַר (sāgar) — “shut/closed”','meaning':'to shut or close; the LORD shuts Noah in, emphasizing divine protection.'},
    {'term':'gābar','language':'Hebrew','verse':'Genesis 7:18-20, 24','words_used':'וַיִּגְבְּרוּ (wayyigbərû) from גָּבַר (gābar) — “prevailed/grew strong”','meaning':'to prevail or grow strong; the waters prevail over the old world.'},
  ],
  8: [
    {'term':'zākar','language':'Hebrew','verse':'Genesis 8:1','words_used':'וַיִּזְכֹּר (wayyizkōr) from זָכַר (zākar) — “remembered”','meaning':'to remember; not mere mental recall, but covenantal action on behalf of someone.'},
    {'term':'rûaḥ','language':'Hebrew','verse':'Genesis 8:1','words_used':'רוּחַ (rûaḥ) — “wind/spirit”','meaning':'wind or spirit; God sends a wind over the waters, echoing creation language.'},
    {'term':'nîḥōaḥ','language':'Hebrew','verse':'Genesis 8:21','words_used':'נִיחֹחַ (nîḥōaḥ) — “pleasing/soothing aroma”','meaning':'pleasing or soothing aroma; Noah’s sacrifice is received by God.'},
  ],
  9: [
    {'term':'bĕrît','language':'Hebrew','verse':'Genesis 9:9-17','words_used':'בְּרִית (bĕrît) — “covenant”','meaning':'covenant; a binding commitment initiated by God.'},
    {'term':'qešet','language':'Hebrew','verse':'Genesis 9:13-16','words_used':'קֶשֶׁת (qešet) — “bow/rainbow”','meaning':'bow; the rainbow sign, also the word for a weapon bow, suggesting judgment is restrained by divine mercy.'},
    {'term':'dām','language':'Hebrew','verse':'Genesis 9:4-6','words_used':'דָּם (dām) — “blood”','meaning':'blood; life is sacred because humans bear God’s image.'},
  ],
  10: [
    {'term':'gôyim','language':'Hebrew','verse':'Genesis 10:5, 20, 31-32','words_used':'גּוֹיִם (gôyim) — “nations/peoples”','meaning':'nations or peoples; the chapter emphasizes the spread of peoples under God’s sovereignty.'},
    {'term':'mišpāḥâ','language':'Hebrew','verse':'Genesis 10:5, 20, 31-32','words_used':'מִשְׁפָּחָה / מִשְׁפְּחֹת (mišpāḥâ / mišpəḥōt) — “family/families/clans”','meaning':'clan or family; nations are described as extended families, not faceless categories.'},
    {'term':'pārad','language':'Hebrew','verse':'Genesis 10:5, 32','words_used':'נִפְרְדוּ (nip̄rədû) from פָּרַד (pārad) — “were separated/divided”','meaning':'to separate or divide; the peoples spread according to lands, languages, families, and nations.'},
  ],
}

def notes_section(ch):
    lines = []
    for n in notes[ch]:
        lines.append(f"- {n['term']} ({n['language']}, {n['verse']}): {n['words_used']}. {n['meaning']}")
    return '\n'.join(lines)

updated_files=[]
for ch, chapter_notes in notes.items():
    p = GEN_DIR / f'{ch:02d}.json'
    data = json.loads(p.read_text(encoding='utf-8'))
    data['original_language_notes'] = chapter_notes
    data['updated_at'] = now()
    # Update content Hebrew Word Notes section if present
    content = data.get('content','')
    start = content.find('## Hebrew Word Notes\n')
    if start != -1:
        after_start = start + len('## Hebrew Word Notes\n')
        next_heading = content.find('\n\n## ', after_start)
        replacement = '## Hebrew Word Notes\n' + notes_section(ch)
        if next_heading != -1:
            content = content[:start] + replacement + content[next_heading:]
        else:
            content = content[:start] + replacement
        data['content'] = content
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    updated_files.append(p)

con = sqlite3.connect(DB)
cur = con.cursor()
for ch in notes:
    p = GEN_DIR / f'{ch:02d}.json'
    data = json.loads(p.read_text(encoding='utf-8'))
    cur.execute("""
        UPDATE commentary_entries
        SET content=?, updated_at=?
        WHERE book_id=1 AND chapter=? AND reference_scope='chapter' AND language_code='en' AND deleted_at IS NULL
    """, (data['content'], data['updated_at'], ch))
con.commit()
rows = cur.execute("SELECT COUNT(*) FROM commentary_entries WHERE book_id=1 AND chapter BETWEEN 1 AND 10 AND deleted_at IS NULL").fetchone()[0]
con.close()
print(json.dumps({'json_files_updated': len(updated_files), 'db_rows_matched': rows, 'example_note_shape': notes[4][0]}, ensure_ascii=False, indent=2))
