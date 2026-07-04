"""Generate Leviticus chapters 2-6 commentaries."""
import sqlite3
import json
import uuid
import os
from datetime import datetime, timezone

DB_PATH = "believers_sword_commentaries.db"
GENERATED_DIR = "generated"
PROGRESS_JSON = "commentary_generation_progress.json"
LOG_FILE = "commentary_generation_log.jsonl"

BOOK_ID = 3
BOOK_NAME = "Leviticus"
BOOK_SLUG = "leviticus"
COLLECTION_ID = 1
COLLECTION_NAME = "Believers Sword Commentaries"

now_str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

CHAPTERS = [
    {
        "chapter": 2,
        "title": "The Grain Offering: Consecrated Labor and the Bread of Devotion",
        "summary": (
            "Leviticus 2 details the grain offering (מִנְחָה, minchah)—the only bloodless offering in the Levitical system. "
            "Whether fine flour, baked bread, griddle cakes, or firstfruits, the grain offering must include oil, salt, and frankincense, "
            "but no leaven or honey. A handful (the 'token portion') is burned on the altar as a memorial; the rest belongs to Aaron and his sons. "
            "Every act of faithful human labor—grain, bread, the fruit of the earth—can become consecrated worship when offered to God."
        ),
        "chapter_overview": (
            "Laws of the grain offering (minchah): fine flour with oil and frankincense; baked in oven, on a griddle, or in a pan; firstfruits of roasted grain. "
            "All include salt (the salt of the covenant); none include leaven or honey. A token portion is burned on the altar; the remainder belongs to Aaron and his sons as most holy."
        ),
        "content": (
            "If the burnt offering (Lev. 1) concerns blood atonement, Leviticus 2 introduces a different register of worship: the grain offering. "
            "Here is bread, oil, and grain—the fruit of human labor, the staples of Israelite life—offered to the God who gave the land and the harvest. "
            "Theology and daily life converge: what you eat to live, you may also offer to God.\n\n"
            "**What Is the Minchah?**\n\n"
            "The Hebrew word מִנְחָה (*minchah*) originally meant 'tribute' or 'gift'—the kind of gift a subject brings to a king. "
            "In Genesis, Jacob sends a *minchah* to Esau; in 1 Samuel, Hannah brings a *minchah* to the LORD. The word carries relational weight: "
            "a *minchah* is not payment for services rendered but an expression of honor and dependent relationship.\n\n"
            "In the sacrificial system, the *minchah* accompanies blood offerings, adding the dimension of consecrated labor to substitutionary atonement. "
            "Together, blood and grain say: *I give You myself (the animal), and I give You my work (the grain).*\n\n"
            "**The Forms of the Grain Offering (vv. 1-10)**\n\n"
            "The *minchah* could be offered in several forms: (1) raw fine flour with oil and frankincense (vv. 1-3); (2) baked loaves or wafers from an oven (vv. 4-5); "
            "(3) prepared on a griddle (vv. 5-6); (4) cooked in a pan (vv. 7-8); (5) firstfruits of grain, roasted with oil and frankincense (vv. 14-16). "
            "The variety is intentional: worshippers could bring what they had prepared in the way they prepared it. "
            "God meets the worshipper within the ordinary rhythms of their kitchen.\n\n"
            "A token portion—a handful of flour plus the frankincense—was burned on the altar as an 'azkara (*memorial portion*, v. 2). "
            "This handful represented the whole before God; the rest went to Aaron and his sons as their portion—'most holy, from the LORD's food offerings' (v. 3). "
            "The priests lived from the altar. Their daily bread was the people's worship.\n\n"
            "**No Leaven, No Honey—But Always Salt (vv. 11-13)**\n\n"
            "Two things were prohibited from the altar's fire: leaven (שְׂאֹר, *se'or*) and honey (דְּבַשׁ, *devash*). "
            "Leaven was a symbol of corruption and pervasiveness—it spreads through the whole loaf—and was therefore unfit for God's table. "
            "Jesus used leaven as a metaphor for the hypocrisy of the Pharisees and the insidious spread of false teaching (Matt. 16:6; 1 Cor. 5:6-8). "
            "At Passover, leaven was entirely removed from Israelite homes (Exod. 12:15), underscoring its association with Egypt and bondage.\n\n"
            "Honey was forbidden—not because it is bad, but because it ferments and thus belongs to the same category as leaven. "
            "God's altar is no place for the ambiguity of fermentation.\n\n"
            "Salt, however, is *required* (v. 13): 'You shall season all your grain offerings with salt. You shall not let the salt of the covenant with your God be lacking from your grain offering.' "
            "Salt preserves; it is the opposite of corruption. In the ancient Near East, salt sealed covenants (Num. 18:19; 2 Chr. 13:5). "
            "Every grain offering was seasoned with covenant fidelity. Worship divorced from covenant loyalty is no offering at all.\n\n"
            "**Firstfruits and Consecrated Labor (vv. 14-16)**\n\n"
            "The firstfruits grain offering—roasted, fresh grain—could be brought before the harvest was complete. "
            "This is significant: you do not wait until everything is safely in before you worship. The firstfruit is offered *before* the full harvest is secured—an act of trust and consecration. "
            "Paul uses this concept when he calls Christ 'the firstfruits of those who have fallen asleep' (1 Cor. 15:20), and when he calls the Spirit 'the firstfruits' of our final redemption (Rom. 8:23).\n\n"
            "**Christ, the True Grain Offering**\n\n"
            "Jesus declared Himself 'the bread of life' (John 6:35, 48)—not metaphorically remote, but the very nourishment the soul requires. "
            "Where the *minchah* brought flour, oil, and frankincense, Christ brought His whole self as the consecrated life of obedience to the Father. "
            "He was without the leaven of sin (Heb. 4:15; 1 Pet. 2:22). He was the grain of wheat that fell into the ground and died—and bore much fruit (John 12:24). "
            "When we break bread at the Lord's Table, we remember the grain offering: His body broken, His life given, consecrated labor offered to the Father on our behalf."
        ),
        "moral_lessons": [
            "The grain offering consecrates human work—bread is not merely food but can become worship when offered to God.",
            "The prohibition of leaven reminds us that what spreads unchecked (pride, sin, hypocrisy) has no place in our approach to God.",
            "Salt as the 'covenant seasoning' teaches that genuine worship is inseparable from covenant faithfulness and integrity.",
            "The variety of forms (oven, griddle, pan) shows that God meets worshippers within the ordinary circumstances of their daily lives.",
            "The firstfruits principle: trust God before the full harvest is secured; consecrate the beginning as an act of faith.",
            "The priests living from the altar reminds us that those who serve God's people should be supported by God's people."
        ],
        "application": (
            "Leviticus 2 sanctifies the ordinary. The grain offering took what was already on the table—flour, oil, salt—and made it an encounter with the holy. "
            "The New Testament equivalent is Romans 12:1-2: 'offer your bodies as a living sacrifice.' Your daily work—the bread you bake, the report you write, "
            "the child you raise—can be a grain offering when done 'as for the Lord' (Col. 3:23). "
            "The leaven prohibition invites self-examination: is there an area of your life where corruption or self-deception is quietly spreading? "
            "The salt of the covenant calls you to integrity—your private life and public worship should be seasoned with the same covenant faithfulness. "
            "Like the firstfruit offering, give before the harvest is safe. Consecrate the beginning of your day, your project, your season to God rather than waiting until success is secured."
        ),
        "prayer": (
            "Lord, we bring the grain of our daily labor to You. Consecrate our ordinary work—make our jobs, our creativity, our service the aroma of Christ to those around us. "
            "Root out from us the leaven of pride, hidden sin, and self-deception that corrupts worship from within. "
            "Season us with the salt of covenant faithfulness—may our inner life match our outward devotion. "
            "Like the firstfruits, we offer you our first and best before the outcome is certain, trusting that You are faithful. "
            "Thank You for Jesus, the Bread of Life, whose perfect consecrated life purchased our access to Your table. Amen."
        ),
        "key_points": [
            "The grain offering (minchah) consecrates human labor—bread, oil, grain—as an act of tribute and dependent relationship with God.",
            "The 'token portion' (azkara) burned on the altar represents the whole offering before God; the remainder fed the priests.",
            "Leaven and honey were forbidden: both ferment and symbolize corruption; they have no place at God's altar.",
            "Salt was required as the 'salt of the covenant'—every act of worship must be seasoned with covenant faithfulness and integrity.",
            "The firstfruits offering consecrates the beginning before the harvest is secured—a posture of trust and pre-emptive devotion.",
            "Jesus is the true Bread of Life (John 6:35)—the grain that fell into the ground and died to bear much fruit (John 12:24)."
        ],
        "study_questions": [
            "The grain offering could be prepared in multiple ways (oven, griddle, pan). What does this variety suggest about how God meets worshippers in their daily circumstances?",
            "Why was leaven prohibited from the altar? How does Jesus' use of leaven as a metaphor (Matt. 16:6) connect to the Levitical prohibition?",
            "Salt is called 'the salt of the covenant with your God' (v. 13). What does salt represent, and why is covenant fidelity essential to genuine worship?",
            "The firstfruits grain offering was presented before the full harvest was in. What does this posture of worship require in terms of trust and character?",
            "How does the concept of the grain offering shape your understanding of Jesus as 'the bread of life' (John 6:35)?",
            "Romans 12:1-2 calls believers to offer their bodies as 'living sacrifices.' How does Leviticus 2 give content to what that might look like practically?",
            "The priests lived from the grain offering—the people's worship was the priests' daily bread. What obligations does this create for how we support those in ministry?"
        ],
        "tags": ["grain offering", "minchah", "salt", "leaven", "firstfruits", "Leviticus", "worship", "covenant", "Christ", "bread of life"],
        "sources": [
            "Leviticus 2",
            "John 6:35, 48",
            "John 12:24",
            "1 Corinthians 15:20",
            "Romans 8:23",
            "Romans 12:1-2",
            "Colossians 3:23",
            "Matthew 16:6",
            "1 Corinthians 5:6-8",
            "Hebrews 4:15"
        ],
        "original_language_notes": [
            {
                "term": "מִנְחָה (minchah)",
                "language": "Hebrew",
                "verse": "2:1",
                "words_used": ["grain offering", "tribute", "gift"],
                "meaning": "Grain offering, tribute, gift. The word originally meant any gift brought to a superior—a king or a god—as an expression of homage and dependent relationship. In the sacrificial system it refers specifically to the bloodless offering of grain, flour, or bread. It accompanies blood offerings as the consecration of human labor alongside the substitutionary element. The same word is used for Jacob's gift to Esau (Gen. 32:13) and for the Magi's gifts to Jesus (Matt. 2:11 in its theological echo), emphasizing the tributary, relational character of the offering."
            },
            {
                "term": "סֹלֶת (solet)",
                "language": "Hebrew",
                "verse": "2:1",
                "words_used": ["fine flour", "semolina"],
                "meaning": "Fine flour, the highest quality of ground grain—sifted, refined, without coarse particles. The solet was the best the worshipper could grind. The requirement of fine flour teaches that worship is not an afterthought—you bring your best work, most carefully prepared, to God. The word appears throughout the grain offering regulations (Lev. 2; 6:14-18) and in the showbread (Lev. 24:5), which was also made of solet."
            },
            {
                "term": "אַזְכָּרָה (azkara)",
                "language": "Hebrew",
                "verse": "2:2",
                "words_used": ["memorial portion", "token portion", "representative portion"],
                "meaning": "Memorial portion, token portion. From זכר (zakar)—to remember. The azkara was the small handful burned on the altar that 'represented' the whole offering before God, causing God to 'remember' the worshipper. It is not a bribe—God does not need reminding—but a covenantal sign: this act is placed before the Lord as a memorial. The Psalms use the same root when David says 'may God remember you' (Ps. 20:3, where 'remember all your offerings' is the same verbal root)."
            },
            {
                "term": "מֶלַח (melach)",
                "language": "Hebrew",
                "verse": "2:13",
                "words_used": ["salt", "salt of the covenant"],
                "meaning": "Salt. Salt preserves and prevents corruption, making it the natural symbol for covenant permanence and integrity. Numbers 18:19 calls the priestly portions 'a covenant of salt forever,' and 2 Chronicles 13:5 refers to God's covenant with David as 'a covenant of salt.' Salt also seasons and makes food palatable—it is that which makes ordinary things good and lasting. Every grain offering was required to be salted, ensuring that the covenant dimension was never absent from Israel's worship."
            },
            {
                "term": "שְׂאֹר (se'or)",
                "language": "Hebrew",
                "verse": "2:11",
                "words_used": ["leaven", "yeast"],
                "meaning": "Leaven, fermentation agent. Leaven was a small piece of old fermented dough introduced into new dough to make it rise. Because of its pervasive, transforming, and corrupting character—and its association with the hasty departure from Egypt (Exod. 12:15, where all leaven must be removed)—it was forbidden from the altar. Jesus used this precise metaphor: 'Beware of the leaven of the Pharisees' (Matt. 16:6)—meaning that hypocrisy, like leaven, quietly and thoroughly corrupts the whole. Paul echoed this in 1 Corinthians 5:6-8."
            }
        ]
    },
    {
        "chapter": 3,
        "title": "The Peace Offering: Communion at God's Table",
        "summary": (
            "Leviticus 3 presents the fellowship or peace offering (שְׁלָמִים, shelamim)—the most joyful of the Levitical sacrifices. "
            "Unlike the wholly-consumed burnt offering, the peace offering was shared: specific fat portions and the blood went to God, "
            "the breast and right thigh to the priests, and the remainder was eaten by the worshipper and family. "
            "The result was a covenant meal at God's table—the closest image in the Old Testament of fellowship restored between holy God and redeemed people."
        ),
        "chapter_overview": (
            "Laws of the peace/fellowship offering (shelamim): bull or cow (v. 1-5), sheep (v. 6-11), or goat (v. 12-16). "
            "In each case, the worshipper presents the animal, lays hands on it, slaughters it at the tent entrance; the priest dashes the blood on the altar. "
            "The fat portions (fat, kidneys, liver) are burned for God; the remainder is a covenant meal shared by priests and worshipper. "
            "Perpetual statute: you shall not eat fat or blood (v. 17)."
        ),
        "content": (
            "If the burnt offering (Lev. 1) is the offering of total consecration and the grain offering (Lev. 2) consecrates human labor, "
            "the peace offering (Lev. 3) is the offering of *communion*—a shared meal between God, His priests, and His people. "
            "It is the most intimate offering in the Levitical system, and for many Israelites it was the most frequently experienced.\n\n"
            "**What Is Shelamim?**\n\n"
            "The Hebrew שְׁלָמִים (*shelamim*) is related to שָׁלוֹם (*shalom*)—peace, wholeness, completeness, well-being. "
            "The peace offering was not necessarily offered to *obtain* peace with God (that was the role of the sin and guilt offerings), "
            "but to *express and celebrate* peace already established. It was offered at moments of thanksgiving, to fulfill a vow, or as a freewill expression of love and gratitude. "
            "You don't eat with your enemy. The peace offering presupposes reconciliation and rejoices in it.\n\n"
            "**The Threefold Division of the Peace Offering**\n\n"
            "What made the peace offering unique was its distribution among three parties:\n\n"
            "1. **God's portion**: the fat (חֵלֶב, *ḥelev*)—the fat covering the inner organs, the kidneys with their fat, and the lobe of the liver—was burned on the altar as God's portion (vv. 3-5, 9-10, 14-15). "
            "Fat was considered the richest, best part of the animal. Giving God the fat first—before the meal begins—expresses that He is honored above all.\n\n"
            "2. **The priests' portion**: Aaron and his sons received the breast (waved before the LORD in the wave offering) and the right thigh (Lev. 7:31-34). "
            "The priests ate at the LORD's table; their portion was God's gift to them.\n\n"
            "3. **The worshipper's portion**: the remaining meat was returned to the offerant to be eaten—by the worshipper, family, and guests—in a sacred meal, before the LORD (Deut. 12:12, 18). "
            "This was covenant feasting: the same sacrifice that had atoned (via the blood) and honored God (via the fat) now fed the worshipper in God's presence.\n\n"
            "**The Three Forms: Bull, Sheep, Goat (vv. 1-16)**\n\n"
            "As with the burnt offering, three types of animals are permitted: a bull or cow (vv. 1-5), a sheep (vv. 6-11), or a goat (vv. 12-16). "
            "Notably, unlike the burnt offering (which required a male), the peace offering permitted female animals as well. "
            "The same hand-laying, slaughter, and blood-dashing procedures apply; the defining feature is the removal and burning of the specified fat portions.\n\n"
            "**The Perpetual Prohibition: No Fat, No Blood (v. 17)**\n\n"
            "The chapter closes with an absolute statute: 'It shall be a perpetual statute throughout your generations, in all your dwelling places, "
            "that you eat neither fat nor blood.' "
            "The fat belongs to God—it is His richest portion, and to eat it would be to steal from God's table (Lev. 7:23-25). "
            "The blood belongs to God as the bearer of life (Lev. 17:11)—'for the life of the flesh is in the blood, and I have given it for you on the altar to make atonement for your souls.' "
            "These prohibitions frame all eating as covenant eating: you eat what God gives you; His portion remains His.\n\n"
            "**The Peace Offering and the Lord's Supper**\n\n"
            "The peace offering is the Old Testament's clearest foreshadowing of communion—the covenant meal. "
            "In Christ, the full peace offering has been offered: He is our peace (Eph. 2:14), who has 'destroyed the dividing wall of hostility.' "
            "His blood atones (the blood on the altar); His body is given (the fat of consecration burned); and then He calls us to eat at His table—'Take, eat; this is my body' (Matt. 26:26). "
            "The Lord's Supper is not a new invention but the fulfillment of what every peace offering announced: God and His people, restored to fellowship, feasting together.\n\n"
            "When Jesus ate with tax collectors and sinners (Luke 15:2), the Pharisees were scandalized. They did not understand that every shared meal, in Israel, carried echoes of the shelamim: "
            "the presupposition of peace, the inclusion of the guest at God's table, the invitation to feast in the presence of the Holy."
        ),
        "moral_lessons": [
            "The peace offering teaches that the goal of atonement is not merely forgiveness but restored fellowship—God wants to feast with His people.",
            "Giving God the fat first (the best portion) before eating yourself is the pattern of all Christian stewardship: first fruits, first priority, first honor to God.",
            "The inclusion of female animals in the peace offering reminds us that God's hospitality and fellowship are for all—no class restriction on communion.",
            "The shared meal—God, priests, and worshipper together—models the community dimension of worship: genuine fellowship with God creates fellowship among people.",
            "The blood prohibition teaches reverence for life and the costliness of atonement; life is not ours to consume but God's to give.",
            "The peace offering was voluntary (freewill or thanksgiving)—the most joyful worship is not compelled but freely given from a heart that has experienced grace."
        ],
        "application": (
            "Leviticus 3 invites us to examine the quality of our communion with God. Do we approach Him only when we need something—only at the sin-offering moments? "
            "Or do we bring voluntary peace offerings—acts of thanksgiving and freewill praise—simply because we delight in His presence? "
            "The peace offering says: *God wants to eat with you.* The Lord's Supper is the Christian peace offering—come often, come gratefully, come knowing that the blood of Christ has already made the feast possible. "
            "The fat-first principle also applies: when we plan our budget, our time, our energy, do we give God the best first or the leftovers? "
            "The peace offering begins with the altar, not the table; God's portion precedes ours. Bring your thanksgiving before you enjoy your blessing."
        ),
        "prayer": (
            "Lord, we come not only with our needs but with thanksgiving—a freewill offering of praise because You have made us whole. "
            "Thank You that Christ is our peace, that the dividing wall of hostility has been torn down, and that we are invited to eat at Your table. "
            "Help us to give You the fat of our lives first—our best hours, our richest gifts, our deepest attention—before we consume what remains. "
            "May our meals, our communities, our shared lives carry the echo of the shelamim: peace restored, fellowship real, the holy God present among His feasting people. Amen."
        ),
        "key_points": [
            "The peace offering (shelamim) celebrates fellowship restored—it is the most joyful Levitical sacrifice, a shared meal between God, priests, and worshipper.",
            "The fat (ḥelev) went to God as His richest portion; the priests received the breast and thigh; the worshipper received the rest—a three-way covenant meal.",
            "The peace offering was voluntary—freewill or thanksgiving—expressing delight in God's presence rather than responding to a specific requirement.",
            "The perpetual prohibition of fat and blood (v. 17) frames all eating as covenant eating: life and richness ultimately belong to God.",
            "Christ is our peace (Eph. 2:14), and the Lord's Supper is the New Testament peace offering—the feast of restored communion.",
            "The peace offering presupposes reconciliation; it is offered not to obtain peace but to celebrate the peace already given through atonement."
        ],
        "study_questions": [
            "The peace offering was voluntary, offered in thanksgiving or to fulfill a vow. What does the voluntary nature of this offering teach about the heart of genuine worship?",
            "Why was the fat designated as God's portion? What does 'giving the best first' look like practically in your life today?",
            "The peace offering was a shared meal—God received the fat, the priests got a portion, and the worshipper ate the rest. What does this three-way sharing teach about the community dimension of worship?",
            "Paul says Christ 'is our peace' (Eph. 2:14). How does the fellowship offering illuminate what Christ accomplished in making peace between Jews, Gentiles, and God?",
            "The blood and fat prohibition (v. 17) was a 'perpetual statute.' What principle does this teach about the boundary between what is God's and what is ours?",
            "How is the Lord's Supper a fulfillment of the peace offering? What elements carry forward, and what is new?",
            "Jesus ate with tax collectors and sinners, which was scandalous. In light of the peace offering's logic (feasting presupposes peace), why did Jesus' table fellowship make the theological statement it did?"
        ],
        "tags": ["peace offering", "shelamim", "fellowship", "communion", "shalom", "Leviticus", "Christ our peace", "covenant meal", "Lord's Supper", "thanksgiving"],
        "sources": [
            "Leviticus 3",
            "Leviticus 7:11-21, 31-34",
            "Leviticus 17:11",
            "Ephesians 2:14",
            "Matthew 26:26",
            "Romans 5:1",
            "Deuteronomy 12:12, 18",
            "Luke 15:2",
            "Colossians 1:20"
        ],
        "original_language_notes": [
            {
                "term": "שְׁלָמִים (shelamim)",
                "language": "Hebrew",
                "verse": "3:1",
                "words_used": ["peace offering", "fellowship offering", "well-being offering"],
                "meaning": "Peace/fellowship/well-being offering. From the root שלם (shalem)—to be complete, whole, at peace. The shelamim is the 'completeness offering'—not offered to obtain peace, but expressing the wholeness and completeness of the relationship already restored. Related to shalom (שָׁלוֹם), the comprehensive Hebrew word for peace, prosperity, health, and flourishing. The New Testament applies this concept directly to Christ: Ephesians 2:14 declares 'He himself is our peace (εἰρήνη, eirene—the Greek equivalent).'"
            },
            {
                "term": "חֵלֶב (ḥelev)",
                "language": "Hebrew",
                "verse": "3:3",
                "words_used": ["fat", "suet", "fat portions"],
                "meaning": "Fat, the internal fat of an animal—particularly the fat covering the kidneys, intestines, and liver. The ḥelev was considered the richest, most nourishing part of the animal. To give God the ḥelev first was to honor Him with the best. Leviticus 7:23-25 strictly prohibits Israel from eating the ḥelev of ox, sheep, or goat; anyone who does is cut off from the people. The same root is used in Psalm 81:16 and 147:14 where God feeds His people 'the finest/fat of wheat'—ḥelev as the richest provision."
            },
            {
                "term": "כְּלָיוֹת (kelayot)",
                "language": "Hebrew",
                "verse": "3:4",
                "words_used": ["kidneys", "reins"],
                "meaning": "Kidneys. In Hebrew thought, the kidneys were considered a seat of deep emotion, will, and moral sensibility—analogous to what we might call the 'gut' or 'conscience.' Several Psalms use the kidneys as the seat of the inner life (Ps. 16:7; 26:2). That the kidneys were given to God in the peace offering (along with their surrounding fat) symbolized giving to God one's innermost self—the will and conscience, not just external action. The kidneys of the sacrifice symbolized the inner offering of the worshipper."
            },
            {
                "term": "תְּנוּפָה (tenufah)",
                "language": "Hebrew",
                "verse": "3:1",
                "words_used": ["wave offering", "presented by waving"],
                "meaning": "Wave offering, presentation by elevation or swinging. From נוף (nuf)—to wave, swing, brandish. In the peace offering, the breast was waved (tenufah) before the LORD as a gesture of presenting it to God and receiving it back as a priestly portion (Lev. 7:30). The waving motion—forward and back, up and down—may have symbolized bringing the offering before God and having Him return it as a gift. The tenufah made explicit the transaction: this belongs to God; He gives it to the priests."
            }
        ]
    },
    {
        "chapter": 4,
        "title": "The Sin Offering: Atonement for Unintentional Sin",
        "summary": (
            "Leviticus 4 introduces the sin offering (חַטָּאת, ḥaṭṭa't)—God's provision for unintentional sins committed by the anointed priest, "
            "the whole congregation, a leader, or an ordinary person. The chapter works outward from the priest (whose sin affects the whole people) "
            "to the individual. Each case involves blood ritual—sprinkling before the veil, application to the altar horns—with the emphatic result: 'the priest shall make atonement for him and he shall be forgiven.' "
            "Forgiveness is God's gift, not humanity's achievement."
        ),
        "chapter_overview": (
            "The sin offering (ḥaṭṭa't) for unintentional sins: for the anointed priest (young bull, blood sprinkled before veil and on incense altar horns; fat burned; carcass burned outside camp); "
            "for the whole congregation (same procedure); for a leader (male goat, blood on altar horns); for an ordinary person (female goat or lamb). "
            "Each case ends: 'the priest shall make atonement for him, and he shall be forgiven.'"
        ),
        "content": (
            "Leviticus 4 confronts a theological problem the burnt offering does not address: what happens when an Israelite sins—not presumptuously, but by mistake, "
            "by inadvertence, by ignorance, or by the kind of failure that is only later recognized as sin? "
            "The burnt offering was general consecration; the sin offering is specific remedy.\n\n"
            "**The Nature of ḥaṭṭa't**\n\n"
            "The word חַטָּאת (*ḥaṭṭa't*) means both 'sin' and 'sin offering'—the same Hebrew word covers the act and its remedy. "
            "This ambiguity is theologically loaded. The same word that names the failure also names the sacrifice that deals with it. "
            "This double meaning reaches its apex in 2 Corinthians 5:21: 'God made him who had no sin to be sin (ἁμαρτία, *hamartia*) for us, so that in him we might become the righteousness of God.' "
            "Christ was made the ḥaṭṭa't—He became identified with sin itself so that sin could be fully judged in His body.\n\n"
            "**Unintentional Sin (v. 2)**\n\n"
            "The key qualification is 'if anyone sins unintentionally (בִּשְׁגָגָה, *bishgagah*).' "
            "The term refers to inadvertence—an error, a failure of oversight, a sin committed without full awareness of its gravity. "
            "This is not a loophole but a recognition of human moral fragility: we are more sinful than we know. "
            "Later (Num. 15:30-31), willful, 'high-handed' sin is explicitly excluded from the sacrificial system's coverage—such sin required a different remedy. "
            "But for the vast terrain of human moral failure that falls short of deliberate rebellion, God graciously provided: there is an offering for this.\n\n"
            "**The Anointed Priest (vv. 3-12)**\n\n"
            "The chapter begins with the most serious case: the anointed priest. "
            "His office represents the whole nation before God; his sin 'brings guilt on the people' (v. 3). "
            "Spiritual leadership amplifies moral influence—for good or ill. The priest's sin offering requires a young bull—the most costly offering—and the most elaborate blood ritual: "
            "blood is sprinkled seven times before the veil of the sanctuary (approaching the very presence of God) and applied to the four horns of the incense altar (the golden altar, closest to the Most Holy Place). "
            "The fat is burned on the altar; the carcass is carried outside the camp and burned on the ash heap. This 'outside the camp' disposal is significant (see Heb. 13:11-13).\n\n"
            "**The Congregation (vv. 13-21)**\n\n"
            "If the whole assembly sins unintentionally (and later recognizes the sin), the elders lay hands on the bull on behalf of the entire community. "
            "Corporate sin requires corporate acknowledgment and corporate atonement. The community is not a collection of isolated individuals; its sin is genuinely shared. "
            "This principle shapes how Israel confesses on the Day of Atonement and how Nehemiah, Ezra, and Daniel confess on behalf of their people (Neh. 1:6; Dan. 9:5).\n\n"
            "**The Leader and the Individual (vv. 22-35)**\n\n"
            "The scale of the offering reflects the scale of the sin's impact. A leader (נָשִׂיא, *nasi*) brings a male goat; an ordinary person brings a female goat or lamb. "
            "In each case, the worshipper lays his hand on the animal, slaughters it, and the priest makes atonement with the blood. "
            "The gradated scale is not God favoring the rich; it is God calibrating accountability: more leadership means more responsibility, which requires more costly atonement.\n\n"
            "**The Assurance: 'He Shall Be Forgiven' (vv. 20, 26, 31, 35)**\n\n"
            "Four times the chapter repeats the phrase: 'the priest shall make atonement for him, and he shall be forgiven.' "
            "This is not tentative or conditional; the forgiveness is declarative. God announces the result. "
            "Where the sacrifice is properly offered, forgiveness follows—not as a hope but as a guarantee. "
            "The New Testament equivalent is 1 John 1:9: 'If we confess our sins, he is faithful and just to forgive us our sins.' "
            "The faithfulness and justice are God's; the result is certain.\n\n"
            "**Christ Outside the Camp**\n\n"
            "Hebrews 13:11-13 draws a direct line between the disposal of the sin offering's carcass 'outside the camp' and the crucifixion: "
            "'Jesus also suffered outside the gate in order to sanctify the people through his own blood. Therefore let us go to him outside the camp.' "
            "The cross happened outside Jerusalem's walls—outside the camp of respectable religion—just as the ḥaṭṭa't carcass was burned outside the camp. "
            "To follow Christ means bearing the reproach of going 'outside'—outside the safety of social approval, outside self-sufficient religiosity, to the place where the sin offering was made."
        ),
        "moral_lessons": [
            "Leadership multiplies moral influence—the priest's sin affected the whole congregation, reminding leaders that their private choices have public consequences.",
            "The sin offering for unintentional sins shows that moral blindness is still sin: what we don't know we are doing can still damage our relationship with God and others.",
            "The repeated 'he shall be forgiven' teaches that forgiveness from God is not uncertain or merely hoped-for—where confession and sacrifice are genuine, God grants assurance.",
            "Corporate sin requires corporate acknowledgment; communities share moral responsibility and cannot simply leave the burden to individuals.",
            "The gradated offerings (bull to lamb) reflect proportional accountability—more authority means more responsibility before God.",
            "Christ became the ḥaṭṭa't (2 Cor. 5:21): not merely a sacrifice for sin but identified with sin itself, bearing its full weight so we might be fully freed."
        ],
        "application": (
            "Leviticus 4 is a chapter for those who have discovered—late—that something they did was wrong. "
            "The sin offering exists precisely because our moral self-knowledge is incomplete. We damage relationships, speak unkindly, neglect duties, fail people—and sometimes only realize it later. "
            "God's provision is not 'you should have known better' but 'here is how to make it right.' "
            "The 'he shall be forgiven' refrain is the most important thing in this chapter—not the procedures but the assurance. "
            "God is not reluctant to forgive; the entire elaborate system was designed to make forgiveness certain and accessible. "
            "Going 'outside the camp' with Christ (Heb. 13:13) is the application: identify with the One who was made sin for you, "
            "even when that identification costs you social comfort or religious approval."
        ),
        "prayer": (
            "Merciful God, You know what we do not know about ourselves. The sins we have committed without full awareness—the damage we have caused in ignorance—weigh on us once we see them. "
            "Thank You that Your provision preceded our knowledge of our need. Thank You that Christ was made sin for us—the ultimate ḥaṭṭa't—so that every failure we discover can be brought to His cross. "
            "Grant us the humility to keep short accounts with You, to confess quickly when we see sin, and to receive forgiveness not as a possibility but as Your declared reality. "
            "Lead us outside the camp—to Christ, to the cross, to the place where sin was dealt with finally. Amen."
        ),
        "key_points": [
            "The sin offering (ḥaṭṭa't) addresses unintentional sins—the vast landscape of moral failure that falls short of deliberate rebellion but is still real sin.",
            "The same Hebrew word (ḥaṭṭa't) means both 'sin' and 'sin offering'—pointing forward to Christ who was made sin (2 Cor. 5:21) to become the remedy.",
            "The anointed priest's sin required the most costly offering because spiritual leadership amplifies moral impact—his sin 'brought guilt on the people.'",
            "The repeated assurance—'he shall be forgiven'—is declarative, not conditional: where the sacrifice is properly made, forgiveness is certain.",
            "The carcass burned 'outside the camp' foreshadows Christ crucified outside Jerusalem's gate (Heb. 13:11-13): to follow Christ is to go 'outside.'",
            "Corporate sin requires corporate acknowledgment; the congregation's sin offering required communal confession and representative hand-laying."
        ],
        "study_questions": [
            "The sin offering specifically covers 'unintentional' sins—things done in ignorance or inadvertence. What does this category of sin reveal about the depth of human moral blindness?",
            "The Hebrew word ḥaṭṭa't means both 'sin' and 'sin offering.' How does this double meaning illuminate 2 Corinthians 5:21, where Christ is 'made sin for us'?",
            "Why did the anointed priest's sin require the most elaborate and costly sin offering? What principle of spiritual leadership does this establish?",
            "Four times in Leviticus 4 God declares: 'He shall be forgiven.' What does this repetition teach about the certainty of forgiveness available through the sacrifice?",
            "How does the disposal of the sin offering 'outside the camp' foreshadow Christ's crucifixion outside Jerusalem's gate (Heb. 13:11-13)?",
            "The congregation's sin required communal confession and a representative offering. What does this teach about corporate moral responsibility in a church, family, or nation?",
            "Is there a difference between 'unintentional sin' and 'ignorance'? Are there sins you do habitually that you have not yet fully recognized as sin? What would the sin-offering posture look like for you?"
        ],
        "tags": ["sin offering", "hattaat", "atonement", "unintentional sin", "forgiveness", "Leviticus", "Christ", "outside the camp", "confession", "leadership"],
        "sources": [
            "Leviticus 4",
            "2 Corinthians 5:21",
            "Hebrews 13:11-13",
            "Numbers 15:30-31",
            "1 John 1:9",
            "Nehemiah 1:6",
            "Daniel 9:5",
            "Romans 8:3"
        ],
        "original_language_notes": [
            {
                "term": "חַטָּאת (ḥaṭṭa't)",
                "language": "Hebrew",
                "verse": "4:3",
                "words_used": ["sin offering", "sin", "purification offering"],
                "meaning": "Sin offering; also the word for 'sin' itself. The same root חטא (ḥata')—to miss the mark, to sin—generates both the act and the remedy. This linguistic double is theologically profound: the ḥaṭṭa't offering takes the name of the very thing it deals with, pointing forward to the New Testament's declaration in 2 Corinthians 5:21 that God 'made him who knew no sin to be sin (hamartia) for us.' Some scholars prefer translating ḥaṭṭa't as 'purification offering' to emphasize its cleansing function. Both readings are present: it addresses personal guilt (sin offering) and defilement (purification offering)."
            },
            {
                "term": "בִּשְׁגָגָה (bishgagah)",
                "language": "Hebrew",
                "verse": "4:2",
                "words_used": ["unintentionally", "through error", "inadvertently", "by mistake"],
                "meaning": "Unintentionally, inadvertently, by error. From שגג (shagag)—to err, stray, wander. The bishgagah sin is committed without full deliberate intent—through oversight, ignorance of the law, incomplete moral awareness, or the kind of human frailty that operates below the level of conscious choice. Numbers 15:30-31 explicitly excludes 'high-handed' (intentional, defiant) sin from the sacrificial system's coverage. The very existence of the bishgagah category acknowledges that human moral self-knowledge is always partial—we sin more than we know."
            },
            {
                "term": "נָשִׂיא (nasi)",
                "language": "Hebrew",
                "verse": "4:22",
                "words_used": ["leader", "ruler", "chief", "prince"],
                "meaning": "Leader, tribal chief, prince, elevated one. From נשא (nasa')—to lift up, carry, bear. A nasi is one who is 'lifted up'—elevated in position and therefore carrying greater responsibility. The same word is used for tribal heads in Numbers, for Ezekiel's restored prince, and for the emerging leader of the community. The sin offering for a nasi (a male goat, less costly than the priest's bull but more costly than an individual's) reflects the principle that leadership accountability is proportionally higher: the one who is lifted up bears more when he falls."
            },
            {
                "term": "כִּפֶּר (kipper)",
                "language": "Hebrew",
                "verse": "4:20",
                "words_used": ["make atonement", "atone", "cover"],
                "meaning": "To make atonement, to atone, to ransom, to cover. The precise etymology is debated: possibly from כפר (kaphar)—to cover; or from an Akkadian root meaning 'to wipe away.' In the sacrificial context, kipper describes the priestly act of applying blood to the altar to accomplish reconciliation between the worshipper and God. It is the operative word of the entire sacrificial system—appearing more than 100 times in Leviticus. Its culmination is Yom Kippur (יוֹם כִּפֻּר, the Day of Atonement)—the day of comprehensive covering/wiping away of sin."
            }
        ]
    },
    {
        "chapter": 5,
        "title": "The Guilt Offering: When Negligence and Treachery Require Restitution",
        "summary": (
            "Leviticus 5 bridges the sin offering and the guilt offering (אָשָׁם, asham), addressing specific failures: silence when called to testify, "
            "touching unclean things, or making rash oaths. A graduated provision allows the very poor to bring grain instead of an animal. "
            "The chapter then transitions to the guilt offering—required when a person wrongs God or neighbor in matters of trust, "
            "requiring both full atonement and restitution plus a fifth. The asham teaches that genuine repentance restores not only relationship but what was taken."
        ),
        "chapter_overview": (
            "Specific sins requiring sin offering: failure to testify (v. 1), touching unclean animals or human uncleanness (vv. 2-3), rash oaths (vv. 4-6). "
            "Graduated provision: two birds if too poor for a lamb; grain if too poor for birds (vv. 7-13). "
            "Transition to the guilt offering (asham): for sacrilege against holy things (vv. 14-16), and for unintentional violation of God's commands with uncertain awareness (vv. 17-19)."
        ),
        "content": (
            "Leviticus 5 operates at the intersection between the sin offering and the guilt offering, addressing some of the most specific categories of moral failure in the Levitical system. "
            "Two things make this chapter distinctive: a graduated poverty provision that ensures even the destitute can make atonement, "
            "and the introduction of the guilt offering (asham)—an offering that requires not just sacrifice but restitution.\n\n"
            "**Three Specific Sins (vv. 1-6)**\n\n"
            "*First, the sin of silence (v. 1):* If a person hears a public call for witnesses and has information relevant to a case but stays silent, "
            "'he shall bear his iniquity.' Silence in the face of injustice—when the truth is known and withheld—is a sin requiring atonement. "
            "Truth-telling is not optional in covenant community; perjury by omission is still perjury.\n\n"
            "*Second, touching uncleanness (vv. 2-3):* Inadvertent contact with a carcass, creature, or human uncleanness that is later recognized creates a state of ritual impurity requiring remedy. "
            "Impurity is contagious in Leviticus—contact with death spreads it. The sin offering does not treat ritual impurity as trivial; it takes seriously that the people of God are to be a clean community before the holy God.\n\n"
            "*Third, rash oaths (vv. 4-6):* If a person swears thoughtlessly—'I will do this' or 'I will not do that'—without considering whether they can keep the oath, "
            "and then fails to follow through, the breach requires a sin offering. Words uttered in the presence of the holy God are binding. "
            "Jesus echoes this: 'Let your yes be yes and your no be no' (Matt. 5:37).\n\n"
            "**The Graduated Provision: Access for All (vv. 7-13)**\n\n"
            "What follows is one of Leviticus's most pastoral passages. If a person cannot afford a lamb (v. 7), they may bring two turtledoves or pigeons. "
            "If they cannot afford even birds (v. 11), they may bring 'a tenth of an ephah of fine flour as a sin offering'—grain. "
            "Notably, no oil or frankincense is added (unlike the grain offering), and only a token portion is burned; the atonement is still fully accomplished. "
            "The provision says clearly: *no one is too poor to be forgiven.* God calibrates His requirements to human capacity. "
            "This is where Luke 2:24 (Mary and Joseph's bird offering after Jesus' birth) carries its full weight—they were among the people God had explicitly provided for in Leviticus 5.\n\n"
            "**The Guilt Offering (Asham): Sacrilege and Restitution (vv. 14-19)**\n\n"
            "The asham (guilt offering) addresses a different category of sin—not general moral failure but specific wrongs involving breach of trust and measurable damage: "
            "unauthorized use of holy things (sacred donations, tithes, firstfruits); and violations of God's commands whose exact nature may not be certain (v. 17-18). "
            "What distinguishes the asham from the ḥaṭṭa't is that the asham requires restitution: 'He shall make restitution for what he has done wrong in regard to the holy thing and shall add a fifth to it' (v. 16). "
            "Not only is the sacrifice offered and the relationship restored, but what was taken is repaid—plus twenty percent. "
            "Forgiveness does not erase obligation; in God's economy, genuine repentance makes things right as well as making things clean.\n\n"
            "**The Ram of the Guilt Offering**\n\n"
            "The asham required a ram—not a small offering—'valued by you in silver shekels.' The costly nature of the ram, and the requirement that it be assessed for its monetary value, "
            "introduces a commercial precision into the sacrificial system. Sin has a cost. Breach of trust can be measured. God takes wrongs done to holy things with economic seriousness.\n\n"
            "**Christ as Our Asham**\n\n"
            "Isaiah 53:10 is the astonishing prophetic application: 'When you make his soul an offering for guilt (asham), he shall see his offspring; he shall prolong his days.' "
            "The Suffering Servant is made the asham—the guilt offering—for His people. Not merely the ḥaṭṭa't (sin offering) but the asham: the offering that not only atones but also pays back what was owed. "
            "Christ's work is not merely forgiveness but restitution—the full payment of every debt, the restoration of everything lost to sin."
        ),
        "moral_lessons": [
            "The sin of silence—withholding testimony when called—reminds us that truth-telling is a moral obligation; failing to speak the truth is as much a sin as speaking falsely.",
            "God's graduated poverty provision teaches that He matches His requirements to human capacity; no one is too poor, too broken, or too little to receive His forgiveness.",
            "The guilt offering's restitution requirement teaches that genuine repentance makes things right—where sin has caused measurable damage, restoration is part of repentance.",
            "Rash oaths that are broken—promising things we cannot deliver—sin against God and community; let your words be careful, few, and trustworthy.",
            "The 'fifth added' (120% restitution) shows that sin has costs; forgiveness does not eliminate obligation to those we have wronged.",
            "Isaiah 53:10 identifies Christ as the asham—the guilt offering—teaching that His death was not only forgiveness but full restitution of everything we owed."
        ],
        "application": (
            "Leviticus 5 confronts the temptation to separate spiritual and material dimensions of repentance. "
            "The guilt offering says: genuine repentance includes making it right. If you have withheld someone's wages, cheated in a business deal, used what belongs to God (your tithe, your gifts) for your own purposes, "
            "then the Levitical principle applies: restore it, plus a fifth. "
            "Zacchaeus understood this: 'If I have defrauded anyone of anything, I restore it fourfold' (Luke 19:8). "
            "The graduated sin offering provision also speaks powerfully to pastoral ministry: no one is too far from God's provision for forgiveness. "
            "When someone says 'I have nothing to offer God,' the answer is: God already calibrated the offering for you. "
            "The cross is the asham—the guilt offering—that cost Christ everything and paid back everything we owe."
        ),
        "prayer": (
            "Lord of justice and mercy, thank You that no one is too poor, too broken, or too sinful to receive Your forgiveness. "
            "Forgive the sins of our silence—the truth we have withheld, the witness we have failed to give, the injustice we have allowed by saying nothing. "
            "Where we have used what belongs to You or others for our own purposes, grant us the courage to make restitution—to restore, not merely to say sorry. "
            "Thank You that Christ was made our asham—the guilt offering—who paid not just the fine but the full debt, restoring everything we lost. Amen."
        ),
        "key_points": [
            "Leviticus 5 opens with the sin of silence: withholding testimony when summoned is a sin requiring atonement—truth-telling is covenantal.",
            "God's graduated provision (lamb → birds → grain) ensures that no one is too poor to access forgiveness; God scales His requirements to human capacity.",
            "The guilt offering (asham) requires both sacrifice and restitution—genuine repentance makes things right as well as making things clean.",
            "The restitution formula (value + a fifth = 120%) shows that sin has measurable costs and forgiveness does not eliminate the obligation to restore.",
            "Isaiah 53:10 applies the asham directly to Christ: the Suffering Servant was made a guilt offering for His people—atonement and full restitution.",
            "Rash oaths—promises made without capacity to keep them—sin against God's character as truth; let your words be careful and your yes mean yes."
        ],
        "study_questions": [
            "The first sin in Leviticus 5 is the sin of silence—failing to testify when called. What moral principle does this establish about the relationship between truth and community?",
            "The graduated poverty provision allows grain as a sin offering for the very poor. What does this reveal about God's character and the accessibility of His forgiveness?",
            "What is the difference between the sin offering (ḥaṭṭa't) and the guilt offering (asham)? Why does the asham require restitution as well as sacrifice?",
            "The guilt offering required restitution plus a fifth (120%). How does Zacchaeus's response in Luke 19:8 reflect this principle? What would this look like practically in your context?",
            "Isaiah 53:10 calls Christ an asham. What does it mean that Christ's death was not only a sin offering but a guilt offering—requiring not just forgiveness but full payment and restitution?",
            "Jesus teaches 'let your yes be yes' (Matt. 5:37). How does the Leviticus 5 warning about rash oaths connect to Jesus' teaching on truthful speech?",
            "Are there areas in your life where you have received God's forgiveness but have not yet made practical restitution to those you have wronged? What would the guilt offering posture look like there?"
        ],
        "tags": ["guilt offering", "asham", "sin offering", "restitution", "silence", "rash oaths", "Leviticus", "Isaiah 53", "Christ", "forgiveness"],
        "sources": [
            "Leviticus 5",
            "Isaiah 53:10",
            "Luke 2:24",
            "Luke 19:8",
            "Matthew 5:37",
            "Numbers 5:5-7",
            "Romans 3:25",
            "Hebrews 2:17"
        ],
        "original_language_notes": [
            {
                "term": "אָשָׁם (asham)",
                "language": "Hebrew",
                "verse": "5:15",
                "words_used": ["guilt offering", "guilt", "trespass offering"],
                "meaning": "Guilt offering; also the state of being guilty. From the root אשם (asham)—to be guilty, to incur guilt. Like ḥaṭṭa't, the word names both the offense and the remedy. The asham is distinguished from the ḥaṭṭa't by its requirement of restitution: where the ḥaṭṭa't addresses the broken relationship, the asham also addresses the measurable wrong done—the thing taken, damaged, or misappropriated. Isaiah 53:10 uses this precise word for the Servant's death: 'when you make his soul an asham'—not merely an offering for sin but a guilt offering that pays full restitution."
            },
            {
                "term": "מַעַל (ma'al)",
                "language": "Hebrew",
                "verse": "5:15",
                "words_used": ["trespass", "unfaithful act", "breach of faith", "sacrilege"],
                "meaning": "Unfaithfulness, breach of trust, sacrilege. A ma'al is a betrayal of trust—specifically the appropriation of what belongs to someone else (God or neighbor) for one's own use. In Leviticus 5:15, it refers to unauthorized use of holy things (God's property). The same word appears in Joshua 7:1 (Achan's sin), Ezra 10:2 (marriage to foreign women as covenant unfaithfulness), and throughout Chronicles for religious infidelity. Ma'al is not merely a mistake but a breach—a violation of the relationship of trust that structures the covenant."
            },
            {
                "term": "בָּטָא (bata')",
                "language": "Hebrew",
                "verse": "5:4",
                "words_used": ["swear rashly", "speak rashly", "utter thoughtlessly"],
                "meaning": "To speak rashly, utter thoughtlessly, swear without deliberation. The word appears in only a handful of Old Testament passages, always associated with speech that outpaces thought—oaths made impulsively without considering whether they can be kept. The rash oath of Leviticus 5:4 is not deliberate false swearing (perjury) but thoughtless overcommitting. The provision of the sin offering for bata'-speech signals that God takes careless speech seriously even when no malice was intended."
            },
            {
                "term": "חֹמֶשׁ (ḥomesh)",
                "language": "Hebrew",
                "verse": "5:16",
                "words_used": ["a fifth", "one fifth", "twenty percent"],
                "meaning": "A fifth, one-fifth, twenty percent. The ḥomesh was added to the principal amount as restitution in guilt offerings involving sacred property. The same formula appears in Numbers 5:7 for wrongs done to neighbors and in Leviticus 27:13-31 for redeeming sacred vows. Adding a fifth to the principal (100% + 20% = 120%) ensured that restitution exceeded the original loss—genuine repentance does not merely return what was taken but restores something beyond that. This principle underpins Zacchaeus's fourfold restitution (Luke 19:8) as a superabundant expression of the asham principle."
            }
        ]
    },
    {
        "chapter": 6,
        "title": "The Perpetual Fire: Priestly Faithfulness and the Holy Things",
        "summary": (
            "Leviticus 6 opens with additional guilt offering regulations (the 'completed' guilt offering for deception and fraud against neighbor, requiring full restitution plus a fifth), "
            "then turns primarily to instructions for the priests regarding the daily maintenance of the offerings: "
            "the burnt offering fire must never go out; the grain offering is most holy; the sin offering eaten by priests is most holy and must be handled with precision. "
            "The chapter establishes the theology of 'most holy'—things consecrated to God require constant, faithful attention and cannot be treated carelessly."
        ),
        "chapter_overview": (
            "Guilt offering extension: fraud and deception against neighbor, requiring full restitution plus a fifth plus a ram (vv. 1-7). "
            "Priestly instructions: the burnt offering's fire must burn continuously, ash removed, priests in linen garments (vv. 8-13). "
            "Grain offering for priests: Aaron's sons receive portions; all grain offerings are fully consumed—priests' daily offering (vv. 14-23). "
            "Sin offering instructions: most holy, eaten by officiating priests, not to go outside the court; any vessel it touches must be cleaned (vv. 24-30)."
        ),
        "content": (
            "Leviticus 6 shifts registers: where chapters 1-5 addressed worshippers, chapters 6-7 (introduced here) turn to the priests. "
            "These are not public liturgical instructions but priestly manuals—the practical theology of what happens at the altar before dawn and after the congregation has gone home. "
            "The chapter reveals that worship requires constant, unseen faithfulness; the fire that the congregation saw blazing had been tended since the night before.\n\n"
            "**Extended Guilt Offering: Fraud Against a Neighbor (vv. 1-7)**\n\n"
            "The chapter opens with an important extension of the guilt offering to cover sins against neighbors: deceit, robbery, extortion, swearing falsely about a deposit or pledge. "
            "These are not ritual transgressions but social crimes—fraud, theft, exploitation. Yet they require the asham (guilt offering) plus full restitution plus a fifth. "
            "This is significant: God does not separate 'religious' from 'social' ethics. Cheating your neighbor is an offense against God (v. 2: 'commit a trespass against the LORD by deceiving his neighbor'). "
            "There is no category of sin against people that is religiously neutral. When Zacchaeus climbed down from his tree (Luke 19), he understood this.\n\n"
            "**The Fire That Must Never Go Out (vv. 8-13)**\n\n"
            "The priest's first duty each morning is the burnt offering: he removes the ashes from the previous night's fire, dresses in his linen garments, carries the ashes outside the camp, "
            "then returns to keep the fire burning. The chapter's refrain: 'Fire shall be kept burning on the altar continually; it shall not go out' (vv. 9, 12, 13—three times in six verses).\n\n"
            "This is not mere hygiene. The fire on the altar was lit by God Himself (Lev. 9:24). To let it go out would be to allow God's own act of acceptance to be extinguished through human negligence. "
            "The perpetual fire was a perpetual act of covenant faithfulness—the altar was always ready; God was always accessible; worship was never interrupted.\n\n"
            "The New Testament carries this image forward. The Spirit is described as fire (Acts 2:3-4); Paul commands: 'Do not quench the Spirit' (1 Thess. 5:19). "
            "The priestly responsibility—keep the fire burning, don't let it go out—becomes the responsibility of every believer: maintain the devotional flame through discipline, prayer, and community. "
            "Spiritual negligence lets fires go out.\n\n"
            "**The Priests' Grain Offering (vv. 14-23)**\n\n"
            "The grain offering for priests operated differently than the layperson's: the token portion went to the altar, but the priestly remainder was *fully burned*, not eaten. "
            "For the people, priests could eat the remainder; for the priests themselves, the grain offering was entirely consumed. "
            "Why? Because the priest is himself the servant of the altar—he cannot receive what he himself offers as his portion. "
            "This was the daily offering of Aaron and his sons: a tenth of an ephah of fine flour, half in the morning and half in the evening, cooked on a griddle with oil. "
            "The priest's worship was not something he performed for others only; it was his own daily consecration.\n\n"
            "Hebrews 7:27 draws an explicit contrast: the Levitical high priest had to offer sacrifices 'first for his own sins and then for those of the people.' "
            "Christ, 'holy, innocent, unstained, separated from sinners,' had no need of the daily priest-offering for Himself.\n\n"
            "**The Most Holy: Sin Offering Regulations (vv. 24-30)**\n\n"
            "The sin offering for the congregation was 'most holy' (קֹדֶשׁ קֳדָשִׁים, *qodesh qodashim*): it must be eaten in the court of the tabernacle by the officiating priest; "
            "it must not be carried outside the court; any clay vessel it touches must be broken; any bronze vessel must be scoured and rinsed; "
            "and if blood from a sin offering is brought into the inner sanctuary (as for the priest's own sin offering), it must be burned entirely and not eaten.\n\n"
            "This is the theology of holiness: sanctity is contagious (the vessel must be broken or purified), and handling holy things carelessly defiles rather than worships. "
            "The most holy offerings require the most careful stewardship. God's nearness is not a casual thing.\n\n"
            "**The Daily Pattern: Faithfulness Before Public Performance**\n\n"
            "Leviticus 6 teaches that the most important worship happens before the congregation arrives. "
            "The priest who cleaned the ash in linen garments before dawn, who kept the fire burning through the night watch, who ate the prescribed portion in the holy place—"
            "his faithfulness in the unseen made the visible worship possible. "
            "Jesus taught: 'When you pray, go into your room and close the door and pray to your Father in secret, and your Father who sees in secret will reward you' (Matt. 6:6). "
            "The perpetual fire of Leviticus 6 is the Old Testament equivalent: the altar of the heart is kept burning through hidden, daily faithfulness."
        ),
        "moral_lessons": [
            "Fraud and deception against a neighbor is described as a 'trespass against the LORD'—there is no social sin that is religiously neutral.",
            "The fire that must never go out calls the people of God to perpetual readiness for worship; spiritual negligence lets divine fires die.",
            "The priests' complete burning of their own grain offering teaches that those who serve others in worship must themselves be fully consecrated—serving is no substitute for personal devotion.",
            "The 'most holy' regulations for the sin offering teach that God's nearness is not casual; holiness requires careful, attentive, disciplined stewardship.",
            "The ash-removal at dawn—unglamorous, unseen priestly work—teaches that faithfulness in the mundane maintenance of worship is itself a holy calling.",
            "Restitution for fraud goes beyond returning what was taken—plus a fifth, plus the guilt offering—because genuine repentance restores dignity and trust, not merely property."
        ],
        "application": (
            "Leviticus 6 is a chapter about maintenance. The glory moments—fire from heaven, the congregation's gasps of awe—require the prior work of the ash-carrier at dawn. "
            "The spiritual life is no different: the public moments of joy, breakthrough, and grace are sustained by the hidden daily work of prayer, Scripture, and honest self-examination. "
            "The 'do not let the fire go out' command is the Old Testament version of Paul's 'do not quench the Spirit'—and both are addressed to people responsible for their own spiritual maintenance. "
            "The social fraud extension of the guilt offering also confronts the comfortable separation of business ethics from spiritual life: cheating customers, falsifying accounts, defrauding neighbors—"
            "all are categorized here as sins against God requiring sacrifice and restitution. "
            "Let your worship practice and your business practice be brought to the same altar."
        ),
        "prayer": (
            "Faithful God, forgive us for letting the fire go out through negligence and distraction. "
            "Rekindle in us the devotion that tends the altar before anyone is watching—the daily prayer, the careful Scripture reading, the honest self-examination. "
            "Where we have defrauded neighbors—in business, in relationships, in the small dishonesties of daily life—give us courage to make it fully right: to restore what was taken and add the fifth. "
            "May our worship never separate spiritual from social, ritual from ethical. "
            "Thank You for the High Priest who needed no daily sin offering for Himself but offered Himself once for all, the fire of whose sacrifice will never be extinguished. Amen."
        ),
        "key_points": [
            "Social fraud and deception are described as a 'trespass against the LORD'—sins against neighbors are simultaneously sins against God, requiring sacrifice and restitution.",
            "The perpetual altar fire—'it shall not go out' (three times in six verses)—was lit by God Himself (Lev. 9:24) and required daily priestly faithfulness to maintain.",
            "The priests' own grain offering was entirely consumed (unlike the layperson's)—those who serve others must themselves be fully consecrated, not just procedurally faithful.",
            "The 'most holy' designation for the sin offering required extraordinary care: vessels touched by it must be broken or scoured, and it must be eaten only within the sanctuary.",
            "Christ as High Priest needed no daily sin offering for Himself (Heb. 7:27)—His once-for-all sacrifice fulfilled what daily priestly offerings could only prefigure.",
            "The ash-removal at dawn models faithful, hidden worship: the unglamorous maintenance of holy things is itself a holy calling."
        ],
        "study_questions": [
            "Leviticus 6:2 calls deception and fraud against a neighbor a 'trespass against the LORD.' What does this tell us about the inseparability of social ethics and worship?",
            "The altar fire was lit by God (Lev. 9:24) and must never go out through priestly negligence. How does this picture of maintained devotion speak to Paul's command to 'not quench the Spirit' (1 Thess. 5:19)?",
            "The priests' daily grain offering was entirely burned—they could not eat any of it. What principle about priestly service and personal consecration does this establish?",
            "The 'most holy' regulations required that vessels touching the sin offering be broken or scoured. What does this intense care for holy things teach about how we should handle sacred practices and truths?",
            "Hebrews 7:27 contrasts the Levitical priests (who needed daily offerings for their own sins) with Christ (who did not). What does this contrast reveal about the superiority of Christ's priesthood?",
            "The chapter describes the ash-removal as a priestly responsibility done before dawn, in linen garments, without any audience. What does this teach about the role of unseen, unglamorous faithfulness in sustaining visible ministry?",
            "How does the guilt offering's coverage of business fraud (fraud, theft, extortion, false oaths about deposits) challenge you to bring your professional life fully under the authority of the same God you worship on Sunday?"
        ],
        "tags": ["perpetual fire", "guilt offering", "priest", "most holy", "altar", "Leviticus", "faithfulness", "worship", "fraud", "restitution"],
        "sources": [
            "Leviticus 6",
            "Leviticus 9:24",
            "Hebrews 7:27",
            "1 Thessalonians 5:19",
            "Acts 2:3-4",
            "Matthew 6:6",
            "Luke 19:8-9",
            "Exodus 29:38-42"
        ],
        "original_language_notes": [
            {
                "term": "קֹדֶשׁ קֳדָשִׁים (qodesh qodashim)",
                "language": "Hebrew",
                "verse": "6:25",
                "words_used": ["most holy", "holy of holies", "most holy thing"],
                "meaning": "Most holy, holy of holies. The superlative form in Hebrew uses reduplication: 'the holiness of holinesses.' The same construction names the inner sanctuary (the Holy of Holies). When applied to offerings, it designates things so intensely consecrated to God that they require special handling, can only be consumed in the court by officiating priests, and must not be taken outside. Holiness in Leviticus is not merely a moral quality but an ontological state—a zone of intense divine presence that affects whatever enters it."
            },
            {
                "term": "תָּמִיד (tamid)",
                "language": "Hebrew",
                "verse": "6:13",
                "words_used": ["continually", "regularly", "always", "perpetually"],
                "meaning": "Continually, regularly, perpetually—without interruption. Tamid describes things that are always ongoing, never suspended. The altar fire was tamid—always burning. The showbread (Lev. 24:8) was replaced tamid—every Sabbath without fail. The lamp in the tabernacle burned tamid (Exod. 27:20). Tamid worship was the Hebrew embodiment of uninterrupted covenantal fidelity: God's presence is constant, and human worship responds in kind. Jesus's high priestly intercession in Hebrews 7:25 is the New Testament tamid: 'He always lives to intercede for them.'"
            },
            {
                "term": "פָּשַׁע (pasha')",
                "language": "Hebrew",
                "verse": "6:2",
                "words_used": ["trespass", "rebel", "transgress"],
                "meaning": "To trespass, transgress, rebel, commit a breach of trust. Pasha' is stronger than ḥata' (to miss the mark); it implies a deliberate breach—crossing a known boundary. In Leviticus 6:2, the social crimes (fraud, deception, theft) are described as pasha' against the LORD, not merely against the neighbor. This is the prophetic insight that social injustice is fundamentally theological rebellion: Amos, Isaiah, and Micah all use the same root when denouncing exploitation of the poor as covenant transgression (Amos 1-2; Isa. 58:1-7; Mic. 3:8)."
            },
            {
                "term": "דֶּשֶׁן (deshen)",
                "language": "Hebrew",
                "verse": "6:10",
                "words_used": ["ashes", "fatness", "ash removal"],
                "meaning": "Ashes, residue of burned sacrifices; also 'fatness' (the richness left after burning). The deshen was the accumulated ash from previous burnt offerings, removed each morning by the priest in his full linen vestments and carried to a clean place outside the camp. Though unglamorous, this removal was a priestly duty requiring full liturgical dress—it was not less holy than the sacrifice itself. The same root appears in Psalm 20:3 where God 'remembers all your offerings and accepts your deshen,' suggesting that even the aftermath of worship is received by God."
            }
        ]
    }
]

