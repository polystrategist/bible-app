#!/usr/bin/env python3
"""Generate Leviticus 7-11 commentaries."""

import sqlite3
import json
import uuid
import os
import re
from datetime import datetime, timezone

DB_PATH = "/mnt/d/Projects/Personal/Believers-Sword/Modules Turso/Commentaries/Believers Sword/believers_sword_commentaries.db"
GENERATED_DIR = "/mnt/d/Projects/Personal/Believers-Sword/Modules Turso/Commentaries/Believers Sword/generated"
PROGRESS_JSON = "/mnt/d/Projects/Personal/Believers-Sword/Modules Turso/Commentaries/Believers Sword/commentary_generation_progress.json"
LOG_FILE = "/mnt/d/Projects/Personal/Believers-Sword/Modules Turso/Commentaries/Believers Sword/commentary_generation_log.jsonl"

COLLECTION_ID = 1
COLLECTION_NAME = "Believers Sword Commentaries"
BOOK_ID = 3
BOOK_NAME = "Leviticus"
BOOK_SLUG = "leviticus"
BOOK_DIR = "03-leviticus"
LANGUAGE_CODE = "en"

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


COMMENTARIES = [
    {
        "chapter": 7,
        "title": "Completing the Offering Laws: Guilt, Peace, Fat, and Blood",
        "summary": "Leviticus 7 concludes the priestly manual on offerings with final guilt offering regulations, detailed instructions for the three forms of the peace offering (thanksgiving, vow, freewill), and the crucial prohibition of eating fat or blood. The chapter closes with a summarizing formula, declaring these laws given at Sinai as binding on all Israel.",
        "content": """Leviticus 7 closes the double section that began in 6:8—the priestly manual for handling what the people bring. Where chapters 1-5 addressed worshippers, chapters 6-7 address priests. Chapter 7 completes the guilt offering, expands the peace offering into its three forms, and then interrupts the legal flow with two absolute prohibitions that apply to all Israelites: no fat, no blood.

**The Guilt Offering: Most Holy (vv. 1-10)**

The guilt offering (אָשָׁם, *asham*) is declared 'most holy' (v. 1). It follows the same slaughter and blood-splash procedure as the burnt offering: the animal is killed at the north side of the altar, its blood thrown against the altar's sides. The fat portions—the fat cover over the entrails, both kidneys with their fat, and the lobe of the liver—are all burned on the altar. These are the same fat pieces offered in the peace offering and sin offering, establishing a consistent theology: the inner richness belongs to God.

The priests' portion rules (vv. 7-10) clarify distribution: the officiating priest gets the skin of the guilt offering's ram; grain offerings that are baked or pan-cooked belong to the officiating priest; dry grain offerings are shared among Aaron's sons. This careful distribution prevented conflict over sacred portions and sustained the priesthood, which had no tribal land inheritance.

**The Peace Offering in Its Three Forms (vv. 11-21)**

The peace offering (שְׁלָמִים, *shelamim*) is unique: it is the only offering where the worshipper eats a portion along with the priests. It is the sacrificial meal, the fellowship offering, the table shared between God, priest, and worshipper. Leviticus 7 reveals it has three distinct forms:

1. **Thanksgiving offering** (תּוֹדָה, *todah*, v. 12): offered in response to divine deliverance. It includes unleavened cakes mixed with oil, unleavened wafers spread with oil, and cakes of fine flour mixed with oil—plus leavened bread. The leavened bread is unique; it is the only place leavened food appears in the offerings. It must all be eaten the same day: the urgency of thanksgiving admits no delay.

2. **Vow offering** (נֶדֶר, *neder*, v. 16): offered in fulfillment of a vow. May be eaten on the day of offering and the day after.

3. **Freewill offering** (נְדָבָה, *nedavah*, v. 16): spontaneous, uncompelled worship. Also two days to eat; on the third day, any remainder must be burned. It is *piggul* (abhorrent, v. 18) if eaten on the third day—it will not be accepted.

The eating deadlines are theologically significant: thanksgiving, which responds to a specific deliverance, must be consumed in one day—its joy is immediate and urgent. Vow and freewill offerings allow more leisurely celebration, but still expire. Worship has a 'freshness date'; delayed rejoicing risks formalism.

The prohibitions of vv. 19-21 address contamination: flesh that touches anything unclean must be burned; anyone unclean who eats from the peace offering will be cut off. The table God shares with His people is a holy table.

**The Prohibition of Fat and Blood (vv. 22-27)**

Two absolute prohibitions interrupt the peace offering regulations and apply to all Israel, not just priests:

1. **No fat** (vv. 22-25): The fat of ox, sheep, or goat must not be eaten. Fat belongs to God on the altar. The fat of an animal that dies naturally or is torn by wild animals may be used for other purposes but not eaten. This is 'throughout your generations, wherever you dwell'—a permanent, universal rule.

2. **No blood** (vv. 26-27): No blood of any animal—bird or beast—may be consumed. The penalty for both violations: 'cut off from his people.' These are not merely dietary recommendations but covenant violations. Blood is life (Lev. 17:11); fat is the richest portion. Both are God's. To eat them is to take what is His.

The blood prohibition carries enormous New Testament weight. Jesus's words at the Last Supper—'Drink from it, all of you, for this is my blood of the covenant' (Matt. 26:27-28)—are scandalous precisely because Israel had been forbidden to drink blood for centuries. To drink His blood is to receive His life (John 6:53-57). The prohibition pointed forward to the One whose blood would be given for the life of the world.

**The Closing Summary (vv. 28-38)**

The chapter closes with the priests' share of the peace offerings: the breast (the 'wave offering') and the right thigh (the 'heave offering') belong to Aaron and his sons, as a perpetual due from the people. Moses then summarizes: these are the laws given at Sinai when God commanded Israel to bring offerings—a reminder that all of this elaborate system was not human invention but divine prescription, given in the wilderness, for a people en route to a holy land.""",
        "chapter_overview": "Guilt offering completion: procedures, fat portions burned, priests receive skins and grain portions (vv. 1-10). Peace offering in three forms: thanksgiving (eaten same day with leavened bread), vow and freewill (two-day window) (vv. 11-21). Absolute prohibitions for all Israel: no eating fat or blood, penalty of being cut off (vv. 22-27). Priests' portions: breast and right thigh as wave and heave offerings; closing summary attributing laws to Sinai (vv. 28-38).",
        "original_language_notes": [
            {
                "term": "אָשָׁם (asham)",
                "language": "Hebrew",
                "verse": "7:1",
                "words_used": ["guilt offering", "trespass offering", "reparation offering"],
                "meaning": "Guilt, guilt offering, reparation offering. Asham encompasses both the state of guilt and the sacrifice that resolves it. Unlike the sin offering (ḥattat) which deals with unintentional violations, the asham specifically addresses desecration of holy things and breach of trust requiring measurable restitution. The same root appears in Isaiah 53:10 where the Suffering Servant makes himself an 'asham'—a guilt offering—for sin. The NT reads this as Christ's death being the ultimate reparation for humanity's breach of covenant with God."
            },
            {
                "term": "תּוֹדָה (todah)",
                "language": "Hebrew",
                "verse": "7:12",
                "words_used": ["thanksgiving", "thanksgiving offering", "praise"],
                "meaning": "Thanksgiving, confession, praise. Todah is the sacrifice offered in response to divine deliverance or in fulfillment of a vow made in distress. The Psalms are filled with todah psalms (22, 116, 118) where the worshipper publicly declares God's rescue. Psalm 50:23 says, 'The one who offers todah glorifies me,' suggesting that genuine thanksgiving is a form of worship more acceptable than mere ritual sacrifice. This is the deepest form of the peace offering: God delivers; the grateful worshipper brings a meal and invites others to hear the story."
            },
            {
                "term": "פִּגּוּל (piggul)",
                "language": "Hebrew",
                "verse": "7:18",
                "words_used": ["abhorrent", "abomination", "impure", "rejected"],
                "meaning": "Abhorrent, detestable, tainted. Piggul describes sacrificial meat that has become ritually repugnant—not because it has physically spoiled but because the intention of the one offering it has corrupted it. Specifically, if the priest intends to eat the sacrifice outside its prescribed time or place, the offering is piggul from the moment of that thought. This is significant: intention contaminates the sacrifice retroactively. Isaiah 65:4 uses piggul for the 'broth of piggul' associated with unlawful sacrifices. The concept anticipates Jesus's teaching that defilement is a matter of inner disposition (Matt. 15:17-20)."
            },
            {
                "term": "שְׁלָמִים (shelamim)",
                "language": "Hebrew",
                "verse": "7:11",
                "words_used": ["peace offering", "fellowship offering", "well-being offering"],
                "meaning": "Peace offerings, from the root shalom (peace, wholeness, well-being). The shelamim was the fellowship meal shared between God, priests, and the worshipper—the only offering where the layperson ate a substantial portion. It embodied the relational dimension of worship: not merely propitiation or atonement, but communion at table with God. The three forms (todah, neder, nedavah) represent three occasions: responding to grace received, fulfilling a promise made in need, and spontaneous overflowing devotion. Together they map the full landscape of grateful human response to God."
            }
        ],
        "moral_lessons": [
            "The three forms of the peace offering teach that gratitude takes different shapes: immediate thanksgiving for specific deliverance (todah), fulfillment of promises made to God in need (vow), and spontaneous, unearned worship from a full heart (freewill).",
            "The 'freshness date' on the thanksgiving offering—eaten the same day—warns against delayed or formalized gratitude; the joy of rescue is meant to be expressed immediately and communally.",
            "The fat and blood prohibitions remind every generation that certain things belong to God alone: the richest portion (fat) and the seat of life (blood) cannot be taken by humans without transgressing the covenant.",
            "The 'piggul' concept—that a corrupted intention taints the whole sacrifice—warns that outward worship motivated by wrong purposes is not merely ineffective but abhorrent.",
            "The priests' careful distribution of portions (skins, thigh, breast) models that those who serve God's people are sustained by God's provision; ministry is not free but neither is it mercenary."
        ],
        "application": "Leviticus 7 invites us to examine the forms and freshness of our gratitude. The thanksgiving offering had to be eaten the same day because delayed gratitude cools into obligation. When God delivers—in health, in provision, in answered prayer—the instinct should be immediate, communal, overflowing acknowledgment. The fat and blood prohibitions are also a check on human appetite: we are not the apex consumers of creation; some things are God's and must be returned to Him untouched. This speaks to giving—of time, money, firstfruits—as an act of covenant faithfulness, not charity. And the piggul warning confronts every worshipper: the sacrifice becomes tainted when the heart intends something other than what the form requires. Come to worship with intention aligned to action.",
        "prayer": "Lord God, forgive us for the piggul of corrupted worship—the outward forms with inward wandering. Stir fresh gratitude in us today; remind us of deliverances we have already begun to forget. Teach us to bring the thanksgiving offering with all its accompaniments—the telling of what You have done, the meal shared with others, the leavened bread of ordinary life placed before You. Help us honor the fat and blood—holding back what is Yours, giving it fully rather than consuming everything for ourselves. Thank You for the One whose blood was not withheld but poured out freely, becoming the peace offering that finally satisfied every form of shelamim. Amen.",
        "key_points": [
            "The guilt offering (asham) is 'most holy'; it follows burnt offering procedures and the fat portions belong entirely to God.",
            "The peace offering appears in three forms—thanksgiving (eaten same day), vow, and freewill (two-day window)—mapping the full range of human gratitude toward God.",
            "Thanksgiving offerings must be eaten the same day, teaching that delayed gratitude becomes formalism; the urgency of acknowledgment is built into the law.",
            "All fat and all blood are absolutely prohibited from consumption by any Israelite—'throughout your generations'—because both belong to God: fat as richest portion, blood as the seat of life.",
            "The 'piggul' (abhorrent) designation warns that intention contaminates sacrifice retroactively; wrong motives in worship make the offering detestable regardless of outward form.",
            "Isaiah 53:10 describes the Suffering Servant making himself an asham (guilt offering), and Jesus's blood-cup at the Last Supper inverts the blood prohibition by offering life itself to be received."
        ],
        "study_questions": [
            "The thanksgiving offering (todah) had to be eaten the same day—no leftovers. What does this time pressure teach about the nature and urgency of gratitude?",
            "Fat and blood are God's—'throughout your generations, wherever you dwell.' What does this permanent prohibition teach about the relationship between appetite, ownership, and covenant faithfulness?",
            "The 'piggul' concept says that an intention to eat the sacrifice at the wrong time makes the whole offering abhorrent to God. How does this principle apply to our modern worship practices?",
            "The peace offering is the only sacrifice where the worshipper eats a significant portion alongside the priests. What does this fellowship meal reveal about God's desire for communion with His people?",
            "Isaiah 53:10 applies the asham (guilt offering) to the Suffering Servant. How does this prepare us to understand Christ's death as more than merely symbolic?",
            "The priests received specific portions (skins, breast, thigh) as their livelihood from the people's offerings. What principles about sustaining those in ministry can be drawn from this system?",
            "Jesus said at the Last Supper, 'Drink from it, all of you, for this is my blood of the covenant' (Matt. 26:27-28). Why is this command scandalous in light of Leviticus 7:26-27, and what does it mean theologically?"
        ],
        "tags": ["peace offering", "guilt offering", "thanksgiving", "fat", "blood", "shelamim", "todah", "Leviticus", "worship", "gratitude"],
        "sources": [
            "Leviticus 7",
            "Isaiah 53:10",
            "John 6:53-57",
            "Matthew 26:27-28",
            "Psalm 50:23",
            "Matthew 15:17-20",
            "Leviticus 17:11"
        ]
    },
    {
        "chapter": 8,
        "title": "The Ordination of Aaron and His Sons: Consecrated by Moses",
        "summary": "Leviticus 8 records the ordination of Aaron and his sons as priests, performed exactly as God commanded in Exodus 29. Moses officiates, washing, vesting, and anointing Aaron, then anointing the tabernacle, and offering the ordination sacrifices—sin offering, burnt offering, and the ram of ordination. The blood of the ordination ram is placed on the right ear, thumb, and big toe of Aaron and his sons, consecrating their hearing, action, and walk.",
        "content": """Leviticus 8 is the enactment of Exodus 29. God prescribed the ordination ceremony in detail before the tabernacle was built; now, with the tabernacle standing, Moses performs exactly what was commanded. The chapter is a model of obedience: ten times the text notes 'as the LORD commanded Moses' (vv. 4, 9, 13, 17, 21, 29, 36). Ordination is not Moses's innovation or human ceremony; it is divine appointment, human execution.

**The Assembly and the Elements (vv. 1-5)**

Moses gathers 'the whole congregation' at the entrance of the tent of meeting. Ordination is not a private ceremony; the entire community witnesses the legitimation of its priestly leadership. The elements Moses brings: Aaron and his sons, the vestments, the anointing oil, the sin offering bull, the two rams, and the basket of unleavened bread. Each has its role in the multi-day ceremony.

**Washing, Vesting, and Anointing Aaron (vv. 6-13)**

Moses washes Aaron and his sons with water—purification before consecration. Then he dresses Aaron in the priestly garments in precise order: tunic, sash, robe, ephod, waistband of the ephod, breastpiece with the Urim and Thummim, and the turban with the golden plate inscribed 'Holy to the LORD.' The order matters: the priest is dressed from the inside out, from basic covering to the sign of his office.

Moses then anoints the tabernacle, sprinkling oil on the altar seven times and anointing all its furniture and utensils, and finally anoints Aaron, pouring oil on his head. The anointing oil is poured out on Aaron, not merely applied; Psalm 133:2 pictures it running down Aaron's beard and onto his robe—an image of superabundant, overflowing consecration.

Then Aaron's sons are vested in their simpler tunics, sashes, and caps. The distinction between high priest and priests is maintained in dress: Aaron bears the Urim and Thummim, the breastpiece, and the golden plate; his sons serve, but he mediates.

**The Sin Offering: Consecrating the Altar (vv. 14-17)**

The first sacrifice is a bull for a sin offering. Aaron and his sons lay their hands on its head—identifying with the sacrifice, transferring their own status to it. Moses slaughters it, takes blood on his finger, and applies it to the four horns of the altar, purifying it. The rest of the blood is poured at the base. The fat, kidneys, and liver lobe are burned on the altar; the remainder of the bull—its hide, flesh, and dung—is burned outside the camp. No one eats from the ordination sin offering; it is entirely for purification.

**The Burnt Offering: Full Consecration (vv. 18-21)**

The ram of burnt offering is brought. Aaron and his sons lay hands on it, Moses slaughters it, throws the blood against the altar, and burns the entire animal. The burnt offering is total—nothing remains for human consumption. It pictures complete self-offering: the priests are not merely employed; they are given, wholly, to God's service. Moses notes: 'It was a burnt offering with a pleasing aroma, a food offering for the LORD, as the LORD commanded Moses' (v. 21).

**The Ordination Ram: Blood on the Ear, Thumb, and Toe (vv. 22-30)**

The second ram is the ram of ordination (מִלֻּאִים, *milu'im*—'filling,' 'installation'). This is the most distinctive part of the ceremony. Moses slaughters the ram, takes some of its blood, and puts it on the right ear lobe, the right thumb, and the right big toe of Aaron—and then of each of his sons. Then blood from the altar is mixed with the anointing oil and sprinkled on Aaron and his sons and their garments, consecrating them.

The blood on the ear, thumb, and toe is the most theologically rich gesture in the chapter. The ear: consecrated to hear the word of God rightly. The thumb: consecrated to do the work of God faithfully. The toe: consecrated to walk in the ways of God. The three together consecrate the whole person—what one hears, what one does, what one walks. This same gesture appears in the cleansing of the healed leper (Lev. 14:14, 25), linking ordination and restoration: both bring a person into full covenant participation through blood applied to the points of perception, action, and movement.

**The Wave Offering and the Seven Days (vv. 29-36)**

Moses takes his portion (the right thigh goes to the officiating priest) and waves the breast before the LORD as a wave offering. Then he instructs Aaron and his sons to boil the remaining meat, eat it with the bread at the tabernacle entrance, and burn any remainder. They must stay at the tabernacle entrance for seven days, not leaving on pain of death: 'the ordination offering for seven days.' The seven days of ordination mirror the seven days of creation: a complete work, from nothing to fully established. When the week ends, the new priests will be ready.

**Moses as Type of Christ**

Throughout this chapter, Moses functions as priest—he performs the ordination, slaughters the animals, applies the blood, and makes atonement. Only after the seven days will Aaron perform priestly functions independently (ch. 9). This places Moses in a transitional priestly role that the NT writers observe: Moses was 'faithful in all God's house as a servant' while Christ is faithful 'as a son over God's house' (Heb. 3:2-6). The ordination ceremony points beyond itself: every human priest requires another to consecrate him. Christ, as eternal Son and High Priest, was appointed by God without human ordination (Heb. 5:5-6, citing Ps. 2:7 and Ps. 110:4).""",
        "chapter_overview": "Assembly at the tabernacle entrance; Moses gathers Aaron, sons, vestments, oil, and sacrificial animals (vv. 1-5). Washing and vesting Aaron in full high priestly garments; anointing the tabernacle and Aaron (vv. 6-13). Sin offering bull: blood on altar horns; remainder burned outside camp (vv. 14-17). Burnt offering ram: whole animal consumed on altar (vv. 18-21). Ordination ram: blood on Aaron's right ear, thumb, and big toe—then his sons'—mixed with oil and sprinkled on garments (vv. 22-30). Seven-day confinement at tabernacle entrance (vv. 31-36).",
        "original_language_notes": [
            {
                "term": "מִלֻּאִים (milu'im)",
                "language": "Hebrew",
                "verse": "8:22",
                "words_used": ["ordination", "consecration", "filling", "installation"],
                "meaning": "Filling, installation, ordination. From the root מָלֵא (male', 'to fill'). The ordination ram is literally the 'ram of the filling'—the sacrifice that fills the hands of the priests with their office. The idiom 'fill the hand' (male' yad) is the Hebrew expression for investing someone with priestly authority. This 'filling of the hands' is the ancient equivalent of placing a scepter or tool of office into someone's hands, signifying transfer of authority and responsibility. The concept is carried into the NT in Christ's installation as High Priest 'by the oath of God' (Heb. 7:20-21)."
            },
            {
                "term": "מִשְׁחָה (mishchah)",
                "language": "Hebrew",
                "verse": "8:12",
                "words_used": ["anointing oil", "anointing"],
                "meaning": "Anointing, anointing oil. From the root מָשַׁח (mashach), which also produces מָשִׁיחַ (mashiach, 'Messiah') and the Greek χριστός (christos, 'Christ'). The anointing of Aaron is thus a messianic act—Aaron is a 'messiah,' an anointed one, a foreshadowing of the Anointed One to come. The oil was poured on Aaron's head in superabundance (Ps. 133:2). Jesus was anointed 'with the Holy Spirit and with power' (Acts 10:38) and is called 'the Christ'—the Anointed—because He is the fulfillment of every priestly and royal anointing in Israel's history."
            },
            {
                "term": "תְּנוּפָה (tenufah)",
                "language": "Hebrew",
                "verse": "8:29",
                "words_used": ["wave offering", "elevation offering", "presented before the LORD"],
                "meaning": "Wave offering, elevation offering. The tenufah was a ritual motion—elevating the offering toward God and bringing it back—symbolizing presentation to God and return to human use. Some scholars read this as a horizontal waving (toward the altar and back), others as a vertical elevation. Either way, the gesture enacts the theology: the offering is God's before it is the priest's. What the priest eats, he receives back as gift from God, not wages he has earned. This priestly relationship to provision—receiving as gift what one has offered to God—models the posture of all Christian ministry."
            },
            {
                "term": "אֹזֶן (ozen)",
                "language": "Hebrew",
                "verse": "8:23",
                "words_used": ["ear", "right ear lobe", "hearing"],
                "meaning": "Ear, ear lobe. The blood was placed on the תְּנוּךְ (tenuch, 'tip') of the right ear—the cartilage at the top of the ear lobe. This same placement appears in the leper's cleansing (Lev. 14:14, 25), linking priestly ordination and covenant restoration. The ear is the organ of hearing divine instruction; its anointing with blood consecrates the priest to hear only what God commands. Proverbs 20:12 says, 'The hearing ear and the seeing eye, the LORD has made them both'—and both may be consecrated. Jesus repeatedly ends his teachings, 'He who has ears to hear, let him hear' (Matt. 11:15)."
            }
        ],
        "moral_lessons": [
            "The ten-fold repetition of 'as the LORD commanded Moses' establishes obedience as the governing principle of ordination and all worship; the ceremony's validity comes entirely from divine prescription, not human creativity.",
            "The blood placed on the ear, thumb, and toe consecrates what one hears, what one does, and where one walks—teaching that priestly (and indeed Christian) service is a whole-person consecration, not a part-time role.",
            "The seven-day confinement at the tabernacle teaches that genuine consecration requires time and sustained separation; transformation cannot be rushed.",
            "Moses washing Aaron before vesting him models the principle that purification precedes empowerment; one cannot be clothed in holiness without first being cleansed.",
            "The anointing oil poured on Aaron's head—overflowing down his beard and onto his robes—pictures the superabundant grace of God that equips those He calls; consecration is never a bare minimum."
        ],
        "application": "Leviticus 8 is about the cost and totality of consecration. Every Christian is a 'royal priest' (1 Pet. 2:9), and the logic of this chapter applies: we are washed (baptism), clothed (Christ's righteousness), and anointed (the Spirit). But the ordination ram's blood on the ear, thumb, and toe calls for a total-life response—what we listen to, what we do with our hands, where we go. Leviticus 8 asks: have you presented your hearing, your labor, your daily walk as holy to the LORD? The seven-day retreat before ministry begins also challenges impatient ministry culture: those who would serve effectively must first be formed. Rushing from conversion to position, from baptism to platform, skips the formative confinement that makes the ministry sustainable.",
        "prayer": "Holy Lord, we thank You for the completeness of Your consecration—that You leave nothing out, no part of us unaddressed. Consecrate our ears to hear Your Word over every competing voice. Consecrate our hands to do Your work faithfully and not for show. Consecrate our feet to walk in Your ways and not drift toward convenience. We receive Your anointing oil poured out in the Spirit, and we confess that we need Your filling to do the ministry You have called us to. Like Aaron and his sons, we wait in the place of preparation, trusting that the seven days of formation are not wasted days. May our obedience be as complete as Moses's—as the LORD commanded, so may we do. Amen.",
        "key_points": [
            "The phrase 'as the LORD commanded Moses' appears ten times in this chapter, establishing that the validity of the ordination comes entirely from divine prescription, not human ceremony.",
            "The blood on the right ear, right thumb, and right big toe consecrates the whole person—hearing, action, and walk—for priestly service.",
            "The anointing oil poured on Aaron's head is the origin of the Hebrew 'mashiach' (Messiah/Anointed One) and Greek 'christos,' directly linking Aaron's anointing to the coming Christ.",
            "The word for ordination, milu'im ('filling'), reflects the idiom 'fill the hand'—investing someone with an office by placing its tools in their hands.",
            "The seven-day confinement at the tabernacle entrance models that genuine formation for ministry requires sustained time and separation before public exercise of the office.",
            "Moses functions as a transitional priest throughout this chapter, anticipating the NT contrast: Moses was faithful as a servant in God's house; Christ is faithful as Son over God's house (Heb. 3:2-6)."
        ],
        "study_questions": [
            "The phrase 'as the LORD commanded Moses' appears ten times in Leviticus 8. What does this repetition communicate about the basis for priestly authority and the validity of the ceremony?",
            "Blood is placed on the right ear, thumb, and big toe of Aaron and his sons. What does this placement communicate about what priestly consecration involves?",
            "The Hebrew word for anointing (mashach) gives us 'Messiah' and 'Christ.' How does Aaron's anointing in this chapter function as a type pointing forward to Christ?",
            "Moses washed Aaron before clothing him. How does this sequence (purification before vesting) reflect the logic of the gospel: justification before sanctification?",
            "The ordination ceremony took seven days of confinement before Aaron could serve independently. What does this teach about the relationship between preparation and public ministry?",
            "The ordination ram (ram of milu'im, 'filling') was unique to this ceremony. What does the imagery of 'filling the hand' communicate about how priestly authority was invested?",
            "1 Peter 2:9 calls all believers 'a royal priesthood.' In light of Leviticus 8, what does it mean for all Christians to be priests—what has been 'placed on our ear, thumb, and toe'?"
        ],
        "tags": ["ordination", "Aaron", "priesthood", "anointing", "consecration", "Leviticus", "vestments", "blood", "Messiah", "seven days"],
        "sources": [
            "Leviticus 8",
            "Exodus 29",
            "Hebrews 3:2-6",
            "Hebrews 5:5-6",
            "Psalm 133:2",
            "Acts 10:38",
            "1 Peter 2:9",
            "Leviticus 14:14",
            "Psalm 2:7",
            "Psalm 110:4"
        ]
    },
    {
        "chapter": 9,
        "title": "The Eighth Day: Aaron's First Sacrifice and the Fire from Heaven",
        "summary": "Leviticus 9 records the climactic eighth day after ordination, when Aaron offers sacrifices independently for the first time. After sin offerings and burnt offerings for himself and the people, Aaron and Moses enter the tent of meeting. When they emerge and bless the people, fire comes out from the LORD and consumes the burnt offering—a divine confirmation of the priesthood, the tabernacle, and the covenant relationship. The people shout and fall on their faces.",
        "content": """Leviticus 9 is the great culmination. The tabernacle has been constructed (Exod. 40), the offerings have been defined (Lev. 1-7), and Aaron has been consecrated through the seven-day ordination (Lev. 8). Now, on the eighth day, the new beginning begins. Eight in Hebrew symbolism is the number of new beginnings—circumcision on the eighth day, the new octave after seven, the resurrection on 'the first day of the week' which is also the eighth day of the cycle. Leviticus 9 is the dawn of the priestly age.

**The Summons (vv. 1-6)**

Moses calls Aaron and his sons along with the elders of Israel. He gives Aaron specific instructions: a calf for a sin offering and a ram for a burnt offering, both for himself; for the people, a male goat for a sin offering, a calf and a lamb for a burnt offering, an ox and a ram for peace offerings, and a grain offering mixed with oil. The reason: 'Today the LORD will appear to you' (v. 4). All of this elaborate system—the regulations, the vestments, the seven-day wait—has been building toward one moment: the appearance of the living God to His people.

**Aaron's Sacrifice for Himself (vv. 7-14)**

Moses commands Aaron: 'Draw near to the altar and offer your sin offering and your burnt offering and make atonement for yourself and for the people' (v. 7). The sequence matters—Aaron must first atone for himself before he can atone for the people. Aaron is not spiritually self-sufficient; he approaches God as a sinner who needs the same grace he mediates.

The sin offering calf is slaughtered; Aaron's sons bring the blood to him; he dips his finger and puts it on the horns of the altar, pours out the blood at the base, and burns the prescribed fat pieces. The burn offerings follow the same pattern. Aaron is priest, but only at cost; he cannot approach God without sacrifice even on this inaugural day.

**Aaron's Sacrifice for the People (vv. 15-21)**

Having atoned for himself, Aaron turns to the people's offerings. The goat sin offering: slaughtered as the first. The burnt offering: calf and lamb, one by one, with precise procedures. The peace offerings: ox and ram for the people; Aaron waves the breast and right thigh—the portions that belong to the priest (established in ch. 7). The grain offering: a handful burned on the altar, the remainder for the priests. Everything proceeds 'in addition to the burnt offering of the morning'—the perpetual fire from ch. 6 is already burning; these offerings are layered on top of the daily sacrifice. The new priestly office does not replace the old rhythms; it fulfills them.

**Moses and Aaron Enter the Tent (v. 23a)**

Aaron and Moses then go into the tent of meeting. This is the only appearance of this gesture in the Pentateuch—the two leaders entering together. What happens inside is not described. But when they come out to bless the people, something extraordinary occurs.

**The Fire of the LORD (vv. 23-24)**

'And Moses and Aaron came out and blessed the people, and the glory of the LORD appeared to all the people. And fire came out from before the LORD and consumed the burnt offering and the fat pieces on the altar, and when all the people saw it, they shouted and fell on their faces.'

This is the seal of divine approval on everything that has been done. The fire did not come because Aaron performed the ritual—the ritual was performed in faith that the fire would come. God was not obligated; He chose to confirm. The same fire that would be lit by the people's careless hand on common coals (ch. 10) is here lit by God Himself on the altar. The contrast is immediate.

The people's response—shouting and falling on their faces—is the double movement of awe: the voice crying out in wonder, the body flattening in reverence. The encounter with the holy God is not emotionally neutral. It undoes human composure.

**The Eighth Day as New Creation**

The theological structure of this chapter mirrors Genesis 1-2. Seven days of preparation (ordination) and then the eighth day—the inauguration of a new order. Creation's seven days culminated in the Sabbath rest; ordination's seven days culminate in the fire of divine presence. When God completes creation, He rests in it; when God completes the priestly system, He inhabits it with fire.

The NT eighth day is the resurrection. Jesus rises on 'the first day of the week'—the eighth day of the creation week. The fire of Pentecost (Acts 2) is the NT equivalent of the fire in Leviticus 9: divine confirmation that the new covenant priesthood (all believers, 1 Pet. 2:9) is accepted. The shout of the congregation and the falling on faces anticipates the eschatological scene in Revelation 7:9-12 where a multitude falls before the throne.""",
        "chapter_overview": "Moses summons Aaron, sons, and elders; instructions for sin offering, burnt offering, and peace offerings for Aaron and the people; promise that the LORD will appear (vv. 1-6). Aaron's sin offering calf and burnt offering ram for himself: blood on altar horns and base, fat burned (vv. 7-14). People's sin offering (goat), burnt offerings (calf and lamb), peace offerings (ox and ram), grain offering (vv. 15-21). Moses and Aaron enter the tent together; emerge to bless the people; the glory of the LORD appears; fire comes from the LORD consuming the burnt offering; people shout and fall on their faces (vv. 22-24).",
        "original_language_notes": [
            {
                "term": "כְּבוֹד יְהוָה (kevod YHWH)",
                "language": "Hebrew",
                "verse": "9:23",
                "words_used": ["glory of the LORD", "the LORD appeared"],
                "meaning": "The glory of the LORD. Kavod (from kavad, 'heavy, weighty') is God's visible, weighty presence—the luminous manifestation of His being. In Exodus, the glory fills the tabernacle (Exod. 40:34-35) as a pillar of cloud and fire. Here in Leviticus 9 the glory appears to 'all the people'—not just Moses or the priests. The democratic appearance of the divine glory is programmatic: the whole congregation is addressed by God's presence. The NT glory is the incarnation (John 1:14: 'we have seen his glory') and the eschatological glory when 'every eye will see him' (Rev. 1:7)."
            },
            {
                "term": "אֵשׁ (esh)",
                "language": "Hebrew",
                "verse": "9:24",
                "words_used": ["fire", "fire came out from the LORD"],
                "meaning": "Fire. The divine fire that consumes the burnt offering in Leviticus 9:24 was not humanly kindled—it 'came out from before the LORD.' This same fire must be kept burning on the altar perpetually (Lev. 6:13). In the next chapter, Nadab and Abihu offer 'strange fire' (esh zarah) that was not commanded—the contrast with 9:24 is explicit: what God kindles, only God may authorize. Fire as divine presence appears throughout Scripture: the burning bush (Exod. 3), Elijah's altar (1 Kgs. 18:38), and Pentecost (Acts 2:3). God is a 'consuming fire' (Heb. 12:29)."
            },
            {
                "term": "וָיָּרֹנּוּ (va-yaronnu)",
                "language": "Hebrew",
                "verse": "9:24",
                "words_used": ["shouted", "cried aloud", "raised a shout"],
                "meaning": "They shouted, cried out for joy. From רוּעַ (rua'), to shout, give a battle cry, or shout for joy. The same root produces the 'shout' of the Psalms (e.g., Ps. 66:1, 'Make a joyful noise to God') and the rua' blown on trumpets at Sinai. The congregation's shout at Leviticus 9:24 is not rehearsed liturgy—it is spontaneous, involuntary response to the presence of God. It is the prototype of doxological shouts throughout biblical worship: Joshua 6 (Jericho), 1 Samuel 4 (ark shout), Ezra 3 (laying the temple foundation)."
            },
            {
                "term": "עֹלָה (olah)",
                "language": "Hebrew",
                "verse": "9:12",
                "words_used": ["burnt offering", "whole burnt offering", "ascent offering"],
                "meaning": "Burnt offering, ascending offering—from עָלָה (alah, 'to go up, ascend'). The olah was entirely consumed on the altar; nothing remained for the worshipper. The smoke—and the offering itself—ascended to God. The fire from heaven consuming the olah in Leviticus 9 completes the image: what was offered to ascend, God receives by descending to meet it with fire. The olah is the primary sacrifice of total consecration, and God's acceptance of it by fire signals the most complete possible confirmation of the worshipper's approach."
            }
        ],
        "moral_lessons": [
            "Aaron must sacrifice for himself before sacrificing for the people—the mediator is not above the need for grace but rather begins from the same place of need as those he serves.",
            "The divine fire that appears confirms that true worship is God's initiative responded to by human faithfulness, not human performance rewarded by divine compliance.",
            "The people's simultaneous shout and prostration is the biblical model of encountering God's holiness: joyful wonder and humble reverence are not opposites but the two halves of genuine awe.",
            "The eighth day as new beginning teaches that God's redemptive work moves in patterns of completion and renewal; after every seven-day formation, a new reality begins.",
            "Moses and Aaron entering the tent together before the great blessing models that those who minister publicly must spend time in the presence of God privately."
        ],
        "application": "Leviticus 9 challenges us to recover the expectation of God's appearance in worship. The people came to the tabernacle because Moses said, 'Today the LORD will appear to you.' They came with sacrifices, but they came expecting. Much modern worship has become a performance that humans put on for God (or for the congregation); Leviticus 9 inverts this: worship is the space where God appears to His people. The fire from heaven is His action, not theirs. Our role is to prepare faithfully—bring the right offerings, follow the right order, stand at the entrance—and then to receive what only God can give. The shouting and face-falling is the response; it is not the content. Let your worship be ordered enough that God's fire is not extinguished by chaos, and expectant enough that you are watching for the flame.",
        "prayer": "Living God, fire-giving God, appear to us today as You appeared to all the congregation of Israel. We confess that we often come to worship without expectation, performing ritual without watching for Your presence. Calibrate our hearts to expect You—not to demand, but to anticipate. Like Aaron, we approach first as sinners who need atonement before we can offer anything to You or for others. Thank You that our High Priest offered once for all what Aaron offered every year, and that the fire of the Spirit fell at Pentecost to confirm the new covenant priesthood. Make us a people who shout and fall on our faces—not because we have planned it, but because we have seen You. Amen.",
        "key_points": [
            "The eighth day represents new beginnings; after seven days of ordination formation, the priestly ministry officially begins—paralleling resurrection (the eighth day of the week) and Pentecost.",
            "Aaron must first offer for his own sin before offering for the people, establishing the principle that mediators are themselves recipients of the same grace they mediate.",
            "Fire comes from the LORD Himself to consume the burnt offering—divine confirmation that the sacrificial system, the priesthood, and the tabernacle are accepted by God.",
            "The people respond with simultaneous shouting and prostration—biblical awe combines expressive joy (rua') and reverent humility (falling on the face).",
            "Moses and Aaron enter the tent together before the blessing, modeling that effective public ministry flows from prior private encounter with God.",
            "The glory (kavod YHWH) appears to 'all the people'—not just the priests—demonstrating that the covenant encompasses the whole congregation, not merely its leaders."
        ],
        "study_questions": [
            "Why must Aaron sacrifice for himself before he can sacrifice for the people (v. 7)? What does this requirement reveal about human priesthood, and how does it contrast with Christ's priesthood in Hebrews 7:27?",
            "The LORD promises, 'Today the LORD will appear to you' (v. 4). What role does expectation play in worship, and how does this verse challenge our approach to gathered worship?",
            "The fire comes from the LORD Himself, not from human hands. What does this teach about the relationship between human faithfulness and divine initiative in worship?",
            "The people shouted (rua') and fell on their faces. How do these two responses complement each other? Is your own experience of God's presence more characterized by one than the other?",
            "Moses and Aaron enter the tent of meeting together before the blessing (v. 23). What might this private moment before public ministry suggest about the preparation required for leadership?",
            "The eighth day is structurally a new beginning. How does the eighth day of Leviticus 9 foreshadow the resurrection (first/eighth day) and Pentecost (Acts 2)?",
            "The glory of the LORD appeared 'to all the people' (v. 23). What does the communal visibility of God's glory suggest about the corporate nature of covenant faith?"
        ],
        "tags": ["eighth day", "Aaron", "priesthood", "fire from heaven", "glory of the LORD", "Leviticus", "sacrifice", "atonement", "worship", "new beginning"],
        "sources": [
            "Leviticus 9",
            "Leviticus 6:13",
            "Exodus 40:34-35",
            "Hebrews 7:27",
            "Acts 2:1-4",
            "1 Peter 2:9",
            "Revelation 7:9-12",
            "1 Kings 18:38",
            "Hebrews 12:29",
            "John 1:14"
        ]
    },
    {
        "chapter": 10,
        "title": "Nadab and Abihu: Unauthorized Fire and the Holiness of God",
        "summary": "Leviticus 10 records one of the most sobering events in the Pentateuch: Aaron's sons Nadab and Abihu offer 'unauthorized fire before the LORD, which he had not commanded,' and God's fire consumes them instantly. The chapter continues with Moses's directives for grief (only from a distance), the prohibition of wine before priestly service, the calling to teach Israel the distinction between holy and common, and an incident with the sin offering where Moses rebukes Eleazar and Ithamar—resolved when Aaron explains his sons' grief.",
        "content": """Leviticus 10 follows immediately and shockingly after chapter 9's glorious fire. In chapter 9, fire came from the LORD to consume the burnt offering and the people fell on their faces in wonder. In chapter 10, fire comes from the LORD to consume two priests, and their father stands stunned to silence. The same fire; the same holiness; an entirely different response from the worshippers—and an entirely different outcome.

**Nadab and Abihu (vv. 1-3)**

'Now Nadab and Abihu, the sons of Aaron, each took his censer and put fire in it and laid incense on it and offered unauthorized fire before the LORD, which he had not commanded them. And fire came out from before the LORD and consumed them, and they died before the LORD.'

The text is almost clinically brief. We are not told what the unauthorized fire was—some speculate it was the wrong fire (not from the altar), offered at the wrong time, possibly under the influence of wine (setting up v. 9's prohibition), or with presumptuous familiarity. What we are told is the verdict: it was 'not commanded' (אֲשֶׁר לֹא צִוָּה אֹתָם, *asher lo tzivvah otam*). The problem is not explicitly wickedness of heart; it is presumption in procedure. They offered what was not authorized.

This is where modern readers often struggle. The punishment seems disproportionate—death for a liturgical deviation? But the chapter must be read in its context. God has just descended in fire to confirm the entire sacrificial system. The covenant has just been inaugurated with awe and shouting. Within moments, two senior priests improvise at the altar of the living God. The message is not that God is petty about procedure; it is that the approach to God cannot be self-defined. 'I will be treated as holy by those who draw near me, and before all the people I will be glorified' (v. 3). The holiness of God is not a sentiment to be managed; it is a reality to be reckoned with.

**Moses's Response and Aaron's Silence (vv. 3-5)**

Moses quotes God's word to Aaron: 'This is what the LORD has spoken: "Among those who are near me I will be treated as holy, and before all the people I will be glorified."' And Aaron was silent (וַיִּדֹּם אַהֲרֹן, *va-yidom Aharon*). His silence is profound. He has no argument. He has no complaint. He does not accuse God. He falls silent before the holy. This is one of the most spiritually significant silences in Scripture—the silence of a man who has just lost two sons to divine judgment and who finds nothing to say except wordless submission.

Moses directs Aaron's cousins to carry the bodies out of the camp in their priestly tunics. The bodies must be removed but without the congregation becoming ceremonially unclean. Even in judgment, the liturgy continues.

**Prohibitions on Grief and Wine (vv. 6-9)**

Moses instructs Aaron and his remaining sons (Eleazar and Ithamar) not to mourn publicly—do not uncover your heads, do not tear your garments—because the anointing oil is on them. The whole congregation may weep for Nadab and Abihu, but the priests must not interrupt the service. They must not go outside the tabernacle entrance lest they die; the anointing oil of the LORD is upon them.

Immediately following: 'Drink no wine or strong drink, you or your sons with you, when you go into the tent of meeting, lest you die. It is a statute forever throughout your generations' (v. 9). The juxtaposition suggests that wine may have been involved in Nadab and Abihu's improvisational act. The prohibition is not merely ascetic; it is protective. The priest who enters God's presence clouded by alcohol cannot 'distinguish between the holy and the common, and between the unclean and the clean' (v. 10)—which is precisely the priestly calling. The priest is the keeper of categories; he cannot blur them.

**Teaching the Distinctions (vv. 10-11)**

The priests' task is twofold: to distinguish (לְהַבְדִּיל, *lehavdil*) between holy and common, between clean and unclean, and to teach Israel all the statutes the LORD has spoken through Moses. The priest is not merely a ritual officiant but a teacher; the maintenance of distinctions is a service to the community. When holy and common blur, moral and spiritual categories collapse.

**The Sin Offering Incident (vv. 12-20)**

Moses instructs Eleazar and Ithamar to eat their portion of the grain offering and the sin offering (the goat sin offering that was for the people). He discovers they have burned the sin offering completely rather than eating it. Moses is angry: the people's sin offering was supposed to be eaten by the priests in the holy place.

But Aaron speaks—his only speech in the chapter: 'Behold, today they have offered their sin offering and their burnt offering before the LORD, and yet such things as these have happened to me. If I had eaten the sin offering today, would the LORD have approved?' Moses heard this and approved. Aaron's argument: his sons have just died under God's judgment; in their grief, eating the sin offering of atonement would have been impossible—an act of hollow ritual with a shattered heart would not have pleased God. Moses accepts the reasoning.

This moment is quietly remarkable. After the rigidity of judgment, there is pastoral flexibility: grief and circumstance can affect the form of worship, and God does not require mechanical performance from a crushed heart. The rule stands; the exception is acknowledged; Moses and Aaron together discern the application.

**The Severity and Mercy of the Holy**

Leviticus 10 holds together two truths that modern readers find hard to hold simultaneously: God's holiness is utterly, immediately serious, and God's mercy is deep and pastoral. The same chapter that records instant judgment on Nadab and Abihu also records Moses's acceptance of Aaron's pastoral exception for grief. The chapter is not harsh; it is realistic about the nature of God: He is holy and He is with us, and both are completely true at the same time.""",
        "chapter_overview": "Nadab and Abihu offer unauthorized fire; divine fire consumes them (vv. 1-2). Moses quotes God: 'I will be treated as holy'; Aaron's profound silence (vv. 3-5). Bodies removed by cousins; Aaron and sons forbidden from mourning publicly (vv. 6-7). Prohibition of wine for priests before entering the tent, 'forever throughout your generations' (vv. 8-9). Priestly calling: distinguish holy from common, teach Israel the statutes (vv. 10-11). Moses instructs remaining sons about the grain and sin offerings (vv. 12-15). Moses discovers the sin offering was burned, rebukes Eleazar and Ithamar (vv. 16-18). Aaron explains their grief made eating the sin offering improper; Moses accepts the reasoning (vv. 19-20).",
        "original_language_notes": [
            {
                "term": "אֵשׁ זָרָה (esh zarah)",
                "language": "Hebrew",
                "verse": "10:1",
                "words_used": ["unauthorized fire", "strange fire", "foreign fire", "unholy fire"],
                "meaning": "Strange fire, foreign fire, unauthorized fire. Zarah means 'strange, foreign, unauthorized, alien'—something not belonging, not sanctioned. The exact nature of the unauthorized fire is debated: wrong source (not from the altar fire God lit in ch. 9), wrong time (outside prescribed hours), wrong place, or wrong attitude. The text emphasizes not the what but the why: 'which he had not commanded them.' The core offense is improvisation at the altar of the holy God—substituting human initiative for divine command. The same root zarah appears in Proverbs for the 'strange woman' (forbidden woman) and 'strange god' (idol), suggesting that zarah worship is a form of adultery against the covenant."
            },
            {
                "term": "וַיִּדֹּם (va-yidom)",
                "language": "Hebrew",
                "verse": "10:3",
                "words_used": ["was silent", "kept silent", "held his peace"],
                "meaning": "He was silent, he fell silent. From דָּמַם (damam), to be silent, still, cease. Aaron's silence is one of the most weighted silences in the Bible. Damam appears in Lamentations 2:10 (elders sit in silence during Jerusalem's destruction) and Psalm 4:4 ('be silent on your beds'—contemplation before God). Aaron does not argue with God; he does not accuse Moses; he does not mourn audibly. His silence is the silence of submission before the unfathomable holiness of God, a grief too deep for human words. Revelation 8:1 has a similar pregnant silence in heaven: 'there was silence in heaven for about half an hour.'"
            },
            {
                "term": "לְהַבְדִּיל (lehavdil)",
                "language": "Hebrew",
                "verse": "10:10",
                "words_used": ["distinguish", "differentiate", "separate", "make a distinction"],
                "meaning": "To distinguish, separate, make a division between. From בָּדַל (badal), the same root used in Genesis 1 for God 'separating' light from darkness, waters above from below, day from night. The priest's calling to distinguish holy from common and clean from unclean is a participation in the ongoing creative order—maintaining the distinctions God established at creation. When priests (or people) collapse these categories, they participate in a kind of de-creation. The NT equivalent is Paul's call to 'discern what is pleasing to the Lord' (Eph. 5:10) and to 'test everything; hold fast what is good' (1 Thess. 5:21)."
            },
            {
                "term": "קָדֹשׁ (kadosh)",
                "language": "Hebrew",
                "verse": "10:3",
                "words_used": ["holy", "treated as holy", "sanctified"],
                "meaning": "Holy, set apart, consecrated. The root קָדַשׁ (kadash) indicates separation, distinction, being set apart from the common. 'I will be treated as holy' (aqadesh, Niphal)—literally 'I will be sanctified, honored as holy'—means God's intrinsic holiness must be acknowledged and reflected in the way He is approached. Those who draw near but treat Him as common profane not only the ritual but God Himself. The entire Levitical system exists to maintain the reality that YHWH is not a manageable deity but the living, holy God of creation and covenant—and drawing near without recognizing this is not worship but presumption."
            }
        ],
        "moral_lessons": [
            "The story of Nadab and Abihu warns that familiarity with holy things can become presumption; proximity to God does not make one immune to His holiness—it intensifies the responsibility.",
            "Aaron's silence before God's judgment is a model of reverent submission in the face of incomprehensible suffering; there are times when the most faithful response is to cease arguing and be still.",
            "The prohibition of wine before priestly service teaches that ministry requires full mental clarity; those who blur the categories of holy and common through impaired judgment endanger themselves and those they serve.",
            "The calling to 'distinguish between the holy and the common' is the fundamental priestly task and extends to all who handle sacred things: teachers, leaders, parents—all must maintain clarity about what God has marked as His.",
            "Moses's acceptance of Aaron's pastoral exception for grief shows that God is not a mechanical rule enforcer; faithful leaders must discern when grief and circumstance affect the form—but not the substance—of worship."
        ],
        "application": "Leviticus 10 is the hardest chapter in the Levitical system. It confronts us with the danger of familiarity with holy things. In an age of casual spirituality, where the sacred is routinely managed and the transcendent is 'personalized,' the fire that consumed Nadab and Abihu is a warning: God does not adjust to our comfort; we are called to approach on His terms. The wine prohibition also speaks to leadership: ministry requires clarity of mind. Anything that clouds our ability to distinguish truth from error, holy from common—entertainment, distraction, numbing—is dangerous when we are handling sacred responsibility. And Aaron's silence is a gift: when God's actions confound us, and we have no argument that holds, the most faithful response is to fall silent and trust the God who is always righteous.",
        "prayer": "Holy God, You are fire. We approach You not with our own fire but through the fire You yourself have provided—the cross of Christ, the intercession of our great High Priest, the gift of the Spirit. Forgive us for the moments we have offered unauthorized fire: worship shaped by preference rather than Your command, service driven by ambition rather than calling, devotion clouded by substances or distractions that blur the holy from the common. Give us Aaron's silence when we cannot understand Your ways. Give us Eleazar and Ithamar's willingness to receive correction. Give us the wisdom to distinguish holy from common, clean from unclean, and the courage to maintain those distinctions in a world that wants everything blurred. Amen.",
        "key_points": [
            "Nadab and Abihu offer 'unauthorized fire'—fire not commanded by God—and are immediately consumed; the offense is not ignorance but presumption in improvising at God's altar.",
            "God's declaration: 'Among those who are near me I will be treated as holy'—proximity to holy things intensifies rather than reduces responsibility.",
            "Aaron's silence (va-yidom) after his sons' death is one of Scripture's most profound moments: reverent submission to God's judgment without argument or accusation.",
            "The prohibition of wine for priests before service protects their ability to distinguish holy from common—the core priestly calling that the chapter defines in verses 10-11.",
            "The priestly role is fundamentally categorial: to lehavdil (distinguish, separate) as God distinguished light from darkness at creation—maintaining the sacred order.",
            "Moses accepts Aaron's pastoral exception about the sin offering—grief and circumstance can affect worship's form without abandoning its substance; God is not a mechanical rule enforcer."
        ],
        "study_questions": [
            "The text says Nadab and Abihu offered fire 'which he had not commanded them.' Why is the absence of divine command—rather than the presence of evil intent—the core problem? What does this teach about the limits of religious creativity?",
            "God says, 'Among those who are near me I will be treated as holy.' How does spiritual proximity increase rather than decrease the seriousness of irreverence?",
            "Aaron's silence (va-yidom) is one of Scripture's most profound moments. What does this silence communicate about how we should respond when God's actions confound or grieve us?",
            "The wine prohibition is placed immediately after the deaths of Nadab and Abihu. What connection does the text suggest between impaired judgment and unauthorized worship?",
            "The priest is called to 'distinguish between the holy and the common, and between the unclean and the clean' (v. 10). What does this categorial function mean for teachers, pastors, and parents today?",
            "Moses initially rebukes Eleazar and Ithamar but then accepts Aaron's explanation about grief. What does this episode reveal about the difference between mechanical rule-following and pastoral discernment?",
            "Hebrews 12:29 says 'our God is a consuming fire.' How does Leviticus 10 help us understand what this means—and what response it calls for?"
        ],
        "tags": ["Nadab", "Abihu", "unauthorized fire", "holiness", "judgment", "Aaron", "Leviticus", "priesthood", "wine", "silence"],
        "sources": [
            "Leviticus 10",
            "Leviticus 9:24",
            "Hebrews 12:29",
            "Numbers 3:4",
            "Ezekiel 44:21",
            "Ephesians 5:10",
            "1 Thessalonians 5:21",
            "Revelation 8:1",
            "Psalm 46:10"
        ]
    },
    {
        "chapter": 11,
        "title": "Clean and Unclean: The Dietary Laws and the Holiness of Israel",
        "summary": "Leviticus 11 introduces Israel's dietary laws: the criteria for clean and unclean land animals (split hoof and cud-chewing), water creatures (fins and scales), birds (a specific prohibited list), and insects (only those with jointed legs for leaping). The chapter also covers uncleanness from touching dead animals. It closes with the foundational rationale: 'You shall be holy, for I am holy.'",
        "content": """Leviticus 11 marks a significant shift in the book. Chapters 1-7 dealt with offerings; chapters 8-10 dealt with priests. Now, with chapter 11, the holiness code begins to address the daily lives of all Israelites. The dietary laws are not merely hygienic regulations; they are a curriculum in holiness. Every meal becomes a moment of decision: am I eating what God has designated as food, or am I crossing the boundary He has drawn? The kitchen is a classroom in covenant faithfulness.

**Land Animals: Two Criteria (vv. 1-8)**

The laws are addressed to Moses and Aaron together—and then to the people. The rule for land animals is binary: to be clean, an animal must both (1) have completely split hooves and (2) chew the cud. Both criteria must be met. The camel, rock hyrax (hyrax/coney), and hare chew the cud but do not have completely split hooves—unclean. The pig has completely split hooves but does not chew the cud—unclean. Their carcasses must not be touched; to touch is to become unclean until evening.

The pig is named as the paradigmatic unclean animal. Its exclusion became the defining badge of Jewish distinctiveness in the Greco-Roman world, where pork was the most common sacrificial and dietary meat. Not eating pig was one of the most visible ways Israel maintained its distinct identity.

**Water Creatures: Fins and Scales (vv. 9-12)**

Fish must have both fins and scales to be clean. Creatures of the sea or streams without fins and scales—shellfish, eels, sharks—are 'detestable' (שֶׁקֶץ, *sheqets*). The fish with fins and scales live in their element cleanly; the creatures without them are bottom-dwellers, scavengers, or predators at the boundaries. The dietary line follows a principle of category-integrity: creatures suited to their element without ambiguity are clean.

**Birds: A List, Not a Criterion (vv. 13-19)**

For birds, no criterion is given; instead, a list of prohibited birds is provided. The list includes eagles, vultures, ravens, hawks, owls, and bats. Most of the prohibited birds are birds of prey or carrion-eaters—they eat blood, which is forbidden (Lev. 7:26-27). The bat is listed with birds; the dietary code follows observable categories, not modern taxonomy.

**Insects: Jointed Legs for Leaping (vv. 20-23)**

Flying insects that go on all fours (a way of saying winged insects that walk) are detestable—except those with 'jointed legs above their feet with which to hop on the ground' (v. 21). The four clean insects are the locust, bald locust (cricket?), cricket, and grasshopper. These are legitimate food; John the Baptist ate them (Matt. 3:4). Other winged crawling insects are detestable.

**Touching Carcasses (vv. 24-40)**

Much of the chapter's second half deals with contact uncleanness: touching or carrying a clean or unclean animal's carcass makes one unclean until evening. Vessels, clothing, ovens, and water containers that contact carcasses have specific purification protocols—some require washing, some must be broken. The principle extends even to clean animals: if a clean animal dies without being slaughtered (not through kosher slaughter), its carcass is unclean. Even the source of good food can become unclean through wrong death.

**The Theological Foundation (vv. 44-47)**

The chapter closes with one of the most important verses in Leviticus: 'For I am the LORD your God. Consecrate yourselves therefore, and be holy, for I am holy. You shall not defile yourselves with any swarming thing that crawls on the ground. For I am the LORD who brought you up out of the land of Egypt to be your God. You shall therefore be holy, for I am holy.'

This rationale is not hygiene, not health (though clean foods may also be healthier), not cultural distinctiveness alone—it is divine character imitating. Israel is to be holy because God is holy. Holiness means, at its root, being set apart, distinct, consecrated—and the dietary laws enact that distinctiveness in the most quotidian human action: eating. Every meal is a reminder: 'I am not Canaanite, not Egyptian, not defined by surrounding culture. I belong to a holy God, and my diet reflects that consecration.'

**The New Testament and Clean/Unclean**

The dietary laws were central to the Judaism of Jesus's day. Jesus's declaration that 'nothing that goes into a person from outside can defile him' (Mark 7:15) was revolutionary, and Mark adds the parenthetical: 'Thus he declared all foods clean' (Mark 7:19). Peter's vision at Joppa (Acts 10) explicitly uses the clean/unclean categories to announce the Gentile mission: 'What God has made clean, do not call common.' Paul addresses the debate in Romans 14-15 and 1 Corinthians 8-10: food offered to idols, clean and unclean, are now matters of conscience in Christ, not covenant obligation.

The abolition of the dietary laws is not a reversal of Leviticus 11 but its fulfillment. The purpose of the dietary laws was to maintain Israel's distinctiveness until the Messiah came, keeping a holy seed through which blessing would come to the nations. Once the Messiah has come, the boundary markers that separated Israel from the nations—dietary laws, circumcision, Sabbath—are fulfilled in Him. Gentiles enter the covenant not by adopting Israel's boundary markers but by faith in the One those markers pointed to. The law's purpose, achieved; the law's boundary, opened.""",
        "chapter_overview": "Land animals: must have completely split hooves AND chew the cud to be clean—camel, hyrax, hare, and pig given as counterexamples (vv. 1-8). Water creatures: must have fins and scales—shellfish and similar creatures are detestable (vv. 9-12). Birds: a list of prohibited species (mostly carrion-eaters and birds of prey) (vv. 13-19). Insects: detestable unless they have jointed legs for leaping (locust, cricket, grasshopper are clean) (vv. 20-23). Contact uncleanness from carcasses: purification protocols for persons and vessels (vv. 24-40). Closing rationale: 'Be holy, for I am holy'—Israel consecrated to YHWH who brought them from Egypt (vv. 41-47).",
        "original_language_notes": [
            {
                "term": "שֶׁקֶץ (sheqets)",
                "language": "Hebrew",
                "verse": "11:10",
                "words_used": ["detestable", "abomination", "abhorrence", "swarming things"],
                "meaning": "Detestable thing, abhorrence, abomination. Sheqets is stronger than 'unclean' (tame')—it describes not merely ritual impurity but something inherently repugnant, something that should evoke disgust. The word is used for unclean sea creatures (v. 10), insects (v. 23), and reptiles (v. 41). Interestingly, sheqets is also used by the prophets for idol worship (e.g., Isa. 66:17; Ezek. 8:10), suggesting that the dietary detestable is an analogue to the theological detestable. Worshipping idols and eating sheqets occupy the same semantic and spiritual register: both are violations of the covenant holiness that defines Israel's identity."
            },
            {
                "term": "גֵּרָה (gerah)",
                "language": "Hebrew",
                "verse": "11:3",
                "words_used": ["cud", "chews the cud", "ruminant"],
                "meaning": "Cud, the ruminated matter. From a root meaning to drag or draw back. The gerah is the food that has been swallowed and then drawn back up from the first stomach to be chewed again—the ruminant's second processing. The cud-chewing criterion (alongside split hooves) defines clean land animals. Interestingly, several ancient and medieval Jewish interpreters saw the two criteria allegorically: chewing the cud represents meditating on God's word (drawing it back up for re-examination—Ps. 1:2, 'meditate day and night'); split hooves represent the ability to distinguish and separate (lehavdil) between true and false. Whether or not this allegory is intended, it captures the spirit of Leviticus 11: the clean animal embodies what Israel is called to be."
            },
            {
                "term": "קָדוֹשׁ (kadosh)",
                "language": "Hebrew",
                "verse": "11:44",
                "words_used": ["holy", "be holy", "consecrate yourselves"],
                "meaning": "Holy, set apart. The closing rationale of Leviticus 11 grounds the dietary laws in divine character: 'I am holy' (kadosh). Kadosh means set apart, distinct, consecrated—the opposite of common (ḥol). God's holiness is His essential distinction from everything created, His complete otherness. Israel is called to reflect this otherness in its daily life—beginning with eating. The phrase 'be holy, for I am holy' (quoting here and repeated in 19:2, 20:7, 26) is the heartbeat of Leviticus and is picked up in 1 Peter 1:16, applying the call directly to Christians: 'As he who called you is holy, be holy in all your conduct.'"
            },
            {
                "term": "טְמֵא (tame')",
                "language": "Hebrew",
                "verse": "11:4",
                "words_used": ["unclean", "impure", "defiled"],
                "meaning": "Unclean, impure, ritually defiled. Tame' is the standard word for ritual impurity in Leviticus. Unlike sheqets (inherent repugnance), tame' can be temporary and cleansable—one becomes tame' by touching a carcass and returns to cleanness after washing and waiting until evening. The clean/unclean (tahor/tame') distinction runs through all of Leviticus 11-15 and represents a binary ordering of creation: God has designated some things as belonging to the holy order and some as outside it. What makes this powerful is that tame' is not primarily moral—one can become unclean through ordinary biological functions. The system teaches that the entire physical world, including normal human life, stands in need of constant consecration."
            }
        ],
        "moral_lessons": [
            "The dietary laws enact the principle that holiness is not limited to 'religious' moments—eating, the most daily of acts, becomes a practice of covenant identity and consecration.",
            "The call to 'be holy as I am holy' grounds all ethical and ritual behavior in divine character rather than in cultural convention or pragmatic benefit: we are holy because God is holy, not because holiness is useful.",
            "The two-criteria rule for land animals models the kind of discernment the dietary laws train: not one indicator but two; genuine cleanness requires meeting the full standard, not just appearing to.",
            "The distinction between sheqets (inherently detestable) and tame' (temporarily unclean but purifiable) teaches that not all impurity is equal—some things are incompatible with holiness by nature; others require only cleansing.",
            "The New Testament fulfillment (Mark 7:19; Acts 10) teaches that the dietary laws' purpose was to maintain Israel's distinctiveness until the Messiah came; their abolition is not cancellation but completion."
        ],
        "application": "Leviticus 11 calls us to holiness in daily life, not just in liturgical moments. While Christians are no longer bound by the Levitical dietary code (Mark 7:19; Acts 10:15), the principle behind it remains: every ordinary act of life can be a practice of consecration. What we consume—food, media, entertainment, information—shapes who we are. The chapter's two-criteria rule also models wisdom: rather than single-factor decisions, genuine discernment requires examining multiple indicators. The closing call, 'be holy, for I am holy,' picked up in 1 Peter 1:16, remains the Christian's charter: not separation from the world for its own sake, but a life so aligned with God's character that it stands visibly distinct. The dietary laws trained Israel to ask 'is this God's?' before eating; the Spirit trains us to ask the same question before every choice.",
        "prayer": "Holy God, You call us to be what You are—not because we can manufacture holiness but because You give it freely and then ask us to live in it. Forgive us for treating holiness as a Sunday category while our daily choices—what we eat, watch, consume, tolerate—are left unconsecrated. Train us, by Your Spirit, to bring the same discernment to our daily decisions that Leviticus 11 brought to the Israelite kitchen. Help us distinguish between the truly detestable (sheqets—inherently incompatible with holiness) and the temporarily unclean (tame'—requiring purification and restoration). Thank You that in Christ, You have declared us clean—not because we have met every criterion, but because He has. May that cleanness be visible in how we live every day. Amen.",
        "key_points": [
            "Dietary laws cover four categories: land animals (two criteria: split hoof AND cud-chewing), water creatures (fins and scales), birds (a prohibited list of mostly carrion-eaters), and insects (jointed legs for leaping are clean).",
            "The two-criteria rule for land animals models discernment: genuine cleanness requires meeting the full standard; an animal that meets only one criterion (pig: split hooves but no cud) is unclean.",
            "Sheqets (detestable) and tame' (unclean) are distinct: some things are inherently repugnant; others are temporarily unclean and can be purified by washing and waiting.",
            "The closing rationale—'Be holy, for I am holy' (v. 44-45)—grounds the dietary laws not in hygiene or cultural strategy but in divine character imitation; Israel's diet reflects God's holiness.",
            "Peter's vision (Acts 10) uses the clean/unclean vocabulary to announce the Gentile mission; Jesus's declaration (Mark 7:19) fulfills rather than cancels the dietary laws by opening the covenant to all nations.",
            "Every meal in ancient Israel was a practice of covenant identity: the kitchen as classroom, the table as a daily reminder of belonging to a holy God who brought them out of Egypt."
        ],
        "study_questions": [
            "The dietary laws require two criteria for land animals (split hoof AND cud-chewing). What does this two-part test model about the nature of genuine discernment—in worship, in ethics, in daily choices?",
            "The pig meets one criterion (split hooves) but not the other (cud-chewing) and is therefore unclean. Can you think of things in modern life that appear 'clean' by one standard but fail another important test?",
            "The closing rationale is: 'Be holy, for I am holy.' What does it mean that the basis for the dietary laws is God's own character rather than health, culture, or social identity?",
            "Peter's vision in Acts 10 uses the language of Leviticus 11 ('what God has made clean, do not call common') to announce the Gentile mission. What does this suggest about the purpose the dietary laws served in Israel's history?",
            "Ancient Jewish interpreters allegorized the dietary criteria: cud-chewing = meditating on God's word; split hooves = ability to distinguish. Even if not the original intent, what does this allegorical reading reveal about the kind of person the laws were meant to form?",
            "Leviticus 11 makes eating a daily spiritual practice. What ordinary, daily act in your life might you 'consecrate'—bring into the framework of holiness—that you have not considered before?",
            "How does 1 Peter 1:14-16 apply the 'be holy, for I am holy' principle to Christian life? What does Christian holiness look like if it is no longer expressed through dietary laws?"
        ],
        "tags": ["dietary laws", "clean", "unclean", "holiness", "sheqets", "pig", "Leviticus", "be holy", "Acts 10", "food"],
        "sources": [
            "Leviticus 11",
            "Mark 7:14-19",
            "Acts 10:9-16",
            "Romans 14:14-20",
            "1 Peter 1:14-16",
            "Matthew 3:4",
            "Deuteronomy 14:3-21",
            "Isaiah 66:17",
            "1 Corinthians 8:8"
        ]
    }
]


