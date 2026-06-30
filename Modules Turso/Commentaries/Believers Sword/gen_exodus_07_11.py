#!/usr/bin/env python3
"""Generate Exodus chapters 7-11 commentaries."""

import sqlite3
import json
import os
import uuid
from datetime import datetime, timezone

DB_PATH = "/mnt/d/Projects/Personal/Believers-Sword/Modules Turso/Commentaries/Believers Sword/believers_sword_commentaries.db"
GENERATED_DIR = "/mnt/d/Projects/Personal/Believers-Sword/Modules Turso/Commentaries/Believers Sword/generated"
PROGRESS_JSON = "/mnt/d/Projects/Personal/Believers-Sword/Modules Turso/Commentaries/Believers Sword/commentary_generation_progress.json"
LOG_JSONL = "/mnt/d/Projects/Personal/Believers-Sword/Modules Turso/Commentaries/Believers Sword/commentary_generation_log.jsonl"

COLLECTION_NAME = "Believers Sword Commentaries"
COLLECTION_SLUG = "believers-sword-commentaries"
LANGUAGE_CODE = "en"
THEOLOGICAL_PERSPECTIVE = "evangelical"
AUTHOR_TYPE = "ai"

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
BATCH_UUID = str(uuid.uuid4())

COMMENTARIES = [
    {
        "book_id": 2,
        "book": "Exodus",
        "chapter": 7,
        "title": "Exodus 7 — The God Who Judges Idols: Aaron's Staff and the First Plague",
        "summary": "God confirms Moses and Aaron as His spokesmen, hardens Pharaoh's heart, and initiates the contest of plagues — beginning with the Nile turned to blood — demonstrating that He alone is LORD over creation.",
        "content": """Exodus 7 marks the formal opening of the great divine contest between the LORD and Pharaoh. God reframes Moses' role: he will be 'as God to Pharaoh' (v. 1), and Aaron will be his prophet. This language is remarkable — not that Moses becomes divine, but that he stands in the place of divine authority before the world's mightiest ruler. The commission is clear: multiply signs and wonders so that Egypt shall know that 'I am the LORD' (v. 5).

The first confrontation ends with Aaron's staff swallowing the staffs of Pharaoh's magicians. The word for 'swallow' (בָּלַע, bālaʿ) can mean to devour completely — a miniature picture of what God would do to all of Egypt's power. Pharaoh's magicians can replicate some of God's acts by their 'secret arts,' but they cannot reverse them. God's power is not merely greater in degree but different in kind.

The first plague — water turned to blood — strikes the Nile, which Egyptians worshipped as the life-giving source of civilization. The god Hapy and the very identity of Egypt was bound up with the Nile. God's first act of judgment is not random; He attacks the foundational idol. Every drop of water in Egypt — rivers, canals, ponds, and even wooden and stone vessels — becomes blood (v. 19). The fish die, the stench rises, and Egypt cannot drink.

Yet Pharaoh hardens his heart and goes back inside, unmoved (v. 23). The hardening of Pharaoh's heart is one of the Bible's most theologically discussed themes. The text shows both that Pharaoh hardened his own heart and that God hardened it — a paradox that affirms both human responsibility and divine sovereignty. God does not harden an innocent man; He confirms Pharaoh in the direction he has already chosen, making him a vessel of judgment and a platform for divine glory (Romans 9:17).

This chapter calls us to recognize that God's judgments are always directed at specific lies and false gods. He does not merely overpower; He exposes. The Nile bled not just to punish but to reveal that Egypt's god was no god at all.""",
        "chapter_overview": "God commissions Moses and Aaron as His authoritative spokesmen, the Egyptian magicians' staffs are swallowed by Aaron's, and the first plague turns all of Egypt's water to blood — striking the sacred Nile and demonstrating that the LORD alone governs creation.",
        "original_language_notes": [
            {
                "term": "בָּלַע (bālaʿ)",
                "language": "Hebrew",
                "verse": "Exodus 7:12",
                "words_used": "swallowed",
                "meaning": "To swallow or devour completely. Aaron's staff swallowed the magicians' staffs, signaling total victory over Egypt's counterfeit power."
            },
            {
                "term": "חָזַק (ḥāzaq)",
                "language": "Hebrew",
                "verse": "Exodus 7:13",
                "words_used": "hardened",
                "meaning": "To be strong, firm, or stiff. Used repeatedly for Pharaoh's hardened heart — he made his will rigid and unyielding against God's word."
            },
            {
                "term": "דָּם (dām)",
                "language": "Hebrew",
                "verse": "Exodus 7:17",
                "words_used": "blood",
                "meaning": "Blood. The transformation of the Nile's water into dām struck at Egypt's most sacred resource and deity, declaring the LORD's supremacy over false gods."
            },
            {
                "term": "אוֹת (ʾôt)",
                "language": "Hebrew",
                "verse": "Exodus 7:3",
                "words_used": "signs",
                "meaning": "A sign, mark, or appointed token. God multiplied His ʾôtôt (signs) and mōpĕtîm (wonders) as authenticated credentials of His authority and purpose."
            }
        ],
        "moral_lessons": [
            "God targets the idols and false foundations of every culture, not just peripheral behaviors.",
            "Human stubbornness in the face of clear divine revelation deepens judgment rather than escaping it.",
            "God uses ordinary human messengers — like Moses and Aaron — to carry His extraordinary authority.",
            "Counterfeit spiritual power may imitate God but can never reverse or overcome His true work.",
            "God's judgments are purposeful: they are designed so that people will 'know that I am the LORD.'"
        ],
        "application": "We are surrounded by modern 'Niles' — sources of meaning, security, and identity that people worship in place of God. When God dismantles them, the purpose is not merely punishment but revelation: He wants every person to know who He truly is. When hardship strikes the things we depend on most, we should ask: is God exposing an idol? Is He calling me to trust Him rather than His gifts? Also consider: like Moses, we are called to speak God's word faithfully even when the audience seems immovable. Faithfulness is the calling; results belong to God.",
        "prayer": "Lord, expose the Niles in my own life — the things I trust and depend on more than You. Soften my heart when Your Word confronts me, and give me the courage to speak Your truth even to resistant hearts. Let me know You more truly through every sign You perform in my life. Amen.",
        "key_points": [
            "Moses is given authority 'as God to Pharaoh' — God delegates His authoritative representation to human spokesmen.",
            "Aaron's staff swallowing the magicians' staffs signals total divine supremacy over counterfeit power.",
            "The first plague strikes the Nile, Egypt's most sacred resource, exposing the impotence of its gods.",
            "Both God's sovereignty and Pharaoh's responsibility are held together in the mystery of the hardened heart.",
            "The goal of every plague is that Egypt — and Israel — will know: 'I am the LORD.'"
        ],
        "study_questions": [
            "What does it mean that Moses was to be 'as God to Pharaoh,' and how does this help us understand how God uses human messengers today?",
            "Why do you think God chose to attack the Nile specifically as His first act of judgment?",
            "How do you reconcile God hardening Pharaoh's heart with Pharaoh's personal responsibility?",
            "In what ways do people today 'harden their hearts' when confronted with evidence of God's power?",
            "What 'Nile' in your own culture or personal life might God be challenging you to release?"
        ],
        "tags": ["exodus", "plagues", "pharaoh", "hardened heart", "idolatry", "signs and wonders", "blood", "Nile", "sovereignty", "judgment"],
        "sources": ["Exodus 7:1-25", "Romans 9:17-18", "Psalm 78:44", "John 2:1-11"]
    },
    {
        "book_id": 2,
        "book": "Exodus",
        "chapter": 8,
        "title": "Exodus 8 — Frogs, Gnats, and Flies: When God Invades Every Corner of Life",
        "summary": "Three more plagues — frogs, gnats, and flies — escalate God's judgment on Egypt. Pharaoh's magicians fail to replicate the gnats and confess 'This is the finger of God,' while Pharaoh continues to harden his heart despite repeated promises to let Israel go.",
        "content": """Exodus 8 records three more plagues, each intensifying the divine pressure on Egypt and on Pharaoh's increasingly exposed stubbornness. The plagues move from the Nile to the land, from macro-scale catastrophe to intimate personal invasion.

The plague of frogs (vv. 1–15) fills every space of Egyptian life — bedrooms, beds, ovens, kneading bowls. The frog goddess Heqet, associated with fertility and childbirth, is effectively mocked as her sacred animal becomes an unbearable plague. Pharaoh actually requests that Moses pray for their removal, and Moses generously gives Pharaoh the choice of timing — demonstrating both God's mercy and the authenticity of the miracle. When the frogs die and are piled into heaps, the stench fills the land. Yet when relief comes, Pharaoh hardens his heart again (v. 15) — showing that human nature often cries out to God only under pressure, then resumes its course the moment the crisis passes.

The plague of gnats (vv. 16–19) is a turning point. Egypt's magicians cannot replicate this plague and declare to Pharaoh: 'This is the finger of God' (v. 19). The Hebrew word אֶצְבַּע (ʾeṣbaʿ), finger, is a striking image — if the plagues are only God's 'finger,' what would His full hand accomplish? The magicians acknowledge what Pharaoh refuses to. Even those who served false gods recognized divine power when they could not match it.

The plague of flies (or swarms, vv. 20–32) introduces a new element: God distinguishes between Egypt and Goshen, where Israel lives (v. 23). This distinction — the Hebrew word פְּדֻת (pĕdût), meaning separation or redemption — is crucial. God does not only judge; He protects His people in the midst of judgment. Pharaoh makes another half-offer: worship God, but do it here in Egypt, within our land. Moses refuses: true worship of God cannot be confined to the world's terms or geography.

Pharaoh's pattern is now clear: desperate promises, partial concessions, and post-crisis reversals. It is the pattern of religious manipulation rather than genuine repentance.""",
        "chapter_overview": "Frogs invade every space of Egypt (and Pharaoh pleads for their removal but then reneges), gnats defeat the magicians who confess 'the finger of God,' and flies swarm only Egypt while Goshen is protected — revealing that God both judges Egypt and distinguishes His people.",
        "original_language_notes": [
            {
                "term": "צְפַרְדֵּעַ (ṣĕpardēaʿ)",
                "language": "Hebrew",
                "verse": "Exodus 8:2",
                "words_used": "frogs",
                "meaning": "Frog. The Egyptian frog-goddess Heqet was associated with fertility, making the plague of frogs a direct affront to one of Egypt's most revered deities."
            },
            {
                "term": "אֶצְבַּע (ʾeṣbaʿ)",
                "language": "Hebrew",
                "verse": "Exodus 8:19",
                "words_used": "finger",
                "meaning": "Finger. The magicians declare 'this is the finger of God' — acknowledging divine power while Pharaoh remains hardened. Jesus later uses the same image (Luke 11:20) for His exorcisms."
            },
            {
                "term": "כִּנִּים (kinnîm)",
                "language": "Hebrew",
                "verse": "Exodus 8:16",
                "words_used": "gnats",
                "meaning": "Gnats, lice, or mosquitoes — the exact insect is debated. The plague came from dust of the earth itself turning against Egypt, symbolizing the reversal of creation's order."
            },
            {
                "term": "פְּדֻת (pĕdût)",
                "language": "Hebrew",
                "verse": "Exodus 8:23",
                "words_used": "distinction / redemption",
                "meaning": "Separation, redemption. God puts pĕdût between His people and Egypt — the same root as 'redemption' — showing that the Exodus itself is a redemptive act of divine separation."
            }
        ],
        "moral_lessons": [
            "Crisis-driven prayer that returns to sin when relief comes is not repentance — it is manipulation.",
            "Even those who oppose God may recognize His power; recognition without submission is not faith.",
            "God's protection of Goshen shows He distinguishes and preserves His people even amid broader judgment.",
            "True worship of God cannot be domesticated to the terms of the surrounding culture.",
            "Partial obedience — 'worship God, but here, under my terms' — is not true obedience."
        ],
        "application": "Pharaoh's pattern — crying out to God in crisis, bargaining for partial obedience, reverting when pressure lifts — is a mirror many of us have looked into. The challenge is to examine whether our prayers are genuine surrender or crisis management. The 'finger of God' image reminds us that even the smallest divine act is beyond human replication. And God's distinction between Egypt and Goshen is a picture of grace: in the midst of a cursed world, God marks out a people for Himself. That same grace is available to all who come to Him.",
        "prayer": "Father, expose any Pharaoh-like patterns in my heart — moments when I call on You only under pressure and then forget You when relief comes. Let my worship be genuine and constant, not crisis-driven. Thank You that You distinguish Your people and protect them in the midst of judgment. Make me part of Your Goshen. Amen.",
        "key_points": [
            "The frog plague mocked Egypt's frog goddess Heqet, showing God's supremacy over every idol.",
            "Egypt's magicians could not replicate the gnat plague and confessed: 'This is the finger of God.'",
            "Pharaoh's pattern of promise-and-relapse reveals the difference between crisis religion and genuine repentance.",
            "God distinguishes between Egypt and Goshen (pĕdût — separation/redemption), protecting His people.",
            "Pharaoh's demand that Israel worship in Egypt is a type of the world's demand that faith stay within its boundaries."
        ],
        "study_questions": [
            "What does Pharaoh's repeated cycle of promising and reneging reveal about human nature and genuine repentance?",
            "Why was it significant that the magicians — Egypt's own spiritual experts — admitted 'This is the finger of God'?",
            "What does the protection of Goshen teach us about God's care for His people during times of wider judgment?",
            "Pharaoh wanted Israel to worship 'in Egypt.' What are modern equivalents of this demand?",
            "How does the image of God's 'finger' (Exodus 8:19) connect to Jesus' ministry in Luke 11:20?"
        ],
        "tags": ["exodus", "plagues", "frogs", "gnats", "flies", "Pharaoh", "repentance", "Goshen", "finger of God", "redemption"],
        "sources": ["Exodus 8:1-32", "Luke 11:20", "Psalm 105:30-31", "Romans 2:4"]
    },
    {
        "book_id": 2,
        "book": "Exodus",
        "chapter": 9,
        "title": "Exodus 9 — Livestock, Boils, and Hail: God Speaks Through Creation",
        "summary": "Three more plagues — the death of Egyptian livestock, festering boils, and devastating hail — escalate God's judgment while Israel remains protected. Pharaoh's false remorse and the hardening of his heart continue, yet God's sovereign purpose is explicitly stated: to display His power throughout the earth.",
        "content": """Exodus 9 contains three plagues that form the middle triad of the ten, each one intensifying in both scope and personal impact. Together, they demonstrate that God's authority extends over agriculture, human bodies, and the heavens themselves.

The death of Egypt's livestock (vv. 1–7) is total — horses, donkeys, camels, cattle, sheep, and goats. The contrast is absolute: not one animal belonging to Israel dies (v. 6). When Pharaoh investigates and finds Israel's livestock untouched, it does not produce repentance but hardens him further (v. 7). This is the chilling logic of a seared conscience: more evidence produces more resistance.

The plague of boils (vv. 8–12) is unique in two ways. First, it comes without warning — the only plague that falls without prior announcement, signaling an acceleration of judgment. Second, it directly incapacitates the magicians: they cannot even stand before Moses because the boils have covered them (v. 11). The ones who once imitated and challenged God's signs are now themselves victims, their bodies testifying to the power they denied. God hardened Pharaoh's heart even against this, fulfilling His word to Moses.

The plague of hail (vv. 13–35) is described as the most severe storm in Egypt's history (v. 18). But this plague comes with a mercy: God warns the Egyptians to bring their servants and livestock inside. Those who feared the word of the LORD brought their servants in; those who did not suffered the consequences (v. 20–21). Even in the midst of devastating judgment, God offers a path of survival to those willing to trust His word. The hail is accompanied by fire — lightning running along the ground — an apocalyptic image of heaven and earth united in judgment.

Pharaoh makes perhaps his most dramatic confession yet: 'I have sinned; the LORD is in the right, and I and my people are in the wrong' (v. 27). But Moses knows it is not genuine (v. 30). True repentance produces changed behavior; Pharaoh's confession vanishes the moment the hail stops. God's purpose is made explicit in verse 16: 'I have raised you up for this very purpose, that I might show you my power and that my name might be proclaimed in all the earth.' The plagues are not merely punitive — they are proclamation.""",
        "chapter_overview": "Egypt's livestock die while Israel's live, boils cover all Egyptians including the magicians, and devastating hail falls after God warns those willing to heed His word — demonstrating God's comprehensive authority over agriculture, human health, and weather, while Pharaoh's repentance proves hollow.",
        "original_language_notes": [
            {
                "term": "מִקְנֶה (miqneh)",
                "language": "Hebrew",
                "verse": "Exodus 9:3",
                "words_used": "livestock",
                "meaning": "Livestock, cattle, property. The word shares a root with 'acquire/possess,' reminding us that Egypt's wealth and agricultural economy was devastated while Israel's miqneh was untouched."
            },
            {
                "term": "שְׁחִין (šĕḥîn)",
                "language": "Hebrew",
                "verse": "Exodus 9:9",
                "words_used": "boils",
                "meaning": "Festering boils or skin inflammation. The same word appears in Job's suffering (Job 2:7) and in descriptions of covenant curses (Deuteronomy 28:35), connecting bodily affliction to divine judgment."
            },
            {
                "term": "בָּרָד (bārād)",
                "language": "Hebrew",
                "verse": "Exodus 9:18",
                "words_used": "hail",
                "meaning": "Hail. The devastating bārād mingled with fire (lightning) was unparalleled in Egypt's history, signifying the rupture of the natural order under divine command."
            },
            {
                "term": "הַעֲמַדְתִּיךָ (heʿĕmadtîkā)",
                "language": "Hebrew",
                "verse": "Exodus 9:16",
                "words_used": "I have raised you up",
                "meaning": "From ʿāmad (to stand) in Hiphil — 'I caused you to stand.' God's raising of Pharaoh was purposeful: to display divine power and spread God's name throughout the earth."
            }
        ],
        "moral_lessons": [
            "A hardened conscience can receive more and more evidence of God's power and still resist — accumulation of proof does not guarantee repentance.",
            "God's judgments often include mercy: the hail warning offered Egyptians a way of safety if they trusted His word.",
            "Confession under pressure without changed behavior is not genuine repentance.",
            "God uses even His enemies as instruments to spread His name and glory throughout the world.",
            "Suffering that does not come with prior warning — like the boils — reminds us that God owes no one advance notice of discipline."
        ],
        "application": "Pharaoh's crisis confession — 'I have sinned' — with no lasting change is a sobering mirror. Genuine repentance is not saying the right words under pain; it is a changed orientation of the will. Ask yourself: are there areas where I 'confess' repeatedly but continue the same patterns once pressure lifts? Also, notice how the hail warning was grace: even in judgment, God gives people a chance to trust His word. Every day of life is a warning invitation — a call to take God at His word before the storm arrives.",
        "prayer": "Lord, protect me from the kind of repentance that only lasts until the pain stops. Give me the deep heart change that produces lasting fruit. Thank You that even in Your judgments You offer ways of safety to those who trust Your word. Help me take You at Your word every day. Amen.",
        "key_points": [
            "The death of Egypt's livestock while Israel's were untouched was an undeniable sign that God makes distinctions.",
            "The boils incapacitated even the magicians, who could no longer stand before Moses — God silenced His opposition.",
            "The hail warning showed God's mercy even within judgment: those who feared His word were protected.",
            "Pharaoh's confession was genuine in moment but not in will — a pattern of false repentance.",
            "God explicitly states His purpose: to display His power so that His name would be proclaimed throughout the earth."
        ],
        "study_questions": [
            "Pharaoh investigated and confirmed Israel's livestock were untouched — yet hardened his heart more. What does this tell us about the limits of evidence in changing a hard heart?",
            "The boils came without warning. Why do you think God escalated without announcement at this stage?",
            "How does the hail warning illustrate God's character even in a context of judgment?",
            "What is the difference between crisis confession (Pharaoh's) and genuine repentance? How can we tell them apart in our own lives?",
            "How does Romans 9:17 use Exodus 9:16, and what does this teach about God's sovereignty over history?"
        ],
        "tags": ["exodus", "plagues", "boils", "hail", "livestock", "Pharaoh", "repentance", "sovereignty", "judgment", "mercy"],
        "sources": ["Exodus 9:1-35", "Romans 9:17", "Job 2:7", "Deuteronomy 28:35", "Psalm 105:32-33"]
    },
    {
        "book_id": 2,
        "book": "Exodus",
        "chapter": 10,
        "title": "Exodus 10 — Locusts and Darkness: When God Strips Away Every Last Resource",
        "summary": "The eighth and ninth plagues — a devastating locust swarm and three days of thick darkness — complete the dismantling of Egypt's economic and religious foundations. Pharaoh's advisors beg him to yield, and even Pharaoh nearly capitulates, but the hardening continues as God purposes these plagues for generational testimony.",
        "content": """Exodus 10 records the eighth and ninth plagues and represents a dramatic escalation in the pressure on Pharaoh and Egypt. By this point, Egypt is an economically ruined nation, and even Pharaoh's own court pleads with him to release Israel.

God opens the chapter with a striking statement to Moses: 'I have hardened his heart and the hearts of his officials so that I may perform these signs of mine among them, that you may tell your children and grandchildren how I dealt harshly with the Egyptians and how I performed my signs among them, and that you may know that I am the LORD' (vv. 1–2). The plagues are designed to become a permanent testimony across generations — a story to be told and retold. The Exodus is designed to be remembered.

The locust plague (vv. 3–20) is preceded by Pharaoh's officials begging him to let Israel go: 'Do you not yet realize that Egypt is ruined?' (v. 7). Even Pharaoh's inner circle grasps what he will not. Pharaoh attempts a compromise — men may go but women and children must stay. Moses refuses: all Israel, young and old, sons and daughters, flocks and herds, must go (v. 9). This is a crucial principle: God demands the whole household, not partial devotion. The locusts devour everything the hail left, covering the ground so thick that it turns black (v. 15). Egypt's agricultural identity is destroyed.

The plague of darkness (vv. 21–29) is perhaps the most theologically charged. Darkness so thick it could be felt (v. 21) covers Egypt for three days — while Israelites had light in their dwellings. The sun god Ra was Egypt's supreme deity, Pharaoh himself believed to be his earthly son. Three days of impenetrable darkness was not just a meteorological disaster; it was a theological statement that Ra was powerless before the LORD God. The darkness also anticipates Good Friday — when 'darkness came over all the land' for three hours as the true Son of God bore the world's judgment (Matthew 27:45).

Pharaoh's final offer: go, take your children, but leave your livestock. Moses refuses again: not one hoof shall be left behind (v. 26). God requires wholeness of devotion. Pharaoh's fury becomes a death threat: if Moses appears before him again, he will die (v. 28). The conversation has reached its breaking point.""",
        "chapter_overview": "Locusts devour everything the hail left in Egypt while Pharaoh's own officials beg for surrender, then three days of tangible darkness cover Egypt while Israel has light — striking Egypt's supreme sun god Ra and reducing Pharaoh's offers to a furious death threat.",
        "original_language_notes": [
            {
                "term": "אַרְבֶּה (ʾarbeh)",
                "language": "Hebrew",
                "verse": "Exodus 10:4",
                "words_used": "locusts",
                "meaning": "Locusts; from the root רָבָה (rābāh), meaning to be or become many/numerous. The plague was so immense that the ground turned black — a complete economic and agricultural annihilation."
            },
            {
                "term": "חֹשֶׁךְ (ḥōšek)",
                "language": "Hebrew",
                "verse": "Exodus 10:21",
                "words_used": "darkness",
                "meaning": "Darkness, obscurity. The same word used in Genesis 1:2 for the primordial darkness before creation. The plague of ḥōšek reverses creation order, unmaking Egypt's light — a direct assault on Ra."
            },
            {
                "term": "יְמַשֵּׁשׁ (yĕmaššēš)",
                "language": "Hebrew",
                "verse": "Exodus 10:21",
                "words_used": "felt",
                "meaning": "To feel, grope, touch. The darkness was tangible — one could feel it. This intensifies the contrast: Egypt groped in palpable darkness while Israel had light in their dwellings."
            },
            {
                "term": "פַּרְעֹה (Parʿōh)",
                "language": "Hebrew",
                "verse": "Exodus 10:28",
                "words_used": "Pharaoh",
                "meaning": "The Hebrew transliteration of the Egyptian 'Per-aa' meaning 'Great House.' By this chapter, the 'great house' is a ruined house — God has dismantled the empire's foundations one plague at a time."
            }
        ],
        "moral_lessons": [
            "God orchestrates history so that His mighty acts will be told from generation to generation.",
            "Those closest to power sometimes see reality more clearly than the powerful — Pharaoh's advisors recognized Egypt was ruined.",
            "God demands the whole person and whole household — He does not accept partial devotion.",
            "Darkness is a biblical image of divine judgment; light belongs to God's people even when the world is in darkness.",
            "As Pharaoh's offers grew closer to full surrender but never arrived, the cost of partial obedience was total ruin."
        ],
        "application": "The intergenerational purpose of the plagues — 'tell your children and grandchildren' (v. 2) — is a call to deliberate testimony. The stories of what God has done must be actively passed on. Is there a story of God's faithfulness in your life that you have not told to the next generation? Also, the plague of darkness points forward to the cross, where darkness covered the land when the Son of God bore judgment. That darkness is what we were saved from — and the light in Israel's dwellings is a picture of what God gives His people even in the darkest of times.",
        "prayer": "Lord of light and darkness, help me to tell the next generation what You have done in my life. When darkness surrounds the world, let me be a person who has light in my dwelling because of You. Forgive me for areas of partial devotion where I have kept some 'livestock' back from You. I give You all. Amen.",
        "key_points": [
            "God stated His purpose for the plagues: to create a testimony to be told to children and grandchildren across generations.",
            "Pharaoh's own officials urged him to yield — 'Do you not yet realize Egypt is ruined?' — yet Pharaoh would not.",
            "Moses refused every partial compromise: God demands wholeness — men, women, children, and livestock.",
            "The plague of darkness directly mocked Ra, Egypt's supreme sun deity, with three days of palpable darkness.",
            "The darkness anticipates Good Friday (Matthew 27:45), when true judgment darkness fell on the Son of God."
        ],
        "study_questions": [
            "Why do you think God explicitly tied the plagues to intergenerational storytelling (v. 1-2)? How does this shape your view of testimony and family discipleship?",
            "What does it mean that Moses refused every partial offer from Pharaoh? How does this apply to our own surrender to God?",
            "How does the plague of darkness connect to Egypt's theology — particularly the cult of Ra — and to the darkness at the crucifixion?",
            "Pharaoh's officials saw the situation more clearly than he did. What warning does this offer about the blinding effects of pride and power?",
            "What 'livestock' — what partial reserves — might God be asking you to fully surrender?"
        ],
        "tags": ["exodus", "plagues", "locusts", "darkness", "Ra", "testimony", "wholeness", "cross", "sovereignty", "generations"],
        "sources": ["Exodus 10:1-29", "Matthew 27:45", "Psalm 105:34-35", "Genesis 1:2", "Amos 8:9"]
    },
    {
        "book_id": 2,
        "book": "Exodus",
        "chapter": 11,
        "title": "Exodus 11 — The Announcement of the Final Plague: Death of the Firstborn and the Great Exodus",
        "summary": "God announces the final and decisive plague — the death of all Egypt's firstborn — and declares that after it, Pharaoh will drive Israel out completely. The chapter closes the cycle of confrontation and sets the stage for Passover, the event that will define Israel's identity forever.",
        "content": """Exodus 11 is a hinge chapter, brief but weighty, standing between the nine plagues already delivered and the devastating tenth. It records God's announcement of the final plague and the command to prepare for departure. The nine plagues have dismantled Egypt's economy, health, agriculture, and religion. The tenth will strike at its heart — and at the heart of every household.

God instructs Moses to have the Israelites ask their Egyptian neighbors for silver and gold articles (v. 2). The Egyptians willingly comply — the text notes that the LORD gave Israel favor in Egyptian eyes (v. 3). This is remarkable: the very oppressors willingly hand over their wealth. This fulfills the covenant promise of Genesis 15:14 — 'afterward they shall come out with great possessions.' God has been orchestrating this transfer of wealth throughout the plagues.

The announcement of the tenth plague is stark: at midnight the LORD will pass through Egypt and every firstborn will die — from Pharaoh's firstborn on the throne to the firstborn of the slave girl at her hand mill, and all the firstborn of the cattle (v. 5). The scope is total. The cry that will arise will be unlike any in Egypt's history. The Hebrew word צְעָקָה (ṣĕʿāqâh), a great cry or wail, echoes the cry of Israel under oppression in Exodus 2:23 — but now it will be Egypt's turn to cry out.

The distinction is again made explicit: not even a dog shall bark at any Israelite (v. 7). This is a vivid way of saying that divine protection will be absolute. While Egypt is consumed by grief, Israel will be in complete safety. Moses leaves Pharaoh's presence in hot anger (v. 8) — one of only two moments in the narrative when Moses' personal emotion surfaces. The injustice of Pharaoh's obstinacy was not something Moses accepted passively.

The final verse confirms the theological framework: Pharaoh will not listen, 'so that the LORD's wonders may be multiplied in Egypt' (v. 9). Everything has been building to this moment of maximum revelation and maximum deliverance. The tenth plague is not only punitive — it is preparatory. Through it, God will both judge Egypt and create the Passover, the event that will shape Israel's worship for the rest of history.

Theologically, this chapter points directly to Christ. Every firstborn in Egypt faced death — but God would provide a substitute through the Passover lamb. This is the pattern Paul makes explicit: 'Christ, our Passover lamb, has been sacrificed' (1 Corinthians 5:7). The death of the firstborn in Egypt foreshadows the death of God's own firstborn Son, who bore the judgment that should have fallen on us.""",
        "chapter_overview": "God announces the tenth and final plague — the death of every firstborn in Egypt — while Israel will be completely protected. The Israelites receive favor from their Egyptian neighbors and collect silver and gold. Moses delivers the announcement in burning anger, and the stage is fully set for the Passover.",
        "original_language_notes": [
            {
                "term": "בְּכוֹר (bĕkôr)",
                "language": "Hebrew",
                "verse": "Exodus 11:5",
                "words_used": "firstborn",
                "meaning": "Firstborn, the first to open the womb. The bĕkôr held special honor and inheritance rights in the ancient Near East, making the death of every firstborn the most devastating conceivable judgment on a household and nation."
            },
            {
                "term": "צְעָקָה (ṣĕʿāqâh)",
                "language": "Hebrew",
                "verse": "Exodus 11:6",
                "words_used": "cry",
                "meaning": "A loud cry, wail, or outcry. This is the same word used for Israel's cry under oppression (Exodus 2:23; 3:7). Egypt's ṣĕʿāqâh will now match what Israel suffered — divine justice in kind."
            },
            {
                "term": "חֵן (ḥēn)",
                "language": "Hebrew",
                "verse": "Exodus 11:3",
                "words_used": "favor",
                "meaning": "Grace, favor, goodwill. God gave Israel ḥēn in the eyes of the Egyptians — an unmerited goodwill that caused oppressors to willingly give their gold and silver to the ones they had enslaved."
            },
            {
                "term": "חָרָה אַף (ḥārāh ʾap)",
                "language": "Hebrew",
                "verse": "Exodus 11:8",
                "words_used": "hot anger",
                "meaning": "Literally 'his nose burned' — a Hebrew idiom for intense anger. Moses left Pharaoh in ḥārāh ʾap, showing that righteous indignation at injustice is a legitimate human (and prophetic) response."
            }
        ],
        "moral_lessons": [
            "God fulfills His covenant promises in precise detail — the promise of leaving with great possessions (Genesis 15:14) came true.",
            "The death of the firstborn was both judgment and foreshadowing: pointing to the Passover lamb and ultimately to Christ.",
            "God's favor can cause even hostile people to extend generosity — He can move the hearts of oppressors.",
            "Righteous anger at injustice — Moses leaving in hot anger — is not sin but an appropriate response to persistent evil.",
            "The distinction between Egypt and Israel in the final plague makes clear: divine judgment is not random but precisely targeted."
        ],
        "application": "This chapter calls us to see the Exodus as more than ancient history — it is the template for the gospel. We were all in Egypt: under judgment, under the power of sin and death, with no power to escape. But God provided a firstborn to die in our place — His own Son, the Lamb of God. The Passover announced in chapters 11 and 12 is the preview; the cross is the reality. Sit with the weight of Exodus 11 not as a tragedy but as a preparation for the most important rescue in human history.",
        "prayer": "Heavenly Father, thank You that You are a God who keeps every promise — even promises made centuries before their fulfillment. Thank You that the judgment that should have fallen on every one of us fell instead on Your Son, our Passover Lamb. Let me never take that substitution for granted. Amen.",
        "key_points": [
            "God's promise to Abraham that Israel would leave with 'great possessions' (Genesis 15:14) is fulfilled through Egyptian favor.",
            "The death of every firstborn — from Pharaoh's throne to the lowest slave girl — shows that God's judgment is comprehensive and impartial.",
            "Israel's complete protection (not even a dog would bark) shows that God's salvation is equally total.",
            "Moses leaving in hot anger reveals that righteous prophets feel the weight of injustice — they are not detached observers.",
            "The tenth plague is the historical and theological foundation for the Passover, and through it, for the gospel of Christ."
        ],
        "study_questions": [
            "How does the fulfillment of Genesis 15:14 in Exodus 11:2-3 increase your confidence in God's covenant faithfulness?",
            "Why do you think God extended His judgment to every firstborn — 'from Pharaoh on the throne to the prisoner in the dungeon'? What does this universality say about divine justice?",
            "The image of 'not even a dog shall bark' (v. 7) describes Israel's total protection. What does this say about the nature of God's salvation?",
            "Moses left in 'hot anger.' When is anger at injustice appropriate, and how should it be expressed?",
            "How does the tenth plague point forward to Christ as the Passover Lamb (1 Corinthians 5:7)?"
        ],
        "tags": ["exodus", "plagues", "firstborn", "Passover", "judgment", "Christ", "substitution", "gospel", "covenant", "favor"],
        "sources": ["Exodus 11:1-10", "1 Corinthians 5:7", "Genesis 15:14", "John 1:29", "Hebrews 11:28"]
    }
]


