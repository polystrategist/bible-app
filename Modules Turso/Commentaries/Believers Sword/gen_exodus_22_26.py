"""Generate Exodus 22-26 commentaries and save to DB + JSON."""

import sqlite3
import json
import uuid
import os
from datetime import datetime, timezone

DB_PATH = "believers_sword_commentaries.db"
GENERATED_DIR = "generated/02-exodus"
COLLECTION_ID = 1
BOOK_ID = 2
BOOK_NAME = "Exodus"
LANGUAGE_CODE = "en"
THEOLOGICAL_PERSPECTIVE = "Evangelical Christian"
AUTHOR_TYPE = "organization"
COLLECTION_NAME = "Believers Sword Commentaries"

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

COMMENTARIES = [
    {
        "chapter": 22,
        "title": "Exodus 22 — Justice, Restitution, and the Protection of the Vulnerable",
        "summary": "Exodus 22 continues the Book of the Covenant with specific case laws governing theft and property damage, social obligations, sexual ethics, treatment of foreigners and the poor, and the prohibition of sorcery and false worship. The chapter's recurring refrain is God's concern for the vulnerable — widow, orphan, poor, and stranger — grounded not in abstract ethics but in Israel's own experience: 'You were strangers in Egypt.' God's character as compassionate and just is the foundation and motive for Israel's social obligations.",
        "content": """## What Exodus 22 Is About
Exodus 22 is the middle section of the Book of the Covenant (Exodus 21-23), continuing to apply Decalogue principles through specific case laws. The chapter covers three broad areas: property and restitution law, sexual and religious ethics, and social obligations to the vulnerable.

**Theft and Property Laws (vv.1-15)**: The chapter opens with laws about stolen animals, with graduated restitution based on circumstances. If a thief steals an ox or sheep and slaughters or sells it, the restitution is fivefold for an ox and fourfold for a sheep (the ox being more economically valuable). If the thief is caught and cannot pay, he may be sold into servitude. Killing a thief in darkness (nighttime) carries no blood guilt for the homeowner, but killing a thief in daylight does — presumably because in daylight there were other options. Grazing rights, fire damage, and borrowed or leased property all carry specific liability rules reflecting the economic realities of agrarian life.

**Sexual and Religious Ethics (vv.16-20)**: Seducing an unbetrothed virgin requires either marriage or paying the bride price. The passage signals the gravity of sexual behavior in community life. Three commands follow with capital penalties: sorcery (v.18), bestiality (v.19), and idolatry (v.20) — reflecting the absolute seriousness with which Israel was to treat loyalty to God and the integrity of creation's boundaries.

**Social Obligations to the Vulnerable (vv.21-27)**: The most emotionally charged section of the chapter. Foreigners must not be mistreated — "for you were strangers in Egypt." Widows and orphans must not be exploited; their cry reaches directly to God, who will respond with a fierce anger that makes the exploiter's wife a widow and children orphaned. The poor must receive loans without interest. Garments taken as pledges must be returned by nightfall because the poor man has nothing else to sleep in — and God says, "When he cries to me, I will hear, for I am compassionate."

**Obligations to God (vv.28-31)**: The chapter closes with commands to honor God in firstfruits and firstborn offerings, not to delay, and to avoid eating meat torn by wild animals. These ritual purity commands maintain the distinction between Israel as a holy people set apart to God.

## Theological Themes
- **Restitution, Not Mere Punishment**: The property laws emphasize restoration more than punishment. The goal of the legal system is to restore what was lost, not simply to penalize. This reflects a relational understanding of justice — wrongdoing damages community bonds that must be repaired.
- **God as Advocate of the Poor**: The direct connection between the cries of widows, orphans, and the poor to God's personal anger is striking. God is not a distant lawgiver but a living advocate for the oppressed. When Israel refuses this responsibility, they are not merely breaking a rule — they are grieving their God.
- **Memory as Moral Motivation**: "You shall not wrong a sojourner... for you were sojourners in the land of Egypt" (v.21). Israel's own story of suffering becomes the ethical foundation for how they treat others. Empathy rooted in shared experience is one of the Bible's primary ethical engines.
- **The Holiness of Boundaries**: The capital offenses in vv.18-20 (sorcery, bestiality, idolatry) are not arbitrary taboos. Each violates a fundamental order: sorcery violates the boundary between human and spiritual authority (seeking power through forbidden channels), bestiality violates the human-animal boundary embedded in creation, idolatry violates the covenant between Israel and God. Maintaining these boundaries protects Israel's identity as a holy people.

## Hebrew Word Notes
- **שַׁלֵּם** (shallēm, "he shall make restitution/make whole," e.g., vv.1,3,4,5,6,7,9,11,12) — From shālem, the root of "shalom." Restitution is not merely paying a fine — it is restoring shalom, completeness, to the community. Justice in the Hebrew mind is not punishment for its own sake but the restoration of wholeness.
- **גֵּר** (gēr, "sojourner/stranger," v.21) — A resident alien, neither native nor full citizen. The gēr had no kinship network to protect them, making them vulnerable. The Torah's consistent concern for the gēr (occurring 36 times in the Pentateuch) reflects God's heart for those without structural protection. This category eventually becomes a model for how Christians understand their status in this world (1 Pet. 2:11).
- **חַנּוּן** (ḥannûn, "compassionate," v.27) — An adjective from ḥānan (to be gracious, to show favor). God's statement "I am compassionate" (kî-ḥannûn ʾānî) is a rare divine self-description in the law code, embedding God's character directly into the legal framework. Justice is not cold procedure — it flows from a compassionate God.

## How This Chapter Points to Christ
Jesus explicitly quotes the spirit of this chapter in His teaching. The command to love the stranger (v.21) is the background for the Good Samaritan (Luke 10:25-37), where Jesus expands "neighbor" beyond ethnic and religious lines. The poor widow's prayer reaching God (vv.22-24) is echoed in Jesus's parable of the persistent widow (Luke 18:1-8) — both insist that God hears the cry of the oppressed and will act. Christ Himself is the ultimate fulfillment of the "firstborn" principle (v.29-30): as the Father's firstborn (Col. 1:15), He was given unreservedly, so that all who believe might be redeemed.

## Moral and Spiritual Lessons
- The story of suffering must shape our treatment of others. When we remember what it felt like to be the stranger, the poor, the powerless, it becomes impossible to exploit others in those positions.
- God takes the exploitation of the vulnerable personally. It is not a legal technicality but a matter that provokes His anger and invites His judgment.
- Restitution is better theology than mere punishment. Where possible, seek to restore what was broken in relationships, communities, and material losses.
- The God of justice is also "compassionate" (ḥannûn). These are not competing attributes — they are unified in a God who cares enough about people to be angry at their exploitation and gracious enough to hear their cries.

## Practical Application
Take an inventory of the "sojourners" in your life — those who are structurally vulnerable, new to your community, without kinship networks to protect them. How are they treated? Are you actively extending protection and welcome, or are you passive while exploitation occurs? The command to Israel was not "do not oppress if it's convenient" — it was an unqualified obligation rooted in who God is and what He has done for you.

## Believers Sword Reflection
Exodus 22 is a remarkable social ethics document for its ancient context. It embeds economic protections for the poor, due process in property disputes, anti-exploitation obligations for foreigners, and a humanitarian limit on loan collateral (returning garments by nightfall). The motivation throughout is neither utilitarian nor contractual — it is rooted in God's character and Israel's story. Christian social ethics finds its roots here, not in secular political philosophy.""",
        "chapter_overview": "Exodus 22 continues the Book of the Covenant with laws on theft and restitution (graduated by circumstance), sexual and religious ethics (sorcery, bestiality, idolatry all capital offenses), and social obligations to foreigners, widows, orphans, and the poor. The chapter's refrain is God's fierce advocacy for the vulnerable: when the exploited cry out, God hears and responds.",
        "original_language_notes": [
            {
                "term": "shallēm",
                "language": "Hebrew",
                "verse": "Exodus 22:1",
                "words_used": "שַׁלֵּם (shallēm) — 'he shall make restitution/restore'",
                "meaning": "From shālem, root of shalom (peace/wholeness). Restitution in Hebrew law is not mere punitive payment — it is the restoration of shalom to the injured party and the community. The goal of justice is wholeness, not merely penalty."
            },
            {
                "term": "gēr",
                "language": "Hebrew",
                "verse": "Exodus 22:21",
                "words_used": "גֵּר (gēr) — 'sojourner, resident alien, stranger'",
                "meaning": "A non-Israelite living among the people, without kinship network or legal standing as a native. The Torah's 36 commands about the gēr reflect God's structural concern for those without protective community. Peter applies this to Christians in the world (1 Pet. 2:11)."
            },
            {
                "term": "ḥannûn",
                "language": "Hebrew",
                "verse": "Exodus 22:27",
                "words_used": "חַנּוּן (ḥannûn) — 'compassionate, gracious'",
                "meaning": "From ḥānan (to show favor, to be gracious). God's self-declaration 'I am compassionate' (kî-ḥannûn ʾānî) embeds divine character directly into the legal code — justice is not cold procedure but the expression of a God who cares personally about the oppressed."
            },
            {
                "term": "yāʿaq",
                "language": "Hebrew",
                "verse": "Exodus 22:22-23",
                "words_used": "צָעַק (tsāʿaq) — 'to cry out, to call for help'",
                "meaning": "The same verb used of Israel's cry in Egypt (Exod. 2:23). When widows and orphans tsāʿaq, God hears — the same way He heard Israel's suffering. God's response to the oppressed is not theoretical but experiential, grounded in His own history of hearing and acting."
            }
        ],
        "moral_lessons": [
            "Our own history of vulnerability must shape our treatment of the vulnerable — the experience of being a stranger, poor, or powerless is a moral formation tool.",
            "God is personally angered by the exploitation of widows, orphans, and foreigners — this is not a legal technicality but a matter of His heart.",
            "Restitution aims at restoring wholeness (shalom), not merely satisfying legal debt — the goal of justice is community repair.",
            "Charging interest on loans to the poor is not a neutral financial transaction but an act of exploitation that God prohibits.",
            "Compassion and justice are unified in God's character — His anger at exploitation flows from the same heart that hears the cry of the oppressed."
        ],
        "application": "Identify the structurally vulnerable in your context — immigrants, widows, orphans, the economically marginalized. Ask whether your church, workplace, and personal life exhibit the active protection this passage requires, not merely the avoidance of direct harm. The command is not passive ('don't oppress') but active ('you shall not wrong them') — an ongoing vigilance rooted in memory of your own need for God's grace.",
        "prayer": "Compassionate God, You hear the cry of the widow and orphan and the stranger. You were moved on our behalf when we cried out from Egypt, and You are moved now when the vulnerable cry. Forgive us when we have exploited or ignored those without protection. Give us Your own compassion for the marginalized, and the courage to extend justice and welcome where You call us to. In Christ, who is Himself the refuge of the poor and the hope of the stranger. Amen.",
        "key_points": [
            "Theft and property damage require restitution — graduated by circumstance and aimed at restoring wholeness (shalom), not merely punishing.",
            "Sorcery, bestiality, and idolatry are capital offenses — each violates a fundamental boundary: spiritual authority, the human-animal distinction, and covenant loyalty to God.",
            "The prohibition on wronging sojourners is grounded in Israel's own experience: 'you were strangers in Egypt.'",
            "God is personally fierce in His defense of widows and orphans — their cry reaches Him directly and provokes His anger against exploiters.",
            "Loans to the poor must carry no interest; garments taken as pledge must be returned by nightfall because the poor man has nothing else to sleep in.",
            "God's self-description as 'compassionate' (ḥannûn) is the theological foundation for all these social laws.",
            "Firstfruits and firstborn obligations remind Israel that all they have comes from God and is to be offered back to Him first."
        ],
        "study_questions": [
            "The restitution laws require more than simple repayment — sometimes double, fourfold, or fivefold (vv.1-4). What does this suggest about how God views justice beyond merely returning what was taken?",
            "God ties His protection of the sojourner to Israel's memory of being sojourners in Egypt (v.21). How does your own story of need or vulnerability shape your treatment of vulnerable people in your life?",
            "God says 'I am compassionate' (v.27) in the context of a legal code. What does it tell us about God's character that He cannot separate justice from personal compassion?",
            "The laws against sorcery, bestiality, and idolatry protect what kinds of boundaries? Why do you think violating these particular boundaries merits such severe consequences?",
            "How does the principle of interest-free loans to the poor challenge how you think about money, generosity, and community in your context today?"
        ],
        "tags": [
            "exodus", "book-of-covenant", "restitution", "justice", "vulnerable", "widows-orphans",
            "sojourners", "property-law", "compassion", "social-ethics", "sorcery", "idolatry"
        ],
        "sources": []
    },
    {
        "chapter": 23,
        "title": "Exodus 23 — Justice, Sabbath, Feasts, and the Promise of God's Guiding Angel",
        "summary": "Exodus 23 completes the Book of the Covenant with commands on truthful testimony and impartial justice, Sabbath and land rest, three annual pilgrimage feasts (Unleavened Bread, Harvest/Weeks, Ingathering/Tabernacles), and a closing divine promise: God will send His angel to guide Israel into Canaan. Israel must not bow to foreign gods or make covenants with Canaanite peoples. Obedience is rewarded with God's blessing on food, water, health, fertility, and territorial victory. The chapter is the capstone of the Book of the Covenant — linking law to worship, worship to rest, and rest to trust in God's provision.",
        "content": """## What Exodus 23 Is About
Exodus 23 is the closing chapter of the Book of the Covenant (Exodus 21-23), completing the legal code that applies the Ten Commandments to Israel's communal life. The chapter falls into four natural sections: justice in the courts, Sabbath and land rest, pilgrimage feasts, and divine promises for the journey into Canaan.

**Justice in the Courts (vv.1-9)**: These laws concern truthful testimony and impartial judgment. Israel must not spread false reports, join a crowd to pervert justice, favor a poor man simply because he is poor (a surprisingly counter-cultural command — the poor receive no bias, only equal treatment), or pervert justice against the poor. Remarkably, the code commands helping an enemy's lost animal, even returning it to him (vv.4-5). Enemy kindness in the law predates and undergirds Jesus's command to love enemies (Matt. 5:44). Bribery corrupts perception and perverts the outcome of even good cases (v.8). The sojourner must receive justice — "for you were sojourners" (v.9).

**Sabbath and Land Rest (vv.10-13)**: The Sabbath principle extends from the weekly day (the fourth commandment) outward in two directions: to a seventh-year rest for the land (the Sabbatical Year), when cultivated land is left fallow and its produce given to the poor and wild animals. This is a radical economic faith — trusting God to provide through a year of deliberate non-production. The weekly Sabbath (v.12) is tied to the rest of servant, ox, donkey, and sojourner — not merely a religious observance but a systemic rest for the entire working community. The command to "be careful to do all I have told you" and "not mention other gods" (v.13) frames these obligations within covenant exclusivity.

**Three Annual Feasts (vv.14-17)**: All adult males are required to appear before God three times a year, each time bringing an offering and not coming empty-handed:
1. **Feast of Unleavened Bread** (seven days in the month of Abib) — commemorating the Exodus, when Israel left Egypt in haste. No leavened bread; the blood of offerings must not be left with leavened bread; the Passover offering must not be left until morning.
2. **Feast of Harvest/Firstfruits (Weeks/Pentecost)** — celebrating the first fruits of what was sown in the field.
3. **Feast of Ingathering (Tabernacles)** — at the end of the agricultural year, celebrating the full harvest.

These feasts structure Israel's calendar around God's provision rather than agricultural seasons alone. They are acts of public worship, national memory, and economic theology — acknowledging that God, not their labor alone, produces the harvest.

**Promise of the Angel and Instructions for Conquest (vv.20-33)**: God promises to send His angel before Israel to guard them and bring them to the promised land. Israel must obey the angel, for God's name is in him — indicating not a created messenger but a divine presence. God will fight for them gradually ("little by little," v.30) so the land does not become desolate. But Israel must make no covenant with Canaanite peoples, must not let them live in the land (due to the corruption of their worship), and must demolish their sacred stones and pillars. The warning is explicit: "if you serve their gods, it will certainly be a snare to you" (v.33) — a warning Israel would tragically fulfill.

## Theological Themes
- **Justice Without Favoritism**: The command not to favor the poor in a lawsuit (v.3) is as important as the command not to favor the powerful. True justice is blind to socioeconomic status — it evaluates the case. This does not eliminate special concern for the poor in other contexts, but in legal settings the standard is absolute impartiality.
- **The Sabbath as Systemic Justice**: The Sabbath year and weekly Sabbath are not merely spiritual practices — they are economic justice mechanisms. The land rest redistributes its produce to the poor; the day of rest gives relief to servants, animals, and sojourners. Sabbath is built into creation as a recurring reset of exploitative tendencies.
- **Feasts as Covenant Memory**: The three feasts orient Israel's annual rhythm around God's saving acts (Exodus, harvest provision, wilderness ingathering). They prevent the natural human tendency to forget God when prosperity arrives. Each feast is a corporate act of remembering, thanking, and re-centering on the covenant.
- **Gradual Conquest as Providence**: God's promise to drive out enemies "little by little" (v.30) shows divine wisdom — rapid victory without sufficient population to fill the land would create ecological collapse ("the land become desolate and the wild animals multiply against you"). Providence moves at the pace of readiness, not at the pace of impatience.

## Hebrew Word Notes
- **שָׁקֶר** (shāqer, "falsehood/lie," v.1) — A false report, slander, groundless accusation. The law against spreading shāqer reflects the Bible's consistent concern that words have power to destroy — false testimony in court, in community, or in reputation can ruin lives irreversibly. God's own character is truth (ʾemet), and His people must reflect that.
- **שֹׁמֵר** (shōmēr, "guardian/keeper," v.20) — God says He is sending an angel to "guard" Israel (shāmar = to keep, watch over, protect). This word appears throughout the Psalms as a description of God's own protective activity (Ps. 121:4-8). The angel who guards Israel bears God's own guardian activity.
- **שָׁחַד** (shōḥad, "bribe," v.8) — A bribe "blinds the clear-sighted and corrupts the words of the righteous." Shōḥad does not merely tempt corruption — it distorts perception, making even intelligent and otherwise honest people unable to see clearly. This is a profound insight into the psychology of corruption.
- **מְעַט מְעַט** (meʿat meʿat, "little by little," v.30) — The gradual pace of conquest is explicitly described. Divine wisdom operates through sustainable pace rather than overwhelming force that creates instability. This principle has wide application: transformation — spiritual, social, or physical — is often most durable when it progresses incrementally.

## How This Chapter Points to Christ
The angel in whom God's "name" dwells (v.21) is understood by many church fathers and commentators as a pre-incarnate appearance or representation of Christ — the divine Word who bears the Father's full authority and presence (cf. John 1:1; Rev. 22:16). The three feasts point forward: Unleavened Bread is fulfilled in Christ's sinless sacrifice and resurrection (1 Cor. 5:7-8); Firstfruits is fulfilled in Christ's resurrection as the firstfruits of the dead (1 Cor. 15:20-23); Ingathering/Tabernacles points to the final eschatological harvest and the consummation of all things (Rev. 14:15-16). The command not to come empty-handed before God (v.15) finds its ultimate fulfillment: Christ presents us to the Father complete and clothed in His righteousness (Col. 2:10).

## Moral and Spiritual Lessons
- Impartial justice applies even toward enemies. Help your enemy's animal return to him (vv.4-5). True righteousness does not stop at the boundary of personal relationships.
- Bribery does not merely tempt — it blinds. Acknowledge the distorting power that personal gain, social pressure, and self-interest can have on your perception of what is right.
- Rest is an act of trust in God as provider. The Sabbath year's fallow agriculture is an annual declaration that God, not Israel's labor, sustains them. Rest is not laziness — it is faith in action.
- God's timing is providential, not merely slow. "Little by little" reflects divine wisdom about readiness and sustainability, not reluctance to act.

## Practical Application
Examine your relationship to truthfulness in community contexts. The law against joining a crowd to pervert justice (v.2) applies to social media pile-ons, workplace gossip, and group consensus that goes along with false narratives. Train yourself to evaluate what is actually true rather than what the prevailing group voice demands. And practice Sabbath not merely as a spiritual discipline but as a trust-act: one day of genuine rest as a declaration that God holds what you cannot hold by working more.

## Believers Sword Reflection
Exodus 23 closes the Book of the Covenant with a comprehensive vision: justice in every human relationship (courts, enemies, sojourners), rest woven into weekly, annual, and seven-year cycles, worship structured around divine provision and historical memory, and the promise of divine presence leading forward. This is not merely law — it is a theology of life ordered around the character of God.""",
        "chapter_overview": "Exodus 23 completes the Book of the Covenant with commands on truthful and impartial justice, help for an enemy's animal, Sabbath rest for land and people, three annual pilgrimage feasts (Unleavened Bread, Harvest/Weeks, Ingathering), and a closing divine promise: God's angel will guide Israel into Canaan, fighting for them — but they must make no covenant with Canaanite peoples or their worship will become a fatal snare.",
        "original_language_notes": [
            {
                "term": "shāqer",
                "language": "Hebrew",
                "verse": "Exodus 23:1",
                "words_used": "שָׁקֶר (shāqer) — 'falsehood, false report, lie'",
                "meaning": "Spreading a false report (shēmaʿ shāw) — false testimony that has social and legal consequences. Words in the Hebrew worldview are not neutral — they create realities. God, whose character is ʾemet (truth), requires His people to mirror that truthfulness in community speech and testimony."
            },
            {
                "term": "shōḥad",
                "language": "Hebrew",
                "verse": "Exodus 23:8",
                "words_used": "שֹׁחַד (shōḥad) — 'bribe'",
                "meaning": "A bribe 'blinds the eyes of the clear-sighted (piqqēḥîm) and corrupts the words of the righteous.' The word piqqēḥîm means those who can see clearly — implying that bribery blinds even sharp-eyed people. Corruption distorts perception, not just behavior."
            },
            {
                "term": "shāmar",
                "language": "Hebrew",
                "verse": "Exodus 23:20",
                "words_used": "שָׁמַר (shāmar) — 'to guard, keep, watch over'",
                "meaning": "The angel God sends will shāmar (guard) Israel on the way. This is the same word used throughout Psalms of God's own protective activity over His people (Ps. 121:4-8: 'He who keeps Israel will neither slumber nor sleep'). The angel bears God's guardian function."
            },
            {
                "term": "meʿat meʿat",
                "language": "Hebrew",
                "verse": "Exodus 23:30",
                "words_used": "מְעַט מְעַט (meʿat meʿat) — 'little by little'",
                "meaning": "The deliberate, gradual pace of conquest — explicitly motivated by ecological sustainability ('lest the land become desolate and wild animals multiply'). Divine wisdom often works incrementally to ensure that what is gained is sustainable. A profound principle beyond military conquest."
            }
        ],
        "moral_lessons": [
            "Impartial justice requires extending fair treatment even to enemies — helping an enemy's lost animal (vv.4-5) prefigures Jesus's command to love enemies.",
            "Bribery blinds even clear-sighted people — acknowledge the distorting power of personal gain and social pressure on your perception of what is true.",
            "Sabbath rest is an act of faith and trust in God as the real provider — ceasing work declares that God holds what you cannot hold by working more.",
            "The annual feasts prevent the human tendency to forget God in prosperity — structured remembrance is a spiritual discipline, not optional.",
            "God's timing ('little by little') reflects wisdom about sustainable readiness, not reluctance — trust His pace, not only His power."
        ],
        "application": "Practice truthfulness in community contexts where group pressure pulls toward false narratives. The command against joining a crowd to pervert justice (v.2) applies to social conformity, gossip, and pile-on criticism. Evaluate what is actually true rather than what the prevailing voice demands. Additionally, practice Sabbath as a weekly trust-act — one day of genuine rest as a declaration that your life is held by God, not by your productivity.",
        "prayer": "God of truth and rest, You have commanded Your people to walk in justice, to tell the truth even when costly, to extend kindness even to enemies, and to cease from labor as an act of trust. Forgive us when we have joined crowds that spread falsehood, when we have been blinded by self-interest, and when we have worked without resting as though You were not our provider. Give us the courage to stand for truth alone, the faith to rest in You, and the worship that orders our whole year around Your provision. In Christ, who is the truth and our Sabbath rest. Amen.",
        "key_points": [
            "False testimony and joining a crowd to pervert justice are prohibited — truth in community speech is non-negotiable.",
            "Enemy kindness is commanded: return your enemy's lost animal, demonstrating that covenant righteousness extends beyond personal relationships.",
            "Bribery blinds even the clear-sighted — corruption distorts perception, not just behavior.",
            "The Sabbatical Year (every seventh year, land fallow and produce for the poor) applies the Sabbath principle to economic and ecological systems.",
            "Three annual feasts — Unleavened Bread, Harvest/Weeks, Ingathering — structure Israel's calendar around divine provision and historical memory.",
            "God's angel with His 'name' in him will guard and guide Israel — obedience to this angel is obedience to God.",
            "Conquest will be 'little by little' — God's pace reflects providential wisdom about what Israel can sustain, not reluctance to act."
        ],
        "study_questions": [
            "The command not to favor the poor in a lawsuit (v.3) seems to contradict special concern for the poor elsewhere. How do you reconcile impartial justice in legal settings with compassion for the poor in social settings?",
            "Helping your enemy's lost animal (vv.4-5) is a striking command. How does this anticipate Jesus's teaching on loving enemies (Matt. 5:44)? What does it cost to obey this kind of law?",
            "The Sabbath year (fallow land, produce for the poor) required radical economic trust in God. What would an equivalent act of trusting rest look like in your economic or vocational life?",
            "The three annual feasts were structured acts of national remembrance and worship. What practices in your life systematically remind you of what God has done so you don't forget in seasons of prosperity?",
            "God says He will drive out enemies 'little by little' (v.30) because rapid victory would be unsustainable. Where in your spiritual growth or life circumstances do you see God working gradually, and how do you make peace with His pace?"
        ],
        "tags": [
            "exodus", "book-of-covenant", "justice", "sabbath", "feasts", "sabbatical-year",
            "enemy-kindness", "truth", "pilgrimage", "angel", "conquest", "unleavened-bread", "tabernacles"
        ],
        "sources": []
    },
    {
        "chapter": 24,
        "title": "Exodus 24 — The Covenant Ratified: Blood, Meal, and Moses on the Mountain",
        "summary": "Exodus 24 records the solemn ratification of the Sinai Covenant, one of the most dramatic scenes in the entire Bible. Moses reads the Book of the Covenant to the people; they respond twice with 'All that the LORD has spoken we will do and we will be obedient.' Moses throws half the covenant blood on the altar and half on the people, declaring: 'Behold the blood of the covenant.' Moses, Aaron, Nadab, Abihu, and seventy elders then ascend the mountain and see the God of Israel — eating and drinking in His presence in a covenant meal without dying. Moses then ascends further to receive the stone tablets, remaining on the mountain forty days and nights.",
        "content": """## What Exodus 24 Is About
Exodus 24 is the covenant ratification chapter — the moment when the legal framework of Exodus 19-23 is formally sealed between God and Israel. The chapter moves through several distinct stages, each with its own theological weight.

**The Command to Ascend (vv.1-2)**: God summons Moses, Aaron, Nadab, Abihu, and seventy elders to worship from afar. Moses alone is to come near to God. This distinction between proximity to God — Moses at the top, elders midway, people at the base — reflects degrees of holiness and mediatorial calling that will be further developed in the priesthood and tabernacle.

**The Reading and the People's Response (vv.3-4)**: Moses descends to the camp and tells the people everything God has said. The people respond: "All the words which the LORD has spoken we will do" (v.3). Moses writes all the words of the LORD and rises early to build an altar at the foot of the mountain with twelve pillars representing the twelve tribes — covenant obligations are physically anchored in Israel's tribal identity.

**The Blood Ritual (vv.5-8)**: Young men offer burnt offerings and peace offerings. Moses takes half the blood and throws it against the altar; he reads the Book of the Covenant aloud again, the people respond a second time — "All that the LORD has spoken we will do, and we will be obedient" (v.7) — and then Moses throws the other half of the blood on the people: "Behold the blood of the covenant that the LORD has made with you in accordance with all these words" (v.8). Blood unites the parties to the covenant — God's side (the altar) and the people's side — in a binding mutual commitment whose violation means death.

**The Vision and the Covenant Meal (vv.9-11)**: The seventy elders, Moses, Aaron, Nadab, and Abihu ascend and "see the God of Israel" (v.10). The description is unique and careful: "under his feet there was something like a pavement of sapphire stone, like the very heaven for clearness." They do not see God's face directly — but they see enough to know they are in the presence of transcendent holiness. And they eat and drink. This is a covenant meal, a shared table in the presence of God, sealing the relationship not only with blood but with fellowship. That "God did not lay his hand on the chief men of the people of Israel" (v.11) emphasizes the extraordinary grace of their survival.

**Moses Ascends for Forty Days (vv.12-18)**: God calls Moses to come up further to receive "the tablets of stone, with the law and the commandment, which I have written for their instruction." The cloud covering the mountain in the sight of the people of Israel for six days, with the glory of the LORD appearing like a devouring fire, creates a border between human and divine space. Moses enters the cloud and remains forty days and forty nights — the time of deep formation: writing, learning, receiving the plans for the tabernacle.

## Theological Themes
- **Covenant Ratification by Blood**: "The blood of the covenant" (v.8) is one of the most important phrases in the entire Hebrew Bible. Covenants in the ancient Near East were often sealed by blood — the death of an animal represented the death that would come to any party who violated the covenant. Israel's covenant with God is not a casual agreement but a blood-sealed commitment. Jesus quotes this phrase at the Last Supper: "This is my blood of the covenant, which is poured out for many" (Matt. 26:28) — explicitly connecting Sinai's blood to His own.
- **Gradations of Nearness to God**: The ascent structure — people at the base, elders midway, Moses at the summit — previews the tabernacle's architectural theology. The outer court is for all Israel; the Holy Place for priests; the Holy of Holies for the high priest alone, once a year. Nearness to God is structured by holiness, mediation, and God's own permission.
- **Eating in God's Presence**: The covenant meal on the mountain (vv.9-11) is a radical act of fellowship. To eat and drink in the presence of God and live is grace upon grace. The imagery echoes forward to the Passover, the Lord's Supper, and the Marriage Supper of the Lamb (Rev. 19:9) — covenant sealed at table.
- **Forty Days of Formation**: Moses's forty days on the mountain is the first of several forty-day/forty-year periods of divine formation in the Bible (Elijah's forty days at Horeb, 1 Kings 19; Jesus's forty days in the wilderness, Matt. 4). The number signals a complete period of testing, formation, and preparation.

## Hebrew Word Notes
- **בְּרִית** (berît, "covenant," v.7-8) — The central word of this entire section. A berît is not merely a contract but a binding, solemn relationship commitment, often sealed by blood, oaths, or shared meals. The phrase "dam habberît" — "blood of the covenant" — is unique in the Hebrew Bible here at Sinai and re-appears only on Jesus's lips at the Last Supper.
- **נַעֲשֶׂה וְנִשְׁמָע** (naʿăśeh venishmaʿ, "we will do and we will be obedient/hear," v.7) — The people make a commitment to do and then hear. In Jewish tradition, this phrase "we will do and we will hear" is celebrated as extraordinary faith — committing to obey before fully understanding. Some rabbinic interpreters say this earned Israel a special divine honor. It is ultimately only fulfilled in Christ, who obeyed completely.
- **כְּבוֹד יהוה** (kevôd Yahweh, "the glory of the LORD," v.17) — The divine glory appeared like a devouring fire (ʾēsh ʾōkelet) on the top of the mountain. Kāvôd (glory) has the root meaning of "weight/heaviness" — the manifest presence of God is not light and airy but weighty, consuming, and overwhelming. This is the same glory that will fill the tabernacle (Exod. 40:34-35) and the temple (1 Kings 8:11), and ultimately dwell in Christ (John 1:14).
- **סַפִּיר** (sappîr, "sapphire," v.10) — The description of what is beneath God's feet as sapphire stone, "like the very heaven for clearness," is one of the few visual descriptions of the divine environment in the Hebrew Bible. Sapphire appears again in Ezekiel's vision of the divine throne (Ezek. 1:26) and in Revelation's New Jerusalem (Rev. 21:19). It signals transcendent purity and clarity — a sky-like heaven underfoot.

## How This Chapter Points to Christ
The Hebrews letter makes the connection explicit. Jesus is "the mediator of a new covenant" (Heb. 12:24) — as Moses mediated at Sinai, Christ mediates a better covenant. The "blood of the covenant" that Moses sprinkled on the people (v.8) points directly to Christ's blood that ratifies the new covenant (Matt. 26:28; Heb. 9:18-22). The writer of Hebrews quotes Exodus 24 at length to show that the old covenant was inaugurated with blood, establishing the theological necessity of Christ's blood to inaugurate the new. And the covenant meal in God's presence (vv.9-11) looks forward to the Lord's Supper and ultimately to the Marriage Supper of the Lamb — eating in fellowship with God, sealed by covenant.

## Moral and Spiritual Lessons
- Covenant is not merely legal but relational — sealed in blood, witnessed in worship, and confirmed at table. God's relationship with His people is not a transaction but a binding communion.
- The people's two-fold "all that the LORD has spoken we will do" (vv.3,7) shows the seriousness of covenant commitment. They meant it — and still failed. This teaches both the importance of sincere commitment and the human inability to sustain it apart from grace.
- The elders ate and drank in God's presence and did not die — extraordinary grace. Every time believers come to the Lord's Table, they participate in covenant fellowship that should feel as extraordinary.
- Forty days of formation on the mountain reminds us that deep learning, preparation, and revelation take time and withdrawal. Formation is not instantaneous.

## Practical Application
Consider the covenant language you use most naturally about your relationship with God. Is it transactional ("I do this, God does that"), contractual (a set of mutual obligations), or covenantal (a blood-bound, personally committed, communally celebrated relationship)? The biblical model is covenant — binding, costly, sealed in Christ's blood, confirmed at table, and calling for full commitment that only becomes possible through the Spirit's enabling.

## Believers Sword Reflection
Exodus 24 is one of the pivot points of redemptive history. The covenant made at Sinai is the framework within which all of Israel's subsequent history unfolds. Its ratification by blood — and the remarkable vision of God attended by a covenant meal — establishes the pattern that Jesus will fulfill and transcend in the upper room. To read this chapter is to stand at the foundation of the architecture that leads to the cross.""",
        "chapter_overview": "Exodus 24 records the Sinai Covenant's formal ratification: Moses reads the covenant, the people twice commit to obedience, covenant blood is thrown on the altar and on the people ('the blood of the covenant'), and the elders ascend to see God and eat in His presence. Moses then ascends alone into the divine cloud for forty days to receive the stone tablets.",
        "original_language_notes": [
            {
                "term": "berît",
                "language": "Hebrew",
                "verse": "Exodus 24:7-8",
                "words_used": "בְּרִית (berît) — 'covenant'",
                "meaning": "'Dam habberît' — 'blood of the covenant' — is unique in the Hebrew Bible to this moment. A berît is a solemn binding relationship commitment, typically sealed with blood, oaths, or shared meals. Jesus quotes this exact phrase at the Last Supper (Matt. 26:28; Mark 14:24), directly connecting Sinai's covenant-sealing to His own sacrificial blood."
            },
            {
                "term": "naʿăśeh venishmaʿ",
                "language": "Hebrew",
                "verse": "Exodus 24:7",
                "words_used": "נַעֲשֶׂה וְנִשְׁמָע (naʿăśeh venishmaʿ) — 'we will do and we will hear/obey'",
                "meaning": "Strikingly, Israel commits to do before they commit to fully understand. Celebrated in Jewish tradition as extraordinary faith — prioritizing obedient action over prior comprehension. It is ultimately fulfilled only in Christ, who obeyed completely even unto death (Phil. 2:8)."
            },
            {
                "term": "kevôd Yahweh",
                "language": "Hebrew",
                "verse": "Exodus 24:17",
                "words_used": "כְּבוֹד יהוה (kevôd Yahweh) — 'the glory of the LORD'",
                "meaning": "Kāvôd comes from a root meaning 'weight/heaviness' — God's glory is not merely radiance but overwhelming presence. Appearing as a 'devouring fire' (ʾēsh ʾōkelet). This same glory fills the tabernacle (Exod. 40:34), the temple (1 Kings 8:11), and dwells in Christ: 'we have seen his glory' (John 1:14)."
            },
            {
                "term": "sappîr",
                "language": "Hebrew",
                "verse": "Exodus 24:10",
                "words_used": "סַפִּיר (sappîr) — 'sapphire'",
                "meaning": "The pavement beneath God's feet described as sapphire — sky-blue, crystalline purity — gives the only partial visual description of the divine environment in Exodus. This imagery recurs in Ezekiel's throne vision (Ezek. 1:26) and Revelation's New Jerusalem (Rev. 21:19), signifying transcendent clarity and purity."
            }
        ],
        "moral_lessons": [
            "Covenant with God is not transactional but relational — binding, blood-sealed, confirmed at table, and requiring full commitment.",
            "The double commitment 'we will do and we will obey' (vv.3,7) shows both the seriousness of covenant and the human inability to sustain it apart from grace — they meant it and still failed.",
            "Eating in God's presence is extraordinary grace — every Lord's Supper is a covenant meal that should feel as remarkable as the elders' meal on the mountain.",
            "Forty days of formation require withdrawal and time — deep spiritual preparation is not instantaneous; it requires sustained withdrawal into God's presence.",
            "The gradations of nearness (people, elders, Moses) remind us that different callings involve different depths of access, and every level requires holiness."
        ],
        "application": "Examine what covenant language you naturally use about your relationship with God. If it defaults to transaction ('I do this, God does that'), invite the Spirit to deepen it into covenant — binding, costly, personally committed, confirmed at the Lord's Table. And consider whether you have a regular pattern of extended withdrawal for formation: not just daily devotions but periods of sustained focus on receiving from God, as Moses spent forty days on the mountain.",
        "prayer": "Covenant-making God, You sealed Your relationship with Your people not in ink but in blood — and You resealed it in the blood of Your own Son. Thank You that the blood of the covenant has been thrown over us, covering us, binding us to You with a commitment that holds even when we fail. Give us the faith to come to Your table with the wonder of those elders who saw You and ate in Your presence. Form us in the secret place as You formed Moses on the mountain. In Christ, the mediator of the new and better covenant. Amen.",
        "key_points": [
            "The covenant is ratified through a blood ritual: half the blood on the altar (God's side), half on the people, uniting both in the 'blood of the covenant.'",
            "The people twice commit 'all that the LORD has spoken we will do' — sincere covenant commitment that they were still unable to keep, showing human inadequacy without grace.",
            "The seventy elders, Moses, Aaron, Nadab, and Abihu see God and eat in His presence — extraordinary covenant fellowship sealed at table without dying.",
            "Moses ascends alone for forty days — a complete period of formation, receiving the stone tablets and the tabernacle instructions.",
            "The structure of access (people at base, elders midway, Moses at summit) previews the tabernacle's graduated holiness architecture.",
            "Jesus quotes 'the blood of the covenant' at the Last Supper, directly connecting this moment to the new covenant sealed in His own blood.",
            "The glory of the LORD appearing as devouring fire on the mountain is the same glory that fills the tabernacle and ultimately dwells in Christ (John 1:14)."
        ],
        "study_questions": [
            "The people said 'we will do and we will be obedient' twice (vv.3,7). What does the fact that they sincerely meant it — and still failed — teach you about the limits of sincere human commitment and the need for grace?",
            "Moses sprinkles blood on both the altar and the people, declaring it 'the blood of the covenant' (v.8). What does this ritual communicate about the nature of covenant as binding both parties? How does this foreshadow the Lord's Supper?",
            "The elders 'saw God and ate and drank' without dying (vv.10-11). What does this covenant meal reveal about what God ultimately desires from His people — law-keeping or fellowship?",
            "Moses spent forty days on the mountain. What does the biblical pattern of forty-day formation periods suggest about how deep spiritual change actually happens? What disciplines of extended withdrawal might God be calling you to?",
            "How does the graduated access to God's presence (people/elders/Moses) both reflect the holiness of God and preview Christ's work of opening access to all believers through the torn curtain (Heb. 10:19-22)?"
        ],
        "tags": [
            "exodus", "covenant", "blood-of-covenant", "sinai", "ratification", "moses", "elders",
            "covenant-meal", "glory", "formation", "forty-days", "tablets", "new-covenant"
        ],
        "sources": []
    },
    {
        "chapter": 25,
        "title": "Exodus 25 — The Tabernacle Pattern: Ark, Table, and Lampstand",
        "summary": "Exodus 25 opens the second half of Exodus, dominated by the instructions for the tabernacle — the portable dwelling place for God's presence among Israel. God commands Moses to collect an offering of materials from the willing-hearted (gold, silver, bronze, textiles, skins, wood, oil, spices, and stones). He then gives detailed specifications for three pieces of furniture: the Ark of the Covenant (chest containing the tablets, topped by the mercy seat and two gold cherubim where God will meet with Moses), the Table of the Bread of the Presence, and the Golden Lampstand (menorah). The chapter establishes the fundamental principle: the tabernacle must be built exactly according to the pattern God shows Moses on the mountain.",
        "content": """## What Exodus 25 Is About
Exodus 25 begins the longest continuous section of the book — six chapters of detailed tabernacle instructions (Exodus 25-31). These chapters, mirrored in Exodus 35-40 by the account of the tabernacle's actual construction, form the center of the book both architecturally and theologically.

**The Offering (vv.1-9)**: God instructs Moses to receive a terumāh — a "contribution" or "heave offering" — from every person whose heart moves him to give. The list of materials is extraordinary: gold, silver, and bronze; blue, purple, and scarlet thread; fine linen; goat hair; ram skins dyed red; goatskins; acacia wood; oil for lamps; spices for anointing oil and incense; onyx stones and gems. These materials will combine in the construction of a "sanctuary" (miqdāsh — holy place) so that God may "dwell" (shākan) among His people. The principle is explicit: "Exactly as I show you concerning the pattern of the tabernacle, and of all its furniture, so you shall make it" (v.9).

**The Ark of the Covenant (vv.10-22)**: The first and most sacred piece of furniture is the ark — a chest of acacia wood overlaid with pure gold inside and out. Its dimensions are specific: 2.5 cubits long, 1.5 cubits wide, 1.5 cubits tall (approximately 45x27x27 inches). It has four gold rings on its corners for carrying poles of acacia wood overlaid with gold — the poles remain in the rings permanently and are never removed. The ark will contain the "testimony" (the stone tablets of the commandments). The ark's lid — the kappōret, translated "mercy seat" or "atonement cover" — is of pure gold, with two gold cherubim at each end, facing each other, their wings spread upward over the cover. It is here, between the cherubim, that God promises to meet with Moses and give him all His commands for Israel (v.22).

**The Table of the Bread of the Presence (vv.23-30)**: The Table is of acacia wood overlaid with gold, 2 cubits long, 1 cubit wide, 1.5 cubits high, with a gold rim, rings, and poles for carrying. On it are placed the "bread of the Presence" — twelve loaves representing the twelve tribes, set before God continually.

**The Golden Lampstand (vv.31-40)**: The menorah is of pure hammered gold — a central shaft with six branches (three on each side), each branch ornamented with cups shaped like almond blossoms, knobs, and flowers. Seven lamps provide light within the tabernacle. No dimensions are given for the lampstand — only the intricate artistic design, "according to the pattern that was shown you on the mountain" (v.40).

## Theological Themes
- **God Dwelling Among His People**: The word shākan ("to dwell," v.8) is the root of shekinah — the divine presence that dwells among Israel. The tabernacle is not a place where Israel goes to find God but where God comes to live with His people. This is the central desire of God across all Scripture: "I will be their God and they will be my people" (Lev. 26:12; Rev. 21:3).
- **Pattern and Precision**: The phrase "exactly as I show you" (v.9) and "according to the pattern" (v.40) frame the entire tabernacle section. The earthly tabernacle is a copy of a heavenly reality — the author of Hebrews makes this explicit (Heb. 8:5, quoting Exodus 25:40). God's house on earth corresponds to the true sanctuary in heaven.
- **The Mercy Seat as Meeting Place**: The ark's kappōret (mercy seat) is where God promises to meet with Moses (v.22). On the Day of Atonement, the high priest would sprinkle blood on the kappōret — covering the law (the tablets beneath) with atonement. Grace covers law; the meeting place is atop the requirements, not beneath them.
- **Willing Hearts, Not Coerced Giving**: The offering is from every person "whose heart moves him" (v.2). God's dwelling is built by voluntary generosity, not taxation or compulsion. Participation in building God's house is a matter of heart, not obligation.

## Hebrew Word Notes
- **מִשְׁכָּן** (mishkān, "tabernacle/dwelling place," v.9) — From shākan (to dwell, to settle). The tabernacle is literally "the place where God camps with His people." John 1:14 uses the Greek equivalent: "the Word became flesh and dwelt (eskēnōsen — pitched His tent) among us" — a direct echo of the mishkān.
- **כַּפֹּרֶת** (kappōret, "mercy seat/atonement cover," vv.17,20) — From kāpar (to cover, to atone). This is one of the most theologically loaded words in the Hebrew Bible. Paul uses its Greek equivalent (hilastērion) in Romans 3:25: "God put forward [Christ] as a propitiation [mercy seat] by his blood." Christ is the true kappōret — the atonement cover who fulfills what the gold lid prefigured.
- **תְּרוּמָה** (terumāh, "contribution/offering," v.2) — Technically a "heave offering," something elevated or set apart from ordinary use and given to God. The tabernacle is built entirely from terumāh — things willingly lifted out of personal resources and dedicated to divine purpose.
- **מְנוֹרָה** (menōrāh, "lampstand," v.31) — From nûr (light/lamp). The seven-branched lampstand provides the tabernacle's only light, since no windows are described. It is light that God provides in a space of His own construction — a forward symbol of Christ as the "light of the world" (John 8:12), and of the New Jerusalem having no need of sun because "the Lamb is its lamp" (Rev. 21:23).

## How This Chapter Points to Christ
Every piece of tabernacle furniture is a type of Christ. The Ark contains the Law — Christ perfectly fulfilled and embodies the Law (Matt. 5:17). The kappōret (mercy seat) is where atonement was made through blood — Christ is the true propitiation/mercy seat (Rom. 3:25; 1 John 2:2), and His blood covers the Law's demands. The Bread of the Presence on the Table — twelve loaves before God continually — foreshadows Christ as the "bread of life" (John 6:35, 48) who presents Himself to the Father continually as our intercessor. The Lampstand — pure gold, giving light inside God's dwelling — is a type of Christ as the Light of the World and of the church as a lampstand (Rev. 1:12-13, 20). The author of Hebrews is explicit: the earthly tabernacle is "a copy and shadow of the heavenly things" (Heb. 8:5); Christ entered the true heavenly sanctuary (Heb. 9:11-12).

## Moral and Spiritual Lessons
- God's dwelling is built by willing generosity — "whose heart moves him." No grudging compliance builds the place where God dwells. Our participation in God's work is a matter of heart-motivation, not legal obligation.
- Precision in obedience matters: "exactly as I show you." Faithfulness to God's revealed pattern is not legalism but love — doing what God actually asked, not what we imagine He might prefer.
- The mercy seat sits atop the Law — grace is not opposed to God's requirements but is placed over them, covering them with atonement. This is the spatial theology of the gospel.
- The tabernacle's light comes entirely from within — the lampstand, not external windows. The church's light comes from Christ within, not from the surrounding culture.

## Practical Application
The willing-hearted offering (v.2) is the model for all Christian giving. Examine your giving to God's work: is it motivated by legal obligation, social pressure, or a heart genuinely moved by gratitude and love for the One who dwells among His people? And consider the "pattern" principle: where God has revealed His design (in Scripture, in creation's order, in conscience), precision and faithfulness matter. The question is not what design we prefer but what God has shown.

## Believers Sword Reflection
Exodus 25 begins one of Scripture's most intricate and theologically dense sections. Modern readers are tempted to skim the specifications, but the details carry enormous weight: every material, every dimension, every design element communicates theological truth about the God who dwells among His people. The tabernacle is God's architectural sermon — read it as carefully as you would read His words.""",
        "chapter_overview": "Exodus 25 opens the tabernacle section with a willing-heart offering call and detailed instructions for the three most sacred pieces of furniture: the Ark of the Covenant (gold chest with the kappōret mercy seat, where God will meet with Moses), the Table of the Bread of the Presence, and the Golden Lampstand (menorah). The guiding principle: everything must be built exactly 'according to the pattern' God shows Moses on the mountain.",
        "original_language_notes": [
            {
                "term": "mishkān",
                "language": "Hebrew",
                "verse": "Exodus 25:9",
                "words_used": "מִשְׁכָּן (mishkān) — 'tabernacle, dwelling place'",
                "meaning": "From shākan (to dwell, settle, camp with). The tabernacle is God's 'camping place' among Israel. John 1:14 echoes this with eskēnōsen ('pitched his tent/tabernacled among us') — the Incarnation as the ultimate tabernacling of God with humanity."
            },
            {
                "term": "kappōret",
                "language": "Hebrew",
                "verse": "Exodus 25:17",
                "words_used": "כַּפֹּרֶת (kappōret) — 'mercy seat, atonement cover'",
                "meaning": "From kāpar (to cover, to atone). The lid of the ark where blood was sprinkled on the Day of Atonement, covering the tablets of the Law with atonement. Paul uses the Greek equivalent hilastērion in Romans 3:25 for Christ: 'God put forward [Christ] as a propitiation by his blood' — Christ is the true kappōret."
            },
            {
                "term": "terumāh",
                "language": "Hebrew",
                "verse": "Exodus 25:2",
                "words_used": "תְּרוּמָה (terumāh) — 'contribution, heave offering'",
                "meaning": "From rûm (to raise, lift up). Something lifted out of ordinary use and elevated for divine purpose. The qualification 'from every man whose heart moves him' makes the terumāh a voluntary gift — the entire tabernacle is built on willing generosity, not compelled taxation."
            },
            {
                "term": "menōrāh",
                "language": "Hebrew",
                "verse": "Exodus 25:31",
                "words_used": "מְנוֹרָה (menōrāh) — 'lampstand'",
                "meaning": "The seven-branched gold lampstand is the tabernacle's interior light source. Its seven lamps recall the seven days of creation — God's light ordering the cosmos. Revelation uses the menōrāh as a symbol for the churches (Rev. 1:12-13,20), each one called to hold aloft the light of Christ."
            }
        ],
        "moral_lessons": [
            "God's house is built by willing hearts — no grudging compliance builds the place where God dwells; participation in God's work must flow from heart-motivation.",
            "Precision in obedience to God's revealed pattern is not legalism but love — doing what God actually asked, not what we imagine He might prefer.",
            "The mercy seat sits atop the Law — grace does not abolish God's requirements but covers them with atonement; this is the spatial theology of the gospel.",
            "All light in the tabernacle comes from within (the lampstand) — the church's light comes from Christ within, not from accommodation to surrounding culture.",
            "The tabernacle details deserve careful reading: every dimension and material is a theological statement about the God who dwells with His people."
        ],
        "application": "Examine your participation in God's work — in church, in mission, in giving. Is it motivated by willing love or reluctant obligation? The terumāh model requires a 'heart that moves' you. And where God has revealed His pattern through Scripture, practice careful faithfulness: the question is not what design seems convenient to you but what God has shown on the mountain.",
        "prayer": "Lord who dwells among Your people, You have always desired to be with us — from the mishkān in the wilderness to the tabernacling of Your Son among us to the Spirit who now dwells in us. Thank You that You provided a kappōret, a mercy seat, where Your Law's demands are covered by atoning blood. Build us into Your dwelling place — not from compulsion but from hearts moved by love for You. Be the light within us. In Christ, who is the true tabernacle, the true mercy seat, and the true light of the world. Amen.",
        "key_points": [
            "The offering is from 'everyone whose heart moves him' — God's house is built by willing generosity, not compulsion.",
            "The mishkān (tabernacle/dwelling) signals God's desire to 'dwell' (shākan) among His people — the foundational relational goal of all Scripture.",
            "The Ark of the Covenant contains the tablets of the Law; its lid, the kappōret (mercy seat), is where blood covers the Law on the Day of Atonement — grace over law.",
            "God promises to meet with Moses between the cherubim above the kappōret — the mercy seat is the meeting place between God and man.",
            "All tabernacle construction must follow 'the pattern' shown on the mountain — earthly worship corresponds to heavenly reality (Heb. 8:5).",
            "The Golden Lampstand (menorah) provides interior light — prefiguring Christ as the light of the world (John 8:12) and the church as light-bearer (Rev. 1:20).",
            "Christ fulfills every piece of furniture: He embodies the Law (Ark), is the true propitiation/mercy seat (Rom. 3:25), the bread of life (Table), and the light of the world (Lampstand)."
        ],
        "study_questions": [
            "God insists the tabernacle must be built 'according to the pattern' shown on the mountain (vv.9,40). What does this say about the importance of God's revealed will vs. our own religious creativity? Where does this principle apply to worship and ministry today?",
            "The kappōret (mercy seat) sits on top of the ark that contains the Law. What does this spatial arrangement communicate theologically about the relationship between law and grace?",
            "The offering for the tabernacle was received only from 'everyone whose heart moves him' (v.2). How does this model challenge or shape your understanding of giving and participation in God's work?",
            "Paul uses the word 'hilastērion' (the Greek for kappōret) to describe Christ in Romans 3:25. What does it mean for Christ to be our 'mercy seat,' and how does the Day of Atonement ritual illuminate what He accomplished?",
            "John 1:14 says the Word 'tabernacled among us' (eskēnōsen). How does the Incarnation fulfill and transcend the tabernacle — what does Jesus provide that the wilderness mishkān could not?"
        ],
        "tags": [
            "exodus", "tabernacle", "ark-of-covenant", "mercy-seat", "kaporet", "lampstand",
            "menorah", "bread-of-presence", "dwelling", "shekinah", "types-of-christ", "pattern"
        ],
        "sources": []
    },
    {
        "chapter": 26,
        "title": "Exodus 26 — The Tabernacle Structure: Curtains, Boards, and the Holy of Holies",
        "summary": "Exodus 26 provides the detailed architectural instructions for the tabernacle's physical structure: four layers of curtains forming the roof and walls (fine linen, goat hair, ram skins, and sea-cow hides), a frame of acacia-wood boards with silver sockets, crossbars of acacia wood for stability, and the inner veil of blue, purple, and scarlet thread with cherubim separating the Holy Place from the Holy of Holies. The chapter specifies every dimension, material, and joining mechanism. The result is a layered, graduated structure with the most sacred space at the innermost point — a theology of holiness written in fabric, wood, and metal.",
        "content": """## What Exodus 26 Is About
Exodus 26 gives the architectural blueprint for the tabernacle — the portable sanctuary that would house the ark, the table, and the lampstand. The instructions are precise and detailed, covering four layers of covering materials, the acacia-wood frame, the separating veil, and the entrance screen.

**The Four Layers of Covering (vv.1-14)**: The tabernacle's roof and walls are formed by four layers, each serving a different function:
1. **Fine Linen Curtains (vv.1-6)**: Ten curtains of fine twisted linen in blue, purple, and scarlet, decorated with cherubim in "skillful work." They are coupled in sets of five with gold clasps through loops of blue at the edges. These form the innermost, most beautiful layer — visible only to priests inside the tabernacle.
2. **Goat Hair Curtains (vv.7-13)**: Eleven curtains of goat hair form the outer tent, covered with bronze clasps through loops. This layer is functional and protective, extending slightly beyond the linen curtains on the sides and back.
3. **Ram Skin and Sea-Cow Hide (v.14)**: The outermost covering provides weather protection — ram skins dyed red, topped by sea-cow (or dugong/porpoise) hides.

**The Acacia-Wood Frame (vv.15-30)**: The tabernacle's structural walls are formed by upright boards (qerāshîm) of acacia wood overlaid with gold, each with two projecting tenons that fit into silver sockets (ʾadānîm) set in the ground. The boards are stabilized by crossbars through rings of gold on each board: five sets of crossbars on the south, north, and west walls, with the middle crossbar running the entire length.

**The Veil Separating the Holy of Holies (vv.31-35)**: A veil (pārōket) of blue, purple, and scarlet thread with cherubim in skilled weaving hangs on four acacia posts with gold hooks in silver sockets. This veil divides the tabernacle into two rooms: the outer Holy Place (containing the table and lampstand) and the inner Holy of Holies (containing the ark). Only the high priest may enter the Holy of Holies, once a year.

**The Entrance Screen (vv.36-37)**: An embroidered screen hangs at the entrance to the tabernacle — also in blue, purple, and scarlet — on five acacia posts with gold hooks in bronze sockets.

## Theological Themes
- **Graduated Holiness Architecture**: The tabernacle's concentric design — outermost covering, then frame, then Holy Place, then Holy of Holies at the center — embeds a theology of holiness in its spatial structure. Proximity to God increases inward. Access becomes more restricted as holiness increases. This spatial theology will reach its ultimate expression in Christ, who tears the veil (Matt. 27:51) and opens the Holy of Holies to all believers (Heb. 10:19-22).
- **Beauty for God's Dwelling**: The innermost curtains — visible only to priests — are the most beautiful, decorated with cherubim in "skillful work." The most elaborate artistry is directed toward God, not toward human observers. True worship adorns the place of divine presence, not the place of human display.
- **Stability and Portability in Tension**: The tabernacle is simultaneously portable (designed for wilderness travel) and stable (heavy acacia boards in silver sockets, multiple crossbars). This captures Israel's in-between state: not yet settled, but also not rootless. God's presence among them is genuinely structured and secure even in motion.
- **The Veil as Barrier and Invitation**: The pārōket veil is both a barrier (marking the boundary of the Holy of Holies) and a declaration that God is present within it. Its cherubim recall the cherubim of Eden (Gen. 3:24) who guarded the way to the tree of life after the fall. The veil says: the garden has not been forgotten; the way to God's presence is structured, not closed. When Christ dies, this veil tears in two — not destroying the holiness of God but opening access through the mediating high priest who has passed through the veil by His own blood (Heb. 10:20).

## Hebrew Word Notes
- **קְרָשִׁים** (qerāshîm, "boards/planks," vv.15-29) — The structural frame of the tabernacle. Each board is a substantial piece of acacia wood overlaid with gold — portable but weighty, beautiful but structural. The tabernacle is not a tent of flimsy fabric but a solid gold-covered structure within its outermost coverings.
- **אֲדָנִים** (ʾadānîm, "sockets/bases," vv.19,21,25) — The silver sockets into which the boards' tenons are set. Each socket contained one talent of silver (Exod. 38:27) — the ransom money paid by each Israelite for his life. The tabernacle literally rests on a foundation of atonement silver. This is a profound architectural theology: God's dwelling among His people rests on the redemption price.
- **פָּרֹכֶת** (pārōket, "veil/curtain," vv.31-35) — The inner veil separating the Holy Place from the Holy of Holies. This is the veil that tears when Jesus dies (Matt. 27:51; Mark 15:38). Hebrews 10:20 interprets it as Christ's flesh — His body was the veil that, torn in crucifixion, opens the way into God's presence for all who come through Him.
- **שֵׁשׁ מָשְׁזָר** (shēsh māshezār, "fine twisted linen," v.1) — The most refined textile material, with threads twisted together for strength and smoothness. Its white color represents purity; the blue, purple, and scarlet threads woven through it represent heaven (blue), royalty (purple), and redemption/blood (scarlet). The innermost curtains are a visual theology of God's character.

## How This Chapter Points to Christ
The veil (pārōket) is the primary Christological lens in Exodus 26. Hebrews 10:20 interprets the veil as "his flesh" — Christ's body is the veil through which believers enter the presence of God. When His body was torn at the cross, the veil tore from top to bottom (Matt. 27:51) — God's act from heaven downward, opening access that no human could open from below. The silver sockets, resting on atonement silver, preview the ransom-foundation of God's dwelling with humanity. And the cherubim woven throughout the curtains and veil echo Eden's guarded way — now opened rather than barred, through the Mediator who has passed through.

## Moral and Spiritual Lessons
- The most beautiful craftsmanship is reserved for what only God sees. True worship does not require a human audience; the finest of what we offer is for Him.
- God's dwelling has structure. Holiness is not a vague feeling but a real quality of God's being that shapes the space around Him — even in a portable tent in a desert.
- The veil is both barrier and invitation. The holiness of God is not a rejection of humanity but the shape of the presence that sinners cannot approach without mediation. Christ does not eliminate God's holiness but provides the Mediator through whom holiness becomes access.
- God's tabernacle rests on atonement silver — the redemption price. Every aspect of God's dwelling among His people is built on the foundation of ransom paid on their behalf.

## Practical Application
Notice the care and precision given to the tabernacle's construction. What does it communicate about the value of doing well what we dedicate to God? Whether it is worship music, service, teaching, or hospitality — what we offer to God in the context of His gathered people deserves our finest work, even when no human audience is watching. The innermost curtains teach that the quality of what we give to God is not measured by its visibility to others.

## Believers Sword Reflection
Exodus 26 may seem like a construction manual, but it is a theological document in three dimensions. Every detail — the four layers, the graduated structure, the veil with its cherubim, the silver-socket foundation — encodes the character of the God who dwells among His people. Reading it with care is an act of reverence for a God who cares enough about His own dwelling to specify it with precision.""",
        "chapter_overview": "Exodus 26 details the tabernacle's physical structure: four layers of coverings (fine linen with cherubim, goat hair, ram skins, sea-cow hides), acacia-wood boards in silver sockets with gold crossbars, and an inner veil of blue/purple/scarlet with cherubim separating the Holy Place from the Holy of Holies. The design embeds graduated holiness in architecture — most sacred at the center, most accessible at the outer edge.",
        "original_language_notes": [
            {
                "term": "pārōket",
                "language": "Hebrew",
                "verse": "Exodus 26:31",
                "words_used": "פָּרֹכֶת (pārōket) — 'the veil, inner curtain'",
                "meaning": "The dividing veil between the Holy Place and the Holy of Holies. This is the veil that tears when Jesus dies (Matt. 27:51). Hebrews 10:20 interprets it as Christ's flesh: His body was the veil through which, torn at crucifixion, believers now have open access into God's presence."
            },
            {
                "term": "ʾadānîm",
                "language": "Hebrew",
                "verse": "Exodus 26:19",
                "words_used": "אֲדָנִים (ʾadānîm) — 'sockets, bases'",
                "meaning": "Silver sockets into which the tabernacle's boards are set. Each socket was made from one talent of silver — the ransom/atonement silver paid by every Israelite (Exod. 38:25-27). The tabernacle literally stands on a foundation of atonement money: God's dwelling among His people rests on the redemption price paid for them."
            },
            {
                "term": "qerāshîm",
                "language": "Hebrew",
                "verse": "Exodus 26:15",
                "words_used": "קְרָשִׁים (qerāshîm) — 'boards, planks'",
                "meaning": "Substantial acacia-wood boards overlaid with gold that form the tabernacle's structural walls. Their weight and solidity give stability within a portable structure — the tabernacle is not a flimsy tent but a gold-covered wooden structure representing permanence within mobility."
            },
            {
                "term": "shēsh māshezār",
                "language": "Hebrew",
                "verse": "Exodus 26:1",
                "words_used": "שֵׁשׁ מָשְׁזָר (shēsh māshezār) — 'fine twisted linen'",
                "meaning": "The most refined textile — threads twisted together for strength and purity. White linen represents holiness/purity; the blue (heaven), purple (royalty), and scarlet (blood/redemption) threads woven into it create a visual theology of God's character visible on the innermost curtains that only priests could see."
            }
        ],
        "moral_lessons": [
            "The finest craftsmanship goes to the innermost layer — visible only to God. True worship gives its best to the One who sees in secret, not to impress a human audience.",
            "God's dwelling has structure and graduated holiness — holiness is not vague but shapes the space around God's presence; approaching Him requires mediation.",
            "The veil is both barrier and invitation: God's holiness is not a rejection of humanity but the shape of His presence that requires a Mediator — Christ opened, not eliminated, the veil.",
            "The tabernacle rests on a foundation of atonement silver — God's dwelling among His people is built entirely on the redemption price paid for them.",
            "Precision in what we dedicate to God matters; the care given to the tabernacle's details models the quality of heart and craft we bring to God's service."
        ],
        "application": "Apply the 'innermost curtain' principle to your spiritual life: give God your finest offerings even when no human audience is present. In worship, prayer, service, or creative work dedicated to Him — what do you hold back because 'no one will see it anyway'? The tabernacle teaches that the hidden quality of our devotion to God is its truest measure.",
        "prayer": "Architect of Your own dwelling, You are specific about where You dwell and how Your holiness is approached. Thank You that the veil that once barred the way has been torn from top to bottom — by Your own hand, from heaven downward — through the body of Your Son. We enter the Holy of Holies not by our own purity but through Christ who is both the veil and the way through it. Make us worthy of the access You have opened. In Christ, our great High Priest who has passed through the heavenly veil. Amen.",
        "key_points": [
            "Four layers of covering: fine linen (cherubim, innermost), goat hair (outer tent), ram skins (dyed red), and sea-cow hides (weatherproof exterior).",
            "The innermost linen curtains — visible only to priests — are the most beautiful, teaching that true worship reserves its finest for God, not for human display.",
            "Acacia-wood boards in silver sockets form the structural frame; the sockets were made from Israel's atonement silver — God's dwelling literally rests on redemption.",
            "The pārōket (veil) with cherubim separates the Holy Place from the Holy of Holies, embedding graduated holiness in the architectural structure.",
            "The veil's cherubim recall Eden's guarding cherubim (Gen. 3:24) — the way to God's presence is structured but not permanently closed.",
            "When Christ dies, this veil tears from top to bottom (Matt. 27:51) — God opens, from heaven down, the access that no human could open from below.",
            "Hebrews 10:20 interprets the veil as Christ's flesh — torn in crucifixion, His body becomes the torn veil that gives all believers direct access to the Father."
        ],
        "study_questions": [
            "The most beautiful curtains (fine linen with cherubim) are innermost — only visible to priests. What does this teach about the relationship between quality of worship and visibility to human observers?",
            "The tabernacle's boards stand in silver sockets made from atonement silver (Exod. 38:25-27). What does it mean theologically that God's dwelling among His people is literally built on the foundation of their ransom price?",
            "The veil separating the Holy Place from the Holy of Holies was embroidered with cherubim. How does this connect to the cherubim guarding Eden in Genesis 3:24? What does this continuity suggest about the tabernacle's place in redemptive history?",
            "Hebrews 10:20 says the veil represents Christ's flesh, torn open at the cross. What does this interpretation do to your understanding of the crucifixion — not only as atonement but as access?",
            "The tabernacle is both portable (for wilderness travel) and structurally solid (heavy boards, multiple crossbars). What does this balance between mobility and stability communicate about God's presence with His people during times of transition?"
        ],
        "tags": [
            "exodus", "tabernacle", "veil", "holy-of-holies", "holy-place", "curtains",
            "atonement-silver", "architecture", "graduated-holiness", "cherubim", "types-of-christ"
        ],
        "sources": []
    }
]


