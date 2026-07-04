#!/usr/bin/env python3
"""Generate Believers Sword Commentaries: Exodus 27-31."""

import json
import os
import sqlite3
import uuid
from datetime import datetime, timezone

DB_PATH = "/mnt/d/Projects/Personal/Believers-Sword/Modules Turso/Commentaries/Believers Sword/believers_sword_commentaries.db"
PROGRESS_JSON = "/mnt/d/Projects/Personal/Believers-Sword/Modules Turso/Commentaries/Believers Sword/commentary_generation_progress.json"
LOG_JSONL = "/mnt/d/Projects/Personal/Believers-Sword/Modules Turso/Commentaries/Believers Sword/commentary_generation_log.jsonl"
GENERATED_DIR = "/mnt/d/Projects/Personal/Believers-Sword/Modules Turso/Commentaries/Believers Sword/generated"

COLLECTION_ID = 1
COLLECTION_NAME = "Believers Sword Commentaries"
BOOK_ID = 2
BOOK = "Exodus"
BOOK_SLUG = "exodus"
BOOK_DIR = "02-exodus"

CHAPTERS = {
    27: {
        "title": "Exodus 27 — The Bronze Altar, the Court, and the Lampstand Oil",
        "summary": (
            "Exodus 27 completes the outer furnishings of the Tabernacle with instructions for the bronze "
            "altar of burnt offering, the surrounding courtyard with its fine-linen curtains, and the "
            "command to supply pure olive oil to keep the lampstand burning continually before the LORD."
        ),
        "content": (
            "## Introduction\n\n"
            "Having described the innermost sanctuary and the veil that partitioned it (Exodus 26), God now "
            "turns to the outer court—the public-facing space of the Tabernacle complex where Israel's "
            "sacrificial worship would take place every day. Exodus 27 presents three distinct but "
            "interconnected revelations: the bronze altar (vv. 1–8), the courtyard enclosure (vv. 9–19), "
            "and the obligation to keep the lampstand burning with pure oil (vv. 20–21). Together they "
            "depict a worship system that moves from the people's approach (altar) to God's holy "
            "presence (lampstand), a movement that foreshadows the gospel's arc from sacrifice to light.\n\n"
            "## The Bronze Altar (vv. 1–8)\n\n"
            "The altar of burnt offering (מִזְבַּח הָעֹלָה, *mizbaḥ hā-ʿōlāh*) stands at the entrance of the "
            "court—the first object encountered when entering the Tabernacle precincts. Its measurements "
            "(five cubits square, three cubits high) made it the largest piece of furniture outside the "
            "sanctuary itself. Its material is acacia wood overlaid with bronze (*nĕḥōshet*), not the "
            "gold of the inner furnishings: bronze speaks of judgment, of endurance under fire. The altar "
            "had a 'horn' at each corner (vv. 2, 8), projections that symbolised power and refuge—to 'seize "
            "the horns of the altar' was to claim sanctuary (1 Kings 1:50).\n\n"
            "The practical design—a grate of bronze network, bronze rings, poles for carrying—enabled the "
            "altar to travel with Israel through the wilderness. The pattern (*tavnît*) must match what God "
            "showed Moses on the mountain (v. 8), underlining that authentic worship is always revealed, "
            "never invented.\n\n"
            "Theologically, the altar's primacy of position declares that approach to a holy God begins with "
            "sacrifice. No Israelite entered the courtyard without passing the altar. The New Testament "
            "interprets this altar christologically: Hebrews 13:10 speaks of 'an altar from which those who "
            "minister in the tent have no right to eat,' pointing to the cross as the definitive altar where "
            "Christ offered Himself as the one complete burnt offering (Heb. 10:5–10). The bronze altar was "
            "perpetually stained with blood; the cross was stained once, but its efficacy is eternal.\n\n"
            "## The Court of the Tabernacle (vv. 9–19)\n\n"
            "The courtyard was a rectangle 100 cubits long (north and south sides) and 50 cubits wide (east "
            "and west), formed by fine-twisted linen curtains five cubits high, hung from silver hooks on "
            "bronze pillars set in bronze sockets. The eastern end featured an entrance screen of 20 cubits "
            "(vv. 16–19), embroidered in blue, purple, and scarlet—the same colours as the inner sanctuary "
            "screens, yet without the cherubim, indicating a lower degree of holiness.\n\n"
            "The fine white linen (שֵׁשׁ, *shesh*) of the curtains speaks of purity and righteousness. This "
            "visible perimeter communicated to Israel and to watching nations that Israel served a God who "
            "was set apart, bounded, holy—not a deity who could be approached casually or manipulated. The "
            "court was neither closed to the people nor open to casual traffic: it required the bronze altar "
            "to be passed through on entry, which meant blood had to be shed. The court is Israel's "
            "'holy space'—not the innermost holiness of the sanctuary, but a real consecration nonetheless.\n\n"
            "For believers today, the church gathers as the temple of the Holy Spirit (1 Cor. 3:16). The "
            "boundary of linen becomes a call to purity among God's people. We are not permitted to live "
            "as the surrounding culture: we have been brought into a distinct courtyard by the blood of "
            "Christ.\n\n"
            "## Pure Oil for the Lampstand (vv. 20–21)\n\n"
            "The chapter closes with an instruction that seems out of place among architectural blueprints: "
            "the people of Israel are to bring *pure beaten olive oil* (*shemen zayit zak kātît*) so that "
            "the lampstand burns 'from evening to morning before the LORD' continually (v. 20). This command "
            "is addressed to all Israel ('you shall command the people of Israel'), making oil-provision a "
            "community act of worship, not a priestly task.\n\n"
            "The Hebrew *kātît* ('beaten') indicates that the olives were not pressed in a mill but crushed "
            "in a mortar so that only the purest first oil flowed—no sediment, the clearest light. "
            "Everything about the lampstand was for light: God had no need of it, but Israel needed to see "
            "His glory and work by its flame. Aaron and his sons tended the lamp in the Tent of Meeting, "
            "ensuring it never went out in the night.\n\n"
            "Jesus declared, 'I am the light of the world' (John 8:12). The lampstand's constant burning "
            "is fulfilled in Christ, who is never extinguished. The church, in whom His Spirit dwells, "
            "inherits this calling: 'You are the light of the world' (Matt. 5:14). The pure oil—the "
            "uncorrupted Spirit of God—keeps that light burning. Wherever the Spirit is quenched or the "
            "Word neglected, the lamp grows dim.\n\n"
            "## Christ in Exodus 27\n\n"
            "The bronze altar points to the cross: a place of fire and death where God's wrath was absorbed "
            "for Israel's (and our) sin. The courtyard's linen walls of purity point to Christ's spotless "
            "righteousness that now encloses all who belong to Him. The pure oil points to the Holy Spirit, "
            "who keeps the light of the gospel burning through every generation of the church. Exodus 27 "
            "is not a chapter about ancient architecture—it is a chapter about how a holy God graciously "
            "provides everything needed for sinful people to draw near to Him.\n\n"
            "## Conclusion\n\n"
            "Exodus 27 calls every believer to three reflections. First, never take sacrifice for granted: "
            "the altar at the gate reminds us that access to God is only through the blood of an "
            "acceptable substitute. Second, live within the boundaries of holy community: the court's linen "
            "walls mark us as a distinct people in the world. Third, supply pure oil: pray for, support, "
            "and participate in the work of the Spirit so that the light of God's truth never goes dark "
            "in your family, your church, or your generation."
        ),
        "chapter_overview": (
            "Exodus 27 provides specifications for the bronze altar of burnt offering (vv. 1–8), the "
            "courtyard enclosure of the Tabernacle (vv. 9–19), and the command for Israel to supply pure "
            "olive oil for the perpetual lampstand (vv. 20–21). The chapter anchors the theology of "
            "approaching God: sacrifice first, purity all around, and continuous light sustained by the "
            "community's devotion."
        ),
        "original_language_notes": [
            {
                "term": "mizbaḥ",
                "language": "Hebrew",
                "verse": "Exodus 27:1",
                "words_used": "מִזְבֵּחַ (mizbaḥ) — 'altar'",
                "meaning": "From the root זָבַח (*zabaḥ*), 'to slaughter/sacrifice.' The altar is, by definition, the place of slaughter. Its bronze material and prominent placement at the entrance declare that there is no access to a holy God without the shedding of blood—a reality fulfilled at Calvary (Heb. 9:22)."
            },
            {
                "term": "qarnōt",
                "language": "Hebrew",
                "verse": "Exodus 27:2",
                "words_used": "קַרְנֹת (qarnōt) — 'horns'",
                "meaning": "Projections at the four corners of the altar. 'Horn' (קֶרֶן, *qeren*) is a biblical symbol of power, strength, and refuge. Blood was smeared on the horns on the Day of Atonement (Lev. 16:18), and criminals fleeing justice would 'grasp the horns' seeking sanctuary (1 Kings 1:50; 2:28). They point to Christ as both Judge and Refuge."
            },
            {
                "term": "nĕḥōshet",
                "language": "Hebrew",
                "verse": "Exodus 27:2",
                "words_used": "נְחֹשֶׁת (nĕḥōshet) — 'bronze/copper'",
                "meaning": "The metal covering the altar and all outer-court fixtures. Distinguished from the gold of the inner sanctuary, bronze is associated in Scripture with judgment and endurance under fire (Num. 21:9; Ezek. 1:7). The altar's bronze declares it the place where divine judgment falls—upon the substitute, not the offerer."
            },
            {
                "term": "shesh",
                "language": "Hebrew",
                "verse": "Exodus 27:9",
                "words_used": "שֵׁשׁ (shesh) — 'fine linen'",
                "meaning": "Fine-twisted white linen used for the court curtains. White linen throughout Scripture symbolises purity and righteousness (Rev. 19:8, 'the fine linen is the righteous deeds of the saints'). The brilliant white perimeter of the court visually proclaimed Israel's calling to be a people set apart in holiness."
            },
            {
                "term": "kātît",
                "language": "Hebrew",
                "verse": "Exodus 27:20",
                "words_used": "כָּתִית (kātît) — 'beaten/crushed'",
                "meaning": "Describes olive oil produced by pounding rather than pressing, yielding the purest, clearest first oil. The word shares a root with כָּתַת (*kātāt*), 'to beat/crush.' That the lampstand required *beaten* oil recalls the Suffering Servant of Isaiah 53:5 who was 'crushed for our iniquities.' The purest light comes through suffering."
            }
        ],
        "moral_lessons": [
            "Access to God is never casual—sacrifice precedes fellowship.",
            "The community of God's people is defined by boundaries of holiness, not culture.",
            "Sustaining the light of God's truth requires the community's ongoing commitment and provision.",
            "God's patterns for worship must be followed exactly—we do not improvise in His presence.",
            "The bronze altar's judgment absorbed is grace for the offerer—our sin has been judged in Christ."
        ],
        "application": (
            "Examine whether you approach God's presence with gratitude for the sacrifice that opened "
            "the way—or whether familiarity has bred presumption. The altar at the gate is not meant to "
            "stop you; it is there to remind you that you are welcome because a price was paid. Live as "
            "someone enclosed in the white linen court: set apart, visibly different, holding the line of "
            "purity. And commit to bringing your 'pure oil'—time, prayer, financial support, faithful "
            "witness—so that the light of the gospel stays lit in your household and congregation."
        ),
        "prayer": (
            "Lord, I thank You that the bronze altar's work is finished at the cross. Jesus has absorbed "
            "every flash of divine judgment that I deserved. Help me never approach Your presence "
            "carelessly, but always with gratitude and awe. Make me a person of the white-linen "
            "court—set apart, pure, distinct. Fill me with Your Spirit, the pure oil, and keep Your "
            "light burning through me in a dark generation. Amen."
        ),
        "key_points": [
            "The bronze altar of burnt offering stood at the gate—the unavoidable starting point for approaching God.",
            "The courtyard's fine linen curtains visually proclaimed Israel's calling to holiness and separation.",
            "All Israel—not just priests—was responsible for supplying pure oil to keep the lampstand burning.",
            "The altar, court, and oil foreshadow Christ's sacrifice, the church's purity, and the Holy Spirit's light.",
            "God's architectural patterns for worship were divinely revealed and must be followed precisely."
        ],
        "study_questions": [
            "Why was the altar the first object encountered when entering the Tabernacle court? What does its position teach about approaching God?",
            "What do the horns of the altar symbolize, and how does this find fulfillment in Christ?",
            "The court's linen curtains were pure white. What does this boundary communicate about the community of God's people, and how does that translate to the church today?",
            "Why was the oil for the lampstand the responsibility of all Israel, not just the priests? What does this teach about shared responsibility for the church's witness?",
            "How does the 'beaten' (kātît) quality of the oil point forward to Christ's suffering?"
        ],
        "tags": ["exodus", "tabernacle", "bronze altar", "sacrifice", "court", "lampstand", "oil", "holiness", "worship", "Christ"],
        "sources": ["Exodus 27:1-21", "Hebrews 9-10", "Hebrews 13:10", "John 8:12", "Matthew 5:14", "1 Corinthians 3:16", "Revelation 19:8", "1 Kings 1:50"]
    },

    28: {
        "title": "Exodus 28 — Garments of Glory and Beauty: The Priestly Vestments",
        "summary": (
            "Exodus 28 details the sacred garments to be made for Aaron and his sons as they serve as "
            "priests before the LORD. These 'garments of glory and beauty' included the ephod, the "
            "breastpiece of judgment, the robe, the turban, and the linen undergarments—each laden "
            "with theological meaning about mediation, representation, and the holiness required "
            "for standing before God."
        ),
        "content": (
            "## Introduction\n\n"
            "If Exodus 25–27 designed the dwelling place of God, Exodus 28 designs the persons who will "
            "serve in it. The chapter opens with a divine appointment: Aaron and his four sons are set "
            "apart 'to serve me as priests' (v. 1). But priestly service requires priestly attire. What "
            "follows is one of the most detailed wardrobe descriptions in world literature—not because "
            "God is concerned with fashion, but because clothing communicates status, function, and "
            "identity. Every thread and gemstone in Aaron's vestments encoded theological truth about "
            "mediation, representation, and the demand for holiness in approaching the living God.\n\n"
            "## 'Garments of Glory and Beauty' (vv. 2–5)\n\n"
            "God's summary description of the priestly garments is 'for glory (כָּבוֹד, *kāvōd*) and for "
            "beauty (תִּפְאֶרֶת, *tifʾeret*)' (v. 2). These words are not mere aesthetic descriptors. "
            "*Kāvōd* is the word for God's own weighty, radiant presence. The priest's garments were to "
            "reflect God's glory—they dressed the mediator in dignified splendour so that Israel would "
            "recognise that approaching God is a weighty, magnificent affair. *Tifʾeret* carries the sense "
            "of splendour and honour. The high priest's clothing made visible what the Tabernacle "
            "itself made architectural: the beauty of holiness.\n\n"
            "The craftsmen called to make these garments were those 'filled with the spirit of wisdom "
            "(חָכְמָה, *ḥokmāh*)' (v. 3)—artisanal skill as a gift of the Spirit of God. Human skill in "
            "service of divine purposes is not secular; when it builds what God designs, it is sacred.\n\n"
            "## The Ephod (vv. 6–14)\n\n"
            "The ephod (אֵפוֹד, *ʾēfōd*) was the signature garment of the high priest—a sleeveless "
            "outer garment of gold, blue, purple, and scarlet thread woven with fine linen. On its two "
            "shoulder pieces were two onyx stones engraved with the names of the twelve tribes of Israel, "
            "six on each stone, in the order of their birth (vv. 9–10). Aaron bore these names 'on his "
            "two shoulders as a memorial before the LORD' (v. 12).\n\n"
            "This is the first explicitly *representative* function described: the high priest carried "
            "God's people on his shoulders into the holy presence. He did not enter alone; he entered "
            "with Israel on him. This prefigures Christ, our Great High Priest, who bears His people "
            "constantly before the Father—not as a memory aid for God, but as a declared presentation: "
            "*these are Mine.* The shepherd in Jesus' parable carries the lost sheep on his shoulders "
            "(Luke 15:5)—the same image of redemptive burden-bearing.\n\n"
            "## The Breastpiece of Judgment (vv. 15–30)\n\n"
            "The breastpiece (חֹשֶׁן הַמִּשְׁפָּט, *ḥōshen ha-mishpāṭ*) was a square pouch of the same "
            "fine workmanship as the ephod, set with twelve gemstones in four rows of three, each stone "
            "engraved with one tribe's name (vv. 17–21). It was fastened to the ephod and rested over "
            "Aaron's heart whenever he entered the Holy Place—'so Aaron shall bear the names of the "
            "sons of Israel in the breastpiece of judgment on his heart' (v. 29).\n\n"
            "Two words stand out: *mishpāṭ* (judgment, justice) and 'heart.' The breastpiece was called "
            "the instrument of 'judgment' because within it were placed the Urim and Thummim (אוּרִים "
            "וְתֻמִּים, *ʾūrîm wĕtummîm*), the mysterious oracular objects God used to communicate His "
            "will to Israel (v. 30). Scholars debate their exact nature, but their function is clear: "
            "when Israel needed divine guidance in critical matters (Num. 27:21; 1 Sam. 14:41), the "
            "high priest consulted the Urim and Thummim, and God answered. The priest was not just "
            "the conduit of sacrifice—he was the conduit of divine guidance.\n\n"
            "Aaron bore the tribes *on his heart*—an expression of priestly love. The good mediator "
            "does not merely perform rituals for people; he carries them with love. Jesus, our High "
            "Priest, 'always lives to make intercession' for us (Heb. 7:25) with a love that surpasses "
            "all human analogy (Heb. 4:14–16).\n\n"
            "## The Robe of the Ephod and the Golden Plate (vv. 31–43)\n\n"
            "The blue robe (מְעִיל הָאֵפוֹד, *mĕʿîl hā-ʾēfōd*) was worn under the ephod; its hem was "
            "ornamented with alternating pomegranates of blue, purple, and scarlet yarn, and golden "
            "bells (vv. 33–34). The bells rang as Aaron moved in the sanctuary, so 'his sound shall "
            "be heard when he goes into the Holy Place before the LORD, and when he comes out, so "
            "that he does not die' (v. 35). The sound of the bells signalled the priest's living "
            "presence before God—the people outside could hear that their mediator was still alive "
            "and moving.\n\n"
            "The golden plate (צִיץ, *ṣîṣ*) worn on the forehead of the turban bore the inscription "
            "קֹדֶשׁ לַיהוָה—*'HOLY TO THE LORD'* (vv. 36–37). It 'shall be on Aaron's forehead, and "
            "Aaron shall bear any guilt from the holy things that the people of Israel consecrate' "
            "(v. 38). Even Israel's most sincere acts of worship were tainted with impurity; the high "
            "priest bore that guilt so their offerings would be acceptable. This is a profound "
            "foreshadowing of Christ, who bore the guilt of even our *best* works—not just our sins, "
            "but the inadequacy of our best worship—so that we are accepted in the Beloved (Eph. 1:6).\n\n"
            "The linen tunics, sashes, and caps for Aaron and his sons (vv. 39–43) completed the priestly "
            "dress. Linen undergarments were required 'so that they do not incur guilt and die' (v. 43)— "
            "even the inner garments served a protective, consecrating function. Holiness in the priestly "
            "office extended from head to hem.\n\n"
            "## Christ: Our Great High Priest\n\n"
            "Hebrews 4–10 draws out the christological significance of Exodus 28 in detail. Jesus is "
            "the High Priest who is simultaneously the sacrifice and the mediator—the One who both "
            "offered Himself and now presents us to the Father. He bears our names 'on His shoulders' "
            "of omnipotent grace and 'on His heart' of inexhaustible love. He needs no golden plate "
            "to declare His holiness—He is inherently holy. He needs no Urim and Thummim—He is the "
            "Word of God, knowing the Father's will perfectly. His priestly robes are not made by "
            "human hands; He was 'clothed in glory and honour' (Heb. 2:9) by virtue of His exaltation. "
            "He is the Priest who 'always lives to intercede' (Heb. 7:25)—the perpetual sound of His "
            "mediatorial bells before the Father.\n\n"
            "## Conclusion\n\n"
            "Exodus 28 teaches that standing before a holy God requires a qualified representative. We "
            "cannot appear before God in our own spiritual 'clothes'—our righteousness is not sufficient. "
            "We need a priest clothed in glory and beauty who bears our names on his shoulders and "
            "over his heart. We have that priest in Jesus Christ. His perfect holiness, His undying "
            "intercession, and His finished sacrifice mean that every believer is carried before the "
            "Father with acceptance—because we are *in Him*, clothed in His righteousness (2 Cor. 5:21)."
        ),
        "chapter_overview": (
            "Exodus 28 specifies the seven sacred garments of the high priest: the ephod with its "
            "shoulder stones bearing the twelve tribal names, the breastpiece of judgment containing "
            "the Urim and Thummim, the blue robe with golden bells and pomegranates, the golden "
            "plate engraved 'Holy to the LORD,' the tunic, turban, and linen undergarments. Each "
            "garment reveals a dimension of priestly mediation fulfilled in Jesus Christ."
        ),
        "original_language_notes": [
            {
                "term": "ʾēfōd",
                "language": "Hebrew",
                "verse": "Exodus 28:6",
                "words_used": "אֵפוֹד (ʾēfōd) — 'ephod'",
                "meaning": "The signature outer garment of the high priest, woven in gold, blue, purple, and scarlet. Its etymology is debated but it functioned as the central garment to which other items (breastpiece) were attached. To wear the ephod was to perform the priestly office (1 Sam. 2:18, 28)."
            },
            {
                "term": "ḥōshen",
                "language": "Hebrew",
                "verse": "Exodus 28:15",
                "words_used": "חֹשֶׁן (ḥōshen) — 'breastpiece'",
                "meaning": "Unique to priestly literature; this pouch rested over Aaron's heart bearing the twelve tribal names and the Urim and Thummim. It is called the ḥōshen ha-mishpāṭ ('breastpiece of judgment/decision') because it was the medium through which God's judgments and decisions were communicated to Israel."
            },
            {
                "term": "ʾūrîm wĕtummîm",
                "language": "Hebrew",
                "verse": "Exodus 28:30",
                "words_used": "אוּרִים וְתֻמִּים (ʾūrîm wĕtummîm) — 'Lights and Perfections' (or 'Curses and Innocences')",
                "meaning": "The exact nature is unknown—possibly two objects used as lots (Num. 27:21; 1 Sam. 14:41-42). The names may derive from אָרַר ('curse') and תָּם ('complete/innocent'), yielding 'guilt and innocence,' or from אוֹר ('light') and תֹּם ('perfection'). They were God's divinely sanctioned means of revealing His will to Israel's leaders."
            },
            {
                "term": "ṣîṣ",
                "language": "Hebrew",
                "verse": "Exodus 28:36",
                "words_used": "צִיץ (ṣîṣ) — 'golden plate/flower/diadem'",
                "meaning": "The golden plate on the high priest's forehead bearing 'HOLY TO THE LORD.' The root means to gleam or blossom. By bearing this inscription on his forehead, Aaron declared that his entrance into God's presence was as one consecrated entirely to the LORD—and the inscription became Israel's credential as well."
            },
            {
                "term": "kāvōd / tifʾeret",
                "language": "Hebrew",
                "verse": "Exodus 28:2",
                "words_used": "כָּבוֹד (kāvōd) — 'glory'; תִּפְאֶרֶת (tifʾeret) — 'beauty/splendour'",
                "meaning": "Two paired terms describing the purpose of the priestly garments. Kāvōd is the term for God's own weighty, radiant presence (Exod. 33:18). Tifʾeret denotes splendour and honour. Together they signal that the high priest's vestments were not merely functional—they were theophanic reflections, making visible the glory of the God in whose presence the priest stood."
            }
        ],
        "moral_lessons": [
            "Our best attempts at self-presentation before God are insufficient; we need a priest clothed in divine glory.",
            "The high priest carried the people on his shoulders and over his heart—mediators must love those they represent.",
            "Holiness before God extends to every dimension of life, from the most visible (the golden plate) to the most hidden (the linen undergarments).",
            "Even our sincere worship needs priestly atonement for its inadequacies—only Christ's perfection makes our offerings acceptable.",
            "God's guidance comes through appointed channels; we must seek His will through the means He provides."
        ],
        "application": (
            "Rest in the reality that Jesus, your Great High Priest, bears your name on His shoulders "
            "and over His heart before the Father—right now. You are not forgotten, not abandoned, not "
            "marginalized. You are a named stone on the shoulder of One who is strong enough to carry "
            "you. You are a named stone on the heart of One who loves you enough to bear you. When you "
            "approach God in prayer, you come *in Christ*, robed in His righteousness, with His golden "
            "plate 'HOLY TO THE LORD' applied to you by grace. This should make prayer both humble and "
            "bold: humble because you have nothing to offer in your own right; bold because your Mediator "
            "is perfectly qualified."
        ),
        "prayer": (
            "Father, thank You for Jesus, my Great High Priest, who carries my name on His shoulders and "
            "over His heart. I confess that I have no righteousness of my own that is fit to stand "
            "before Your glory. But Jesus bears the inscription 'HOLY TO THE LORD,' and because I am "
            "clothed in His righteousness, that inscription covers me too. Make me bold in prayer, "
            "knowing I come to You through a perfectly qualified Mediator. Amen."
        ),
        "key_points": [
            "The priestly garments were designed for 'glory and beauty'—reflecting the dignity required when approaching a holy God.",
            "The ephod's shoulder stones bore all twelve tribal names; the priest carried the whole nation into God's presence.",
            "The breastpiece of judgment over Aaron's heart combined representational love with divine guidance (Urim and Thummim).",
            "The golden plate 'HOLY TO THE LORD' on the forehead covered even the inadequacies of Israel's worship.",
            "Every detail of the priestly garments is fulfilled in Christ, our permanent, sinless Great High Priest."
        ],
        "study_questions": [
            "Why were the priestly garments described as being for 'glory and beauty'? What does this communicate about the nature of the priestly office?",
            "The high priest bore the tribal names on both his shoulders and over his heart. What is the significance of both locations?",
            "What were the Urim and Thummim, and what does their placement in the breastpiece tell us about the relationship between priestly mediation and divine guidance?",
            "The golden plate bore guilt for Israel's holy things (v. 38). What does this reveal about the purity required by God even for sincere worship, and how does Christ fulfil this need?",
            "How does Hebrews 4:14–16 and 7:23–25 draw out the contrast between Aaron's priesthood and Christ's? What makes Christ's priesthood superior?"
        ],
        "tags": ["exodus", "priesthood", "ephod", "breastpiece", "Urim and Thummim", "Aaron", "mediation", "holiness", "Christ", "high priest"],
        "sources": ["Exodus 28:1-43", "Hebrews 4:14-16", "Hebrews 7:23-25", "Hebrews 10:5-10", "Ephesians 1:6", "2 Corinthians 5:21", "Numbers 27:21", "Luke 15:5"]
    },

    29: {
        "title": "Exodus 29 — The Ordination of Priests and the Promise of God's Presence",
        "summary": (
            "Exodus 29 prescribes the elaborate seven-day ordination ceremony for Aaron and his sons, "
            "culminating in God's declaration: 'I will dwell among the people of Israel and will be "
            "their God.' The chapter moves from blood and fire to covenant intimacy, revealing that "
            "all the ceremony serves one supreme end—God dwelling with His redeemed people."
        ),
        "content": (
            "## Introduction\n\n"
            "Having designed the Tabernacle and its furnishings (Exod. 25–27) and prescribed the "
            "priestly vestments (Exod. 28), God now details how the priests are to be consecrated "
            "for their office. Exodus 29 is one of the longest and most detailed ritual chapters "
            "in the Bible—29 verses of precise sacrificial instruction. Yet the chapter does not end "
            "in blood and smoke; it ends in a breathtaking divine declaration of covenant fellowship "
            "(vv. 43–46). The elaborate ritual serves a relational goal: God wants to dwell with "
            "His people, and the ordination of the priests is how He structures that dwelling.\n\n"
            "## Washing, Robing, and Anointing (vv. 1–9)\n\n"
            "The ordination ceremony began with washing: 'You shall bring Aaron and his sons to the "
            "entrance of the tent of meeting and wash them with water' (v. 4). This initial washing "
            "was a once-for-all cleansing for the priests at ordination; thereafter, daily hand-and-foot "
            "washing at the bronze laver preceded each service (Exod. 30:18–21).\n\n"
            "Aaron was then robed in the full vestments described in chapter 28, anointed with oil "
            "(*shemen ha-mishḥāh*, the anointing oil, v. 7), and formally set apart. His sons were "
            "robed more simply in tunics and sashes. The act of vesting created a visible, public "
            "commissioning—these men were separated from Israel's congregation to stand between God "
            "and the people. The name *kōhēn* (priest) does not have a clear root etymology, but the "
            "function is evident: the priest stands 'before' (*lifnê*) God on behalf of the people.\n\n"
            "## The Three Ordination Sacrifices (vv. 10–35)\n\n"
            "Three animals were sacrificed in sequence:\n\n"
            "**1. The Bull for Sin (ḥaṭṭāʾt, vv. 10–14):** Aaron and his sons placed their hands on "
            "the bull's head (סָמַךְ יָד, *sāmak yād*)—the act of identification and transference. "
            "The priest-candidates needed cleansing before they could cleanse others. The bull's blood "
            "was applied to the altar's horns; its fat, organs, and extremities were burned on the "
            "altar; its hide, flesh, and dung were burned outside the camp—bearing the reproach of sin "
            "outside the sacred precinct. The writer of Hebrews sees this pattern fulfilled in Christ: "
            "'So Jesus also suffered outside the gate in order to sanctify the people through his own "
            "blood' (Heb. 13:12).\n\n"
            "**2. The Ram of Burnt Offering (ʿōlāh, vv. 15–18):** The entire ram was burned on the "
            "altar after the laying-on of hands. The burnt offering communicated total consecration—"
            "nothing held back, everything surrendered to God. As the priests committed themselves "
            "wholly to God's service, this sacrifice enacted the same truth at the altar. It was 'a "
            "pleasing aroma to the LORD' (v. 18)—a formula signalling divine acceptance.\n\n"
            "**3. The Ram of Ordination (milluʾîm, vv. 19–35):** The most distinctive sacrifice. "
            "Blood from this ram was applied to the right ear, right thumb, and right big toe of Aaron "
            "and his sons (v. 20)—ears consecrated to hear God's word, hands consecrated for His "
            "service, feet consecrated to walk in His ways. Moses then waved the fat portions, the "
            "right thigh, and bread before the LORD (the wave offering, תְּנוּפָה, *tĕnûfāh*), burned "
            "some on the altar, and gave the rest to Aaron and his sons to eat as the ordination meal "
            "(vv. 31–34). This was uniquely the priests' meal from the ordination offerings.\n\n"
            "The seven-day duration (v. 35) underscores completion and solemnity: ordination was not "
            "a single ceremony but a sustained, progressive consecration.\n\n"
            "## The Daily Burnt Offering (vv. 38–42)\n\n"
            "Following the ordination ceremony, God instituted the *tāmîd* (תָּמִיד, 'continual') "
            "offering: two one-year-old lambs every day—one in the morning, one in the evening—"
            "accompanied by grain offering and drink offering. This daily sacrifice at the entrance "
            "of the Tent of Meeting structured Israel's time: every day began and ended with sacrifice "
            "and the acknowledgement of God. The *tāmîd* became the rhythm of Israelite national "
            "worship.\n\n"
            "The New Testament sees the *tāmîd* completed in Christ's 'once for all' sacrifice "
            "(Heb. 7:27; 10:10)—not because repetition was meaningless, but because every repetition "
            "was pointing toward the singular Lamb who would replace all lambs. The Revelation's "
            "vision of 'the Lamb standing, as though it had been slain' (Rev. 5:6) is the eternal "
            "*tāmîd*: the once-for-all sacrifice that stands before God permanently on behalf of "
            "His people.\n\n"
            "## The Climax: God's Dwelling (vv. 43–46)\n\n"
            "The chapter closes with one of the most moving passages in Exodus:\n\n"
            "*'There I will meet with the people of Israel, and it shall be sanctified by my glory. "
            "I will consecrate the tent of meeting and the altar... I will dwell among the people "
            "of Israel and will be their God. And they shall know that I am the LORD their God, who "
            "brought them out of the land of Egypt that I might dwell among them. I am the LORD "
            "their God.'* (vv. 43–46)\n\n"
            "The entire sacrificial system—every cut and splash of blood, every wave and burning—"
            "exists to make this one thing possible: God dwelling with His people. The Exodus was not "
            "ultimately about deliverance from Egypt; it was about the destination of God's presence. "
            "The New Testament declares this promise fulfilled in Jesus: 'the Word became flesh and "
            "dwelt among us' (John 1:14), and ultimately in the New Jerusalem: 'Behold, the dwelling "
            "place of God is with man' (Rev. 21:3).\n\n"
            "## Conclusion\n\n"
            "Exodus 29 is not merely about ancient priestly rites. It is about the lengths God goes to "
            "in order to be with His people. The blood, the fire, the seven days, the precise gestures—"
            "all of it removes every obstacle that sin creates so that the holy God can draw near. "
            "This reaches its consummation in the incarnation and atonement of Jesus, the Priest who "
            "consecrated Himself by His own blood so that God could dwell in us by His Spirit "
            "(1 Cor. 3:16; Eph. 2:21–22)."
        ),
        "chapter_overview": (
            "Exodus 29 prescribes the seven-day ordination of Aaron and his sons, featuring three "
            "key sacrifices: a sin offering bull (cleansing the candidates), a burnt offering ram "
            "(total consecration), and an ordination ram (blood applied to ear, thumb, toe). It "
            "establishes the daily *tāmîd* offering and closes with God's declaration to dwell "
            "among Israel—the goal all the ceremony was designed to achieve."
        ),
        "original_language_notes": [
            {
                "term": "milluʾîm",
                "language": "Hebrew",
                "verse": "Exodus 29:22",
                "words_used": "מִלֻּאִים (milluʾîm) — 'ordination; filling'",
                "meaning": "The technical term for the priestly ordination ceremony, from מָלֵא (*māleʾ*), 'to fill.' The ordination 'fills the hand' of the priest—a Hebrew idiom meaning to install formally into an office. The priest's hand is 'filled' with the authority and privilege of service. The phrase echoes through Chronicles and Kings as the standard way to describe priestly installation."
            },
            {
                "term": "sāmak yād",
                "language": "Hebrew",
                "verse": "Exodus 29:10",
                "words_used": "סָמַךְ יָד (sāmak yād) — 'to lay the hand'",
                "meaning": "The gesture of placing hands on the sacrifice's head. This act communicated identification: the offerer was associating himself with the animal so that what happened to the animal would be reckoned as happening to the offerer. It is the foundation of substitutionary atonement theology—the animal dies in the place of the guilty party."
            },
            {
                "term": "tāmîd",
                "language": "Hebrew",
                "verse": "Exodus 29:38",
                "words_used": "תָּמִיד (tāmîd) — 'continual, perpetual'",
                "meaning": "The adjective describing the daily burnt offering—two lambs, morning and evening, every day without exception. *Tāmîd* means 'ongoing, unbroken, perpetual.' The word is used of the lampstand (Exod. 27:20), the showbread (Lev. 24:8), and the morning/evening sacrifice, suggesting that the entire Tabernacle complex was designed for uninterrupted, ceaseless worship."
            },
            {
                "term": "ʿōlāh",
                "language": "Hebrew",
                "verse": "Exodus 29:18",
                "words_used": "עֹלָה (ʿōlāh) — 'burnt offering; that which goes up'",
                "meaning": "From עָלָה (*ʿālāh*), 'to go up, ascend.' The entire animal was burned—nothing returned to the offerer. The smoke ascended to God as a totality-offering, signifying complete consecration and surrender. Paul echoes this in Romans 12:1: 'present your bodies as a living sacrifice (*thysian zōsan*)—a New Testament ʿōlāh."
            },
            {
                "term": "rêaḥ nîḥōaḥ",
                "language": "Hebrew",
                "verse": "Exodus 29:18",
                "words_used": "רֵיחַ נִיחֹחַ (rêaḥ nîḥōaḥ) — 'pleasing aroma'",
                "meaning": "The formulaic phrase indicating divine acceptance of a sacrifice. A wordplay: *nîḥōaḥ* shares the consonants of נוּחַ (*nûaḥ*), 'to rest,' suggesting the offering brings rest/satisfaction to God. The phrase is applied to Christ's self-offering in Ephesians 5:2: 'a fragrant offering and sacrifice to God.'"
            }
        ],
        "moral_lessons": [
            "Before serving God, one must be cleansed—the priests were washed before they were robed.",
            "Total consecration (the burnt offering) must accompany every act of ministry in God's service.",
            "The blood applied to ear, thumb, and toe teaches that consecration covers what we hear, what we do, and where we walk.",
            "The daily sacrifice structured Israel's time around God—morning and evening devotion is rooted in ancient covenant practice.",
            "All ceremony, all worship, all sacrifice ultimately exists to achieve one end: God dwelling with His people."
        ],
        "application": (
            "Ask yourself: have you been 'washed' and 'robed' in Christ's righteousness, or are you "
            "still trying to minister from your own qualifications? The message of Exodus 29 is that "
            "qualification for God's service is not natural—it is conferred through the blood of "
            "consecration. Practically, structure your days around morning and evening encounter with "
            "God (the *tāmîd* pattern). Let your ears, hands, and feet—what you hear, what you do, "
            "where you go—be consciously consecrated to His service each day. And remember the goal: "
            "God's dwelling. Every discipline, every sacrifice, every act of worship is in service "
            "of the greatest gift—the presence of God."
        ),
        "prayer": (
            "Lord God, I come to You washed in the blood of Jesus and robed in His righteousness—not "
            "in any merit of my own. Consecrate my ears to hear Your Word, my hands to do Your work, "
            "my feet to walk in Your ways. Make me a daily *tāmîd* offering—morning and evening "
            "surrendered to You. And may the deepest desire of my heart be Your presence: that You "
            "would dwell in me and I in You. Amen."
        ),
        "key_points": [
            "The ordination ceremony began with washing, then robing, then anointing—cleansing precedes commissioning.",
            "Three sacrifices marked the ordination: sin offering (cleansing), burnt offering (total consecration), ordination ram (blood on ear, thumb, toe).",
            "The blood applied to the priest's right ear, thumb, and toe consecrated his hearing, his work, and his walk.",
            "The daily *tāmîd* offering—two lambs morning and evening—structured all of Israel's time around sacrifice and worship.",
            "The chapter's climax is God's declaration to dwell among His people—all the ceremony serves this relational purpose."
        ],
        "study_questions": [
            "Why was washing the first act of the ordination ceremony? What does this order (wash, then robe, then anoint) communicate about how one enters God's service?",
            "What is the significance of blood being applied to the right ear, thumb, and big toe? What does this say about the scope of priestly consecration?",
            "Why did God establish a daily (*tāmîd*) offering rather than a weekly or monthly one? What does this rhythm teach about the nature of ongoing relationship with God?",
            "How does the ordination ram's wave offering and shared meal (vv. 26–34) anticipate the Lord's Supper and the communion of believers with their Priest?",
            "The chapter ends with God's declared goal: 'I will dwell among the people of Israel' (v. 45). How does this goal reframe the entire preceding ritual? How is it fulfilled in the New Testament?"
        ],
        "tags": ["exodus", "ordination", "priesthood", "consecration", "sin offering", "burnt offering", "tāmîd", "daily sacrifice", "God's presence", "Christ"],
        "sources": ["Exodus 29:1-46", "Hebrews 7:27", "Hebrews 10:10", "Hebrews 13:12", "John 1:14", "Revelation 5:6", "Revelation 21:3", "Romans 12:1", "Ephesians 5:2"]
    },

    30: {
        "title": "Exodus 30 — Incense, Atonement, Anointing: Drawing Near to a Holy God",
        "summary": (
            "Exodus 30 adds five more instructions for the Tabernacle's operation: the golden altar of "
            "incense (vv. 1–10), the half-shekel atonement tax (vv. 11–16), the bronze washing basin "
            "(vv. 17–21), the sacred anointing oil (vv. 22–33), and the sacred incense formula "
            "(vv. 34–38). Each element addresses a different dimension of holiness: prayer, atonement "
            "for the census, ritual purity, consecration, and worship."
        ),
        "content": (
            "## Introduction\n\n"
            "Exodus 30 interrupts the ordination narrative of chapters 28–29 to provide supplementary "
            "instructions for Tabernacle worship. The five distinct topics covered here are not random: "
            "they form a unified theology of how sinful people draw near to the utterly holy God. "
            "Incense rises as prayer, atonement money covers the community's guilt, water cleanses "
            "the ministers, oil consecrates people and objects, and incense sanctifies the atmosphere "
            "of worship. Together, these elements create a complete picture of the multidimensional "
            "holiness required in God's presence.\n\n"
            "## The Golden Altar of Incense (vv. 1–10)\n\n"
            "The altar of incense (מִזְבַּח הַקְּטֹרֶת, *mizbaḥ haq-qĕṭōret*) was a small acacia-wood "
            "altar overlaid with pure gold, placed before the veil in the Holy Place—in front of the "
            "Ark of the Covenant. Aaron burned fragrant incense on it every morning and evening, "
            "synchronised with his tending of the lampstand (v. 7–8). This altar was uniquely "
            "*qdosh qodashim* ('most holy,' v. 10), a designation shared with the Ark and the inner "
            "sanctuary.\n\n"
            "The Hebrew *qĕṭōret* (incense, from קָטַר, *qāṭar*, 'to cause to rise in smoke') "
            "represents ascending prayer. Psalm 141:2 makes the connection explicit: 'Let my prayer "
            "be counted as incense before you.' The New Testament vision of Revelation 5:8 and 8:3–5 "
            "presents golden bowls of incense as 'the prayers of the saints'—the image is directly "
            "drawn from this altar. The incense altar, closest to the veil that separated the Holy "
            "Place from the Holy of Holies, depicts prayer as the activity that draws the worshipper "
            "closest to God's immediate presence.\n\n"
            "Once a year, on the Day of Atonement, blood from the sin offering was applied to the "
            "altar's horns (v. 10)—even the prayer altar needed atonement. The most spiritual human "
            "activity remains infected by the human condition. Only Christ's intercession—perfect, "
            "sinless, perpetual—needs no atonement. His prayer is ever-fragrant before the Father "
            "(Heb. 7:25; Rom. 8:34).\n\n"
            "## The Atonement Tax (vv. 11–16)\n\n"
            "When Israel conducted a census, each man over twenty years old was to pay a half-shekel "
            "(*beka*, בֶּקַע, v. 13) as 'a ransom for his life to the LORD.' Rich and poor alike paid "
            "the same amount (v. 15): before God, there is no distinction of wealth. The silver "
            "collected went toward the service of the Tent of Meeting and served as an atonement "
            "(*kōfer*, כֹּפֶר, 'ransom price') so that 'no plague' would come upon them when they "
            "were numbered (v. 12).\n\n"
            "The census itself was dangerous because it tempted a king (or nation) to trust in numbers "
            "rather than God (cf. 2 Sam. 24). The atonement tax was a corrective: even as you count "
            "your strength, acknowledge that each life belongs to God and must be ransomed. The "
            "uniform half-shekel enacted equality before God: the ground at the foot of the cross is "
            "level. This passage stands behind the New Testament principle that the atonement "
            "Christ provides is for 'all alike' (Rom. 3:22–24).\n\n"
            "## The Bronze Basin (vv. 17–21)\n\n"
            "A bronze washing basin (*kiyyōr*, כִּיּוֹר, v. 18) was placed between the altar of "
            "burnt offering and the entrance to the Tent of Meeting. Aaron and his sons were "
            "required to wash their hands and feet before ministering at the altar or entering the "
            "tent. The penalty for failure was death (v. 20–21).\n\n"
            "The basin addressed not the initial ordination washing (a once-for-all cleansing) but "
            "the ongoing purity required for daily service. Even priests who had been ordained and "
            "consecrated needed continual cleansing. The New Testament applies this pattern to "
            "believers: the initial washing is regeneration (Titus 3:5), but the ongoing washing "
            "is sanctification through the Word (John 17:17; Eph. 5:26). Jesus told Peter: 'The one "
            "who has bathed does not need to wash, except for his feet' (John 13:10)—the same "
            "distinction between initial cleansing and ongoing purity.\n\n"
            "## The Sacred Anointing Oil (vv. 22–33)\n\n"
            "God provided Moses with a precise formula for anointing oil: myrrh, cinnamon, aromatic "
            "cane, cassia, and olive oil (vv. 23–24). This compounded oil—uniquely composed, never "
            "to be duplicated for personal use—was to anoint the Tabernacle and all its furnishings "
            "(*qiddēsh*, 'consecrate' them, v. 29) and the priests. Whatever the oil touched became "
            "*qōdesh qodāshîm* ('most holy,' v. 29).\n\n"
            "The Hebrew *māshîaḥ* (מָשִׁיחַ, 'anointed one,' *Messiah*) comes from the same root: "
            "to be anointed was to be set apart for divine service. Kings, prophets, and priests were "
            "all anointed in Israel. The oil's prohibition against personal imitation (vv. 32–33) "
            "guarded against trivialising the sacred anointing. In the New Testament, believers are "
            "anointed by the Holy Spirit (1 John 2:20, 27; 2 Cor. 1:21–22)—the Spirit is God's "
            "consecrating oil, setting apart those who belong to the Anointed One (*Christos*, the "
            "Greek equivalent of *Māshîaḥ*).\n\n"
            "## The Sacred Incense Formula (vv. 34–38)\n\n"
            "The final instruction parallels the anointing oil: a specific formula of stacte, onycha, "
            "galbanum, and frankincense—salted, pure, and holy (vv. 34–35). This incense was to be "
            "used *only* on the incense altar before the Testimony; any person who made it for personal "
            "use would be 'cut off from his people' (v. 38). The uniqueness of the sacred incense "
            "protected the worship of God from casual imitation.\n\n"
            "The insistence on uniqueness in both oil and incense declares that God's presence and "
            "God's worship cannot be replicated or commercialised. The incense of prayer directed "
            "to God must be genuine—not performed for human audiences, not manufactured for emotional "
            "effect. Jesus' critique of hypocritical prayer (Matt. 6:5) echoes this principle: the "
            "sacred fragrance of true prayer is not a product to be displayed.\n\n"
            "## Conclusion\n\n"
            "Exodus 30 builds a comprehensive picture of what sustained, holy communion with God "
            "requires: continual prayer (incense altar), recognition of personal ransomed value "
            "(atonement tax), ongoing cleansing (bronze basin), Spirit-consecration (anointing oil), "
            "and authentic worship (sacred incense). These are not abolished in Christ—they are "
            "fulfilled and internalised. The Christian draws near through the incense of Christ's "
            "intercession, stands ransomed by His blood (not a half-shekel), is washed daily in "
            "the Word, anointed by the Spirit, and worships in spirit and in truth (John 4:24)."
        ),
        "chapter_overview": (
            "Exodus 30 provides instructions for five additional Tabernacle elements: the golden "
            "incense altar (closest to the veil, representing prayer), the half-shekel atonement "
            "census tax (equal for all, covering the community), the bronze washing basin (ongoing "
            "purity for priests), the sacred anointing oil formula (consecrating everything it "
            "touches), and the sacred incense formula (uniquely for God's altar alone). Together "
            "they depict the multidimensional holiness required for sustained communion with God."
        ),
        "original_language_notes": [
            {
                "term": "qĕṭōret",
                "language": "Hebrew",
                "verse": "Exodus 30:1",
                "words_used": "קְטֹרֶת (qĕṭōret) — 'incense'",
                "meaning": "From קָטַר (*qāṭar*), 'to cause smoke to ascend.' The incense's rising smoke was a visible symbol of prayer ascending to God (Ps. 141:2; Rev. 5:8; 8:3–4). The morning and evening burning of incense at the altar nearest the veil depicted prayer as the activity that brings the worshipper closest to God's immediate presence."
            },
            {
                "term": "kōfer",
                "language": "Hebrew",
                "verse": "Exodus 30:12",
                "words_used": "כֹּפֶר (kōfer) — 'ransom, atonement price'",
                "meaning": "The technical term for an amount paid to redeem or buy back a life that is forfeit. From the same root as כִּפֻּר (*kippūr*, atonement). The half-shekel was not a tax in the modern sense but a ransom price—each counted life acknowledged its debt to God and its need for redemption. This root underlies Yom Kippur ('Day of Atonement') and prefigures Christ as the *kōfer* for all humanity (Mark 10:45, *lytron*)."
            },
            {
                "term": "kiyyōr",
                "language": "Hebrew",
                "verse": "Exodus 30:18",
                "words_used": "כִּיּוֹר (kiyyōr) — 'laver, basin'",
                "meaning": "A large bronze vessel holding water for priestly washing. The root may relate to a round vessel. Made from the bronze mirrors of the women who served at the tabernacle entrance (Exod. 38:8), suggesting that what once served personal vanity (reflection) was repurposed for consecrated purity—a transformation picture of sanctification."
            },
            {
                "term": "māshîaḥ",
                "language": "Hebrew",
                "verse": "Exodus 30:30",
                "words_used": "מָשַׁח (māshaḥ) — 'to anoint'; מָשִׁיחַ (māshîaḥ) — 'anointed one'",
                "meaning": "The verb used for anointing Aaron and his sons with the sacred oil. From this root comes *māshîaḥ* (Messiah), 'anointed one.' Kings, priests, and prophets were anointed for their offices. Jesus is the *Christos* (Greek translation of *māshîaḥ*)—the Priest, King, and Prophet anointed not with fragrant oil but with the Holy Spirit without measure (Luke 4:18; John 3:34)."
            },
            {
                "term": "qōdesh qodāshîm",
                "language": "Hebrew",
                "verse": "Exodus 30:29",
                "words_used": "קֹדֶשׁ קָדָשִׁים (qōdesh qodāshîm) — 'most holy' (lit. 'holy of holies')",
                "meaning": "The superlative form in Hebrew, meaning the highest degree of holiness. Applied to the tabernacle furnishings anointed with the sacred oil and to the altar of incense (v. 10). This grade of holiness meant that anyone or anything coming into contact with these objects became holy—they 'infected' with holiness rather than contaminating with impurity (cf. Exod. 29:37)."
            }
        ],
        "moral_lessons": [
            "Prayer—like incense—should be regular (morning and evening), fragrant (genuine and God-directed), and ascending (acknowledging God above us).",
            "Every person stands before God on equal ground: the atonement price is the same for rich and poor, powerful and weak.",
            "Ministry requires ongoing cleansing; initial conversion must be followed by daily washing in the Word.",
            "True consecration cannot be counterfeited—genuine anointing by the Holy Spirit is unique and irreplaceable.",
            "Authentic worship cannot be commercialised, performed for show, or manufactured; like the sacred incense, it is meant for God alone."
        ],
        "application": (
            "Let the incense altar teach you to pray consistently—morning and evening, as a rhythm of "
            "life. Let the atonement tax remind you that your life is ransom-bought: Christ paid more "
            "than a half-shekel for you. Let the laver call you to daily renewal through Scripture and "
            "confession—ongoing cleansing for ongoing service. Let the anointing oil make you grateful "
            "for the Spirit's work of consecration in your life: you have been set apart for God. And "
            "let the incense formula warn you against mere performance in worship—God desires the "
            "fragrance of authentic, Spirit-led prayer and praise."
        ),
        "prayer": (
            "Father, let my prayers rise before You like incense—morning and evening, genuine and "
            "ascending. Thank You that I have been ransomed not with silver but with the precious blood "
            "of Christ. Cleanse me daily by Your Word, anoint me afresh by Your Spirit, and may my "
            "worship be true and fragrant before You alone—never for human approval. Amen."
        ),
        "key_points": [
            "The golden incense altar, placed nearest the veil, represents prayer as the closest approach to God's presence.",
            "The half-shekel atonement tax was equal for all—rich and poor alike—declaring God's impartial value of every human life.",
            "The bronze basin addressed ongoing, daily purity required for ministry—distinct from the once-for-all ordination washing.",
            "The sacred anointing oil formula was unique and irreproducible—pointing to the unique consecrating work of the Holy Spirit.",
            "Both the anointing oil and the incense were protected by prohibition of personal imitation, guarding true worship from trivialisation."
        ],
        "study_questions": [
            "Why was the altar of incense placed closest to the veil, just before the Ark? What does this spatial arrangement communicate about prayer's relationship to God's presence?",
            "The atonement tax was exactly the same for rich and poor (v. 15). What theological principle does this enforce, and how does it compare with the New Testament message of salvation?",
            "What is the difference between the initial ordination washing and the daily laver washing? How does John 13:10 draw on this same distinction?",
            "Why were both the anointing oil and the incense formulae strictly forbidden for personal use? What principle about worship and consecration does this protect?",
            "How does the New Testament reinterpret each element of Exodus 30: the incense altar (Rom. 8:34; Rev. 8:3-4), the ransom tax (Mark 10:45), the laver (Eph. 5:26), and the anointing oil (1 John 2:20)?"
        ],
        "tags": ["exodus", "incense", "prayer", "atonement", "laver", "anointing oil", "Messiah", "holiness", "worship", "consecration"],
        "sources": ["Exodus 30:1-38", "Psalm 141:2", "Revelation 5:8", "Revelation 8:3-5", "Hebrews 7:25", "Romans 8:34", "Mark 10:45", "John 13:10", "Ephesians 5:26", "1 John 2:20"]
    },

    31: {
        "title": "Exodus 31 — Spirit-Filled Craftsmen and the Sabbath as Covenant Sign",
        "summary": (
            "Exodus 31 names Bezalel and Oholiab as the Spirit-filled craftsmen appointed to build "
            "the Tabernacle and its furnishings, then closes the entire Tabernacle instruction section "
            "with a solemn command to observe the Sabbath as a covenant sign between God and Israel. "
            "The chapter shows that artistic skill is a gift of the Spirit, and that even holy work "
            "must pause before God's rest."
        ),
        "content": (
            "## Introduction\n\n"
            "The long section of divine Tabernacle instructions that began in Exodus 25 comes to its "
            "close in Exodus 31. God has specified what is to be built and how it is to be served; "
            "now He names who will build it. But the chapter does not end with the craftsmen—it ends "
            "with the Sabbath. The juxtaposition is striking: the very people called to construct "
            "God's dwelling must stop their construction every seventh day. The holiest work must "
            "still yield to the holy rest. This pairing of gifting and sabbath, of industry and "
            "ceasing, frames the chapter's twin message: God equips with His Spirit and God rules "
            "over time.\n\n"
            "## Bezalel: Filled with the Spirit for Craftsmanship (vv. 1–6)\n\n"
            "God names Bezalel son of Uri son of Hur, from the tribe of Judah, and declares: 'I have "
            "filled him with the Spirit of God (*Rûaḥ ʾElōhîm*, רוּחַ אֱלֹהִים), with ability and "
            "intelligence, with knowledge and all craftsmanship, to devise artistic designs, to work "
            "in gold, silver, and bronze, in cutting stones for setting, and in carving wood, to work "
            "in every craft' (vv. 3–5). This is a remarkable statement. The first specific mention of "
            "a person being 'filled with the Spirit of God' in all of Scripture is in connection with "
            "artistic craftsmanship, not prophecy or preaching.\n\n"
            "The Hebrew term used for Bezalel's skill is חָכְמָה (*ḥokmāh*, wisdom)—the same word "
            "used for Solomonic wisdom and for the fear of the LORD (Prov. 1:7). Craftsmanship done "
            "in God's service is an exercise of Spirit-granted wisdom. God does not dichotomise "
            "between 'spiritual' and 'manual' gifts: He fills a woodworker and goldsmith with His "
            "Spirit just as He fills prophets and priests. The artisan working for God's purposes "
            "is doing Spirit-led work.\n\n"
            "Alongside Bezalel, God appointed Oholiab son of Ahisamach, from the tribe of Dan "
            "(v. 6)—Judah in the south and Dan in the north, the farthest-apart tribes, together "
            "representing all Israel in the building project. God also gave 'ability to all able "
            "men'—the Spirit did not merely fill one exceptional craftsman; He gifted an entire "
            "team for the sacred work.\n\n"
            "The New Testament extends this principle: every believer is gifted by the Spirit for "
            "service (1 Cor. 12:4–11; Eph. 4:7–12). The gifts are diverse—teaching, serving, "
            "administration, mercy—but they all originate from the same Spirit and serve the same "
            "purpose: building the dwelling of God (Eph. 2:21–22).\n\n"
            "## What Bezalel Was to Build (vv. 7–11)\n\n"
            "God summarises the entire scope of Bezalel and Oholiab's commission: the Tent of "
            "Meeting, the Ark, the mercy seat, all the furnishings, the table, the lampstand, the "
            "incense altar, the altar of burnt offering, the bronze basin, the sacred garments—"
            "everything described in Exodus 25–30. The craftsmen were not given freedom to "
            "improvise: they were to build 'according to all that I have commanded you' (v. 11). "
            "Spirit-filling does not override obedience; it empowers faithful execution of God's "
            "revealed will.\n\n"
            "## The Sabbath as Covenant Sign (vv. 12–17)\n\n"
            "After 130 verses of Tabernacle instructions (Exod. 25–31:11), God addresses the "
            "Sabbath for the third time in Exodus—but with the most solemn language yet. The Sabbath "
            "command is introduced as something God gives to Israel: 'You shall keep my Sabbaths' "
            "(v. 13). Three elements make this passage distinctive:\n\n"
            "**1. The Sabbath as sign (אוֹת, *ʾōt*):** 'It is a sign between me and you throughout "
            "your generations' (v. 13). Signs in the Bible are visible, sacramental markers of "
            "covenant relationships: the rainbow (Noah), circumcision (Abraham), the Passover blood "
            "(Egypt). The Sabbath was Israel's weekly covenant marker, distinguishing them from all "
            "other nations who did not rest on the seventh day. It was not merely a productivity "
            "pause; it was a declaration of who Israel belonged to.\n\n"
            "**2. The Sabbath as sanctifier:** 'that you may know that I, the LORD, sanctify you' "
            "(v. 13). Israel's holiness (*qiddēsh*, the same word used for the Tabernacle's "
            "furnishings) comes from God, not from their own effort. When Israel rested, they "
            "demonstrated that their security and identity rested in God's faithfulness, not in their "
            "own industry.\n\n"
            "**3. The severity of violation:** 'Whoever does any work on the Sabbath day shall be "
            "put to death' (v. 15). This capital sentence—applied even to Tabernacle construction "
            "(rabbinic tradition uses this passage to define the 39 categories of forbidden Sabbath "
            "work)—declares that the Sabbath was not a suggestion. No project, however holy, "
            "overrides the covenant rhythm of rest. Even God's own house could not be built seven "
            "days a week.\n\n"
            "Verse 17 provides the theological grounding: 'In six days the LORD made heaven and "
            "earth, and on the seventh day he rested and was refreshed.' The Hebrew *wayyinnāpash* "
            "(וַיִּנָּפַשׁ, v. 17) is striking—'was refreshed,' as if God's rest was revitalising. "
            "God does not grow tired (Isa. 40:28), so this is anthropomorphic language teaching "
            "that the seventh day is characterised by the satisfaction and delight of completed "
            "work—not exhaustion. The Sabbath is the day that savours what God has done.\n\n"
            "## The Two Stone Tablets (v. 18)\n\n"
            "The chapter closes simply but powerfully: 'When he finished speaking with him on Mount "
            "Sinai, he gave to Moses the two tablets of the testimony, tablets of stone, written "
            "with the finger of God.' The phrase 'finger of God' appears only twice in the Pentateuch: "
            "here, and in Exodus 8:19 when the Egyptian magicians recognised the plagues as divine. "
            "God's direct writing on stone—rather than through a human scribe—underscored the "
            "absolute authority and permanence of the Law He was entrusting to Moses. It is also "
            "the prelude to the catastrophe about to unfold in Exodus 32: the moment Moses descends "
            "with the 'finger of God' tablets, he will find Israel worshipping a golden calf.\n\n"
            "## Christ and the Sabbath\n\n"
            "Jesus declared Himself 'Lord of the Sabbath' (Matt. 12:8), placing Himself above the "
            "institution. Hebrews 4 presents the ultimate Sabbath rest as entering into God's own "
            "rest through faith in Christ—a rest that the weekly Sabbath anticipated but could not "
            "fully provide. The Christian observes not merely one day's rest but a continuous "
            "posture of resting in Christ's finished work, trusting not in works but in the One "
            "who said 'It is finished' (John 19:30)—the language of completed creative work, as "
            "on the seventh day of creation.\n\n"
            "## Conclusion\n\n"
            "Exodus 31 bookends the Tabernacle instructions with two truths: Spirit-given gifts "
            "equip us for holy service, and covenant-shaped rest defines the rhythm of holy life. "
            "Bezalel teaches us that every good skill, when consecrated to God, is Spirit-enabled "
            "ministry. The Sabbath teaches us that even the holiest work must be punctuated by "
            "trust—the declaration that God, not our industry, is what makes life and worship "
            "possible."
        ),
        "chapter_overview": (
            "Exodus 31 names Bezalel of Judah and Oholiab of Dan as Spirit-filled craftsmen "
            "appointed to build everything described in Exodus 25–30. It then commands Israel to "
            "observe the Sabbath as a covenant sign between God and Israel—a sign of sanctification, "
            "not merely rest. The chapter closes with Moses receiving the two stone tablets written "
            "by God's own finger. Together, the chapter teaches that God's Spirit equips for His "
            "work, and His covenant rhythm defines the boundaries of that work."
        ),
        "original_language_notes": [
            {
                "term": "Rûaḥ ʾElōhîm",
                "language": "Hebrew",
                "verse": "Exodus 31:3",
                "words_used": "רוּחַ אֱלֹהִים (Rûaḥ ʾElōhîm) — 'Spirit of God'",
                "meaning": "The first explicit statement in Scripture of a person being 'filled' (מָלֵא, *māleʾ*) with the Spirit of God—and it is in the context of artistic craftsmanship. The same Spirit who hovered over creation (Gen. 1:2) now fills a craftsman to create God's earthly dwelling. This is a theological statement that artistry, when consecrated to God, is genuinely Spirit-empowered work."
            },
            {
                "term": "ḥokmāh",
                "language": "Hebrew",
                "verse": "Exodus 31:3",
                "words_used": "חָכְמָה (ḥokmāh) — 'wisdom'",
                "meaning": "The primary Hebrew word for wisdom, used here for Bezalel's craftsmanship skill. In the Old Testament, wisdom is not merely abstract intellectual capacity—it is skilled, practical expertise applied in accordance with God's revealed purposes. Calling Bezalel's artisan skill 'wisdom' elevates it to the same category as divine wisdom in Proverbs (3:19–20; 8:22–31), which God used in creation."
            },
            {
                "term": "ʾōt",
                "language": "Hebrew",
                "verse": "Exodus 31:13",
                "words_used": "אוֹת (ʾōt) — 'sign'",
                "meaning": "A visible, tangible marker or token of covenant relationship. Used of the rainbow (Gen. 9:12), circumcision (Gen. 17:11), the plagues (Exod. 10:1), and here the Sabbath. Calling the Sabbath an *ʾōt* places it alongside these major covenant signs—it is not merely a wellness practice but a weekly declaration of Israel's identity as the covenant people of the LORD."
            },
            {
                "term": "wayyinnāpash",
                "language": "Hebrew",
                "verse": "Exodus 31:17",
                "words_used": "וַיִּנָּפַשׁ (wayyinnāpash) — 'and he rested/was refreshed'",
                "meaning": "From נֶפֶשׁ (*nefeš*), 'soul/breath/life.' The verb means to rest in a way that is refreshing or life-giving—'to catch one's breath.' Used here of God's seventh-day rest and in Exodus 23:12 of humans and animals needing the Sabbath. The anthropomorphism is deliberate: the Sabbath is characterised by soul-nourishing, life-giving completion and satisfaction, not mere cessation."
            },
            {
                "term": "ʾeṣbaʿ ʾElōhîm",
                "language": "Hebrew",
                "verse": "Exodus 31:18",
                "words_used": "אֶצְבַּע אֱלֹהִים (ʾeṣbaʿ ʾElōhîm) — 'finger of God'",
                "meaning": "An anthropomorphism expressing God's direct, personal action without human mediation. The phrase appears in Exodus 8:19 (the magicians recognising the plagues as God's direct work) and here (God directly inscribing the Law). The 'finger of God' in Luke 11:20 (parallel to Matthew 12:28's 'Spirit of God') indicates that Jesus' miracles demonstrate God's direct, unmediated power at work."
            }
        ],
        "moral_lessons": [
            "All human skill, when offered to God's purposes, is Spirit-empowered work—there is no sacred/secular divide.",
            "Spirit-filling does not override obedience; Bezalel's Spirit-given skill was employed precisely in following God's design.",
            "The Sabbath rest declares that God, not our labour, is the foundation of our identity and security.",
            "Even the holiest work must yield to God's covenant rhythms—no project, however important, exempts us from rest.",
            "The Sabbath is a sign of sanctification: our resting in God testifies that He is the One who makes us holy."
        ],
        "application": (
            "Whatever your skills—technical, artistic, administrative, manual—they are Spirit-given. "
            "Offer them to God's purposes, and you are doing sacred work. Resist the secular/spiritual "
            "divide in how you think about your abilities. Then practice Sabbath rest: not as "
            "legalism, but as a weekly covenant act that declares 'my life is not defined by my "
            "productivity.' In Christ, you have entered a rest that is deeper than one day per week—"
            "the rest of finished redemption. Live from that place of sufficiency, and let it shape "
            "every day, especially the one set aside."
        ),
        "prayer": (
            "Lord, thank You for filling Bezalel with Your Spirit and showing me that every skill "
            "You give is sacred when offered to You. Consecrate my abilities, whatever they are, "
            "for Your purposes. Teach me the discipline and delight of Sabbath rest—the weekly "
            "declaration that You are my sufficiency, not my effort. And let me rest daily in "
            "Christ's finished work, entering the true Sabbath of a soul at peace with God. Amen."
        ),
        "key_points": [
            "The first person in Scripture explicitly filled with the Spirit of God (Exodus 31:3) was an artisan, not a prophet or priest—Bezalel the craftsman.",
            "Bezalel and Oholiab represented Judah and Dan—the southernmost and northernmost tribes—symbolising all Israel participating in building God's dwelling.",
            "The Sabbath was given as a covenant sign (*ʾōt*) between God and Israel, marking them as His people just as surely as circumcision did.",
            "The violation of the Sabbath carried the death penalty, even during Tabernacle construction—no holy project overrides the holy rhythm of rest.",
            "The Sabbath was grounded in creation (v. 17) and points forward to the ultimate rest in Christ (Heb. 4:9–11)."
        ],
        "study_questions": [
            "Why is it significant that the first person described as 'filled with the Spirit of God' was an artisan? What does this say about the relationship between the Holy Spirit and human creativity/craftsmanship?",
            "God chose craftsmen from both Judah (Bezalel) and Dan (Oholiab). What might the inclusion of different tribes in the Tabernacle project signify about the nature of community worship?",
            "The Sabbath is called an '*ʾōt*' (sign). What does it mean for a weekly rest to function as a covenant sign? How is this similar to or different from baptism and the Lord's Supper in the New Testament?",
            "The death penalty for Sabbath violation seems extreme. What does the severity of this command reveal about what God thought was at stake in Israel's Sabbath observance?",
            "Hebrews 4:9–11 speaks of a 'Sabbath rest' for the people of God that is still available. How does Christ fulfil and supersede the Mosaic Sabbath? What does entering God's rest look like practically for a believer today?"
        ],
        "tags": ["exodus", "Bezalel", "Holy Spirit", "craftsmanship", "Sabbath", "covenant sign", "rest", "stone tablets", "gifts of the Spirit", "Christ"],
        "sources": ["Exodus 31:1-18", "Hebrews 4:1-11", "Matthew 12:8", "John 19:30", "1 Corinthians 12:4-11", "Ephesians 2:21-22", "Ephesians 4:7-12", "Genesis 1:2", "Proverbs 3:19-20"]
    }
}


