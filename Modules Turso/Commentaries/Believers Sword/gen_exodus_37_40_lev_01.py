#!/usr/bin/env python3
"""
Generate commentaries for Exodus 37-40 and Leviticus 1.
Continues from progress checkpoint: Exodus 36 completed.
"""

import sqlite3, json, uuid, os, datetime

DB_PATH = "believers_sword_commentaries.db"
GENERATED_DIR = "generated"
PROGRESS_JSON = "commentary_generation_progress.json"
LOG_FILE = "commentary_generation_log.jsonl"

NOW = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
BATCH_UUID = str(uuid.uuid4())

COMMENTARIES = [
    # ── Exodus 37 ─────────────────────────────────────────────────────────────
    {
        "book_id": 2,
        "book": "Exodus",
        "chapter": 37,
        "title": "The Sacred Furnishings: Ark, Table, Lampstand, and Incense Altar",
        "summary": (
            "Bezalel crafts the four holiest furnishings of the Tabernacle: the Ark of the "
            "Covenant with its golden mercy seat and cherubim, the table of showbread, the "
            "golden lampstand with its seven branches, and the altar of incense. Each piece "
            "precisely matches God's specifications, embodying theological truths about "
            "God's presence, provision, light, and intercession."
        ),
        "content": (
            "Exodus 37 records Bezalel's personal crafting of the four most sacred objects "
            "in Israel's worship—each destined for the Most Holy Place or the Holy Place, "
            "each a theological statement about how humanity approaches the living God.\n\n"
            "**The Ark of the Covenant (vv. 1-9)**\n\n"
            "Bezalel builds the Ark (אָרוֹן, *aron*) of acacia wood overlaid inside and out "
            "with pure gold—2.5 cubits long, 1.5 cubits wide, 1.5 cubits high. The gold "
            "molding, rings, and poles ensure it can be carried without being touched. This "
            "portability is intentional: God's presence travels *with* His people, not merely "
            "residing in fixed geography.\n\n"
            "The mercy seat (כַּפֹּרֶת, *kapporet*) is beaten from a single piece of pure gold, "
            "with two cherubim of hammered gold facing each other, wings spread overhead. "
            "Between them is where God would speak (25:22)—this is the *throne* of the "
            "invisible God. The term *kapporet* comes from the root כפר (*kapar*)—to cover, "
            "to atone. It is the site of atonement on Yom Kippur when the high priest "
            "sprinkled blood there (Lev. 16). The New Testament identifies Christ as the "
            "fulfillment: 'God presented Christ as a sacrifice of atonement [Greek: *hilasterion*, "
            "the same word the LXX uses for *kapporet*]' (Romans 3:25). Jesus is the mercy seat "
            "in human flesh—God's throne meeting our guilt, covered by blood.\n\n"
            "**The Table of Showbread (vv. 10-16)**\n\n"
            "The table of acacia wood overlaid with gold (2 cubits × 1 cubit × 1.5 cubits) "
            "held the twelve loaves of the Presence—bread placed before God continually, "
            "representing Israel's twelve tribes in perpetual fellowship with God. Eating "
            "and fellowship are inseparable in Scripture; the table symbolizes covenant "
            "communion. Christ fulfills this as the Bread of Life (John 6:35, 48), whose "
            "body given for us is the ultimate bread of presence.\n\n"
            "**The Golden Lampstand (vv. 17-24)**\n\n"
            "The menorah (מְנוֹרָה, *menorah*) was beaten from a single talent of pure gold—"
            "no joints, no assembly, but one continuous hammered form. Its seven branches "
            "with cups shaped like almond blossoms provided the only light in the Holy "
            "Place. The number seven speaks of completeness; the almond form (שָׁקֵד, *shaqed*) "
            "resonates with God's watchfulness (Jer. 1:11-12, where almond imagery signals "
            "God's vigilance). Christ is the Light of the World (John 8:12), and the Church "
            "is called to be lampstands bearing His light (Rev. 1:20).\n\n"
            "**The Altar of Incense (vv. 25-29)**\n\n"
            "The incense altar of acacia wood overlaid with gold (1 cubit × 1 cubit × 2 "
            "cubits high) stood directly before the veil separating the Holy Place from "
            "the Most Holy Place. Incense burned on it morning and evening—the ascending "
            "smoke a perpetual picture of prayer rising before God (Ps. 141:2; Rev. 5:8; "
            "8:3-4). Bezalel also prepares the holy anointing oil and the pure incense "
            "(v. 29), the fragrant formula given in 30:23-38. These are not "
            "manufactured for personal use but consecrated exclusively for God's sanctuary—"
            "a reminder that worship belongs to God alone and cannot be domesticated.\n\n"
            "**The Craftsman as Theologian**\n\n"
            "Bezalel's work here is explicitly theological. The Hebrew says he *made* (*asah*) "
            "each item—the same verb used of God's creative acts in Genesis 1. The skilled "
            "craftsman, filled with God's Spirit (31:3), becomes an instrument of revelation: "
            "his art shapes the means by which Israel will know and approach their God. "
            "Every dimension, material, and form is a lesson in holiness, atonement, "
            "provision, light, and prayer."
        ),
        "chapter_overview": (
            "Bezalel makes the Ark and mercy seat with cherubim; the table of showbread; "
            "the seven-branched golden lampstand hammered from one piece; and the golden "
            "altar of incense, along with the holy anointing oil and pure incense."
        ),
        "original_language_notes": [
            {
                "term": "כַּפֹּרֶת (kapporet)",
                "language": "Hebrew",
                "verse": "37:6",
                "words_used": ["mercy seat", "atonement cover", "propitiation cover"],
                "meaning": (
                    "Atonement cover, mercy seat. From the root כפר (kapar)—to cover, atone, "
                    "ransom. This is the lid of the Ark where the high priest sprinkled blood "
                    "on Yom Kippur. The Septuagint translates it *hilasterion*, which Paul uses "
                    "in Romans 3:25 for Christ: the ultimate mercy seat where divine justice and "
                    "mercy meet."
                )
            },
            {
                "term": "מְנוֹרָה (menorah)",
                "language": "Hebrew",
                "verse": "37:17",
                "words_used": ["lampstand", "candlestick"],
                "meaning": (
                    "Lampstand. From the root נור (nur)—to give light. The menorah was hammered "
                    "from one solid piece of gold—a remarkable feat of craftsmanship. Its seven "
                    "branches with almond-blossom cups speak of complete illumination. The "
                    "Revelation's seven lampstands (Rev. 1:12, 20) echo this imagery, representing "
                    "the Church as bearers of divine light."
                )
            },
            {
                "term": "שָׁקֵד (shaqed)",
                "language": "Hebrew",
                "verse": "37:19",
                "words_used": ["almond blossoms", "almond"],
                "meaning": (
                    "Almond. In Jeremiah 1:11-12, God uses an almond branch (shaqed) as a "
                    "wordplay on 'watching' (shoqed)—'I am watching to perform my word.' The "
                    "almond blossoms on the menorah cups may carry this same nuance: the light "
                    "in God's house burns under His watchful care."
                )
            },
            {
                "term": "אָרוֹן (aron)",
                "language": "Hebrew",
                "verse": "37:1",
                "words_used": ["ark", "chest", "box"],
                "meaning": (
                    "Box, chest, ark. The same word is used for the chest in which baby Moses "
                    "was placed (Exod. 2:3). The Ark is a container—it held the tablets of the "
                    "law, Aaron's staff, and the manna jar. But its significance lies above, "
                    "at the mercy seat, where God dwells and speaks. The Ark is the meeting "
                    "point of law and grace."
                )
            },
            {
                "term": "מִקְשָׁה (miqshah)",
                "language": "Hebrew",
                "verse": "37:22",
                "words_used": ["hammered work", "beaten work"],
                "meaning": (
                    "Hammered work, beaten from a single piece. The menorah was not assembled "
                    "from parts but beaten into shape from one talent of gold. This *miqshah* "
                    "construction emphasizes unity and purity—no seams, no solder, no joins—"
                    "fitting for the symbol of God's undivided light."
                )
            }
        ],
        "moral_lessons": [
            "God's presence demands the finest—gold, craftsmanship, precision—not because He needs luxury, but because what we bring reflects what we believe about Him.",
            "The mercy seat reminds us that access to God is always through atonement; we do not come to Him on the basis of our own merit.",
            "The lampstand as a single beaten piece pictures the unity required of the Church: one body, one light source, many branches.",
            "The incense altar teaches that prayer is not optional supplementary worship—it is built into the very architecture of approaching God.",
            "Every sacred item had poles for carrying—God's presence is not stationary. He walks with His people through every wilderness season.",
            "The table of bread before God pictures ongoing communion: the Christian life is not just crisis moments of prayer but continual fellowship at God's table."
        ],
        "application": (
            "Exodus 37 invites us to reflect on how we approach God. The four furnishings represent "
            "four dimensions of the spiritual life: atonement (ark/mercy seat), fellowship and "
            "provision (table), illumination and witness (lampstand), and prayer (incense altar). "
            "Every believer needs all four—a deep awareness of forgiveness through Christ's "
            "atonement, ongoing communion at His table, being carriers of His light, and a "
            "consistent, ascending prayer life. Bezalel's careful craftsmanship also challenges "
            "us to bring our best skills and creativity into God's service. What we offer to God "
            "should be thoughtful, excellent, and shaped by His specifications—not our own "
            "convenience."
        ),
        "prayer": (
            "Lord Jesus, You are our Ark—the place where law and mercy meet. You are our Bread of "
            "Life, our Light, and our Great High Priest at the altar of intercession. May we "
            "approach You through the atonement You have accomplished, feed on You as the Bread "
            "of Life, carry Your light into darkness, and never cease the incense of prayer. As "
            "Bezalel poured his finest skill into sacred work, may we offer You the very best of "
            "who we are. Amen."
        ),
        "key_points": [
            "Bezalel makes the Ark and kapporet (mercy seat)—the atonement center of Israel's worship, fulfilled in Christ as *hilasterion* (Romans 3:25).",
            "The table of showbread represents perpetual covenant fellowship between God and Israel, fulfilled in Christ as the Bread of Life.",
            "The menorah, beaten from one piece of gold, symbolizes complete divine light and unity—Christ is the Light of the World.",
            "The incense altar positioned before the veil pictures prayer as the constant activity of the worshipping community.",
            "All furnishings had poles for transport, showing that God's presence accompanies His people on their journey.",
            "Bezalel's Spirit-filled craftsmanship models the integration of skill, creativity, and obedience in service to God."
        ],
        "study_questions": [
            "The mercy seat (kapporet) literally means 'atonement cover.' How does Paul's use of *hilasterion* in Romans 3:25 connect Christ to this object?",
            "The table of showbread kept twelve loaves before God perpetually. What does this continual presence of the twelve tribes' bread suggest about God's relationship with His people?",
            "The menorah was hammered from one solid piece of gold. What does this unity of material suggest about the nature of divine light and the Church's witness?",
            "Why was the incense altar placed immediately before the veil to the Most Holy Place? What does its location teach about the relationship between prayer and God's presence?",
            "Every sacred furnishing had carrying poles. What does this mobility suggest about God's character and His intentions for His people?",
            "How do the four furnishings (Ark, table, lampstand, incense altar) map onto dimensions of the Christian spiritual life?",
            "Bezalel is described as filled with God's Spirit for artistic work (31:3). How does this challenge the sacred/secular divide in how we think about vocation?"
        ],
        "tags": ["Tabernacle", "Ark of the Covenant", "mercy seat", "atonement", "lampstand", "incense", "Bezalel", "furnishings", "Exodus", "worship"],
        "sources": ["Exodus 37", "Romans 3:25", "John 6:35", "John 8:12", "Revelation 1:20", "Leviticus 16", "Psalm 141:2", "Hebrews 9:4-5"]
    },

    # ── Exodus 38 ─────────────────────────────────────────────────────────────
    {
        "book_id": 2,
        "book": "Exodus",
        "chapter": 38,
        "title": "The Altar, the Laver, the Courtyard, and the Inventory of Materials",
        "summary": (
            "Bezalel constructs the bronze altar of burnt offering and the bronze laver, then "
            "the courtyard of the Tabernacle with its linen curtains and bronze-socketed posts. "
            "The chapter closes with a precise inventory of the gold, silver, and bronze donated "
            "and used—showing the community's extraordinary generosity and God's faithful accounting."
        ),
        "content": (
            "Exodus 38 moves from the interior furnishings to the outer structures: the altar "
            "where sacrifice happens, the laver where priests are cleansed, and the courtyard "
            "that defines sacred space. It closes with a rare financial accounting of all "
            "materials used—testimony to both the generosity of the people and the integrity "
            "of God's leaders.\n\n"
            "**The Altar of Burnt Offering (vv. 1-7)**\n\n"
            "The altar (מִזְבֵּחַ, *mizbeach*) is built of acacia wood overlaid with bronze—5 "
            "cubits square and 3 cubits high. Its grating of bronze network, rings, and poles "
            "make it portable. All of the altar's utensils (pots, shovels, basins, forks, "
            "firepans) were bronze.\n\n"
            "The altar stood at the entrance of the Tabernacle court—the very first object "
            "encountered. You could not enter God's presence without passing the altar. This "
            "is profoundly theological: there is no access to God without sacrifice. The smoke "
            "of offerings ascending heavenward anticipates Christ's 'one sacrifice for sins "
            "forever' (Heb. 10:12). Every animal offered on this altar pointed forward; the "
            "altar itself is a sermon in bronze and wood: *sin has a cost, and that cost must "
            "be paid*.\n\n"
            "**The Bronze Laver (v. 8)**\n\n"
            "The laver (כִּיּוֹר, *kiyor*)—a basin for priestly washing—is made from the "
            "bronze mirrors of the women who served at the entrance of the tent of meeting. "
            "This single verse is striking on multiple levels. First, women are acknowledged "
            "as having a recognized ministry role—they 'served' (Hebrew: *tsava*, a word used "
            "for military service) at the tent entrance. Second, their mirrors—objects of "
            "personal vanity and appearance—are transformed into an instrument of priestly "
            "holiness. What was used to see oneself is remade into what enables priests to "
            "serve God: a beautiful picture of consecration—personal beauty yielded for "
            "communal sanctity.\n\n"
            "The laver enabled priests to wash before entering the tabernacle—an outer "
            "ritual of inner necessity. John 13:10 and Ephesians 5:26 speak of Christ "
            "washing His bride with water through the Word; Titus 3:5 refers to the "
            "'washing of regeneration.' The laver anticipates baptism and the cleansing "
            "of the Holy Spirit that must precede ministry.\n\n"
            "**The Courtyard (vv. 9-20)**\n\n"
            "The rectangular courtyard (100 × 50 cubits) was enclosed by linen curtains "
            "5 cubits high, hung from silver hooks on bronze-socketed posts. The entrance "
            "gate on the east side was a 20-cubit screen of embroidered linen—more ornate "
            "than the plain white walls, marking it as the one way in.\n\n"
            "The single gate on the east echoes Eden's cherub-guarded eastern gate (Gen. 3:24) "
            "and anticipates Christ's declaration, 'I am the door' (John 10:9). There is "
            "one way into God's presence, and that way is prescribed, gracious, and clear.\n\n"
            "**The Inventory of Materials (vv. 21-31)**\n\n"
            "Ithamar son of Aaron recorded the materials under Bezalel and Oholiab's oversight: "
            "29 talents and 730 shekels of gold; 100 talents and 1,775 shekels of silver; "
            "70 talents and 2,400 shekels of bronze. The silver (100 talents) came entirely "
            "from the census half-shekel—one talent per socket for the 100 sockets of the "
            "frames and the bases of the pillars of the veil. The 1,775 shekels remaining "
            "were used for the pillar hooks.\n\n"
            "This audit serves multiple purposes. It honors the donors by accounting for "
            "every contribution. It models integrity in financial stewardship. And it reveals "
            "the scale of the community's sacrifice: tons of precious metal freely given for "
            "God's dwelling. Paul echoes this principle: each person should give 'as he has "
            "decided in his heart, not reluctantly or under compulsion' (2 Cor. 9:7)."
        ),
        "chapter_overview": (
            "Construction of the bronze altar of burnt offering; the bronze laver made from "
            "women's mirrors; the Tabernacle courtyard with its linen walls and single "
            "entrance gate; detailed financial inventory of all gold, silver, and bronze used."
        ),
        "original_language_notes": [
            {
                "term": "מִזְבֵּחַ (mizbeach)",
                "language": "Hebrew",
                "verse": "38:1",
                "words_used": ["altar"],
                "meaning": (
                    "Altar. From the root זבח (zabach)—to slaughter, to sacrifice. The mizbeach "
                    "is literally 'a place of slaughter.' Its positioning at the Tabernacle "
                    "entrance is theologically deliberate: every approach to God begins with "
                    "acknowledging the need for atoning sacrifice."
                )
            },
            {
                "term": "כִּיּוֹר (kiyor)",
                "language": "Hebrew",
                "verse": "38:8",
                "words_used": ["laver", "basin", "washbasin"],
                "meaning": (
                    "Basin, laver, pot. The kiyor was a large basin for the priestly washings "
                    "required before entering the Tabernacle. Made from bronze mirrors, it "
                    "connects outward purification with inward consecration. The connection "
                    "between washing and ministry runs throughout Scripture (John 13; Eph. 5:26; "
                    "Titus 3:5)."
                )
            },
            {
                "term": "צָבָא (tsava)",
                "language": "Hebrew",
                "verse": "38:8",
                "words_used": ["served", "ministered", "assembled"],
                "meaning": (
                    "To serve, to assemble for service, to wage war. The women who donated their "
                    "mirrors are described as 'serving' at the tent entrance using this word—the "
                    "same root as 'armies' (tsavaot) in 'Lord of hosts/armies.' Their service "
                    "at the tent was considered a form of holy warfare—a remarkable elevation "
                    "of their role."
                )
            },
            {
                "term": "עָמוּד (amud)",
                "language": "Hebrew",
                "verse": "38:10",
                "words_used": ["pillar", "post", "column"],
                "meaning": (
                    "Pillar, post, column. The courtyard's framework of pillars defined sacred "
                    "space from profane space. The word is also used for the pillar of cloud "
                    "and fire (Exod. 13:21)—a subtle connection between structural pillars "
                    "and the divine pillar that guided Israel."
                )
            },
            {
                "term": "כִּכָּר (kikkar)",
                "language": "Hebrew",
                "verse": "38:24",
                "words_used": ["talent"],
                "meaning": (
                    "Talent, a unit of weight and value. One talent ≈ 34 kg / 75 lbs. "
                    "29 talents of gold represents roughly 1,000 kg of gold given by the "
                    "community. This accounting demonstrates the extraordinary scale of "
                    "Israel's generosity and the reliability of its leaders."
                )
            }
        ],
        "moral_lessons": [
            "Access to God begins at the altar—there is no approach to holiness without dealing with sin through the sacrifice God provides.",
            "The laver's origin in women's mirrors illustrates that personal vanity can be surrendered to become instruments of holy service.",
            "The single gate teaches that God's way of access is particular—there is one door to God, and it is through Christ (John 10:9).",
            "Financial transparency in ministry honors both the givers and God—the careful inventory models integrity in stewardship.",
            "The courtyard's walls created boundary between sacred and ordinary—holiness involves clear distinctions, not blurring of categories.",
            "Even the most mundane materials (bronze, linen) when dedicated to God's purpose become vehicles of His presence and glory."
        ],
        "application": (
            "Exodus 38 presents a striking contrast: vanity transformed into sanctity (the mirrors becoming the laver), and personal beauty surrendered "
            "for communal holiness. In Christ, we are called to the same kind of transformation—giving what we treasure for the sake of His house. "
            "The chapter's detailed financial audit challenges churches and ministries to model the same integrity: every contribution is known "
            "and accounted for. The altar at the entrance also remains relevant: we do not enter God's presence presumptuously. We come through "
            "the sacrifice of Christ—the one altar whose work is 'once for all.'"
        ),
        "prayer": (
            "Father, as the women yielded their mirrors for Your service, may we surrender what we use to see ourselves—our image, our reputation, "
            "our self-focus—to become instruments of Your glory. Thank You that Christ is our altar and our laver—the one through whom our sins "
            "are atoned and our lives are cleansed. May we steward what You have given with integrity, generosity, and joy. Amen."
        ),
        "key_points": [
            "The altar of burnt offering stood at the entrance—no one could approach God's presence without first passing the place of sacrifice.",
            "The bronze laver was made from women's mirrors—a picture of personal beauty yielded to priestly holiness.",
            "The single courtyard gate anticipates Christ as 'the door'—there is one prescribed way into God's presence.",
            "The detailed inventory of gold, silver, and bronze models financial integrity and honors every donor's contribution.",
            "The census silver (one talent per socket) built the very foundation of the Tabernacle—each redeemed person literally holds up God's dwelling.",
            "The entire Tabernacle enterprise demonstrates that generous, willing worship transforms communities."
        ],
        "study_questions": [
            "Why was the altar placed at the very entrance of the Tabernacle court? What does this positioning communicate about approaching God?",
            "The laver was made from the bronze mirrors of serving women. What does the transformation of mirrors into a priestly wash basin suggest about consecration?",
            "The women who donated their mirrors are said to have 'served' (tsava) at the tent entrance—a word related to 'armies.' What does this suggest about the nature of their ministry?",
            "The Tabernacle had only one gate. How does this relate to Jesus's statement, 'I am the door' (John 10:9)?",
            "Why do you think the text provides such a detailed financial accounting (vv. 21-31)? What values does this inventory reflect?",
            "The atonement-money silver became the foundation sockets. How does this reinforce the theme that God's presence rests on atonement?",
            "How does the principle of the altar—that sin has a cost and sacrifice is required—apply to the New Testament believer who knows Christ has paid that cost?"
        ],
        "tags": ["altar", "laver", "courtyard", "bronze", "sacrifice", "atonement", "stewardship", "Tabernacle", "Exodus", "worship"],
        "sources": ["Exodus 38", "Hebrews 10:12", "John 10:9", "John 13:10", "Ephesians 5:26", "2 Corinthians 9:7", "Titus 3:5"]
    },

    # ── Exodus 39 ─────────────────────────────────────────────────────────────
    {
        "book_id": 2,
        "book": "Exodus",
        "chapter": 39,
        "title": "Priestly Garments Completed: Clothed for Holy Service",
        "summary": (
            "The priestly garments—ephod, breastplate, robe, tunic, turban, and sash—are "
            "carefully crafted according to God's exact specifications. The breastplate bears "
            "twelve gemstones with the names of Israel's tribes, and the golden plate on "
            "Aaron's turban reads 'Holy to the LORD.' When all the work is finished, Moses "
            "inspects it and blesses the people, for they have done everything just as God commanded."
        ),
        "content": (
            "Exodus 39 narrates the completion of the priestly wardrobe—garments that are not "
            "merely uniform but theology worn on the body. The chapter is framed by a repeated "
            "refrain: 'as the LORD commanded Moses' (vv. 1, 5, 7, 21, 26, 29, 31)—seven times, "
            "the number of completeness. Full obedience is total obedience.\n\n"
            "**The Ephod (vv. 2-7)**\n\n"
            "The ephod (אֵפוֹד, *ephod*) was a priestly vest or apron of gold, blue, purple, "
            "and scarlet threads woven into fine linen. Two onyx stones on the shoulder straps "
            "bore the names of Israel's twelve tribes—six names on each stone, engraved like a "
            "signet ring. Aaron carried the names of all Israel on his *shoulders* when he "
            "entered God's presence: a memorial before the LORD (v. 7). The high priest did not "
            "go in alone; he bore the whole people with him. This is the theology of "
            "intercession—the priest represents the people before God.\n\n"
            "Christ, our great High Priest, enters the Most Holy Place bearing His people "
            "(Heb. 4:14-16). The names engraved on Aaron's shoulders anticipate the truth that "
            "we are known and held by our Intercessor.\n\n"
            "**The Breastplate (vv. 8-21)**\n\n"
            "The breastplate (חֹשֶׁן, *choshen*) of judgment—a square of doubled fabric "
            "holding twelve gems in four rows, each engraved with a tribal name—rested "
            "over Aaron's heart. Not only did he carry Israel on his shoulders but also over "
            "his heart. The breastplate also held the Urim and Thummim (v. 21)—mysterious "
            "sacred lots by which divine guidance was sought.\n\n"
            "The image is deeply relational: the priest carries his people both on his "
            "back (strength, intercession, sustaining) and on his chest (affection, care, "
            "love). Christ carries His people in exactly this way—interceding with authority "
            "and loving with compassion. 'He always lives to make intercession for them' "
            "(Heb. 7:25).\n\n"
            "**The Robe of the Ephod (vv. 22-26)**\n\n"
            "The solid blue robe had an opening reinforced like armor so it could not tear, "
            "and around its hem alternated pomegranates of blue, purple, and scarlet and "
            "golden bells. The bells rang as the high priest moved in the Most Holy Place—"
            "a sound of life, an audible signal that he still lived before God. Jewish "
            "tradition says the absence of the bells would signal the priest's death "
            "from unholy approach.\n\n"
            "The ringing bells also announced the priest's coming and going—the people "
            "outside could track his ministry by the sound. Priestly intercession was "
            "acoustically witnessed.\n\n"
            "**The Golden Plate (vv. 27-31)**\n\n"
            "The golden plate (צִיץ, *tzitz*) attached to the front of Aaron's turban bore "
            "the inscription קֹדֶשׁ לַיהוָה (*Qodesh la-YHWH*)—'Holy to the LORD.' This "
            "crown-like inscription declared Aaron's complete dedication. He wore God's "
            "name on his forehead—an echo of Revelation's promise that the redeemed bear "
            "God's name on their foreheads (Rev. 22:4). The tzitz also served a "
            "substitutionary purpose: it bore Israel's iniquities in the holy things "
            "(Exod. 28:38)—the priest absorbed what made the people's worship defiled "
            "so they could approach God acceptably.\n\n"
            "**Moses's Inspection and Blessing (vv. 32-43)**\n\n"
            "The completion of all the Tabernacle work is celebrated with a remarkable "
            "summary: the Israelites did all the work 'according to all that the LORD "
            "had commanded Moses'—and Moses looked at all the work and *blessed them* "
            "(v. 43). The echo of Genesis 1 is intentional. Just as God examined His "
            "creation and saw that it was good, Moses examines God's Tabernacle and "
            "pronounces blessing. The new creation is complete; the holy sanctuary is "
            "ready for God's presence to fill it."
        ),
        "chapter_overview": (
            "Craftsmen complete the priestly ephod with shoulder stones bearing tribal names; "
            "the breastplate of twelve gems; the blue robe with bell-and-pomegranate hem; "
            "the golden plate inscribed 'Holy to the LORD'; all priestly garments finished. "
            "Moses inspects the completed Tabernacle work and blesses the people."
        ),
        "original_language_notes": [
            {
                "term": "אֵפוֹד (ephod)",
                "language": "Hebrew",
                "verse": "39:2",
                "words_used": ["ephod"],
                "meaning": (
                    "Ephod. A priestly garment, likely a vest or apron. Its precise form is "
                    "debated, but its function is clear: it supported the breastplate and bore "
                    "the shoulder stones. The ephod became so associated with divinely-guided "
                    "leadership that later texts use 'wearing an ephod' to signify legitimate "
                    "priestly service (1 Sam. 2:28; 22:18)."
                )
            },
            {
                "term": "חֹשֶׁן (choshen)",
                "language": "Hebrew",
                "verse": "39:8",
                "words_used": ["breastplate", "breastpiece"],
                "meaning": (
                    "Breastplate, breastpiece of judgment. The choshen was a folded square "
                    "fabric holding twelve precious stones engraved with the tribal names. "
                    "Called the 'breastplate of judgment' (28:15)—it held the Urim and "
                    "Thummim (divine lots)—judgment here means discernment/decision-making, "
                    "not condemnation."
                )
            },
            {
                "term": "צִיץ (tzitz)",
                "language": "Hebrew",
                "verse": "39:30",
                "words_used": ["plate", "medallion", "crown", "diadem"],
                "meaning": (
                    "Flower, blossom, plate. The golden front-piece of Aaron's turban. "
                    "The tzitz bore the inscription 'Holy to the LORD' and functioned to "
                    "bear the iniquity of Israel's holy things (28:38)—a substitutionary "
                    "covering for the imperfections in their worship. This is a priestly "
                    "type of Christ who bears our defiled offerings and presents them "
                    "acceptable to the Father."
                )
            },
            {
                "term": "קֹדֶשׁ לַיהוָה (Qodesh la-YHWH)",
                "language": "Hebrew",
                "verse": "39:30",
                "words_used": ["Holy to the LORD"],
                "meaning": (
                    "Holy to the LORD—the inscription on the golden plate. Qodesh (holy, "
                    "set apart) + la (to, for) + YHWH (the personal covenant name of God). "
                    "This dedication phrase appears throughout later Scripture. Zechariah "
                    "14:20-21 envisions the eschatological day when even ordinary cooking "
                    "pots will bear this inscription—holiness democratized to all of life."
                )
            },
            {
                "term": "אוּרִים וְתֻמִּים (Urim and Thummim)",
                "language": "Hebrew",
                "verse": "39:21",
                "words_used": ["Urim and Thummim"],
                "meaning": (
                    "Lights and Perfections (or Curse and Innocence—debated). Sacred lots "
                    "kept in the breastplate pouch, consulted for divine guidance in major "
                    "decisions. Their precise mechanism is unknown, but their presence in "
                    "the breastplate over the priest's heart signifies that discernment "
                    "comes from close proximity to God's presence, not from human wisdom alone."
                )
            }
        ],
        "moral_lessons": [
            "Aaron carried Israel's names on both his shoulders and his heart—strength and love are both required for true intercession.",
            "The tzitz bore Israel's iniquities so their worship could be acceptable—Christ bears our imperfect offerings before the Father.",
            "The phrase 'as the LORD commanded Moses' repeated seven times teaches that obedience is not partial but total.",
            "The bells on the robe made the high priest's ministry audible—God's people should be able to hear and witness their leaders' intercession.",
            "Moses blessing the completed work echoes God's blessing of creation—faithful work done according to God's pattern brings divine approval.",
            "The breastplate gems—twelve tribes, twelve stones—picture God valuing the distinctiveness of each person in His community."
        ],
        "application": (
            "The priestly garments in Exodus 39 are rich with intercession theology. Aaron physically bore Israel before God—on his shoulders "
            "(strength/advocacy) and on his heart (love/compassion). This pattern is fulfilled in Christ, who carries His people into the Father's "
            "presence both as mighty Advocate and as tender Friend. The golden plate inscribed 'Holy to the LORD' challenges every believer: "
            "what would it mean to have this inscription on our minds? Zechariah envisions a day when all of life will be 'holy to the LORD' "
            "(Zech. 14:20). That age is already inaugurated in Christ—every believer is a royal priest, called to live with this inscription "
            "on their whole existence."
        ),
        "prayer": (
            "Lord Jesus, our great High Priest, thank You for carrying our names on Your shoulders and keeping us on Your heart. "
            "Where our worship falls short, You present us acceptable before the Father. Where our obedience is partial, Your perfect "
            "obedience covers us. May the inscription of our hearts be 'Holy to the LORD'—and may we live as people set apart for "
            "Your purposes in every sphere of life. Amen."
        ),
        "key_points": [
            "Aaron carried Israel's twelve tribal names on his shoulders (ephod) and on his heart (breastplate)—intercession requires both strength and love.",
            "The phrase 'as the LORD commanded Moses' appears seven times, marking total obedience as the standard of acceptable worship.",
            "The golden plate inscribed 'Holy to the LORD' symbolizes complete consecration—fulfilled in Christ and called for in believers (1 Pet. 2:9).",
            "The tzitz bore the iniquity of Israel's holy things—a priestly atonement for the deficiency in the people's offerings.",
            "Moses's blessing of the completed work (v. 43) deliberately echoes God's blessing of creation—the Tabernacle is a new-creation act.",
            "The ringing bells on the high priest's robe made intercession audible to the waiting community outside."
        ],
        "study_questions": [
            "Aaron bore the twelve tribal names on both his shoulders and his breastplate (over his heart). What is the theological significance of both locations?",
            "The phrase 'as the LORD commanded Moses' appears seven times in this chapter. Why might the author emphasize this complete obedience so insistently?",
            "How does the function of the tzitz—bearing the iniquity of Israel's holy things—parallel Christ's priestly work (Heb. 7:25)?",
            "The golden plate reads 'Holy to the LORD.' Zechariah 14:20-21 envisions these words on everyday objects. What does this eschatological vision suggest about the goal of history?",
            "Moses's inspection and blessing (vv. 43) echo Genesis 1. What is the author saying by drawing this parallel?",
            "If every believer is now a 'royal priest' (1 Pet. 2:9), what does the breastplate's function—bearing the names of God's people before Him—look like for us?",
            "The bells on the robe made the high priest's presence audible. What might this suggest about the visibility and accountability of ministry?"
        ],
        "tags": ["priestly garments", "ephod", "breastplate", "high priest", "intercession", "obedience", "Tabernacle", "Exodus", "worship", "consecration"],
        "sources": ["Exodus 39", "Hebrews 4:14-16", "Hebrews 7:25", "1 Peter 2:9", "Revelation 22:4", "Zechariah 14:20-21"]
    },

    # ── Exodus 40 ─────────────────────────────────────────────────────────────
    {
        "book_id": 2,
        "book": "Exodus",
        "chapter": 40,
        "title": "The Glory Fills the Tabernacle: God Dwells Among His People",
        "summary": (
            "God commands Moses to erect the Tabernacle on the first day of the first month. "
            "Moses obediently assembles every component, anoints and consecrates each piece, "
            "and ordains Aaron and his sons as priests. When Moses finishes all the work, the "
            "cloud of the LORD covers the tent and God's glory fills the Tabernacle so "
            "completely that even Moses cannot enter. The cloud then guides Israel through "
            "every subsequent journey."
        ),
        "content": (
            "Exodus 40 is the climax and culmination of everything from Exodus 19 onward. "
            "The Sinai covenant, the Tabernacle instructions, the golden calf crisis, the "
            "covenant renewal, and months of meticulous construction—all converge in this "
            "final chapter when God Himself moves in.\n\n"
            "**The Command to Erect (vv. 1-15)**\n\n"
            "God gives Moses precise instructions for erecting and consecrating the Tabernacle "
            "on the first day of the first month (v. 2)—one year after the Exodus from Egypt "
            "(cf. 12:2; 19:1; Num. 1:1). The entire year in the wilderness has been leading "
            "to this moment: God taking up residence among His delivered people. The "
            "instructions include anointing every component with the holy anointing oil, "
            "consecrating them as 'most holy' (v. 10), and ordaining Aaron and his sons "
            "for priestly service (vv. 12-15).\n\n"
            "**Moses Obeys (vv. 16-33)**\n\n"
            "Verses 16-33 carefully narrate Moses's obedience, with the phrase 'as the LORD "
            "commanded Moses' appearing seven more times (vv. 19, 21, 23, 25, 27, 29, 32). "
            "Fourteen total occurrences across chapters 39-40 form a literary bookend: the "
            "craftsmen obeyed completely (chapter 39) and now Moses obeys completely (chapter 40). "
            "Complete obedience produces complete readiness for God's presence.\n\n"
            "Moses erects the structure, sets up the Ark, places the furnishings, hangs the "
            "curtains and veil, washes Aaron and his sons, and clothes them in their sacred "
            "garments. Every action is deliberate, reverent, and ordered. When Moses finishes "
            "(v. 33), he has done something unprecedented in human history: he has built a "
            "dwelling for the living God.\n\n"
            "**The Glory of the LORD (vv. 34-38)**\n\n"
            "The Shekinah arrives without announcement or fanfare: 'the cloud covered the "
            "tent of meeting, and the glory of the LORD filled the Tabernacle' (v. 34). "
            "The word glory (כָּבוֹד, *kavod*) means weightiness, heaviness, substance—what "
            "is real and substantial. God's presence has weight. And it is overwhelming: "
            "Moses was *not able* to enter the tent (v. 35). The God who was intimate enough "
            "to speak with Moses face-to-face (33:11) is also transcendent enough to fill a "
            "space with presence too heavy for any human to bear.\n\n"
            "This tension—God's intimacy and transcendence—runs throughout Scripture. "
            "Solomon's temple is later filled in the same way (1 Kings 8:10-11). And the "
            "New Testament promises an even greater fulfillment: the Word became flesh and "
            "'tabernacled among us, and we beheld his glory' (John 1:14)—the Greek verb "
            "*eskénosen* literally means 'pitched His tent' among us. The Tabernacle's "
            "glory prefigures the incarnation.\n\n"
            "**The Guiding Cloud (vv. 36-38)**\n\n"
            "The cloud of the LORD covered the Tabernacle by day; the fire was in the cloud "
            "by night—visible to all Israel throughout their journeys. When the cloud lifted, "
            "Israel traveled; when it settled, they camped. God's presence was the schedule, "
            "the compass, and the comfort. The cloud connects backward to the pillar that "
            "led Israel out of Egypt (13:21-22) and forward to every subsequent wilderness "
            "stage—God is the constant through every change.\n\n"
            "**The Book of Exodus Ends**\n\n"
            "Exodus opened with 'Now these are the names' of seventy people who descended "
            "into slavery. It ends with God's glory filling the Tabernacle He shares with "
            "those liberated people. The arc of redemption is complete: from bondage to "
            "worship, from Egypt to encounter, from Pharaoh's house to God's house. "
            "The Exodus narrative is not primarily about escaping Egypt—it is about "
            "arriving at the presence of God."
        ),
        "chapter_overview": (
            "God commands Moses to erect the Tabernacle on the first day of the first month; "
            "Moses obediently assembles, anoints, and consecrates every component; Aaron and "
            "sons are ordained; the cloud covers the tent and God's glory fills the Tabernacle—"
            "overwhelming even Moses; the cloud guides Israel in every journey."
        ),
        "original_language_notes": [
            {
                "term": "כָּבוֹד (kavod)",
                "language": "Hebrew",
                "verse": "40:34",
                "words_used": ["glory", "honor", "weight"],
                "meaning": (
                    "Glory, weight, substance, honor. From the root כבד (kaved)—to be heavy. "
                    "The kavod of God is His substantive, overwhelming, reality-defining presence. "
                    "The same glory filled Solomon's Temple (1 Kings 8:11), is seen by Isaiah "
                    "(Isa. 6:3), and the NT says 'became flesh and dwelt among us' (John 1:14). "
                    "The kavod is not a feeling but a Presence."
                )
            },
            {
                "term": "עָנָן (anan)",
                "language": "Hebrew",
                "verse": "40:34",
                "words_used": ["cloud"],
                "meaning": (
                    "Cloud. In Exodus, the anan is the visible presence-marker of God—a theophanic "
                    "cloud. It led Israel out of Egypt (13:21), descended on Sinai (19:16), and now "
                    "settles on the Tabernacle. The cloud is both concealment (God is hidden) and "
                    "revelation (God is present). It reappears at the Transfiguration (Matt. 17:5) "
                    "and the Ascension (Acts 1:9)."
                )
            },
            {
                "term": "מִשְׁכָּן (mishkan)",
                "language": "Hebrew",
                "verse": "40:34",
                "words_used": ["tabernacle", "dwelling", "tent"],
                "meaning": (
                    "Dwelling, tabernacle. From שכן (shakan)—to dwell, settle, abide. God's "
                    "'shekinah' (dwelling presence) takes its name from this root. The LXX "
                    "translates mishkan with *skéné* (tent/tabernacle), the same root used in "
                    "John 1:14 where the Word 'tabernacled' (eskénosen) among us—the incarnation "
                    "as the ultimate mishkan."
                )
            },
            {
                "term": "יָכֹל (yakhol)",
                "language": "Hebrew",
                "verse": "40:35",
                "words_used": ["was able", "could"],
                "meaning": (
                    "To be able, to prevail, to have capacity for. Moses 'was not able' (lo yakhol) "
                    "to enter the tent. This is not physical barrier but glory-saturation. The "
                    "same inability overcomes the priests in Solomon's temple (1 Kings 8:11). "
                    "God's fullness exceeds human capacity to enter or contain."
                )
            },
            {
                "term": "מָשַׁח (mashah)",
                "language": "Hebrew",
                "verse": "40:9",
                "words_used": ["anoint"],
                "meaning": (
                    "To anoint, smear, rub with oil. The Tabernacle and all its components "
                    "were anointed—set apart from common use to holy purpose. The same root "
                    "gives us Messiah (מָשִׁיחַ, *mashiach*)—the Anointed One. In anointing "
                    "the Tabernacle, Moses performs a priestly act that ultimately points to "
                    "the Messiah who is the final Anointed."
                )
            }
        ],
        "moral_lessons": [
            "God's glory arriving is the goal of all worship construction—not the building itself, but whether God fills it.",
            "Complete obedience (as the LORD commanded—7 times) is the condition under which God's glory is welcomed in.",
            "God's transcendence and intimacy are not contradictions but two aspects of the same holy love—He speaks with us face to face and overwhelms us with glory.",
            "The cloud guiding every movement shows that God's presence is not for fixed religious moments but for every step of life's journey.",
            "The Exodus arc—from slavery to God's dwelling—is a pattern God repeats: He always moves us from bondage toward His presence.",
            "Even the most faithful servant (Moses) cannot enter God's fullness by his own ability—we all need the One who is the door."
        ],
        "application": (
            "Exodus ends not with Israel arriving in Canaan but with God arriving among Israel. The true destination was never a geographic land "
            "but a relational reality: God dwelling with His people. This is still the goal of redemption. Christ came to 'tabernacle' among us "
            "(John 1:14), and the Spirit now dwells in believers (1 Cor. 3:16). The cloud that guided every Israelite step models Spirit-led "
            "discipleship: we do not move until God moves; we follow His initiative. The challenge of Exodus 40 for the contemporary believer "
            "is: Is your life built in such a way that God's glory can fill it? Have you ordered your worship, obedience, and community by "
            "His specifications—so that there is space and structure ready for His presence?"
        ),
        "prayer": (
            "Lord God, fill our lives as You filled the Tabernacle—with the weight of Your glory, the clarity of Your guidance, and the warmth "
            "of Your presence. We are grateful that in Christ, You have tabernacled among us, that Your Spirit now dwells within us. Guide us "
            "as the cloud guided Israel—may we not move apart from You. May the goal of our lives, our churches, and our worship be not "
            "impressive structure but Your indwelling presence. To You be all glory, now and forever. Amen."
        ),
        "key_points": [
            "Moses's sevenfold obedience ('as the LORD commanded Moses') in chapter 40 completes the fourteen-fold refrain with chapter 39—total obedience.",
            "The cloud covering the tent and God's glory filling the Tabernacle is the culmination of the entire Exodus narrative.",
            "God's kavod (glory/weight) was so overwhelming that even Moses could not enter—a picture of divine transcendence meeting human limitation.",
            "The guiding cloud—covering by day, fire by night—shows God's active, continuous direction for every journey Israel would take.",
            "John 1:14 deliberately echoes Exodus 40: the Word 'tabernacled' among us and we beheld His glory—the incarnation as the ultimate Tabernacle.",
            "Exodus's arc from slavery to God's indwelling is the pattern of all salvation: delivered from bondage to become God's dwelling."
        ],
        "study_questions": [
            "Why does the text record 'as the LORD commanded Moses' seven times in chapter 40 (and fourteen times across chapters 39-40)? What is the theological message?",
            "Moses could not enter the tent because the glory was too overwhelming. What does this reveal about God's transcendence? How does it relate to the intimacy in Exodus 33:11?",
            "John 1:14 says the Word 'tabernacled' (eskénosen) among us. How does Exodus 40 enrich our understanding of the Incarnation?",
            "The cloud guided every journey and encampment. What does this moment-by-moment divine guidance suggest about the nature of faith and obedience?",
            "Exodus ends with God's presence, not with the Israelites reaching Canaan. What does this ending reveal about the true goal of redemption?",
            "Paul says believers are now God's temple and the Spirit dwells in them (1 Cor. 3:16). How does this relate to the Tabernacle's purpose?",
            "How does the pattern of Exodus—bondage → redemption → wilderness → God's dwelling—map onto your personal spiritual journey?"
        ],
        "tags": ["glory", "cloud", "Tabernacle", "dwelling", "completion", "obedience", "incarnation", "Spirit", "Exodus", "presence of God"],
        "sources": ["Exodus 40", "John 1:14", "1 Kings 8:10-11", "1 Corinthians 3:16", "Acts 1:9", "Matthew 17:5", "Revelation 21:3"]
    },

    # ── Leviticus 1 ───────────────────────────────────────────────────────────
    {
        "book_id": 3,
        "book": "Leviticus",
        "chapter": 1,
        "title": "Drawing Near to God: The Law of the Burnt Offering",
        "summary": (
            "God speaks to Moses from the newly-erected tent of meeting, giving the laws of "
            "the burnt offering (olah). The worshipper may bring a bull, a sheep or goat, or "
            "a bird—according to their means. In each case, the offering is slaughtered and "
            "entirely burned on the altar as 'a pleasing aroma to the LORD.' The chapter "
            "introduces the fundamental principle of Leviticus: sinful people approach the "
            "holy God through substitutionary sacrifice."
        ),
        "content": (
            "Leviticus opens exactly where Exodus 40 ended: God has taken up residence in "
            "the Tabernacle, and now He speaks from within it (v. 1). The book's very first "
            "word in Hebrew is וַיִּקְרָא (*vayiqra*)—'And He called'—giving the book its "
            "Hebrew name. God takes the initiative; the regulations that follow are not "
            "burdensome demands but divine invitations: *Come near. Here is how.*\n\n"
            "**The Fundamental Question of Leviticus**\n\n"
            "Leviticus asks and answers the most pressing question of Israel's new reality: "
            "*Now that the holy God dwells among a sinful people, how can they approach Him "
            "without dying?* The answer is the sacrificial system—elaborate, costly, and "
            "precise—because holiness and sin cannot simply coexist. Something must be "
            "done about the gap.\n\n"
            "**The Name: Olah—The Whole Burnt Offering (vv. 3-9)**\n\n"
            "The burnt offering (עֹלָה, *olah*) is so named because it 'goes up' (*alah*)—"
            "the entire animal, except the skin, is consumed by fire and ascends as smoke "
            "to God. Nothing is retained by the worshipper; nothing is eaten by the priests. "
            "It is total, complete offering—the fullest expression of dedication and "
            "consecration available in Israel's worship.\n\n"
            "The worshipper brings a male animal without blemish, presents it at the entrance "
            "of the tent of meeting, lays his hand on its head (v. 4), and then slaughters "
            "it. The hand-laying (סְמִיכָה, *semikha*) is the gesture of identification and "
            "transfer: *I am in this animal; let its death stand for my sin.* This is the "
            "theology of substitution—the animal bears what the worshipper deserves.\n\n"
            "The blood is then dashed against the sides of the altar by the priests (v. 5). "
            "Blood represents life (Lev. 17:11); its application to the altar makes atonement. "
            "The animal is then cut up, washed, and burned—every piece ascending to God. "
            "The result is 'a pleasing aroma to the LORD' (נִיחֹחַ, *nikoach*)—a relational "
            "term suggesting God's delightful reception of what is genuinely offered.\n\n"
            "**The Sheep or Goat (vv. 10-13)**\n\n"
            "Those who cannot afford a bull may bring a male sheep or goat. Same procedure: "
            "laying of hands, slaughter, blood on the altar, fire, ascending aroma. The "
            "God of Leviticus does not demand only what the wealthy can give.\n\n"
            "**The Bird Offering (vv. 14-17)**\n\n"
            "For those who cannot even afford livestock, God provides: a turtledove or "
            "young pigeon. The priest wrings its neck, drains its blood, removes the crop, "
            "tears it without dividing completely, and burns it. Even the poorest Israelite "
            "has access to atonement. This is significant: God provides a way for everyone.\n\n"
            "Luke 2:24 records that Mary and Joseph offered 'a pair of turtledoves, or two "
            "young pigeons'—the offering of the poor. Jesus entered the world as the son of "
            "people who could only afford the minimal offering; He who is the Lamb of God "
            "(John 1:29) grew up in the household of those who brought birds.\n\n"
            "**The Fulfillment: Christ the Perfect Burnt Offering**\n\n"
            "Every olah points forward to Christ. He was without blemish (1 Pet. 1:19). "
            "He was completely given—nothing held back, no part of His life withheld from "
            "the Father's will. He is the 'fragrant offering' (Eph. 5:2). He is our "
            "atonement (Rom. 3:25). The burnt offerings of Leviticus were genuine—they "
            "accomplished real forgiveness in their time—but they were also shadows (Heb. "
            "10:1-4) that required constant repetition because no animal could finally remove "
            "sin. Christ's 'one sacrifice for sins for all time' (Heb. 10:12) is the "
            "substance the shadows announced."
        ),
        "chapter_overview": (
            "God speaks from the tent of meeting; laws of the burnt offering (olah): a bull "
            "from the herd (with hand-laying, slaughter, blood on altar, fully burned); "
            "alternatively a sheep/goat; or for the poor, a turtledove or pigeon. Each "
            "offering is 'a pleasing aroma to the LORD.'"
        ),
        "original_language_notes": [
            {
                "term": "עֹלָה (olah)",
                "language": "Hebrew",
                "verse": "1:3",
                "words_used": ["burnt offering", "whole burnt offering"],
                "meaning": (
                    "Burnt offering. From the root עלה (alah)—to go up, ascend. The olah is "
                    "the 'ascending offering' because the entire animal is burned and rises as "
                    "smoke to God. No portion is retained by the worshipper or eaten by priests—"
                    "total dedication. It is the most comprehensive of the offerings, pointing "
                    "toward Christ who gave Himself entirely (Eph. 5:2)."
                )
            },
            {
                "term": "קָרְבָּן (korban)",
                "language": "Hebrew",
                "verse": "1:2",
                "words_used": ["offering", "sacrifice", "gift"],
                "meaning": (
                    "Offering, gift brought near. From קרב (qarav)—to draw near, to approach. "
                    "A korban is literally 'that which is brought near'—approaching God. The "
                    "word frames the entire sacrificial system as relational rather than merely "
                    "transactional: offerings are the means of *drawing near* to the holy God."
                )
            },
            {
                "term": "סְמִיכָה (semikha)",
                "language": "Hebrew",
                "verse": "1:4",
                "words_used": ["lay hand", "lean hand", "press hand"],
                "meaning": (
                    "Laying of hands, pressing hands upon. From סמך (samach)—to lean upon, "
                    "support. The worshipper pressed both hands on the animal's head before "
                    "slaughter—a gesture of identification and transference. 'Let this animal "
                    "stand in my place; let its death count for my sin.' Semikha later became "
                    "the gesture for ordination (Num. 27:18-23), evoking the same transference "
                    "of calling and authority."
                )
            },
            {
                "term": "נִיחֹחַ (nikoach)",
                "language": "Hebrew",
                "verse": "1:9",
                "words_used": ["pleasing aroma", "soothing aroma", "sweet savor"],
                "meaning": (
                    "Pleasing aroma, soothing fragrance. From נוח (nuach)—to rest, settle, "
                    "be satisfied. The nikoach is the metaphor for God's relational acceptance "
                    "of a genuine offering—it 'settles' or 'satisfies' His sense of justice. "
                    "Paul applies this directly to Christ's offering (Eph. 5:2) and to the "
                    "Philippians' financial gift (Phil. 4:18), showing that any act of faithful "
                    "self-giving participates in this 'pleasing aroma.'"
                )
            },
            {
                "term": "תָּמִים (tamim)",
                "language": "Hebrew",
                "verse": "1:3",
                "words_used": ["without blemish", "perfect", "whole"],
                "meaning": (
                    "Without blemish, perfect, complete, whole. An animal offered to God had "
                    "to be tamim—free from defect. This requirement of perfection points "
                    "forward to the Lamb of God who was 'without blemish or spot' (1 Pet. 1:19). "
                    "The word is also used of Noah (Gen. 6:9) and Abraham (Gen. 17:1), showing "
                    "that tamim is not merely ritual purity but the character of whole-hearted "
                    "devotion to God."
                )
            }
        ],
        "moral_lessons": [
            "God takes the initiative in worship—'He called' first; our coming to God is always in response to His invitation.",
            "The burnt offering's totality—nothing held back—sets the standard: true worship is complete self-offering, not partial compliance.",
            "Hand-laying on the animal demonstrates that atonement is personal, not abstract—there must be an act of identification with the sacrifice.",
            "God's provision of bird offerings for the poor shows His concern for equal access to His presence regardless of economic standing.",
            "The 'pleasing aroma' language reveals that God is not a distant cosmic judge but a relational God who responds to genuine worship.",
            "The animal must be without blemish—our approach to God requires perfection we cannot supply, which is why we need the Perfect Substitute."
        ],
        "application": (
            "Leviticus 1 invites the contemporary reader not to distance but to worship. The book often seems remote and ritualistic, but its "
            "core question—*How does a sinful person approach a holy God?*—is permanently relevant. The answer Leviticus gives is: *through "
            "sacrifice*. The answer the New Testament gives is: *through Christ, who is the sacrifice.* Hebrews 10 makes explicit what "
            "Leviticus implies: the daily and annual sacrifices were 'a shadow of the good things to come' (Heb. 10:1). When we take "
            "communion, confess our sins, and give ourselves to God (Rom. 12:1-2—'a living sacrifice'), we are participating in the spiritual "
            "reality that the Levitical burnt offering foreshadowed. Approach God. Not presumptuously, but boldly—through the blood of "
            "Christ who is your perfect olah."
        ),
        "prayer": (
            "Holy Lord, You called us before we called on You. Thank You for making a way to draw near when our sin made nearness "
            "impossible. We worship Christ as our perfect burnt offering—without blemish, fully given, a pleasing aroma to You. "
            "May we, as living sacrifices, offer ourselves wholly to You—our bodies, minds, time, and resources held back from nothing. "
            "May our lives be the aroma of Christ in every place we go. Amen."
        ),
        "key_points": [
            "Leviticus opens with God calling from the tent He just filled with glory—the regulations are God's invitation, not human invention.",
            "The burnt offering (olah) is named 'the ascending one'—it goes up entirely to God, symbolizing total self-dedication.",
            "The worshipper's hand-laying (semikha) on the animal's head was a gesture of personal identification and substitutionary transfer.",
            "God provided bird offerings for the poor—equal access to atonement regardless of economic standing.",
            "The 'pleasing aroma' (nikoach) is relational language: God's acceptance of genuine, whole-hearted offering.",
            "Christ is the fulfillment of every olah—without blemish (1 Pet. 1:19), wholly given, a fragrant offering (Eph. 5:2)."
        ],
        "study_questions": [
            "Leviticus's Hebrew name is 'Vayiqra'—'And He called.' Why is it significant that God calls first? What does this reveal about the nature of worship?",
            "The word 'korban' (offering) comes from a root meaning 'to draw near.' How does understanding offerings as 'means of drawing near' change how you read Leviticus?",
            "What is the theological meaning of the worshipper laying his hand on the animal's head before slaughter? What was being communicated by this act?",
            "God provided bird offerings for those who could not afford larger animals. What does this provision reveal about God's character?",
            "Hebrews 10:1 calls the sacrificial system 'a shadow of the good things to come.' How does Leviticus 1 both reveal and point beyond itself to Christ?",
            "Paul says Christ gave Himself as 'a fragrant offering and sacrifice to God' (Eph. 5:2), using language from Leviticus. How does this shape your understanding of the cross?",
            "Romans 12:1-2 calls believers to offer themselves as 'living sacrifices.' In what practical ways does the burnt offering's demand for totality apply to this calling?"
        ],
        "tags": ["burnt offering", "olah", "sacrifice", "atonement", "Leviticus", "approach to God", "Christ", "worship", "substitution", "holiness"],
        "sources": ["Leviticus 1", "Hebrews 10:1-12", "Romans 3:25", "Ephesians 5:2", "1 Peter 1:19", "Romans 12:1-2", "John 1:29", "Philippians 4:18"]
    }
]