def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def ensure_dirs():
    book_dir = os.path.join(GENERATED_DIR, BOOK_DIR)
    os.makedirs(book_dir, exist_ok=True)
    return book_dir


def get_collection_id(conn):
    row = conn.execute(
        "SELECT id FROM commentary_collections WHERE slug='believers-sword-commentaries'"
    ).fetchone()
    if row:
        return row[0]
    # Create it
    conn.execute(
        "INSERT INTO commentary_collections (name, slug, language_code, status) VALUES (?,?,?,?)",
        (COLLECTION_NAME, 'believers-sword-commentaries', LANGUAGE_CODE, 'active')
    )
    conn.commit()
    return conn.execute("SELECT last_insert_rowid()").fetchone()[0]


def entry_exists(conn, collection_id, book_id, chapter):
    row = conn.execute(
        """SELECT id, content FROM commentary_entries
           WHERE collection_id=? AND book_id=? AND chapter=?
             AND language_code=? AND reference_scope='chapter' AND deleted_at IS NULL""",
        (collection_id, book_id, chapter, LANGUAGE_CODE)
    ).fetchone()
    if row:
        content = row[1] or ""
        return len(content) > 200
    return False


def insert_entry(conn, collection_id, c):
    entry_uuid = str(uuid.uuid4())
    key_points_json = json.dumps(c["key_points"])
    study_questions_json = json.dumps(c["study_questions"])
    tags_json = json.dumps(c["tags"])
    sources_json = json.dumps(c["sources"])

    conn.execute(
        """INSERT INTO commentary_entries
           (uuid, collection_id, book_id, chapter, verse_start, verse_end,
            reference_scope, title, summary, content, application, prayer,
            key_points, study_questions, language_code, theological_perspective,
            status, is_ai_generated, created_at, updated_at)
           VALUES (?,?,?,?,NULL,NULL,'chapter',?,?,?,?,?,?,?,?,?,?,1,?,?)""",
        (
            entry_uuid, collection_id, BOOK_ID, c["chapter"],
            c["title"], c["summary"], c["content"],
            c["application"], c["prayer"],
            key_points_json, study_questions_json,
            LANGUAGE_CODE, "evangelical", "draft",
            NOW, NOW
        )
    )
    conn.commit()
    return entry_uuid