def get_or_create_collection(cur):
    cur.execute("SELECT id FROM commentary_collections WHERE slug = ?", (COLLECTION_SLUG,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        "INSERT INTO commentary_collections (uuid, name, slug, description, language_code, created_at, updated_at) VALUES (?,?,?,?,?,?,?)",
        (str(uuid.uuid4()), COLLECTION_NAME, COLLECTION_SLUG, "Verse-by-chapter Bible commentaries for the Believers Sword app.", LANGUAGE_CODE, NOW, NOW)
    )
    return cur.lastrowid


def get_or_create_author(cur):
    cur.execute("SELECT id FROM commentary_authors WHERE display_name = ?", ("Believers Sword AI Commentary Writer",))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        "INSERT INTO commentary_authors (uuid, display_name, biography, author_type, language_code, created_at, updated_at) VALUES (?,?,?,?,?,?,?)",
        (str(uuid.uuid4()), "Believers Sword AI Commentary Writer", "AI-generated evangelical Bible commentaries.", AUTHOR_TYPE, LANGUAGE_CODE, NOW, NOW)
    )
    return cur.lastrowid


def entry_exists(cur, collection_id, book_id, chapter):
    cur.execute(
        """SELECT id, content FROM commentary_entries
           WHERE collection_id=? AND book_id=? AND chapter=? AND language_code=? AND reference_scope='chapter' AND deleted_at IS NULL""",
        (collection_id, book_id, chapter, LANGUAGE_CODE)
    )
    row = cur.fetchone()
    if row:
        content = row[1] or ""
        return len(content) > 200
    return False


