#!/usr/bin/env python3
"""Generate Exodus chapters 6-10 commentaries."""

import sqlite3
import json
import uuid
import os
from datetime import datetime, timezone

WORKSPACE = "/mnt/d/Projects/Personal/Believers-Sword/Modules Turso/Commentaries/Believers Sword"
DB_PATH = os.path.join(WORKSPACE, "believers_sword_commentaries.db")
GENERATED_DIR = os.path.join(WORKSPACE, "generated", "02-exodus")
PROGRESS_JSON = os.path.join(WORKSPACE, "commentary_generation_progress.json")
LOG_JSONL = os.path.join(WORKSPACE, "commentary_generation_log.jsonl")

os.makedirs(GENERATED_DIR, exist_ok=True)

COLLECTION_ID = 1
COLLECTION_NAME = "Believers Sword Commentaries"
BOOK_ID = 2
BOOK = "Exodus"

FORBIDDEN_KEYS = {"is_ai_generated", "model_name", "prompt_version"}

REQUIRED_KEYS = [
    "uuid", "collection_name", "author_type", "language_code",
    "theological_perspective", "status", "book_id", "book", "chapter",
    "title", "summary", "content", "chapter_overview", "original_language_notes",
    "moral_lessons", "application", "prayer", "key_points", "study_questions",
    "tags", "sources", "created_at", "updated_at",
]

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