def write_json(book_dir, c, entry_uuid):
    data = {
        "uuid": entry_uuid,
        "collection_name": COLLECTION_NAME,
        "author_type": "ai",
        "language_code": LANGUAGE_CODE,
        "theological_perspective": "evangelical",
        "status": "draft",
        "book_id": BOOK_ID,
        "book": BOOK_NAME,
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
        "updated_at": NOW,
    }
    # Verify no forbidden keys
    forbidden = {"is_ai_generated", "model_name", "prompt_version"}
    for k in forbidden:
        assert k not in data, f"Forbidden key found: {k}"

    filename = f"{c['chapter']:02d}.json"
    path = os.path.join(book_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Verify it parses back
    with open(path, "r", encoding="utf-8") as f:
        parsed = json.load(f)
    for k in forbidden:
        assert k not in parsed, f"Forbidden key in parsed JSON: {k}"

    return path


def update_progress(conn, last_chapter):
    leviticus_chapters = 27
    if last_chapter < leviticus_chapters:
        next_chapter = last_chapter + 1
        next_book_id = BOOK_ID
        next_book = BOOK_NAME
    else:
        next_chapter = 1
        next_book_id = 4
        next_book = "Numbers"

    data = {
        "next_book_id": next_book_id,
        "next_book": next_book,
        "next_chapter": next_chapter,
        "last_completed_book_id": BOOK_ID,
        "last_completed_book": BOOK_NAME,
        "last_completed_chapter": last_chapter,
        "completed": False,
        "updated_at": NOW
    }
    with open(PROGRESS_JSON, "w") as f:
        json.dump(data, f, indent=2)

    # Update DB progress table (schema uses current_book_id / current_chapter)
    existing = conn.execute(
        "SELECT id, uuid, collection_id FROM commentary_generation_progress WHERE deleted_at IS NULL LIMIT 1"
    ).fetchone()
    if existing:
        row_id, row_uuid, coll_id = existing
        conn.execute(
            """UPDATE commentary_generation_progress
               SET current_book_id=?, current_chapter=?,
                   last_completed_book_id=?, last_completed_chapter=?,
                   updated_at=?
               WHERE id=?""",
            (next_book_id, next_chapter, BOOK_ID, last_chapter, NOW, row_id)
        )
    else:
        row_uuid = str(uuid.uuid4())
        conn.execute(
            """INSERT INTO commentary_generation_progress
               (uuid, collection_id, language_code, current_book_id, current_chapter,
                last_completed_book_id, last_completed_chapter, target_book_id,
                chapters_per_batch, status, updated_at)
               VALUES (?,?,?,?,?,?,?,66,5,'draft',?)""",
            (row_uuid, COLLECTION_ID, LANGUAGE_CODE,
             next_book_id, next_chapter, BOOK_ID, last_chapter, NOW)
        )
    conn.commit()


def append_log(batch_id, start_ref, end_ref, generated, skipped, inserted, files):
    entry = {
        "timestamp": NOW,
        "generation_batch_id": batch_id,
        "start_reference": start_ref,
        "end_reference": end_ref,
        "chapters_generated": generated,
        "chapters_skipped": skipped,
        "db_rows_inserted": inserted,
        "files_written": files
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


def main():
    conn = sqlite3.connect(DB_PATH)
    book_dir = ensure_dirs()
    collection_id = get_collection_id(conn)

    batch_id = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    chapters_generated = 0
    chapters_skipped = 0
    db_rows_inserted = 0
    files_written = []
    start_ref = None
    end_ref = None

    for c in COMMENTARIES:
        chapter = c["chapter"]
        ref = f"{BOOK_NAME} {chapter}"

        if entry_exists(conn, collection_id, BOOK_ID, chapter):
            print(f"SKIP: {ref} already exists")
            chapters_skipped += 1
            if start_ref is None:
                start_ref = ref
            end_ref = ref
            continue

        print(f"GENERATE: {ref}")
        entry_uuid = insert_entry(conn, collection_id, c)
        path = write_json(book_dir, c, entry_uuid)

        if start_ref is None:
            start_ref = ref
        end_ref = ref

        chapters_generated += 1
        db_rows_inserted += 1
        files_written.append(path)
        print(f"  -> Inserted {entry_uuid}")
        print(f"  -> Written {path}")

    last_chapter = COMMENTARIES[-1]["chapter"]
    update_progress(conn, last_chapter)

    append_log(
        batch_id, start_ref or "N/A", end_ref or "N/A",
        chapters_generated, chapters_skipped,
        db_rows_inserted, len(files_written)
    )

    print(f"\n=== DONE ===")
    print(f"Generated: {chapters_generated}, Skipped: {chapters_skipped}")
    print(f"DB rows inserted: {db_rows_inserted}")
    print(f"Files written: {len(files_written)}")
    print(f"Next: {BOOK_NAME} {last_chapter + 1}" if last_chapter < 27 else "Next: Numbers 1")

    conn.close()


if __name__ == "__main__":
    main()
