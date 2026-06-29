import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

BASE = Path('/mnt/d/Projects/Personal/Believers-Sword/Modules Turso/Commentaries/Believers Sword')
DB = BASE / 'believers_sword_commentaries.db'
GEN_DIR = BASE / 'generated' / '01-genesis'
GEN_DIR.mkdir(parents=True, exist_ok=True)
now = lambda: datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

chapters = {
1: {
 'title':'Genesis 1 — The God Who Creates, Orders, and Blesses',
 'overview':'Genesis 1 introduces God as the eternal Creator who speaks light into darkness, forms order from emptiness, fills creation with life, and crowns humanity with His image. The chapter is not merely about origins; it reveals the character of God: sovereign, wise, generous, purposeful, and good.',
 'words':[{'term':'bārāʾ','language':'Hebrew','meaning':'to create; used with God as the subject, emphasizing divine creative action that depends on no rival power.'},{'term':'tōhû wābōhû','language':'Hebrew','meaning':'formless and empty; the unshaped condition that God orders by His word.'},{'term':'ṣelem','language':'Hebrew','meaning':'image; humanity is made to represent God’s rule and character within creation.'}],
 'themes':['God creates by His word, not by struggle','Creation is repeatedly called good','Human dignity is grounded in the image of God','Rest is built into God’s design'],
 'lessons':['Your life is not accidental; it is created with purpose before God.','God brings order into chaos, so darkness is not final when God speaks.','Human worth does not come from productivity, status, or possessions but from bearing God’s image.'],
 'christ':'The New Testament presents Christ as the Word through whom all things were made. Genesis 1 prepares us to see Jesus not only as Savior but as Lord of creation, the Light who shines into darkness.',
 'prayer':'Creator God, teach me to see the world as Your good gift and my life as Your purposeful design. Speak into the dark and disordered places of my heart, and make me a faithful image-bearer of Your goodness. Amen.'
},
2: {
 'title':'Genesis 2 — The Garden, the Gift, and the Calling of Humanity',
 'overview':'Genesis 2 zooms in on humanity’s place in creation. God forms the man, plants a garden, gives meaningful work, establishes moral boundaries, and creates woman as a corresponding helper. The chapter shows that human life is relational: with God, with creation, and with one another.',
 'words':[{'term':'yāṣar','language':'Hebrew','meaning':'to form or fashion, like a potter shaping clay; it portrays God’s personal care in making man.'},{'term':'ʿēzer kĕnegdô','language':'Hebrew','meaning':'a helper corresponding to him; not inferiority, but a strong companion suited to him.'},{'term':'šāmar','language':'Hebrew','meaning':'to keep, guard, or watch; humanity is called to protect and steward what God entrusts.'}],
 'themes':['Humanity is formed with personal care','Work is a gift before it becomes toil','God’s command gives moral shape to freedom','Marriage is covenant companionship'],
 'lessons':['Freedom without God’s wisdom becomes danger; boundaries can be gifts.','Work is not a curse in itself; it is part of worshipful stewardship.','God designed people for communion, not isolated self-sufficiency.'],
 'christ':'The garden points forward to Christ, the true Bridegroom, who gives Himself for His bride. Where Adam is placed in a garden and later fails, Jesus enters a garden in obedience and surrender.',
 'prayer':'Lord, help me receive my calling, relationships, and boundaries as gifts from You. Teach me to steward what You place in my hands and to love others with covenant faithfulness. Amen.'
},
3: {
 'title':'Genesis 3 — The Fall, the Lie, and the First Promise of Redemption',
 'overview':'Genesis 3 explains why the good world is now marked by sin, shame, pain, conflict, and death. The serpent questions God’s word, humanity distrusts God’s goodness, and sin fractures every relationship. Yet judgment is not the final word: God gives the first promise that the woman’s offspring will crush the serpent.',
 'words':[{'term':'nāḥāš','language':'Hebrew','meaning':'serpent; the deceiver who twists God’s word and invites suspicion against God.'},{'term':'ʿārûm / ʿărummîm','language':'Hebrew wordplay','meaning':'crafty / naked; the chapter contrasts the serpent’s craftiness with humanity’s exposed shame.'},{'term':'zéraʿ','language':'Hebrew','meaning':'seed or offspring; in Genesis 3:15 it becomes a promise of conflict and final victory.'}],
 'themes':['Temptation often begins by distorting God’s word','Sin brings shame and hiding','God judges evil but also seeks sinners','The gospel promise begins immediately after the fall'],
 'lessons':['Do not measure God’s goodness by the serpent’s accusations.','Shame makes people hide, but God’s grace calls them out for healing.','Sin has consequences, yet God’s mercy moves toward sinners before they can repair themselves.'],
 'christ':'Genesis 3:15 is often called the protoevangelium, the first gospel announcement. Christ is the promised offspring who is wounded yet defeats the serpent through His death and resurrection.',
 'prayer':'Merciful Father, expose the lies I have believed and draw me out of hiding. Thank You for promising a Savior before humanity ever deserved one. Keep my heart anchored in Christ’s victory. Amen.'
},
4: {
 'title':'Genesis 4 — Worship, Anger, and the Spread of Sin',
 'overview':'Genesis 4 shows sin moving from the garden into the family. Cain and Abel bring offerings, but Cain’s heart is revealed by resentment and murder. The chapter follows the spread of violence and pride, while also preserving a line of people who begin to call on the name of the Lord.',
 'words':[{'term':'ḥaṭṭāʾt','language':'Hebrew','meaning':'sin; pictured as crouching at the door, ready to dominate if not resisted.'},{'term':'minḥâ','language':'Hebrew','meaning':'offering or tribute; worship is not merely the object offered but the heart before God.'},{'term':'qārāʾ bĕšēm YHWH','language':'Hebrew phrase','meaning':'to call on the name of the LORD; public dependence and worship.'}],
 'themes':['Worship reveals the heart','Unchecked anger can become violence','God warns before judgment','Human culture develops under both common grace and sinful pride'],
 'lessons':['Jealousy must be brought to God quickly before it masters the heart.','Religious activity cannot hide a heart that refuses repentance.','Even when evil grows, God preserves worship and hope.'],
 'christ':'Abel’s blood cries from the ground for justice, but Hebrews says Jesus’ blood speaks a better word. Christ answers both the demand for justice and the need for mercy.',
 'prayer':'Lord, search my worship and my anger. Do not let envy rule me. Teach me to repent quickly, love sincerely, and call upon Your name with a humble heart. Amen.'
},
5: {
 'title':'Genesis 5 — Generations, Death, and the Hope of Walking with God',
 'overview':'Genesis 5 traces Adam’s line through repeated generations. The phrase “and he died” echoes like a bell, showing the reality of the curse. Yet Enoch’s walk with God interrupts the pattern, and Noah’s birth raises hope for comfort in a cursed ground.',
 'words':[{'term':'tôlĕdōt','language':'Hebrew','meaning':'generations or account; a structuring word in Genesis that traces God’s purposes through family lines.'},{'term':'hālak','language':'Hebrew','meaning':'to walk; Enoch’s life is described as ongoing fellowship with God.'},{'term':'nāḥam','language':'Hebrew','meaning':'to comfort or give relief; connected to Noah’s name and the longing for rest from curse.'}],
 'themes':['Death is the repeated consequence of sin','God works through generations','A life can be defined by walking with God','Hope remains even in genealogies'],
 'lessons':['Ordinary faithfulness matters in long histories that only God fully sees.','The certainty of death should teach wisdom, humility, and urgency.','Walking with God is possible even in a fallen world.'],
 'christ':'The genealogy creates longing for the One who can break death’s pattern. Christ enters Adam’s line to become the last Adam, conquering death and giving eternal life.',
 'prayer':'Eternal God, teach me to number my days and walk with You faithfully. Let my life leave a testimony of trust, and anchor my hope in Christ who conquers death. Amen.'
},
6: {
 'title':'Genesis 6 — Corruption, Judgment, and Grace in Noah’s Generation',
 'overview':'Genesis 6 describes the deepening corruption of humanity and God’s grief over violence and evil. Yet in a world under judgment, Noah finds grace. God commands Noah to build the ark, showing that judgment and salvation are both rooted in God’s holy character.',
 'words':[{'term':'ḥāmās','language':'Hebrew','meaning':'violence; the earth is filled with destructive injustice.'},{'term':'ḥēn','language':'Hebrew','meaning':'grace or favor; Noah finds grace before the LORD, not because the world is safe but because God is merciful.'},{'term':'tāmîm','language':'Hebrew','meaning':'blameless or whole; Noah’s integrity contrasts with the corruption around him.'}],
 'themes':['God is grieved by human evil','Judgment is moral, not arbitrary','Grace preserves a remnant','Faith obeys before the rain appears'],
 'lessons':['A corrupt culture does not excuse personal compromise.','God’s patience should not be mistaken for indifference.','Faith often looks like building in obedience long before others understand.'],
 'christ':'The ark points to Christ as the place of refuge from judgment. Those who are in Him are carried safely through waters of judgment into new creation hope.',
 'prayer':'Holy Lord, keep me faithful in a corrupt generation. Give me Noah-like obedience, a heart sensitive to Your holiness, and refuge in Christ alone. Amen.'
},
7: {
 'title':'Genesis 7 — The Flood and the Seriousness of God’s Word',
 'overview':'Genesis 7 records the flood itself. Noah enters the ark as God commanded, the waters rise, and the old world is judged. The chapter is sobering because it shows that God’s warnings are real, but it also shows that God knows how to preserve those who trust Him.',
 'words':[{'term':'mabbûl','language':'Hebrew','meaning':'flood or deluge; used for the catastrophic judgment in Noah’s day.'},{'term':'sāgar','language':'Hebrew','meaning':'to shut or close; the LORD shuts Noah in, emphasizing divine protection.'},{'term':'gābar','language':'Hebrew','meaning':'to prevail or grow strong; the waters prevail over the old world.'}],
 'themes':['God’s warnings become reality','Obedience matters before crisis arrives','Judgment is comprehensive','God Himself secures His people'],
 'lessons':['Delayed judgment is not canceled judgment.','The safest place is wherever God commands you to be.','When God shuts the door of refuge, His people are secure even while judgment falls outside.'],
 'christ':'Jesus compares the days of Noah to the coming judgment. Genesis 7 urges readiness and points us to Christ, the only true refuge before the final day.',
 'prayer':'Lord, make me attentive to Your word and ready in faith. Thank You that in Christ I am not left exposed to judgment but brought into refuge by grace. Amen.'
},
8: {
 'title':'Genesis 8 — Remembered by God and Renewed for Worship',
 'overview':'Genesis 8 turns from rising waters to God’s remembering of Noah. The flood recedes, dry ground appears, and Noah responds with worship. God promises stability in the rhythms of creation despite the continuing reality of human sin.',
 'words':[{'term':'zākar','language':'Hebrew','meaning':'to remember; not mere mental recall, but covenantal action on behalf of someone.'},{'term':'rûaḥ','language':'Hebrew','meaning':'wind or spirit; God sends a wind over the waters, echoing creation language.'},{'term':'nîḥōaḥ','language':'Hebrew','meaning':'pleasing or soothing aroma; Noah’s sacrifice is received by God.'}],
 'themes':['God remembers His people in judgment','New creation imagery follows the flood','Worship is the right response to deliverance','God sustains creation by mercy'],
 'lessons':['When you feel forgotten, God’s covenant care is still active.','Deliverance should lead to worship before it leads to ordinary life.','God’s mercy sustains a world that still needs redemption.'],
 'christ':'Noah’s altar points forward to the sacrifice of Christ, whose offering is fully pleasing to God and secures lasting mercy for His people.',
 'prayer':'Remember me, Lord, according to Your covenant mercy. Let every deliverance in my life become worship, and keep my hope fixed on Christ’s perfect sacrifice. Amen.'
},
9: {
 'title':'Genesis 9 — Covenant, Human Dignity, and the Rainbow of Mercy',
 'overview':'Genesis 9 establishes God’s covenant with Noah and all living creatures. Humanity receives renewed creation commands, the sanctity of life is affirmed, and the rainbow becomes a sign that God will not again destroy the earth by flood. Yet Noah’s failure reminds us that sin remains even after judgment.',
 'words':[{'term':'bĕrît','language':'Hebrew','meaning':'covenant; a binding commitment initiated by God.'},{'term':'qešet','language':'Hebrew','meaning':'bow; the rainbow sign, also the word for a weapon bow, suggesting judgment is restrained by divine mercy.'},{'term':'dām','language':'Hebrew','meaning':'blood; life is sacred because humans bear God’s image.'}],
 'themes':['God binds Himself by covenant mercy','Human life has sacred dignity','Creation continues under God’s promise','The flood did not remove sin from the human heart'],
 'lessons':['Respect for human life is rooted in the image of God, not social usefulness.','Every rainbow is a reminder that mercy triumphs over deserved judgment.','External rescue must be followed by inward transformation, which only God can give.'],
 'christ':'The covenant with Noah preserves the world in which redemption will unfold. In Christ, God’s mercy is not only a restraint of judgment but the full bearing of judgment for sinners.',
 'prayer':'Covenant Lord, thank You for preserving life and showing mercy. Teach me to honor every person as made in Your image and to trust the greater mercy revealed in Jesus. Amen.'
},
10: {
 'title':'Genesis 10 — The Table of Nations and God’s Rule Over All Peoples',
 'overview':'Genesis 10 lists the nations descending from Noah’s sons. What may seem like a simple genealogy is a theological map: all peoples share one origin under God, and God’s purposes are larger than one tribe. The chapter prepares for Babel and eventually for Abraham, through whom all nations will be blessed.',
 'words':[{'term':'gôyim','language':'Hebrew','meaning':'nations or peoples; the chapter emphasizes the spread of peoples under God’s sovereignty.'},{'term':'mišpāḥâ','language':'Hebrew','meaning':'clan or family; nations are described as extended families, not faceless categories.'},{'term':'pārad','language':'Hebrew','meaning':'to separate or divide; the peoples spread according to lands, languages, families, and nations.'}],
 'themes':['All nations belong within God’s providence','Human diversity is known and ordered by God','Genealogy prepares for mission','God’s blessing will eventually extend to all peoples'],
 'lessons':['No nation or people group is outside God’s sight.','Ethnic pride is humbled by the shared origin of all humanity.','God’s mission has always been global, even before Israel’s story begins.'],
 'christ':'Genesis 10 anticipates the promise to Abraham and the Great Commission. In Christ, people from every tribe, language, people, and nation are gathered into one redeemed family.',
 'prayer':'Sovereign God of all nations, enlarge my heart for Your global purpose. Free me from pride and prejudice, and make me a witness of Christ’s blessing to all peoples. Amen.'
}
}