def get_connection():
    return sqlite3.connect(DB_PATH)


def get_collection_id(conn):
    c = conn.cursor()
    c.execute("SELECT id FROM commentary_collections WHERE slug='believers-sword-commentaries' AND deleted_at IS NULL LIMIT 1")
    row = c.fetchone()
    return row[0] if row else None


def already_exists(conn, collection_id, book_id, chapter):
    c = conn.cursor()
    c.execute(
        "SELECT id, length(content) FROM commentary_entries "
        "WHERE collection_id=? AND book_id=? AND chapter=? AND language_code='en' "
        "AND reference_scope='chapter' AND deleted_at IS NULL LIMIT 1",
        (collection_id, book_id, chapter)
    )
    row = c.fetchone()
    if row:
        entry_id, content_len = row
        if content_len and content_len > 500:
            return True
    return False


def insert_entry(conn, collection_id, chapter_num, data, batch_uuid):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    entry_uuid = str(uuid.uuid4())
    c = conn.cursor()
    c.execute("""
        INSERT INTO commentary_entries (
            uuid, collection_id, book_id, chapter, verse_start, verse_end,
            reference_scope, title, summary, content, application, prayer,
            key_points, study_questions, language_code, theological_perspective,
            status, is_ai_generated, ai_generation_batch_uuid, word_count,
            created_at, updated_at
        ) VALUES (?,?,?,?,NULL,NULL,?,?,?,?,?,?,?,?,?,?,?,1,?,?,?,?)
    """, (
        entry_uuid,
        collection_id,
        BOOK_ID,
        chapter_num,
        'chapter',
        data['title'],
        data['summary'],
        data['content'],
        data['application'],
        data['prayer'],
        json.dumps(data['key_points']),
        json.dumps(data['study_questions']),
        'en',
        'evangelical',
        'draft',
        batch_uuid,
        len(data['content'].split()),
        now,
        now
    ))
    conn.commit()
    return entry_uuid, now


