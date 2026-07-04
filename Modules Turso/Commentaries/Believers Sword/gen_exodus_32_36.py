import sqlite3
import json
import uuid
import os
from datetime import datetime, timezone

WORKSPACE = "/mnt/d/Projects/Personal/Believers-Sword/Modules Turso/Commentaries/Believers Sword"
DB_PATH = os.path.join(WORKSPACE, "believers_sword_commentaries.db")
GENERATED_DIR = os.path.join(WORKSPACE, "generated")
PROGRESS_JSON = os.path.join(WORKSPACE, "commentary_generation_progress.json")
LOG_JSONL = os.path.join(WORKSPACE, "commentary_generation_log.jsonl")

COLLECTION_NAME = "Believers Sword Commentaries"
COLLECTION_SLUG = "believers-sword-commentaries"
LANGUAGE_CODE = "en"
AUTHOR_TYPE = "ai"
THEOLOGICAL_PERSPECTIVE = "evangelical"
STATUS = "draft"

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
BATCH_ID = str(uuid.uuid4())

CHAPTERS = [
    {
        "book_id": 2,
        "book": "Exodus",
        "chapter": 32,
        "title": "The Golden Calf: Israel's Great Rebellion",
        "summary": "While Moses is on Mount Sinai receiving the law, the Israelites convince Aaron to make a golden calf idol. God threatens to destroy the nation, but Moses intercedes. Moses descends, destroys the tablets, grinds the calf to powder, and calls the Levites to execute judgment. Three thousand die. Moses returns to God to atone for the people's sin.",
        "content": """Exodus 32 stands as one of the most sobering chapters in all of Scripture, narrating Israel's catastrophic fall into idolatry at the very moment God was inscribing His law on stone tablets. The timing could not be more damning—while Moses communed with God on Sinai for forty days, the people grew impatient and demanded from Aaron a visible god to lead them.

**The Sin of Impatience and Idolatry (vv. 1-6)**

The root of Israel's sin was a failure of faith in the invisible God. Unable to see Moses or the Lord, they reverted to the religious patterns of Egypt, where gods were crafted and controlled. Aaron's compliance is shocking—he not only acquiesced but personally fashioned the calf and announced, "These are your gods, O Israel, who brought you up out of Egypt" (v. 4). Aaron even proclaimed a "feast to the LORD" (v. 5), an attempt to blend worship of the calf with Yahweh worship—a syncretism God utterly rejects. The people's revelry (v. 6) echoed Canaanite fertility worship and represented a wholesale abandonment of covenant loyalty.

**God's Response: Holy Wrath and the Intercessor (vv. 7-14)**

God's response to Moses reveals the severity of the transgression. He calls Israel "your people" (not "my people"), signaling that the covenant relationship has been breached. The command to Moses—"Let me alone, that my wrath may burn hot against them and I may consume them, in order that I may make a great nation of you" (v. 10)—is not God expressing uncertainty, but a divine invitation for Moses to intercede. Moses's prayer is remarkable: he appeals to God's honor among the nations, His sworn promises to Abraham, Isaac, and Jacob, and the nature of God's own character. This is one of Scripture's most powerful portraits of intercession. God "relented" (v. 14)—not because He changed His mind arbitrarily, but because Moses's prayer aligned with God's own redemptive purposes.

**Moses and Judgment (vv. 15-29)**

When Moses descends and sees the calf and the dancing, his anger burns and he shatters the tablets—a dramatic sign that Israel had already broken the covenant. He burns the calf, grinds it to powder, and forces the people to drink the mixture—a public humiliation of their idol. Moses confronts Aaron, who offers a pathetically evasive explanation: "I threw [the gold] into the fire, and out came this calf!" (v. 24). Moses then calls upon the Levites, who execute judgment—three thousand die. This act of judgment actually consecrated the Levites for priestly service, demonstrating that faithfulness to God surpasses familial loyalties.

**Atonement and Its Limits (vv. 30-35)**

Moses's offer to be blotted from God's book in place of the people prefigures the atoning work of Christ, yet God refuses: "Whoever has sinned against me, I will blot out of my book." There is no proxy atonement apart from the divinely appointed Mediator. God sends a plague, and promises His angel will lead them forward—but the full weight of the sin is not forgotten. Exodus 32 teaches that no manufactured substitute can replace the living God, that sin has consequences even when judgment is deferred, and that genuine intercession flows from love for both God and people.

**Christ in Exodus 32**

Moses's intercessory prayer—offering himself for the people—points to the ultimate Mediator, Jesus Christ, who would not merely offer Himself symbolically but actually bear the sins of His people on the cross. Unlike Moses, whose intercession could only delay judgment, Christ's intercession accomplishes full and final atonement (Hebrews 7:25; Romans 8:34). The golden calf prefigures all human attempts to replace God with something visible, controllable, and fashioned by human hands—the essence of idolatry in every age.""",
        "chapter_overview": "Israel falls into golden calf idolatry; God threatens judgment; Moses intercedes; covenant tablets shattered; Levites execute judgment; Moses offers himself for atonement.",
        "original_language_notes": [
            {
                "term": "חָטָא (chata)",
                "language": "Hebrew",
                "verse": "32:21",
                "words_used": ["sin", "sinned"],
                "meaning": "To miss the mark, to err, to commit an offense. Used here of Aaron causing Israel to sin (hiphil causative form), emphasizing his culpability in leading the people into transgression."
            },
            {
                "term": "עֵגֶל (egel)",
                "language": "Hebrew",
                "verse": "32:4",
                "words_used": ["calf"],
                "meaning": "A young bull or calf. In ancient Near Eastern religion, bulls symbolized strength and fertility. Egypt's Apis bull cult likely influenced Israel's choice of this form for their idol."
            },
            {
                "term": "נָחַם (nacham)",
                "language": "Hebrew",
                "verse": "32:14",
                "words_used": ["relented", "repented"],
                "meaning": "To be sorry, to relent, to have compassion. God 'relenting' does not indicate a change in His eternal will, but a responsive adjustment to human repentance and intercession within time—consistent with His immutable character."
            },
            {
                "term": "כָּפַר (kaphar)",
                "language": "Hebrew",
                "verse": "32:30",
                "words_used": ["atone", "atonement"],
                "meaning": "To cover, to appease, to make atonement. Moses's stated intention to 'make atonement' (v.30) uses this cultic term which underlies all of Israel's sacrificial system—ultimately pointing to Christ's definitive atonement."
            },
            {
                "term": "מָחָה (machah)",
                "language": "Hebrew",
                "verse": "32:32",
                "words_used": ["blot out"],
                "meaning": "To wipe out, erase, obliterate. Moses asks God to blot him from the divine record—a dramatic intercession paralleling Paul's similar anguished cry in Romans 9:3, where apostolic love drives one to offer oneself for others."
            }
        ],
        "moral_lessons": [
            "Impatience with God's timing leads to spiritual compromise and idolatry.",
            "Leaders bear special responsibility—Aaron's compliance in sin had catastrophic consequences.",
            "True intercession is costly and flows from genuine love for both God and people.",
            "Syncretism—mixing true worship with false religion—is as offensive to God as outright paganism.",
            "Sin always has consequences, even when immediate judgment is deferred by God's mercy.",
            "Faithfulness to God must sometimes take precedence over human loyalties, even family."
        ],
        "application": "In an age of instant gratification, Exodus 32 warns against manufacturing spiritual shortcuts when God seems silent or slow. We must resist substituting emotional experiences, human traditions, or cultural Christianity for genuine encounter with the living God. Like Moses, believers are called to intercessory prayer that appeals to God's character and promises. Leaders must never accommodate the crowd's spiritual demands when those demands run contrary to God's revealed will. We should examine what 'golden calves' we construct—status, comfort, entertainment, ideologies—that we subtly place in God's position.",
        "prayer": "Heavenly Father, forgive us for the times we have grown impatient with Your ways and sought visible substitutes for invisible faith. Guard us against all forms of idolatry, whether obvious or subtle. Raise up intercessors among us who will stand in the gap as Moses did, appealing to Your mercy and Your covenant faithfulness. May we, like the Levites, choose loyalty to You above all else. In Jesus's name, Amen.",
        "key_points": [
            "Israel's idolatry occurred at the very moment God was giving the law—contrasting divine faithfulness with human unfaithfulness.",
            "Aaron's leadership failure demonstrates how spiritual leaders can capitulate to popular pressure with devastating consequences.",
            "Moses's intercession is one of Scripture's greatest portraits of mediatorial prayer, pointing to Christ's own intercession.",
            "The shattering of the tablets dramatizes the covenant-breaking nature of Israel's sin.",
            "God's justice and mercy are both displayed: judgment falls on the unrepentant, while mercy is extended through intercession.",
            "Moses's offer to be blotted out for the people prefigures Christ's substitutionary atonement, though human atonement is ultimately insufficient."
        ],
        "study_questions": [
            "What motivated Israel to demand a golden calf, and what does this reveal about the human tendency toward idolatry when God seems distant or silent?",
            "How does Aaron's response to the people's demand illustrate the dangers of leadership that prioritizes peace over faithfulness?",
            "What elements of Moses's intercessory prayer (vv. 11-13) can serve as a model for our own prayers of intercession?",
            "Why do you think God invited Moses to intercede (v. 10) rather than simply declaring His judgment?",
            "How does the shattering of the tablets connect symbolically to what Israel had done in their relationship with God?",
            "Moses offered to be blotted from God's book for Israel's sake (v. 32). How does this prefigure Christ, and in what way does Christ's atonement surpass Moses's offer?",
            "In what ways do modern Christians construct 'golden calves'—substitutes for genuine relationship with God?"
        ],
        "tags": ["idolatry", "golden calf", "intercession", "covenant", "judgment", "Moses", "Aaron", "Levites", "atonement", "Exodus"],
        "sources": ["Exodus 32", "Romans 9:3", "Hebrews 7:25", "Romans 8:34", "1 Corinthians 10:7-8"]
    },
    {
        "book_id": 2,
        "book": "Exodus",
        "chapter": 33,
        "title": "The Presence of God: Moses's Boldest Prayer",
        "summary": "In the aftermath of the golden calf, God tells Israel He will send an angel but will not go with them personally, lest His holiness destroy them. The people mourn. Moses intercedes at the Tent of Meeting, speaking face to face with God as a friend. Moses makes his most audacious request—to see God's glory—and God promises His goodness will pass by while hiding Moses in the cleft of the rock.",
        "content": """Exodus 33 is a chapter of divine intimacy and profound theological depths. Following the catastrophe of Exodus 32, God and Israel must navigate the broken covenant, and the question at the center is: will God's presence remain with His people?

**The Withdrawal of Presence (vv. 1-6)**

God's first word after the golden calf incident is that He will still fulfill His land promise—sending an angel ahead—but He Himself will not go with them: "I will not go up among you, lest I consume you on the way, for you are a stiff-necked people" (v. 3). This threat is more terrifying than death. God's presence is simultaneously Israel's greatest privilege and greatest danger. The people's mourning (v. 4) at this news is theologically appropriate—they recognize that land without God's presence is worthless. The removal of their ornaments signals repentance, stripping away the symbols of the golden calf celebration.

**The Tent of Meeting: Communion Restored (vv. 7-11)**

Before the formal Tabernacle was built, Moses used a tent—called the "Tent of Meeting"—pitched outside the camp. This location "outside the camp" is significant: sin had created distance. Yet when Moses entered this tent, the pillar of cloud descended and the LORD spoke with Moses "face to face, as a man speaks to his friend" (v. 11). This phrase does not mean Moses literally saw God's face (cf. v. 20), but describes the quality of intimacy—direct, personal, unhidden communication. Joshua's lingering in the tent (v. 11) reveals his devotion to seeking God's presence.

**Moses's Audacious Intercession (vv. 12-17)**

Moses presses God in one of the most remarkable dialogues in Scripture. His argument for God's continued presence rests on three foundations: (1) God has commissioned him but not shown him whom He will send with him; (2) God's knowing Moses by name and finding favor with him implies ongoing relationship; (3) Israel is "Your people"—stressing covenant obligation. Moses's words are extraordinarily bold: "If your presence will not go with me, do not bring us up from here" (v. 15). He refuses the land without the Presence. This is the proper posture of faith—valuing God Himself above all His gifts. God relents and promises: "My presence will go with you, and I will give you rest" (v. 14). Moses pushes further: "What other nation has God so near to it?" (v. 16, paraphrase)—making God's presence the distinguishing mark of Israel.

**The Vision of Glory (vv. 18-23)**

Moses's boldest request: "Please show me your glory" (v. 18). God's answer is astonishing: He will cause His goodness to pass by and will proclaim His name. But the face of God—the full, direct, unmediated divine glory—"cannot be seen, for no one may see me and live" (v. 20). God places Moses in a "cleft of the rock" (v. 22), covers him with His hand, and allows Moses to see His "back"—His aftermath, the residue of glory. This passage teaches that God is simultaneously self-revealing and incomprehensible, accessible yet transcendent. The rock that sheltered Moses from divine glory points to Christ: "the rock was Christ" (1 Cor. 10:4), and it is in Christ—the cleft in God's revealed character—that we can behold divine glory without being destroyed.

**Christ in Exodus 33**

The entire chapter is a foreshadowing of the incarnation. In Christ, God's full presence comes to dwell among a sinful people without destroying them (John 1:14). The "face to face" friendship Moses enjoyed is now available to all believers through the Spirit (2 Cor. 3:18). Jesus is both the Mediator of God's presence and the "cleft of the rock" in which we stand safely to behold the Father's glory. The New Covenant surpasses the Old in this very point: Moses could only glimpse the back of God's glory, but we "behold the glory of God in the face of Jesus Christ" (2 Cor. 4:6).""",
        "chapter_overview": "God threatens to withdraw His presence; the Tent of Meeting is established outside the camp; Moses intercedes for God's presence; Moses asks to see God's glory; God promises to show His goodness while hiding Moses in the rock's cleft.",
        "original_language_notes": [
            {
                "term": "כָּבוֹד (kavod)",
                "language": "Hebrew",
                "verse": "33:18",
                "words_used": ["glory"],
                "meaning": "Weighty, heavy, honor, glory. Moses requests to see God's kavod—His manifest presence and splendor. The word suggests something of immense weight and substance. God distinguishes between His kavod and His goodness (v. 19), suggesting that the full, unmediated kavod is beyond human capacity to endure."
            },
            {
                "term": "פָּנִים (panim)",
                "language": "Hebrew",
                "verse": "33:11",
                "words_used": ["face", "face to face"],
                "meaning": "Face, presence, surface. 'Panim el-panim' (face to face) describes the directness and intimacy of Moses's encounter with God. This is relational language, contrasted with v. 20 where God says no one can see His face (panim) and live—the paradox of intimate yet veiled divine communication."
            },
            {
                "term": "חֵן (chen)",
                "language": "Hebrew",
                "verse": "33:13",
                "words_used": ["favor", "grace"],
                "meaning": "Grace, favor, charm. Moses repeatedly appeals to having found 'chen' in God's eyes. This is unmerited divine favor—the same Hebrew root underlying God's gracious character. Moses's access to God is entirely based on grace, not merit."
            },
            {
                "term": "נָחַם (nacham)",
                "language": "Hebrew",
                "verse": "33:14",
                "words_used": ["rest", "give you rest"],
                "meaning": "Rest, comfort, relief. The promise of 'rest' (menucha) in v. 14 is more than physical rest—it is the rest that comes from being in the presence of God Himself, anticipating the Sabbath rest and ultimately the eschatological rest of Hebrews 4."
            },
            {
                "term": "טוּב (tuv)",
                "language": "Hebrew",
                "verse": "33:19",
                "words_used": ["goodness"],
                "meaning": "Goodness, beauty, the good. God promises to make all His 'goodness' (tuv) pass before Moses—His essential moral perfection and beneficent character—even as the full glory (kavod) remains inaccessible. The proclamation of the divine name that follows (34:6-7) is the verbal equivalent of this 'goodness' passing by."
            }
        ],
        "moral_lessons": [
            "The presence of God is more valuable than any material blessing, including the Promised Land.",
            "True friendship with God is possible—Scripture models a bold, honest, intimate communion with God.",
            "Sin creates distance from God, but repentance and intercession can restore relationship.",
            "God is simultaneously approachable and transcendent; holy reverence and intimate friendship are not opposites.",
            "God's grace (chen) is the only basis for any human to seek or receive divine favor.",
            "Boldness in prayer, grounded in God's promises and character, honors God rather than dishonoring Him."
        ],
        "application": "Exodus 33 calls every believer to make God's presence the supreme priority. In a results-oriented culture that values what God gives over God Himself, Moses models a radical reorientation: 'If You don't go with us, don't send us.' This is a prayer every believer should make their own. We should pursue the 'face to face' intimacy with God that Moses knew—through Scripture, prayer, and the Spirit—not settling for impersonal religion or secondhand faith. The cleft of the rock is available to us in Christ: we can behold God's glory without being consumed.",
        "prayer": "Lord, above all else, let Your presence go with us. We refuse to journey anywhere without You. Like Moses, we ask boldly: show us Your glory. Hide us in Christ, the Rock, and let Your goodness pass over us. May we never be satisfied with religion without relationship, with Your gifts without Yourself. Teach us what it means to speak with You as a friend speaks to a friend. In Jesus's name, Amen.",
        "key_points": [
            "God's threatened withdrawal of His presence was more terrifying to Moses than any military threat or natural disaster.",
            "The Tent of Meeting outside the camp illustrates how sin creates distance from God, requiring a mediator.",
            "Moses's 'face to face' communication with God describes relational intimacy, not literal vision of God's physical face.",
            "Moses's boldest intercession demands God's presence over the Promised Land itself, setting a model for all prayer.",
            "God's willingness to show His 'goodness' while concealing His full glory balances divine transcendence with divine self-revelation.",
            "The cleft of the rock points to Christ as our shelter from the consuming holiness of God."
        ],
        "study_questions": [
            "Why did God threaten to withdraw His presence rather than simply destroy the people after the golden calf?",
            "What does Moses's refusal to proceed without God's presence (v. 15) reveal about his values and theology?",
            "How does the Tent of Meeting being 'outside the camp' reflect the spiritual condition of Israel at this moment?",
            "What is the difference between seeing God's 'face' and seeing His 'back' (vv. 20, 23)? What theological truth does this distinction convey?",
            "Moses's request to see God's glory was audacious. What gave him the confidence to make such a request?",
            "How does Paul's use of this chapter in 2 Corinthians 3-4 show how the New Covenant surpasses the Old in terms of access to God's glory?",
            "What 'promised lands'—good things God has given or promised—are we tempted to pursue without insisting on God's presence?"
        ],
        "tags": ["presence of God", "glory", "intercession", "Moses", "Tent of Meeting", "prayer", "covenant", "theophany", "grace", "Exodus"],
        "sources": ["Exodus 33", "2 Corinthians 3:18", "2 Corinthians 4:6", "John 1:14", "1 Corinthians 10:4", "Hebrews 4:9-10"]
    },
    {
        "book_id": 2,
        "book": "Exodus",
        "chapter": 34,
        "title": "The Renewal of the Covenant: God's Name Proclaimed",
        "summary": "God instructs Moses to cut two new stone tablets. On Sinai, God proclaims His name and character—the foundational self-revelation of Yahweh in all of Scripture. Moses intercedes and God renews the covenant with Israel, giving renewed commandments. Moses's face shines with reflected glory when he descends, and he veils himself before the people.",
        "content": """Exodus 34 contains one of the most theologically rich passages in all of Scripture: God's own self-proclamation of His name and character in verses 6-7. This is the anchor point of Israel's theology—a text quoted, alluded to, or echoed more than any other Old Testament passage.

**The Second Tablets (vv. 1-4)**

The second set of stone tablets marks a remarkable act of divine grace. Israel had shattered the covenant; God chose to restore it. Moses must cut the tablets himself this time—perhaps indicating that renewal requires human participation—but the writing on them will again be God's own. The preparation mirrors Sinai's first theophany: rising early, ascending alone, with no one else present.

**The Divine Name Proclaimed (vv. 5-7)**

As the cloud descends and God passes before Moses, He proclaims: "The LORD, the LORD, a God merciful and gracious, slow to anger, and abounding in steadfast love and faithfulness, keeping steadfast love for thousands, forgiving iniquity and transgression and sin, but who will by no means clear the guilty, visiting the iniquity of the fathers on the children and the children's children, to the third and the fourth generation" (vv. 6-7).

This proclamation—often called the "Thirteen Attributes" in Jewish tradition—is not abstract theology but God's own autobiography. Every attribute is relational:

- **Merciful (rachum)**: Derived from rechem (womb), conveying tender, motherly compassion.
- **Gracious (channun)**: Giving favor to those who have no claim to it.
- **Slow to anger (erekh apayim)**: Literally "long of nose"—patience that takes long to exhaust.
- **Abounding in steadfast love (chesed)**: Covenant loyalty; faithful, enduring love that goes beyond what is owed.
- **Faithfulness (emet)**: Truth, reliability, constancy.
- **Keeping steadfast love for thousands**: God's love extends generationally, disproportionately to His judgment.
- **Forgiving iniquity, transgression, and sin**: Three Hebrew words covering the full spectrum of wrongdoing—guilt, rebellion, and moral failure.
- **Not clearing the guilty**: Divine mercy does not abolish divine justice; forgiveness is not universalism.

This passage is quoted or echoed in Numbers 14:18, Nehemiah 9:17, Psalms 86:15, 103:8, 145:8, Joel 2:13, Jonah 4:2, Nahum 1:3, and many more—demonstrating its foundational importance across the entire canon.

**Moses's Intercession and Covenant Renewal (vv. 8-28)**

Moses immediately worships and intercedes: "Please go with us, even though this is a stiff-necked people, and pardon our iniquity and our sin, and take us for your inheritance" (v. 9). He appeals to exactly those attributes God just proclaimed. God renews the covenant, emphasizing the prohibition of idolatry and intermarriage with Canaanites, the sanctity of Sabbath, the festival calendar, and the offering of firstborn animals. The "Ten Commandments" (v. 28) here likely refers to this renewed covenant summary.

**The Radiant Face of Moses (vv. 29-35)**

When Moses descends from Sinai, his face shines (qaran)—literally "emits rays"—because he had been speaking with God. He is unaware of this transformation. Aaron and the people are afraid to approach him. This glory is temporary and external—Moses veils himself when not communicating God's words. Paul meditates on this contrast in 2 Corinthians 3, arguing that Moses veiled the fading glory, while the New Covenant imparts an increasing, unveiled glory through the Spirit. The Law's glory was real but transitional; Christ's glory is permanent and transforming.

**Christ in Exodus 34**

The divine attributes proclaimed in 34:6-7 find their fullest expression in Jesus Christ. John 1:14 echoes the exact terms: "the Word became flesh…full of grace (chen) and truth (emet)." In Christ, both the mercy and the justice of God are fully displayed: He "did not clear the guilty" (v. 7) but bore the full penalty as a substitute, so that sinners could be fully forgiven without God's justice being violated (Romans 3:25-26). The renewed covenant of Exodus 34 anticipates the New Covenant in Christ's blood (Luke 22:20).""",
        "chapter_overview": "God calls Moses to cut new tablets; God proclaims His thirteen attributes of grace and justice; Moses intercedes; covenant renewed with festivals, Sabbath, and prohibition of idolatry; Moses's face shines with divine glory.",
        "original_language_notes": [
            {
                "term": "חֶסֶד (chesed)",
                "language": "Hebrew",
                "verse": "34:6",
                "words_used": ["steadfast love", "lovingkindness", "mercy"],
                "meaning": "Covenant loyalty, steadfast love, faithful kindness. Chesed is one of the most theologically rich Hebrew words, denoting love that goes beyond what is contractually required—God's persistent, faithful commitment to His covenant people even when they are faithless. It occurs twice in v. 6-7, emphasizing its centrality to God's character."
            },
            {
                "term": "רַחוּם (rachum)",
                "language": "Hebrew",
                "verse": "34:6",
                "words_used": ["merciful", "compassionate"],
                "meaning": "Compassionate, merciful. Derived from rechem (womb), this word carries connotations of tender, instinctive, maternal compassion—the feeling a mother has for the child of her womb. God's mercy toward Israel is described with this intimate, visceral word."
            },
            {
                "term": "אֱמֶת (emet)",
                "language": "Hebrew",
                "verse": "34:6",
                "words_used": ["faithfulness", "truth"],
                "meaning": "Truth, faithfulness, reliability, constancy. Paired with chesed throughout the Old Testament (as in v. 6), emet describes God's unwavering consistency and reliability. John 1:14's 'grace and truth' is a deliberate echo of chesed and emet—the New Testament sees Christ as the fullest expression of these divine attributes."
            },
            {
                "term": "קָרַן (qaran)",
                "language": "Hebrew",
                "verse": "34:29",
                "words_used": ["shone", "radiant", "rays"],
                "meaning": "To emit rays, to shine, to have horns of light. Moses's face 'shone' (qaran) with reflected divine glory—a physical manifestation of his time in God's presence. The word's association with 'horns' (qeren) led Jerome's Vulgate to translate it as Moses having horns, resulting in Michelangelo's famous (if mistaken) horned Moses sculpture."
            },
            {
                "term": "נָקֵה (naqeh)",
                "language": "Hebrew",
                "verse": "34:7",
                "words_used": ["clear", "innocent", "unpunished"],
                "meaning": "To be clean, innocent, exempt from punishment. The declaration that God 'will by no means clear the guilty' (lo-yenaqeh lo-yenaqeh—emphatic double negative) establishes that divine forgiveness does not negate divine justice. Both mercy and justice are fully expressed in God's character."
            }
        ],
        "moral_lessons": [
            "God's grace is greater than human sin—the renewal of the covenant after the golden calf is pure divine initiative.",
            "Knowing God's character (34:6-7) is the foundation of all true prayer, worship, and theology.",
            "God's forgiveness is real but not cheap: He forgives iniquity while also not clearing the guilty without atonement.",
            "Prolonged time in God's presence transforms us—Moses's shining face is a pattern for all believers.",
            "Intermarriage and entanglement with idolatry are dangers God takes seriously, threatening the purity of covenant faith.",
            "Covenant renewal after failure is possible through the grace of a merciful God."
        ],
        "application": "Exodus 34:6-7 is the theological foundation every believer should memorize and return to when doubt, discouragement, or a distorted view of God's character threatens. When we are tempted to think God is harsh, distant, or quick to condemn, we return to His own self-proclamation: He is merciful, gracious, slow to anger, abounding in steadfast love. When we are tempted to take His forgiveness lightly, we remember He will not clear the guilty—His justice is as real as His mercy. Christ satisfies both, making the New Covenant possible. We should also note Moses's glowing face as a challenge: How often do we spend enough time in God's presence that it visibly transforms us?",
        "prayer": "LORD, You proclaimed Your name to Moses, and we receive it: You are merciful, gracious, slow to anger, abounding in steadfast love and faithfulness. Forgive our iniquity, transgression, and sin. Renew the covenant that we so often break through faithlessness. Let our faces too reflect something of Your glory as we spend time in Your presence. May we know You not as we imagine You, but as You have revealed Yourself. In Jesus's name, who is full of grace and truth, Amen.",
        "key_points": [
            "God's self-proclamation in vv. 6-7 is the most cited theological statement in the entire Old Testament.",
            "The renewal of covenant after the golden calf demonstrates that God's grace overcomes human faithlessness.",
            "God's character holds both mercy and justice in perfect balance—forgiveness is real, but it does not violate justice.",
            "Moses's shining face demonstrates that proximity to God transforms the one who draws near.",
            "The renewed covenant emphases (Sabbath, festivals, firstborn) reinforce Israel's distinct identity as a covenant people.",
            "Christ is the fullest expression of chesed and emet—grace and truth—making complete covenant renewal possible."
        ],
        "study_questions": [
            "Why do you think God commanded Moses to cut the new tablets himself, while God wrote on them? What does this division of labor suggest about covenant renewal?",
            "Study each attribute in 34:6-7. Which attribute do you find most surprising or most personally significant, and why?",
            "How does God's statement that He 'will by no means clear the guilty' relate to His mercy and forgiveness? Are these in tension?",
            "The covenant renewal in chapter 34 emphasizes worship practices, festivals, and Sabbath. Why do these external practices matter so much to God?",
            "What is the significance of Moses's face shining without his knowledge (v. 29)? What does this suggest about authentic transformation?",
            "Paul contrasts the fading glory of Moses's face with the increasing glory of New Covenant believers (2 Cor. 3). What does this contrast reveal about the difference between law and grace?",
            "If 34:6-7 is God's own self-description, how should this shape your prayers and your understanding of His character?"
        ],
        "tags": ["covenant renewal", "divine attributes", "glory", "Moses", "chesed", "grace", "justice", "theophany", "law", "Exodus"],
        "sources": ["Exodus 34", "2 Corinthians 3:7-18", "John 1:14", "Romans 3:25-26", "Numbers 14:18", "Psalms 86:15", "Joel 2:13"]
    },
    {
        "book_id": 2,
        "book": "Exodus",
        "chapter": 35,
        "title": "Willing Hearts: Sabbath, Offerings, and the Call to Build",
        "summary": "Moses convenes Israel and reiterates the Sabbath law, then calls for freewill offerings for the Tabernacle. The people respond with willing hearts and generosity, bringing gold, silver, bronze, fine fabrics, animal skins, oil, spices, and precious stones. The craftsmen Bezalel and Oholiab are identified as Spirit-filled builders, and the people are summoned to participate in the Tabernacle's construction.",
        "content": """After the catastrophe of the golden calf and the gracious renewal of the covenant, Exodus 35 marks a new beginning—Israel's joyful, willing participation in building a dwelling place for the God who had restored His presence among them. The chapter is a study in contrast: the corrupt generosity of chapter 32 (bringing gold for an idol) versus the Spirit-led generosity of chapter 35 (bringing gold for the Tabernacle).

**The Sabbath Reminder (vv. 1-3)**

Before the call to build, Moses repeats the Sabbath commandment. This placement is deliberate and theologically significant. Even the urgency of building God's house does not override the rhythm of rest He has ordained. The prohibition of fire on the Sabbath (v. 3) is the strictest application—even cooking fire must wait. The Sabbath frames the entire Tabernacle project: the work of worship is bounded by the worship of rest.

**The Call for Freewill Offerings (vv. 4-19)**

Moses calls for contributions from "everyone whose heart moves him" (v. 5). The list of required materials is extensive: gold, silver, bronze, blue/purple/scarlet yarn, fine linen, goat hair, ram skins, acacia wood, olive oil, spices, and precious gemstones. The breadth of materials reflects how God's dwelling among His people requires the whole range of creation's resources—nothing is too common or too precious.

**The Generous Response (vv. 20-29)**

The people's response is extraordinary. They return to their tents and bring what moves their hearts. The repetition of the phrase "everyone whose heart stirred him" and "everyone whose spirit moved him" (vv. 21, 26, 29) emphasizes that this giving was entirely voluntary—not coerced, not taxed, but freely offered out of love and gratitude for God's restored presence. Both men and women participated equally (v. 22, 25-26). Skill and material resources were both offered. This is the generosity that flows naturally from a heart that has been forgiven and restored.

**Bezalel and Oholiab: Spirit-Filled Artisans (vv. 30-35)**

Moses identifies Bezalel son of Uri and Oholiab son of Ahisamach as the lead craftsmen—men whom God has "filled…with the Spirit of God, with skill, with intelligence, with knowledge, and with all craftsmanship" (v. 31). This is a remarkable passage: the first individual explicitly said to be "filled with the Spirit of God" in Scripture is an artist. This challenges any sacred/secular divide. God's Spirit is not limited to prophets and priests; He equips craftsmen, designers, and builders with Spirit-empowered excellence. The gifting of Bezalel covers design, engraving, weaving, embroidery—every form of artistic and technical skill needed to create the Tabernacle.

**Christ in Exodus 35**

The Tabernacle itself—the structure being built in chapters 35-40—is a type of Christ. As the Tabernacle was God's dwelling among Israel, Christ is "Immanuel, God with us" (Matthew 1:23; John 1:14). The freewill offering of the people parallels the willing sacrifice of Christ: "I lay down my life…No one takes it from me, but I lay it down of my own accord" (John 10:17-18). The Spirit-empowered artistry of Bezalel points to the Spirit's role in the New Testament community, where all believers are gifted for the building of God's new temple—the Church (1 Corinthians 3:16; Ephesians 2:21-22).""",
        "chapter_overview": "Sabbath reaffirmed before Tabernacle construction; freewill offerings called for; people respond with willing hearts and generous gifts; Bezalel and Oholiab identified as Spirit-filled craftsmen.",
        "original_language_notes": [
            {
                "term": "נְדִיבָה (nedivah)",
                "language": "Hebrew",
                "verse": "35:22",
                "words_used": ["willing", "freewill", "generous"],
                "meaning": "Willingness, nobility, generosity. The freewill offering described here is a nedavah—a voluntary, spontaneous gift. The root implies a noble generosity that is not compelled. True giving to God flows from a grateful, transformed heart, not obligation."
            },
            {
                "term": "לֵב (lev)",
                "language": "Hebrew",
                "verse": "35:5",
                "words_used": ["heart"],
                "meaning": "Heart, mind, will, the center of the person. The repeated phrase 'everyone whose heart moves him' (nadav libbo) emphasizes that authentic participation in God's purposes flows from the innermost person. The Tabernacle was to be built by willing hearts, not compulsory labor—anticipating the New Testament principle that 'God loves a cheerful giver' (2 Cor. 9:7)."
            },
            {
                "term": "רוּחַ (ruach)",
                "language": "Hebrew",
                "verse": "35:31",
                "words_used": ["Spirit", "spirit"],
                "meaning": "Spirit, wind, breath. The filling of Bezalel with the ruach Elohim (Spirit of God) is the same language used of creation (Gen. 1:2) and prophecy. God's Spirit is the agent of all creative excellence, not merely spiritual gifts—a foundation for Christian engagement with art, craft, and skilled labor."
            },
            {
                "term": "חׇכְמָה (chokmah)",
                "language": "Hebrew",
                "verse": "35:31",
                "words_used": ["skill", "wisdom"],
                "meaning": "Wisdom, skill, expertise. Chokmah encompasses both intellectual wisdom and practical skill—the ability to apply knowledge effectively. God fills Bezalel with chokmah for craftsmanship, indicating that technical skill in service of God's purposes is a form of Spirit-endowed wisdom."
            },
            {
                "term": "שַׁבָּת (shabbat)",
                "language": "Hebrew",
                "verse": "35:2",
                "words_used": ["Sabbath", "rest"],
                "meaning": "Cessation, rest, Sabbath. The reiteration of shabbat before Tabernacle construction signals that even the holiest human project must yield to the divine rhythm of rest. Shabbat is not merely a day off—it is a declaration that God, not human productivity, sustains life and accomplishes His purposes."
            }
        ],
        "moral_lessons": [
            "Genuine gratitude for God's grace produces voluntary, joyful generosity—not reluctant obligation.",
            "No category of skill or gift is secular: Spirit-filled artistry is as honored as prophecy or priestly service.",
            "The Sabbath limits even the most worthy projects, reminding us that rest is not laziness but covenant faithfulness.",
            "Both men and women are called to participate in building God's community and worship.",
            "Generosity in giving to God is a form of worship that reflects the condition of the heart.",
            "God equips those He calls—Bezalel's gifting was specifically matched to the task assigned."
        ],
        "application": "Exodus 35 challenges the church to foster a culture of 'willing heart' giving—of time, talent, and treasure—not merely for institutional maintenance but for genuine dwelling-place-of-God purposes. Every believer's skills, whether carpentry, accounting, technology, music, or design, can be Spirit-empowered offerings for God's purposes. The Sabbath principle reminds us not to sacrifice rest on the altar of even worthy ministry. We should ask: What has God equipped me to offer for the building of His community? And: Do I give from a heart moved by grace, or from a sense of obligation?",
        "prayer": "Lord, move our hearts to give willingly—our time, our skills, our resources—for the building of Your kingdom. As You filled Bezalel with Your Spirit for craftsmanship, fill us with Your Spirit for every task to which You call us. Remind us that no gift is too small and no skill too ordinary to offer in Your service. And teach us the grace of Sabbath—that we might rest as those who trust that You hold all things. In Jesus's name, Amen.",
        "key_points": [
            "The Sabbath commandment prefacing the Tabernacle project establishes that God's work must be done in God's rhythm, not human productivity.",
            "The freewill offering emphasizes that God desires willing, heart-motivated giving, not coerced or routine contributions.",
            "The people's generous response stands in sharp contrast to their corrupt generosity with the golden calf—restored relationship produces right worship.",
            "Bezalel is the first person in Scripture explicitly described as filled with the Spirit of God—and he is an artist/craftsman.",
            "The Spirit equips for all kinds of excellence, not only spiritual gifts—challenging sacred/secular divisions.",
            "The Tabernacle being built is a type of Christ, God's ultimate dwelling among humanity."
        ],
        "study_questions": [
            "Why do you think Moses reiterates the Sabbath command (vv. 1-3) immediately before calling for Tabernacle contributions? What principle does this establish?",
            "The chapter emphasizes 'willing hearts' multiple times. What are the conditions that produce willing, generous hearts toward God?",
            "How does the people's offering in chapter 35 contrast with their 'offering' for the golden calf in chapter 32? What made the difference?",
            "Bezalel is the first person said to be 'filled with the Spirit of God' in Scripture. What does this teach us about how the Spirit works in the world?",
            "How does the principle of Spirit-empowered craftsmanship apply to your own vocation and skill set?",
            "What types of 'freewill offerings' does the New Testament call believers to make (Romans 12:1-2; 2 Corinthians 9:7)?",
            "If the Tabernacle is a type of the Church as God's dwelling place (1 Cor. 3:16; Eph. 2:21-22), what does Exodus 35 teach about how the Church should be built?"
        ],
        "tags": ["Tabernacle", "generosity", "freewill offering", "Sabbath", "Bezalel", "Holy Spirit", "worship", "craftsmanship", "giving", "Exodus"],
        "sources": ["Exodus 35", "2 Corinthians 9:7", "1 Corinthians 3:16", "Ephesians 2:21-22", "John 10:17-18", "Romans 12:1"]
    },
    {
        "book_id": 2,
        "book": "Exodus",
        "chapter": 36,
        "title": "Overflowing Generosity and the Construction Begins",
        "summary": "Bezalel, Oholiab, and skilled craftsmen begin work on the Tabernacle using the freewill offerings. The gifts pour in so abundantly that Moses must command the people to stop bringing more—there is more than enough. The craftsmen begin with the curtains and coverings of the Tabernacle, crafting the ten linen curtains, the goat-hair coverings, and the frames with silver bases.",
        "content": """Exodus 36 opens a remarkable section: the actual construction of the Tabernacle, narrated in detail that mirrors the instructions given in chapters 25-31. This repetition is not careless editing—it is theological. The telling and the doing frame the Tabernacle as a wholly God-directed project, from divine specification to human execution.

**Overflowing Generosity (vv. 1-7)**

The chapter begins with Bezalel and Oholiab taking up the work with all the skilled craftsmen. The people's generosity from chapter 35 proves overwhelming: "The people bring much more than enough for doing the work that the LORD has commanded us to do" (v. 5). Moses is compelled to issue a unique prohibition in all of Scripture—a command to stop giving: "Let no man or woman do anything more for the contribution for the sanctuary" (v. 6). So the people were restrained from bringing more!

This is extraordinary. In the aftermath of the golden calf, the same people who had stripped off their gold for an idol now give so abundantly for God's Tabernacle that they must be told to stop. This transformation illustrates what genuine repentance and covenant renewal produces: extravagant, overflowing worship. The "more than enough" (Hebrew: yeter) stands as a witness to the grace that had been poured out on Israel.

**The Curtains and Coverings (vv. 8-19)**

The craftsmen begin with the structure's interior: ten fine linen curtains (v. 8-13), blue-purple-scarlet with cherubim woven in—matching exactly the divine specifications of chapter 26. The curtains were coupled with fifty clasps of gold. Over these, eleven curtains of goat hair formed the tent covering (vv. 14-18), joined with fifty bronze clasps. Finally, ram skin coverings dyed red and dolphin/dugong skin coverings were added as the outermost protection (v. 19).

This layered structure is highly symbolic: the innermost curtains, visible only to priests, were the most beautiful—fine linen with cherubim. The outer coverings were plain and weather-resistant. What is holy is often hidden from casual view; the beauty of God's presence is reserved for those who draw near in worship.

**The Frames and Sockets (vv. 20-34)**

The acacia-wood frames (qeresh—planks or frames) stood upright, overlaid with gold, set into silver sockets (adonim—bases or pedestals). The silver sockets were cast from the half-shekel atonement money given in the census (Exodus 30:11-16; 38:27)—so the very foundation of the Tabernacle rested on atonement. This is a profound architectural theology: the dwelling place of God among His people is built on redemption money, on the cost of atonement.

**Bars and Framework (vv. 31-34)**

Five bars of acacia wood overlaid with gold ran through rings on each frame, holding the structure together. The middle bar ran from end to end—structurally central, hidden within the frames. The physical solidity of the Tabernacle reflects the theological solidity of God's covenant—everything connected, held together, sustained by divine order.

**Christ in Exodus 36**

The Tabernacle's construction as a whole is a rich type of Christ. The layered coverings—most beautiful inside, utilitarian outside—reflect Christ's incarnation: divinity hidden within human flesh (Isaiah 53:2; John 1:14). The silver-socket foundation of atonement money anticipates Christ as the foundation of the Church (1 Corinthians 3:11), and the "more than enough" generosity of the people echoes Paul's declaration that in Christ, grace has "abounded all the more" (Romans 5:20). The willing labor of the craftsmen mirrors the willing obedience of the Son who came to do His Father's will (John 6:38).""",
        "chapter_overview": "Bezalel and Oholiab begin Tabernacle construction; people give so abundantly Moses commands them to stop; ten linen curtains and goat-hair covering made; acacia frames with silver-socket foundations constructed.",
        "original_language_notes": [
            {
                "term": "יֶתֶר (yeter)",
                "language": "Hebrew",
                "verse": "36:5",
                "words_used": ["more than enough", "too much", "surplus"],
                "meaning": "Remainder, surplus, excess. The declaration that the people had brought yeter—more than enough—marks one of Scripture's most remarkable moments of communal generosity. This abundance testifies to genuine heart-transformation following the golden calf catastrophe."
            },
            {
                "term": "קֶרֶשׁ (qeresh)",
                "language": "Hebrew",
                "verse": "36:20",
                "words_used": ["frames", "boards", "planks"],
                "meaning": "Frame, plank, board. Scholars debate whether the qeresh were solid planks or open frames. Most modern scholarship favors a lattice-frame structure that would have been lighter and more transportable for a nomadic people. The precision of their construction—identical dimensions, gold overlay—reflects the Tabernacle's divine specification."
            },
            {
                "term": "אֶדֶן (eden)",
                "language": "Hebrew",
                "verse": "36:26",
                "words_used": ["socket", "base", "pedestal"],
                "meaning": "Base, socket, foundation. Each frame required two silver adonim (sockets/bases) into which the tenons of the frame were inserted. The same Hebrew root relates to 'adon' (lord, master)—the bases were both structural foundations and symbolic submissions to divine lordship."
            },
            {
                "term": "בְּרִיחַ (beriyach)",
                "language": "Hebrew",
                "verse": "36:31",
                "words_used": ["bar", "crossbar"],
                "meaning": "Bar, crossbar, bolt. The beriachim (bars) running horizontally through the frames held the entire structure together. The middle bar's spanning of the full length (v. 33) provided structural integrity—a physical image of the unifying center that holds God's house together."
            },
            {
                "term": "כְּרוּב (keruv)",
                "language": "Hebrew",
                "verse": "36:8",
                "words_used": ["cherubim"],
                "meaning": "Cherub (plural: cherubim). Winged divine beings associated with the presence of God, first appearing as guardians of Eden (Gen. 3:24). The cherubim woven into the innermost curtains place worshippers symbolically in the heavenly throne room—the Tabernacle as a portable Eden, God's presence re-established among His people."
            }
        ],
        "moral_lessons": [
            "Transformed hearts produce overflowing generosity—Israel's 'too much' giving contrasts their earlier corrupt giving for the golden calf.",
            "The most beautiful things in God's design are often hidden from casual observers—interior beauty is for those who draw near.",
            "God's house is built on atonement—the silver sockets from redemption money establish that God's dwelling among us rests entirely on His redemptive work.",
            "Willing, skilled labor offered to God is a form of worship equally honoring as prayer or sacrifice.",
            "The precision of the craftsmen—following God's exact specifications—models the believer's call to faithful obedience.",
            "When God's people are genuinely moved by His grace, they give more than enough—generosity becomes a problem of abundance rather than scarcity."
        ],
        "application": "The 'more than enough' of Exodus 36 is a challenge and a hope for the contemporary church. It suggests that when people genuinely encounter God's grace and renewal, the natural result is lavish, willing giving—of time, skill, and resources—not reluctant compliance. Churches experiencing spiritual renewal should not struggle for resources; they should struggle to direct abundant offerings wisely. On a personal level, we should ask: Is my giving a reflection of a heart moved by God's grace? And we can take encouragement from the silver-socket foundation: everything that holds God's people together rests not on our contributions but on the atonement Christ has already accomplished.",
        "prayer": "Lord, may we be a people whose giving testifies to genuine transformation by Your grace. May Your house—Your people—be built with the willing labor and generous offering of those who have encountered Your mercy. Thank You that the foundation is not our generosity but Your atonement, accomplished fully in Christ. Let what we build together reflect Your specifications, Your beauty, and Your order. In Jesus's name, Amen.",
        "key_points": [
            "The 'more than enough' giving of Israel after the golden calf demonstrates the transforming power of forgiveness and covenant renewal.",
            "Moses commanding the people to stop giving is unique in Scripture—a powerful testimony to the depth of their changed hearts.",
            "The layered Tabernacle coverings—beautiful inside, plain outside—reflect a theological pattern: divine beauty revealed to those who draw near.",
            "The silver sockets—made from atonement money—establish that the Tabernacle's foundation is redemption, not human achievement.",
            "The careful mirroring of divine specifications in human execution models the faithful obedience God desires.",
            "The Tabernacle's construction is a type of the Church built on Christ as foundation (1 Cor. 3:11)."
        ],
        "study_questions": [
            "What is the significance of Moses having to tell the people to stop giving (vv. 5-7)? What does this 'problem of abundance' reveal about the people's heart condition?",
            "How does the overflowing generosity of Exodus 36 contrast with the people's gold-giving in Exodus 32? What produced the difference?",
            "The innermost curtains were most beautifully crafted but hidden from most people's view. What theological principle does this hidden beauty illustrate?",
            "The silver sockets were made from the atonement money of the census (Exod. 30). What does it mean theologically that the Tabernacle's foundation rests on atonement?",
            "The craftsmen follow God's specifications exactly, with no recorded deviation. Why is this precision important for worship?",
            "How does Paul's statement that in Christ 'grace abounded all the more' (Romans 5:20) resonate with the 'more than enough' generosity of Exodus 36?",
            "If the Tabernacle is a type of the Church (Eph. 2:20-22), what principles from its construction should guide how we build Christian community today?"
        ],
        "tags": ["Tabernacle", "generosity", "construction", "Bezalel", "atonement", "Sabbath", "worship", "craftsmanship", "offerings", "Exodus"],
        "sources": ["Exodus 36", "Romans 5:20", "1 Corinthians 3:11", "1 Corinthians 3:16", "Ephesians 2:20-22", "Exodus 30:11-16"]
    }
]


