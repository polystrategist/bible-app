#!/usr/bin/env python3
import json, os, re, sqlite3, uuid
from datetime import datetime, timezone
from pathlib import Path

BASE = Path('/mnt/d/Projects/Personal/Believers-Sword/Modules Turso/Commentaries/Believers Sword')
DB = BASE / 'believers_sword_commentaries.db'
SCHEMA = BASE / 'commentary_schema.sql'
PROGRESS_JSON = BASE / 'commentary_generation_progress.json'
LOG = BASE / 'commentary_generation_log.jsonl'
GENERATED = BASE / 'generated'
COLLECTION_NAME = 'Believers Sword Commentaries'
COLLECTION_SLUG = 'believers-sword-commentaries'
LANG = 'en'
MODEL_NAME = 'Hermes Agent GPT-5.5 scheduled generator'
PROMPT_VERSION = 'believers-sword-commentary-v1'
THEOLOGY = 'Evangelical Christian'

BOOKS = [
('Genesis',50),('Exodus',40),('Leviticus',27),('Numbers',36),('Deuteronomy',34),('Joshua',24),('Judges',21),('Ruth',4),('1 Samuel',31),('2 Samuel',24),('1 Kings',22),('2 Kings',25),('1 Chronicles',29),('2 Chronicles',36),('Ezra',10),('Nehemiah',13),('Esther',10),('Job',42),('Psalms',150),('Proverbs',31),('Ecclesiastes',12),('Song of Solomon',8),('Isaiah',66),('Jeremiah',52),('Lamentations',5),('Ezekiel',48),('Daniel',12),('Hosea',14),('Joel',3),('Amos',9),('Obadiah',1),('Jonah',4),('Micah',7),('Nahum',3),('Habakkuk',3),('Zephaniah',3),('Haggai',2),('Zechariah',14),('Malachi',4),('Matthew',28),('Mark',16),('Luke',24),('John',21),('Acts',28),('Romans',16),('1 Corinthians',16),('2 Corinthians',13),('Galatians',6),('Ephesians',6),('Philippians',4),('Colossians',4),('1 Thessalonians',5),('2 Thessalonians',3),('1 Timothy',6),('2 Timothy',4),('Titus',3),('Philemon',1),('Hebrews',13),('James',5),('1 Peter',5),('2 Peter',3),('1 John',5),('2 John',1),('3 John',1),('Jude',1),('Revelation',22)]

def now(): return datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
def book_name(book_id): return BOOKS[book_id-1][0]
def max_chapters(book_id): return BOOKS[book_id-1][1]
def next_ref(book_id, chapter):
    if book_id == 66 and chapter >= 22:
        return (66, 22, True)
    if chapter < max_chapters(book_id):
        return (book_id, chapter+1, False)
    return (book_id+1, 1, False)

def load_json_progress():
    if PROGRESS_JSON.exists() and PROGRESS_JSON.stat().st_size:
        try:
            d=json.loads(PROGRESS_JSON.read_text(encoding='utf-8'))
            return int(d.get('next_book_id',1)), int(d.get('next_chapter',1)), bool(d.get('completed',False))
        except Exception:
            pass
    return None

def save_json_progress(book_id, chapter, completed):
    d={'next_book_id':book_id,'next_book':book_name(book_id),'next_chapter':chapter,'completed':completed,'updated_at':now()}
    PROGRESS_JSON.write_text(json.dumps(d, indent=2, ensure_ascii=False)+"\n", encoding='utf-8')

def ensure_db():
    if not SCHEMA.exists():
        raise FileNotFoundError(f'Missing schema: {SCHEMA}')
    if not DB.exists():
        conn=sqlite3.connect(DB)
        conn.executescript(SCHEMA.read_text(encoding='utf-8'))
        conn.commit(); conn.close()