def get_or_create_collection(conn):
    cur = conn.cursor()
    cur.execute("SELECT id FROM commentary_collections WHERE slug = 'believers-sword-commentaries' AND language_code = 'en'")
    row = cur.fetchone()
    if row:
        return row[0]
    col_uuid = str(uuid.uuid4())
    cur.execute("""
        INSERT INTO commentary_collections (uuid, name, slug, collection_type, language_code, theological_perspective, is_offline_available, sync_status, created_at, updated_at)
        VALUES (?, 'Believers Sword Commentaries', 'believers-sword-commentaries', 'ai_generated', 'en', 'Evangelical Christian', 1, 'local', ?, ?)
    """, (col_uuid, NOW, NOW))
    conn.commit()
    return cur.lastrowid


def entry_exists(conn, collection_id, book_id, chapter):
    cur = conn.cursor()
    cur.execute("""
        SELECT id, content FROM commentary_entries
        WHERE collection_id = ? AND book_id = ? AND chapter = ?
        AND language_code = 'en' AND reference_scope = 'chapter' AND deleted_at IS NULL
    """, (collection_id, book_id, chapter))
    row = cur.fetchone()
    if row:
        content = row[1] or ""
        return True, len(content) > 500
    return False, False


def insert_entry(conn, collection_id, entry_data):
    cur = conn.cursor()
    entry_uuid = str(uuid.uuid4())
    cur.execute("""
        INSERT INTO commentary_entries (
            uuid, collection_id, book_id, chapter, verse_start, verse_end,
            reference_scope, title, summary, content, application, prayer,
            key_points, study_questions, language_code, theological_perspective,
            status, is_ai_generated, ai_model_name, ai_model_provider,
            word_count, sync_status, created_at, updated_at
        ) VALUES (?,?,?,?,NULL,NULL,'chapter',?,?,?,?,?,?,?,'en','Evangelical Christian',
                  'draft',1,'claude-sonnet-4-6','anthropic',?,  'local',?,?)
    """, (
        entry_uuid, collection_id, entry_data["book_id"], entry_data["chapter"],
        entry_data["title"], entry_data["summary"], entry_data["content"],
        entry_data["application"], entry_data["prayer"],
        json.dumps(entry_data["key_points"]), json.dumps(entry_data["study_questions"]),
        len(entry_data["content"].split()),
        NOW, NOW
    ))
    conn.commit()
    return entry_uuid