def save_json(chapter_num, data, entry_uuid, created_at, updated_at):
    chapter_dir = os.path.join(GENERATED_DIR, BOOK_DIR)
    os.makedirs(chapter_dir, exist_ok=True)
    filename = os.path.join(chapter_dir, f"{chapter_num:02d}.json")
    payload = {
        "uuid": entry_uuid,
        "collection_name": COLLECTION_NAME,
        "author_type": "ai",
        "language_code": "en",
        "theological_perspective": "evangelical",
        "status": "draft",
        "book_id": BOOK_ID,
        "book": BOOK,
        "chapter": chapter_num,
        "title": data['title'],
        "summary": data['summary'],
        "content": data['content'],
        "chapter_overview": data['chapter_overview'],
        "original_language_notes": data['original_language_notes'],
        "moral_lessons": data['moral_lessons'],
        "application": data['application'],
        "prayer": data['prayer'],
        "key_points": data['key_points'],
        "study_questions": data['study_questions'],
        "tags": data['tags'],
        "sources": data['sources'],
        "created_at": created_at,
        "updated_at": updated_at
    }
    # Verify no forbidden keys
    forbidden = {'is_ai_generated', 'model_name', 'prompt_version'}
    assert not (set(payload.keys()) & forbidden), f"Forbidden keys found: {set(payload.keys()) & forbidden}"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    # Verify it parses
    with open(filename, 'r', encoding='utf-8') as f:
        verify = json.load(f)
    assert not (set(verify.keys()) & forbidden), "Forbidden keys in verified file"
    return filename


