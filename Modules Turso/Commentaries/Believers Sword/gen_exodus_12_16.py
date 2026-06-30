#!/usr/bin/env python3
"""Generate Exodus chapters 12-16 commentaries."""

import sqlite3
import json
import uuid
import os
from datetime import datetime, timezone

DB_PATH = "believers_sword_commentaries.db"
GENERATED_DIR = "generated"
PROGRESS_JSON = "commentary_generation_progress.json"
LOG_FILE = "commentary_generation_log.jsonl"

BOOK_ID = 2
BOOK_NAME = "Exodus"
BOOK_SLUG = "02-exodus"
COLLECTION_ID = 1
COLLECTION_NAME = "Believers Sword Commentaries"

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
BATCH_UUID = str(uuid.uuid4())

CHAPTERS = [
    {
        "chapter": 12,
        "title": "Exodus 12 — The Passover: Blood, Death, and Deliverance",
        "summary": "Exodus 12 records the institution of the Passover — the pivotal night when God struck down every firstborn in Egypt while passing over the households marked with the blood of a slaughtered lamb. Israel was commanded to eat the meal in haste, ready to leave. The tenth plague broke Pharaoh's will, and Israel departed Egypt after 430 years. The Passover is established as a perpetual memorial and points unmistakably to Jesus Christ, the Lamb of God whose blood protects from judgment.",
        "content": """## What Exodus 12 Is About
Exodus 12 is one of the most theologically dense chapters in the entire Old Testament. It records God's institution of the Passover feast — a precise ritual that would protect Israel from the final and most devastating plague while simultaneously enacting Israel's departure from Egypt. The chapter moves between divine instruction (vv. 1-28), the execution of the tenth plague (vv. 29-36), and the beginning of the Exodus march (vv. 37-51).

At the heart of the chapter is a simple but profound act: each household is to slaughter a lamb without blemish, apply its blood to the doorposts and lintel, and eat the roasted meal with unleavened bread and bitter herbs — staff in hand, ready to move. When the LORD passes through Egypt to strike the firstborn, He will "pass over" every house marked with blood. The substitutionary death of the lamb shields the firstborn of Israel.

## Theological Themes
- **Substitutionary Atonement**: The lamb dies in place of the firstborn. Death comes to every household in Egypt — either the lamb dies, or the son dies. This is the logic of sacrifice that runs through the entire Bible.
- **The Centrality of Blood**: "The blood shall be a sign for you … and when I see the blood, I will pass over you" (v.13). Salvation on that night was not based on the moral standing of individual Israelites — it was based on the applied blood. This anticipates the New Testament teaching that Christ's blood, appropriated by faith, is the basis of our standing before God.
- **Haste and Readiness**: The meal was eaten in haste (v.11), sandals on feet, staff in hand. The Passover is a meal of departure — Israel was no longer Egypt's people but God's people on the move.
- **Memorial and Covenant Identity**: God immediately institutes the feast as a perpetual ordinance (v.14). Israel's identity would be perpetually shaped by remembering their redemption.

## Hebrew Word Notes
- **פֶּסַח** (pesach, "Passover/pass over," v.13, 23) — The word describes God's protective passing over the marked houses, or perhaps the covering/protecting movement. The feast name derives from this divine action.
- **תָּמִים** (tāmîm, "without blemish/perfect," v.5) — The same word used for moral perfection and wholeness in Leviticus. The lamb must be flawless, pointing to the necessity of a perfect sacrifice.
- **מַצּוֹת** (maṣṣôt, "unleavened bread," v.8) — The absence of leaven (yeast) represented departure in haste but also became associated with the removal of moral corruption (cf. 1 Corinthians 5:7-8).

## How This Chapter Points to Christ
The New Testament makes the connection explicit: "Christ, our Passover lamb, has been sacrificed" (1 Corinthians 5:7). John the Baptist called Jesus "the Lamb of God, who takes away the sin of the world" (John 1:29). The timing of the crucifixion at Passover was not coincidental — Jesus was crucified at the precise season when lambs were being slaughtered throughout Jerusalem. As the blood on the doorposts shielded Israel from judgment, so Christ's blood, applied by faith, shields the believer from the wrath of God. The Passover meal itself became the template for the Lord's Supper (Luke 22:14-20).

## Moral and Spiritual Lessons
- Salvation is by blood, not by merit. The firstborn of Israel were not spared because they were good — they were spared because the blood was on the door.
- Obedience to God's precise instructions matters. God gave specific requirements for the lamb, the blood application, and the meal. Casual compliance would not do.
- God's judgment is real and impartial. No corner of Egypt was untouched — from Pharaoh's household to the prisoner in the dungeon (v.29). This soberness belongs in our understanding of God.
- Redemption calls for a new beginning. God resets Israel's calendar at the Passover (v.2) — it becomes their "first month," the start of sacred time.

## Practical Application
The Lord's Supper is the New Covenant Passover — the meal in which we proclaim the Lord's death until He comes (1 Corinthians 11:26). Celebrate it with the awareness the original participants had: we are under judgment, a Lamb has been slain in our place, and we are people on a journey — not yet home. Let the Passover's urgency shape your spiritual posture: live as those who are traveling, not as those who have settled in Egypt.

## Believers Sword Reflection
Exodus 12 stands as the great type of the cross. Every detail — the lamb, the blood, the haste, the night of death turned into morning of departure — is a shadow of what God accomplished in Christ. Read this chapter and see your own redemption: not earned, not merited, but purchased by blood and applied by faith.""",
        "chapter_overview": "Exodus 12 institutes the Passover — a substitutionary ritual in which the blood of a spotless lamb shields Israel from God's judgment on Egypt's firstborn. The chapter records the tenth plague, Israel's departure after 430 years, and the permanent establishment of the Passover feast as a defining memorial of redemption.",
        "original_language_notes": [
            {
                "term": "pesach",
                "language": "Hebrew",
                "verse": "Exodus 12:13, 23",
                "words_used": "פֶּסַח (pesach) — 'Passover / to pass over / to protect'",
                "meaning": "The root suggests a protective passing over or hovering. When God 'passed over' the marked houses, He was not merely skipping them — He was actively shielding them. The word gave the feast its name and defines God's protective response to applied blood."
            },
            {
                "term": "tāmîm",
                "language": "Hebrew",
                "verse": "Exodus 12:5",
                "words_used": "תָּמִים (tāmîm) — 'without blemish / perfect / complete'",
                "meaning": "Used throughout Leviticus for sacrificial requirements and also for moral wholeness (Genesis 6:9, Job 1:1). The Passover lamb must be physically perfect — a requirement that points toward the moral perfection required of the ultimate sacrifice, Jesus Christ."
            },
            {
                "term": "maṣṣôt",
                "language": "Hebrew",
                "verse": "Exodus 12:8, 15",
                "words_used": "מַצּוֹת (maṣṣôt) — 'unleavened bread'",
                "meaning": "Bread baked without yeast, eaten in haste. Leaven (chametz) later became associated with corruption and sin in both Jewish and NT usage (1 Cor 5:7-8). The removal of leaven from households symbolized purging corruption and departing from the old life."
            }
        ],
        "moral_lessons": [
            "Salvation from divine judgment is by blood alone, not by human merit or moral standing.",
            "God's protective covering is applied by faith-obedience — the blood had to be actively put on the doorposts.",
            "God's judgment is real, comprehensive, and impartial — every house in Egypt was touched.",
            "Redemption creates a new identity and a new calendar — life begins again from the point of deliverance.",
            "God's precise instructions in worship and ritual are not arbitrary but carry deep meaning."
        ],
        "application": "Meditate on the Lord's Supper through the lens of Passover. You were under judgment; a Lamb has been slain; His blood has been applied. Like Israel on that night, you are not yet home — you are traveling, staff in hand. Let this awareness shape how you live: grateful, humble, urgent, and oriented toward a destination that lies beyond Egypt.",
        "prayer": "Lord God, You passed over our judgment because Your own Son became our Passover Lamb. His blood — not our goodness — is our standing before You. Give us gratitude deep enough to change how we live, and faith that rests wholly in the blood of Christ. Help us to live as people who have been delivered, not as those still enslaved. Amen.",
        "key_points": [
            "God institutes the Passover with precise requirements: a spotless lamb, blood on doorposts, eaten in haste.",
            "The blood of the lamb shields the firstborn of Israel — substitutionary death at work.",
            "'When I see the blood, I will pass over you' — salvation is by applied blood, not merit.",
            "The tenth plague strikes every firstborn in Egypt, breaking Pharaoh's resistance.",
            "Israel departs Egypt after exactly 430 years of sojourning.",
            "The Passover is established as a permanent annual memorial.",
            "The Passover is the foundational type of Christ's atoning sacrifice."
        ],
        "study_questions": [
            "How does the requirement for a 'spotless' lamb (v.5) anticipate the character of Jesus Christ as the true Passover Lamb (1 Peter 1:19)?",
            "Why do you think God required the blood to be visibly applied to the doorposts rather than simply trusting that an Israelite lived there?",
            "What does God's resetting of Israel's calendar (v.2) suggest about what redemption does to a person's identity and sense of time?",
            "How does the meal's urgency — sandals on, staff in hand — challenge how you think about your own status as a 'traveler' in this world?",
            "In what ways does the Lord's Supper continue and fulfill the meaning of the Passover meal?"
        ],
        "tags": ["exodus", "passover", "blood", "atonement", "lamb-of-god", "plagues", "deliverance", "lords-supper", "substitution"]
    },
    {
        "chapter": 13,
        "title": "Exodus 13 — Firstborns, Feasts, and the Pillar of God",
        "summary": "Exodus 13 establishes two sacred institutions: the consecration of every firstborn male to the LORD, and the Feast of Unleavened Bread as a seven-day annual remembrance of the Exodus. The chapter also records God's guidance of Israel through the wilderness by a pillar of cloud by day and fire by night — a visible, continuous sign of divine presence and direction.",
        "content": """## What Exodus 13 Is About
Exodus 13 follows the Passover night with two ordinances that are meant to inscribe the memory of redemption into Israel's annual and generational life. The first is the consecration of firstborns (vv. 1-2, 11-16): because God struck down Egypt's firstborn while sparing Israel's, every firstborn male — human and animal — now belongs to God. This is not arbitrary; it is a living memorial of substitutionary grace. The second is the Feast of Unleavened Bread (vv. 3-10): seven days each year, Israel was to eat unleavened bread and explain to their children why: "By strength of hand the LORD brought us out of Egypt" (v.14).

The chapter closes with Israel's departure route and the great sign of God's presence: a pillar of cloud by day and a pillar of fire by night, going before them (vv. 21-22). God does not lead them the short way through Philistine territory but the longer way through the wilderness — a sovereign routing that protects Israel from discouragement and battle before they are ready.

## Theological Themes
- **Consecration as Memorial**: The firstborn consecration is a perpetual, embodied reminder that Israel's firstborns should have died in Egypt. God spared them; therefore they belong to Him. This logic — "you were purchased, you are not your own" — runs through the entire Bible to 1 Corinthians 6:19-20.
- **Generational Transmission of Faith**: The command to explain the feast to children (vv. 8, 14) reveals God's design for faith to be transmitted through story, ritual, and honest conversation. Every generation must understand why Israel is who she is.
- **Divine Guidance**: The pillar of cloud and fire is one of the most tender images of God in the Old Testament — a God who goes before, who does not leave His people to navigate alone, who is visibly present in both day and night.
- **Sovereign Path-Making**: God's redirection away from the Philistine coast (v.17) shows that the shortest path is not always God's path. His routing accounts for what His people can bear.

## Hebrew Word Notes
- **קָדַּשׁ** (qādash, "consecrate/set apart," v.2) — The word means to make holy, to set apart for divine use. The firstborn's consecration marks them as belonging to another — to God — rather than to the family's disposal.
- **זָכַר** (zākar, "remember," v.3) — "Remember this day" is a covenant command. Biblical remembrance is not merely mental recollection but active, shaping commemoration that forms identity.
- **עַמּוּד** (ʿammûd, "pillar," vv. 21-22) — The pillar of cloud/fire is the visible form of God's presence going before Israel. It is a theophany — God making Himself perceptible and directable for His people's sake.

## How This Chapter Points to Christ
The firstborn consecration points to the ultimate Firstborn. Jesus is called "the firstborn over all creation" (Colossians 1:15) and "the firstborn from the dead" (Revelation 1:5). He is consecrated to God absolutely, and in His redemption, He consecrates all who belong to Him. The unleavened bread feast — seven days of purging leaven — is applied by Paul directly to Christian living: "Therefore let us keep the feast, not with old leaven … but with the unleavened bread of sincerity and truth" (1 Corinthians 5:8). Christ is the end and fulfillment of every Mosaic memorial.

## Moral and Spiritual Lessons
- What God has redeemed, He consecrates. You belong to Him not as a burden but as a treasured possession He delivered at great cost.
- Faith must be transmitted deliberately. Israel was commanded to tell their children the story — not assume they would absorb it. The church has the same responsibility.
- God guides through what seems like detours. When life takes you the longer way, consider that God is protecting you from battles you are not yet equipped to fight.
- God's presence is constant — cloud by day, fire by night. There is no season of life when He withdraws completely.

## Practical Application
Ask yourself: Am I transmitting faith or merely practicing it privately? The command to teach children why we do what we do is urgent — the next generation will not inherit faith by osmosis. Also examine what it means that your life is consecrated to God. You are not your own (1 Corinthians 6:19-20). This is not oppressive — it is the most liberating truth imaginable: you do not have to build your own identity, because God has given you one.

## Believers Sword Reflection
Exodus 13 teaches that redemption creates obligation — not to earn salvation but to live in the reality of it. To consecrate what was spared, to remember what was done, to follow where God leads: these are the rhythms of a redeemed life.""",
        "chapter_overview": "Exodus 13 consecrates Israel's firstborns to God as a living memorial of the Passover sparing, establishes the Feast of Unleavened Bread as annual generational remembrance, and records God leading Israel through the wilderness by a pillar of cloud and fire — choosing the longer route for their protection.",
        "original_language_notes": [
            {
                "term": "qādash",
                "language": "Hebrew",
                "verse": "Exodus 13:2",
                "words_used": "קַדֶּשׁ-לִי כָל-בְּכוֹר (qaddesh-lî kol-bekhôr) — 'Consecrate to Me every firstborn'",
                "meaning": "קָדַשׁ means to set apart as holy, to remove from common use for divine purpose. The firstborn's consecration was not a tax but a living declaration that the redeemed belong to their Redeemer."
            },
            {
                "term": "zākar",
                "language": "Hebrew",
                "verse": "Exodus 13:3",
                "words_used": "זָכוֹר אֶת-הַיּוֹם הַזֶּה (zākhôr ʾet-hayyôm hazzeh) — 'Remember this day'",
                "meaning": "Biblical remembrance (zākar) is active and formative — it reshapes behavior and identity, not merely recalling a fact. The feast was designed to make Israel who they are by re-enacting what God did."
            },
            {
                "term": "ʿammûd",
                "language": "Hebrew",
                "verse": "Exodus 13:21-22",
                "words_used": "עַמּוּד עָנָן / עַמּוּד אֵשׁ (ʿammûd ʿānān / ʿammûd ʾēsh) — 'pillar of cloud / pillar of fire'",
                "meaning": "The pillar (ʿammûd, a standing column) is a theophanic form — God making Himself directionally visible to lead Israel. Its continuous presence (never departing, v.22) signals that God's guidance is constant, not occasional."
            }
        ],
        "moral_lessons": [
            "Those whom God redeems are consecrated to Him — we belong to our Redeemer.",
            "Intentional transmission of faith to the next generation is a divine command, not optional.",
            "God's routing through life takes into account what His people can bear, even when it seems longer.",
            "God's guidance is constant — He does not leave His people to navigate alone in any season."
        ],
        "application": "Examine whether you are actively transmitting faith to those in your sphere of influence — especially children. Practice the discipline of telling your story of redemption: what God brought you out of, and why you live the way you do. Also, the next time God seems to be leading you the 'long way,' resist the impulse to find shortcuts. Ask what He may be sparing you from.",
        "prayer": "Lord, You have redeemed us and made us Your own. Teach us to live consecrated lives — set apart for Your use, not just in title but in practice. Guide us through cloud and fire, and give us the courage to follow even when Your path is longer than we expected. Help us tell Your story to those who come after us. Amen.",
        "key_points": [
            "Every firstborn male is consecrated to God because He spared Israel's firstborn in Egypt.",
            "The Feast of Unleavened Bread is established as a seven-day annual memorial of the Exodus.",
            "Parents are commanded to explain the meaning of these memorials to their children.",
            "God leads Israel the longer way through the wilderness to protect them from premature war.",
            "A pillar of cloud by day and fire by night represents God's continuous guiding presence.",
            "The chapter links consecration, memory, and guidance as pillars of covenant life."
        ],
        "study_questions": [
            "What is the logic behind consecrating the firstborn to God as a response to the Passover? How does this apply to Christian living today (cf. 1 Corinthians 6:19-20)?",
            "Why do you think God places such strong emphasis on parents explaining these feasts to their children? What happens to a community when this transmission breaks down?",
            "What does God's choice to take Israel the longer route tell you about how He leads us today?",
            "How is the pillar of cloud and fire a picture of God's relationship to His people — both protective and directional?",
            "Paul applies unleavened bread to Christian ethics in 1 Corinthians 5:7-8. What 'leaven' might God be calling you to purge from your life?"
        ],
        "tags": ["exodus", "firstborn", "consecration", "unleavened-bread", "pillar-of-cloud", "guidance", "memory", "generational-faith", "presence-of-god"]
    },
    {
        "chapter": 14,
        "title": "Exodus 14 — Through the Sea: God Fights for His People",
        "summary": "Exodus 14 records the crossing of the Red Sea — the defining miracle of the Old Testament. With Pharaoh's army closing behind them and the sea before them, Israel cried out in fear. God commanded Moses to stretch out his staff, and the sea parted. Israel crossed on dry ground while the pursuing Egyptians were engulfed. When Israel saw the great power of God, they feared the LORD and believed in Him and in Moses His servant.",
        "content": """## What Exodus 14 Is About
Exodus 14 is the climax of the Exodus narrative. After departing Egypt, Israel finds itself in an apparently impossible situation: the sea in front, mountains or desert on the sides, and Pharaoh's elite chariot force bearing down from behind. God had led them here deliberately (vv. 1-4) — the apparent trap is a stage God set for His own glory.

The chapter moves through fear (vv. 10-12), divine reassurance (vv. 13-14), miraculous action (vv. 15-22), the Egyptian pursuit (vv. 23-25), and the sea's return (vv. 26-29). It closes with one of the most theologically resonant statements in the Torah: Israel "feared the LORD and believed in His servant Moses" (v.31).

Central to the chapter is Moses's declaration in verse 14: "The LORD will fight for you; you need only to be still." This is not passivity but trust — a restful confidence in God's ability and willingness to act on behalf of those who cannot save themselves.

## Theological Themes
- **Divine Initiative in Salvation**: Israel does not fight their way through. They walk through on dry ground while God fights. Salvation is God's work, not a collaboration between human effort and divine assistance.
- **God's Glory Through Impossible Circumstances**: God explicitly says He will get glory through Pharaoh (v.4, 17). He positions His people in impossibility so that the rescue is unambiguously His.
- **Faith Born from Witness**: The chapter ends with Israel believing (v.31) — not because they reasoned their way to faith but because they witnessed God's power. Faith is anchored in what God actually does in history.
- **Hardening of Pharaoh**: God hardens Pharaoh's heart (vv. 4, 8, 17) — not mechanically overriding a neutral will, but confirming and accelerating the direction Pharaoh had already chosen.

## Hebrew Word Notes
- **יָשַׁע** (yāshaʿ, "save/deliver," v.13) — "Stand still and see the salvation of the LORD." This is the root of the name Yeshua (Jesus). At the sea, God's salvation (yĕshuʿāh) is utterly His own act.
- **יָרֵא** (yārēʾ, "feared/revered," v.31) — "Israel saw … and feared the LORD." The same word used of the midwives in chapter 1. Fear here is not terror but the reverent awe that sees God's power and submits to His majesty.
- **חָזַק** (ḥāzaq, "strengthen/harden," vv. 4, 8) — The verb used for Pharaoh's hardened heart. It means to make firm or strong. God's hardening of Pharaoh confirms a trajectory already set in motion by Pharaoh's own repeated defiance.

## How This Chapter Points to Christ
Paul explicitly interprets the Red Sea crossing as a baptism: "all were baptized into Moses in the cloud and in the sea" (1 Corinthians 10:1-2). As Israel passed through water from slavery to freedom, believers pass through the waters of baptism from death to new life. The armies of Pharaoh drowned in the sea just as the power of sin is broken in Christ's death. Jesus's death and resurrection is the greater Exodus — the true crossing from bondage to freedom, from death to life.

## Moral and Spiritual Lessons
- When you are cornered with no human exit, God's word to you is the same as to Israel: "The LORD will fight for you; be still" (v.14). Stillness before God is not resignation — it is faith.
- The most impossible circumstances are often the stage God has chosen to display His power most clearly.
- Deliverance witnessed produces faith. When God acts, take note — record it, tell it, return to it when the next crisis comes.
- Pharaoh's pursuit even after devastating plagues shows that hardened hearts do not learn from partial consequences — they must be finally broken.

## Practical Application
Identify a situation in your life where you feel "hemmed in" — the sea before you, the army behind. Resist the instinct to scheme your way out. Instead, practice the discipline of stillness before God: acknowledge His power, confess your helplessness, and ask Him to fight. Then step forward in obedience to what He has said, trusting that the sea will part at His command — not before you step.

## Believers Sword Reflection
Exodus 14 is the Old Testament's most dramatic picture of salvation by grace: God does it all, the enemy is defeated, His people walk on dry ground. Nothing they contributed made it possible. This is the grammar of the gospel — and the Red Sea is God's own object lesson.""",
        "chapter_overview": "Exodus 14 records the crossing of the Red Sea, where Israel — trapped between the sea and Pharaoh's army — witnesses God part the waters, lead them through on dry ground, and destroy the pursuing Egyptians. The chapter ends with Israel fearing and believing God, establishing the sea crossing as the definitive Old Testament image of divine salvation.",
        "original_language_notes": [
            {
                "term": "yĕshuʿāh",
                "language": "Hebrew",
                "verse": "Exodus 14:13",
                "words_used": "יְשׁוּעַת יְהוָה (yĕshuʿat YHWH) — 'the salvation of the LORD'",
                "meaning": "From the root יָשַׁע (yāshaʿ), the same root as the name Yeshua/Jesus. At the sea, God's yĕshuʿāh is entirely His own act — Israel contributes nothing to their rescue. This word previews the ultimate salvation God would accomplish in Christ."
            },
            {
                "term": "yārēʾ",
                "language": "Hebrew",
                "verse": "Exodus 14:31",
                "words_used": "וַיִּירְאוּ הָעָם אֶת-יְהוָה (wayyîrĕʾû hāʿām ʾet-YHWH) — 'the people feared the LORD'",
                "meaning": "The same verb used for the midwives' godly fear in chapter 1. Here it describes the awe that grips Israel when they see God's power at the sea — reverent submission born from witnessed power. This fear produces belief (emunah)."
            },
            {
                "term": "ḥāzaq",
                "language": "Hebrew",
                "verse": "Exodus 14:4, 8",
                "words_used": "וַאֲחַזֵּק אֶת-לֵב פַּרְעֹה (waʾăḥazzēq ʾet-lēb parʿōh) — 'I will harden Pharaoh's heart'",
                "meaning": "ḥāzaq means to make firm, strong, or hard. God's hardening of Pharaoh is judicial confirmation of a will already set against God — accelerating the direction Pharaoh chose, so that God's glory is displayed in Pharaoh's ultimate defeat."
            }
        ],
        "moral_lessons": [
            "God positions His people in impossible situations precisely so that the rescue is unmistakably His.",
            "True faith sometimes means standing still and watching God fight — not scheming or panicking.",
            "Witnessing God act in history is a foundation for faith — record His deeds and return to them.",
            "God's glory is the goal of history, including the defeat of those who oppose Him.",
            "Hardened hearts do not respond to partial consequences — only final judgment breaks them."
        ],
        "application": "When you face a situation where all human solutions have failed — practice the discipline of Exodus 14:14. Write down what seems impossible. Confess you cannot fix it. Ask God to fight. Then move forward in whatever small obedience He has given you, trusting that He parts seas for those who trust Him. After He acts, write it down — so that your future self has evidence for faith.",
        "prayer": "LORD, You fought for Israel when they had nothing left but You. Teach me to stand still when I have exhausted my own resources — not in defeat but in trust. Fight my battles that are too large for me. Remind me of every Red Sea You have already parted in my life. Let the record of Your faithfulness be my foundation for faith in what lies ahead. Amen.",
        "key_points": [
            "God deliberately leads Israel to the sea to set a stage for His glory.",
            "Israel panics when they see Pharaoh's army; Moses calls them to stand still and watch.",
            "'The LORD will fight for you; you need only be still' — one of Scripture's great declarations of faith.",
            "God parts the Red Sea through Moses's staff; Israel crosses on dry ground.",
            "The Egyptian army pursues and is destroyed when the waters return.",
            "The chapter ends with Israel fearing the LORD and believing in Moses.",
            "The sea crossing is the definitive OT type of salvation and is interpreted as baptism in the NT."
        ],
        "study_questions": [
            "Why do you think God deliberately led Israel into what looked like a trap (vv. 1-4)? What does this tell you about how God orchestrates difficult circumstances?",
            "What is the difference between the 'stillness' Moses commands in verse 14 and passive fatalism? How do you practice this kind of trust?",
            "Paul calls the sea crossing a 'baptism' in 1 Corinthians 10. What does this connection teach about what baptism means?",
            "How does Israel's terror in verses 10-12 — despite just witnessing the ten plagues — speak to the nature of faith and human weakness?",
            "Where in your life do you need to apply the truth of verse 14 right now?"
        ],
        "tags": ["exodus", "red-sea", "miracles", "faith", "salvation", "pharaoh", "divine-warfare", "baptism", "trust"]
    },
    {
        "chapter": 15,
        "title": "Exodus 15 — The Song of Moses: Praise After Deliverance, Trial After Victory",
        "summary": "Exodus 15 opens with the Song of Moses — Israel's great hymn of praise after the Red Sea crossing, celebrating God's power and salvation. The second half records a swift reversal: Israel reaches Marah and finds the water bitter, immediately grumbling against Moses. God shows Moses a piece of wood that sweetens the water and uses the moment to teach Israel about trust and obedience, ending with the promise that He is the LORD their healer.",
        "content": """## What Exodus 15 Is About
Exodus 15 has two very different sections, and their juxtaposition is deliberate. The first (vv. 1-21) is one of the oldest and most exalted pieces of Hebrew poetry in the Bible — the Song of Moses, also called the Song of the Sea. Israel sings praise to God with full hearts after witnessing His power at the Red Sea. The song celebrates God's warrior strength, His incomparability, His judgment on Egypt, and His plan to bring Israel into His holy dwelling.

Then, only three days after the crossing (v.22), Israel enters the wilderness of Shur, travels without water, and reaches Marah — but the water is bitter and undrinkable. Immediately the people grumble against Moses. God shows Moses a piece of wood; Moses throws it in the water and it becomes sweet. Then God speaks a word of covenant: if Israel will listen and obey, He will not put on them the diseases He put on Egypt — "for I am the LORD your healer" (v.26).

## Theological Themes
- **Praise as the Proper Response to Salvation**: The Song of Moses models that salvation should move the redeemed to worship. The same event (the sea crossing) gives birth to both exodus and song.
- **The Brevity of Spiritual Highs and the Normalcy of Testing**: Three days after the greatest miracle in Israel's history, they are grumbling at a water source. This is the pattern of human spiritual experience — not a sign of catastrophic failure but of the need for ongoing trust.
- **The Wood That Heals**: The piece of wood that transforms bitter water into sweet water is one of the most evocative typological images in Exodus. Early church interpreters saw in it a foreshadowing of the cross.
- **God as Healer (Rāphāʾ)**: The revelation of God as YHWH-Rāphāʾ ("the LORD who heals") is the chapter's theological destination. Healing is not primarily physical here — it is the covenant promise that God will not deal with His people as He dealt with Egypt.

## Hebrew Word Notes
- **שִׁיר** (shîr, "song," v.1) — The word for song is also used of the greatest poems in Israel's canon (the Song of Songs, Psalms). The shîr is not casual praise but exalted, composed worship — testimony shaped into art.
- **גָּאָה גָאָה** (gāʾāh gāʾāh, "highly exalted," v.1) — A doubled form for emphasis: "He has triumphed gloriously." The doubling intensifies the greatness of God's victory and is a feature of biblical hymnic poetry.
- **רָפָא** (rāphāʾ, "heal," v.26) — The root of YHWH-Rōphēʾkhā ("I am the LORD your healer"). The word covers physical healing but extends to restoration, remedy, and making whole — God's comprehensive care for His people.

## How This Chapter Points to Christ
The Song of Moses reappears in Revelation 15:3-4, where the saints who have triumphed over the Beast sing "the song of Moses … and the song of the Lamb" — the two great deliverances of God's people united in final praise. The wood thrown into the bitter water is a profound type of the cross: the instrument of death and curse (Galatians 3:13 — "Cursed is everyone who hangs on a tree") becomes the source of healing and life. Christ on the cross transforms the bitterness of sin and death into the sweetness of forgiveness and new life.

## Moral and Spiritual Lessons
- Praise after deliverance is not just appropriate — it is the trained reflex of a grateful soul. The Song of Moses shows what a community shaped by God's saving acts looks like.
- Spiritual highs do not inoculate against immediate trials. Israel's rapid transition from song to grumbling is not unusual — it is human. The lesson is that faith must be cultivated daily, not coasted on.
- Grumbling reveals what we truly trust. When comfort disappears, what comes out of us? Israel's grumbling was really a question about God's faithfulness.
- God uses bitter experiences to test what is in our hearts (v.25). The bitterness of Marah is not punishment — it is curriculum.

## Practical Application
Make a practice of celebrating what God has done — write it down, sing it, tell it to others. The Song of Moses was corporate and composed; spontaneous private gratitude is good, but shaped, shared praise is also a biblical discipline. When the Marah moments come — and they will, often soon after the Red Sea moments — remember that the same God who parted the sea has not forgotten you. Ask Him to show you the piece of wood that makes bitter water sweet.

## Believers Sword Reflection
Exodus 15 tells us that the life of faith is not a steady ascent from victory to victory — it moves between song and suffering, between Elim (the oasis at the end of the chapter) and Marah. God's purpose in both is the same: to be known as the God who heals, who provides, who transforms bitter things into sweet.""",
        "chapter_overview": "Exodus 15 records the Song of Moses — Israel's triumphant hymn of praise after the Red Sea — followed immediately by the trial at Marah where bitter water causes grumbling. God sweetens the water through a piece of wood and reveals Himself as YHWH-Rāphāʾ, the LORD their healer, binding the promise of healing to Israel's covenant obedience.",
        "original_language_notes": [
            {
                "term": "gāʾāh",
                "language": "Hebrew",
                "verse": "Exodus 15:1",
                "words_used": "גָּאֹה גָּאָה (gāʾōh gāʾāh) — 'He has triumphed gloriously / highly exalted'",
                "meaning": "A doubled infinitive absolute for emphatic intensification — literally 'rising He has risen.' A signature of Hebrew hymnic poetry, the doubling celebrates the unqualified greatness of God's victory over Pharaoh."
            },
            {
                "term": "rāphāʾ",
                "language": "Hebrew",
                "verse": "Exodus 15:26",
                "words_used": "יְהוָה רֹפְאֶךָ (YHWH rōphĕkhā) — 'the LORD your healer / I am YHWH who heals you'",
                "meaning": "רָפָא (rāphāʾ) covers physical restoration but also moral and covenant restoration — making whole what is broken. This is the first revelation of YHWH by this name, and it links God's healing directly to covenant obedience."
            },
            {
                "term": "mārar",
                "language": "Hebrew",
                "verse": "Exodus 15:23",
                "words_used": "כִּי מָרִים הֵם (kî mārîm hēm) — 'for they [the waters] were bitter'",
                "meaning": "From מָרַר (mārar), 'to be bitter.' The same root gives the place its name Marah and also describes Naomi's bitterness in Ruth 1:20. Bitterness is a recurring biblical motif for the painful, ungovernable circumstances that test trust in God."
            }
        ],
        "moral_lessons": [
            "Salvation should produce praise — the trained reflex of the redeemed is worship, not just relief.",
            "Spiritual victories do not prevent immediate trials — faith must be practiced daily, not coasted on.",
            "Grumbling reveals what we truly believe about God's faithfulness and character.",
            "Bitter circumstances are often God's curriculum for learning to trust Him more deeply.",
            "God transforms bitter things into sweet through means that seem unlikely — the cross is the ultimate example."
        ],
        "application": "Start a practice of recording your 'Red Sea' moments — the times God acted decisively for you. When the Marah moments come (bitter water, unmet expectations, immediate reversals after victories), return to the record. Then ask God: What is the piece of wood here? What cross-shaped instrument has He provided to transform this bitterness? Often, it is the word of God itself — bitter to the flesh, sweet to the soul.",
        "prayer": "Lord, You are the God who triumphs gloriously and who heals. Teach us to sing before we move on, so the song of Your salvation is deep in us when bitter water comes. And when bitterness comes — as it will — show us the wood that transforms it. You are YHWH-Rāphāʾ. We trust You to make us whole. Amen.",
        "key_points": [
            "The Song of Moses is Israel's great hymn of praise after the Red Sea, celebrating God's warrior power.",
            "The song declares God as incomparable: 'Who is like You among the gods, O LORD?'",
            "Only three days after the sea crossing, Israel reaches bitter water at Marah and grumbles.",
            "God shows Moses a piece of wood that sweetens the bitter water — a type of the cross.",
            "God reveals Himself as YHWH-Rāphāʾ: 'I am the LORD your healer.'",
            "The chapter ends at Elim, an oasis with twelve springs and seventy palm trees — a place of rest.",
            "The Song of Moses reappears in Revelation 15 as the song of final victory."
        ],
        "study_questions": [
            "What does the Song of Moses teach us about the role of poetry and music in expressing faith? Why might prose be insufficient for some encounters with God?",
            "How do you explain Israel's rapid shift from exultant praise to bitter grumbling in just three days? Does this encourage or discourage you, and why?",
            "What does the wood that sweetens bitter water suggest to you about God's methods of provision? How might this point to the cross?",
            "The revelation 'I am the LORD your healer' comes in the context of obedience (v.26). What is the relationship between obedience and experiencing God's healing in your own life?",
            "Revelation 15:3 quotes the Song of Moses in the context of final judgment. How does knowing this song will be sung at the end of history change how you read it now?"
        ],
        "tags": ["exodus", "song-of-moses", "praise", "worship", "marah", "bitter-water", "yhwh-rapha", "healing", "cross", "testing", "faith"]
    },
    {
        "chapter": 16,
        "title": "Exodus 16 — Bread from Heaven: Manna, Quail, and the Sabbath",
        "summary": "Exodus 16 records God's provision of manna and quail to the grumbling Israelites in the Sinai wilderness. Each morning, fine flakes of bread appeared on the ground; each evening, quail came in abundance. The manna came with instructions designed to teach dependence on God: gather only what you need, gather double on the sixth day, rest on the seventh. Those who hoarded found it rotted. The chapter establishes the Sabbath principle through the rhythm of manna collection.",
        "content": """## What Exodus 16 Is About
Exodus 16 is a chapter about daily dependence and the spiritual disease of grumbling. One month into the wilderness journey, Israel confronts hunger and immediately looks backward to Egypt with nostalgia: "We sat by meat pots and ate bread to the full" (v.3). The irony is that they remember Egypt through the filter of hunger — forgetting the slavery, the infanticide, and the bitterness that made them cry out to God in the first place.

God responds to the grumbling with grace, not punishment. He promises bread from heaven every morning and meat every evening. The manna ("What is it?" — the word itself is a question) arrives daily, except on the Sabbath. The instructions around manna gathering are pedagogical: the daily portion cannot be hoarded (it rots if kept overnight on regular days), double must be gathered on the sixth day for the Sabbath, and on the seventh day there is none — rest is built into the provision.

The chapter ends with God commanding that a jar of manna be kept as a memorial "before the Testimony" — a permanent reminder of how God fed His people in the wilderness.

## Theological Themes
- **Grace in Response to Grumbling**: Israel's grumbling earns them bread, not judgment. God hears the complaint not as righteous petition but as faithlessness — yet He feeds them anyway. This is not because grumbling is acceptable but because God's faithfulness transcends Israel's unfaithfulness.
- **Daily Dependence as Spiritual Formation**: The manna could not be stored. This was intentional — God wanted Israel to come back every morning, to practice the discipline of daily dependence. The Lord's Prayer ("give us this day our daily bread") echoes this very structure.
- **The Sabbath Embedded in Provision**: Long before Sinai's explicit command, the manna establishes a six-day work and one-day rest rhythm. The Sabbath is not merely a law to observe but a pattern built into creation and redemption.
- **Testing Through Provision**: Verse 4 is striking: God gives manna explicitly as a test — "that I may test them, whether they will walk in My law or not." Obedience to simple instructions is the measure of deeper loyalty.

## Hebrew Word Notes
- **מָן** (mān, "manna / what is it?," v.15) — When Israel saw the substance, they said מָן הוּא (mān hûʾ) — "What is it?" The word manna likely derives from this puzzled question, making the name itself a record of Israel's incomprehension before God's provision.
- **לֶחֶם** (leḥem, "bread / food," v.4) — "I will rain bread from heaven." This is the ordinary word for bread and food, used throughout the OT. Calling manna "bread from heaven" (leḥem min-hashshāmayim) is the language Jesus applies to Himself in John 6.
- **שַׁבָּת** (shabbāt, "Sabbath / rest," v.23) — First explicit use of this word in Scripture (though the concept is in Genesis 2:2-3). The Sabbath here is established not by law but by provision — the manna simply does not come on the seventh day.

## How This Chapter Points to Christ
Jesus explicitly identifies Himself as the true manna from heaven: "I am the bread of life. Your fathers ate the manna in the wilderness, and they died. This is the bread that comes down from heaven, so that one may eat of it and not die" (John 6:48-50). The manna sustained physical life temporarily; Christ sustains eternal life permanently. As Israel needed to gather manna daily, we need daily communion with Christ — through prayer, Scripture, and trust. The manna that did not rot when kept in the jar before the Testimony points to Christ's imperishable resurrection life.

## Moral and Spiritual Lessons
- Grumbling often involves selective memory — Israel romanticized Egypt because they were hungry. Beware of nostalgia for what God delivered you from.
- God provides enough for today. The impulse to hoard is a failure of trust — it says "I don't believe God will provide tomorrow."
- Rest is built into God's design. The Sabbath rhythm is not a religious imposition but a creaturely necessity woven into the structure of provision.
- Obedience to simple instructions reveals the state of the heart. Those who hoarded on regular days found rot. Those who gathered double on Friday found it fresh Saturday. God sees our trust in the small things.

## Practical Application
Practice the discipline of daily reliance. Take time each morning to acknowledge that what you need for today — wisdom, strength, grace, provision — must come from God, not from reserves you stockpiled yesterday. The manna principle challenges the self-sufficiency that wants to live this week on what God gave last month. It also invites you to guard the Sabbath not merely as rule-keeping but as a confessional act: one day a week you stop, and your stopping says "I am not the engine of my own life."

## Believers Sword Reflection
Exodus 16 is one of the great chapters on the spiritual discipline of dependence. The manna teaches what the wilderness was designed to teach: that man does not live by bread alone, but by every word that proceeds from the mouth of God (Deuteronomy 8:3 — and cited by Jesus in His own wilderness testing in Matthew 4:4). Every morning of manna was a lesson in that truth.""",
        "chapter_overview": "Exodus 16 records God's miraculous provision of manna and quail to grumbling Israel in the wilderness, with instructions designed to teach daily dependence and Sabbath rest. The manna system — gather only what you need daily, double on the sixth day, rest on the seventh — is a school of trust that the Lord's Prayer and Jesus's 'I am the bread of life' both echo.",
        "original_language_notes": [
            {
                "term": "mān",
                "language": "Hebrew",
                "verse": "Exodus 16:15",
                "words_used": "מָן הוּא (mān hûʾ) — 'What is it?'",
                "meaning": "The puzzled question the Israelites asked when they first saw the substance became the name of the food itself — manna. The name embeds Israel's incomprehension before God's provision, and perhaps deliberately so: what God provides often defies our categories."
            },
            {
                "term": "leḥem min-hashshāmayim",
                "language": "Hebrew",
                "verse": "Exodus 16:4",
                "words_used": "לֶחֶם מִן-הַשָּׁמַיִם (leḥem min-hashshāmayim) — 'bread from heaven'",
                "meaning": "Ordinary word leḥem (bread/food) combined with 'from the heavens.' This phrase becomes Jesus's self-description in John 6:32-35 — He is the true bread from heaven that gives eternal life, of which the manna was a temporary type."
            },
            {
                "term": "shabbāt",
                "language": "Hebrew",
                "verse": "Exodus 16:23",
                "words_used": "שַׁבַּת-קֹדֶשׁ לַיהוָה (shabbat-qōdesh laYHWH) — 'a holy Sabbath to the LORD'",
                "meaning": "First explicit use of shabbāt (from shābat, 'to cease/rest') in Scripture outside Genesis 2. Its introduction through manna provision — not law — shows that Sabbath rest is embedded in God's pattern of provision before it becomes a legal requirement at Sinai."
            }
        ],
        "moral_lessons": [
            "Grumbling often involves selective memory and romanticized nostalgia for what God delivered us from.",
            "God's provision is for today — hoarding is a spiritual failure, not prudent planning.",
            "Daily dependence on God is not weakness but the proper posture of a creature before the Creator.",
            "Sabbath rest is a confessional act: stopping says we are not the engine of our own lives.",
            "Obedience in small, simple instructions reveals the true state of the heart toward God."
        ],
        "application": "Try a week of intentional daily dependence prayer — each morning, acknowledge that what you need today (wisdom, strength, provision, grace) must come fresh from God. Notice what changes in your anxiety level and your sense of trust. Also examine your Sabbath practice: is there a day each week where you stop, genuinely rest, and confess by your rest that God is your sustainer?",
        "prayer": "Father, You rained bread from heaven for a grumbling people. You are more faithful than we deserve. Teach us to come to You each morning, empty-handed, trusting that You will provide what we need for this day. Break us of the hoard-instinct, the self-sufficiency that pretends we don't need You daily. You are our bread. Jesus is our manna. We receive Him fresh today. Amen.",
        "key_points": [
            "Israel grumbles about hunger, longing for Egypt — a failure of memory and trust.",
            "God provides manna each morning and quail each evening as daily supernatural provision.",
            "The manna instructions are pedagogical: gather only what you need, no hoarding, double on the sixth day.",
            "Those who disobeyed and hoarded found the manna rotted and infested with worms.",
            "The Sabbath principle is embedded in the manna rhythm before Sinai's explicit law.",
            "Jesus calls Himself the true bread from heaven in John 6, explicitly connecting to this chapter.",
            "A jar of manna is preserved as a memorial before the Ark of the Covenant."
        ],
        "study_questions": [
            "Why do you think Israel remembered Egypt so fondly when they had been slaves there? What does selective nostalgia reveal about how we handle hardship?",
            "What is the spiritual significance of manna that could not be stored (it rotted overnight on regular days)? How does this challenge modern approaches to security and self-sufficiency?",
            "The Sabbath emerges through manna provision before it is commanded at Sinai. What does this tell you about the nature of the Sabbath — is it a law or a rhythm?",
            "Jesus quotes Deuteronomy 8:3 ('man shall not live by bread alone') in His wilderness testing, which refers back to Exodus 16. What was He claiming about His own dependence on the Father?",
            "In what areas of your life are you trying to live on yesterday's provision instead of seeking fresh daily dependence on God?"
        ],
        "tags": ["exodus", "manna", "quail", "bread-from-heaven", "sabbath", "dependence", "grumbling", "provision", "daily-bread", "jesus-bread-of-life"]
    }
]