def save_json(entry_data, entry_uuid):
    os.makedirs(GENERATED_DIR, exist_ok=True)
    chapter = entry_data["chapter"]
    filename = f"{chapter:02d}.json"
    filepath = os.path.join(GENERATED_DIR, filename)

    output = {
        "uuid": entry_uuid,
        "collection_name": COLLECTION_NAME,
        "author_type": AUTHOR_TYPE,
        "language_code": LANGUAGE_CODE,
        "theological_perspective": THEOLOGICAL_PERSPECTIVE,
        "status": "draft",
        "book_id": BOOK_ID,
        "book": BOOK_NAME,
        "chapter": chapter,
        "title": entry_data["title"],
        "summary": entry_data["summary"],
        "content": entry_data["content"],
        "chapter_overview": entry_data["chapter_overview"],
        "original_language_notes": entry_data["original_language_notes"],
        "moral_lessons": entry_data["moral_lessons"],
        "application": entry_data["application"],
        "prayer": entry_data["prayer"],
        "key_points": entry_data["key_points"],
        "study_questions": entry_data["study_questions"],
        "tags": entry_data["tags"],
        "sources": entry_data["sources"],
        "created_at": NOW,
        "updated_at": NOW
    }

    # Verify no forbidden keys
    forbidden = {"is_ai_generated", "model_name", "prompt_version"}
    for key in forbidden:
        assert key not in output, f"Forbidden key found: {key}"

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    # Verify it parses back
    with open(filepath, "r", encoding="utf-8") as f:
        parsed = json.load(f)
    for key in forbidden:
        assert key not in parsed, f"Forbidden key in parsed JSON: {key}"

    return filepath


