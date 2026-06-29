"""
Generate Genesis 31–35 commentaries for Believers Sword.
Writes to believers_sword_commentaries.db and generated/01-genesis/<ch>.json
"""

import sqlite3
import json
import os
import uuid
from datetime import datetime, timezone

WORKSPACE = "/mnt/d/Projects/Personal/Believers-Sword/Modules Turso/Commentaries/Believers Sword"
DB_PATH = os.path.join(WORKSPACE, "believers_sword_commentaries.db")
GENERATED_DIR = os.path.join(WORKSPACE, "generated", "01-genesis")
PROGRESS_JSON = os.path.join(WORKSPACE, "commentary_generation_progress.json")
LOG_JSONL = os.path.join(WORKSPACE, "commentary_generation_log.jsonl")

COLLECTION_ID = 1
COLLECTION_NAME = "Believers Sword Commentaries"
BOOK_ID = 1
BOOK = "Genesis"
LANGUAGE_CODE = "en"
BATCH_UUID = str(uuid.uuid4())

FORBIDDEN_KEYS = {"is_ai_generated", "model_name", "prompt_version"}

CHAPTERS = [

# ── GENESIS 31 ─────────────────────────────────────────────────────────────
{
  "chapter": 31,
  "title": "Genesis 31 — The God of Bethel Calls Jacob Home: Flight, Pursuit, and the Covenant at Gilead",
  "summary": "Jacob, sensing Laban's hostility and hearing God's command to return to Canaan, secretly departs with his wives, children, and flocks. Rachel steals her father's household gods (teraphim). Laban pursues and catches Jacob at Gilead after seven days, but God warns him in a dream not to harm Jacob. A heated confrontation ensues: Laban searches in vain for the teraphim (Rachel sits on them), and Jacob delivers a passionate defense of his 20 years of faithful service. The two men make a covenant at the heap of stones called Galeed/Mizpah, establishing a boundary they swear not to cross for harm.",
  "content": """Genesis 31 is the chapter of departure — Jacob finally leaving the land of his exile and beginning the return to Canaan that God promised at Bethel twenty years earlier (28:15). It is also a chapter about divine protection in the midst of human deception, family dysfunction, and competing loyalties.

The chapter opens with a report: Laban's sons are saying Jacob has taken all that belonged to their father (v. 1), and Laban's own face has changed toward Jacob (v. 2). The LORD speaks directly: "Return to the land of your fathers and to your kindred, and I will be with you" (v. 3). God introduces Himself explicitly as "the God of Bethel" (v. 13) — the covenant made in a dream twenty years earlier is now being called in. The hour of return has come.

Jacob calls Rachel and Leah to the field — away from Laban's household — and makes his case for leaving in a remarkable speech (vv. 5–13). He rehearses the entire Haran episode: Laban's repeated changing of his wages (ten times, v. 7), God's protection through the selective breeding (vv. 10–12 — here Jacob reveals that it was a dream, not his rod-strategy, that produced the results), and finally God's command to leave. Rachel and Leah respond with surprising solidarity: "Is there any portion or inheritance left to us in our father's house? Are we not regarded by him as foreigners? For he has sold us and has indeed devoured our money" (vv. 14–15). They are not sentimental about Laban. His daughters have become fully committed to Jacob's household and God's call.

Rachel's theft of the teraphim (v. 19) is one of the most discussed details in the patriarchal narratives. What are teraphim? The Hebrew word refers to household gods — small figurines associated with ancestral religion and possibly (in some ancient Near Eastern contexts) with inheritance rights. Some scholars suggest Rachel stole them to secure a legal claim on Laban's estate; others that she was not yet fully weaned from polytheistic religion; still others that she stole them to prevent Laban from consulting them to track Jacob. The text does not moralize about Rachel's action directly, but the consequences are ironic: Jacob, not knowing Rachel has them, pronounces a death sentence on whoever took them (v. 32). The teraphim become the occasion for one of Scripture's most darkly comic scenes: Rachel sits on the saddlebag containing the gods and tells her father she cannot rise because "the way of women is upon me" (v. 35). The household gods are overpowered by a woman's menstrual impurity — a sharp implicit commentary on their worth.

Jacob's speech to Laban in verses 36–42 is one of the most emotionally raw passages in Genesis. The man who deceived his father and fled from his brother now turns on his father-in-law with righteous anger: "What is my offense? What is my sin, that you have hotly pursued me? For you have felt through all my goods; what have you found of all your household goods? Set it here before my kinsmen and your kinsmen, that they may decide between us two" (vv. 36–37). Jacob then rehearses twenty years of service: the heat of the day, frost at night, sleepless nights, fourteen years for his wives, six for the flocks, wages changed ten times. The culminating verse is theologically central: "If the God of my father, the God of Abraham and the Fear of Isaac, had not been on my side, surely now you would have sent me away empty-handed. God saw my affliction and the labor of my hands and rebuked you last night" (v. 42).

Two divine names appear here that are worth noting. "The God of Abraham" connects Jacob to the original covenant. "The Fear of Isaac" (pachad Yitschak, v. 42) is unusual — it may mean the God whom Isaac fears/reveres, or it may refer to the God who appeared in terror to Isaac at Moriah. Either reading establishes continuity in the patriarchal chain while marking Isaac's particular relationship with God as one of reverential awe.

The covenant ceremony (vv. 44–55) involves a heap of stones, two names (Galeed in Hebrew, "heap of witness"; Jegar-sahadutha in Aramaic — the same meaning), and the famous Mizpah benediction: "The LORD watch between you and me, when we are out of one another's sight" (v. 49). This verse is often used as a warm parting blessing between friends, but in context it is a border treaty: "May God watch to make sure neither of us crosses this boundary to harm the other." The covenant is enforced by the God of Abraham and the God of Nahor, the God of their father (v. 53). Laban kisses his grandchildren and daughters and departs. The long entanglement with Haran is over.

The chapter's theological spine is this: when God commands a return, He guarantees the journey. Laban's hostility, Rachel's theft, the legal confrontations — all are overruled by the "Fear of Isaac" who watches the boundary. Jacob did not leave because the circumstances were favorable; he left because God said to go. The protection of the journey comes not from Jacob's strategy but from the God of Bethel who still remembers His promise.""",

  "chapter_overview": "Jacob departs from Laban in secret after God commands him to return to Canaan. Rachel steals Laban's teraphim. Laban pursues and catches Jacob at Gilead after seven days, warned by God in a dream not to harm Jacob. Laban confronts Jacob over his secret departure and the stolen gods; Jacob defends his 20 years of faithful labor; the teraphim are not found because Rachel conceals them. Jacob and Laban make a stone-heap covenant (Galeed/Mizpah) establishing a boundary of peace.",

  "original_language_notes": [
    {
      "term": "תְּרָפִים (teraphim)",
      "language": "Hebrew",
      "verse": 19,
      "words_used": ["teraphim"],
      "meaning": "Household gods or cult figurines. The word is plural and of uncertain etymology. Teraphim appear in contexts of divination (Ezek. 21:21; Zech. 10:2), ancestral religion, and possibly legal inheritance claims (as attested in Nuzi tablets where possession of household gods could indicate heirship). Rachel's theft is unexplained in motive — the text presents it without endorsement. The irony of the scene: the teraphim are hidden under a menstrual seat, ritually the most impure possible location, rendering them powerless."
    },
    {
      "term": "פַּחַד יִצְחָק (pachad Yitschak)",
      "language": "Hebrew",
      "verse": 42,
      "words_used": ["pachad", "Yitschak"],
      "meaning": "'The Fear of Isaac' — a unique divine name appearing only here and in v. 53. Pachad means dread, terror, or the object of reverent fear. Most likely it refers to 'the One whom Isaac fears/reveres' — a name for God rooted in Isaac's experiential knowledge of God, perhaps from the Moriah event (ch. 22) or the Beersheba theophany (26:24). Some translate 'the Kinsman of Isaac.' Either way, it anchors Jacob's God in Isaac's living relationship — the covenant is personal, not merely inherited."
    },
    {
      "term": "גַּלְעֵד (Galeed)",
      "language": "Hebrew",
      "verse": 47,
      "words_used": ["Galeed"],
      "meaning": "'Heap of witness.' From gal (heap of stones) and ed (witness). Jacob's name for the covenant boundary marker. Laban names it in Aramaic Jegar-sahadutha (the same meaning). The double naming in two languages records the meeting of two linguistic worlds — Jacob's Hebrew world and Laban's Aramean world — under the witness of one God. Galeed gives its name to the region of Gilead (Transjordanian highlands)."
    },
    {
      "term": "מִצְפָּה (Mitzpah)",
      "language": "Hebrew",
      "verse": 49,
      "words_used": ["Mitzpah"],
      "meaning": "'Watchtower' or 'lookout.' From tsafah (to watch, to look out). The Mizpah saying ('May the LORD watch between you and me') is a covenant enforcement clause, not a warm blessing — it invokes God as the only reliable witness when the parties are separated and cannot see one another. Mizpah becomes a place name in multiple regions of the Bible (Gilead, Benjamin, Judah), all suggesting elevated vantage points."
    },
    {
      "term": "עֲמַל כַּפַּי (amal kappai)",
      "language": "Hebrew",
      "verse": 42,
      "words_used": ["amal", "kappai"],
      "meaning": "'The labor/toil of my hands.' Amal refers to wearisome labor, often under oppressive conditions. Kappai is the plural of kaph (palm of the hand). Jacob's climactic argument is that God has seen what his hands have actually produced and rebuke Laban. The phrase is deeply personal — it is not an abstract theological statement but a working man's cry that his labor has been witnessed by God when men have disregarded it."
    }
  ],

  "moral_lessons": [
    "Jacob's departure at God's command — not when circumstances improved but when God spoke — teaches that obedience to divine direction often requires leaving security behind before the way becomes clear.",
    "Rachel's theft of the teraphim illustrates that the people of God can carry old religious attachments and family idols even while following God's call; Jacob's command to put away foreign gods (35:2) becomes necessary precisely because the household had not left them behind at Haran.",
    "Jacob's passionate self-defense (vv. 36–42) models the righteous anger of someone whose decades of faithful labor have been minimized — God sees what people dismiss, and that divine acknowledgment is itself sufficient.",
    "The Mizpah covenant reveals that when human relationships have been too damaged for trust, God can still serve as the enforcing Witness — a high God is sometimes the only neutral party available.",
    "Laban's parting kiss of his grandchildren is poignant: even a manipulative man has genuine love for his family. The Bible rarely presents pure villains — it presents complicated people whose failings coexist with real affections."
  ],

  "application": "Genesis 31 speaks directly to seasons of difficult departure. When God calls us to leave a situation — a job, a relationship, a place — the call rarely comes when circumstances are comfortable. Jacob leaves under suspicion and threat; the departing itself is turbulent. The chapter's invitation is to trust that the God who commands the journey is the God who watches the road. It also speaks to those who carry old idols into new seasons: Rachel brought the teraphim into Canaan. Part of the journey home is always the 35:2 moment — burying what we carried out of our Haran under the oak tree and leaving it behind for good.",

  "prayer": "Lord God of Bethel, You called Jacob home after twenty hard years, and You call us home in every season of exile and displacement. When You say 'return,' give us the courage to pack and leave — even when Laban is still watching, even when the road is uncertain. See the labor of our hands, as You saw Jacob's. Watch the boundaries of our lives when only You can. And where we have hidden household gods in our saddlebags, give us the grace to bury them under the oak and go forward with You alone as our portion. In Jesus' name, Amen.",

  "key_points": [
    "God commands Jacob to return using His covenant name — 'the God of Bethel' — calling in the promise made twenty years earlier (28:15), teaching that God's word stands however long it takes to fulfill.",
    "Rachel and Leah's unanimous response ('Is there any portion for us in our father's house?') shows that Jacob's household is fully aligned with God's call — a moment of remarkable family solidarity.",
    "Rachel's theft of the teraphim (household gods) is presented without editorial condemnation but with irony: the gods end up under a menstrual saddle, suggesting their total impotence.",
    "Jacob's 20-year defense speech (vv. 36–42) is a theology of unseen labor: 'God saw my affliction and the labor of my hands and rebuked you last night' — what people dismiss, God records.",
    "'The Fear of Isaac' (pachad Yitschak) is a rare divine name anchored in personal experiential reverence, reminding us that covenant continuity (Abraham's God) combines with personal encounter (Isaac's awe).",
    "The Mizpah covenant-blessing is actually a border-enforcement clause: God watches the boundary when humans cannot be trusted — a solemn, not sentimental, function for the divine Witness.",
    "The chapter completes Jacob's Haran cycle: he arrived with a staff, he departs with wives, children, servants, and great flocks — God has fulfilled every promise made at Bethel (28:20–22)."
  ],

  "study_questions": [
    "God commanded Jacob to leave, yet the departure involved deception, stolen idols, and a furious pursuit. Does God's command guarantee a clean departure, or only a protected one? What does this teach about following God's direction through messy circumstances?",
    "Rachel stole the teraphim without Jacob's knowledge, and Jacob inherited the consequences (unknowingly pronouncing a death curse on her). How does this episode illustrate the hidden costs of unaddressed family spiritual compromises?",
    "Jacob's speech in vv. 36–42 is raw, angry, and entirely justified. Are there moments when righteous anger at injustice is the appropriate response — even in family confrontations? What boundaries did Jacob observe even in his anger?",
    "The Mizpah benediction ('The LORD watch between you and me') is often used as a warm farewell. Read it in context. How does knowing it was a covenant enforcement clause change how you hear it? When is God as Witness the only available form of accountability?",
    "Jacob left with far more than he arrived with, fulfilling God's promise at Bethel (28:20–22). Looking back, where do you see moments in your own life where God was quietly fulfilling a promise while you were simply working faithfully through ordinary days?"
  ],

  "tags": ["Genesis", "Jacob", "Laban", "Rachel", "Leah", "teraphim", "Mizpah", "covenant", "departure", "providence", "household gods", "Gilead"],
  "sources": []
},

# ── GENESIS 32 ─────────────────────────────────────────────────────────────
{
  "chapter": 32,
  "title": "Genesis 32 — Peniel: The Night Jacob Wrestled with God and Became Israel",
  "summary": "Jacob, journeying home, is met by angels and sends messengers to Esau, learning that Esau is approaching with 400 men. In fear, Jacob divides his company, prays, and sends elaborate gifts ahead. That night, alone at the ford of Jabbok, Jacob wrestles with a mysterious Man until dawn. When the Man sees He cannot overpower Jacob, He dislocates Jacob's hip; Jacob clings and demands a blessing. The Man renames him 'Israel' ('he strives with God and prevails') and blesses him. Jacob names the place Peniel ('face of God'), saying he has seen God face to face and survived. He limps as he crosses the Jabbok.",
  "content": """Genesis 32 is the pivot of Jacob's story and one of the most theologically dense chapters in all of Scripture. Jacob has been running his entire life — from Esau, to Haran, now from Laban — but at the Jabbok ford God stops him and transforms him. The chapter is the answer to what began in the womb (25:26) and what was hinted at Bethel (28:10–22): the God who pursues Jacob is the God who reshapes him.

The chapter opens with angels: "Jacob went on his way, and the angels of God met him" (v. 1). Jacob names the place Mahanaim ('two camps'), and the double-camp motif carries into his human strategy (v. 7 — he divides his people into two camps so one might survive Esau's attack). The angels at the beginning foreshadow the divine encounter at the end — Jacob's world is saturated with heavenly presence even when he cannot see it.

The fear that grips Jacob in verse 7 is described with unusual force: "Jacob was greatly afraid and distressed" — two near-synonyms piled together to convey paralysis. Esau and 400 men. Jacob's mind immediately calculates losses: if Esau attacks one camp, the other might escape (v. 8). His prayer (vv. 9–12) is one of the most carefully constructed prayers in Genesis. It begins with covenantal ground: "O God of my father Abraham and God of my father Isaac, O LORD who said to me, 'Return to your country and to your kindred, that I may do you good'" (v. 9). Jacob anchors his prayer in God's own word — not his own worthiness. Then comes one of the great moments of humility in the patriarchal narrative: "I am not worthy of the least of all the deeds of steadfast love and all the faithfulness that you have shown to your servant" (v. 10). The man who deceived his father and wrestled his brother has reached a moment of honest self-assessment. Yet he does not stop praying; he moves to petition: "Please deliver me from the hand of my brother, from the hand of Esau, for I fear him" (v. 11). The prayer closes by quoting God's promise: "You said, 'I will surely do you good, and make your offspring as the sand of the sea'" (v. 12). Jacob is reminding God of God's own word — a form of faith-in-prayer that runs throughout the Bible (Moses in Ex. 32:13; Nehemiah 1:8; the Psalms).

Jacob sends his gifts ahead in strategic waves (vv. 13–21): 200 female goats, 20 male goats, 200 ewes, 20 rams, 30 milking camels with their calves, 40 cows, 10 bulls, 20 female donkeys, 10 male donkeys. The scale is staggering. Each drove of animals is a separate wave of gift, with instructions: "Let there be space between each drove" (v. 16). Jacob wants to overwhelm Esau with accumulated generosity before the face-to-face meeting. He is not merely being strategic; he is trying to "appease" (kipper, v. 20) his face — the same root used later for the Day of Atonement. Jacob is doing what he can; God will have to do the rest.

Then the wrestling. Jacob is alone. A Man wrestles with him until dawn (vv. 24–32). The narrative is spare and physical: "and the Man saw that he did not prevail against Jacob" (v. 25). The Hebrew word for "prevail" is yakol — to be able, to overcome. The mysterious wrestler cannot overcome Jacob by ordinary force. When He touches Jacob's hip socket and dislocates it, Jacob does not let go. This is extraordinary: a dislocated hip is disabling, agonizing — and Jacob clings. "I will not let you go unless you bless me" (v. 26).

The Man's question — "What is your name?" — is not a request for information. It parallels Isaac's question in 27:18 ("Who are you, my son?"), which Jacob answered with the lie that cost him decades of exile. Now, at the Jabbok, Jacob answers honestly: "Jacob" — the deceiver, the supplanter, the heel-grabber. The true name, spoken honestly, is the turning point. The Man responds: "Your name shall no longer be called Jacob, but Israel, for you have striven with God and with men, and have prevailed" (v. 28). Israel means "he strives with God" or "God strives" — the name is deliberately ambiguous in Hebrew (from sarah, to strive, and El, God). The name carries the wrestling — Jacob's entire biography in two syllables.

When Jacob asks the Man's name, the answer is a question: "Why is it that you ask my name?" And then the Man blesses him. Jacob names the place Peniel: "For I have seen God face to face, and yet my life has been delivered" (v. 30). The Hebrew word for "face" — panim — appears repeatedly in this chapter. Jacob has wrestled with God face to face; he is about to face his brother Esau. The two confrontations are related: the one who has faced God can face men.

Hosea 12:3–4 interprets the Jabbok as a moment of prayer: "In the womb he took his brother by the heel, and in his manhood he strove with God. He strove with the angel and prevailed; he wept and sought his favor." Hosea adds the weeping — Jacob's clinging was not triumphant grasping but desperate, tearful dependence. That changes the picture considerably.

Jacob limps as he crosses the Jabbok. The wound is permanent. The naming of Israel is inseparable from the limping. God's blessing did not remove the injury; the injury is the mark of the encounter. In every subsequent generation of the people who bear Jacob's new name, they will be asked: why do you not eat the sinew of the hip? The answer is: because of this night. The nation's identity is marked by the place where their ancestor was broken open and renamed.

This chapter is a theology of encounter: God must sometimes disable what we are relying on — our strength, our strategy, our running — before He can rename who we are. Jacob the deceiver became Israel the God-wrestler not despite the darkness and the dislocated hip, but through it.""",

  "chapter_overview": "Jacob heads toward Canaan and is met by angels. News of Esau approaching with 400 men fills him with fear; he divides his camp, prays, and sends gifts ahead in waves. That night, alone at the Jabbok ford, Jacob wrestles with a mysterious Man until dawn. The Man cannot overpower Jacob; He dislocates Jacob's hip socket. Jacob refuses to release the Man without a blessing. The Man renames Jacob 'Israel' — 'he strives with God' — and blesses him. Jacob calls the place Peniel. He limps from the injury; Israel does not eat the hip sinew to this day.",

  "original_language_notes": [
    {
      "term": "יִשְׂרָאֵל (Yisrael)",
      "language": "Hebrew",
      "verse": 28,
      "words_used": ["Yisrael"],
      "meaning": "The name 'Israel' derives from the root sarah (שָׂרָה, to strive, to persist, to struggle) + El (God). Possible meanings: 'he strives with God,' 'God strives,' or 'one who persists with God.' The name is ambiguous in Hebrew — it can be active (Jacob strives) or passive (God strives for him). Both dimensions are theologically appropriate: Jacob wrestled, but it was God who initiated the encounter. The nation named after Jacob inherits both the struggle and the blessing."
    },
    {
      "term": "פְּנִיאֵל (Peniel) / פְּנוּאֵל (Penuel)",
      "language": "Hebrew",
      "verse": 30,
      "words_used": ["Peniel", "Penuel"],
      "meaning": "'Face of God' — from panim (face) + El (God). Jacob names the location after his encounter: 'I have seen God face to face (panim el panim) and my life is preserved.' The word panim is plural in form in Hebrew (a plural of intensity or majesty), always used for the face/presence of God. The name becomes the city of Penuel in the Transjordan region, mentioned in later history (Judges 8:8; 1 Kings 12:25)."
    },
    {
      "term": "יְאָבֵק (Yabbok)",
      "language": "Hebrew",
      "verse": 22,
      "words_used": ["Yabbok"],
      "meaning": "The Jabbok River (modern Zarqa in Jordan), a tributary of the Jordan flowing into it from the east. The Hebrew name contains the same consonants as 'wrestle' (ye'avek, from avak) — the wordplay is deliberate: Jacob wrestles (ye'avek) at the Jabbok (Yabbok). The location is a liminal space: a ford between two lands, at night, alone. Ancient Near Eastern thought associated fords and thresholds with dangerous spiritual encounters."
    },
    {
      "term": "כַּף יֶרֶךְ (kaph yerekh)",
      "language": "Hebrew",
      "verse": 25,
      "words_used": ["kaph", "yerekh"],
      "meaning": "'Hip socket' — literally 'the hollow/palm of the thigh.' Kaph means the hollow or palm (same word as the palm of the hand); yerekh means the thigh or upper leg. The phrase refers to the joint at the top of the femur. This is the location of the injury that produced Jacob's permanent limp. The sinew of this joint (gid hanasheh, v. 32) became permanently forbidden as food in Israel — one of the oldest Jewish dietary restrictions, rooted in this night."
    },
    {
      "term": "כִּפֶּר (kipper)",
      "language": "Hebrew",
      "verse": 20,
      "words_used": ["kipper"],
      "meaning": "'To appease / cover / atone.' Jacob says 'I will appease (akapper) his face with the gift that goes before me.' The root kpr is the same word used for the Day of Atonement (Yom Kippur) and the mercy seat (kapporeth). Jacob's gift-giving before facing Esau uses the same word that will later describe Israel's ritual atonement before God. The gifts 'cover' the offense just as the blood on the mercy seat covers Israel's sin. The domestic act and the liturgical act share a vocabulary."
    }
  ],

  "moral_lessons": [
    "Jacob's prayer (vv. 9–12) teaches the structure of biblical petition: anchor in God's promise, confess unworthiness, make specific request, quote God's own word back to Him — all while continuing to act.",
    "The wrestling match models a theology of persisting with God in the dark seasons: Jacob did not let go even when he was injured. The limp was the price of the blessing, and he accepted it.",
    "Jacob's honest answer — 'My name is Jacob' — is the pivot of the encounter. Confessing what we actually are (deceiver, grasper, supplanter) is the precondition for being renamed by God.",
    "The permanent limp from the divine encounter teaches that genuine transformation by God is not costless. Jacob walked differently for the rest of his life because he had met God at the Jabbok.",
    "God could have prevailed against Jacob by force from the beginning; He chose to wrestle through the night, suggesting God honors persistent, desperate, clinging faith rather than crushing it."
  ],

  "application": "Genesis 32 speaks to anyone in a dark night before a feared confrontation. Jacob stood to lose everything — his family, his life, his future — and God chose that night to wrestle with him rather than simply reassure him. The chapter's invitation is not to avoid the night but to cling through it. When God seems to be against you, it may be that He is actually reshaping you. The blessing comes at dawn, after the night, to the person who refused to let go even when injured. And the name change — from Jacob to Israel — announces that who you were is not who you will be, provided you are willing to be honest about who you were.",

  "prayer": "Lord, meet us at the Jabbok — in the dark, in the alone, in the night before the feared morning. Disable what we have relied on apart from You. We confess our names honestly: we are graspers, deceivers, heel-grabbers. Rename us. Bless us. And if the blessing comes with a limp, let us receive both together, knowing the wound is the mark of Your encounter and the limp is the testimony that we have seen Your face and lived. In Jesus' name, Amen.",

  "key_points": [
    "Jacob's prayer (vv. 9–12) is a masterclass in biblical petition: he cites God's covenant name, quotes God's own promise, confesses his unworthiness, makes a specific request, and ends by holding God to His word.",
    "The angels at the opening (Mahanaim, v. 2) and the Man at the crossing frame the chapter: Jacob's journey is surrounded by heavenly presence he cannot always see.",
    "The mysterious Wrestler cannot overpower Jacob by direct force — a theologically astonishing detail. God honors Jacob's persistence rather than simply overwhelming it.",
    "Jacob's confession of his name ('Jacob' = deceiver/supplanter) is the pivot of the encounter — honesty about who he is becomes the doorway to who he will be.",
    "The name 'Israel' (he strives with God / God strives) becomes the permanent identity of both the man and the nation — a people defined by their wrestling with God rather than their ease with Him.",
    "Peniel ('face of God') and the limp are inseparable: Jacob does not emerge from the encounter unscathed, and the injury is permanent — genuine transformation always costs something.",
    "The dietary law (not eating the sinew of the hip, v. 32) embeds the Jabbok night into Israel's daily bodily practice — every meal is a memorial to the night Jacob was broken and renamed."
  ],

  "study_questions": [
    "Jacob prays by quoting God's own promise back to Him (v. 12). Why is this a legitimate form of prayer rather than manipulation? What does it reveal about how God wants us to engage with His word?",
    "The Wrestler could not overpower Jacob (v. 25). What does it mean that God honors Jacob's persistence? Are there situations where God waits for us to cling rather than simply resolving the situation immediately?",
    "Jacob's honest answer 'My name is Jacob' — the deceiver — is the turning point. When have you had to honestly name what you are (rather than what you aspire to be) before God could rename you?",
    "Jacob received both a blessing and a permanent limp from the same encounter. What does the permanence of the limp suggest about the relationship between genuine transformation and ongoing vulnerability?",
    "Hosea 12:4 says Jacob 'wept and sought God's favor' in this encounter. How does the addition of tears change your picture of Jacob's wrestling? What does it suggest about strength and desperation in prayer?"
  ],

  "tags": ["Genesis", "Jacob", "Israel", "Peniel", "Jabbok", "wrestling", "prayer", "transformation", "Esau", "name change", "perseverance", "encounter with God"],
  "sources": []
},

# ── GENESIS 33 ─────────────────────────────────────────────────────────────
{
  "chapter": 33,
  "title": "Genesis 33 — Esau Runs to Embrace: Reconciliation, Restored Brotherhood, and the God of New Beginnings",
  "summary": "Jacob crosses the Jabbok, limping, and arranges his family in order of vulnerability (servants first, then Leah, then Rachel and Joseph). He himself goes ahead and bows seven times as Esau approaches with 400 men. Esau runs and embraces Jacob, weeping. Esau meets Jacob's family and asks about the gift-droves he received; Jacob says they are to find favor. Esau offers to escort Jacob to Seir; Jacob demurs, citing the pace of children and flocks. Esau returns to Seir; Jacob travels to Succoth, builds shelters, then arrives at Shechem and purchases a plot of land, where he erects an altar he names El-Elohe-Israel.",
  "content": """Genesis 33 is the resolution of a forty-year crisis. Jacob and Esau have not seen each other since Jacob fled with the stolen blessing (27:41–45). Esau swore to kill his brother. Now they meet, and what happens is one of Scripture's most moving scenes of reconciliation — and one of its most carefully crafted acts of narrative theology.

The chapter opens with Jacob seeing Esau and the 400 men — and immediately arranging his family in the order of their relative value to him (v. 2). The servants and their children first, Leah and her children next, Rachel and Joseph last. It is a moment of honest human calculation: if the worst happens, those he loves most will have the most time to escape. He himself goes ahead of all of them — an act of courage or of accepting responsibility for what his deception has set in motion, or both.

Jacob bows to the ground seven times as he approaches his brother. Seven prostrations is the formal greeting of an inferior to a superior — it is what diplomatic correspondence from Canaan to Egypt used for subjects addressing the Pharaoh. Jacob is offering himself as the lesser, the supplicant, the one who owes a debt. The context of the seven bows echoes the seven years Jacob served for Rachel, the seven years for Leah — Jacob's life has been structured by sevens.

"But Esau ran to meet him and embraced him and fell on his neck and kissed him, and they wept" (v. 4). The verse is spare and overwhelming. Esau does not respond with the measured acknowledgment of a received protocol; he runs. He embraces. He falls on Jacob's neck. They weep together. The verse echoes — intentionally — the parable Jesus would tell in Luke 15: the father who sees his son "while he was still a long way off" and runs and falls on his neck and kisses him. Jesus knew this verse when He told that story. The older brother who is outside the feast in Luke 15 is Esau transposed into a parable with a different ending — or perhaps the same ending, since Esau did receive Jacob with grace.

Esau asks about the gift-droves (v. 8). Jacob's answer is a sentence that deserves to be read slowly: "To find favor in the sight of my lord" (v. 8). He is not giving gifts out of guilt or strategy alone; he is seeking restored relationship — the phrase is the same one used of covenant relationship and of God's grace throughout the Old Testament (to find favor/grace in the eyes of). Esau declines: "I have enough, my brother; keep what you have for yourself" (v. 9). The word "brother" — in Esau's mouth, after forty years of estrangement — is the reconciliation in a single word. Jacob insists, using language of extraordinary weight: "Please, if I have found favor in your sight, then accept my present from my hand. For I have seen your face, which is like seeing the face of God, and you have accepted me" (v. 10). "Seeing your face is like seeing the face of God" — the day before, Jacob saw the face of God at Peniel and survived; today he sees Esau's face and the same verb of survival applies. The brother who was supposed to kill him has shown him grace. God's face and a brother's forgiving face are, for Jacob at this moment, of the same order of gift.

The further conversation about traveling together is interesting and has been read differently by commentators. Esau offers to escort Jacob to Seir; Jacob declines, citing the pace of children and nursing animals (v. 13). He says he will come to Seir at his own pace. He then goes to Succoth — not toward Seir at all. Has Jacob deceived his brother again? Some read it that way. Others suggest Jacob simply changed plans without malice, that the two households were better off establishing themselves separately. The text does not adjudicate — it reports. What is clear is that Jacob and Esau do meet again at their father Isaac's burial (35:29), suggesting that the relationship remained viable even if they lived separately.

Jacob arrives at Shechem and purchases land (vv. 18–20). The purchase of land in Canaan by a patriarch is always significant — Abraham bought the cave at Machpelah (ch. 23) to bury Sarah; now Jacob buys land to build a camp. Both purchases are acts of faith: these foreigners are staking a claim in the land God promised to their seed. Jacob erects an altar and names it El-Elohe-Israel: "God, the God of Israel." The name is his first act of public worship under his new name. He is not calling the altar after himself but after the God who wrestled with him and renamed him — the God who is specifically and personally the God of this Israel, this limping, renamed, reconciled man.

The chapter as a whole presents a theology of reconciliation that runs deeper than mere diplomacy. The grace Esau showed Jacob was not earned, was not deserved, came after decades of absence and injury. It came while Jacob was still bowing in submission, still bearing the marks of his guilt. And Jacob recognized it as, in some sense, a divine gift: "seeing your face is like seeing the face of God." The grace of a forgiving brother is one of the faces through which God's grace is made visible in the world.""",

  "chapter_overview": "Jacob, limping from the Jabbok, arranges his family in order and goes ahead alone, bowing seven times as Esau approaches. Esau runs and embraces Jacob with tears — a stunning reconciliation. Esau meets the family; Jacob explains the gift-droves as expressions of seeking favor. Jacob calls Esau's face 'like the face of God.' Esau offers to escort Jacob; Jacob politely declines and eventually travels to Succoth, where he builds shelters, then to Shechem, where he purchases land and builds an altar named El-Elohe-Israel.",

  "original_language_notes": [
    {
      "term": "וַיָּרָץ עֵשָׂו לִקְרָאתוֹ (va-yaratz Esav likrato)",
      "language": "Hebrew",
      "verse": 4,
      "words_used": ["va-yaratz", "Esav", "likrato"],
      "meaning": "'And Esau ran to meet him.' The verb ruts (to run) is the same used in Luke 15's background narrative — the father who runs toward his returning son. In ancient Near Eastern culture, running was undignified for a person of status; Esau abandons dignity to close the distance. The verse's four verbs in rapid sequence — ran, embraced, fell on his neck, kissed — create a breathless pace that mirrors the emotional acceleration of the reunion."
    },
    {
      "term": "כִּרְאוֹת פְּנֵי אֱלֹהִים (kir'ot pnei Elohim)",
      "language": "Hebrew",
      "verse": 10,
      "words_used": ["kir'ot", "pnei", "Elohim"],
      "meaning": "'Like seeing the face of God.' Jacob says seeing Esau's face is like seeing pnei Elohim. The phrase directly echoes Peniel (32:30) — 'I have seen God face to face.' The Jabbok night and the Esau morning are theologically connected: both encounters are described as seeing the divine face. Jacob is recognizing that reconciling grace, wherever it appears, bears a family resemblance to God's own grace."
    },
    {
      "term": "אֵל אֱלֹהֵי יִשְׂרָאֵל (El Elohe Yisrael)",
      "language": "Hebrew",
      "verse": 20,
      "words_used": ["El", "Elohe", "Yisrael"],
      "meaning": "'God, the God of Israel.' Jacob's altar name is his first public act of worship under his new name. The name is personal and possessive — not merely 'God the Creator' but the God who is specifically and personally the God of this Israel, this renamed man. Elohe is the construct form of Elohim (God of...). The name anticipates the Exodus formula 'I am the LORD your God' — covenant identity language binding a divine person to a specific people."
    },
    {
      "term": "מִנְחָה (minchah)",
      "language": "Hebrew",
      "verse": 10,
      "words_used": ["minchah"],
      "meaning": "'Gift / present / tribute offering.' Jacob repeatedly calls the animals he sent ahead a minchah. The word is also the standard word for the grain offering in Levitical sacrifice — the gift that accompanies a burnt offering and is presented before God. Jacob's minchah to Esau occupies the same semantic field as Israel's offering to God: both are acts of approach, of seeking favor, of restoring relationship with one who was offended."
    },
    {
      "term": "סֻכּוֹת (Succoth)",
      "language": "Hebrew",
      "verse": 17,
      "words_used": ["Succoth"],
      "meaning": "'Booths / shelters.' From sakak (to cover, to shelter). Jacob builds booths (sukkot) for himself and stalls for his livestock — the first permanent structures he has built in Canaan. The place takes its name from the structures. Succoth also becomes the first stopping point of the Exodus (Num. 33:5), making it a place of new beginnings for both the patriarch and the nation. The Feast of Booths (Sukkot) commemorates Israel's wilderness dwelling and shares this root."
    }
  ],

  "moral_lessons": [
    "Esau's running embrace after forty years of estrangement demonstrates that human hearts, shaped by time and God's quiet work, can receive those who have wronged them with genuine grace.",
    "Jacob's posture — bowing seven times, approaching humbly — models that seeking reconciliation requires the one who caused the harm to approach first, to submit first, to seek favor rather than demand it.",
    "Jacob's naming of the altar El-Elohe-Israel is the first act of worship after the Peniel transformation: before settling, before building a house, he builds an altar — establishing that the new Israel's first priority is worship of the God who renamed him.",
    "The chapter's placement immediately after the Jabbok wrestling teaches that the inner transformation (wrestling with God) precedes the relational healing (reconciling with Esau) — we cannot give to others what we have not received from God.",
    "Jacob's acknowledgment that Esau's face is 'like the face of God' models a spiritually mature vision: the forgiving face of another person can be the place where divine grace becomes visible and tangible."
  ],

  "application": "Genesis 33 is the chapter for anyone who fears an overdue reconciliation. Jacob spent twenty years dreading the moment he would face Esau — and when it came, Esau ran toward him. The chapter does not promise that every feared reunion will end this way; Esau's grace was a gift, not a guarantee. But it does promise that the one who has faced God at their own Jabbok — who has been honest about who they are and received God's blessing through the night — can face any human confrontation with a different posture than defensive strategy. Go ahead of your people. Bow down. Let the other person run to you or not. El-Elohe-Israel is the God who made this possible.",

  "prayer": "God of Israel, You are the God of reconciliations we did not dare to hope for. Thank You for Esau's run — for the brother's embrace that Jacob did not deserve and could not have predicted. Where we have injured relationships that need to be faced, give us Jacob's courage to go ahead and bow. Where we are in Esau's position — nursing a legitimate wound — give us the grace to run. Let every forgiving face become for us a glimpse of Your own. And wherever we set up our tents, let the first thing we build be an altar to You. In Jesus' name, Amen.",

  "key_points": [
    "Jacob's arrangement of his family in order of vulnerability (servants first, beloved last) and his going ahead alone shows a mix of protective love and personal accountability — he will face the consequences of his past first.",
    "Esau's running, embracing, and weeping are the narrative surprise of Genesis — the intended killer has become the forgiver, suggesting decades of God quietly working in Esau's heart.",
    "Jacob's 'seeing your face is like seeing the face of God' (v. 10) connects Esau's grace directly to the Peniel encounter: the God who showed grace at the ford now shows grace through a brother's face.",
    "The altar named El-Elohe-Israel ('God, the God of Israel') is Jacob's first worship under his new name — a declaration that his identity is now publicly defined by his relationship with this God.",
    "Succoth (booths/shelters) is Jacob's first established camp in Canaan, and its name anticipates both the Exodus stopping point and Israel's annual Feast of Booths — the patriarch's rest point becomes a permanent memorial.",
    "The purchase of land at Shechem, like Abraham's purchase at Machpelah, is an act of faith in the promise: these wanderers buy ground in the promised land as a down payment on a future they trust but do not yet possess.",
    "The chapter demonstrates that the sequence God uses is: encounter God → then face your brother. Inner transformation precedes relational healing."
  ],

  "study_questions": [
    "Jacob arranged his family with Rachel and Joseph last — those he loved most, most protected. What does this reveal about his love? Is it admirable, troubling, or both?",
    "Esau's running to embrace Jacob parallels the father's running to embrace the prodigal son in Luke 15. If Jesus had Genesis 33 in mind, what is he saying about God's reception of returning sinners?",
    "Jacob says Esau's forgiving face is 'like the face of God.' Have you experienced a moment when another person's grace toward you gave you a glimpse of what God's grace feels like? How did it change you?",
    "Jacob builds an altar immediately upon arriving at Shechem — before building a house or establishing a residence. What does this sequence suggest about the role of worship in establishing a new beginning?",
    "Some commentators read Jacob's polite refusal to travel with Esau (and subsequent travel away from Seir) as another deception. Others read it as a reasonable separation of households. What do you think? What values are in tension in that reading?"
  ],

  "tags": ["Genesis", "Jacob", "Esau", "reconciliation", "forgiveness", "El-Elohe-Israel", "Shechem", "Succoth", "worship", "brotherly grace", "return to Canaan"],
  "sources": []
},

# ── GENESIS 34 ─────────────────────────────────────────────────────────────
{
  "chapter": 34,
  "title": "Genesis 34 — Dinah, Shechem, and the Violence of Simeon and Levi: Justice, Vengeance, and the Cost of Deception",
  "summary": "Dinah, Jacob's daughter by Leah, goes out to see the women of the land and is seized and violated by Shechem son of Hamor the Hivite, who then desires to marry her. Hamor comes to negotiate; Jacob's sons return from the field furious. Hamor proposes intermarriage between their peoples; Jacob's sons demand all Shechem's men be circumcised. Shechem and Hamor agree and persuade their city. On the third day, while the men are in pain, Simeon and Levi attack, kill all the men, and take Dinah. The other brothers plunder the city. Jacob is horrified; his sons respond 'Should he treat our sister like a prostitute?'",
  "content": """Genesis 34 is the most disturbing chapter of the Jacob narrative and one of the most carefully constructed morally ambiguous chapters in the Bible. It presents four interlocking violations — Shechem's violation of Dinah, Jacob's silence in the face of his daughter's assault, Simeon and Levi's deceptive massacre, and the other brothers' opportunistic plunder — and refuses to resolve the moral tension neatly. The chapter ends with two unanswered questions, one from Jacob and one from his sons, and neither is answered in the text.

The chapter opens with a single defining sentence: "Now Dinah the daughter of Leah, whom she had borne to Jacob, went out to see the women of the land" (v. 1). Dinah is specifically identified as Leah's daughter — the connection matters in the sibling dynamics that follow, since Simeon and Levi are also Leah's sons. Her going out to "see the women of the land" is presented without moral comment; it is an ordinary thing for a young woman to want to do, to find female companionship in a new territory.

What happens next is narrated with clinical precision: "And when Shechem the son of Hamor the Hivite, the prince of the land, saw her, he seized her and lay with her and humiliated her" (v. 2). Three verbs — seized, lay with, humiliated. The first and third frame the act as violation; the middle provides the act itself. The word "humiliated" (innah) is the same used for Hagar's oppression (16:6) and Israel's Egyptian bondage (Ex. 1:12). It is the word for the suffering of the powerless under the powerful.

Then the complicating verse: "And his soul was drawn to Dinah the daughter of Jacob. He loved the young woman and spoke tenderly to her" (v. 3). Shechem desires Dinah after the assault. He wants to marry her. He speaks "to her heart" (al lev hanaarah) — the phrase used when Joseph's brothers speak to Jacob's heart (50:21) and when Boaz speaks to Ruth's heart (Ruth 2:13). The text does not excuse the assault; it insists simultaneously on Shechem's genuine attachment. The human beings in this chapter are not simple moral categories.

Hamor's negotiation with Jacob (vv. 6–10) is public and seemingly reasonable: intermarriage, trade, common prosperity. But Jacob's silence throughout the negotiation is striking. The text says Jacob heard what happened and "held his peace" until his sons came (v. 5). The word for "held his peace" (hecharish) means to be silent, to withhold speech. Some read this as wisdom (waiting for his sons); others as a failure of fatherly protection. The narrative does not interpret; it records.

Jacob's sons return from the field and react with grief and fury: "the men were indignant and very angry, because he had done an outrageous thing (nebalah) in Israel by lying with Jacob's daughter, for such a thing must not be done" (v. 7). The term nebalah — outrage, disgrace, a violation of the moral order — is the same applied to the rape of Tamar by Amnon (2 Sam. 13:12) and to sexual violations in Judges. The sons are naming what Shechem did correctly, even if their response will be disproportionate.

Simeon and Levi's plan is deceptive. They require circumcision — the covenant sign of God's people — as a condition of intermarriage, with no intention of honoring the agreement. They weaponize the sacred. The men of Shechem undergo circumcision, and on the third day, while in pain, Simeon and Levi attack and kill every male. They rescue Dinah from Shechem's house (v. 26 — she was still there). The other brothers then take the plunder: flocks, herds, donkeys, women, children, wealth.

Jacob's response is immediate and pragmatic: "You have troubled me by making me stink to the inhabitants of the land" (v. 30). His concern is retaliation and his own precarious position. He does not address the justice of the cause, only the political danger. This is a different Jacob from the man who prayed at the Jabbok; the crisis of his daughter's assault has not produced the prayer-warrior of chapter 32 but a frightened householder calculating political survival.

Simeon and Levi's final answer — "Should he treat our sister like a prostitute?" — is the chapter's last line and its open wound. They are not wrong that Shechem treated Dinah as someone who could be taken and used without consequence. But their violence has also used deception, turned a covenant sign into a weapon, killed men who were technically innocent of Dinah's assault, enslaved women and children, and plundered an entire city. The question hangs.

Jacob's deathbed curse on Simeon and Levi (49:5–7) settles the narrator's assessment: "Cursed be their anger, for it is fierce, and their wrath, for it is cruel. I will divide them in Jacob and scatter them in Israel." The excessive violence is condemned. But the question "Should he treat our sister like a prostitute?" is never answered in the text, because it is the right question — it is simply not answered by massacre.

This chapter insists on sitting in moral complexity. The violation of Dinah is real and serious. Her brothers' outrage is legitimate. Her father's silence is a failure. The deception and violence are condemned by Jacob and ultimately by Jacob's own blessing on his sons. The innocents who suffer in the city — the uninvolved men, the women and children enslaved — are collateral casualties of a cycle of dishonor. The chapter does not present a clean hero or a clean solution. It presents a world in which real sins produce cascading consequences that entangle the innocent with the guilty. This is why the Bible needs a Redeemer.

From a redemptive-historical perspective: this chapter, set at Shechem, becomes the site where Israel later places the covenant renewal ceremony (Josh. 8:30–35; 24:1) and where Joseph's bones are finally buried (Josh. 24:32). God can redeem any location from its bloodiest history. Shechem also appears in John 4 — Jesus meets the Samaritan woman at Jacob's well, in the very city where this chapter's events unfolded, and offers living water. The geography of shame becomes the geography of grace.""",

  "chapter_overview": "Dinah goes out to meet the women of the land and is violated by Shechem, the Hivite prince, who then desires to marry her. Hamor negotiates with Jacob for intermarriage; Jacob's sons demand circumcision of all Shechem's men. The city agrees; on the third day Simeon and Levi massacre all the men and rescue Dinah. The other brothers plunder the city. Jacob protests that this endangers them; his sons ask 'Should he have treated our sister like a prostitute?' The question is left unanswered.",

  "original_language_notes": [
    {
      "term": "נְבָלָה (nebalah)",
      "language": "Hebrew",
      "verse": 7,
      "words_used": ["nebalah"],
      "meaning": "'Outrage / disgrace / a vile thing.' A strong legal-ethical term for a violation of the moral order that is both personal and communal. Used for Shechem's act here, for Amnon's rape of Tamar (2 Sam. 13:12), and for various sexual violations in Judges 20. The word carries the sense of something that unravels the social fabric — a 'thing not done in Israel' (lo yeaseh ken). It is not merely wrong; it is an assault on communal identity and moral coherence."
    },
    {
      "term": "עִנָּה (innah)",
      "language": "Hebrew",
      "verse": 2,
      "words_used": ["innah"],
      "meaning": "'Humiliated / afflicted / violated.' The Pi'el form of anah (to answer, to respond) becomes in the Pi'el a verb of oppression: to humble, to afflict, to violate. Used for Hagar's affliction (16:6), Israel's bondage in Egypt (Ex. 1:12), and sexual violation (Deut. 22:24, 29; 2 Sam. 13:12, 14). The choice of this word frames Shechem's act in the context of power over the powerless — the same word that describes systemic slavery is used for this assault."
    },
    {
      "term": "חַרְמוֹר (hecharish)",
      "language": "Hebrew",
      "verse": 5,
      "words_used": ["hecharish"],
      "meaning": "'He kept silent / held his peace.' From charash (to be silent, to be deaf, to plow — the plow cutting silently through soil). Jacob's silence while waiting for his sons is the single most commented-upon detail about Jacob's response. The word recurs in Nathan's parable to David (2 Sam. 12:4) and in Psalm 50:21 ('These things you have done, and I have kept silent'). The silence of those with authority to protect can itself be a form of complicity."
    },
    {
      "term": "כַּזּוֹנָה (kazonah)",
      "language": "Hebrew",
      "verse": 31,
      "words_used": ["kazonah"],
      "meaning": "'Like a prostitute / harlot.' From zanah (to prostitute, to commit fornication — the same root as 'harlotry' throughout the prophets, used both literally and metaphorically for Israel's spiritual unfaithfulness). Simeon and Levi's final question — 'Should he treat our sister like a prostitute?' — uses this word to frame Shechem's act as a reduction of Dinah to a commercial transaction: someone who can be taken without cost. The question is legitimate; the answer (massacre) is condemned."
    },
    {
      "term": "שְׁכֶם (Shechem)",
      "language": "Hebrew",
      "verse": 2,
      "words_used": ["Shechem"],
      "meaning": "The name means 'shoulder / neck / ridge' — referring to the geographical ridge where the city sits between Mount Ebal and Mount Gerizim in central Canaan. Shechem is also the person (the prince). The place Shechem becomes a site of repeated covenant significance: Abraham's first stop in Canaan (12:6), Jacob's purchase of land (33:19), the covenant renewal under Joshua (24:1), and the site of Jacob's well (John 4). A city marked by violence becomes a city marked by covenant and eventually by the grace Jesus offers."
    }
  ],

  "moral_lessons": [
    "Dinah's violation is presented as a serious outrage (nebalah) that demands a response — the chapter does not minimize sexual violence or treat it as inconsequential to the community.",
    "Jacob's silence in the face of his daughter's assault is implicitly criticized: those with authority and responsibility to protect cannot simply wait and calculate political risk when the vulnerable in their household have been harmed.",
    "Simeon and Levi's use of circumcision — the sacred covenant sign — as a cover for deception and massacre demonstrates that sacred things can be weaponized for violence, and that a just cause does not justify any method of responding to it.",
    "The chapter shows that cycles of dishonor and violence entangle the innocent: the men of Shechem who were not involved in Dinah's assault were killed; the women and children who were not involved were enslaved. Disproportionate vengeance destroys the innocent alongside the guilty.",
    "Jacob's deathbed curse on Simeon and Levi (49:5–7) provides the biblical verdict: the anger was legitimate, but 'cursed be their anger, for it is fierce' — the severity of the response was itself sinful."
  ],

  "application": "Genesis 34 is Scripture's refusal to let the community of faith avoid its hardest ethical terrain. The chapter holds together several truths simultaneously: sexual violence is a serious communal sin that demands a community response; protective silence by fathers and authorities is a failure; deceptive vengeance is not justice; and disproportionate violence harms the innocent. The chapter does not give us a clean hero or a clean method. It gives us a world that needs redemption — and it awaits the One who will bear nebalah on behalf of all who have been violated and all who have responded to violation wrongly. Jesus, who meets the Samaritan woman at Jacob's well in the very city where this chapter unfolds, brings living water to a geography saturated with shame.",

  "prayer": "Lord, we sit in the tension of Genesis 34 and do not flinch from it. We name the violation of Dinah as the serious sin it was. We confess that Jacob's silence represents every time those with authority have failed to protect the vulnerable in their care. We confess that Simeon and Levi represent every time we have weaponized sacred things in the service of vengeance rather than justice. Bring true justice, the justice that only You can bring — that heals without destroying the innocent, that restores without deception. In Jesus, who came to Shechem and offered the violated woman living water, You have shown us what real redemption looks like. May we seek justice with clean hands and mourning hearts. Amen.",

  "key_points": [
    "Dinah's assault is named with the full weight of the term nebalah — an outrage against the communal moral order, not merely a private wrong — establishing that sexual violence in the biblical framework is always also a community concern.",
    "Jacob's silence (hecharish) while waiting for his sons is the chapter's most debated detail: the one with authority to act chose to calculate rather than protect, a failure the narrative embeds without explicit commentary.",
    "Simeon and Levi's use of circumcision as a weapon for deception is particularly condemned because it weaponizes the covenant sign — they used God's mark for murder.",
    "Jacob's deathbed blessing in Genesis 49:5–7 provides the narrative's verdict: the anger was justified, but 'cursed be their anger, for it is fierce' — righteous outrage does not justify savage methods.",
    "The collateral victims of the massacre — uninvolved men killed, women and children enslaved — illustrate that disproportionate vengeance harms the innocent and destroys any claim to justice.",
    "The chapter ends with two unresolved questions (Jacob's and his sons'), teaching that some situations in a broken world resist clean moral resolution — this is why humanity needs divine redemption, not just human justice.",
    "Shechem's geography becomes redemptive history: the site of this chapter's violence becomes the site of covenant renewals (Josh. 24), Joseph's burial (Josh. 24:32), and Jesus's encounter with the Samaritan woman (John 4) — God reclaims geography from its darkest stories."
  ],

  "study_questions": [
    "Jacob's silence after learning of Dinah's assault has been read as wisdom (waiting for his sons), as fear, or as a failure of fatherly protection. What does the text suggest? What does Jacob's response to the massacre (only political concern, no mention of justice for Dinah) reveal about his priorities?",
    "Shechem violated Dinah but then genuinely loved her and wanted to marry her. The text presents both realities simultaneously. How does this moral complexity affect your reading of the situation — and what does it say about how the Bible handles real human sin?",
    "Simeon and Levi used circumcision — the covenant sign — as a tool of deception and massacre. What warnings does this carry about the misuse of religious or sacred symbols for violent ends?",
    "Jacob's only objection to the massacre is political ('you have made me stink to the inhabitants of the land'). What is missing from his response? What would a response that honored Dinah as a person look like?",
    "Jesus met the Samaritan woman at Jacob's well in Shechem (John 4). What does it mean that the Redeemer brought living water to this specific geography? How does that inform your understanding of divine redemption?"
  ],

  "tags": ["Genesis", "Dinah", "Shechem", "Simeon", "Levi", "Jacob", "sexual violence", "justice", "vengeance", "deception", "moral complexity", "redemption"],
  "sources": []
},

# ── GENESIS 35 ─────────────────────────────────────────────────────────────
{
  "chapter": 35,
  "title": "Genesis 35 — Return to Bethel: Purified Household, Renewed Covenant, and the Grief of New Beginnings",
  "summary": "God commands Jacob to return to Bethel and build an altar. Jacob commands his household to put away foreign gods and purify themselves; they surrender idols and earrings, which Jacob buries under an oak at Shechem. They travel to Bethel and Jacob builds the altar; God appears and reaffirms Jacob's new name Israel and renews the Abrahamic covenant promises. Deborah, Rebekah's nurse, dies at Bethel. The family moves south; Rachel goes into labor, bears Benjamin, and dies. Jacob erects a pillar at her tomb. Reuben sins with Bilhah. The twelve sons of Jacob are listed. Isaac dies at 180 years; Esau and Jacob bury him.",
  "content": """Genesis 35 is a chapter of purification, covenant renewal, birth, and death — the full human range compressed into a single chapter as Jacob returns to Bethel and then continues south to Canaan's heartland. It resolves the Shechem crisis (ch. 34), closes the chapter on Bethel vows made twenty years earlier (ch. 28), introduces the twelfth son of Jacob, and marks the death of both Rachel and Isaac.

The chapter opens with a divine command: "Arise, go up to Bethel and dwell there. Make an altar there to the God who appeared to you when you fled from your brother Esau" (v. 1). God is recalling Jacob to the vow he made at Bethel (28:20–22). Before the return, Jacob demands an act of household purification: "Put away the foreign gods that are among you and purify yourselves and change your garments" (v. 2). The foreign gods here include Rachel's teraphim from chapter 31 and apparently other items the household has accumulated — including earrings, which in the ancient Near East often served as amulets or as offerings to local deities. Jacob buries everything under the oak at Shechem. The return to Bethel requires the purging of what was brought from Haran and accumulated at Shechem.

The "terror of God" (v. 5) falls on the cities around them as they travel — no one pursues them despite the recent massacre at Shechem. God's protection is explicit and strange: the surrounding peoples are paralyzed. This is reminiscent of the Exodus language (Ex. 15:15–16: "terror and dread fell upon them"). Jacob's people travel in divine sanctuary.

At Bethel, God appears to Jacob again (the third major theophany of Jacob's life: Bethel at the ladder, Peniel at the ford, now Bethel again) and reaffirms the renaming. "Your name is Jacob; no longer shall your name be called Jacob, but Israel shall be your name" (v. 10). The reaffirmation is important: the Peniel renaming (32:28) could have been dismissed as a dream or a mysterious nighttime encounter. God's repetition at Bethel, in the daylight, in the land of the original promise, seals it. God then states the Abrahamic covenant in its fullest form for Jacob: "I am God Almighty (El Shaddai): be fruitful and multiply. A nation and a company of nations shall come from you, and kings shall come from your own body. The land that I gave to Abraham and Isaac I will give to you, and I will give the land to your offspring after you" (vv. 11–12). El Shaddai appears first to Abraham (17:1) in the context of covenant renewal and the promise of descendants. Its appearance here marks Jacob as fully in the Abrahamic line — the covenant has been formally handed to the third generation.

Jacob erects a stone pillar at the place (v. 14) — an echo of his original Bethel pillar (28:18). He pours oil on it and wine — the first mention of a libation in the Bible. He names the place Bethel, though it was already called that (28:19): the naming is an act of re-consecration, not discovery.

The deaths in this chapter are significant. Deborah, Rebekah's nurse (v. 8), dies at a place immediately named "Allon-bacuth" — Oak of Weeping. Deborah is mentioned only here by name in all of Genesis; she was presumably with Jacob's household either because Rebekah sent her or because she eventually migrated south with Rebekah. Her death draws tears from the entire household, a measure of her place among them. Rebekah's own death is never recorded in Genesis — the mother who shaped Jacob's destiny disappears from the narrative without a farewell. Her nurse weeps; her passing is unmarked. This is one of the narrative's quiet griefs.

The death of Rachel (vv. 16–20) is one of the most poignant passages in Genesis. In labor with her second son, Rachel is in such distress that the midwife tells her while she is dying: "Do not fear, for you have another son" (v. 17). Rachel has longed for sons throughout chapter 30; she died to give her second son life. With her last breath she names him Ben-oni: "son of my sorrow." Jacob immediately renames him Benjamin: "son of my right hand." Both names are true: he is the son of Rachel's dying sorrow and the son of Jacob's hope and strength. Jacob erects a pillar over her tomb — not the full patriarchal burial at Machpelah, but a monument on the road to Bethlehem. Rachel's tomb "on the way to Ephrath, that is, Bethlehem" (v. 19) becomes a landmark of mourning in Israel: Jeremiah will hear Rachel weeping for her children (Jer. 31:15), which Matthew applies to the slaughter of the innocents at Bethlehem (Matt. 2:18).

Reuben's sin with Bilhah (v. 22) is stated in a single verse and set aside — "And Israel heard of it." The act is an assertion of dominance over his father's household (sleeping with a father's concubine was equivalent to claiming the father's authority — cf. Absalom in 2 Sam. 16:20–22). Reuben's birthright will be forfeited for this act (49:4); his tribe will not lead. The single verse is a legal fact, not a dramatic scene — the Bible records it because the consequences for the tribes (49:3–4) require the explanation.

The listing of Jacob's twelve sons (vv. 22–26) — with their mothers — is a formal tribal register. This is the first time all twelve are listed together in one place. What is remarkable is the context: they are listed in the chapter that includes Rachel's death, Reuben's sin, and Isaac's death. The twelve who will become a nation are named in the middle of grief, failure, and loss. Israel is not born in triumph but in the full texture of human frailty.

Isaac's death at 180 years (vv. 27–29) is peaceful — "he breathed his last and died and was gathered to his people, old and full of days" (v. 29). The same phrase used for Abraham (25:8). Esau and Jacob bury him together — the same way they appeared together at Abraham's burial (25:9), and the last time in the narrative the two brothers are in the same place. The chapter thus closes the loop: Jacob and Esau, once divided by stolen blessing, stand together over their father's grave. Reconciliation at Peniel, reunion at the burial — God's work in human estrangement is patient and persistent.

Chapter 35 is the end of the Jacob narrative proper. What follows (chs. 36–50) is Joseph's story. Jacob will live on — struggling, grieving, misjudging — but the central narrative arc of his life is complete. He returned to Bethel. He fulfilled his vow. He buried his wife and his father. He was renamed twice by God. He is Israel.""",

  "chapter_overview": "God commands Jacob to return to Bethel. Jacob purges foreign gods from his household; they travel under divine protection. At Bethel, God reaffirms Jacob as 'Israel' and renews the Abrahamic covenant as El Shaddai. Deborah, Rebekah's nurse, dies at Allon-bacuth. The family moves south; Rachel dies in childbirth, naming her son Ben-oni before dying; Jacob renames him Benjamin. Reuben sins with Bilhah. The twelve sons of Jacob are formally listed. Jacob arrives at Mamre; Isaac dies at 180 years; Esau and Jacob bury him together.",

  "original_language_notes": [
    {
      "term": "אֵל שַׁדַּי (El Shaddai)",
      "language": "Hebrew",
      "verse": 11,
      "words_used": ["El", "Shaddai"],
      "meaning": "'God Almighty' — the divine name by which God revealed Himself to Abraham (17:1) and Isaac, now repeated to Jacob. The etymology of Shaddai is debated: possibly from shadad (to overpower, to be almighty), from shad (breast, nurturing), or from a Semitic root for mountain. El Shaddai appears most in Job (31 times) and the patriarchal narratives. It is the name of God as the all-sufficient, all-capable One who makes impossible promises to the elderly and barren possible."
    },
    {
      "term": "בֶּן-אוֹנִי / בִּנְיָמִין (Ben-Oni / Binyamin)",
      "language": "Hebrew",
      "verse": 18,
      "words_used": ["Ben-Oni", "Binyamin"],
      "meaning": "Ben-Oni: 'son of my sorrow/pain' (from ben, son + on/oni, sorrow, trouble, strength diminished by grief). Binyamin/Benjamin: 'son of the right hand' (from ben + yamin, right hand — the favored hand, the hand of power and blessing). The same child receives two names from two different perspectives: his dying mother's grief and his father's love and hope. Both names are true and constitute the child's complete identity. The right hand in Hebrew thought is the place of favor (Ps. 110:1; Matt. 25:33)."
    },
    {
      "term": "אַלּוֹן בָּכוּת (Allon-Bacuth)",
      "language": "Hebrew",
      "verse": 8,
      "words_used": ["Allon", "Bacuth"],
      "meaning": "'Oak of Weeping.' Allon (oak) + bacuth (weeping, from bakah, to weep). The death of Deborah, Rebekah's nurse, is marked by a place-name that encodes communal mourning. The oak (a large, long-lived tree used as a landmark) becomes a memorial of grief. Oaks appear throughout Genesis as significant markers: the oak at Shechem (12:6; 35:4), the oaks of Mamre (18:1). The naming of grief into landscape is a Hebrew practice of memory — the tears of one generation are embedded in geography for the next."
    },
    {
      "term": "מַצֵּבָה (matsevah)",
      "language": "Hebrew",
      "verse": 14,
      "words_used": ["matsevah"],
      "meaning": "'Pillar / standing stone.' From natsav (to stand, to set up). Jacob erects a matsevah at Bethel (28:18 and here) and at Rachel's tomb (v. 20). The standing stone was a common ancient Near Eastern memorial marker for divine encounters, covenant ratification, and burial. Jacob pours oil on it (as at the original Bethel) and adds wine — the first libation (nesek) in Genesis. The pillars Jacob erects are personal memorials that become permanent geography: Bethel and Rachel's tomb on the road to Bethlehem."
    },
    {
      "term": "חִתַּת אֱלֹהִים (chittat Elohim)",
      "language": "Hebrew",
      "verse": 5,
      "words_used": ["chittat", "Elohim"],
      "meaning": "'Terror of God' — from chatat (to be shattered, to be terrified; the noun form is chittah, terror) + Elohim. The phrase describes the paralyzing fear that fell on surrounding cities as Jacob's household traveled. The same vocabulary appears in Exodus 15:16 ('terror and dread fell upon them') describing the Canaanites' fear before the approaching Israelites. The chittat Elohim is not merely political intimidation but divine protection — God makes the surrounding nations unable to pursue or attack."
    }
  ],

  "moral_lessons": [
    "Jacob's command to 'put away foreign gods' before returning to Bethel demonstrates that covenant renewal always requires household purification — we cannot come to God carrying what we collected in our previous compromises.",
    "God's reaffirmation of the 'Israel' name at Bethel (after the first at Peniel) shows that God confirms His transforming work in the full light of day and in the context of covenant — He does not leave His renaming of us ambiguous.",
    "Rachel's dying naming of Benjamin (Ben-Oni / Benjamin) holds together grief and hope simultaneously: the same reality can be named from sorrow or from faith. Jacob's renaming is not a denial of Rachel's pain but a faith-affirmation of the same child.",
    "The burial of Jacob's father Isaac alongside Esau suggests that reconciled brothers can perform the ultimate act of filial piety together — the estrangement of their youth need not define the end of their story.",
    "Reuben's sin and its consequences (forfeiture of the birthright) teach that actions in private have public, generational consequences — the verse is brief; the tribe of Reuben will bear the weight of it in the tribal blessings (49:3–4)."
  ],

  "application": "Genesis 35 is the purification chapter — the chapter where what was carried from Haran and Shechem is finally buried under the oak. Every season of genuine return to God involves this kind of surrender: not just the teraphim, but the earrings, the amulets, the things we have been keeping 'just in case.' God calls Jacob back to Bethel — back to the original vow, the original encounter, the original altar. He calls us back to our first encounter with Him and asks us to bring nothing from the journey except ourselves, purified. And there He meets us again as El Shaddai — the all-sufficient One who still knows our name — and renews the covenant from the beginning.",

  "prayer": "El Shaddai — God Almighty — You called Jacob back to Bethel, and You call us back to the place of our first encounter with You. Show us what we are still carrying from our Shechemites and our Labans — the earrings, the teraphim, the things we have not surrendered. Give us the courage to bury them under the oak. Then meet us at Bethel, call us by our covenant name, and renew Your promise from the beginning. You are still the God of Abraham, of Isaac, and of Israel — the God of the limping, the grieving, the burying. Be sufficient for us today. In Jesus' name, Amen.",

  "key_points": [
    "Jacob's household purge of foreign gods and amulets before returning to Bethel establishes a pattern: genuine return to the place of God's covenant requires releasing what was accumulated in the intervening compromises.",
    "God's second formal renaming of Jacob as Israel (v. 10) — the first was at Peniel (32:28) — confirms the transformation in the full light of the covenant land, sealing what was started at the ford.",
    "El Shaddai (v. 11) — the name God used when establishing the Abrahamic covenant with Abraham (17:1) — now marks Jacob's full inheritance of the covenant: the same name, the same promises, now to the third generation.",
    "Rachel's double-naming of Benjamin (Ben-Oni in grief, Benjamin by Jacob's hope) shows that the same person can be named simultaneously by sorrow and by faith — both names are true, and Jacob chose to let the faith-name prevail.",
    "Rachel's tomb 'on the way to Bethlehem' (v. 19) becomes a landmark of prophetic grief: Jeremiah's Rachel weeping for her children (Jer. 31:15) echoes this site, pointing ultimately to the slaughter of the innocents (Matt. 2:18).",
    "Isaac's peaceful death and joint burial by Esau and Jacob closes the patriarchal narrative of the second generation: the brothers who were divided by stolen blessing stand together at their father's grave.",
    "The formal listing of all twelve sons (vv. 22–26) in a chapter saturated with grief, sin, and loss is the Bible's reminder that Israel as a nation is built not in triumph but in the full mixture of human faithfulness and failure."
  ],

  "study_questions": [
    "Jacob commanded his household to surrender foreign gods before returning to Bethel. What 'foreign gods' or spiritual compromises do you carry that need to be buried before you can return to the place of your original covenant with God?",
    "God confirmed Jacob's new name twice — at Peniel and now at Bethel. Why might God need to confirm a renaming? What does the repetition say about how transformation is received and internalized?",
    "Rachel named her son Ben-Oni (son of my sorrow); Jacob renamed him Benjamin (son of my right hand). Both names are valid. When have you experienced something that could be named by grief or by faith? How do you hold both?",
    "Reuben's sin is reported in a single verse with no immediate consequence, but it costs him his birthright decades later (49:3–4). What does this suggest about how private sins have quiet, slow, generational consequences?",
    "Esau and Jacob stand together at Isaac's grave (v. 29). What does it mean that two brothers who were divided by one of Scripture's most dramatic acts of deception ended their story burying their father together? What does it tell you about God's long work of reconciliation?"
  ],

  "tags": ["Genesis", "Jacob", "Israel", "Bethel", "Rachel", "Benjamin", "El Shaddai", "purification", "covenant renewal", "death", "burial", "twelve tribes", "Isaac"],
  "sources": []
}

] # end CHAPTERS list


