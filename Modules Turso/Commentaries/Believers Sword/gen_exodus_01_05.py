#!/usr/bin/env python3
"""Generate Believers Sword Commentaries for Exodus chapters 1-5."""

import sqlite3
import json
import os
import uuid
from datetime import datetime, timezone

DB_PATH = "believers_sword_commentaries.db"
GENERATED_DIR = "generated"
PROGRESS_JSON = "commentary_generation_progress.json"
LOG_FILE = "commentary_generation_log.jsonl"

BOOK_ID = 2
BOOK_NAME = "Exodus"
BOOK_SLUG = "exodus"
CHAPTERS = list(range(1, 6))  # 1-5

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

COMMENTARIES = {
    1: {
        "title": "Exodus 1 — Oppression Cannot Silence Providence",
        "summary": (
            "Exodus 1 opens with Israel multiplying in Egypt, fulfilling God's covenant promise to Abraham. "
            "A new Pharaoh, threatened by their growth, enslaves them and orders the death of every Hebrew son. "
            "Yet the midwives fear God over Pharaoh, and God rewards their courage. This chapter teaches that "
            "human oppression cannot frustrate divine purpose — God's plan for His people advances even through suffering."
        ),
        "content": (
            "## What Exodus 1 Is About\n"
            "Exodus 1 opens a new act in the drama of redemption. The patriarchs are gone, but God's covenant promise "
            "to Abraham — that his descendants would be as numerous as the stars — is visibly unfolding. The sons of "
            "Israel multiplied greatly in Egypt, just as God said. But when a new Pharaoh rose who did not remember Joseph, "
            "Israel's growth became a political threat, and systematic oppression began.\n\n"
            "The chapter moves through three escalating stages: forced labor, infanticide ordered through midwives, "
            "and finally a public decree that every newborn Hebrew boy be thrown into the Nile. At each stage, God's "
            "people are pressed harder — yet they continue to multiply (v.12). This paradox is not accidental; it is "
            "the narrator's way of showing that Pharaoh's power, though terrifying, is no match for God's.\n\n"
            "## Theological Themes\n"
            "- **Divine Faithfulness Through Suffering**: Israel's multiplication (v.7) uses language echoing Genesis 1:28 and "
            "God's promise to Abraham. The covenant cannot be undone by human cruelty.\n"
            "- **The Fear of God vs. the Fear of Man**: The midwives Shiphrah and Puah feared God rather than Pharaoh (v.17). "
            "This is the moral hinge of the chapter — courage rooted in reverence for God, not in a political calculation.\n"
            "- **Oppression as a Catalyst**: The harder Pharaoh pressed Israel, the more they grew (v.12). God often uses "
            "opposition to accelerate His purposes, not suppress them.\n"
            "- **Sovereign Limitation of Evil**: Pharaoh's decrees are brutal, but they are also historically temporary. "
            "The chapter anticipates a Deliverer who will break the power of Egypt entirely.\n\n"
            "## Hebrew Word Notes\n"
            "- The word פָּרָה (pārāh, 'be fruitful') and רָבָה (rāvāh, 'multiply') in verse 7 echo Genesis 1:28 and 9:1, "
            "marking Israel's growth as part of God's creational and covenantal design.\n"
            "- עֲבֹדָה קָשָׁה (ʿăvōdāh qāšāh, 'hard service/bitter labor') in verse 14 describes not just physical work "
            "but a dehumanizing system designed to break spirit as much as body.\n"
            "- יָרֵא (yārēʾ, 'feared') in verses 17 and 21 describes the midwives' relationship to God — the same word "
            "used throughout the Old Testament for the reverent trust that defines a life of faith.\n\n"
            "## How This Chapter Points to Christ\n"
            "Israel's suffering under Pharaoh prefigures the suffering of God's people in every age, and ultimately "
            "of God's own Son who entered a world of oppression. Just as the infant Hebrew boys were targeted for death, "
            "so Herod sought to kill the infant Jesus (Matthew 2). God preserved Moses as He later preserved Christ — "
            "the Deliverer could not be destroyed before His appointed time. The Exodus that follows points to a greater "
            "Exodus: Christ's death and resurrection deliver His people from a bondage far deeper than Egypt's.\n\n"
            "## Moral and Spiritual Lessons\n"
            "- Faithfulness to God may put you at odds with earthly authority. The midwives' example is not passive "
            "resistance but active obedience to a higher King.\n"
            "- Suffering does not mean God has forgotten His covenant. The more Israel was pressed, the more they multiplied — "
            "God was at work in what looked like abandonment.\n"
            "- God rewards those who fear Him (v.21). This reward is not always immediate, but it is certain.\n\n"
            "## Practical Application\n"
            "When circumstances suggest God's promises are failing, return to what God has actually said. In seasons of "
            "oppression, the courage of the midwives is a model: obey God quietly, faithfully, without spectacle, trusting "
            "that He sees and rewards. When you must choose between the fear of God and the fear of man, the midwives show "
            "us which fear leads to life.\n\n"
            "## Believers Sword Reflection\n"
            "Exodus 1 invites believers to trust that their history is held in God's hands even when human powers seem "
            "to dominate. The same God who overruled Pharaoh is sovereign over every structure that oppresses His people today."
        ),
        "chapter_overview": (
            "Exodus 1 shows Israel multiplying in Egypt despite brutal oppression, as a new Pharaoh attempts to crush "
            "their growth through forced labor and infanticide. The courage of the midwives who fear God rather than "
            "Pharaoh demonstrates that divine providence advances through and despite human cruelty."
        ),
        "original_language_notes": [
            {
                "term": "pārāh / rāvāh",
                "language": "Hebrew",
                "verse": "Exodus 1:7",
                "words_used": "פָּרָה וַיִּשְׁרְצוּ וַיִּרְבּוּ (pārāh … rāvāh) — 'fruitful … multiplied'",
                "meaning": "These verbs echo the blessing of Genesis 1:28 and 9:1, showing that Israel's growth is not accidental but the outworking of God's creational and covenantal blessing."
            },
            {
                "term": "ʿăvōdāh qāšāh",
                "language": "Hebrew",
                "verse": "Exodus 1:14",
                "words_used": "עֲבֹדָה קָשָׁה (ʿăvōdāh qāšāh) — 'hard/bitter service'",
                "meaning": "Describes the crushing, dehumanizing nature of Egypt's forced labor — not merely difficult work but deliberate oppression designed to break Israel's spirit and reduce them to instruments."
            },
            {
                "term": "yārēʾ",
                "language": "Hebrew",
                "verse": "Exodus 1:17, 21",
                "words_used": "וַתִּירֶאןָ הַמְיַלְּדֹת אֶת-הָאֱלֹהִים (tîrĕʾnāh … ʾet-hāʾĕlōhîm) — 'the midwives feared God'",
                "meaning": "יָרֵא (yārēʾ) is the standard OT word for godly fear — reverent trust and submission to God that shapes moral action. The midwives' fear of God overrode their fear of Pharaoh and became the basis for their courage."
            }
        ],
        "moral_lessons": [
            "God's covenant purposes cannot be crushed by human power, however fearsome.",
            "Fearing God rather than man is the foundation of true moral courage.",
            "Suffering under unjust authority does not mean God has abandoned His people.",
            "God rewards those who act in faithfulness to Him, even at personal risk."
        ],
        "application": (
            "Identify the areas of your life where you are tempted to fear human authority or social pressure more than God. "
            "Let the midwives' example challenge you to quiet, courageous faithfulness. When you cannot see God at work in "
            "a difficult season, recall that Israel's multiplication happened in the middle of their greatest oppression — "
            "God is often most active when He seems most absent."
        ),
        "prayer": (
            "Lord, You are sovereign over every power that rises against Your people. Teach me to fear You above all else, "
            "and to trust that Your purposes cannot be undone by human cruelty or opposition. Give me the quiet courage "
            "of the midwives, and the faith to believe You are at work even when I cannot see it. Amen."
        ),
        "key_points": [
            "Israel's multiplication in Egypt fulfills God's covenant promise to Abraham.",
            "A new Pharaoh enslaves Israel out of fear of their growth.",
            "Oppression intensifies in three stages: forced labor, ordered infanticide, public decree.",
            "The midwives Shiphrah and Puah defy Pharaoh because they fear God.",
            "God blesses the midwives and Israel continues to grow despite oppression.",
            "Human evil cannot frustrate God's covenant purposes."
        ],
        "study_questions": [
            "How does verse 7 connect Israel's growth in Egypt to God's earlier promises (Genesis 12, 15, 17)?",
            "What does it mean practically to 'fear God' rather than 'fear man'? How did the midwives embody this?",
            "Why do you think God allowed the oppression to increase rather than stopping it earlier?",
            "In what ways does Israel's situation in Exodus 1 foreshadow the suffering and eventual deliverance of Jesus Christ?",
            "Where in your own life or your community do you see injustice that calls for the midwives' kind of courage?"
        ],
        "tags": ["exodus", "oppression", "providence", "fear-of-god", "moses", "covenant", "deliverance", "courage"]
    },
    2: {
        "title": "Exodus 2 — The Hidden Hand: Moses Born, Hidden, and Called",
        "summary": (
            "Exodus 2 narrates the birth of Moses, his miraculous preservation through his mother's faith and Pharaoh's "
            "daughter's compassion, his failed first attempt at justice, his exile in Midian, and the cry of Israel that "
            "ascends to God. The chapter shows God at work behind every human decision — sustaining the one who will "
            "become Israel's deliverer and hearing the groaning of His oppressed people."
        ),
        "content": (
            "## What Exodus 2 Is About\n"
            "Exodus 2 introduces the hero of the Exodus story but does so with careful humility — Moses is born, hidden, "
            "found, and shaped by forces largely outside his control. A Levite woman hides her beautiful son three months, "
            "then places him in a papyrus basket among the reeds of the Nile. Pharaoh's own daughter draws him out, names "
            "him Moses, and raises him in the very household seeking to destroy him.\n\n"
            "Moses grows up and identifies with his people. He kills an Egyptian beating a Hebrew, but his act is "
            "premature and he must flee. In Midian he defends Jethro's daughters, marries Zipporah, and lives as a "
            "shepherd — the preparation God uses before public ministry. The chapter closes with the most important "
            "theological statement of the narrative: God heard Israel's groaning, remembered His covenant, and looked "
            "upon them with concern (vv.24–25). The Deliverer is being prepared, and God is watching.\n\n"
            "## Theological Themes\n"
            "- **God Preserves His Servants Through Unexpected Means**: Moses' preservation comes through his mother's "
            "faith, a sister's alertness, and the compassion of a pagan princess. God's providence works through "
            "unlikely human instruments.\n"
            "- **The Ark/Basket as Symbol**: The Hebrew word for Moses' basket (tēvāh) is the same word used for Noah's "
            "ark. Both men are preserved through water in a vessel of salvation, pointing to God's repeated pattern of "
            "preserving His instruments of redemption.\n"
            "- **Preparation Through Wilderness**: Moses' forty years in Midian are not wasted years. God shapes His "
            "servants in obscurity before elevating them to public mission. The wilderness teaches dependence.\n"
            "- **God's Covenant Memory**: Verses 24–25 are among the most important in Exodus: God 'remembered His "
            "covenant' — not that He had forgotten it, but that the appointed time for its fulfillment had arrived. "
            "Divine attention was turning toward Israel's deliverance.\n\n"
            "## Hebrew Word Notes\n"
            "- תֵּבָה (tēvāh, v.3) — 'basket/ark': The same word used for Noah's ark in Genesis 6–9. This lexical "
            "connection is intentional, linking Moses' preservation with Noah's — both are carried through waters of "
            "judgment into a life of redemptive purpose.\n"
            "- מֹשֶׁה (Mōšeh, v.10) — 'Moses': The name means 'drawn out' (מָשָׁה, māšāh — to draw out). Pharaoh's "
            "daughter unwittingly names the one who will draw Israel out of Egypt. The name itself prophesies his mission.\n"
            "- גֵּרְשֹׁם (Gēršōm, v.22) — Moses names his son 'I have been a stranger (gēr) there (šām),' embedding "
            "his exile into his family identity and preserving the memory that his true home and calling lay elsewhere.\n"
            "- וַיִּזְכֹּר אֱלֹהִים (vayyizkōr ʾĕlōhîm, v.24) — 'God remembered': In Hebrew, 'remember' (zākar) "
            "carries the sense of covenantal attention that leads to action, not merely mental recall.\n\n"
            "## How This Chapter Points to Christ\n"
            "Moses' life parallels Christ's at multiple points. Both were endangered as infants by a king who "
            "feared the one who would displace him (Pharaoh/Herod). Both were preserved in Egypt. Both identified "
            "with their people's suffering at great personal cost. But Moses was a flawed type — he acted in "
            "premature violence and fled. Christ, by contrast, bore all injustice without premature resistance, "
            "going to the cross at the appointed time. Moses' story shows both the pattern of the deliverer and "
            "the need for a greater Deliverer who does not fail.\n\n"
            "## Moral and Spiritual Lessons\n"
            "- Faith often looks like a small act of courage in an impossible situation — a basket placed in a river.\n"
            "- God's servants are often prepared through obscurity, exile, and what feels like irrelevance before "
            "their appointed hour.\n"
            "- The impulse for justice must be submitted to God's timing, or it becomes self-defeating, as Moses learned.\n"
            "- God's silence over oppressed people does not mean indifference; His covenant memory is always turning "
            "toward their deliverance.\n\n"
            "## Practical Application\n"
            "If you feel in a season of obscurity, remember Moses' forty years in Midian were not subtracted from "
            "his life — they were part of it. God wastes nothing. If you have acted with good motives but wrong timing, "
            "like Moses who killed the Egyptian, there is still a path forward in God's grace. Look for the small acts "
            "of courage God is calling you to — the basket placed in the river — and trust Him with the outcome.\n\n"
            "## Believers Sword Reflection\n"
            "Exodus 2 teaches that God is never absent from the sufferings of His people, even when His name is not "
            "mentioned. He is the hidden hand in every act of preservation, every compassionate exception to cruelty, "
            "every wilderness season that looks like waste but produces readiness."
        ),
        "chapter_overview": (
            "Exodus 2 narrates Moses' birth, miraculous preservation through a basket in the Nile, adoption by "
            "Pharaoh's daughter, failed early attempt at justice, exile in Midian, marriage, and the theological "
            "turning point where God hears Israel's cry and remembers His covenant — setting the stage for the Exodus."
        ),
        "original_language_notes": [
            {
                "term": "tēvāh",
                "language": "Hebrew",
                "verse": "Exodus 2:3",
                "words_used": "תֵּבַת גֹּמֶא (tēvat gōmeʾ) — 'basket of papyrus/ark of reeds'",
                "meaning": "The same word תֵּבָה (tēvāh) used for Noah's ark in Genesis 6–9. The connection is deliberate — both men are preserved through water in a vessel of salvation, establishing a pattern of God rescuing His chosen instruments."
            },
            {
                "term": "Mōšeh",
                "language": "Hebrew",
                "verse": "Exodus 2:10",
                "words_used": "מֹשֶׁה (Mōšeh) — 'Moses'",
                "meaning": "Derived from מָשָׁה (māšāh, 'to draw out'). Pharaoh's daughter names him 'drawn out' because she drew him from the water — yet the name prophetically describes his entire mission: drawing Israel out of Egypt."
            },
            {
                "term": "Gēršōm",
                "language": "Hebrew",
                "verse": "Exodus 2:22",
                "words_used": "גֵּרְשֹׁם (Gēršōm) — 'a stranger there'",
                "meaning": "A combination of גֵּר (gēr, 'stranger/sojourner') and שָׁם (šām, 'there'). Moses names his son to memorialize his exile — a constant reminder that his calling lay not in Midian but with his people in Egypt."
            },
            {
                "term": "vayyizkōr",
                "language": "Hebrew",
                "verse": "Exodus 2:24",
                "words_used": "וַיִּזְכֹּר אֱלֹהִים (vayyizkōr ʾĕlōhîm) — 'God remembered'",
                "meaning": "זָכַר (zākar, 'remember') in Hebrew carries covenantal weight — it means God's active attention that leads to decisive action. God's 'remembering' here signals that the time for covenant fulfillment has arrived."
            }
        ],
        "moral_lessons": [
            "Small acts of faithful courage — like placing a baby in a basket — can redirect history.",
            "God uses unexpected and unlikely instruments to accomplish His purposes.",
            "Seasons of exile and obscurity are often God's preparation for greater mission.",
            "Good intentions do not substitute for God's timing; premature action can exile us from our calling.",
            "God's silence over suffering is not indifference — He hears, remembers, and acts at the appointed time."
        ],
        "application": (
            "Reflect on any season of obscurity or exile in your own life. Consider how God may be shaping you "
            "through what feels like waiting or detour. If you have acted with good heart but wrong timing, "
            "receive grace and continue — Moses' failure in chapter 2 did not disqualify him from chapter 3. "
            "Pray for the quiet faith of Moses' mother: act on what you can, and release the outcome to God."
        ),
        "prayer": (
            "Heavenly Father, You are the hidden hand behind all preservation. Thank You for working even when "
            "I cannot see You. In seasons that feel like exile, remind me that You are shaping me. Give me faith "
            "to take small courageous steps and trust You with the outcome. And for those who suffer in silence, "
            "Lord — hear their groaning as You heard Israel's, and act in Your perfect time. Amen."
        ),
        "key_points": [
            "Moses' birth and survival fulfill God's providential plan despite Pharaoh's death decree.",
            "The word for Moses' basket (tēvāh) is the same as Noah's ark — God preserves His people through water.",
            "Moses' name ('drawn out') prophesies his mission to draw Israel out of Egypt.",
            "Moses' exile in Midian is divine preparation, not divine abandonment.",
            "God's 'remembering' His covenant (v.24) signals that deliverance is imminent.",
            "God hears the groaning of oppressed people and responds according to His covenant."
        ],
        "study_questions": [
            "What does the connection between Moses' basket and Noah's ark suggest about God's patterns in redemptive history?",
            "How does Moses' premature act of violence (killing the Egyptian) teach us about the importance of God's timing?",
            "What does it mean that 'God remembered His covenant' (v.24)? Does God forget?",
            "In what ways is Moses' life a type or foreshadowing of Jesus Christ?",
            "How should the truth that God hears the groaning of suffering people shape how we pray for the oppressed?"
        ],
        "tags": ["exodus", "moses", "providence", "preparation", "covenant", "suffering", "deliverance", "midian"]
    },
    3: {
        "title": "Exodus 3 — The Burning Bush: God Reveals His Name and His Mission",
        "summary": (
            "Exodus 3 is one of the most theologically rich chapters in Scripture. At a burning bush on holy ground, "
            "God reveals Himself to Moses as the God of Abraham, Isaac, and Jacob — and discloses His covenant name "
            "YHWH ('I AM WHO I AM'). He commissions Moses to confront Pharaoh and lead Israel out of Egypt. "
            "This chapter establishes the character and name of God as the foundation for all that follows in Exodus."
        ),
        "content": (
            "## What Exodus 3 Is About\n"
            "After forty years as a shepherd in Midian, Moses encounters God at Horeb — the mountain of God — in "
            "the form of a bush that burns without being consumed. The bush is a theophany: a visible manifestation "
            "of God's presence. God speaks: He identifies Himself as the God of the patriarchs, declares that He "
            "has heard and seen Israel's affliction, and commissions Moses to go to Pharaoh and lead Israel out.\n\n"
            "Moses' first response is retreat (v.6, he hides his face). His second is a question: 'Who am I to do "
            "this?' (v.11). God's answer is not a list of Moses' qualifications but a promise: 'I will be with you' "
            "(v.12). Moses then asks the deepest question: What is Your name? God's answer — אֶהְיֶה אֲשֶׁר אֶהְיֶה "
            "('I AM WHO I AM') — is the theological summit of the chapter and one of the most important self-disclosures "
            "of God in the entire Bible.\n\n"
            "## Theological Themes\n"
            "- **The Holiness of God**: 'Remove your sandals, for the place where you are standing is holy ground' (v.5). "
            "God's holiness is not a property that humanity can approach casually. Moses must prepare, recognize, and "
            "reverence the distinction between the holy God and created humanity.\n"
            "- **God Sees and Hears Suffering**: 'I have indeed seen the misery of my people… I have heard them crying "
            "out… I am concerned about their suffering' (v.7). Before commissioning Moses, God establishes His compassion. "
            "The Exodus flows from divine seeing, hearing, and caring.\n"
            "- **The Divine Name YHWH**: 'I AM WHO I AM' (ʾehyeh ʾăšer ʾehyeh) speaks of God's self-existence, "
            "eternal being, and absolute independence. He exists from Himself, is defined by nothing outside Himself, "
            "and is the ground of all existence. This name is also covenantal — He is the I AM who will be with His people.\n"
            "- **The Covenant God of the Patriarchs**: God identifies Himself as the God of Abraham, Isaac, and Jacob (v.6, 15). "
            "The Exodus is not a new plan — it is the fulfillment of promises made centuries earlier. Covenant faithfulness "
            "drives the whole narrative.\n\n"
            "## Hebrew Word Notes\n"
            "- אֶהְיֶה אֲשֶׁר אֶהְיֶה (ʾehyeh ʾăšer ʾehyeh, v.14) — 'I AM WHO I AM': The first-person form of the "
            "verb הָיָה (hāyāh, 'to be'). This name conveys absolute, underived existence — God is the one who simply "
            "IS, the ground of being itself. The third-person form is יְהוָה (YHWH), traditionally rendered 'LORD.'\n"
            "- יְהוָה (YHWH, v.15) — The covenant name of God, often called the Tetragrammaton (four letters: "
            "י-ה-ו-ה). It was so sacred that ancient Jewish tradition avoided pronouncing it, substituting אֲדֹנָי "
            "(ʾĂdōnāy, 'Lord'). This name becomes the central name of God throughout the rest of the OT.\n"
            "- קֹדֶשׁ (qōdeš, v.5) — 'holy/holiness': Derived from a root meaning 'set apart.' Holy ground is ground "
            "where God's presence is concentrated — a place requiring special reverence because God Himself is there.\n"
            "- רָאֹה רָאִיתִי (rāʾōh rāʾîtî, v.7) — 'I have indeed seen': A Hebrew infinitive absolute construction "
            "that intensifies the verb. God does not merely glance at Israel's misery — He has fully, intently, "
            "covenantally seen it.\n\n"
            "## How This Chapter Points to Christ\n"
            "Jesus' 'I AM' statements in the Gospel of John (John 6:35; 8:12; 10:9; 11:25; 14:6; 15:1) are deliberate "
            "echoes of Exodus 3:14. When Jesus told the Pharisees 'Before Abraham was, I AM' (John 8:58), He was "
            "claiming the divine name revealed to Moses. The bush that burned without being consumed is also a "
            "theological image — God's holy presence in finite matter without destruction — that prefigures the "
            "Incarnation: God dwelling in human flesh without diminishing His deity or destroying His vessel.\n\n"
            "## Moral and Spiritual Lessons\n"
            "- Holiness demands reverence. In an age that treats God casually, the burning bush reminds us that "
            "approach to God requires the recognition that we stand on holy ground.\n"
            "- God's commissioning of the reluctant, unqualified Moses shows that He does not call the equipped — "
            "He equips the called. 'I will be with you' is always the sufficient answer to 'Who am I?'\n"
            "- God is not distant from human suffering. He sees, hears, and is concerned about the afflictions of "
            "His people — and He moves to deliver.\n"
            "- The name I AM means God's being is not conditioned by circumstances. He is not 'I was' or 'I might be' "
            "but 'I AM' — eternally present and fully engaged.\n\n"
            "## Practical Application\n"
            "When God calls you to something that exceeds your natural capacity, remember Moses' story. The question "
            "'Who am I?' is not wrong — it is honest. But God's answer is always the same: 'I will be with you.' "
            "The sufficiency is in His presence, not your preparation. Cultivate the habit of approaching God with "
            "reverence — removing your sandals, so to speak — recognizing that every encounter with Him is holy ground.\n\n"
            "## Believers Sword Reflection\n"
            "Exodus 3 is the chapter in which God's name is given, and names matter — they reveal character. YHWH, "
            "the I AM, is self-existent, covenant-keeping, compassion-moved, and mission-sending. Every subsequent "
            "action in the Bible flows from this revelation of who God is."
        ),
        "chapter_overview": (
            "At the burning bush on Horeb, God reveals Himself to Moses as the covenant God of the patriarchs, "
            "discloses His divine name I AM WHO I AM (YHWH), declares His compassion for suffering Israel, "
            "and commissions Moses to lead the Exodus — with the foundational promise 'I will be with you.'"
        ),
        "original_language_notes": [
            {
                "term": "ʾehyeh ʾăšer ʾehyeh",
                "language": "Hebrew",
                "verse": "Exodus 3:14",
                "words_used": "אֶהְיֶה אֲשֶׁר אֶהְיֶה (ʾehyeh ʾăšer ʾehyeh) — 'I AM WHO I AM'",
                "meaning": "From הָיָה (hāyāh, 'to be'). This name expresses God's absolute, self-existent, underived being. He exists from Himself and is defined by nothing outside Himself. The third-person form yields יְהוָה (YHWH), the covenant name rendered 'LORD' in most English Bibles."
            },
            {
                "term": "YHWH",
                "language": "Hebrew",
                "verse": "Exodus 3:15",
                "words_used": "יְהוָה (YHWH) — the Tetragrammaton, 'the LORD'",
                "meaning": "The four-letter covenant name of God (י-ה-ו-ה). So sacred that ancient Jews did not pronounce it, substituting ʾĂdōnāy ('Lord'). YHWH is the name by which God binds Himself to Israel in covenant relationship — 'This is my name forever' (v.15)."
            },
            {
                "term": "qōdeš",
                "language": "Hebrew",
                "verse": "Exodus 3:5",
                "words_used": "אַדְמַת-קֹדֶשׁ (ʾadmat qōdeš) — 'holy ground'",
                "meaning": "קֹדֶשׁ (qōdeš) means 'set apart/holy.' The ground is holy not because of any inherent property but because God's presence is there — holiness is relational to God's nature, radiating outward from His presence."
            },
            {
                "term": "rāʾōh rāʾîtî",
                "language": "Hebrew",
                "verse": "Exodus 3:7",
                "words_used": "רָאֹה רָאִיתִי (rāʾōh rāʾîtî) — 'I have indeed seen'",
                "meaning": "The infinitive absolute (rāʾōh) before the finite verb (rāʾîtî) is an emphatic Hebrew construction meaning 'I have truly, certainly, fully seen.' God is stressing the completeness and certainty of His seeing — not a passing glance but a thorough, covenantal attention to Israel's suffering."
            }
        ],
        "moral_lessons": [
            "Holiness requires reverence — we approach God on His terms, not our own.",
            "God's calling is always accompanied by His promise of presence, not a list of our qualifications.",
            "God sees and hears the suffering of His people and is moved to act — His compassion drives the Exodus.",
            "The name I AM establishes that God's being and faithfulness do not depend on circumstances.",
            "Reluctance in the face of God's call should be honest, not an excuse — Moses questioned; God answered and still sent him."
        ],
        "application": (
            "Examine your own response when God's call exceeds your perceived ability. Are you hiding behind 'Who am I?' "
            "as an excuse, or as honest humility? Receive God's answer: 'I will be with you.' Practice approaching "
            "prayer, Scripture, and worship with conscious reverence — removing the sandals of distraction and "
            "casualness to stand attentively before the holy God who is truly present."
        ),
        "prayer": (
            "Holy Father, You are the I AM — self-existent, eternal, and fully present. I stand on holy ground "
            "whenever I approach You. Forgive me for the casualness with which I sometimes treat Your presence. "
            "When You call me beyond my capacity, let Your promise — 'I will be with you' — be enough. "
            "Teach me to know Your name, trust Your character, and follow Your commission. Amen."
        ),
        "key_points": [
            "God appears to Moses in a burning bush that is not consumed — a theophany revealing His presence.",
            "Holy ground requires reverence — God's holiness is not to be approached casually.",
            "God identifies Himself as the covenant God of Abraham, Isaac, and Jacob.",
            "'I AM WHO I AM' (YHWH) reveals God's self-existent, eternal, independent being.",
            "God's commission is accompanied by His sufficiency: 'I will be with you.'",
            "God's seeing and hearing of Israel's suffering precede and motivate the Exodus."
        ],
        "study_questions": [
            "What does 'holy ground' mean theologically? How should the concept of God's holiness shape how we approach worship?",
            "Unpack the name 'I AM WHO I AM.' What does it teach us about God's nature and His covenant relationship with Israel?",
            "Moses asks 'Who am I?' (v.11). God's answer is not about Moses but about Himself. What does this teach us about the basis of Christian calling?",
            "How do Jesus' 'I AM' statements in John's Gospel connect to Exodus 3:14? What does this imply about Jesus' identity?",
            "Why does God first remind Moses of His covenant with the patriarchs before giving His commission? What does this tell us about the nature of the Exodus?"
        ],
        "tags": ["exodus", "burning-bush", "moses", "yhwh", "i-am", "holiness", "covenant", "divine-name", "calling"]
    },
    4: {
        "title": "Exodus 4 — Signs, Objections, and the Appointed Deliverer",
        "summary": (
            "Exodus 4 records Moses' ongoing objections to God's call, God's patient answers with miraculous signs, "
            "the appointment of Aaron as Moses' spokesperson, and Moses' obedient return to Egypt. A mysterious "
            "encounter along the way — where God nearly kills Moses until Zipporah circumcises their son — "
            "underscores that even the deliverer must be under the covenant. The chapter shows God's sovereign "
            "persistence with a reluctant servant and His insistence that covenant obligations cannot be bypassed."
        ),
        "content": (
            "## What Exodus 4 Is About\n"
            "Even after the blazing theophany of Exodus 3, Moses continues to object. Four objections emerge across "
            "chapters 3–4, each met by a divine response:\n\n"
            "1. **'Who am I?'** (3:11) — 'I will be with you.'\n"
            "2. **'What is Your name?'** (3:13) — 'I AM WHO I AM.'\n"
            "3. **'What if they don't believe me?'** (4:1) — Three signs: a staff/serpent, a leprous hand, water "
            "turned to blood.\n"
            "4. **'I am not eloquent'** (4:10) — 'Who made your mouth? I will help you speak.'\n"
            "5. **'Please send someone else'** (4:13) — God becomes angry and appoints Aaron.\n\n"
            "After this, Moses returns to his father-in-law Jethro, gathers his family, and begins the journey to "
            "Egypt. On the way, a chilling episode: God seeks to kill Moses. Zipporah circumcises their son, "
            "averting the crisis. This strange passage establishes that Moses himself must be under covenant "
            "obligation before he can be God's covenant representative to Israel. Finally, Aaron meets Moses, "
            "and together they gather the elders of Israel, who believe when they see the signs.\n\n"
            "## Theological Themes\n"
            "- **God's Patience with Human Weakness**: God meets each objection with a concrete answer. This does "
            "not mean objections are always appropriate — by the fifth, God is angry — but it reveals His gracious "
            "commitment to prepare His servant rather than simply overpowering him.\n"
            "- **Signs as Attestation of God's Messenger**: The three signs (serpent, leprous hand, water/blood) "
            "are credentials — evidence that Moses comes with divine authority, not his own. Signs serve the word "
            "they authenticate.\n"
            "- **Covenant Obligation Applies to All**: The circumcision episode (vv.24–26) is theologically "
            "significant: Moses had apparently not circumcised his son, neglecting the covenant sign given to "
            "Abraham. God would not overlook this even in His chosen deliverer. Covenant faithfulness is not "
            "optional for God's servants.\n"
            "- **God's Sovereignty over Speech**: When Moses claims to be not eloquent, God asks: 'Who gave human "
            "beings their mouths? Who makes them deaf or mute?' (v.11). The Creator of the organ of speech will "
            "supply words to His servant.\n\n"
            "## Hebrew Word Notes\n"
            "- כְּבַד-פֶּה וּכְבַד לָשׁוֹן (kĕvad-peh ûkĕvad lāšōn, v.10) — 'heavy of mouth and heavy of tongue': "
            "Moses' self-description of his speech impediment or inexperience. Ironically, the Torah — which Moses "
            "will receive and transmit — is the most enduring verbal revelation in history.\n"
            "- פֶּה (peh, v.11–12) — 'mouth': God's argument is from creation: He who made the mouth governs it. "
            "He will be with Moses' פֶּה and teach him what to say.\n"
            "- מוֹל (môl, v.25) — 'to circumcise': The act Zipporah performs to save Moses. Circumcision (מִילָה, "
            "mîlāh) was the covenant sign given to Abraham (Genesis 17). Moses' failure to circumcise his son "
            "jeopardized his standing before the covenant God he was sent to represent.\n"
            "- חֲתַן דָּמִים (ḥătan dāmîm, v.25–26) — 'bridegroom of blood': Zipporah's enigmatic words after the "
            "circumcision, understood as connecting the blood of circumcision with deliverance — a foreshadowing "
            "of Passover, where blood would again be the difference between death and life.\n\n"
            "## How This Chapter Points to Christ\n"
            "Moses' repeated inadequacies and final reluctance ('Please send someone else') contrast sharply with "
            "the obedience of Christ, who said 'Not my will, but yours be done' (Luke 22:42) and willingly accepted "
            "the mission of redemption. Where Moses needed coaxing, signs, and an assistant, Christ went willingly "
            "to accomplish what no one else could do. Moses foreshadows the deliverer while demonstrating why a "
            "greater, perfect Deliverer was needed. The circumcision episode — where blood averts divine judgment — "
            "anticipates the Passover and ultimately Calvary, where Christ's blood averts the judgment His people "
            "deserve.\n\n"
            "## Moral and Spiritual Lessons\n"
            "- We may raise honest questions with God, but persistent excuses to avoid His call reveal a heart "
            "not yet fully surrendered.\n"
            "- God can use weak instruments, but He requires that they be under His covenant — he cannot use a "
            "deliverer who exempts himself from covenant obligations.\n"
            "- Signs authenticate messengers but are not ends in themselves; they serve the word of God.\n"
            "- The blood of covenant has always been the ground of deliverance — from circumcision to Passover to "
            "the cross.\n\n"
            "## Practical Application\n"
            "Examine any lingering excuses you are offering God for not moving into the calling He has placed on "
            "your life. Has He provided signs, answers, and companions for the journey? Then move forward in obedience. "
            "Also examine your covenant faithfulness — before representing God to others, are the obligations God "
            "has placed on your own life being met? Moses needed to have his own house in order before he could "
            "confront Pharaoh.\n\n"
            "## Believers Sword Reflection\n"
            "Exodus 4 is both an encouragement and a warning. The encouragement: God is patient with the reluctant "
            "servant. The warning: patience has limits, and covenant obligations are not optional. God is committed "
            "to His mission; He will pursue it with or without our full cooperation — but He pursues us into "
            "obedience before He pursues Pharaoh."
        ),
        "chapter_overview": (
            "Moses raises five objections to God's call; God answers each with patience, signs, and ultimately "
            "the appointment of Aaron. The mysterious circumcision episode reveals that God's deliverer must "
            "himself be under covenant obligation. Moses returns to Egypt with Aaron, and Israel believes when "
            "they see the signs — setting the stage for the confrontation with Pharaoh."
        ),
        "original_language_notes": [
            {
                "term": "kĕvad-peh",
                "language": "Hebrew",
                "verse": "Exodus 4:10",
                "words_used": "כְּבַד-פֶּה וּכְבַד לָשׁוֹן (kĕvad-peh ûkĕvad lāšōn) — 'heavy of mouth and heavy of tongue'",
                "meaning": "Moses' self-description of his speech limitation. כָּבֵד (kāvēd, 'heavy') conveys the sense of difficulty, slowness, or impediment. The same root describes Pharaoh's 'hardened' (כָּבֵד) heart — the deliverer and his opponent share the same vocabulary, highlighting the contrast God will overcome."
            },
            {
                "term": "peh",
                "language": "Hebrew",
                "verse": "Exodus 4:11-12",
                "words_used": "פֶּה (peh) — 'mouth'",
                "meaning": "God's response to Moses' speech objection appeals to His role as Creator of the mouth itself. The one who designed the organ of speech will equip it. This word appears three times in verses 11–12, emphasizing that God's authority over speech is the answer to Moses' inadequacy."
            },
            {
                "term": "môl",
                "language": "Hebrew",
                "verse": "Exodus 4:25",
                "words_used": "וַתִּכְרֹת צִפֹּרָה צֹר (vattikrot Tsippora tsōr) — 'Zipporah cut with a flint'",
                "meaning": "The act of circumcision (מָל, môl, 'to circumcise') was the covenant sign established in Genesis 17. Neglecting this for Moses' son meant Moses himself violated the covenant he was called to represent. Zipporah's act restores covenant standing and averts divine judgment."
            },
            {
                "term": "ḥătan dāmîm",
                "language": "Hebrew",
                "verse": "Exodus 4:25-26",
                "words_used": "חֲתַן דָּמִים (ḥătan dāmîm) — 'bridegroom/son-in-law of blood'",
                "meaning": "An enigmatic phrase Zipporah speaks after circumcising her son. Most interpreters understand it as connecting the blood of circumcision with her husband's preservation — the blood averts death. This anticipates the Passover where blood on doorposts averts the angel of death."
            }
        ],
        "moral_lessons": [
            "Honest questions about our calling are acceptable, but persistent excuses reveal a resistant heart.",
            "God's servants must be under covenant obligation themselves before representing God to others.",
            "God is patient with our weakness but not infinitely tolerant of our disobedience.",
            "Signs and companions for the journey are given by God — obedience is still required.",
            "Blood covenant is the pattern of deliverance throughout Scripture, fulfilled ultimately at the cross."
        ],
        "application": (
            "Identify any 'send someone else' prayer you have been praying — a resistance to God's specific call "
            "on your life disguised as humility. Receive the signs and companions God has already provided and "
            "move forward. Then examine your own covenant faithfulness: are there areas where you are representing "
            "God publicly while neglecting private covenant obligations? Let Moses' circumcision episode prompt "
            "honest self-examination."
        ),
        "prayer": (
            "Lord God, forgive my excuses for avoiding Your call. You have answered every objection I have raised "
            "and provided signs and companions for the journey. Give me a surrendered heart that says yes to Your "
            "commission. And where I have been lax in covenant faithfulness in my own life, show me and restore me. "
            "I trust that You who made my mouth will fill it when I need to speak. Amen."
        ),
        "key_points": [
            "Moses raises five objections to God's call, each met by a patient divine response.",
            "Three signs (serpent, leprous hand, water to blood) authenticate Moses as God's messenger.",
            "Aaron is appointed as Moses' spokesperson after Moses' persistent reluctance.",
            "The circumcision episode shows that covenant obligation applies even to God's chosen deliverer.",
            "Blood (circumcision) averts divine judgment — a pattern pointing forward to the Passover and the cross.",
            "Israel believes when Moses and Aaron present the signs — the mission is confirmed."
        ],
        "study_questions": [
            "What does Moses' repeated reluctance reveal about human nature when faced with God's call? Is any of it justified?",
            "Why would God give Moses miraculous signs to present to Israel? What is the relationship between signs and faith?",
            "The circumcision episode (vv.24–26) is one of the most mysterious in Exodus. Why was it so serious that Moses had not circumcised his son?",
            "How does Exodus 4 contrast Moses' obedience with Jesus' willing acceptance of the cross? What does this contrast teach us about the limits of typology?",
            "What does it mean practically that God is 'with our mouth'? How should this shape how we speak about faith in difficult contexts?"
        ],
        "tags": ["exodus", "moses", "aaron", "signs", "covenant", "circumcision", "calling", "obedience", "blood-covenant"]
    },
    5: {
        "title": "Exodus 5 — Who Is the LORD? Pharaoh's Defiance and Israel's Suffering",
        "summary": (
            "Exodus 5 records the first confrontation between Moses, Aaron, and Pharaoh. Pharaoh's arrogant question "
            "'Who is the LORD?' frames the entire Exodus narrative — the answer will unfold through ten plagues. "
            "Pharaoh increases Israel's suffering by demanding bricks without straw, the Israelites blame Moses, "
            "and Moses brings his complaint to God. The chapter prepares us for the theology of the plagues: "
            "God's goal is not merely Israel's freedom but the revelation of His identity to Egypt and the world."
        ),
        "content": (
            "## What Exodus 5 Is About\n"
            "Moses and Aaron appear before Pharaoh with a simple, bold request: 'Let my people go, so that they "
            "may hold a festival to me in the wilderness' (v.1). Pharaoh's response is one of the most theologically "
            "significant statements in the Old Testament: 'Who is the LORD, that I should obey him and let Israel "
            "go? I do not know the LORD and I will not let Israel go' (v.2).\n\n"
            "Pharaoh's question sets up the theological drama of everything that follows. The plagues are not "
            "primarily humanitarian rescue operations — they are divine self-disclosure. God's goal, stated "
            "repeatedly, is that both Israel and Egypt will 'know that I am the LORD.' Pharaoh will learn who "
            "YHWH is through a series of increasingly devastating demonstrations.\n\n"
            "In response to Moses' request, Pharaoh intensifies the oppression. The Israelites must now gather "
            "their own straw while maintaining the same quota of bricks — an impossible demand designed to "
            "occupy and crush them. The Israelite foremen are beaten when quotas fail. They confront Moses "
            "and Aaron with bitter words, and Moses himself turns to God in complaint, expressing confusion "
            "and near despair: 'Why have you brought trouble on this people? Is this why you sent me?' (v.22).\n\n"
            "## Theological Themes\n"
            "- **'Who is the LORD?'**: Pharaoh's question is the central theological question of the Exodus. "
            "It is not asked in genuine inquiry but in defiant dismissal. Yet the question is real: YHWH is "
            "unknown to Pharaoh. The plagues will be His answer, written in history and nature.\n"
            "- **Suffering Before Deliverance**: The pattern of Exodus is that things get worse before they "
            "get better. The intensified suffering is not evidence that God is absent or powerless; it is "
            "the pressure that builds toward the decisive intervention of Passover and the crossing of the sea.\n"
            "- **Honest Prayer in the Face of Failure**: Moses' lament (vv.22–23) is a model of honest prayer. "
            "He does not pretend things are going well when they are not. He brings his confusion and near-despair "
            "directly to God. The Psalms of lament stand in this same tradition.\n"
            "- **Idolatry and Power**: Pharaoh's resistance is not merely political — it is theological. He is "
            "himself worshipped as a god in Egypt. To acknowledge YHWH would mean acknowledging a higher authority. "
            "The contest is between false and true deity.\n\n"
            "## Hebrew Word Notes\n"
            "- מִי יְהוָה (mî YHWH, v.2) — 'Who is the LORD?': Pharaoh's dismissive question. The Hebrew "
            "interrogative מִי (mî, 'who') carries defiant contempt here — not philosophical inquiry but "
            "a claim that YHWH is unknown and therefore has no authority over him.\n"
            "- מְלָאכָה (mĕlāʾkāh, v.4) — 'work/labor': The same word used for God's creative work in "
            "Genesis 2:2–3. In Genesis, God rests from His mĕlāʾkāh on the seventh day. In Exodus 5, "
            "Pharaoh refuses rest to Israel and intensifies their mĕlāʾkāh — a grotesque parody of creation's "
            "intended order.\n"
            "- תֶּבֶן (teven, vv.7, 10–13, 16, 18) — 'straw': The material Israel was required to gather "
            "themselves. Its repetition in the chapter (seven times!) emphasizes the relentlessness of "
            "Pharaoh's oppression and the impossibility of the demand.\n"
            "- לָמָּה שְׁלַחְתָּנִי (lāmmāh šĕlaḥtānî, v.22) — 'Why did you send me?': Moses' question to God "
            "echoes the language of lament throughout the Psalms. It is also echoed by Jesus from the cross: "
            "'My God, my God, why have you forsaken me?' (Psalm 22:1; Matthew 27:46).\n\n"
            "## How This Chapter Points to Christ\n"
            "Pharaoh's 'Who is the LORD?' is answered not only through the Exodus but ultimately through Christ. "
            "The Gospel of John opens: 'In the beginning was the Word… and the Word was God' — the ultimate "
            "answer to who YHWH is. Jesus is the full and final revelation of God's identity (Hebrews 1:1–3). "
            "Moses' lament — 'Why have you brought trouble on this people?' — anticipates the cry of desolation "
            "from the cross, where the suffering of the innocent reached its deepest point before the greatest "
            "deliverance in history. Things got worse before they got infinitely better — and that pattern "
            "is fulfilled in the cross and resurrection.\n\n"
            "## Moral and Spiritual Lessons\n"
            "- When God's will meets worldly power, things often get harder before they get better. This is "
            "not evidence of divine failure but of divine purpose building toward a decisive revelation.\n"
            "- Honest lament directed to God — even when confused or frustrated — is a form of faith. "
            "Moses' complaint is prayer, not rebellion.\n"
            "- Pharaoh's refusal to acknowledge God's authority is the root of all oppression. "
            "Every system of injustice operates on the question 'Who is the LORD that I should obey Him?'\n"
            "- God's purpose in suffering is often not merely our release from pain but the revelation of "
            "His identity to us and to those watching.\n\n"
            "## Practical Application\n"
            "When you have obeyed God's call and things have gotten harder, not easier, resist the conclusion "
            "that you were wrong to obey. Bring your honest complaint to God as Moses did. Ask the real "
            "questions. But hold on to what God has already said — His character and His covenant are more "
            "reliable than your current circumstances. Also consider: are there areas of your life where "
            "you are answering 'Who is the LORD?' with Pharaoh's dismissal rather than submission?\n\n"
            "## Believers Sword Reflection\n"
            "Exodus 5 reminds us that the road from calling to fulfillment often passes through a place "
            "that looks like failure. The true test of faith is not whether we feel successful after obeying "
            "God, but whether we remain in honest, dependent conversation with Him even when the mission seems "
            "to have made things worse."
        ),
        "chapter_overview": (
            "Moses and Aaron's first confrontation with Pharaoh ends in disaster: Pharaoh dismisses YHWH, "
            "increases Israel's suffering with impossible labor demands, and the Israelites turn on Moses. "
            "Moses' honest lament to God sets up the theological framework for the plagues: God's purpose "
            "is that Pharaoh and Egypt will know who YHWH is."
        ),
        "original_language_notes": [
            {
                "term": "mî YHWH",
                "language": "Hebrew",
                "verse": "Exodus 5:2",
                "words_used": "מִי יְהוָה אֲשֶׁר אֶשְׁמַע בְּקֹלוֹ (mî YHWH ʾăšer ʾešmaʿ bĕqōlô) — 'Who is the LORD that I should obey His voice?'",
                "meaning": "Pharaoh's rhetorical question expresses contempt, not curiosity. מִי (mî, 'who') here carries defiant dismissal — he does not know YHWH and claims no authority requires him to. This question frames the entire Exodus: the plagues are God's extended answer, written in history."
            },
            {
                "term": "mĕlāʾkāh",
                "language": "Hebrew",
                "verse": "Exodus 5:4",
                "words_used": "מְלַאכְתָּם (mĕlaʾktām) — 'their work/labor'",
                "meaning": "מְלָאכָה (mĕlāʾkāh) is the same word used for God's creative work in Genesis 2:2–3, from which He rests on the Sabbath. In Exodus 5, Pharaoh denies Israel rest and intensifies their mĕlāʾkāh — a theological irony: the very word for God's creative work is now the tool of brutal dehumanization."
            },
            {
                "term": "teven",
                "language": "Hebrew",
                "verse": "Exodus 5:7",
                "words_used": "תֶּבֶן (teven) — 'straw'",
                "meaning": "The material for brick-making that Israel was now required to gather themselves. The word appears seven times in the chapter, its repetition mirroring the relentless, crushing logic of Pharaoh's impossible demand — emphasizing that he sought not just labor but demoralization."
            },
            {
                "term": "lāmmāh šĕlaḥtānî",
                "language": "Hebrew",
                "verse": "Exodus 5:22",
                "words_used": "לָמָּה זֶּה שְׁלַחְתָּנִי (lāmmāh zeh šĕlaḥtānî) — 'Why did you even send me?'",
                "meaning": "Moses' lament uses the language of the Psalms of desolation. The word שָׁלַח (šālaḥ, 'to send') connects back to God's commission in chapters 3–4. Moses is not rejecting the call but wrestling honestly with the gap between God's promise and present reality — the posture of honest faith."
            }
        ],
        "moral_lessons": [
            "Obedience to God may initially produce worse circumstances, not better — this is not a sign of failure.",
            "Honest lament brought to God is a form of faith, not a failure of it.",
            "Pharaoh's question 'Who is the LORD?' is the root question behind every human refusal of divine authority.",
            "God's ultimate goal in difficult seasons is often the deeper revelation of who He is.",
            "The suffering of the righteous is not the final word — it is the dark before God's decisive dawn."
        ],
        "application": (
            "If obedience to God has recently made your situation more difficult, resist despair. Bring your "
            "honest confusion to God in prayer — not as rejection of His call but as honest engagement with "
            "the gap between His promise and your experience. Then wait for His response, which will come "
            "in chapter 6. Ask yourself: In any area of life, am I answering 'Who is the LORD?' with "
            "Pharaoh's dismissal instead of submission?"
        ),
        "prayer": (
            "LORD, there are times when my obedience seems to have made things worse, and I don't understand. "
            "Like Moses, I bring my confusion to You honestly. You know the gap between Your promise and my "
            "experience. Teach me to trust Your purposes even when I cannot see them. Reveal Yourself — in "
            "power and in mercy — to me and to those around me who do not yet know who You are. Amen."
        ),
        "key_points": [
            "Pharaoh's question 'Who is the LORD?' frames the theological purpose of the entire Exodus narrative.",
            "The plagues that follow are God's extended answer to Pharaoh's dismissal of YHWH.",
            "Pharaoh increases Israel's suffering in response to Moses' request — things get worse before the deliverance.",
            "Moses brings honest lament to God — a model of authentic prayer in the face of apparent failure.",
            "God's goal is not merely Israel's release but the revelation of His identity to Egypt and the world.",
            "Suffering before deliverance is a recurring biblical pattern, fulfilled most deeply in the cross."
        ],
        "study_questions": [
            "Why does God allow Israel's situation to worsen immediately after Moses obeys His call? What does this teach about the nature of faith and obedience?",
            "Pharaoh asks 'Who is the LORD?' in contempt. How would you answer that question from the book of Exodus alone? How would you answer it from the whole Bible?",
            "How does Moses' lament in verses 22–23 model how believers should handle disappointment and confusion in prayer?",
            "The word for 'labor' (mĕlāʾkāh) in v.4 is the same word used for God's creative work in Genesis 2:2–3. What does this connection suggest about Pharaoh's system of slavery?",
            "Where do you see the pattern of 'worse before better' in your own spiritual life or in Scripture's broader story? How does the cross and resurrection reframe this pattern?"
        ],
        "tags": ["exodus", "pharaoh", "moses", "aaron", "lament", "suffering", "oppression", "who-is-the-lord", "plagues-setup"]
    }
}