def get_or_create_collection(cur):
    cur.execute("SELECT id FROM commentary_collections WHERE slug=?", (COLLECTION_SLUG,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        "INSERT INTO commentary_collections (name, slug, language_code, theological_perspective, created_at, updated_at) VALUES (?,?,?,?,?,?)",
        (COLLECTION_NAME, COLLECTION_SLUG, LANGUAGE_CODE, THEOLOGICAL_PERSPECTIVE, NOW, NOW)
    )
    return cur.lastrowid


def chapter_exists(cur, collection_id, book_id, chapter):
    cur.execute(
        """SELECT id, content FROM commentary_entries
           WHERE collection_id=? AND book_id=? AND chapter=? AND language_code=?
             AND reference_scope='chapter' AND deleted_at IS NULL""",
        (collection_id, book_id, chapter, LANGUAGE_CODE)
    )
    row = cur.fetchone()
    if not row:
        return False
    content = row[1] or ""
    return len(content) > 200


def insert_chapter(cur, collection_id, ch_data):
    entry_uuid = str(uuid.uuid4())
    word_count = len(ch_data["content"].split())
    cur.execute(
        """INSERT INTO commentary_entries
           (uuid, collection_id, book_id, chapter, verse_start, verse_end, reference_scope,
            title, summary, content, application, prayer,
            key_points, study_questions, language_code, theological_perspective, status,
            is_ai_generated, ai_generation_batch_uuid, word_count,
            created_at, updated_at)
           VALUES (?,?,?,?,NULL,NULL,?,?,?,?,?,?,?,?,?,?,?,1,?,?,?,?)""",
        (
            entry_uuid, collection_id, ch_data["book_id"], ch_data["chapter"], "chapter",
            ch_data["title"], ch_data["summary"], ch_data["content"],
            ch_data["application"], ch_data["prayer"],
            json.dumps(ch_data["key_points"]),
            json.dumps(ch_data["study_questions"]),
            LANGUAGE_CODE, THEOLOGICAL_PERSPECTIVE, STATUS,
            BATCH_ID, word_count, NOW, NOW
        )
    )
    return entry_uuid


def save_json(ch_data, entry_uuid):
    book_dir = f"{ch_data['book_id']:02d}-{ch_data['book'].lower().replace(' ', '-')}"
    dir_path = os.path.join(GENERATED_DIR, book_dir)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, f"{ch_data['chapter']:02d}.json")

    record = {
        "uuid": entry_uuid,
        "collection_name": COLLECTION_NAME,
        "author_type": AUTHOR_TYPE,
        "language_code": LANGUAGE_CODE,
        "theological_perspective": THEOLOGICAL_PERSPECTIVE,
        "status": STATUS,
        "book_id": ch_data["book_id"],
        "book": ch_data["book"],
        "chapter": ch_data["chapter"],
        "title": ch_data["title"],
        "summary": ch_data["summary"],
        "content": ch_data["content"],
        "chapter_overview": ch_data["chapter_overview"],
        "original_language_notes": ch_data["original_language_notes"],
        "moral_lessons": ch_data["moral_lessons"],
        "application": ch_data["application"],
        "prayer": ch_data["prayer"],
        "key_points": ch_data["key_points"],
        "study_questions": ch_data["study_questions"],
        "tags": ch_data["tags"],
        "sources": ch_data["sources"],
        "created_at": NOW,
        "updated_at": NOW,
    }
    # Verify no forbidden keys
    forbidden = {"is_ai_generated", "model_name", "prompt_version"}
    assert not forbidden.intersection(record.keys()), f"Forbidden keys found: {forbidden.intersection(record.keys())}"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    # Verify it parses back
    with open(file_path, "r", encoding="utf-8") as f:
        parsed = json.load(f)
    assert not forbidden.intersection(parsed.keys())
    return file_path