def update_progress(next_chapter):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    if next_chapter > 40:
        # Exodus done, move to Leviticus
        progress = {
            "next_book_id": 3,
            "next_book": "Leviticus",
            "next_chapter": 1,
            "last_completed_book_id": 2,
            "last_completed_book": "Exodus",
            "last_completed_chapter": 40,
            "completed": False,
            "updated_at": now
        }
    else:
        progress = {
            "next_book_id": 2,
            "next_book": "Exodus",
            "next_chapter": next_chapter,
            "last_completed_book_id": 2,
            "last_completed_book": "Exodus",
            "last_completed_chapter": next_chapter - 1,
            "completed": False,
            "updated_at": now
        }
    with open(PROGRESS_JSON, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2)
    # Update DB progress table
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='commentary_generation_progress'")
    if c.fetchone():
        c.execute("""
            INSERT OR REPLACE INTO commentary_generation_progress
            (id, next_book_id, next_book, next_chapter, last_completed_book_id,
             last_completed_book, last_completed_chapter, completed, updated_at)
            VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            progress['next_book_id'], progress['next_book'], progress['next_chapter'],
            progress['last_completed_book_id'], progress['last_completed_book'],
            progress['last_completed_chapter'], 0, now
        ))
        conn.commit()
    conn.close()
    return progress


def append_log(batch_uuid, start_ref, end_ref, generated, skipped, inserted, files):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    entry = {
        "timestamp": now,
        "generation_batch_id": batch_uuid,
        "start_reference": start_ref,
        "end_reference": end_ref,
        "chapters_generated": generated,
        "chapters_skipped": skipped,
        "db_rows_inserted": inserted,
        "files_written": files
    }
    with open(LOG_JSONL, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')


def main():
    batch_uuid = str(uuid.uuid4())
    conn = get_connection()
    collection_id = get_collection_id(conn)
    assert collection_id, "Collection not found!"

    chapters_to_generate = sorted(CHAPTERS.keys())  # [27,28,29,30,31]
    generated = 0
    skipped = 0
    inserted = 0
    files_written = []
    start_ref = f"Exodus {chapters_to_generate[0]}"
    end_ref = f"Exodus {chapters_to_generate[-1]}"
    last_chapter = chapters_to_generate[0]

    for ch in chapters_to_generate:
        if already_exists(conn, collection_id, BOOK_ID, ch):
            print(f"SKIP: Exodus {ch} already exists with substantial content.")
            skipped += 1
            last_chapter = ch
            continue

        data = CHAPTERS[ch]
        entry_uuid, created_at = insert_entry(conn, collection_id, ch, data, batch_uuid)
        filepath = save_json(ch, data, entry_uuid, created_at, created_at)
        print(f"GEN:  Exodus {ch} — '{data['title']}' | UUID={entry_uuid}")
        generated += 1
        inserted += 1
        files_written.append(filepath)
        last_chapter = ch

    conn.close()

    next_chapter = last_chapter + 1
    progress = update_progress(next_chapter)
    append_log(batch_uuid, start_ref, end_ref, generated, skipped, inserted, files_written)

    print(f"\n--- SUMMARY ---")
    print(f"Generated: {generated} chapters | Skipped: {skipped} | DB rows inserted: {inserted}")
    print(f"Files written: {len(files_written)}")
    for f in files_written:
        print(f"  {f}")
    print(f"Next starting reference: {progress['next_book']} {progress['next_chapter']}")


if __name__ == '__main__':
    main()