def get_or_create_collection(conn):
    cur = conn.cursor()
    cur.execute("SELECT id FROM commentary_collections WHERE slug='believers-sword-commentaries'")
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("""
        INSERT INTO commentary_collections (uuid, name, slug, description, collection_type, is_public, language_code, theological_perspective, license_info, notes, is_active, sync_status)
        VALUES (?, 'Believers Sword Commentaries', 'believers-sword-commentaries', 'Practical, reverent, evangelical Christian chapter commentaries for Believers Sword offline study.', 'ai_generated', 1, 'en', 'Evangelical Christian', 'All rights reserved for project use.', 'Generated for Believers Sword.', 1, 'local')
    """, (str(uuid.uuid4()),))
    conn.commit()
    return cur.lastrowid


def entry_exists(conn, collection_id, book_id, chapter):
    cur = conn.cursor()
    cur.execute("""
        SELECT id, content FROM commentary_entries
        WHERE collection_id=? AND book_id=? AND chapter=? AND language_code='en' AND reference_scope='chapter' AND deleted_at IS NULL
    """, (collection_id, book_id, chapter))
    row = cur.fetchone()
    if row:
        content = row[1] or ""
        if len(content) > 200:
            return True, row[0]
        return False, row[0]
    return False, None


def insert_entry(conn, collection_id, chapter_data):
    cur = conn.cursor()
    entry_uuid = str(uuid.uuid4())
    ch = chapter_data
    key_points_json = json.dumps(ch["key_points"])
    study_questions_json = json.dumps(ch["study_questions"])

    cur.execute("""
        INSERT INTO commentary_entries
        (uuid, collection_id, book_id, chapter, verse_start, verse_end, reference_scope, title, summary, content,
         application, prayer, key_points, study_questions, language_code, theological_perspective, status,
         is_ai_generated, ai_model_name, word_count, sync_status, created_at, updated_at)
        VALUES (?,?,?,?,NULL,NULL,'chapter',?,?,?,?,?,?,?,'en','Evangelical Christian','draft',1,'claude-sonnet-4-6',?,  'local',?,?)
    """, (
        entry_uuid, collection_id, BOOK_ID, ch["chapter"],
        ch["title"], ch["summary"], ch["content"],
        ch["application"], ch["prayer"],
        key_points_json, study_questions_json,
        len(ch["content"].split()),
        NOW, NOW
    ))
    conn.commit()
    return entry_uuid