COMMENTARIES = [
    # ─────────────────────────────────────────────────────────────────────────
    # EXODUS 6
    # ─────────────────────────────────────────────────────────────────────────
    {
        "chapter": 6,
        "title": "Exodus 6 — The Covenant Name Unveiled: God's Four Promises and the Genealogy of Redemption",
        "summary": (
            "After Moses' lament, God responds not with explanation but with covenant. "
            "He reveals the full weight of His name YHWH, four binding promises of deliverance, "
            "and the genealogy connecting Moses and Aaron to the tribe of Levi. The chapter is a "
            "theological anchor: when circumstances seem to contradict God's word, His response is "
            "deeper revelation of who He is and a re-statement of unbreakable covenant promises."
        ),
        "content": (
            "## What Exodus 6 Is About\n"
            "Exodus 6 is God's response to Moses' lament at the end of chapter 5. Moses had brought "
            "Israel's worsened suffering to God and asked 'Why have You brought trouble on this people? "
            "Is this why You sent me?' God's answer is remarkable — He does not explain the delay or "
            "apologize for the difficulty. Instead, He deepens the revelation of Himself and restates "
            "His covenant with an intensity not heard since He first spoke to Moses at the burning bush.\n\n"
            "God introduces Himself with these words: 'I am the LORD. I appeared to Abraham, to Isaac, "
            "and to Jacob as God Almighty (El Shaddai), but by my name the LORD (YHWH) I did not make "
            "myself fully known to them' (vv.2–3). This is not a contradiction of Genesis — the name "
            "YHWH appears there — but a statement about depth of revelation. The patriarchs knew the "
            "name; they did not yet know the full meaning of that name in action. Exodus will show what "
            "YHWH means: the God who intervenes, who keeps covenant, who redeems, who judges, who "
            "makes Himself known through history.\n\n"
            "## The Four 'I Will' Promises (vv.6–8)\n"
            "God gives four promises to Israel, each introduced by 'I will':\n"
            "1. 'I will bring you out from under the yoke of the Egyptians' — liberation\n"
            "2. 'I will free you from being slaves to them' — rescue from bondage\n"
            "3. 'I will redeem you with an outstretched arm and with mighty acts of judgment' — redemption "
            "(using the Hebrew גָּאַל, gāʾal — the language of the kinsman-redeemer)\n"
            "4. 'I will take you as my own people, and I will be your God' — covenant adoption\n\n"
            "A fifth promise follows: 'I will bring you to the land I swore with uplifted hand to give "
            "to Abraham, to Isaac, and to Jacob. I will give it to you as a possession. I am the LORD.' "
            "The repetition of 'I am the LORD' bookends this entire speech (vv.2, 6, 7, 8, 29) — seven "
            "occurrences in the chapter — driving home that the substance of every promise is YHWH Himself.\n\n"
            "## Israel's Discouragement (vv.9, 12)\n"
            "When Moses relays these promises to Israel, they do not receive them. The text says they 'did "
            "not listen to him because of their discouragement and harsh labor' (v.9). The Hebrew phrase "
            "translated 'discouragement' is קֹצֶר רוּחַ (qōtser rûaḥ) — literally 'shortness of spirit' "
            "or 'crushed spirit.' They cannot receive a long-horizon promise when their spirit has been "
            "compressed to the present agony. This is a profound pastoral note: prolonged suffering can "
            "make people unable to hear even true words of hope.\n\n"
            "## The Genealogy (vv.14–27)\n"
            "Before the plagues begin, the narrative pauses to establish Moses and Aaron's lineage through "
            "Levi's son Kohath. This is not digression — it is theological grounding. The deliverers are "
            "identified precisely, their credentials established, their names set in the record of covenant "
            "history. Aaron and Moses are verified as belonging to the people they are sent to deliver.\n\n"
            "## Theological Themes\n"
            "- **The Depth of the Name YHWH**: The patriarchs knew God as El Shaddai ('God Almighty'), "
            "the provider and sustainer. Exodus reveals YHWH as the redeemer and covenant-keeper who acts "
            "in history. Each divine name reveals a dimension of God's character; no single name is exhaustive.\n"
            "- **Covenant as God's Framework for Action**: God acts within the framework of His prior "
            "commitments. The redemption from Egypt is not a new idea — it fulfills what God swore to "
            "Abraham (Genesis 15). God's freedom is never arbitrary; it is faithful.\n"
            "- **The Kinsman-Redeemer Language**: 'I will redeem you' (גָּאַל, gāʾal) — used in Leviticus "
            "and Ruth for a close relative who buys back a family member from slavery or debt. God is "
            "positioning Himself as Israel's nearest kin, their gōʾēl. This language is picked up in "
            "Isaiah 40–55 and ultimately in Christ, who is 'the firstborn among many brothers' (Romans 8:29).\n"
            "- **Hardened Hearts and Unheard Words**: Israel's inability to hear God's promises due to "
            "crushed spirit anticipates the problem of the hardened heart — a theme that runs through "
            "Exodus, the Psalms, and the prophets, and which Jesus addresses in His parable of the sower.\n\n"
            "## How This Chapter Points to Christ\n"
            "The four promises of Exodus 6 find their ultimate fulfillment in Christ. He brings us out of "
            "slavery to sin (Galatians 5:1), frees us from condemnation (Romans 8:1), redeems us with His "
            "own blood (1 Peter 1:18–19), and makes us God's own people (1 Peter 2:9–10). The kinsman-"
            "redeemer imagery is fulfilled perfectly: Jesus becomes one of us (takes on flesh) precisely "
            "so that He has the right to redeem us. 'I am the LORD' — the divine self-disclosure of Exodus "
            "— finds its New Testament counterpart in Jesus' 'I AM' statements in the Gospel of John.\n\n"
            "## Moral and Spiritual Lessons\n"
            "- When we bring lament to God, He responds with deeper revelation of Himself and His covenant, "
            "not with explanations that satisfy our timeline.\n"
            "- The 'shortness of spirit' caused by prolonged suffering is not weakness — it is a documented "
            "human reality that God recognizes and addresses with patience.\n"
            "- God's promises are rooted in covenant, not in our current circumstances or feelings.\n"
            "- The proper response to suffering is not silence or despair, but bringing our complaints to "
            "God and receiving again, by faith, the promises He has already given.\n\n"
            "## Practical Application\n"
            "When your circumstances seem to contradict God's promises, return to the covenant He has made. "
            "Read Exodus 6:6–8 alongside its New Testament fulfillments and ask: Is my spirit 'shortened' "
            "by present difficulty so that I cannot hear long-horizon truth? Bring your qōtser rûaḥ "
            "('crushed spirit') to God honestly. Let His 'I am the LORD' be the anchor of your faith "
            "when the storm makes His promises seem distant.\n\n"
            "## Believers Sword Reflection\n"
            "Exodus 6 teaches that God does not move faster just because we are suffering harder. He moves "
            "within the logic of covenant and revelation — building a story whose ending will vindicate every "
            "promise. 'I am the LORD' is not a title but a testimony: everything I said, I will do."
        ),
        "chapter_overview": (
            "God responds to Moses' lament by revealing the full weight of His name YHWH, giving four "
            "covenant promises of redemption to Israel, and establishing Moses and Aaron's Levitical "
            "genealogy. Israel cannot receive the promises because of their crushed spirit. God "
            "recommissions Moses despite his continued hesitation."
        ),
        "original_language_notes": [
            {
                "term": "YHWH (יְהוָה)",
                "language": "Hebrew",
                "verse": "Exodus 6:2–3",
                "words_used": "אֲנִי יְהוָה (ʾănî YHWH) — 'I am the LORD/YHWH'",
                "meaning": (
                    "The divine name YHWH (often rendered LORD in English translations) derives from "
                    "the verb הָיָה (hāyāh, 'to be'). God tells Moses He appeared to the patriarchs as "
                    "El Shaddai but not by this name in full force — meaning the full experiential weight "
                    "of YHWH as covenant-keeper and redeemer was not yet displayed. Exodus will make the "
                    "name's meaning visible in action."
                )
            },
            {
                "term": "gāʾal (גָּאַל)",
                "language": "Hebrew",
                "verse": "Exodus 6:6",
                "words_used": "וְגָאַלְתִּי אֶתְכֶם (wĕgāʾaltî ʾetkhem) — 'I will redeem you'",
                "meaning": (
                    "גָּאַל (gāʾal) is the legal term for a kinsman-redeemer — a close relative with "
                    "both the right and obligation to buy back a family member from slavery or debt. "
                    "God uses this word deliberately: He is positioning Himself as Israel's nearest kin "
                    "with the authority and commitment to purchase their freedom. Ruth 4 and Isaiah 44 "
                    "develop this imagery, which is ultimately fulfilled in Christ."
                )
            },
            {
                "term": "qōtser rûaḥ (קֹצֶר רוּחַ)",
                "language": "Hebrew",
                "verse": "Exodus 6:9",
                "words_used": "מִקֹּצֶר רוּחַ (miqqōtser rûaḥ) — 'because of shortness of spirit/crushed spirit'",
                "meaning": (
                    "Literally 'shortness/constriction of breath/spirit.' The word קֹצֶר (qōtser) "
                    "means 'shortness' or 'impatience.' Together with רוּחַ (rûaḥ, 'spirit/breath'), it "
                    "describes a spirit so compressed by suffering that it cannot extend itself to "
                    "receive long-horizon hope. This is one of the most psychologically accurate "
                    "descriptions of trauma's effect on faith in the entire Old Testament."
                )
            },
            {
                "term": "El Shaddai (אֵל שַׁדַּי)",
                "language": "Hebrew",
                "verse": "Exodus 6:3",
                "words_used": "בְּאֵל שַׁדַּי (bĕʾēl šadday) — 'as God Almighty'",
                "meaning": (
                    "El Shaddai is the name by which God was primarily known to the patriarchs "
                    "(Genesis 17:1; 28:3; 35:11). Its exact derivation is debated — possibly from "
                    "שַׁדַּי related to 'mountain' (strength/majesty) or 'breast' (nourishment). "
                    "Either way, it emphasizes God as the all-sufficient sustainer of the covenant "
                    "family. Exodus reveals a new dimension of the same God: YHWH the redeemer-in-action."
                )
            }
        ],
        "moral_lessons": [
            "God responds to lament with deeper covenant revelation, not quick-fix explanations.",
            "A crushed spirit (qōtser rûaḥ) makes receiving God's promises difficult — this is recognized and met with patience, not condemnation.",
            "God's action is always grounded in prior covenant commitment, not arbitrary will.",
            "God's 'I will' is more stable than our circumstances; faith trusts what God has said over what circumstances show.",
            "The right response to spiritual discouragement is to return to God's stated promises and His covenant character."
        ],
        "application": (
            "Identify an area where prolonged difficulty has 'shortened your spirit' so that you find "
            "God's promises hard to receive. Write out the four 'I will' promises of Exodus 6:6–8 and "
            "their New Testament fulfillments. Pray them back to God honestly, acknowledging both the "
            "difficulty and His covenant faithfulness. Let 'I am the LORD' be your anchor this week."
        ),
        "prayer": (
            "LORD, my spirit is often shortened by the weight of what I carry. Like Israel, I sometimes "
            "cannot hear Your promises because the present pain is too loud. Speak again to me — not "
            "to explain the delay, but to reveal Yourself more deeply. You are my gōʾēl, my "
            "kinsman-redeemer. What You have sworn, You will do. I am the LORD — let that be enough "
            "for me today. Amen."
        ),
        "key_points": [
            "God responds to Moses' lament with deeper revelation of His name YHWH and a re-statement of covenant.",
            "The patriarchs knew God as El Shaddai; Exodus reveals what YHWH means in redemptive action.",
            "God gives four binding 'I will' promises: liberation, freedom, redemption (gāʾal), and covenant adoption.",
            "Israel cannot receive the promises due to 'crushed spirit' (qōtser rûaḥ) caused by harsh labor.",
            "The kinsman-redeemer language (gāʾal) places God in the role of nearest kin with the right and duty to redeem.",
            "The genealogy establishes Moses and Aaron as verified Levitical deliverers within covenant history."
        ],
        "study_questions": [
            "God says He appeared to the patriarchs as El Shaddai but not by His name YHWH in full force. What is the difference between knowing a name and knowing its full meaning? How does Exodus answer this?",
            "The four 'I will' promises in verses 6–8 use different verbs. What is the significance of the word gāʾal ('redeem') and its kinsman-redeemer background?",
            "Israel could not receive God's promises because of their crushed spirit (qōtser rûaḥ). Have you experienced a season when suffering made God's words hard to receive? What helped?",
            "Why does God repeat 'I am the LORD' seven times in this chapter? What is the rhetorical and theological effect of that repetition?",
            "How do the four 'I will' promises of Exodus 6 find fulfillment in Jesus Christ according to the New Testament?"
        ],
        "tags": ["exodus", "covenant", "yhwh", "redemption", "kinsman-redeemer", "el-shaddai", "promises", "genealogy", "moses", "crushed-spirit"],
        "sources": []
    },
    # ─────────────────────────────────────────────────────────────────────────
    # EXODUS 7
    # ─────────────────────────────────────────────────────────────────────────
    {
        "chapter": 7,
        "title": "Exodus 7 — Moses Like God, Aaron Like a Prophet: The Staff, the Serpent, and the First Plague",
        "summary": (
            "Exodus 7 begins the plague cycle. God commissions Moses as 'like God to Pharaoh' and Aaron "
            "as his prophet. Aaron's staff swallows the magicians' serpents — a sign of divine supremacy. "
            "Then the first plague strikes: the Nile and all Egyptian waters turn to blood. Pharaoh's "
            "heart is hardened. The chapter introduces the theological structure of the plagues: they are "
            "God's systematic demolition of Egypt's gods and a revelation of YHWH's identity."
        ),
        "content": (
            "## What Exodus 7 Is About\n"
            "Exodus 7 is the beginning of the plague cycle — the most sustained series of divine "
            "judgments in the Old Testament. Before the plagues begin, God gives Moses and Aaron "
            "their final commissioning and explains the theological purpose of what is about to happen.\n\n"
            "God tells Moses: 'See, I have made you like God to Pharaoh, and your brother Aaron will "
            "be your prophet' (v.1). This echoes the language of Exodus 4:16, where God said Aaron "
            "would be Moses' mouth and Moses would be 'like God to him.' Now the frame expands: Moses "
            "is God's representative not just to Israel but to the ruler of the most powerful empire on "
            "earth. Aaron speaks for Moses as Moses speaks for God.\n\n"
            "## The Sign of the Serpent (vv.8–13)\n"
            "When Pharaoh demands a miracle, Aaron throws down his staff and it becomes a snake. "
            "Pharaoh's magicians replicate the feat — but Aaron's serpent swallows theirs. This is not "
            "merely a contest of magic tricks. The Hebrew word here is תַּנִּין (tannîn) — a great "
            "sea-monster or dragon, associated in the ancient Near East with chaos and the enemies of "
            "divine order. Egyptian iconography placed the serpent at the center of royal and divine "
            "symbolism (the uraeus cobra on Pharaoh's crown represented divine power and protection). "
            "Aaron's serpent swallowing the Egyptian serpents is a declaration: YHWH's power consumes "
            "the power of Egypt's gods.\n\n"
            "## The First Plague: Water to Blood (vv.14–24)\n"
            "God commands Moses to meet Pharaoh at the Nile — the economic, religious, and physical "
            "lifeblood of Egypt. Moses strikes the water with Aaron's staff and the Nile turns to blood. "
            "All the water in Egypt — rivers, canals, ponds, reservoirs, even vessels of wood and stone "
            "— becomes blood. Fish die. The Nile stinks. No one can drink.\n\n"
            "The Nile was not merely a river to Egyptians — it was Hapy, the fertility god, source of "
            "life and abundance. Turning it to blood is a direct attack on one of Egypt's most revered "
            "deities. The plague begins the systematic demolition of Egyptian religion. The magicians "
            "replicate the plague (presumably with water from somewhere) but cannot reverse it. Their "
            "'success' only deepens the devastation. Pharaoh's heart remains hard.\n\n"
            "## Theological Themes\n"
            "- **The Plagues as Anti-Idolatry**: Each plague targets a specific deity or domain of "
            "Egyptian religion. The Nile/blood targets Hapy (the Nile god). The plagues are a theological "
            "argument conducted in nature and history, not just humanitarian intervention.\n"
            "- **Hardening of Pharaoh's Heart**: Verses 13 and 22 report that Pharaoh's heart 'was "
            "hardened' (וַיֶּחֱזַק, wayyeḥĕzaq). Earlier in chapters 4 and 7, God says He will harden "
            "Pharaoh's heart. Later texts say Pharaoh hardened his own heart. Theologians have long "
            "noted the interplay: Pharaoh's self-hardening (moral responsibility) and God's judicial "
            "hardening (sovereign judgment) are not mutually exclusive. God does not impose an alien "
            "will on Pharaoh — He confirms and intensifies the direction Pharaoh has already chosen.\n"
            "- **Moses 'Like God'**: The phrase positions the entire contest between Moses and Pharaoh "
            "as a confrontation between YHWH and Pharaoh-as-deity. Egypt's system depends on Pharaoh "
            "being divine; God places His servant as 'god' over against Pharaoh to unmask the fraud.\n"
            "- **The Role of the Prophet**: Aaron's role as Moses' prophet defines the biblical pattern "
            "of prophecy: the prophet does not speak his own words but relays and enacts the words of "
            "the one who sends him.\n\n"
            "## How This Chapter Points to Christ\n"
            "The contest between Moses and Pharaoh prefigures Christ's confrontation with 'the ruler of "
            "this world' (John 12:31; 14:30; 16:11). As Moses was 'like God to Pharaoh,' Jesus is "
            "the fullness of God in flesh (Colossians 2:9), confronting and defeating the powers of "
            "darkness. The swallowing of the serpents by Aaron's staff anticipates the cross, where "
            "Christ 'disarmed the powers and authorities' (Colossians 2:15) and ultimately destroys "
            "the ancient serpent (Revelation 20:10). The turning of water to blood — the lifeblood "
            "of Egypt's false god — is reversed in the upper room, where Jesus takes the cup of "
            "wine and says: 'This is my blood of the covenant' (Matthew 26:28). What was death "
            "in Egypt becomes life in Christ.\n\n"
            "## Moral and Spiritual Lessons\n"
            "- God's judgment on false systems of power begins by exposing and defeating them at the "
            "point of their greatest strength, not their weakness.\n"
            "- Hardness of heart is both a human moral choice and, when persisted in, a divine "
            "judicial consequence — a solemn warning.\n"
            "- God's representatives are sent with His authority; the word they carry is not their own.\n"
            "- The inability of Pharaoh's magicians to reverse the plague reveals the difference "
            "between counterfeiting and genuine divine power.\n\n"
            "## Practical Application\n"
            "Examine areas where you may be hardening your heart against what God is saying. Every "
            "time we hear God's word and harden against it, we move further toward a condition where "
            "the softening becomes more difficult. Ask: What 'Nile' — what source of provision or "
            "identity — do I trust more than God? The plagues attack idolatry at the point of "
            "greatest attachment. God may do the same in your life.\n\n"
            "## Believers Sword Reflection\n"
            "Exodus 7 shows that God does not merely overpower; He exposes. The plagues do not just "
            "defeat Egypt — they unmask the emptiness of every Egyptian claim to divine power. "
            "Aaron's serpent did not fight the Egyptian serpents; it consumed them. YHWH's answer "
            "to the powers of this world is not just superior force but total sufficiency."
        ),
        "chapter_overview": (
            "God commissions Moses as 'like God to Pharaoh' and Aaron as his prophet, then initiates "
            "the plague cycle. Aaron's staff-serpent swallows the Egyptian magicians' serpents. The "
            "first plague turns all Egyptian water to blood, targeting the Nile god Hapy. Pharaoh's "
            "heart is hardened and he refuses to let Israel go."
        ),
        "original_language_notes": [
            {
                "term": "tannîn (תַּנִּין)",
                "language": "Hebrew",
                "verse": "Exodus 7:9–12",
                "words_used": "לְתַנִּין (lĕtannîn) — 'into a serpent/dragon/sea-monster'",
                "meaning": (
                    "תַּנִּין (tannîn) is not the ordinary word for snake (נָחָשׁ, nāḥāš, used in "
                    "Genesis 3). It refers to a great sea-creature or dragon associated with chaos and "
                    "cosmic opposition to divine order (cf. Psalm 74:13; Isaiah 27:1; Ezekiel 29:3). "
                    "In Egyptian symbolism, the serpent was central to royal and divine iconography. "
                    "Aaron's tannîn consuming the Egyptians' is a statement of cosmic supremacy, not "
                    "a simple magic contest."
                )
            },
            {
                "term": "wayyeḥĕzaq (וַיֶּחֱזַק)",
                "language": "Hebrew",
                "verse": "Exodus 7:13, 22",
                "words_used": "וַיֶּחֱזַק לֵב פַּרְעֹה (wayyeḥĕzaq lēb parʿōh) — 'and Pharaoh's heart was hardened/strengthened'",
                "meaning": (
                    "חָזַק (ḥāzaq) means 'to be strong, firm, hard.' The verb form here is Qal imperfect "
                    "with waw-consecutive — describing repeated or ongoing state. Exodus uses three "
                    "different verbs for hardening: ḥāzaq ('to be strong/hard'), כָּבֵד (kābēd, 'to be "
                    "heavy'), and קָשָׁה (qāšāh, 'to be severe/hard'). Together they convey a heart "
                    "that grows progressively resistant to divine appeal — both by Pharaoh's own choice "
                    "and by divine judicial confirmation of that choice."
                )
            },
            {
                "term": "nĕhār (נָהָר) / ye'ōr (יְאֹר)",
                "language": "Hebrew",
                "verse": "Exodus 7:17–21",
                "words_used": "הַיְאֹר (hayyĕʾōr) — 'the Nile river'",
                "meaning": (
                    "יְאֹר (yĕʾōr) is the specific Hebrew word for the Nile, borrowed from Egyptian. "
                    "The Nile was the center of Egyptian civilization, its annual flood the source of "
                    "agricultural fertility, and it was personified as Hapy, the god of the Nile flood. "
                    "Striking the yĕʾōr first is a deliberate theological choice: God attacks Egypt's "
                    "primary source of life and divine provision before moving to lesser targets."
                )
            },
            {
                "term": "nĕbālāh (נְבָלָה)",
                "language": "Hebrew",
                "verse": "Exodus 7:18, 21",
                "words_used": "וּבָאַשׁ הַיְאֹר (ûbāʾaš hayyĕʾōr) — 'and the Nile will stink/become foul'",
                "meaning": (
                    "בָּאַשׁ (bāʾaš) means 'to stink, to become foul.' The death of the fish and "
                    "the corruption of the Nile's water is described with sensory vividness. The "
                    "sacred river of Egypt — associated with divine life and fertility — becomes a "
                    "source of stench and death. The reversal is total: what was life-giving is now "
                    "life-destroying."
                )
            }
        ],
        "moral_lessons": [
            "God confronts false power at its strongest point, not its weakest — the Nile, Egypt's greatest god, falls first.",
            "Heart hardening is both a human moral choice and a divine judicial confirmation; persistence in sin leads to deepened blindness.",
            "Those who speak for God carry His authority, not their own — the prophet's role is faithful relay, not personal invention.",
            "The enemy's ability to counterfeit divine signs does not mean they have divine power; only God can reverse what He sends.",
            "What we treat as our greatest source of life and identity is often exactly where God tests our deepest allegiances."
        ],
        "application": (
            "Ask honestly: What is my 'Nile' — the source of security, identity, or provision I trust "
            "more than God? The first plague attacks what Egypt worshipped most. God often works the "
            "same way in our hearts. Also examine: Is there an area where repeated exposure to God's "
            "word has left you calloused rather than softened? Hardening is gradual; softening "
            "requires active response to each encounter with God's truth."
        ),
        "prayer": (
            "LORD, You are the God who exposes and defeats false powers. Show me where I have trusted "
            "the 'Nile' of my own provision more than You. Soften my heart where it has grown hard to "
            "Your word. Let me not be like Pharaoh, who turned away every time You spoke. Make me "
            "quick to hear and quick to respond when You call. Amen."
        ),
        "key_points": [
            "God commissions Moses as 'like God to Pharaoh' — positioning the contest as YHWH vs. Pharaoh-as-deity.",
            "Aaron's staff becomes a tannîn (dragon/sea-monster), not merely a snake — a cosmic-level sign of supremacy.",
            "The Egyptian magicians replicate the sign but cannot reverse it — counterfeiting power vs. true divine authority.",
            "The first plague turns the Nile and all Egyptian water to blood — targeting Hapy, Egypt's Nile god.",
            "Pharaoh's heart hardens (wayyeḥĕzaq) — the beginning of a pattern of judicial hardening.",
            "The plagues are systematic demolition of Egyptian religion, not just humanitarian liberation."
        ],
        "study_questions": [
            "Why does God say He has made Moses 'like God to Pharaoh'? What does this reveal about the nature of the confrontation?",
            "What is the difference between נָחָשׁ (nāḥāš, ordinary snake) and תַּנִּין (tannîn, sea-dragon)? Why does the choice of word matter for the sign Aaron performs?",
            "How do you understand the relationship between Pharaoh hardening his own heart and God hardening Pharaoh's heart? Are these in tension?",
            "The Nile was Egypt's most sacred river and was worshipped as a deity. What does it tell us about God's judgment strategy that He strikes the Nile first?",
            "What 'Nile' in your own life — what source of provision, identity, or security — might need to be submitted to God's authority?"
        ],
        "tags": ["exodus", "plagues", "first-plague", "nile", "blood", "pharaoh", "hardening", "moses", "aaron", "serpent", "tannin", "idolatry"],
        "sources": []
    },
    # ─────────────────────────────────────────────────────────────────────────
    # EXODUS 8
    # ─────────────────────────────────────────────────────────────────────────
    {
        "chapter": 8,
        "title": "Exodus 8 — Frogs, Gnats, and Flies: The Plagues Escalate and the Magicians Confess",
        "summary": (
            "Exodus 8 contains three plagues: frogs (second), gnats (third), and flies (fourth). "
            "The plagues escalate in their impact and theological significance. The magicians can "
            "replicate the frogs but cannot reverse them; they cannot replicate gnats at all and "
            "confess 'This is the finger of God.' The fourth plague — flies — introduces a new "
            "element: a distinction between Goshen (where Israel lives) and the rest of Egypt. "
            "Pharaoh negotiates twice, conceding and retreating each time."
        ),
        "content": (
            "## What Exodus 8 Is About\n"
            "Exodus 8 accelerates the plague narrative with three more devastating interventions. "
            "Each plague builds on the last in intensity, geographic reach, and theological clarity. "
            "Together they advance the central argument of Exodus: that YHWH is God and there is "
            "no other.\n\n"
            "## The Second Plague: Frogs (vv.1–15)\n"
            "God sends frogs from the Nile in massive numbers — they invade Pharaoh's palace, "
            "his bedroom, his bed, the houses of his officials, the ovens and kneading troughs "
            "of the people. Frogs everywhere, inescapable. The magicians replicate the plague "
            "(they make more frogs) but cannot remove them. This underscores the futility of "
            "Egypt's counterfeit power: it can only add to the disaster.\n\n"
            "For the first time, Pharaoh comes to Moses with a request. He asks Moses to pray "
            "that YHWH remove the frogs, and he promises to let the people go. Moses gives "
            "Pharaoh the freedom to choose the time — 'when shall I pray for you?' — and Pharaoh "
            "says 'Tomorrow.' This is one of Scripture's most human details: even with frogs "
            "covering his bed, Pharaoh asks for one more night with them rather than immediate "
            "relief. Why? Perhaps pride — he will not look desperate. Moses prays, the frogs die, "
            "and they are piled in heaps that stink across the land. Pharaoh, relieved, hardens "
            "his heart and breaks his promise.\n\n"
            "The frog was associated with Heqet, the Egyptian goddess of fertility and childbirth "
            "(depicted with a frog's head). The plague takes Egypt's fertility deity and turns it "
            "into an invasion of death-stinking piles.\n\n"
            "## The Third Plague: Gnats (vv.16–19)\n"
            "Without warning — no advance notice to Pharaoh this time — Aaron strikes the dust "
            "of the ground and it becomes gnats (or lice, dust-mites — the Hebrew כִּנִּים, "
            "kinnîm, is uncertain). The gnats cover all humans and animals in Egypt. The "
            "magicians attempt to replicate this plague and cannot. They bring the first "
            "confession of defeat: אֶצְבַּע אֱלֹהִים הִוא (ʾeṣbaʿ ʾĕlōhîm hîʾ) — 'This is "
            "the finger of God.' The plagues have moved beyond what human manipulation can "
            "imitate. Egypt's own specialists concede divine agency. Pharaoh, however, does "
            "not listen.\n\n"
            "## The Fourth Plague: Flies (vv.20–32)\n"
            "The fourth plague introduces a critical new element: geographical distinction. "
            "'I will deal differently with the land of Goshen, where my people live; no swarms "
            "of flies will be there' (v.22). For the first three plagues, Israelites suffered "
            "alongside Egyptians. Now God begins separating His people from the judgment falling "
            "on Egypt. This distinction — in Hebrew הִפְלָה (hiflāh), 'to make a distinction/set "
            "apart' — is a declaration of covenant: God's people are not the same as Egypt's "
            "people, and His judgment falls with precision.\n\n"
            "Pharaoh negotiates a second time, offering a compromise: 'Go and sacrifice to your "
            "God here in the land' (v.25). Moses declines — the sacrifices required would be "
            "offensive to Egyptians and potentially provoke violence. Pharaoh concedes further: "
            "'I will let you go to offer sacrifices to the LORD your God in the wilderness, but "
            "you must not go very far' (v.28). Moses prays, the flies leave — but 'Pharaoh "
            "hardened his heart and would not let the people go' (v.32). The pattern repeats.\n\n"
            "## Theological Themes\n"
            "- **Escalating Judgment**: Each set of three plagues follows a pattern: the first two "
            "are announced; the third comes without warning. The severity escalates across each "
            "group. God is patient, but His patience operates within an intensifying logic.\n"
            "- **The Magicians' Confession**: 'The finger of God' (ʾeṣbaʿ ʾĕlōhîm) is a "
            "theological concession from inside Egypt's own religious establishment. Compare "
            "Deuteronomy 9:10 and Luke 11:20, where Jesus uses the same image ('if I drive out "
            "demons by the finger of God, then the kingdom of God has come to you').\n"
            "- **God's Distinction (hiflāh)**: The Goshen/Egypt distinction reveals that "
            "God's judgment is not indiscriminate. He judges what He targets and protects "
            "what He has claimed. This becomes a theological template for the Passover and "
            "ultimately for the doctrine of election.\n"
            "- **Pharaoh's Negotiations**: Pharaoh's repeated concessions and retreats reveal "
            "the nature of sin under pressure: temporary acknowledgment without genuine repentance. "
            "He wants relief from consequences without change of direction.\n\n"
            "## How This Chapter Points to Christ\n"
            "'The finger of God' in Luke 11:20 is Jesus' own self-description of His ministry. "
            "When Jesus drives out demons, He is doing what the plagues do on a cosmic scale: "
            "demonstrating that the kingdom of God has come and the kingdom of darkness must "
            "yield. The distinction between Goshen and Egypt anticipates the New Testament's "
            "distinction between those who are 'in Christ' and those who are not — not based "
            "on ethnicity but on covenant relationship. The failure of Egypt's magicians points "
            "to all human religious and intellectual systems that can imitate but never originate "
            "genuine divine grace. Only Christ can reverse what He has declared.\n\n"
            "## Moral and Spiritual Lessons\n"
            "- Temporary relief from the consequences of sin without genuine repentance leads to "
            "deeper hardening, not true freedom.\n"
            "- When God's own opponents concede His power ('the finger of God'), it is time to "
            "pay close attention.\n"
            "- God distinguishes between His people and the world in the midst of judgment — "
            "covenant relationship matters.\n"
            "- Pharaoh's offer of compromise ('sacrifice here, but don't go far') represents "
            "the enemy's strategy: accept God, but on terms that keep you from full obedience.\n\n"
            "## Practical Application\n"
            "Notice Pharaoh's pattern: suffering → concession → relief → hardening. This is "
            "the cycle of sin-management rather than repentance. Ask yourself: Is there an "
            "area where I only turn to God under pressure, then return to my own way when the "
            "pressure lifts? Also consider the enemy's compromise offer — 'worship God, but "
            "don't go too far.' Are there limits you've placed on your obedience? Moses refused "
            "every partial compromise. Full obedience cannot be negotiated.\n\n"
            "## Believers Sword Reflection\n"
            "Exodus 8 shows that God's judgment is both comprehensive (touching every domain "
            "of Egyptian life) and precise (sparing Goshen). He is not spraying indiscriminate "
            "wrath; He is making a statement about who He is and who His people are. 'I will "
            "make a distinction' — this is covenant language. You belong to Him."
        ),
        "chapter_overview": (
            "Three plagues strike Egypt: frogs (second) — replicated but not reversed by magicians, "
            "Pharaoh negotiates then re-hardens; gnats (third) — cannot be replicated, magicians "
            "confess 'finger of God'; flies (fourth) — first plague to spare Goshen, Pharaoh "
            "offers compromise then re-hardens again."
        ),
        "original_language_notes": [
            {
                "term": "kinnîm (כִּנִּים)",
                "language": "Hebrew",
                "verse": "Exodus 8:16–18",
                "words_used": "כֵּן הָיוּ הַכִּנִּם (kēn hāyû hakkinnîm) — 'so there were gnats/lice'",
                "meaning": (
                    "The exact identification of כִּנִּים (kinnîm) is uncertain — traditional "
                    "translations give 'lice,' 'gnats,' 'mosquitoes,' or 'dust mites.' What is clear "
                    "is the origin: they come from the dust of the earth (עַפַר הָאָרֶץ, ʿafar "
                    "hāʾāreṣ). The ground itself, the most elemental material of creation, becomes "
                    "a source of plague — suggesting that nature, down to its most basic level, "
                    "is subject to YHWH's command."
                )
            },
            {
                "term": "ʾeṣbaʿ ʾĕlōhîm (אֶצְבַּע אֱלֹהִים)",
                "language": "Hebrew",
                "verse": "Exodus 8:19",
                "words_used": "אֶצְבַּע אֱלֹהִים הִוא (ʾeṣbaʿ ʾĕlōhîm hîʾ) — 'this is the finger of God'",
                "meaning": (
                    "אֶצְבַּע (ʾeṣbaʿ, 'finger') is anthropomorphic language for direct divine "
                    "action without human mediation. It appears again in Deuteronomy 9:10 (the "
                    "tablets written by the finger of God) and in Luke 11:20, where Jesus uses "
                    "the identical expression to describe His exorcisms ('if I cast out demons "
                    "by the finger of God, then the kingdom of God has come upon you'). The "
                    "concession comes from Pharaoh's own magicians — an internal confession "
                    "of divine supremacy."
                )
            },
            {
                "term": "hiflāh (הִפְלָה)",
                "language": "Hebrew",
                "verse": "Exodus 8:22–23",
                "words_used": "וְהִפְלֵיתִי בַיּוֹם הַהוּא (wĕhiflêtî bayyôm hahûʾ) — 'I will make a distinction on that day'",
                "meaning": (
                    "הִפְלָה (hiflāh) derives from פָּלָה (pālāh, 'to be marvelous, distinct, set "
                    "apart'). The same root appears in Exodus 33:16 ('what else will distinguish "
                    "me and your people from all the other people on the face of the earth?'). "
                    "The distinction God makes between Goshen and Egypt is not geographic "
                    "favoritism but covenant precision: His people bear a different relationship "
                    "to His judgments. This concept underlies the doctrine of election."
                )
            },
            {
                "term": "ʿārōb (עָרֹב)",
                "language": "Hebrew",
                "verse": "Exodus 8:21–24",
                "words_used": "עָרֹב כָּבֵד (ʿārōb kābēd) — 'a heavy/dense swarm of flies'",
                "meaning": (
                    "עָרֹב (ʿārōb) is traditionally translated 'flies' but the root means 'mixture' "
                    "or 'swarm' — possibly a mixture of biting insects. כָּבֵד (kābēd, 'heavy, "
                    "dense') is the same root as the word used for Pharaoh's hardened heart "
                    "(כָּבֵד לֵב). The density of the swarm and the density of Pharaoh's heart "
                    "share a word — a subtle irony: what he refuses to acknowledge, he literally "
                    "has to wade through."
                )
            }
        ],
        "moral_lessons": [
            "Temporary relief from pressure without genuine repentance leads to deeper hardening — Pharaoh's cycle is a warning.",
            "Even the opponents of God's work may concede His power while refusing His authority.",
            "God's judgment is precise, not arbitrary — He distinguishes between His people and those outside the covenant.",
            "The enemy's strategy is partial compromise: 'accept God, but don't go too far.' Full obedience cannot be negotiated.",
            "When God removes a consequence we brought through prayer, the temptation to forget the lesson is strong — guard against it."
        ],
        "application": (
            "Examine whether your relationship with God follows Pharaoh's cycle: crisis → turning to God → "
            "relief → returning to old patterns. True repentance does not reverse when pressure lifts. "
            "Also consider where you have accepted a partial commitment to God — worshipping 'here in "
            "the land' rather than going fully out. What specific area of full obedience are you "
            "currently negotiating away?"
        ),
        "prayer": (
            "LORD, I do not want to be a person who seeks relief from consequences rather than "
            "genuine transformation. Guard me from the cycle of crisis-prayer and fair-weather "
            "abandonment. Let the 'finger of God' that I see in Your working be enough to move "
            "me to genuine, lasting change. I accept no partial compromise — take all of me. Amen."
        ),
        "key_points": [
            "Three plagues in Exodus 8: frogs (second), gnats (third), flies (fourth) — escalating severity.",
            "Magicians replicate frogs but cannot reverse them; they cannot replicate gnats at all.",
            "The magicians confess 'This is the finger of God' — the first concession from inside Egypt's religious system.",
            "The fourth plague (flies) spares Goshen — first time God makes a distinction (hiflāh) between His people and Egypt.",
            "Pharaoh twice negotiates, offers compromise ('sacrifice here'), then hardens after pressure is removed.",
            "The frog plague targeted Heqet (frog-headed goddess of fertility) — another Egyptian deity is defeated."
        ],
        "study_questions": [
            "Why do you think Pharaoh asked for 'tomorrow' when asked when Moses should pray to remove the frogs? What does this reveal about human nature under pressure?",
            "The magicians confess 'This is the finger of God' but Pharaoh ignores them. What does this tell us about the relationship between intellectual acknowledgment of God's power and genuine submission?",
            "What is the theological significance of God making a distinction (hiflāh) between Goshen and Egypt starting with the fourth plague?",
            "Pharaoh offers Moses a compromise: 'Sacrifice here in the land.' Why does Moses refuse? What principle does his refusal model for our own discipleship?",
            "Trace Pharaoh's pattern in Exodus 8: pressure → concession → relief → hardening. Where do you see this same cycle in human hearts — including your own?"
        ],
        "tags": ["exodus", "plagues", "frogs", "gnats", "flies", "pharaoh", "finger-of-god", "goshen", "distinction", "magicians", "compromise"],
        "sources": []
    },
    # ─────────────────────────────────────────────────────────────────────────
    # EXODUS 9
    # ─────────────────────────────────────────────────────────────────────────
    {
        "chapter": 9,
        "title": "Exodus 9 — Livestock, Boils, and Hail: Pharaoh Confesses Sin but Hardens Again",
        "summary": (
            "Exodus 9 contains the fifth, sixth, and seventh plagues: death of Egyptian livestock, "
            "boils on humans and animals, and devastating hail. Each plague intensifies the pressure "
            "on Pharaoh and Egypt. For the first time, Pharaoh makes a genuine-sounding confession: "
            "'I have sinned; the LORD is in the right, and I and my people are in the wrong.' Yet "
            "he hardens his heart again. The chapter reveals the difference between remorse that "
            "seeks relief and repentance that produces change."
        ),
        "content": (
            "## What Exodus 9 Is About\n"
            "Exodus 9 marks the midpoint of the plague cycle and introduces several theological "
            "firsts: the first plague to kill (Egyptian livestock), the first plague that strikes "
            "the physical bodies of Pharaoh's officials (boils), and the most spectacular atmospheric "
            "plague so far (hail). It also contains Pharaoh's most explicit verbal confession of sin "
            "in the entire Exodus narrative — and his most dramatic reversal back to hardness.\n\n"
            "## The Fifth Plague: Death of Livestock (vv.1–7)\n"
            "God sends a severe plague against the livestock of Egypt — horses, donkeys, camels, "
            "cattle, sheep, and goats. All die. But 'not one animal belonging to the Israelites "
            "died' (v.6). The distinction established in Exodus 8 continues and deepens. When "
            "Pharaoh investigates, he confirms the report — Israel's livestock are untouched. "
            "Yet his heart is hardened.\n\n"
            "The loss of livestock was catastrophic economically — the animals were Egypt's "
            "agricultural power, military asset, and trade commodity. The plague targeted Apis "
            "(the sacred bull) and Hathor (cow-goddess) among Egypt's deities. The survival "
            "of Israel's livestock is an unmistakable theological statement: the God who "
            "kills Egypt's cattle is actively protecting the cattle of His people.\n\n"
            "## The Sixth Plague: Boils (vv.8–12)\n"
            "For the second time in the third sub-group (the pattern continues), the plague "
            "comes without warning to Pharaoh. Moses takes soot from a furnace (the kiln "
            "or forge — a symbol of Egyptian industrial power) and throws it into the air. "
            "It becomes festering boils on humans and animals throughout Egypt. The magicians "
            "cannot even stand before Moses because the boils are on them too. For the first "
            "time, Pharaoh's own religious specialists are personally afflicted by the plague. "
            "God Himself is said to have hardened Pharaoh's heart (v.12) — we have now passed "
            "from Pharaoh hardening his own heart (chapters 7–8) to God's judicial hardening "
            "confirmed.\n\n"
            "## The Seventh Plague: Hail (vv.13–35)\n"
            "This is the longest and most rhetorically developed plague account. Before it strikes, "
            "God gives the most explicit theological explanation of the plagues: 'But I have "
            "raised you up for this very purpose, that I might show you my power and that my name "
            "might be proclaimed in all the earth' (v.16). The hail is unprecedented in Egypt's "
            "history — accompanied by fire (lightning) running along the ground. Everything left "
            "in the fields is struck; flax and barley are destroyed. But wheat and spelt, which "
            "ripen later, survive — a mercy in the midst of judgment.\n\n"
            "For the first time, some of Pharaoh's officials fear God's word and bring their "
            "servants and livestock inside, sparing them. Those who dismiss the warning lose "
            "everything. This division within Egypt foreshadows the mixed crowd who will leave "
            "with Israel in chapter 12.\n\n"
            "## Pharaoh's Confession (vv.27–28)\n"
            "'This time I have sinned,' Pharaoh says. 'The LORD is in the right, and I and "
            "my people are in the wrong' (v.27). This is the most explicit confession in the "
            "Exodus narrative. But Moses' response is revealing: 'When I have gone out of the "
            "city, I will spread out my hands in prayer to the LORD. The thunder will stop and "
            "there will be no more hail, so you may know that the earth is the LORD's. But I "
            "know that you and your officials still do not fear the LORD God' (vv.29–30). Moses "
            "sees through the confession: it is relief-seeking, not repentance. Pharaoh confirms "
            "this by hardening his heart the moment the hail stops.\n\n"
            "## Theological Themes\n"
            "- **'For This Very Purpose I Raised You Up' (v.16)**: This is one of the most theologically "
            "striking statements in Exodus, quoted by Paul in Romans 9:17 in his discussion of divine "
            "sovereignty and human responsibility. God's purpose in hardening Pharaoh is not arbitrary "
            "cruelty but the proclamation of His name throughout the earth. Even Pharaoh's resistance "
            "serves the revelation of divine glory.\n"
            "- **Remorse vs. Repentance**: Pharaoh's confession ('I have sinned') is genuine in the "
            "sense that he accurately states what happened. But it is not repentance — it does not "
            "produce change of direction. This distinction between remorse (feeling bad) and repentance "
            "(turning around) runs throughout Scripture and is sharpened in Paul's language in "
            "2 Corinthians 7:10: 'Godly sorrow brings repentance that leads to salvation and leaves "
            "no regret, but worldly sorrow brings death.'\n"
            "- **The Earth Is the LORD's (v.29)**: Moses' statement before the hail stops is "
            "the theological conclusion of the plague: the earth does not belong to Pharaoh "
            "or Egypt's gods. YHWH owns all creation. Every judgment in Exodus is a "
            "reclamation of what belongs to Him.\n"
            "- **Grace Within Judgment**: The survival of wheat and spelt, the warning given "
            "to officials before the hail, the survival of those who heeded God's word — "
            "God's judgment is never without mercy for those who respond to the warning.\n\n"
            "## How This Chapter Points to Christ\n"
            "Paul quotes Exodus 9:16 ('for this purpose I raised you up') in Romans 9:17 to "
            "discuss God's sovereign purposes in both mercy and judgment. God's goal — that "
            "His name be proclaimed in all the earth — is ultimately fulfilled in the Great "
            "Commission and the proclamation of the gospel to every nation (Matthew 28:18–20). "
            "Pharaoh's confession without repentance anticipates the warning of James 2:19: "
            "'Even the demons believe that — and shudder.' Intellectual acknowledgment of "
            "God's rightness is not saving faith. The hail of judgment that God will bring "
            "on the last day will also be preceded by warnings — those who take shelter "
            "in Christ (the greater Goshen) will be protected.\n\n"
            "## Moral and Spiritual Lessons\n"
            "- Remorse that seeks relief from consequences, without genuine change of direction, "
            "is not the same as repentance.\n"
            "- God's judgment is purposeful — not arbitrary punishment but revelation of His "
            "identity and the proclamation of His name.\n"
            "- God shows grace within judgment: those who heeded the warning before the hail "
            "were spared. Every divine warning is an act of mercy.\n"
            "- Judicial hardening — God confirming and intensifying a direction a heart has "
            "already chosen — is a solemn possibility for those who repeatedly reject divine "
            "appeals.\n\n"
            "## Practical Application\n"
            "Examine any confession you've recently made to God. Was it primarily driven by "
            "desire to escape consequences, or by genuine sorrow over the offense against "
            "God Himself? The test is what happens after the pressure lifts. Also consider: "
            "are there warnings God has sent into your life — through suffering, Scripture, "
            "or the counsel of others — that you have dismissed? Those who brought their "
            "livestock inside before the hail were spared. Heed the warning.\n\n"
            "## Believers Sword Reflection\n"
            "Exodus 9:29 — 'the earth is the LORD's' — is the theological summary of the "
            "plagues. Egypt believed the earth belonged to Pharaoh and Egypt's gods. The "
            "plagues demonstrate, systematically, that this is false. Every natural force "
            "God deploys — water, animal life, dust, insects, disease, fire, ice — obeys "
            "His word. What Pharaoh claimed to own, God demonstrates He holds."
        ),
        "chapter_overview": (
            "The fifth plague kills Egyptian livestock (Israel's survive), the sixth plague (boils) "
            "strikes humans and animals — even the magicians cannot stand — and the seventh plague "
            "(hail) devastates crops and animals left in the open. God explains His purpose: 'that "
            "my name might be proclaimed in all the earth.' Pharaoh confesses sin but re-hardens "
            "after the hail stops. Officials who heeded the warning were spared."
        ),
        "original_language_notes": [
            {
                "term": "hĕqîmōtîkā (הֲקִימֹתִיךָ)",
                "language": "Hebrew",
                "verse": "Exodus 9:16",
                "words_used": "וְאוּלָם בַּעֲבוּר זֹאת הֶעֱמַדְתִּיךָ (wĕʾûlām baʿăbûr zōʾt heʿĕmadtîkā) — 'But for this purpose I have raised you up'",
                "meaning": (
                    "הֶעֱמַדְתִּיךָ (heʿĕmadtîkā) from עָמַד (ʿāmad, 'to stand/raise up') — "
                    "God tells Pharaoh he was positioned where he is for a divine purpose. Paul "
                    "quotes this in Romans 9:17 using the Greek ἐξήγειρά (exēgeira, 'I raised up'), "
                    "reading it as a statement of divine sovereignty. The verse is central to "
                    "Reformed discussions of predestination and divine hardening. Its context "
                    "is clear: the goal is the proclamation of God's name in all the earth, "
                    "not Pharaoh's eternal damnation."
                )
            },
            {
                "term": "ḥāṭāʾtî (חָטָאתִי)",
                "language": "Hebrew",
                "verse": "Exodus 9:27",
                "words_used": "חָטָאתִי הַפַּעַם (ḥāṭāʾtî happāʿam) — 'I have sinned this time'",
                "meaning": (
                    "חָטָא (ḥāṭāʾ) is the most common Hebrew word for sin, literally meaning "
                    "'to miss the mark' or 'to fail.' Pharaoh's admission is technically accurate — "
                    "he names YHWH as righteous (צַדִּיק, ṣaddîq) and himself as wicked (רָשָׁע, "
                    "rāšāʿ). But the phrase הַפַּעַם (happāʿam, 'this time') reveals its limitation: "
                    "it is situational acknowledgment, not covenant repentance. He says 'this time' "
                    "rather than 'I have sinned against YHWH' with an unconditional commitment to change."
                )
            },
            {
                "term": "bārād (בָּרָד)",
                "language": "Hebrew",
                "verse": "Exodus 9:18–34",
                "words_used": "מָטָר בָּרָד (māṭār bārād) — 'rain of hail'",
                "meaning": (
                    "בָּרָד (bārād, 'hail') appears 29 times in Exodus 9 — the highest concentration "
                    "in any biblical chapter. The repetition mirrors the relentless nature of the "
                    "storm. The accompanying אֵשׁ (ʾēš, 'fire/lightning') 'running along the ground' "
                    "creates the vivid image of a superstorm unlike anything Egypt had seen. Egypt's "
                    "climate historically made hail rare — its occurrence at divine command further "
                    "unmasks the God who controls what Egyptians assumed was governed by their own sky deities."
                )
            },
            {
                "term": "lĕʾumōr (לְאמֹר) + warning structure",
                "language": "Hebrew",
                "verse": "Exodus 9:13, 19",
                "words_used": "הַמְהֵר הָעֵז אֶת מִקְנְךָ (hammahēr hāʿēz ʾet miqnĕkā) — 'Hurry, bring your livestock to shelter'",
                "meaning": (
                    "The warning before the hail is an act of divine mercy embedded within judgment. "
                    "הַמְהֵר (hammahēr, 'hurry') and הָעֵז (hāʿēz, 'bring in/shelter') use urgent "
                    "imperative forms. This pattern — warning before destruction — is consistent "
                    "across the biblical prophets and into Revelation, where every divine judgment "
                    "is preceded by appeal. Some of Pharaoh's officials heeded (v.20) — the first "
                    "Egyptians to respond positively to God's word in the entire Exodus narrative."
                )
            }
        ],
        "moral_lessons": [
            "Remorse that seeks relief from consequences is not the same as repentance that produces change of direction.",
            "God's judgments are always purposeful: they reveal His identity and name to those who witness them.",
            "Divine warnings embedded within judgment are acts of mercy — heeding them is life, dismissing them is death.",
            "Even devastating loss (livestock, crops) does not soften a heart that has chosen to be hard.",
            "Judicial hardening follows repeated rejection of divine appeal — this is a solemn warning, not a comfort."
        ],
        "application": (
            "Test your confessions: are they driven by pain from consequences, or by genuine sorrow "
            "that God has been wronged? Ask what changed in your behavior after the last confession "
            "you made. Also identify any warnings God has given you through suffering, Scripture, or "
            "counsel that you have dismissed. Take shelter before the storm — God's warning is "
            "always also His mercy."
        ),
        "prayer": (
            "LORD, I do not want Pharaoh's confession — accurate words without changed heart. Give "
            "me the godly sorrow that leads to genuine repentance. Where I have heard Your warning "
            "and turned away, have mercy. I acknowledge: the earth is Yours, my life is Yours, "
            "my sin is real. Change me from the inside out. Amen."
        ),
        "key_points": [
            "Fifth plague: all Egyptian livestock die; Israel's are untouched — the distinction between God's people and Egypt continues.",
            "Sixth plague: boils on humans and animals — even the magicians are afflicted and cannot stand before Moses.",
            "Seventh plague: unprecedented hail with lightning destroys crops and animals left in the open.",
            "God's stated purpose (Exodus 9:16): 'that my name might be proclaimed in all the earth' — quoted by Paul in Romans 9:17.",
            "Pharaoh's confession ('I have sinned') is relief-seeking remorse, not repentance — he re-hardens immediately.",
            "Some Egyptian officials heed the warning and are spared — the first Egyptians in Exodus to respond positively to God's word."
        ],
        "study_questions": [
            "What does it mean that God 'raised up' Pharaoh 'for this very purpose'? How does Romans 9:17 use this verse, and what does it teach about divine sovereignty?",
            "What is the difference between Pharaoh's confession 'I have sinned' in verse 27 and genuine biblical repentance? What textual clues reveal the shallowness of his confession?",
            "Why does God include a warning before the hail and allow those who believe it to be spared? What does this reveal about His character even in the midst of judgment?",
            "The text says God hardened Pharaoh's heart (v.12) — whereas earlier, Pharaoh hardened his own heart. How do you understand the relationship between these two truths?",
            "Moses says 'the earth is the LORD's' (v.29). How does this statement summarize the theological argument of all the plagues?"
        ],
        "tags": ["exodus", "plagues", "livestock", "boils", "hail", "pharaoh", "confession", "repentance", "sovereignty", "judgment", "mercy", "romans"],
        "sources": []
    },
    # ─────────────────────────────────────────────────────────────────────────
    # EXODUS 10
    # ─────────────────────────────────────────────────────────────────────────
    {
        "chapter": 10,
        "title": "Exodus 10 — Locusts and Darkness: Egypt Is Brought Low and Pharaoh's Officials Break",
        "summary": (
            "Exodus 10 brings the eighth and ninth plagues: locusts that devour everything remaining "
            "after the hail, and three days of thick darkness so heavy it can be 'felt.' For the "
            "first time, Pharaoh's own officials plead with him to release Israel. God reveals a new "
            "purpose for the plagues: that Israel's children and grandchildren will know what He did "
            "in Egypt. Pharaoh's final negotiation fails; he threatens Moses' life. The chapter "
            "stands at the edge of the decisive final act."
        ),
        "content": (
            "## What Exodus 10 Is About\n"
            "Exodus 10 is the penultimate chapter of the plague narrative and one of the most "
            "theologically rich. God reveals a new layer of purpose for the plagues — not just "
            "Pharaoh's education or Egypt's demolition, but the multigenerational testimony "
            "God is building for Israel. 'That you may tell your children and grandchildren how "
            "I dealt harshly with the Egyptians and how I performed my signs among them, and "
            "that you may know that I am the LORD' (vv.1–2). The plagues are not just crisis "
            "management; they are story-making for every future generation.\n\n"
            "## The Eighth Plague: Locusts (vv.1–20)\n"
            "Before the plague is announced, God tells Moses the purpose: the hardening of "
            "Pharaoh's heart is so that these signs may be performed, multiplied, and told "
            "across generations (vv.1–2). Moses and Aaron deliver the warning — and this time, "
            "for the first time in the narrative, Pharaoh's officials break. 'Do you not yet "
            "realize that Egypt is ruined?' they say (v.7). They plead with Pharaoh to let "
            "Israel go. Egypt's ruling class has collapsed internally.\n\n"
            "Pharaoh summons Moses and Aaron back for a negotiation. He agrees to let the "
            "Israelites go — but only the men. 'Clearly you are bent on evil,' he tells Moses. "
            "Moses refuses: 'We will go with our young and our old, with our sons and our "
            "daughters, and with our flocks and herds' (v.9). Pharaoh drives them out.\n\n"
            "The locusts arrive on an east wind — dense beyond anything Egypt had ever seen, "
            "covering the land so it was black. They devour everything the hail had left: "
            "every plant, every tree, all the remaining vegetation of Egypt. Nothing green "
            "remains. Pharaoh summons Moses quickly: 'I have sinned against the LORD your "
            "God and against you' (v.16) — a step forward in his language (he now names "
            "YHWH as 'the LORD your God') but still fundamentally seeking relief. Moses "
            "prays; a west wind drives the locusts into the Red Sea. Not one locust remains. "
            "Pharaoh's heart is hardened.\n\n"
            "## The Ninth Plague: Darkness (vv.21–29)\n"
            "Moses stretches out his hand and thick darkness covers Egypt for three days — "
            "darkness that can be 'felt' (v.21). No one can see anyone else; no one can move. "
            "But in Goshen, Israel has light.\n\n"
            "The darkness is the most direct assault on Egypt's chief deity: Ra (or Re), the "
            "sun god, the most powerful god in the Egyptian pantheon. Pharaoh himself was the "
            "son of Ra, the earthly embodiment of the sun god's power. Three days of impenetrable "
            "darkness is a direct, total defeat of Ra and therefore of Pharaoh's divine legitimacy. "
            "After three days, Pharaoh calls Moses and offers his most generous concession: "
            "'Go, worship the LORD. Even your women and children may go with you; only leave "
            "your flocks and herds behind' (v.24). Moses refuses even this: 'Not a hoof is "
            "to be left behind' (v.26). Pharaoh erupts: 'Get out of my sight! Make sure you "
            "do not appear before me again! The day you see my face you will die.' Moses "
            "responds with the words that close the chapter: 'Just as you say, I will never "
            "appear before you again' (v.29).\n\n"
            "## Theological Themes\n"
            "- **Multigenerational Testimony (vv.1–2)**: God explicitly states that the plagues "
            "are being designed as narrative memory for future generations. This is the seed of "
            "the Passover seder, the Psalms of history, and the pattern of telling God's story "
            "across time. The Exodus is not just an event — it is the founding story of a people.\n"
            "- **Ra and the Three Days of Darkness**: The sun was Egypt's supreme deity. Three "
            "days of darkness over Egypt while Israel has light is the decisive theological "
            "statement: YHWH outranks Egypt's highest god. The 'three days' will echo in "
            "Israel's history — three days of Jonah in the fish, three days in the wilderness "
            "(the original journey request), and ultimately three days of Jesus in the tomb "
            "before resurrection light.\n"
            "- **Not a Hoof Left Behind**: Moses' refusal to leave even livestock behind is "
            "not stubbornness — it is theological principle. Nothing of what belongs to God's "
            "people can remain in slavery. Full deliverance leaves nothing behind. This becomes "
            "a principle for the total redemption Christ accomplishes: nothing — not our past, "
            "our bodies, our relationships — is left in death's domain.\n"
            "- **Pharaoh's Disintegration**: By the end of chapter 10, Egypt's officials have "
            "broken (v.7), Pharaoh has made his most desperate concession (v.24), and has now "
            "threatened the death of God's representative. He is no longer negotiating from "
            "strength but from the rage of a cornered man.\n\n"
            "## How This Chapter Points to Christ\n"
            "The three days of darkness in Egypt foreshadow the three hours of darkness at the "
            "cross (Matthew 27:45) and the three days in the tomb — the moment when the sun "
            "seemed to be extinguished and God Himself appeared defeated. But as Israel had "
            "light in Goshen while Egypt was dark, so the resurrection brings light out of "
            "the deepest darkness. 'The light shines in the darkness, and the darkness has "
            "not overcome it' (John 1:5). The locust judgment prefigures Revelation 9, where "
            "locusts are again instruments of divine judgment in the final plague-sequence. "
            "'Not a hoof left behind' anticipates the total, nothing-excluded redemption "
            "Christ accomplishes: 'I have lost none of all those you have given me' (John 18:9).\n\n"
            "## Moral and Spiritual Lessons\n"
            "- God designs His works for multigenerational testimony — we are to tell our "
            "children what God has done.\n"
            "- Even those closest to the centers of worldly power (Pharaoh's officials) "
            "eventually see the reality of God's work; pride is what prevents Pharaoh from "
            "following his own advisors.\n"
            "- Anger at God's representatives when they refuse to compromise is a sign of "
            "a heart fully committed to its own authority.\n"
            "- True deliverance is total — 'not a hoof left behind.' God does not do "
            "partial redemption.\n\n"
            "## Practical Application\n"
            "Are you intentionally telling your children or younger believers what God has "
            "done in your life? The Exodus was designed as a story to be told. Invest in "
            "the practice of testimony — not just in crisis, but as regular family and "
            "community conversation. Also: is there any area where you are negotiating "
            "with God about how much you will release — keeping some 'livestock' behind "
            "rather than giving everything to Him? Moses refused any partial deal. "
            "Receive nothing less than total freedom.\n\n"
            "## Believers Sword Reflection\n"
            "Exodus 10 stands at the threshold of the final, definitive act. Egypt is "
            "ruined. The darkness has made Ra irrelevant. Pharaoh has raged and threatened. "
            "And Moses walks out with the words: 'Just as you say, I will never appear "
            "before you again.' What remains is not more negotiation — it is judgment and "
            "exodus. The next chapter will change everything."
        ),
        "chapter_overview": (
            "Eighth plague: locusts devour all remaining vegetation; Pharaoh's officials beg him "
            "to let Israel go; Pharaoh's concession negotiations fail. Ninth plague: three days "
            "of thick darkness over Egypt (targeting Ra, the sun god); Israel has light in Goshen. "
            "Pharaoh offers to let everyone go except livestock; Moses refuses ('not a hoof left "
            "behind'); Pharaoh threatens Moses' life and the two part ways permanently."
        ),
        "original_language_notes": [
            {
                "term": "ḥōšek (חֹשֶׁך) / maʾăpēl (מַאֲפֵל)",
                "language": "Hebrew",
                "verse": "Exodus 10:21–22",
                "words_used": "חֹשֶׁךְ אֲפֵלָה (ḥōšek ʾăpēlāh) — 'darkness of thick darkness'; וַיְמַשֵּׁשׁ חֹשֶׁך (waymašeš ḥōšek) — 'that one can feel the darkness'",
                "meaning": (
                    "Two words for darkness appear together: חֹשֶׁך (ḥōšek, ordinary darkness) and "
                    "אֲפֵלָה (ʾăpēlāh, thick/deep darkness — the darkest possible night). The "
                    "instruction 'that darkness may be felt' uses וַיְמַשֵּׁשׁ (waymašeš, 'to touch/feel'), "
                    "conveying a darkness so dense it has physical presence. This is beyond mere absence "
                    "of light — it is the presence of anti-light. The contrast with Israel's light "
                    "(אוֹר, ʾôr) in Goshen makes the theological point absolute: YHWH is the source of "
                    "light; those outside His covenant walk in qualitatively different darkness."
                )
            },
            {
                "term": "ʾarbeh (אַרְבֶּה)",
                "language": "Hebrew",
                "verse": "Exodus 10:4–15",
                "words_used": "אַרְבֶּה (ʾarbeh) — 'locust'",
                "meaning": (
                    "אַרְבֶּה (ʾarbeh) from רָבָה (rābāh, 'to be many/multiply') — the locust, "
                    "named for its overwhelming multitude. Verse 14 says the locusts were 'more "
                    "numerous than those before them or after them.' They covered the face of the "
                    "whole land (כִּסָּה אֶת עֵין כָּל הָאָרֶץ, kissāh ʾet ʿên kol hāʾāreṣ, "
                    "literally 'covered the eye of all the land'). The locust plague appears in "
                    "Joel 1–2 as a model for divine judgment and in Revelation 9 as an eschatological "
                    "plague. It targets what remains after the hail — a systematic stripping of "
                    "Egypt's agricultural foundation."
                )
            },
            {
                "term": "lĕmaʿan sipēr (לְמַעַן תְּסַפֵּר)",
                "language": "Hebrew",
                "verse": "Exodus 10:1–2",
                "words_used": "לְמַעַן תְּסַפֵּר בְּאָזְנֵי בִנְךָ (lĕmaʿan tĕsappēr bĕʾoznê binkā) — 'so that you may tell in the ears of your son'",
                "meaning": (
                    "סָפַר (sāpar, 'to count, to tell, to recount') — the root of both סֵפֶר "
                    "(sēfer, 'book/scroll') and the practice of telling stories. God explicitly "
                    "designs the plagues as testimony for multigenerational oral transmission. "
                    "'In the ears of your son and your son's son' — God is writing a story "
                    "meant to be retold. This becomes the theological basis for the Passover "
                    "seder, the Psalms of history (78, 105, 106), and the Christian practice "
                    "of testimony and preaching."
                )
            },
            {
                "term": "ṭappĕkem (טַפְּכֶם)",
                "language": "Hebrew",
                "verse": "Exodus 10:10, 24",
                "words_used": "טַפְּכֶם (ṭappĕkem) — 'your little ones/children'",
                "meaning": (
                    "טַף (ṭaf) refers to small children, those who 'trip along' (from a root "
                    "meaning 'to take small steps'). Pharaoh insists the children stay behind "
                    "as hostages to guarantee the Israelites' return. Moses refuses — the "
                    "children are the reason for the journey ('so that we may hold a festival "
                    "to the LORD'). This conflict over the children foreshadows the final "
                    "plague, where Pharaoh's own firstborn will die while every Israelite "
                    "household with the blood on the doorpost is protected."
                )
            }
        ],
        "moral_lessons": [
            "God designs His great works as multigenerational testimony — we are responsible for telling the next generation.",
            "Pride prevents leaders from heeding wise counsel, even when those around them can see the truth (Pharaoh's officials vs. Pharaoh).",
            "True deliverance is total — 'not a hoof left behind.' God does not do partial redemption; neither should we accept it.",
            "Rage at those who refuse to compromise is a sign of a will fully committed to its own sovereignty.",
            "Even the most powerful false religious system (Ra) can be shown impotent by divine action — darkness covering the sun god."
        ],
        "application": (
            "Begin or renew the practice of intentional testimony with the next generation — telling "
            "your children, grandchildren, or younger believers what God has done in your life. "
            "Also: inventory what you are keeping back from full surrender to God. 'Not a hoof "
            "left behind' is the standard. Identify any 'livestock' — any area of life — you "
            "have been holding back from full consecration, and release it."
        ),
        "prayer": (
            "LORD, I want to be a faithful teller of Your story to the generation after me. "
            "Give me the courage and clarity to testify to what You have done. And where I "
            "have kept something back from You — some area of life I have not released — "
            "I surrender it now. Not a hoof left behind. Take all of me. Let Egypt's darkness "
            "make Your light in my life all the more unmistakable. Amen."
        ),
        "key_points": [
            "God explicitly states a new purpose for the plagues: multigenerational testimony for Israel's children and grandchildren.",
            "Eighth plague (locusts): officials beg Pharaoh to release Israel — Egypt's ruling class collapses internally.",
            "Pharaoh offers to let only the men go; Moses refuses — 'we will go with our young and our old... and with our flocks and herds.'",
            "Ninth plague (thick darkness): three days over Egypt while Israel has light — directly defeating Ra, Egypt's chief deity.",
            "Moses refuses Pharaoh's final concession ('leave your livestock'): 'Not a hoof is to be left behind.'",
            "Pharaoh threatens Moses' life; Moses accepts the terms — 'I will never appear before you again' — closing negotiations permanently."
        ],
        "study_questions": [
            "God says the plagues are designed so that Israel will tell their children (Exodus 10:1–2). How does this multigenerational purpose change how you think about God's works in history and in your own life?",
            "Why do Pharaoh's officials plead with him to let Israel go, but Pharaoh refuses? What does pride do to a person's ability to receive wisdom from those around them?",
            "The ninth plague (darkness) targeted Ra, Egypt's most powerful god and the divine identity behind Pharaoh himself. How does defeating the sun god defeat Pharaoh's own claim to divine status?",
            "Moses refuses to leave even the livestock behind ('not a hoof'). What principle does this embody about the nature of true freedom and complete redemption?",
            "How does the three days of darkness in Egypt connect to three days in other key moments in Scripture — Jonah, the original 'three-day journey' request, and Jesus' resurrection?"
        ],
        "tags": ["exodus", "plagues", "locusts", "darkness", "ra", "pharaoh", "testimony", "generations", "freedom", "redemption", "not-a-hoof"],
        "sources": []
    },
]