def get_or_create_batch_id(conn):
    cur = conn.cursor()
    cur.execute("SELECT MAX(generation_batch_id) FROM commentary_entries")
    row = cur.fetchone()
    return (row[0] or 0) + 1


def entry_exists(conn, book_id, chapter):
    cur = conn.cursor()
    cur.execute("""
        SELECT id, content FROM commentary_entries
        WHERE collection_id=? AND book_id=? AND chapter=?
          AND language_code='en' AND reference_scope='chapter'
          AND deleted_at IS NULL
    """, (COLLECTION_ID, book_id, chapter))
    row = cur.fetchone()
    if row is None:
        return False, None
    # shallow check: content shorter than 500 chars
    content = row[1] or ""
    return True, len(content) >= 500


def insert_entry(conn, batch_id, data, chapter_uuid, now_iso):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO commentary_entries (
            uuid, collection_id, generation_batch_id, book_id, chapter,
            verse_start, verse_end, reference_scope,
            title, summary, content, application, prayer,
            key_points, study_questions,
            language_code, theological_perspective, status,
            is_ai_generated, ai_model_name, ai_model_provider,
            ai_prompt_version, ai_generation_batch_uuid, ai_confidence,
            word_count, sync_status, created_at, updated_at
        ) VALUES (?,?,?,?,?,NULL,NULL,'chapter',?,?,?,?,?,?,?,
                  'en','evangelical','draft',
                  1,'claude-sonnet-4-6','anthropic',
                  'believers-sword-commentary-v2',?,0.95,
                  ?,  'local', ?, ?)
    """, (
        chapter_uuid, COLLECTION_ID, batch_id, BOOK_ID, data["chapter"],
        data["title"], data["summary"], data["content"],
        data["application"], data["prayer"],
        json.dumps(data["key_points"]),
        json.dumps(data["study_questions"]),
        BATCH_UUID,
        len(data["content"].split()),
        now_iso, now_iso,
    ))
    conn.commit()


def save_json(data, chapter_uuid, now_iso):
    os.makedirs(GENERATED_DIR, exist_ok=True)
    payload = {
        "uuid": chapter_uuid,
        "collection_name": COLLECTION_NAME,
        "author_type": "ai",
        "language_code": LANGUAGE_CODE,
        "theological_perspective": "evangelical",
        "status": "draft",
        "book_id": BOOK_ID,
        "book": BOOK,
        "chapter": data["chapter"],
        "title": data["title"],
        "summary": data["summary"],
        "content": data["content"],
        "chapter_overview": data["chapter_overview"],
        "original_language_notes": data["original_language_notes"],
        "moral_lessons": data["moral_lessons"],
        "application": data["application"],
        "prayer": data["prayer"],
        "key_points": data["key_points"],
        "study_questions": data["study_questions"],
        "tags": data["tags"],
        "sources": data["sources"],
        "created_at": now_iso,
        "updated_at": now_iso,
    }
    # verify no forbidden keys
    for k in FORBIDDEN_KEYS:
        assert k not in payload, f"Forbidden key found: {k}"
    filename = os.path.join(GENERATED_DIR, f"{data['chapter']:02d}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    # verify parses back
    with open(filename, encoding="utf-8") as f:
        parsed = json.load(f)
    for k in FORBIDDEN_KEYS:
        assert k not in parsed, f"Forbidden key in parsed: {k}"
    return filename


def update_progress(next_chapter, last_chapter):
    payload = {
        "next_book_id": BOOK_ID,
        "next_book": BOOK,
        "next_chapter": next_chapter,
        "last_completed_book_id": BOOK_ID,
        "last_completed_book": BOOK,
        "last_completed_chapter": last_chapter,
        "completed": False,
        "updated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    with open(PROGRESS_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO commentary_generation_progress
            (id, next_book_id, next_book, next_chapter,
             last_completed_book_id, last_completed_book, last_completed_chapter,
             completed, updated_at)
        VALUES (1,?,?,?,?,?,?,0,?)
    """, (
        BOOK_ID, BOOK, next_chapter,
        BOOK_ID, BOOK, last_chapter,
        payload["updated_at"]
    ))
    conn.commit()
    conn.close()