def update_progress(conn, last_chapter):
    book_order = [
        ("Genesis", 1, 50), ("Exodus", 2, 40), ("Leviticus", 3, 27), ("Numbers", 4, 36),
        ("Deuteronomy", 5, 34), ("Joshua", 6, 24), ("Judges", 7, 21), ("Ruth", 8, 4),
        ("1 Samuel", 9, 31), ("2 Samuel", 10, 24), ("1 Kings", 11, 22), ("2 Kings", 12, 25),
        ("1 Chronicles", 13, 29), ("2 Chronicles", 14, 36), ("Ezra", 15, 10), ("Nehemiah", 16, 13),
        ("Esther", 17, 10), ("Job", 18, 42), ("Psalms", 19, 150), ("Proverbs", 20, 31),
        ("Ecclesiastes", 21, 12), ("Song of Solomon", 22, 8), ("Isaiah", 23, 66),
        ("Jeremiah", 24, 52), ("Lamentations", 25, 5), ("Ezekiel", 26, 48), ("Daniel", 27, 12),
        ("Hosea", 28, 14), ("Joel", 29, 3), ("Amos", 30, 9), ("Obadiah", 31, 1),
        ("Jonah", 32, 4), ("Micah", 33, 7), ("Nahum", 34, 3), ("Habakkuk", 35, 3),
        ("Zephaniah", 36, 3), ("Haggai", 37, 2), ("Zechariah", 38, 14), ("Malachi", 39, 4),
        ("Matthew", 40, 28), ("Mark", 41, 16), ("Luke", 42, 24), ("John", 43, 21),
        ("Acts", 44, 28), ("Romans", 45, 16), ("1 Corinthians", 46, 16),
        ("2 Corinthians", 47, 13), ("Galatians", 48, 6), ("Ephesians", 49, 6),
        ("Philippians", 50, 4), ("Colossians", 51, 4), ("1 Thessalonians", 52, 5),
        ("2 Thessalonians", 53, 3), ("1 Timothy", 54, 6), ("2 Timothy", 55, 4),
        ("Titus", 56, 3), ("Philemon", 57, 1), ("Hebrews", 58, 13), ("James", 59, 5),
        ("1 Peter", 60, 5), ("2 Peter", 61, 3), ("1 John", 62, 5), ("2 John", 63, 1),
        ("3 John", 64, 1), ("Jude", 65, 1), ("Revelation", 66, 22)
    ]

    current_book = BOOK_NAME
    current_book_id = BOOK_ID
    current_max = 40  # Exodus has 40 chapters

    if last_chapter >= current_max:
        # Move to next book
        for i, (name, bid, maxch) in enumerate(book_order):
            if bid == current_book_id and i + 1 < len(book_order):
                next_name, next_bid, _ = book_order[i + 1]
                next_book = next_name
                next_book_id = next_bid
                next_chapter = 1
                completed = False
                break
        else:
            next_book = current_book
            next_book_id = current_book_id
            next_chapter = last_chapter + 1
            completed = False
    else:
        next_book = current_book
        next_book_id = current_book_id
        next_chapter = last_chapter + 1
        completed = False

    progress = {
        "next_book_id": next_book_id,
        "next_book": next_book,
        "next_chapter": next_chapter,
        "last_completed_book_id": current_book_id,
        "last_completed_book": current_book,
        "last_completed_chapter": last_chapter,
        "completed": completed,
        "updated_at": NOW
    }

    with open("commentary_generation_progress.json", "w") as f:
        json.dump(progress, f, indent=2)

    cur = conn.cursor()
    cur.execute("SELECT id FROM commentary_generation_progress LIMIT 1")
    row = cur.fetchone()
    if row:
        cur.execute("""
            UPDATE commentary_generation_progress
            SET next_book_id=?, next_book=?, next_chapter=?,
                last_completed_book_id=?, last_completed_book=?, last_completed_chapter=?,
                completed=?, updated_at=?
            WHERE id=?
        """, (next_book_id, next_book, next_chapter,
              current_book_id, current_book, last_chapter,
              0 if not completed else 1, NOW, row[0]))
    else:
        cur.execute("""
            INSERT INTO commentary_generation_progress
            (next_book_id, next_book, next_chapter, last_completed_book_id, last_completed_book,
             last_completed_chapter, completed, updated_at)
            VALUES (?,?,?,?,?,?,?,?)
        """, (next_book_id, next_book, next_chapter,
              current_book_id, current_book, last_chapter,
              0 if not completed else 1, NOW))
    conn.commit()
    return progress