def get_or_create_collection(conn):
    cur = conn.cursor()
    cur.execute("SELECT id FROM commentary_collections WHERE slug='believers-sword-commentaries'")
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        "INSERT INTO commentary_collections (name, slug, language_code) VALUES (?, ?, ?)",
        ("Believers Sword Commentaries", "believers-sword-commentaries", "en")
    )
    conn.commit()
    return cur.lastrowid


def chapter_exists(conn, collection_id, book_id, chapter):
    cur = conn.cursor()
    cur.execute(
        """SELECT id, content FROM commentary_entries
           WHERE collection_id=? AND book_id=? AND chapter=?
           AND language_code='en' AND reference_scope='chapter'
           AND deleted_at IS NULL""",
        (collection_id, book_id, chapter)
    )
    row = cur.fetchone()
    if not row:
        return False
    content = row[1] or ""
    return len(content.strip()) > 200


def insert_entry(conn, collection_id, data, book_id, chapter):
    cur = conn.cursor()
    entry_uuid = str(uuid.uuid4())
    cur.execute("""
        INSERT INTO commentary_entries (
            uuid, collection_id, book_id, chapter, verse_start, verse_end,
            reference_scope, title, summary, content, application, prayer,
            key_points, study_questions, language_code, theological_perspective,
            status, is_ai_generated, word_count, created_at, updated_at
        ) VALUES (?,?,?,?,NULL,NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        entry_uuid, collection_id, book_id, chapter,
        "chapter",
        data["title"], data["summary"], data["content"],
        data["application"], data["prayer"],
        json.dumps(data["key_points"]),
        json.dumps(data["study_questions"]),
        "en", "Evangelical Christian", "draft",
        1, len(data["content"].split()),
        NOW, NOW
    ))
    conn.commit()
    return entry_uuid


def save_json(data, book_id, book, chapter, entry_uuid):
    dir_path = os.path.join(WORKSPACE, "generated", f"{book_id:02d}-{book.lower().replace(' ', '-')}")
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, f"{chapter:02d}.json")

    record = {
        "uuid": entry_uuid,
        "collection_name": COLLECTION_NAME,
        "author_type": "organization",
        "language_code": "en",
        "theological_perspective": "Evangelical Christian",
        "status": "draft",
        "book_id": book_id,
        "book": book,
        "chapter": chapter,
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
        "created_at": NOW,
        "updated_at": NOW,
    }

    for key in FORBIDDEN_KEYS:
        assert key not in record, f"Forbidden key found: {key}"

    for key in REQUIRED_KEYS:
        assert key in record, f"Required key missing: {key}"

    assert isinstance(record["original_language_notes"], list), "original_language_notes must be a list"
    for note in record["original_language_notes"]:
        for field in ["term", "language", "verse", "words_used", "meaning"]:
            assert field in note, f"Missing field in original_language_note: {field}"

    json_str = json.dumps(record, ensure_ascii=False, indent=2)
    parsed = json.loads(json_str)
    for key in FORBIDDEN_KEYS:
        assert key not in parsed, f"Forbidden key in parsed JSON: {key}"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(json_str)

    return file_path


def update_progress(conn, book_id, book, chapter):
    cur = conn.cursor()
    next_chapter = chapter + 1
    # Exodus has 40 chapters
    if book_id == 2 and chapter >= 40:
        next_book_id = 3
        next_book = "Leviticus"
        next_chapter = 1
    else:
        next_book_id = book_id
        next_book = book

    cur.execute("""
        UPDATE commentary_generation_progress SET
            next_book_id=?, next_book=?, next_chapter=?,
            last_completed_book_id=?, last_completed_book=?, last_completed_chapter=?,
            updated_at=?
        WHERE id=1
    """, (next_book_id, next_book, next_chapter, book_id, book, chapter, NOW))
    if cur.rowcount == 0:
        cur.execute("""
            INSERT INTO commentary_generation_progress
            (id, next_book_id, next_book, next_chapter, last_completed_book_id,
             last_completed_book, last_completed_chapter, completed, updated_at)
            VALUES (1,?,?,?,?,?,?,0,?)
        """, (next_book_id, next_book, next_chapter, book_id, book, chapter, NOW))
    conn.commit()
    return next_book_id, next_book, next_chapter


def main():
    conn = sqlite3.connect(DB_PATH)
    collection_id = get_or_create_collection(conn)

    batch_uuid = str(uuid.uuid4())
    generated = []
    skipped = []
    files_written = []

    for commentary in COMMENTARIES:
        chapter = commentary["chapter"]
        if chapter_exists(conn, collection_id, BOOK_ID, chapter):
            print(f"  SKIP: {BOOK} {chapter} already exists")
            skipped.append(chapter)
            continue

        print(f"  INSERT: {BOOK} {chapter} — {commentary['title']}")
        entry_uuid = insert_entry(conn, collection_id, commentary, BOOK_ID, chapter)
        fp = save_json(commentary, BOOK_ID, BOOK, chapter, entry_uuid)
        files_written.append(fp)
        generated.append(chapter)
        update_progress(conn, BOOK_ID, BOOK, chapter)
        print(f"    -> Saved: {fp}")

    # Update progress JSON
    cur = conn.cursor()
    cur.execute("SELECT next_book_id, next_book, next_chapter FROM commentary_generation_progress WHERE id=1")
    prog = cur.fetchone()
    if prog:
        next_book_id, next_book, next_chapter = prog
    else:
        next_book_id, next_book, next_chapter = 2, "Exodus", 11

    progress_data = {
        "next_book_id": next_book_id,
        "next_book": next_book,
        "next_chapter": next_chapter,
        "last_completed_book_id": BOOK_ID,
        "last_completed_book": BOOK,
        "last_completed_chapter": generated[-1] if generated else (skipped[-1] if skipped else 10),
        "completed": False,
        "updated_at": NOW,
    }
    with open(PROGRESS_JSON, "w", encoding="utf-8") as f:
        json.dump(progress_data, f, indent=2)
    print(f"\nProgress updated: next = {next_book} {next_chapter}")

    # Append log
    log_entry = {
        "timestamp": NOW,
        "generation_batch_id": batch_uuid,
        "start_reference": f"{BOOK} {min(COMMENTARIES, key=lambda x: x['chapter'])['chapter']}",
        "end_reference": f"{BOOK} {max(COMMENTARIES, key=lambda x: x['chapter'])['chapter']}",
        "chapters_generated": len(generated),
        "chapters_skipped": len(skipped),
        "db_rows_inserted": len(generated),
        "files_written": len(files_written),
    }
    with open(LOG_JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

    conn.close()
    print(f"\n=== DONE ===")
    print(f"Generated: Exodus {generated}")
    print(f"Skipped:   Exodus {skipped}")
    print(f"DB rows inserted: {len(generated)}")
    print(f"Files written: {len(files_written)}")
    print(f"Next starting reference: {next_book} {next_chapter}")


if __name__ == "__main__":
    main()