def save_json(chapter_data, entry_uuid):
    dir_path = os.path.join(GENERATED_DIR, BOOK_SLUG)
    os.makedirs(dir_path, exist_ok=True)
    filename = f"{chapter_data['chapter']:02d}.json"
    filepath = os.path.join(dir_path, filename)

    out = {
        "uuid": entry_uuid,
        "collection_name": COLLECTION_NAME,
        "author_type": "organization",
        "language_code": "en",
        "theological_perspective": "Evangelical Christian",
        "status": "draft",
        "book_id": BOOK_ID,
        "book": BOOK_NAME,
        "chapter": chapter_data["chapter"],
        "title": chapter_data["title"],
        "summary": chapter_data["summary"],
        "content": chapter_data["content"],
        "chapter_overview": chapter_data["chapter_overview"],
        "original_language_notes": chapter_data["original_language_notes"],
        "moral_lessons": chapter_data["moral_lessons"],
        "application": chapter_data["application"],
        "prayer": chapter_data["prayer"],
        "key_points": chapter_data["key_points"],
        "study_questions": chapter_data["study_questions"],
        "tags": chapter_data["tags"],
        "sources": [],
        "created_at": NOW,
        "updated_at": NOW
    }

    # Verify no forbidden keys
    forbidden = {"is_ai_generated", "model_name", "prompt_version"}
    assert not forbidden.intersection(out.keys()), f"Forbidden key found in JSON output: {forbidden.intersection(out.keys())}"

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    # Verify it parses back cleanly
    with open(filepath, "r", encoding="utf-8") as f:
        parsed = json.load(f)
    assert not forbidden.intersection(parsed.keys()), "Forbidden key in parsed JSON"

    return filepath