def update_progress(last_book_id, last_book, last_chapter, next_book_id, next_book, next_chapter, completed):
    progress = {
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
        json.dump(progress, f, indent=2)
    return progress


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    collection_id = get_or_create_collection(cur)
    conn.commit()

    generated = 0
    skipped = 0
    db_rows = 0
    files_written = []

    first_chapter = CHAPTERS[0]
    last_chapter = CHAPTERS[-1]
    start_ref = f"{first_chapter['book']} {first_chapter['chapter']}"
    end_ref = f"{last_chapter['book']} {last_chapter['chapter']}"

    for ch in CHAPTERS:
        if chapter_exists(cur, collection_id, ch["book_id"], ch["chapter"]):
            print(f"SKIP: {ch['book']} {ch['chapter']} already exists")
            skipped += 1
            continue

        entry_uuid = insert_chapter(cur, collection_id, ch)
        conn.commit()
        db_rows += 1

        file_path = save_json(ch, entry_uuid)
        files_written.append(file_path)
        generated += 1
        print(f"GENERATED: {ch['book']} {ch['chapter']} -> {file_path}")

    # Update progress — next chapter after Exodus 36
    # Exodus has 40 chapters, so next is Exodus 37
    next_book_id = 2
    next_book = "Exodus"
    next_chapter = 37

    last_ch = last_chapter
    progress = update_progress(
        last_ch["book_id"], last_ch["book"], last_ch["chapter"],
        next_book_id, next_book, next_chapter, False
    )

    # Update progress in DB using actual schema columns
    try:
        cur.execute("SELECT id FROM commentary_generation_progress LIMIT 1")
        row = cur.fetchone()
        if row:
            cur.execute(
                """UPDATE commentary_generation_progress SET
                   current_book_id=?, current_chapter=?,
                   last_completed_book_id=?, last_completed_chapter=?,
                   updated_at=?
                   WHERE id=?""",
                (next_book_id, next_chapter,
                 last_ch["book_id"], last_ch["chapter"], NOW, row[0])
            )
        conn.commit()
    except Exception as e:
        print(f"DB progress update warning: {e}")
    conn.close()

    # Write log
    log_entry = {
        "timestamp": NOW,
        "generation_batch_id": BATCH_ID,
        "start_reference": start_ref,
        "end_reference": end_ref,
        "chapters_generated": generated,
        "chapters_skipped": skipped,
        "db_rows_inserted": db_rows,
        "files_written": files_written
    }
    with open(LOG_JSONL, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    print("\n=== SUMMARY ===")
    print(f"Generated: {start_ref} - {end_ref}")
    print(f"Chapters generated: {generated}, skipped: {skipped}")
    print(f"DB rows inserted: {db_rows}")
    print(f"Files written: {len(files_written)}")
    print(f"Next starting reference: {next_book} {next_chapter}")


if __name__ == "__main__":
    main()