def get_or_create_collection(conn):
    cur = conn.cursor()
    cur.execute("SELECT id FROM commentary_collections WHERE slug='believers-sword-commentaries' AND language_code='en'")
    row = cur.fetchone()
    if row:
        return row[0]
    col_uuid = str(uuid.uuid4())
    cur.execute(
        """INSERT INTO commentary_collections
           (uuid, name, slug, collection_type, language_code, theological_perspective, is_offline_available, sync_status)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (col_uuid, "Believers Sword Commentaries", "believers-sword-commentaries",
         "ai_generated", "en", "Evangelical Christian", 1, "local")
    )
    conn.commit()
    return cur.lastrowid


def entry_exists(conn, collection_id, book_id, chapter):
    cur = conn.cursor()
    cur.execute(
        """SELECT id, LENGTH(content) FROM commentary_entries
           WHERE collection_id=? AND book_id=? AND chapter=? AND language_code='en'
             AND reference_scope='chapter' AND deleted_at IS NULL""",
        (collection_id, book_id, chapter)
    )
    row = cur.fetchone()
    if row and row[1] and row[1] > 200:
        return True
    return False


def insert_entry(conn, collection_id, book_id, chapter, data):
    cur = conn.cursor()
    entry_uuid = str(uuid.uuid4())
    cur.execute(
        """INSERT INTO commentary_entries
           (uuid, collection_id, book_id, chapter, verse_start, verse_end,
            reference_scope, title, summary, content, application, prayer,
            key_points, study_questions, language_code, theological_perspective,
            status, is_ai_generated, word_count, sync_status)
           VALUES (?, ?, ?, ?, NULL, NULL, 'chapter', ?, ?, ?, ?, ?, ?, ?, 'en', ?, 'draft', 1, ?, 'local')""",
        (
            entry_uuid,
            collection_id,
            book_id,
            chapter,
            data["title"],
            data["summary"],
            data["content"],
            data["application"],
            data["prayer"],
            json.dumps(data["key_points"]),
            json.dumps(data["study_questions"]),
            data.get("theological_perspective", "Evangelical Christian"),
            len(data["content"].split()),
        )
    )
    conn.commit()
    return entry_uuid


def save_json(book_id, book_name, book_slug, chapter, entry_uuid, collection_id, data):
    dir_name = f"{book_id:02d}-{book_slug}"
    dir_path = os.path.join(GENERATED_DIR, dir_name)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, f"{chapter:02d}.json")

    obj = {
        "uuid": entry_uuid,
        "collection_name": "Believers Sword Commentaries",
        "author_type": "organization",
        "language_code": "en",
        "theological_perspective": "Evangelical Christian",
        "status": "draft",
        "book_id": book_id,
        "book": book_name,
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
        "sources": [],
        "created_at": NOW,
        "updated_at": NOW,
    }

    # Verify no forbidden keys
    forbidden = {"is_ai_generated", "model_name", "prompt_version"}
    for k in forbidden:
        assert k not in obj, f"Forbidden key found: {k}"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

    # Verify it parses back
    with open(file_path, "r", encoding="utf-8") as f:
        parsed = json.load(f)
    for k in forbidden:
        assert k not in parsed, f"Forbidden key in parsed JSON: {k}"

    return file_path


def update_progress(conn, collection_id, next_chapter, chapters_done):
    """Update both DB and JSON progress."""
    next_book_id = BOOK_ID
    next_book = BOOK_NAME
    last_book_id = BOOK_ID
    last_book = BOOK_NAME
    last_chapter = chapters_done[-1]
    next_ch = last_chapter + 1

    # Exodus has 40 chapters
    if next_ch > 40:
        next_book_id = 3
        next_book = "Leviticus"
        next_ch = 1

    # Update JSON
    progress = {
        "next_book_id": next_book_id,
        "next_book": next_book,
        "next_chapter": next_ch,
        "last_completed_book_id": last_book_id,
        "last_completed_book": last_book,
        "last_completed_chapter": last_chapter,
        "completed": False,
        "updated_at": NOW,
    }
    with open(PROGRESS_JSON, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2)

    # Update DB
    cur = conn.cursor()
    cur.execute(
        """UPDATE commentary_generation_progress
           SET current_book_id=?, current_chapter=?,
               last_completed_book_id=?, last_completed_chapter=?,
               updated_at=?
           WHERE collection_id=? AND language_code='en'""",
        (next_book_id, next_ch, last_book_id, last_chapter, NOW, collection_id)
    )
    if cur.rowcount == 0:
        prog_uuid = str(uuid.uuid4())
        cur.execute(
            """INSERT INTO commentary_generation_progress
               (uuid, collection_id, language_code, current_book_id, current_chapter,
                last_completed_book_id, last_completed_chapter,
                target_book_id, chapters_per_batch, status, sync_status)
               VALUES (?, ?, 'en', ?, ?, ?, ?, 66, 5, 'draft', 'local')""",
            (prog_uuid, collection_id, next_book_id, next_ch, last_book_id, last_chapter)
        )
    conn.commit()

    return progress


def append_log(batch_id, start_ref, end_ref, generated, skipped, inserted, files):
    log_entry = {
        "timestamp": NOW,
        "generation_batch_id": batch_id,
        "start_reference": start_ref,
        "end_reference": end_ref,
        "chapters_generated": generated,
        "chapters_skipped": skipped,
        "db_rows_inserted": inserted,
        "files_written": files,
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")


def main():
    batch_id = str(uuid.uuid4())[:8]

    conn = sqlite3.connect(DB_PATH)
    collection_id = get_or_create_collection(conn)

    generated_chapters = []
    skipped_chapters = []
    db_rows_inserted = 0
    files_written = []

    for chapter in CHAPTERS:
        if entry_exists(conn, collection_id, BOOK_ID, chapter):
            print(f"  SKIP: {BOOK_NAME} {chapter} already exists with content")
            skipped_chapters.append(chapter)
            continue

        data = COMMENTARIES[chapter]
        entry_uuid = insert_entry(conn, collection_id, BOOK_ID, chapter, data)
        db_rows_inserted += 1

        file_path = save_json(BOOK_ID, BOOK_NAME, BOOK_SLUG, chapter, entry_uuid, collection_id, data)
        files_written.append(file_path)

        generated_chapters.append(chapter)
        print(f"  DONE: {BOOK_NAME} {chapter} — {data['title']}")

    all_covered = generated_chapters + skipped_chapters
    if all_covered:
        all_covered.sort()
        update_progress(conn, collection_id, max(all_covered) + 1, all_covered)

    conn.close()

    start_ref = f"{BOOK_NAME} {min(CHAPTERS)}"
    end_ref = f"{BOOK_NAME} {max(CHAPTERS)}"
    append_log(batch_id, start_ref, end_ref, len(generated_chapters), len(skipped_chapters), db_rows_inserted, len(files_written))

    print(f"\n=== SUMMARY ===")
    print(f"Generated: {BOOK_NAME} chapters {generated_chapters}")
    print(f"Skipped:   {skipped_chapters}")
    print(f"DB rows inserted: {db_rows_inserted}")
    print(f"Files written: {len(files_written)}")
    for f in files_written:
        print(f"  {f}")
    print(f"Next: Exodus 6 (or as updated in progress)")


if __name__ == "__main__":
    main()