def get_or_create_collection(conn):
    cur = conn.cursor()
    cur.execute("SELECT id FROM commentary_collections WHERE slug='believers-sword-commentaries'")
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        "INSERT INTO commentary_collections (uuid, name, slug, description, language_code, collection_type, is_offline_available, sync_status, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (str(uuid.uuid4()), "Believers Sword Commentaries", "believers-sword-commentaries",
         "Comprehensive evangelical Bible commentaries for every chapter.", "en", "ai_generated", 1, "local", NOW, NOW)
    )
    conn.commit()
    return cur.lastrowid


def get_or_create_author(conn):
    cur = conn.cursor()
    cur.execute("SELECT id FROM commentary_authors WHERE display_name='Believers Sword AI Commentary Writer'")
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        "INSERT INTO commentary_authors (uuid, display_name, author_type, language_code, sync_status, created_at, updated_at) VALUES (?,?,?,?,?,?,?)",
        (str(uuid.uuid4()), "Believers Sword AI Commentary Writer", "ai", "en", "local", NOW, NOW)
    )
    conn.commit()
    return cur.lastrowid


def entry_exists(conn, collection_id, book_id, chapter):
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
    # Shallow check: content must be more than 200 chars
    return len(row[1] or "") > 200


def insert_entry(conn, collection_id, author_id, c):
    cur = conn.cursor()
    entry_uuid = str(uuid.uuid4())
    cur.execute(
        """INSERT INTO commentary_entries
           (uuid, collection_id, author_id, book_id, chapter, verse_start, verse_end,
            reference_scope, title, summary, content, application, prayer,
            key_points, study_questions, language_code, theological_perspective,
            status, is_ai_generated, word_count, created_at, updated_at)
           VALUES (?,?,?,?,?,NULL,NULL,?,?,?,?,?,?,?,?,?,?,?,1,?,?,?)""",
        (
            entry_uuid, collection_id, author_id,
            c["book_id"], c["chapter"],
            "chapter", c["title"], c["summary"], c["content"],
            c["application"], c["prayer"],
            json.dumps(c["key_points"]),
            json.dumps(c["study_questions"]),
            "en", "evangelical", "draft",
            len(c["content"].split()),
            NOW, NOW
        )
    )
    conn.commit()
    return entry_uuid, cur.lastrowid