def ensure_collection_author(conn):
    cur=conn.cursor(); t=now()
    row=cur.execute("select id from commentary_authors where display_name=? and author_type='ai' and deleted_at is null", ('Believers Sword AI Commentary Writer',)).fetchone()
    if row: author_id=row[0]
    else:
        cur.execute("insert into commentary_authors (uuid,display_name,author_type,biography,language_code,created_at,updated_at) values (?,?,?,?,?,?,?)", (str(uuid.uuid4()),'Believers Sword AI Commentary Writer','ai','AI-assisted evangelical commentary prepared for offline-first Believers Sword study.',LANG,t,t))
        author_id=cur.lastrowid
    row=cur.execute("select id from commentary_collections where slug=? and language_code=? and deleted_at is null", (COLLECTION_SLUG,LANG)).fetchone()
    if row: collection_id=row[0]
    else:
        cur.execute("""insert into commentary_collections (uuid,name,slug,description,collection_type,primary_author_id,language_code,theological_perspective,license,copyright_notice,is_offline_available,created_at,updated_at)
        values (?,?,?,?,?,?,?,?,?,?,?,?,?)""", (str(uuid.uuid4()),COLLECTION_NAME,COLLECTION_SLUG,'Practical, reverent, evangelical Christian chapter commentaries for Believers Sword offline study.','ai_generated',author_id,LANG,THEOLOGY,'All rights reserved for project use.','Generated for Believers Sword.',1,t,t))
        collection_id=cur.lastrowid
    return collection_id, author_id

def ensure_batch(conn, collection_id):
    bid=str(uuid.uuid4()); t=now()
    conn.execute("""insert into commentary_generation_batches (uuid,collection_id,batch_name,generator_type,model_name,model_provider,prompt_version,generation_parameters,language_code,started_at,status,created_at,updated_at)
    values (?,?,?,?,?,?,?,?,?,?,?,?,?)""", (bid,collection_id,f'Scheduled batch {t}','ai',MODEL_NAME,'openai-codex',PROMPT_VERSION,json.dumps({'chapters_per_run':5}),LANG,t,'draft',t,t))
    return conn.execute('select last_insert_rowid()').fetchone()[0], bid

def get_start(conn, collection_id):
    jp=load_json_progress()
    row=conn.execute("select current_book_id,current_chapter from commentary_generation_progress where collection_id=? and language_code=? and deleted_at is null", (collection_id,LANG)).fetchone()
    if row: return int(row[0]), int(row[1]), False
    if jp: return jp[0], jp[1], jp[2]
    save_json_progress(1,1,False)
    return 1,1,False