def insert_entry(cur, collection_id, author_id, c):
    entry_uuid = str(uuid.uuid4())
    key_points_json = json.dumps(c["key_points"])
    study_questions_json = json.dumps(c["study_questions"])
    tags_json = json.dumps(c["tags"])

    cur.execute(
        """INSERT INTO commentary_entries
           (uuid, collection_id, author_id, book_id, chapter, verse_start, verse_end,
            reference_scope, title, summary, content, application, prayer,
            key_points, study_questions, language_code, theological_perspective,
            status, is_ai_generated, created_at, updated_at)
           VALUES (?,?,?,?,?,NULL,NULL,?,?,?,?,?,?,?,?,?,?,?,1,?,?)""",
        (entry_uuid, collection_id, author_id, c["book_id"], c["chapter"],
         "chapter", c["title"], c["summary"], c["content"],
         c["application"], c["prayer"], key_points_json, study_questions_json,
         LANGUAGE_CODE, THEOLOGICAL_PERSPECTIVE, "draft", NOW, NOW)
    )
    return entry_uuid


def save_json(c, entry_uuid):
    book_slug = c["book"].lower().replace(" ", "-")
    folder_name = f"{c['book_id']:02d}-{book_slug}"
    folder_path = os.path.join(GENERATED_DIR, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, f"{c['chapter']:02d}.json")

    data = {
        "uuid": entry_uuid,
        "collection_name": COLLECTION_NAME,
        "author_type": AUTHOR_TYPE,
        "language_code": LANGUAGE_CODE,
        "theological_perspective": THEOLOGICAL_PERSPECTIVE,
        "status": "draft",
        "book_id": c["book_id"],
        "book": c["book"],
        "chapter": c["chapter"],
        "title": c["title"],
        "summary": c["summary"],
        "content": c["content"],
        "chapter_overview": c["chapter_overview"],
        "original_language_notes": c["original_language_notes"],
        "moral_lessons": c["moral_lessons"],
        "application": c["application"],
        "prayer": c["prayer"],
        "key_points": c["key_points"],
        "study_questions": c["study_questions"],
        "tags": c["tags"],
        "sources": c["sources"],
        "created_at": NOW,
        "updated_at": NOW
    }

    # Verify no forbidden keys
    forbidden = {"is_ai_generated", "model_name", "prompt_version"}
    assert not forbidden.intersection(data.keys()), f"Forbidden keys found: {forbidden.intersection(data.keys())}"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Verify it parses back
    with open(file_path, "r", encoding="utf-8") as f:
        parsed = json.load(f)
    assert not forbidden.intersection(parsed.keys())

    return file_path