def append_log(batch_start, batch_end, generated, skipped, inserted, files):
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "generation_batch_id": BATCH_UUID,
        "start_reference": f"{BOOK} {batch_start}",
        "end_reference": f"{BOOK} {batch_end}",
        "chapters_generated": generated,
        "chapters_skipped": skipped,
        "db_rows_inserted": inserted,
        "files_written": files,
        "errors": [],
    }
    with open(LOG_JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def main():
    conn = sqlite3.connect(DB_PATH)
    batch_id = get_or_create_batch_id(conn)

    chapters_generated = 0
    chapters_skipped = 0
    db_rows_inserted = 0
    files_written = []
    batch_start = CHAPTERS[0]["chapter"]
    batch_end = CHAPTERS[-1]["chapter"]
    last_completed = None

    for ch_data in CHAPTERS:
        ch = ch_data["chapter"]
        now_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        exists, is_deep = entry_exists(conn, BOOK_ID, ch)
        if exists and is_deep:
            print(f"  SKIP {BOOK} {ch} — already exists with deep content")
            chapters_skipped += 1
            last_completed = ch
            continue

        chapter_uuid = str(uuid.uuid4())
        # Insert DB
        insert_entry(conn, batch_id, ch_data, chapter_uuid, now_iso)
        db_rows_inserted += 1
        # Save JSON
        fpath = save_json(ch_data, chapter_uuid, now_iso)
        files_written.append(fpath)
        chapters_generated += 1
        last_completed = ch
        print(f"  GENERATED {BOOK} {ch} — {ch_data['title'][:60]}...")

    conn.close()

    if last_completed:
        next_ch = last_completed + 1
        update_progress(next_ch, last_completed)

        # update progress table check
        conn2 = sqlite3.connect(DB_PATH)
        cur = conn2.cursor()
        cur.execute("SELECT next_chapter FROM commentary_generation_progress WHERE id=1")
        row = cur.fetchone()
        conn2.close()
        if row:
            print(f"\nProgress table next_chapter = {row[0]}")

    append_log(batch_start, batch_end, chapters_generated, chapters_skipped, db_rows_inserted, files_written)

    print(f"\n=== SUMMARY ===")
    print(f"Generated: Genesis {batch_start}–{batch_end}")
    print(f"Chapters generated: {chapters_generated}")
    print(f"Chapters skipped: {chapters_skipped}")
    print(f"DB rows inserted: {db_rows_inserted}")
    print(f"Files written: {len(files_written)}")
    for f in files_written:
        print(f"  {f}")
    if last_completed:
        print(f"Next starting reference: {BOOK} {last_completed + 1}")


if __name__ == "__main__":
    main()