def update_progress(conn, last_chapter):
    # Determine next
    if last_chapter < 40:
        next_chapter = last_chapter + 1
        next_book = "Exodus"
        next_book_id = 2
        completed = False
    else:
        next_chapter = 1
        next_book = "Leviticus"
        next_book_id = 3
        completed = False

    progress = {
        "next_book_id": next_book_id,
        "next_book": next_book,
        "next_chapter": next_chapter,
        "last_completed_book_id": BOOK_ID,
        "last_completed_book": BOOK_NAME,
        "last_completed_chapter": last_chapter,
        "completed": completed,
        "updated_at": NOW
    }

    with open(PROGRESS_JSON, "w") as f:
        json.dump(progress, f, indent=2)

    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO commentary_generation_progress
        (id, next_book_id, next_book, next_chapter, last_completed_book_id, last_completed_book, last_completed_chapter, completed, updated_at)
        VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (next_book_id, next_book, next_chapter, BOOK_ID, BOOK_NAME, last_chapter, 0 if not completed else 1, NOW))
    conn.commit()
    return progress


def write_log(start_ref, end_ref, generated, skipped, inserted, files):
    log_entry = {
        "timestamp": NOW,
        "generation_batch_id": BATCH_UUID,
        "start_reference": start_ref,
        "end_reference": end_ref,
        "chapters_generated": generated,
        "chapters_skipped": skipped,
        "db_rows_inserted": inserted,
        "files_written": files
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")


def main():
    conn = sqlite3.connect(DB_PATH)
    collection_id = get_or_create_collection(conn)

    chapters_generated = 0
    chapters_skipped = 0
    db_rows_inserted = 0
    files_written = []
    last_chapter = None

    for chapter_data in CHAPTERS:
        ch_num = chapter_data["chapter"]
        exists, existing_id = entry_exists(conn, collection_id, BOOK_ID, ch_num)

        if exists:
            print(f"SKIP: {BOOK_NAME} {ch_num} — already exists (id={existing_id})")
            chapters_skipped += 1
            last_chapter = ch_num
            continue

        print(f"GENERATING: {BOOK_NAME} {ch_num} — {chapter_data['title']}")

        entry_uuid = insert_entry(conn, collection_id, chapter_data)
        filepath = save_json(chapter_data, entry_uuid)

        db_rows_inserted += 1
        files_written.append(filepath)
        chapters_generated += 1
        last_chapter = ch_num
        print(f"  -> DB inserted uuid={entry_uuid}")
        print(f"  -> JSON written: {filepath}")

    if last_chapter:
        progress = update_progress(conn, last_chapter)
        print(f"\nProgress updated: next={progress['next_book']} {progress['next_chapter']}")

    start_ref = f"{BOOK_NAME} {CHAPTERS[0]['chapter']}"
    end_ref = f"{BOOK_NAME} {CHAPTERS[-1]['chapter']}"
    write_log(start_ref, end_ref, chapters_generated, chapters_skipped, db_rows_inserted, files_written)

    conn.close()

    print(f"\n=== SUMMARY ===")
    print(f"Generated: {chapters_generated} | Skipped: {chapters_skipped}")
    print(f"DB rows inserted: {db_rows_inserted}")
    print(f"Files written: {len(files_written)}")
    for f in files_written:
        print(f"  {f}")
    next_book = progress["next_book"] if last_chapter else "Unknown"
    next_ch = progress["next_chapter"] if last_chapter else "?"
    print(f"Next starting reference: {next_book} {next_ch}")


if __name__ == "__main__":
    main()