def slugify(name):
    return name.lower().replace(" ", "-").replace("'", "")


def generate_commentary(conn, chapter_data):
    chapter_num = chapter_data["chapter"]
    entry_uuid = str(uuid.uuid4())

    cur = conn.cursor()
    # Check if already exists
    cur.execute("""
        SELECT id, content FROM commentary_entries
        WHERE collection_id=? AND book_id=? AND chapter=? AND language_code='en'
          AND reference_scope='chapter' AND deleted_at IS NULL
    """, (COLLECTION_ID, BOOK_ID, chapter_num))
    existing = cur.fetchone()
    if existing and existing[1] and len(existing[1]) > 100:
        print(f"SKIP: Leviticus {chapter_num} already exists (id={existing[0]})")
        return "skipped"

    key_points_json = json.dumps(chapter_data["key_points"])
    study_questions_json = json.dumps(chapter_data["study_questions"])
    tags_json = json.dumps(chapter_data["tags"])
    sources_json = json.dumps(chapter_data["sources"])
    original_language_notes_json = json.dumps(chapter_data["original_language_notes"])
    moral_lessons_json = json.dumps(chapter_data["moral_lessons"])

    cur.execute("""
        INSERT INTO commentary_entries (
            uuid, collection_id, book_id, chapter, verse_start, verse_end,
            reference_scope, title, summary, content, application, prayer,
            key_points, study_questions, language_code, theological_perspective,
            status, is_ai_generated, created_at, updated_at
        ) VALUES (?, ?, ?, ?, NULL, NULL, 'chapter', ?, ?, ?, ?, ?, ?, ?, 'en', 'evangelical', 'draft', 1, ?, ?)
    """, (
        entry_uuid, COLLECTION_ID, BOOK_ID, chapter_num,
        chapter_data["title"],
        chapter_data["summary"],
        chapter_data["content"],
        chapter_data["application"],
        chapter_data["prayer"],
        key_points_json,
        study_questions_json,
        now_str, now_str
    ))
    conn.commit()

    # Build JSON for file (no forbidden keys)
    json_data = {
        "uuid": entry_uuid,
        "collection_name": COLLECTION_NAME,
        "author_type": "ai",
        "language_code": "en",
        "theological_perspective": "evangelical",
        "status": "draft",
        "book_id": BOOK_ID,
        "book": BOOK_NAME,
        "chapter": chapter_num,
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
        "sources": chapter_data["sources"],
        "created_at": now_str,
        "updated_at": now_str
    }

    # Verify no forbidden keys
    forbidden = {"is_ai_generated", "model_name", "prompt_version"}
    for key in forbidden:
        assert key not in json_data, f"Forbidden key found: {key}"

    # Write JSON backup
    book_dir = os.path.join(GENERATED_DIR, f"{BOOK_ID:02d}-{BOOK_SLUG}")
    os.makedirs(book_dir, exist_ok=True)
    json_path = os.path.join(book_dir, f"{chapter_num:02d}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    # Verify round-trip
    with open(json_path, "r", encoding="utf-8") as f:
        parsed = json.load(f)
    for key in forbidden:
        assert key not in parsed, f"Forbidden key in saved file: {key}"

    print(f"GENERATED: Leviticus {chapter_num} — {chapter_data['title']}")
    return "generated"


def main():
    conn = sqlite3.connect(DB_PATH)

    generated = 0
    skipped = 0
    files_written = []

    batch_uuid = str(uuid.uuid4())
    start_ref = f"Leviticus 2"
    end_ref = f"Leviticus 6"

    for ch_data in CHAPTERS:
        result = generate_commentary(conn, ch_data)
        ch_num = ch_data["chapter"]
        if result == "generated":
            generated += 1
            files_written.append(f"generated/03-leviticus/{ch_num:02d}.json")
            end_ref = f"Leviticus {ch_num}"
        else:
            skipped += 1
            end_ref = f"Leviticus {ch_num}"

    # Update progress
    last_ch = CHAPTERS[-1]["chapter"]
    progress = {
        "next_book_id": 3,
        "next_book": "Leviticus",
        "next_chapter": last_ch + 1,
        "last_completed_book_id": 3,
        "last_completed_book": "Leviticus",
        "last_completed_chapter": last_ch,
        "completed": False,
        "updated_at": now_str
    }
    with open(PROGRESS_JSON, "w") as f:
        json.dump(progress, f, indent=2)

    # Update DB progress
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='commentary_generation_progress'")
    if cur.fetchone()[0] > 0:
        cur.execute("DELETE FROM commentary_generation_progress")
        cur.execute("""
            INSERT INTO commentary_generation_progress
            (next_book_id, next_book, next_chapter, last_completed_book_id, last_completed_book, last_completed_chapter, completed, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (3, "Leviticus", last_ch + 1, 3, "Leviticus", last_ch, 0, now_str))
        conn.commit()

    # Append log
    log_entry = {
        "timestamp": now_str,
        "generation_batch_id": batch_uuid,
        "start_reference": start_ref,
        "end_reference": end_ref,
        "chapters_generated": generated,
        "chapters_skipped": skipped,
        "db_rows_inserted": generated,
        "files_written": files_written
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    conn.close()

    print(f"\n=== SUMMARY ===")
    print(f"Generated: {generated}, Skipped: {skipped}")
    print(f"Files: {files_written}")
    print(f"DB rows inserted: {generated}")
    print(f"Next starting reference: Leviticus {last_ch + 1}")


if __name__ == "__main__":
    main()