def update_progress(next_book_id, next_book, next_chapter, last_book_id, last_book, last_chapter):
    data = {
        "next_book_id": next_book_id,
        "next_book": next_book,
        "next_chapter": next_chapter,
        "last_completed_book_id": last_book_id,
        "last_completed_book": last_book,
        "last_completed_chapter": last_chapter,
        "completed": False,
        "updated_at": NOW
    }
    with open(PROGRESS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return data


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    collection_id = get_or_create_collection(cur)
    author_id = get_or_create_author(cur)
    conn.commit()

    chapters_generated = 0
    chapters_skipped = 0
    db_rows_inserted = 0
    files_written = []

    last_book_id = 2
    last_book = "Exodus"
    last_chapter = 6

    for c in COMMENTARIES:
        if entry_exists(cur, collection_id, c["book_id"], c["chapter"]):
            print(f"SKIP: {c['book']} {c['chapter']} already exists")
            chapters_skipped += 1
            last_chapter = c["chapter"]
            continue

        entry_uuid = insert_entry(cur, collection_id, author_id, c)
        conn.commit()
        db_rows_inserted += 1

        file_path = save_json(c, entry_uuid)
        files_written.append(file_path)
        chapters_generated += 1
        last_chapter = c["chapter"]
        print(f"GENERATED: {c['book']} {c['chapter']} — {c['title']}")

    # Determine next chapter (Exodus 12)
    next_chapter = last_chapter + 1
    next_book_id = 2
    next_book = "Exodus"
    if next_chapter > 40:
        next_book_id = 3
        next_book = "Leviticus"
        next_chapter = 1

    progress = update_progress(next_book_id, next_book, next_chapter, last_book_id, last_book, last_chapter)

    # Update progress table in DB
    cur.execute("SELECT id FROM commentary_generation_progress LIMIT 1")
    prog_row = cur.fetchone()
    if prog_row:
        cur.execute(
            "UPDATE commentary_generation_progress SET current_book_id=?, current_chapter=?, last_completed_book_id=?, last_completed_chapter=?, updated_at=? WHERE id=?",
            (next_book_id, next_chapter, last_book_id, last_chapter, NOW, prog_row[0])
        )
    else:
        cur.execute(
            "INSERT INTO commentary_generation_progress (uuid, current_book_id, current_chapter, last_completed_book_id, last_completed_chapter, status, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?)",
            (str(uuid.uuid4()), next_book_id, next_chapter, last_book_id, last_chapter, 'active', NOW, NOW)
        )
    conn.commit()
    conn.close()

    # Write log entry
    log_entry = {
        "timestamp": NOW,
        "generation_batch_id": BATCH_UUID,
        "start_reference": f"Exodus 7",
        "end_reference": f"Exodus {last_chapter}",
        "chapters_generated": chapters_generated,
        "chapters_skipped": chapters_skipped,
        "db_rows_inserted": db_rows_inserted,
        "files_written": files_written
    }
    with open(LOG_JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

    print("\n=== SUMMARY ===")
    print(f"Generated: Exodus 7–{last_chapter}")
    print(f"Chapters generated: {chapters_generated}")
    print(f"Chapters skipped: {chapters_skipped}")
    print(f"DB rows inserted: {db_rows_inserted}")
    print(f"Files written: {len(files_written)}")
    print(f"Next start: {next_book} {next_chapter}")
    for f in files_written:
        print(f"  {f}")


if __name__ == "__main__":
    main()