def save_json(c, entry_uuid):
    book_slug = c["book"].lower().replace(" ", "-")
    book_dir = f"{GENERATED_DIR}/{c['book_id']:02d}-{book_slug}"
    os.makedirs(book_dir, exist_ok=True)
    filepath = f"{book_dir}/{c['chapter']:02d}.json"
    payload = {
        "uuid": entry_uuid,
        "collection_name": "Believers Sword Commentaries",
        "author_type": "ai",
        "language_code": "en",
        "theological_perspective": "evangelical",
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
    assert not (forbidden & set(payload.keys())), f"Forbidden key in JSON: {forbidden & set(payload.keys())}"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    # Verify it parses back
    with open(filepath, "r", encoding="utf-8") as f:
        parsed = json.load(f)
    assert not (forbidden & set(parsed.keys())), "Forbidden key found after parse"
    return filepath


def update_progress(conn, last_book_id, last_book, last_chapter, next_book_id, next_book, next_chapter, completed):
    cur = conn.cursor()
    status = "completed" if completed else "draft"
    cur.execute("SELECT COUNT(*) FROM commentary_generation_progress")
    if cur.fetchone()[0] == 0:
        cur.execute(
            """INSERT INTO commentary_generation_progress
               (uuid, collection_id, language_code, current_book_id, current_chapter,
                last_completed_book_id, last_completed_chapter, target_book_id, target_chapter,
                chapters_per_batch, status, sync_status, created_at, updated_at)
               VALUES (?,1,'en',?,?,?,?,66,22,5,?,'local',?,?)""",
            (str(uuid.uuid4()), next_book_id, next_chapter, last_book_id, last_chapter, status, NOW, NOW)
        )
    else:
        cur.execute(
            """UPDATE commentary_generation_progress
               SET current_book_id=?, current_chapter=?,
                   last_completed_book_id=?, last_completed_chapter=?,
                   status=?, updated_at=?""",
            (next_book_id, next_chapter, last_book_id, last_chapter, status, NOW)
        )
    conn.commit()
    prog = {
        "next_book_id": next_book_id,
        "next_book": next_book,
        "next_chapter": next_chapter,
        "last_completed_book_id": last_book_id,
        "last_completed_book": last_book,
        "last_completed_chapter": last_chapter,
        "completed": completed,
        "updated_at": NOW
    }
    with open(PROGRESS_JSON, "w") as f:
        json.dump(prog, f, indent=2)
    return prog


def append_log(start_ref, end_ref, generated, skipped, db_rows, files_written):
    entry = {
        "timestamp": NOW,
        "generation_batch_id": BATCH_UUID,
        "start_reference": start_ref,
        "end_reference": end_ref,
        "chapters_generated": generated,
        "chapters_skipped": skipped,
        "db_rows_inserted": db_rows,
        "files_written": files_written
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


def main():
    conn = sqlite3.connect(DB_PATH)
    collection_id = get_or_create_collection(conn)
    author_id = get_or_create_author(conn)

    generated = 0
    skipped = 0
    db_rows = 0
    written_files = []
    start_ref = None
    end_ref = None
    last_book_id = None
    last_book = None
    last_chapter = None

    for c in COMMENTARIES:
        ref = f"{c['book']} {c['chapter']}"
        if start_ref is None:
            start_ref = ref
        end_ref = ref

        if entry_exists(conn, collection_id, c["book_id"], c["chapter"]):
            print(f"SKIP {ref} (already exists)")
            skipped += 1
        else:
            entry_uuid, row_id = insert_entry(conn, collection_id, author_id, c)
            filepath = save_json(c, entry_uuid)
            written_files.append(filepath)
            db_rows += 1
            generated += 1
            print(f"GENERATED {ref} -> {filepath} (uuid={entry_uuid})")

        last_book_id = c["book_id"]
        last_book = c["book"]
        last_chapter = c["chapter"]

    # Determine next starting point
    BOOK_ORDER = [
        (1,"Genesis",50),(2,"Exodus",40),(3,"Leviticus",27),(4,"Numbers",36),
        (5,"Deuteronomy",34),(6,"Joshua",24),(7,"Judges",21),(8,"Ruth",4),
        (9,"1 Samuel",31),(10,"2 Samuel",24),(11,"1 Kings",22),(12,"2 Kings",25),
        (13,"1 Chronicles",29),(14,"2 Chronicles",36),(15,"Ezra",10),(16,"Nehemiah",13),
        (17,"Esther",10),(18,"Job",42),(19,"Psalms",150),(20,"Proverbs",31),
        (21,"Ecclesiastes",12),(22,"Song of Solomon",8),(23,"Isaiah",66),(24,"Jeremiah",52),
        (25,"Lamentations",5),(26,"Ezekiel",48),(27,"Daniel",12),(28,"Hosea",14),
        (29,"Joel",3),(30,"Amos",9),(31,"Obadiah",1),(32,"Jonah",4),(33,"Micah",7),
        (34,"Nahum",3),(35,"Habakkuk",3),(36,"Zephaniah",3),(37,"Haggai",2),
        (38,"Zechariah",14),(39,"Malachi",4),(40,"Matthew",28),(41,"Mark",16),
        (42,"Luke",24),(43,"John",21),(44,"Acts",28),(45,"Romans",16),
        (46,"1 Corinthians",16),(47,"2 Corinthians",13),(48,"Galatians",6),
        (49,"Ephesians",6),(50,"Philippians",4),(51,"Colossians",4),(52,"1 Thessalonians",5),
        (53,"2 Thessalonians",3),(54,"1 Timothy",6),(55,"2 Timothy",4),(56,"Titus",3),
        (57,"Philemon",1),(58,"Hebrews",13),(59,"James",5),(60,"1 Peter",5),
        (61,"2 Peter",3),(62,"1 John",5),(63,"2 John",1),(64,"3 John",1),
        (65,"Jude",1),(66,"Revelation",22)
    ]
    completed = False
    next_book_id, next_book, next_chapter = last_book_id, last_book, last_chapter + 1
    for bid, bname, bchaps in BOOK_ORDER:
        if bid == last_book_id:
            if last_chapter >= bchaps:
                # Move to next book
                idx = BOOK_ORDER.index((bid, bname, bchaps))
                if idx + 1 < len(BOOK_ORDER):
                    next_book_id, next_book, _ = BOOK_ORDER[idx + 1]
                    next_chapter = 1
                else:
                    completed = True
                    next_book_id, next_book, next_chapter = bid, bname, bchaps
            break

    prog = update_progress(conn, last_book_id, last_book, last_chapter, next_book_id, next_book, next_chapter, completed)
    append_log(start_ref, end_ref, generated, skipped, db_rows, len(written_files))
    conn.close()

    print("\n=== SUMMARY ===")
    print(f"Generated: {generated}, Skipped: {skipped}")
    print(f"DB rows inserted: {db_rows}")
    print(f"Files written: {written_files}")
    print(f"Next starting reference: {next_book} {next_chapter}")
    print(f"Progress: {prog}")


if __name__ == "__main__":
    main()