def render_content(ch, d):
    words = '\n'.join(f"- {w['term']} ({w['language']}): {w['meaning']}" for w in d['words'])
    themes = '\n'.join(f"- {t}" for t in d['themes'])
    lessons = '\n'.join(f"- {l}" for l in d['lessons'])
    return f"""## What Genesis {ch} Is About
{d['overview']}

## Theological Insight
{themes}

## Hebrew Word Notes
{words}

## What We Can Learn
{lessons}

## How This Chapter Points to Christ
{d['christ']}

## Believers Sword Reflection
Genesis {ch} calls believers to read Scripture not only for information but for formation. The chapter reveals God's character, exposes the human condition, and invites a faithful response. Its message should move us toward worship, repentance, hope, and obedience.
"""

def slug(s):
    return s.lower().replace(' ', '-')

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
con.execute('PRAGMA foreign_keys=ON')
cur = con.cursor()
ts = now()
# Ensure author and collection
cur.execute("SELECT id FROM commentary_authors WHERE display_name=? AND deleted_at IS NULL", ('Believers Sword Commentary Team',))
row = cur.fetchone()
if row: author_id = row['id']
else:
    cur.execute("INSERT INTO commentary_authors (uuid, display_name, author_type, language_code, created_at, updated_at) VALUES (?,?,?,?,?,?)", (str(uuid.uuid4()), 'Believers Sword Commentary Team', 'organization', 'en', ts, ts))
    author_id = cur.lastrowid