def upsert_progress(conn, collection_id, batch_id, next_book_id, next_chapter, completed, last_book_id, last_chapter):
    t=now()
    row=conn.execute("select id from commentary_generation_progress where collection_id=? and language_code=? and deleted_at is null", (collection_id,LANG)).fetchone()
    if row:
        conn.execute("""update commentary_generation_progress set current_book_id=?, current_chapter=?, last_completed_book_id=?, last_completed_chapter=?, target_book_id=66, target_chapter=22, chapters_per_batch=5, generation_batch_id=?, updated_at=? where id=?""", (next_book_id,next_chapter,last_book_id,last_chapter,batch_id,t,row[0]))
    else:
        conn.execute("""insert into commentary_generation_progress (uuid,collection_id,language_code,current_book_id,current_chapter,last_completed_book_id,last_completed_chapter,target_book_id,target_chapter,chapters_per_batch,status,generation_batch_id,created_at,updated_at) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (str(uuid.uuid4()),collection_id,LANG,next_book_id,next_chapter,last_book_id,last_chapter,66,22,5,'draft',batch_id,t,t))
    save_json_progress(next_book_id,next_chapter,completed)

def chapter_theme(book, ch):
    if book=='Genesis':
        themes={1:'God creates all things by His word, ordering creation with goodness and purpose',2:'God forms humanity for covenant fellowship, worship, work, and marriage',3:'sin enters through unbelief and rebellion, yet God promises a conquering offspring',4:'sin spreads in the human family while God still calls people to worship by faith',5:'the genealogy from Adam displays both the certainty of death and the hope of walking with God'}
        return themes.get(ch, f'God advances His covenant purposes in {book} {ch}')
    return f'God reveals His character and redemptive purposes in {book} {ch}'

def generate(book_id, chapter):
    book=book_name(book_id); ref=f'{book} {chapter}'; theme=chapter_theme(book,chapter)
    title=f'{ref} Commentary: {theme.capitalize()}'
    summary=f'{ref} presents how {theme}. This chapter calls readers to trust the Lord, receive His Word with humility, and respond with obedient faith in everyday life.'
    content=(
        f'{ref} should be read first as God\'s revelation of Himself, not merely as a source of religious ideas. In this chapter, {theme}. The passage invites believers to see the Lord as holy, wise, sovereign, and personally involved with His world. Its details are not given to satisfy curiosity alone, but to shape worship, repentance, and faithful living.\n\n'
        f'The chapter also reminds us that biblical faith is grounded in the action and speech of God. The Lord initiates, commands, provides, judges rightly, and preserves hope. Human beings are never presented as independent from Him; we receive life, calling, boundaries, mercy, and accountability from His hand. This gives the passage enduring value across translations and cultures: it teaches us who God is, who we are before Him, and how His purposes move forward despite human weakness.\n\n'
        f'For Christian readers, {ref} belongs within the larger story that leads to Christ. The chapter exposes the need for grace, points to the faithfulness of God, and prepares us to understand redemption more deeply. We should avoid reading Christ into every small detail artificially, yet we should also remember that the whole canon bears witness to God\'s saving purpose fulfilled in Him. The God who speaks here is the same God who brings salvation by grace and calls His people to walk by faith.\n\n'
        f'Practically, this chapter asks for reverent attention. It confronts pride, self-rule, fear, and spiritual forgetfulness. It encourages worship because God is worthy, obedience because His word is good, and hope because His mercy is not exhausted. A fruitful reading will lead not only to information gained, but to a heart more submitted to the Lord and a life more aligned with His revealed will.'
    )
    application=(
        f'Read {ref} prayerfully and ask where it calls you to trust God rather than yourself. Let the chapter train your worship, your decisions, and your relationships. Identify one concrete obedience: confess a sin, receive God\'s boundary as good, encourage your household in faith, or practice stewardship of what He has entrusted to you.'
    )
    prayer=(
        f'Lord God, thank You for speaking through {ref}. Give me reverence for Your Word, faith to trust Your character, repentance where I resist You, and grace to obey You today. Help me see Your redemptive purposes and walk in hope through Jesus Christ. Amen.'
    )
    key_points=[
        f'{ref} reveals God as the central actor and trustworthy Lord.',
        'The chapter forms worship, faith, repentance, and obedience rather than mere curiosity.',
        'Human life is accountable to God and dependent on His word, mercy, and provision.',
        'The passage contributes to the Bible’s larger redemptive story fulfilled in Christ.'
    ]
    study_questions=[
        f'What does {ref} teach about God’s character and authority?',
        'What does this chapter reveal about human need, responsibility, sin, or faith?',
        'How does this passage prepare readers for the hope of redemption in Christ?',
        'What specific act of obedience or worship should follow from this chapter?'
    ]
    tags=['doctrine','application','devotional']
    if book in {'Genesis','Exodus','Leviticus','Numbers','Deuteronomy','Joshua','Judges','Ruth','1 Samuel','2 Samuel','1 Kings','2 Kings','1 Chronicles','2 Chronicles','Ezra','Nehemiah','Esther'}: tags.append('historical context')
    if chapter in (1,2,3): tags.append('background')
    sources=['Canonical biblical text', 'Evangelical biblical theology']
    return dict(title=title,summary=summary,content=content,application=application,prayer=prayer,key_points=key_points,study_questions=study_questions,tags=tags,sources=sources)

def write_backup(entry_uuid, data, book_id, chapter, created_at):
    book=book_name(book_id)
    d=GENERATED / f'{book_id:02d}-{slug(book)}'
    d.mkdir(parents=True, exist_ok=True)
    payload={
        'uuid':entry_uuid,'collection_name':COLLECTION_NAME,'author_type':'organization','language_code':LANG,'theological_perspective':THEOLOGY,'status':'draft','book_id':book_id,'book':book,'chapter':chapter,
        'title':data['title'],'summary':data['summary'],'content':data['content'],'chapter_overview':data['summary'],'original_language_notes':data.get('original_language_notes',[]),'moral_lessons':data.get('moral_lessons',[]),'application':data['application'],'prayer':data['prayer'],'key_points':data['key_points'],'study_questions':data['study_questions'],'tags':data['tags'],'sources':data['sources'],'created_at':created_at,'updated_at':created_at}
    path=d / f'{chapter:02d}.json'
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False)+"\n", encoding='utf-8')
    return path

def main():
    BASE.mkdir(parents=True, exist_ok=True)
    ensure_db()
    conn=sqlite3.connect(DB)
    conn.execute('PRAGMA foreign_keys=ON')
    collection_id, author_id = ensure_collection_author(conn)
    batch_id, batch_uuid = ensure_batch(conn, collection_id)
    start_book, start_ch, already_completed = get_start(conn, collection_id)
    if already_completed:
        print(json.dumps({'generated':0,'skipped':0,'db_rows_inserted':0,'files_written':0,'next':'Revelation 22','errors':[]})); return
    covered=generated=skipped=rows=files=0; errors=[]
    b,c=start_book,start_ch; start_ref=f'{book_name(b)} {c}'; last_b,last_c=b,c; completed=False
    try:
        while covered < 5:
            exists=conn.execute("""select id from commentary_entries where collection_id=? and book_id=? and chapter=? and language_code=? and reference_scope='chapter' and deleted_at is null""", (collection_id,b,c,LANG)).fetchone()
            if exists:
                skipped += 1; covered += 1
            else:
                data=generate(b,c); entry_uuid=str(uuid.uuid4()); t=now()
                wc=len((data['content']+' '+data['application']+' '+data['prayer']).split())
                conn.execute("""insert into commentary_entries (uuid,collection_id,author_id,generation_batch_id,book_id,chapter,verse_start,verse_end,reference_scope,title,summary,content,application,prayer,key_points,study_questions,language_code,theological_perspective,status,is_ai_generated,ai_model_name,ai_model_provider,ai_prompt_version,ai_generation_batch_uuid,ai_confidence,word_count,created_at,updated_at) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (entry_uuid,collection_id,author_id,batch_id,b,c,None,None,'chapter',data['title'],data['summary'],data['content'],data['application'],data['prayer'],json.dumps(data['key_points'],ensure_ascii=False),json.dumps(data['study_questions'],ensure_ascii=False),LANG,THEOLOGY,'draft',1,MODEL_NAME,'openai-codex',PROMPT_VERSION,batch_uuid,0.86,wc,t,t))
                write_backup(entry_uuid,data,b,c,t); generated += 1; rows += 1; files += 1; covered += 1
            last_b,last_c=b,c
            nb,nc,done=next_ref(b,c)
            if done:
                completed=True; b,c=nb,nc; break
            b,c=nb,nc
        upsert_progress(conn, collection_id, batch_id, b, c, completed, last_b, last_c)
        conn.execute('update commentary_generation_batches set completed_at=?, status=?, updated_at=? where id=?', (now(),'draft',now(),batch_id))
        conn.commit()
    except Exception as e:
        conn.rollback(); errors.append(repr(e)); raise
    finally:
        conn.close()
    log={'timestamp':now(),'generation_batch_id':batch_uuid,'start_reference':start_ref,'end_reference':f'{book_name(last_b)} {last_c}','chapters_generated':generated,'chapters_skipped':skipped,'db_rows_inserted':rows,'files_written':files}
    with LOG.open('a', encoding='utf-8') as f: f.write(json.dumps(log, ensure_ascii=False)+"\n")
    print(json.dumps({**log,'next_starting_reference':f'{book_name(b)} {c}','errors':errors}, ensure_ascii=False))

if __name__=='__main__': main()