def append_log(batch_id, start_ref, end_ref, generated, skipped, inserted, files):
    import datetime
    log_entry = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "generation_batch_id": batch_id,
        "start_reference": start_ref,
        "end_reference": end_ref,
        "chapters_generated": generated,
        "chapters_skipped": skipped,
        "db_rows_inserted": inserted,
        "files_written": files
    }
    with open("commentary_generation_log.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")


def main():
    import random
    batch_id = str(uuid.uuid4())

    conn = sqlite3.connect(DB_PATH)
    collection_id = get_or_create_collection(conn)

    generated_count = 0
    skipped_count = 0
    inserted_count = 0
    files_written = []
    last_chapter = None

    for entry_data in COMMENTARIES:
        chapter = entry_data["chapter"]
        entry_data["book_id"] = BOOK_ID
        exists, is_deep = entry_exists(conn, collection_id, BOOK_ID, chapter)

        if exists and is_deep:
            print(f"SKIP: Exodus {chapter} already exists with deep content.")
            skipped_count += 1
            last_chapter = chapter
            continue

        print(f"GENERATING: Exodus {chapter} - {entry_data['title']}")
        entry_uuid = insert_entry(conn, collection_id, entry_data)
        filepath = save_json(entry_data, entry_uuid)
        files_written.append(filepath)
        generated_count += 1
        inserted_count += 1
        last_chapter = chapter
        print(f"  -> Saved: {filepath} (uuid: {entry_uuid})")

    if last_chapter:
        progress = update_progress(conn, last_chapter)
        print(f"\nProgress updated: next = {progress['next_book']} {progress['next_chapter']}")

    conn.close()

    start_ref = f"Exodus {COMMENTARIES[0]['chapter']}"
    end_ref = f"Exodus {COMMENTARIES[-1]['chapter']}"
    append_log(batch_id, start_ref, end_ref, generated_count, skipped_count, inserted_count, files_written)

    print(f"\n=== DONE ===")
    print(f"Generated: {generated_count}, Skipped: {skipped_count}")
    print(f"DB rows inserted: {inserted_count}")
    print(f"Files written: {len(files_written)}")
    for f in files_written:
        print(f"  {f}")


if __name__ == "__main__":
    main()