cur.execute("SELECT id FROM commentary_collections WHERE slug=? AND language_code=? AND deleted_at IS NULL", ('believers-sword-commentaries','en'))
row = cur.fetchone()
if row: collection_id = row['id']
else:
    cur.execute("INSERT INTO commentary_collections (uuid, name, slug, description, collection_type, primary_author_id, language_code, theological_perspective, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?)", (str(uuid.uuid4()), 'Believers Sword Commentaries', 'believers-sword-commentaries', 'Chapter-based Believers Sword Bible commentaries.', 'mixed', author_id, 'en', 'Evangelical Christian', ts, ts))
    collection_id = cur.lastrowid

written=[]; updated=0; inserted=0
for ch, d in chapters.items():
    ts = now(); entry_uuid = str(uuid.uuid4())
    content = render_content(ch, d)
    key_points = d['themes'] + d['lessons'] + [d['christ']]
    questions = [
        f'What does Genesis {ch} reveal about God’s character?',
        'Which Hebrew word note helps you understand the chapter more deeply?',
        'What moral or spiritual lesson should shape your decisions this week?',
        'How does this chapter point forward to Christ or God’s redemptive plan?'
    ]
    summary = d['overview']
    application = 'Live with reverent trust in God’s word, humility about the human condition, and practical obedience shaped by the lesson of this chapter. Let the truth move from study into worship, relationships, work, and witness.'
    tags = ['background','doctrine','application','devotional']
    if ch in (3,6,7,8,9): tags.append('prophecy' if ch==3 else 'historical context')
    sources = ['Genesis canonical text', 'Hebrew lexical observations from standard biblical Hebrew usage']
    cur.execute("SELECT id, uuid FROM commentary_entries WHERE collection_id=? AND book_id=1 AND chapter=? AND reference_scope='chapter' AND language_code='en' AND deleted_at IS NULL", (collection_id, ch))
    existing = cur.fetchone()
    word_count = len(content.split())
    if existing:
        cur.execute("""UPDATE commentary_entries SET author_id=?, title=?, summary=?, content=?, application=?, prayer=?, key_points=?, study_questions=?, theological_perspective=?, status='draft', review_notes=?, word_count=?, updated_at=? WHERE id=?""", (author_id, d['title'], summary, content, application, d['prayer'], json.dumps(key_points, ensure_ascii=False), json.dumps(questions, ensure_ascii=False), 'Evangelical Christian', 'Regenerated with deeper chapter overview, Hebrew word notes, moral lessons, and Christ-centered insight.', word_count, ts, existing['id']))
        db_uuid = existing['uuid']; updated += 1
    else:
        cur.execute("""INSERT INTO commentary_entries (uuid, collection_id, author_id, bible_version_id, book_id, chapter, verse_start, verse_end, reference_scope, title, summary, content, application, prayer, key_points, study_questions, language_code, theological_perspective, status, is_ai_generated, review_notes, word_count, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (entry_uuid, collection_id, author_id, None, 1, ch, None, None, 'chapter', d['title'], summary, content, application, d['prayer'], json.dumps(key_points, ensure_ascii=False), json.dumps(questions, ensure_ascii=False), 'en', 'Evangelical Christian', 'draft', 1, 'Generated with chapter overview, Hebrew word notes, moral lessons, and Christ-centered insight.', word_count, ts, ts))
        db_uuid = entry_uuid; inserted += 1
    # Write JSON WITHOUT forbidden keys
    payload = {
        'uuid': db_uuid,
        'collection_name': 'Believers Sword Commentaries',
        'author_type': 'organization',
        'language_code': 'en',
        'theological_perspective': 'Evangelical Christian',
        'status': 'draft',
        'book_id': 1,
        'book': 'Genesis',
        'chapter': ch,
        'title': d['title'],
        'summary': summary,
        'content': content,
        'chapter_overview': d['overview'],
        'original_language_notes': d['words'],
        'moral_lessons': d['lessons'],
        'application': application,
        'prayer': d['prayer'],
        'key_points': key_points,
        'study_questions': questions,
        'tags': tags,
        'sources': sources,
        'created_at': ts,
        'updated_at': ts,
    }
    path = GEN_DIR / f'{ch:02d}.json'
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    written.append(str(path))

# progress to Genesis 11 if not beyond
progress = {
    'next_book_id': 1,
    'next_book': 'Genesis',
    'next_chapter': 11,
    'last_completed_book_id': 1,
    'last_completed_book': 'Genesis',
    'last_completed_chapter': 10,
    'completed': False,
    'updated_at': now()
}
(BASE / 'commentary_generation_progress.json').write_text(json.dumps(progress, ensure_ascii=False, indent=2), encoding='utf-8')
# update DB progress if table available
cur.execute("SELECT id FROM commentary_generation_progress WHERE collection_id=? AND language_code='en' AND deleted_at IS NULL", (collection_id,))
r = cur.fetchone()
if r:
    cur.execute("UPDATE commentary_generation_progress SET current_book_id=1,current_chapter=11,last_completed_book_id=1,last_completed_chapter=10,updated_at=? WHERE id=?", (now(), r['id']))
else:
    cur.execute("INSERT INTO commentary_generation_progress (uuid, collection_id, language_code, current_book_id, current_chapter, last_completed_book_id, last_completed_chapter, target_book_id, target_chapter, chapters_per_batch, status, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (str(uuid.uuid4()), collection_id, 'en', 1, 11, 1, 10, 66, 22, 5, 'draft', now(), now()))
con.commit(); con.close()
# validate forbidden json keys
bad=[]
for p in written:
    data=json.loads(Path(p).read_text(encoding='utf-8'))
    for k in ['is_ai_generated','model_name','prompt_version']:
        if k in data: bad.append((p,k))
print(json.dumps({'inserted': inserted, 'updated': updated, 'json_files_written': len(written), 'forbidden_keys_found': bad, 'next': 'Genesis 11'}, indent=2))
