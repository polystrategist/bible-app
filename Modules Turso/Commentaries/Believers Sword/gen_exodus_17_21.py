"""Generate Exodus 17-21 commentaries and save to DB + JSON."""

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
        "chapter": 17,
        "title": "Exodus 17 — Water from the Rock and War Against Amalek",
        "summary": "Exodus 17 records two pivotal events: God providing water from a rock at Massah and Meribah when Israel quarreled with Moses, and Israel's first military battle against the Amalekites at Rephidim. In the battle, Joshua led the fighting while Moses held up the staff of God; when his hands were raised, Israel prevailed; when they dropped, Amalek gained. Aaron and Hur supported his arms until sunset. Both events test Israel's trust in God and reveal how victory depends not on human strength but on divine sustenance.",
        "content": """## What Exodus 17 Is About
Exodus 17 contains two narratives that together teach a single lesson: Israel's survival depends entirely on God, not on their own resources or strength.

In the first account (vv.1-7), the Israelites camp at Rephidim with no water. Instead of praying or trusting in God's past provision, they quarrel with Moses and test the Lord: "Is the LORD among us or not?" (v.7). God instructs Moses to strike the rock at Horeb with his staff — the same staff used to strike the Nile and part the Red Sea. Water gushes from solid stone. Moses names the place Massah ("testing") and Meribah ("quarreling"), embedding the people's failure into geography.

In the second account (vv.8-16), the Amalekites attack Israel. The battle is fought on two levels simultaneously: Joshua and the warriors fight on the plain, while Moses, Aaron, and Hur intercede on the hill. The correlation is direct and visible — when Moses raises his hands (holding the staff of God), Israel prevails; when his hands fall, Amalek prevails. Aaron and Hur solve the problem practically: they find a stone for Moses to sit on and hold up his arms from either side until the sun sets and Israel wins.

The chapter closes with God declaring perpetual war against Amalek and commanding Moses to write the account as a memorial.

## Theological Themes
- **Testing God vs. Trusting God**: The people's question — "Is the LORD among us?" — is devastating in its forgetfulness. They have already seen the plagues, the Red Sea, the manna, the cloud and fire. Doubt in the face of such evidence is not intellectual but moral — a failure to trust accumulated evidence of God's faithfulness.
- **God's Power Through Unlikely Means**: Water from a rock is impossible. This is precisely the point. God chooses means that eliminate human credit. The rock at Horeb becomes a New Testament type of Christ (1 Cor. 10:4).
- **Intercession and Community**: Moses cannot hold his arms up alone — he needs Aaron and Hur. The battle is won not by individual heroism but by communal intercession. This is one of the Bible's earliest pictures of sustained intercessory prayer as warfare.
- **Holy War and Amalek**: The Amalekites became the paradigmatic enemy in Israel's theology — descended from Esau, they attacked Israel's most vulnerable (the weak and weary at the rear, Deut. 25:17-18). The command to blot out their memory and the LORD's "war with Amalek from generation to generation" signals that opposition to God's people is opposition to God's redemptive purposes.

## Hebrew Word Notes
- **מַסָּה** (Massāh, "testing," v.7) — From nāsāh (to test/prove). The people tested God — turning the tables on the test that God had given them. This word recurs in Deuteronomy 6:16 and is quoted by Jesus in His wilderness temptation (Matt. 4:7): "You shall not put the Lord your God to the test."
- **מְרִיבָה** (Merîbāh, "quarreling/strife," v.7) — From rîb (to contend, to bring a legal case). Israel brought a lawsuit against God — demanding proof of His presence as if He owed them demonstration. The name recurs in Psalm 95:8, Hebrews 3:8.
- **יָד** (yād, "hand," vv.11-12) — Moses's hands (yadayim) are the pivot of the battle. When they are raised toward heaven, God acts; when they fall, God withholds. The hand here represents prayer and dependence, not magical power.

## How This Chapter Points to Christ
Paul explicitly identifies the rock struck at Horeb as a type of Christ: "they drank from the spiritual Rock that followed them, and the Rock was Christ" (1 Cor. 10:4). As the rock was struck so water could flow, so Christ was struck — crucified — so that living water could flow to His people (John 7:37-39). Moses's outstretched arms on the hill, sustaining the battle below, have been seen by the church fathers as a prefiguration of the crucifixion — arms spread, interceding, while the battle against the enemy rages below.

## Moral and Spiritual Lessons
- A track record of God's faithfulness is not automatic protection against doubt. We must actively remember what God has done.
- Prayer is battle. Moses's intercession was not passive devotion but active warfare — exhausting, requiring support, and directly connected to what happened on the battlefield.
- We need the Aaron and Hur in our lives — those who hold up our arms when we are weak and cannot sustain prayer alone.
- God embeds our failures into the landscape — Massah and Meribah — not to shame us forever but to ensure we do not repeat them.

## Practical Application
When you face a crisis, notice whether your first response is to quarrel (like Israel) or to pray. Train yourself to pray before complaining. Also, consider who in your life needs their arms held up right now — who is fighting a long battle and has become weary? Identify your Aaron and Hur relationships: the people whose role in your life is to support you when you can no longer support yourself.

## Believers Sword Reflection
Exodus 17 captures the twin realities of the Christian life: external conflict (the battle against Amalek) and internal temptation (the quarreling and testing of God). Victory in both requires sustained dependence on God — through prayer, community, and trust in the One who provides water from rock and strength from weakness.""",
        "chapter_overview": "Exodus 17 records God providing water from the rock at Massah and Meribah (testing Israel's trust), then Israel's first battle against Amalek — won as long as Moses held his arms raised in intercession, sustained by Aaron and Hur. The chapter is a dual lesson in dependence: on God's supernatural provision and on the community of prayer.",
        "original_language_notes": [
            {
                "term": "Massāh",
                "language": "Hebrew",
                "verse": "Exodus 17:7",
                "words_used": "מַסָּה (Massāh) — 'testing'",
                "meaning": "From nāsāh (to test/prove). The people tested God by demanding proof of His presence — reversing the dynamic in which God tests His people. Jesus quotes Deut. 6:16 ('Do not put the LORD your God to the test') against Satan in Matt. 4:7, referencing this very place."
            },
            {
                "term": "Merîbāh",
                "language": "Hebrew",
                "verse": "Exodus 17:7",
                "words_used": "מְרִיבָה (Merîbāh) — 'quarreling/strife'",
                "meaning": "From rîb (to contend, to bring a legal dispute). Israel essentially filed a lawsuit against God, demanding He prove Himself. Both place names are embedded in Israel's memory as warnings (Ps. 95:8; Heb. 3:8)."
            },
            {
                "term": "yādayim",
                "language": "Hebrew",
                "verse": "Exodus 17:11-12",
                "words_used": "יָדַיִם (yādayim) — 'hands'",
                "meaning": "Moses's raised hands (plural of yād) are the pivot point of the battle. They represent intercession and dependence on God rather than any magical power in the gesture itself. The image of arms raised to heaven is a universal posture of prayer in the ancient Near East."
            },
            {
                "term": "tsûr",
                "language": "Hebrew",
                "verse": "Exodus 17:6",
                "words_used": "צוּר (tsûr) — 'rock/cliff'",
                "meaning": "The same word used as a divine title: 'The LORD is my rock' (Ps. 18:2). Paul identifies the rock struck at Horeb as a type of Christ (1 Cor. 10:4) — the spiritual Rock who was struck so that living water might flow."
            }
        ],
        "moral_lessons": [
            "Past experiences of God's faithfulness do not automatically sustain present trust — we must actively remember and rehearse them.",
            "Prayer is spiritual warfare: Moses's intercession on the hill was as decisive as Joshua's fighting on the plain.",
            "We cannot sustain intercession alone — we need the community of Aaron and Hur to hold our arms up when we grow weary.",
            "Demanding proof of God's presence after evidence already given is a moral failure, not merely intellectual doubt.",
            "God preserves the memory of our failures (Massah, Meribah) as corrective, not condemnation."
        ],
        "application": "Identify the 'Amalek' battle in your life right now — the conflict that is wearing you down. Who is your Joshua (fighting on your behalf)? Who is your Aaron and Hur (supporting you in prayer)? Cultivate a community where intercession is shared, where no one has to hold their arms up alone indefinitely. And examine your last crisis: did you quarrel first or pray first?",
        "prayer": "Lord, forgive us for asking 'Is the LORD among us?' after all You have done. You have struck the rock; living water has flowed. You have held out the staff; the enemy has fled. Teach us to pray before we complain, and give us community that holds up our weary arms. You are the Rock. In Christ's name. Amen.",
        "key_points": [
            "Israel quarrels at Rephidim demanding water — testing God after He has already proven Himself repeatedly.",
            "God instructs Moses to strike the rock at Horeb with his staff; water gushes from solid stone.",
            "The place is named Massah (testing) and Meribah (quarreling) to memorialize Israel's failure.",
            "Amalekites attack Israel; Joshua fights below while Moses intercedes on the hill with the staff of God.",
            "When Moses's hands are raised, Israel prevails; when they drop, Amalek prevails.",
            "Aaron and Hur hold Moses's arms up from either side until sunset and Israel wins.",
            "Paul identifies the rock struck at Horeb as a type of Christ who was struck so living water might flow (1 Cor. 10:4)."
        ],
        "study_questions": [
            "Israel had already seen miraculous water provision (Marah, Elim) before Rephidim. What does it reveal about the human heart that they quarreled again so quickly?",
            "What is the difference between crying out to God in desperation and 'testing' God as Israel did at Massah?",
            "Moses's outstretched arms won the battle — not Joshua's sword. What does this teach about the relationship between prayer and action?",
            "Paul says 'the Rock was Christ' (1 Cor. 10:4). In what way does the struck rock foreshadow Christ's crucifixion and the gift of the Spirit?",
            "Who in your life serves as your 'Aaron and Hur'? How are you intentionally building those sustaining relationships?"
        ],
        "tags": ["exodus", "water-from-rock", "massah", "meribah", "amalek", "intercession", "prayer", "joshua", "aaron", "hur", "testing-god", "christ-the-rock"]
    },
    {
        "chapter": 18,
        "title": "Exodus 18 — Jethro's Wisdom: Delegation and the Organization of Leadership",
        "summary": "Exodus 18 is a chapter of reunion and wise counsel. Jethro, Moses's father-in-law and priest of Midian, comes to Moses in the wilderness with Zipporah and Moses's two sons. He hears Moses's account of the Exodus and worships God. Then, watching Moses adjudicate disputes from morning until evening, he offers a practical critique: the current system is unsustainable. He advises Moses to appoint capable, God-fearing men as judges over thousands, hundreds, fifties, and tens. Moses implements the counsel, and Jethro returns home.",
        "content": """## What Exodus 18 Is About
Exodus 18 is an unexpected chapter — not miracle or law or battle, but organizational wisdom. It is a chapter about sustainable leadership, wise delegation, and the humility to receive correction from an outsider.

Jethro arrives at the camp of Israel with Moses's wife Zipporah and their two sons — Gershom ("a stranger there") and Eliezer ("my God is help"). Their names summarize Moses's biography in two words: exile and divine deliverance. Moses bows in greeting and invites Jethro into the tent. He recounts everything God has done for Israel, and Jethro responds with joy and theological confession: "Now I know that the LORD is greater than all gods" (v.11). He offers burnt offerings and the elders of Israel eat a covenant meal together.

Then Jethro watches Moses work. From morning to evening, Moses sits as sole judge of Israel. The people queue all day for every dispute, every question, every conflict. Jethro sees the problem with one observation: "What you are doing is not good. You and the people with you will certainly wear yourselves out, for the thing is too heavy for you. You are not able to do it alone" (vv.17-18).

His proposed solution is elegant: identify godly, capable, honest, and non-corrupt men from the community. Structure them in tiers — leaders of thousands, hundreds, fifties, and tens. Let them handle the ordinary cases; bring only the extraordinary or difficult cases to Moses. This distributes the burden, trains leaders, and serves the people more efficiently.

Moses listens, implements the system, and Jethro goes home. The chapter ends quietly — no miracle, no divine speech — just the practical reorganization of a community preparing for the demands ahead at Sinai.

## Theological Themes
- **Wisdom from Unexpected Sources**: Jethro is a Midianite priest — not an Israelite. Yet he speaks the wisest words in this section of Exodus. God can give insight to those outside the covenant community, and spiritual maturity requires the humility to receive it.
- **Sustainable Leadership**: Moses was performing a heroic but unsustainable role. Jethro's intervention is an act of pastoral care for Moses as much as for the people. The burning-out of leaders is not virtuous; it is a failure of stewardship.
- **Qualifications for Leadership**: Jethro's criteria for appointed judges are specific and demanding: capable (competent), God-fearing (spiritually grounded), trustworthy (reliable), and non-covetous (not motivated by profit). These four qualities form a template for leadership selection across Scripture.
- **Community as the Body**: The tiered structure Jethro proposes foreshadows the body-of-Christ principle: every member exercising function, with no one person carrying what is meant to be shared. The entire community is served when leadership is distributed.

## Hebrew Word Notes
- **חֹתֵן** (ḥōtēn, "father-in-law," v.1) — Used repeatedly throughout the chapter. Jethro's relational identity to Moses is central — the wisdom here is family wisdom, the kind that comes from a trusted elder who has your best interests at heart.
- **אֱלִיעֶזֶר** (Elîʿezer, "my God is help," v.4) — Moses named this son to commemorate God's deliverance from Pharaoh. The name itself is a testimony embedded in a person: every time Moses called his son's name, he rehearsed the rescue.
- **יִתְרוֹ** (Yitrô, "Jethro / abundance/excellence," v.1) — Jethro's name itself carries the meaning of excellence or pre-eminence. He is introduced with his relational and reputational context intact — a significant person whose counsel deserves respect.

## How This Chapter Points to Christ
Christ is the ultimate leader who bears the burdens of His people (Matt. 11:28-30). The tiered structure Jethro proposes anticipates the body of Christ in the New Testament — apostles, elders, deacons, members — each bearing appropriate portions of the community's burden (Eph. 4:11-16; Acts 6:1-7). When the apostles faced an analogous problem in Acts 6 (overwhelmed by distribution duties), they did exactly what Jethro prescribed: they delegated to capable, Spirit-filled men so they could focus on prayer and the word. The principle is continuous from Sinai through the New Testament church.

## Moral and Spiritual Lessons
- Burnout is not a spiritual virtue. Moses was running an unsustainable system; Jethro's intervention was mercy, not criticism.
- Good leaders develop other leaders. The point of Jethro's system is not just efficiency but leadership formation across the community.
- Humility is required to receive correction from someone outside your peer group or tradition — Jethro was an in-law from Midian, not an elder of Israel.
- The selection criteria for leaders — capable, God-fearing, truthful, not covetous — are not negotiable. Lowering the bar for leadership always costs the community.
- Community health requires distributed function. One person doing everything is not faithfulness; it is a symptom of either pride or systemic dysfunction.

## Practical Application
Audit the structures in your life — at work, at church, in your family — where one person is carrying what should be distributed. If you are that person, ask who in your community is capable, God-fearing, truthful, and non-covetous, and identify one responsibility you can genuinely hand off. If you are a leader, build a leadership pipeline: don't just solve problems yourself, invest in the people who can solve them with you and after you.

## Believers Sword Reflection
Exodus 18 is a rare chapter of organizational wisdom in the middle of the Exodus narrative. It does not diminish the miraculous by introducing the practical. Rather, it shows that God cares about sustainable structures as much as supernatural interventions. The same God who parts seas also cares whether His servant has help. The Incarnation is the ultimate demonstration that God does not despise the practical: He became human to inhabit our real conditions, not just our crises.""",
        "chapter_overview": "Exodus 18 records Jethro's visit to Moses in the wilderness: a family reunion, a worship moment, and a crucial act of practical wisdom — advising Moses to delegate judicial authority to capable, God-fearing men organized in tiers. Moses's humble reception and implementation of an outsider's counsel models sustainable leadership.",
        "original_language_notes": [
            {
                "term": "ḥōtēn",
                "language": "Hebrew",
                "verse": "Exodus 18:1",
                "words_used": "חֹתֵן (ḥōtēn) — 'father-in-law'",
                "meaning": "Used 9 times in this chapter, emphasizing Jethro's relational role. The frequency underscores that this wisdom comes through family relationship — a trusted elder with no agenda except the welfare of Moses and the people."
            },
            {
                "term": "Elîʿezer",
                "language": "Hebrew",
                "verse": "Exodus 18:4",
                "words_used": "אֱלִיעֶזֶר (Elîʿezer) — 'my God is help'",
                "meaning": "Moses embedded his testimony into his son's name: 'The God of my father was my help, and delivered me from the sword of Pharaoh.' Every time this son's name was spoken, Moses rehearsed God's deliverance. Names in Hebrew narrative often carry theological weight as portable testimony."
            },
            {
                "term": "yāgēaʿ",
                "language": "Hebrew",
                "verse": "Exodus 18:18",
                "words_used": "נָבֹל תִּבֹּל (nābōl tibbōl) — 'you will surely wear out/wither'",
                "meaning": "The verb nābal means to fade, wither, or wear out — the same word used of withering leaves (Isa. 1:30). Jethro uses vivid language: Moses and the people will wither like autumn foliage under this system. The imagery captures what unsustainable leadership eventually does to a leader."
            },
            {
                "term": "yirʾat Elohim",
                "language": "Hebrew",
                "verse": "Exodus 18:21",
                "words_used": "יִרְאֵי אֱלֹהִים (yirʾê Elohim) — 'God-fearing men'",
                "meaning": "Yirʾāh (fear/reverence of God) is the foundational qualification in Jethro's list. It precedes competence in the priority order — the most competent leader without this quality is dangerous. Fear of God is the source of the moral accountability that makes the other qualities sustainable."
            }
        ],
        "moral_lessons": [
            "Burnout in leadership is not faithfulness — it is a failure to steward the gift God has given, and Jethro's gentle rebuke is pastoral care, not criticism.",
            "God can speak wisdom through unexpected people, including those outside the covenant community.",
            "The criteria for leadership — capable, God-fearing, truthful, non-covetous — cannot be compromised without cost to the whole community.",
            "Distributed leadership is not a concession to weakness but a design principle: the whole community functions better when every tier is functioning.",
            "Good leaders develop other leaders rather than creating dependency on themselves."
        ],
        "application": "Identify one area of your life where you are the bottleneck — where everything passes through you because you haven't trusted or trained others. Apply Jethro's criteria: find someone capable, God-fearing, reliable, and non-self-serving. Delegate a genuine responsibility to them — not to reduce your burden but to invest in them and serve the people under you better.",
        "prayer": "Father, give us the humility of Moses — to receive correction from wherever You choose to send it. Protect us from the pride that says no one else can do what only You can accomplish through us. Teach us to build up others, to share the burden, to lead in ways that are sustainable. Give us wisdom to choose leaders well: capable, God-fearing, honest, and generous. Amen.",
        "key_points": [
            "Jethro arrives with Zipporah and Moses's two sons — a family reunion in the wilderness.",
            "Jethro hears Moses's account of the Exodus and responds with worship and theological confession.",
            "The elders of Israel join Jethro in a covenant meal — including an outsider in communal worship.",
            "Jethro observes Moses adjudicating disputes from morning to evening and identifies the unsustainability.",
            "He proposes a tiered system: leaders of thousands, hundreds, fifties, and tens — qualified by character, not just competence.",
            "Qualifications: capable, God-fearing (first), trustworthy, and non-covetous.",
            "Moses listens and implements the system — modeling the humility to receive outside wisdom."
        ],
        "study_questions": [
            "Jethro is a Midianite priest — not an Israelite. What does it tell us about God that He sent practical wisdom through a non-Israelite at this critical juncture?",
            "Why do you think Moses had not already implemented some form of delegation? What kept him doing everything himself?",
            "Jethro lists four qualifications for judges in v.21 in a specific order: capable, God-fearing, trustworthy, non-covetous. Why do you think 'God-fearing' comes before 'capable'?",
            "In Acts 6:1-7, the apostles face an almost identical problem and apply a nearly identical solution. What does this continuity tell you about how God governs communities across time?",
            "Where are you the bottleneck in a system that was designed to be shared? What would it take to genuinely delegate?"
        ],
        "tags": ["exodus", "jethro", "moses", "leadership", "delegation", "wisdom", "judges", "organization", "community", "father-in-law", "sustainable-ministry"]
    },
    {
        "chapter": 19,
        "title": "Exodus 19 — Sinai: The Holy Mountain and the Covenant Proposal",
        "summary": "Exodus 19 is the preparatory chapter for the giving of the Law — one of the most theologically dense chapters in all of Scripture. Israel arrives at Sinai three months after leaving Egypt, and God meets Moses on the mountain with a stunning declaration: 'You will be to me a kingdom of priests and a holy nation.' God instructs Moses to consecrate the people for three days, and the chapter culminates in a terrifying theophany — thunder, lightning, thick cloud, fire, earthquake, and the trumpet blast that shook the entire mountain. The people are warned not to breach the boundary or they will die.",
        "content": """## What Exodus 19 Is About
Exodus 19 is the hinge of the Exodus narrative. Everything before has been preparation for this — the plagues, the crossing, the wilderness journey — and everything that follows (the Law, the tabernacle) flows from what happens here. The chapter is about the terms of a covenant and the terrifying holiness of the God who offers it.

Israel arrives at Sinai three months to the day after leaving Egypt (v.1). They camp at the base of the mountain, and Moses goes up to God. God's opening speech (vv.3-6) is one of the most significant passages in the Old Testament: He recounts what He has done ("how I bore you on eagles' wings"), identifies what He wants ("obey My voice and keep My covenant"), and states what Israel will be ("a treasured possession among all peoples... a kingdom of priests and a holy nation").

The phrase "kingdom of priests" is extraordinary. Israel is not called to be a priestly nation in isolation — they are to be priests for the world, mediating God's presence to the nations, just as individual priests mediated God's presence to Israel. The call is cosmic in scope.

God then instructs Moses to consecrate the people for three days in preparation for the divine descent. The boundaries of the mountain are set — anyone or anything who touches the mountain must be put to death. The consecration includes washing garments and abstaining from sexual relations, not because sexuality is impure but because it represents the kind of focusing of attention appropriate before a holy encounter.

On the third day, the theophany: thunder and lightning, thick cloud, the sound of a very loud trumpet, fire and smoke, an earthquake. The entire mountain is wrapped in smoke. The trumpet grows louder and louder. God descends in fire. Moses speaks, God answers in thunder. The people tremble. They stand at a distance. Even the priests are warned not to "break through to the LORD to gaze and many of them fall" (v.21).

## Theological Themes
- **Holy Condescension**: The God who fills heaven and earth descends to Sinai. He did not have to. The entire covenant relationship is initiated by divine grace — God proposes it, establishes its terms, and enables Israel's participation. Israel contributes nothing to the initiation.
- **Conditional Blessing, Unconditional Election**: The covenant offer has conditions ("if you obey My voice"), but the election of Israel — the choice to give them this offer at all — is unconditional. God did not choose Israel because of their size or merit (Deut. 7:7). The "if" governs blessing, not belonging.
- **Holiness as Separateness**: The mountain boundaries are not arbitrary cruelty. They represent the ontological gap between God's nature and human nature. Drawing near to the holy God without mediation and preparation is not a spiritual experience — it is death. This is why the entire sacrificial and priestly system will be established: to provide the mediation that makes safe approach possible.
- **Kingdom of Priests**: Israel's corporate vocation is priestly — mediating God's presence to the nations. The church inherits this vocation (1 Pet. 2:9) and will fulfill it ultimately in the new creation (Rev. 5:10; 20:6).

## Hebrew Word Notes
- **סְגֻלָּה** (segullāh, "treasured possession," v.5) — Not merely "possession" but specifically a personal treasure — the special property of a king. Israel is not God's property in the sense of a nation's territory, but His personal treasure among all peoples. The word occurs six times in the OT, always describing Israel's unique covenant status.
- **קְדֹשִׁים** (qedôshîm, "holy," v.6) — From qādash (to be set apart, consecrated). Holiness is not primarily ethical in the Hebrew root — it is relational and ontological: set apart for and belonging to God. Ethics follows from that belonging.
- **גָּבֹהַּ** from נָגַע (nāgaʿ, "to touch," vv.12-13) — The command not to "touch" the mountain uses this common word for physical contact. The boundary is physical, not merely symbolic: the danger of coming near the holy without preparation and mediation is real and lethal.

## How This Chapter Points to Christ
The new covenant provides what Sinai's terrifying boundaries pointed to the need for: a Mediator who can bridge the gap between human sinfulness and divine holiness. Hebrews 12:18-24 draws the contrast explicitly: "You have not come to a mountain that can be touched and that is burning with fire... to darkness, gloom and storm... but you have come to Mount Zion... to Jesus the mediator of a new covenant, and to the sprinkled blood that speaks a better word than the blood of Abel." The terror of Sinai and the grace of Zion are not opposites — Sinai displays the problem (the gap) and Zion displays the solution (the Mediator). Christ fulfills Israel's vocation as the Kingdom-Priest who mediates God's presence to the nations, and through union with Him, the church becomes "a royal priesthood" (1 Pet. 2:9).

## Moral and Spiritual Lessons
- The God of grace is the God of holy fire. Familiarity with God that loses sight of His otherness becomes idolatry — remaking God in our image. Sinai corrects the domestication of God.
- Preparation for encountering God matters. Consecration, fasting, focused attention — these are not works-righteousness but postures of reverence appropriate to the encounter.
- The priestly vocation is communal, not just individual. The entire nation of Israel was called to a collective identity as God's mediating presence in the world — as is the church.
- Proximity to God without proper mediation brings death, not life. This is why the cross is not optional sentimentality but structural necessity.

## Practical Application
How do you approach God? Do you come with the easy familiarity of one who has forgotten He is a consuming fire, or with the paralysis of one who has forgotten He has made a way? Sinai is meant to produce neither complacency nor terror, but reverence — the posture of someone who knows exactly how holy God is and how completely the Mediator has opened the way. Spend time this week reading both Exodus 19 and Hebrews 12:18-29 together, letting each passage illuminate the other.

## Believers Sword Reflection
Exodus 19 is the chapter that makes the rest of Scripture interpretable. Without understanding the terrifying holiness displayed at Sinai — the smoke, the fire, the trumpet, the earthquake, the absolute prohibition on unauthorized approach — we cannot understand why Jesus had to die, why the priestly system was necessary, or what it costs for a holy God to draw near to sinful people. The cross is not an overreaction. Sinai shows us why it was the only way.""",
        "chapter_overview": "Exodus 19 prepares Israel for the Sinai covenant: God proposes a kingdom-of-priests identity, commands three days of consecration, then descends in terrifying theophany — fire, thunder, earthquake, and the growing blast of a trumpet. The chapter is the hinge of the Exodus narrative, establishing the ontological gap between divine holiness and human sinfulness that the entire sacrificial system (and ultimately Christ) will bridge.",
        "original_language_notes": [
            {
                "term": "segullāh",
                "language": "Hebrew",
                "verse": "Exodus 19:5",
                "words_used": "סְגֻלָּה (segullāh) — 'treasured possession'",
                "meaning": "A king's personal treasure — the special property of a monarch distinct from general royal holdings. Used only 6 times in the OT, always of Israel's unique covenant status. It is not mere ownership but intimate, personal possession. The word communicates that among all nations, Israel is God's own special jewel."
            },
            {
                "term": "mamleḵet kōhanîm",
                "language": "Hebrew",
                "verse": "Exodus 19:6",
                "words_used": "מַמְלֶכֶת כֹּהֲנִים (mamleḵet kōhanîm) — 'kingdom of priests'",
                "meaning": "A corporate priestly identity for the entire nation. As individual priests mediated between Israel and God, the nation was to mediate between God and the nations. This vocation is inherited by the church (1 Pet. 2:9) and fulfilled in the new creation (Rev. 5:10; 20:6)."
            },
            {
                "term": "qādôsh",
                "language": "Hebrew",
                "verse": "Exodus 19:6",
                "words_used": "גּוֹי קָדוֹשׁ (gôy qādôsh) — 'holy nation'",
                "meaning": "Qādosh (from qādash, to separate/consecrate) — holiness as set-apartness and belonging to God. Primary meaning is relational and ontological, not primarily ethical. Ethics flows from the consecrated identity, not the reverse. Israel is to be a nation that is visibly different because it belongs to a visibly different God."
            },
            {
                "term": "nāgaʿ",
                "language": "Hebrew",
                "verse": "Exodus 19:12",
                "words_used": "נָגַע (nāgaʿ) — 'to touch'",
                "meaning": "Common Hebrew verb for physical contact. The prohibition against touching the mountain is physical, not merely symbolic — contact with the holy mountain without preparation and mediation brings death. This same concept of dangerous holiness appears throughout Leviticus and explains the elaborate precautions around the ark of the covenant."
            }
        ],
        "moral_lessons": [
            "The God of grace is simultaneously the God of consuming fire — familiarity that loses sight of God's holiness drifts into idolatry.",
            "Preparation and consecration for encountering God are postures of reverence, not works-righteousness.",
            "The priestly vocation — mediating God's presence to the world — is communal, not merely individual.",
            "Proximity to a holy God without proper mediation brings death rather than life; this is why the cross is structural necessity, not sentiment.",
            "God's initiative is everything: the covenant was His proposal, on His terms, at His mountain."
        ],
        "application": "Read Exodus 19 alongside Hebrews 12:18-29 this week. Let Sinai show you the holiness problem; let Hebrews show you the Mediator's solution. Then examine your prayer life: do you approach God with the irreverence of cheap familiarity, or the paralysis of forgotten grace? Aim for reverence — awe at His holiness held together with confidence in Christ's mediation.",
        "prayer": "Holy God, who descended on Sinai in fire and thunder — we have not come to a mountain that can be touched but to Mount Zion and to Jesus the Mediator. Thank You that what Your holiness demanded, Your mercy provided. Give us reverence without terror, confidence without presumption. Make us what You called Israel to be: a kingdom of priests, Your treasured possession among the peoples of the earth. In Christ, who is our High Priest, Amen.",
        "key_points": [
            "Israel arrives at Sinai three months after leaving Egypt — a three-month journey into covenant.",
            "God's covenant proposal: 'If you obey My voice, you will be My treasured possession, a kingdom of priests and a holy nation.'",
            "The 'kingdom of priests' identity is cosmic: Israel is to mediate God's presence to the nations.",
            "Three days of consecration: washing garments, sexual abstinence, setting boundaries around the mountain.",
            "On the third day: thunder, lightning, thick cloud, fire, earthquake, and a trumpet that grew louder and louder.",
            "Even the priests are warned not to breach the boundary — unauthorized approach to the holy God brings death.",
            "Hebrews 12:18-24 contrasts terrifying Sinai with gracious Zion — both are fulfilled in Christ the Mediator."
        ],
        "study_questions": [
            "God's covenant offer comes with a condition ('if you obey') but is preceded by His unconditional act of election ('I bore you on eagles' wings'). What is the relationship between grace and obedience in the Sinai covenant?",
            "What does 'kingdom of priests' mean as a national vocation? How does the church inherit and fulfill this calling (1 Pet. 2:9)?",
            "Why was the three-day preparation period necessary? What do the acts of consecration (washing, abstinence) communicate about approaching God?",
            "The theophany at Sinai was terrifying — thunder, fire, earthquake. How does Hebrews 12:18-24 reframe this for New Testament believers?",
            "What does it mean practically that you have come to Mount Zion, to the sprinkled blood of Jesus (Heb. 12:22-24)? How should that change how you pray?"
        ],
        "tags": ["exodus", "sinai", "covenant", "holiness", "theophany", "kingdom-of-priests", "holy-nation", "consecration", "moses", "ten-commandments", "presence-of-god"]
    },
    {
        "chapter": 20,
        "title": "Exodus 20 — The Ten Commandments: God's Covenant Charter for His People",
        "summary": "Exodus 20 contains the Decalogue — the Ten Commandments — spoken directly by God to the assembled people of Israel at Sinai. These ten words form the covenantal constitution of the redeemed community, beginning not with obligation but with identity: 'I am the LORD your God, who brought you out of Egypt, out of the house of slavery.' The commandments govern Israel's relationship with God (commandments 1-4) and with one another (commandments 5-10), culminating in the people's terrified response and Moses's explanation that the fear of God is the beginning of true obedience.",
        "content": """## What Exodus 20 Is About
Exodus 20 is one of the most consequential chapters in all of Scripture. The Ten Commandments have shaped Western civilization's moral framework, Israel's covenant life, the church's catechesis, and every individual believer's understanding of what it means to live before God. But to read them rightly, we must read them in their original context.

The Decalogue begins with a preamble — not a command but an identity statement: "I am the LORD your God, who brought you out of the land of Egypt, out of the house of slavery" (v.2). This is not preface filler. It is the theological foundation of everything that follows. The commandments are not the conditions for becoming God's people; they are the way of life for those who already are. Law follows grace.

**Commandments 1-4 (God-directed)**:
- First: "You shall have no other gods before Me" — exclusive allegiance to YHWH
- Second: No carved images or idols — God cannot be domesticated into a created form
- Third: Do not misuse the LORD's name — His name (His revealed identity) carries His weight
- Fourth: Keep the Sabbath holy — one day in seven belongs to God; rest is covenant obedience

**Commandments 5-10 (Neighbor-directed)**:
- Fifth: Honor your father and mother — with a promise of long life in the land
- Sixth: You shall not murder
- Seventh: You shall not commit adultery
- Eighth: You shall not steal
- Ninth: You shall not give false testimony against your neighbor
- Tenth: You shall not covet

The people's response (vv.18-21) is terror — they stand far off and beg Moses to mediate. Moses explains: "Do not be afraid. God has come to test you, that the fear of Him may be before you, that you may not sin" (v.20). Fear that produces obedience is the appropriate response; terror that drives you away from God is not.

The chapter ends with two regulations about the altar that will be built — a bridge into the detailed law codes that follow.

## Theological Themes
- **Grace Before Law**: The preamble ("who brought you out of Egypt") precedes the commandments. Obedience is the response of the redeemed to their Redeemer, not the means of achieving redemption. This is the Reformation's great recovery: law after gospel, not law as gospel.
- **The Unity of the Decalogue**: The commandments are not ten independent rules but a unified covenant charter. You cannot violate one without affecting the whole. Jesus would capture this in His summary: love God (commandments 1-4) and love your neighbor (commandments 5-10) (Matt. 22:37-40).
- **The Second Commandment and Iconoclasm**: The prohibition on images is not a prohibition on art but on creating any visual representation of God that replaces or reduces His revealed nature. God has revealed Himself through words, not images — "you heard a voice but saw no form" (Deut. 4:15).
- **The Tenth Commandment and Interiority**: The prohibition on covetousness is internal — it targets not an act but a disposition, a desire. Paul would say this commandment showed him what sin really is (Rom. 7:7). Sin begins in the heart before it reaches the hand.

## Hebrew Word Notes
- **עֲנָוָה** from **אָנֹכִי יְהוָה** (ʾānōkî YHWH, "I am the LORD," v.2) — The divine self-disclosure that opens the Decalogue. YHWH (the Tetragrammaton) — God's personal covenant name — is the subject of the commandments. These are not universal human ethics; they are the covenant obligations of YHWH's own people to their covenant God.
- **קַנָּא** (qannāʾ, "jealous/zealous," v.5) — "For I, the LORD your God, am a jealous God." Qannāʾ describes the fervent, exclusive commitment of a covenant partner who will not share what belongs to Him by covenant. This is not petty insecurity but covenantal fidelity — the same fervor that characterizes faithful love in marriage.
- **שָׁוְא** (shāwʾ, "in vain / emptiness / worthlessness," v.7) — "Do not take the name of the LORD in vain." Shāwʾ means empty, worthless, false. To use God's name "in vain" is to use it emptily — as a word stripped of its weight, divorced from its meaning. This covers not just profanity but using God's name in oaths, treaties, or blessings with no genuine commitment.
- **שָׁבַת** (shābat, "to cease/rest," v.10) — The Sabbath command grounds the day of rest in creation (vv.11) and redemption (Deut. 5:15). Both grounds matter: creation Sabbath says humanity is designed for rest; redemption Sabbath says the freed people need not labor to justify their existence.

## How This Chapter Points to Christ
Jesus is the fulfillment of the Law, not its abolisher (Matt. 5:17). In the Sermon on the Mount, He radicalizes each commandment to its interior intention: murder begins with anger; adultery begins with lust; false testimony begins with the heart that has not trained itself in truth. He fulfills the Law by being everything it pointed to: the one truly faithful human, the second Adam who kept every command from the inside. He also pays the penalty for those who have violated the Law — not annulling it but absorbing its just consequence (Gal. 3:13). The result is not a Christianity without moral structure but one whose moral structure is now written on the heart by the Spirit (Jer. 31:33; 2 Cor. 3:3).

## Moral and Spiritual Lessons
- The Ten Commandments are not a ladder to climb into God's favor but a description of what it looks like to live freely as God's redeemed people.
- The Sabbath is a gift before it is a demand — a day God gives back to His people for restoration, relationship, and rest.
- The commandments cover the entire person: the heart (covetousness), the mouth (false testimony, misusing God's name), the hand (murder, theft, adultery), and the will (honoring parents, keeping Sabbath).
- The severity of the people's terror teaches that a casual approach to the holy God is not humble but presumptuous. Reverence is appropriate.

## Practical Application
Memorize the Ten Commandments and their order. Then meditate through them in light of Jesus's interiorization in Matthew 5-7. For each commandment, ask: Am I obeying the surface level? Am I obeying the interior level? Which commandment convicts you most deeply? That is often where the Spirit is doing His most important work.

## Believers Sword Reflection
The Ten Commandments are not ten arbitrary rules from a divine legislator who wants compliance. They are ten windows into the character of God: the first four show what God is like (singular, invisible, weighty, restful), and the last six show what His image-bearers should look like among one another. To obey them is to be conformed to the image of God. To break them is to suppress what we were created to reflect. Christ restores both the image and the obedience.""",
        "chapter_overview": "Exodus 20 contains the Decalogue — the Ten Commandments — spoken by God directly at Sinai, beginning with the gospel preamble ('I am the LORD who brought you out of Egypt') before listing obligations. Commands 1-4 govern the God-human relationship; commands 5-10 govern human-human relationships. The people's terror prompts Moses's explanation that holy fear produces obedience without driving people away from God.",
        "original_language_notes": [
            {
                "term": "ʾānōkî YHWH",
                "language": "Hebrew",
                "verse": "Exodus 20:2",
                "words_used": "אָנֹכִי יְהוָה (ʾānōkî YHWH) — 'I am the LORD'",
                "meaning": "The divine self-disclosure that frames every commandment as the obligation of covenant partners, not the conditions of becoming God's people. YHWH's personal covenant name (the Tetragrammaton) identifies the specific God who speaks — not a generic deity but the God of Abraham, Isaac, and Jacob who acted in history to rescue Israel."
            },
            {
                "term": "qannāʾ",
                "language": "Hebrew",
                "verse": "Exodus 20:5",
                "words_used": "קַנָּא (qannāʾ) — 'jealous/zealous'",
                "meaning": "Describes God's exclusive covenantal commitment — not petty insecurity but the fervent fidelity of a covenant partner who will not share what belongs to Him by covenant. The same intensity that characterizes faithful love in marriage. God's jealousy is His love refusing to be diluted."
            },
            {
                "term": "shāwʾ",
                "language": "Hebrew",
                "verse": "Exodus 20:7",
                "words_used": "שָׁוְא (shāwʾ) — 'in vain / emptiness / worthlessness'",
                "meaning": "To use God's name 'in vain' means to use it emptily — stripped of its weight and meaning. This covers casual profanity but extends to using God's name in oaths, covenants, or speech with no genuine intent to honor what is being invoked. The name of God carries His full weight and character."
            },
            {
                "term": "shābat",
                "language": "Hebrew",
                "verse": "Exodus 20:10",
                "words_used": "שָׁבַת (shābat) — 'to cease, rest, stop work'",
                "meaning": "Root of 'Sabbath' — to cease from activity, to rest. The Sabbath command is grounded in both creation (God rested on the seventh day, Gen. 2:2-3) and redemption (Deut. 5:15 grounds it in the Exodus). Both grounds matter: as creatures, humans are designed for rest; as redeemed people, they need not labor to justify their existence before God."
            }
        ],
        "moral_lessons": [
            "The Decalogue begins with grace ('who brought you out of Egypt') — obedience is the response of the redeemed, not the means of redemption.",
            "The commandments cover the entire person: heart (covetousness), mouth (false testimony, God's name), hand (murder, theft, adultery), and will.",
            "The Sabbath is a gift before it is a demand — God restoring time to His people for relationship and restoration.",
            "Reverence before a holy God is not the opposite of freedom but its proper foundation.",
            "The tenth commandment reveals that God's law addresses not just actions but desires — sin begins before the deed."
        ],
        "application": "Memorize the Ten Commandments in order. Then read Matthew 5:21-48 to see how Jesus interiorizes each one. Which commandment — at its interior level — convicts you most? That is often where the Spirit is doing His deepest transformative work this season.",
        "prayer": "LORD, You are the God who brought us out of Egypt — out of every form of slavery. We receive Your Law not as a burden but as a charter for the free life You have given us. Forgive us where we have broken Your commands — in action and in the hidden desires of the heart. Write Your law on our hearts by Your Spirit, and make us people who love You with all we are and our neighbors as ourselves. In Christ, who fulfilled every word of this covenant. Amen.",
        "key_points": [
            "The Decalogue begins with a gospel preamble — identity before obligation: 'I am the LORD who brought you out of Egypt.'",
            "Commandments 1-4 govern the God-human relationship: exclusive allegiance, no images, honoring God's name, Sabbath.",
            "Commandments 5-10 govern the human-human relationship: parents, life, marriage, property, truth, desires.",
            "The Sabbath command is grounded in creation (God's rest in Genesis 2) and redemption (freedom from Egypt).",
            "The tenth commandment prohibits covetousness — targeting a disposition, not just an action; sin of the heart before the hand.",
            "The people's terror causes them to stand far off and beg for a mediator — Moses.",
            "Jesus fulfills the Law from the inside, radicalizing it to its interior intention in the Sermon on the Mount."
        ],
        "study_questions": [
            "The commandments are preceded by 'I am the LORD your God who brought you out of Egypt.' How does this preamble change how you understand the nature of biblical law — is it a means of earning God's favor or the charter of those already favored?",
            "The second commandment prohibits images of God. Why do you think God communicates through words rather than images? What is lost when God is depicted visually?",
            "Jesus says in Matthew 5:17 that He came not to abolish the Law but to fulfill it. How does His treatment of the commandments in Matthew 5:21-48 deepen rather than abolish them?",
            "Paul says in Romans 7:7 that the tenth commandment ('do not covet') showed him what sin really is. Why is covetousness the commandment that most reveals the heart?",
            "What is the relationship between the fear of God (v.20 — the fear that keeps you from sin) and the terror of the people (v.18 — the fear that drives them to distance)? Is holy fear a gift or a burden?"
        ],
        "tags": ["exodus", "ten-commandments", "decalogue", "law", "sinai", "sabbath", "covenant", "idolatry", "holiness", "moral-law", "jesus-fulfills-law"]
    },
    {
        "chapter": 21,
        "title": "Exodus 21 — Laws for Just Community: Servants, Life, and Injury",
        "summary": "Exodus 21 begins the 'Book of the Covenant' (Exodus 21-23), a section of case law that applies the principles of the Decalogue to concrete situations in Israel's community life. The chapter covers the rights and release of Hebrew servants, consequences for murder and manslaughter, protection for parents, laws regarding injuries in conflict, and the principle of proportional justice (lex talionis — eye for eye). Read in historical context, these laws represent a significant humanitarian advance: they protect the vulnerable, limit vengeance, and embed proportionality into a legal system where the powerful commonly exploited the weak.",
        "content": """## What Exodus 21 Is About
Exodus 21 is the first section of the Book of the Covenant (Exodus 21-23), the law code that expands and applies the Ten Commandments to specific situations in Israel's communal life. Coming immediately after the Decalogue, it answers the question: "What does covenant fidelity look like in the practical details of daily life?"

**Hebrew Servant Laws (vv.1-11)**: The chapter opens with regulations governing Hebrew debt-servants. This is not chattel slavery in the sense of permanent ownership of a human being. Poverty in the ancient world could force a person to indenture themselves to work off a debt. The regulations here set firm limits: a Hebrew servant is released after six years (mirroring the Sabbath principle), without debt. If he entered with a wife, she leaves with him; if his master gave him a wife and they had children, the wife and children remain. But if the servant loves his master and chooses to stay permanently, a covenant ceremony (boring the ear to the doorpost) formalizes the voluntary bond. Female servants who were sold as potential wives have specific protections: if the arrangement doesn't proceed, they go free; they cannot be sold to foreigners; they retain their rights to food, clothing, and conjugal rights if the man later takes another wife.

**Protection of Life (vv.12-17)**: Murder is punishable by death. But the law distinguishes intentional from unintentional killing — cities of refuge are provided for the latter. Kidnapping, cursing parents, and striking parents are each capital offenses, reflecting the severity with which Israel was to treat assaults on life and family order.

**Injury Laws and Lex Talionis (vv.18-36)**: The remaining laws govern various injury scenarios: fights that don't kill, the rights of slaves who are struck, pregnant women caught in conflict, and the famous "eye for eye, tooth for tooth" principle. This principle (lex talionis) is not a license for private revenge but a limit on it — punishment must be proportional and cannot exceed the injury done. In a world where the powerful could demand unlimited retribution from the weak, capping penalties at equivalence was a radical humanitarian advance.

## Theological Themes
- **The Dignity of the Vulnerable**: The detailed protections for servants, women, and the injured reflect God's concern for those with less power. Long before modern concepts of human rights, these laws embedded the principle that even the least person has inherent dignity before God and the law.
- **Proportional Justice**: Lex talionis ("eye for eye") is regularly misread as a justification for revenge. In its original context it is a cap on vengeance, not a floor. It prevented wealthy or powerful offenders from buying their way out and prevented victors from demanding unlimited retribution. Jesus's expansion ("turn the other cheek," Matt. 5:38-39) does not abrogate this principle but transcends it with the grace of non-retaliation in personal disputes.
- **Sabbath Logic in the Servant Laws**: The six-year service and seventh-year release directly apply the Sabbath principle to human relationships. The Sabbath year (Deuteronomy 15 expands this) is the Decalogue's fourth commandment extended into social practice — freedom and rest are not just personal but systemic.
- **Intention Matters**: The distinction between murder and manslaughter (vv.12-14) shows that Israel's law recognizes moral psychology — the state of a person's intention at the time of the act affects the nature of the crime and its appropriate consequence. This is a surprisingly sophisticated legal principle.

## Hebrew Word Notes
- **עֶבֶד עִבְרִי** (ʿeved ʿivrî, "Hebrew servant," v.2) — ʿEved means a servant or slave, but context determines the nature of the servitude. Here it is specifically a Hebrew national in debt-bondage with clear temporal limits — not permanent chattel slavery. The law code treats such servants with consistent protection of their dignity and eventual freedom.
- **רְצַח** (rātsaḥ, "murder," v.13) — The sixth commandment uses this specific word, which the law codes distinguish from killing in war or capital punishment. The law here makes the same distinction: rātsaḥ (murder) is distinguished from accidental killing by the presence of premeditation and malice.
- **עַיִן תַּחַת עַיִן** (ʿayin taḥat ʿayin, "eye for eye," v.24) — Taḥat means "in place of" or "instead of" — the punishment substitutes for the injury, proportionally. The text calls for equivalence, not excess. This principle appears in Hammurabi's Code (c. 1750 BC) but applies more equitably in Exodus, as Hammurabi's version varies by social class.

## How This Chapter Points to Christ
Christ stands as the ultimate fulfillment of these laws in two ways: First, He is the cities-of-refuge reality — those who "flee to Him" from the avenger (the judgment of the Law) find safety in Him (Heb. 6:18). Second, He transcends lex talionis not by abolishing it but by absorbing it — He received the eye-for-eye punishment we deserved (2 Cor. 5:21), exhausting the law's demand so that forgiveness, not equivalence, becomes the currency of His community. What the law demanded, He provided; what His people owe, He paid.

## Moral and Spiritual Lessons
- Law reflects the character of the lawgiver. Israel's laws embedding dignity for the servant and limit to retribution reveal a God who cares about the vulnerable and opposes the exploitative.
- Proportionality in justice is a biblical value, not merely a secular legal concept. Over-punishment and under-punishment both violate God's character.
- Intention shapes moral responsibility. The law's distinction between murder and manslaughter teaches that God evaluates the heart, not just the hand.
- The servant who chooses to remain at the doorpost teaches that chosen service out of love is not slavery. Christians are "bond-servants of Christ" by choice, not compulsion.

## Practical Application
Study how the Book of the Covenant moves from principles (Decalogue) to cases. In your own ethical decision-making, practice this move: identify the underlying principle (love your neighbor, protect the vulnerable, seek proportional justice), then reason carefully about how it applies to your specific situation. Don't look for your exact case in the text — learn the principle and apply it faithfully.

## Believers Sword Reflection
Exodus 21 requires the reader to resist two opposite mistakes. The first is to read the laws anachronistically as if they endorse modern Western slavery — they don't; they restrict and humanize an institution present in all ancient Near Eastern societies. The second is to dismiss them as merely cultural — they aren't; they embed permanent moral principles about human dignity, proportional justice, and the protection of the vulnerable that remain authoritative in their principle even where their specific form belongs to Israel's historical context.""",
        "chapter_overview": "Exodus 21 opens the Book of the Covenant with specific laws applying the Decalogue to community life: rights and release of Hebrew servants, protection for women in service arrangements, distinctions between murder and manslaughter, penalties for assault, and the lex talionis (eye for eye) principle of proportional justice. These laws embed human dignity and limited vengeance in a culture where unchecked power commonly exploited the weak.",
        "original_language_notes": [
            {
                "term": "ʿeved ʿivrî",
                "language": "Hebrew",
                "verse": "Exodus 21:2",
                "words_used": "עֶבֶד עִבְרִי (ʿeved ʿivrî) — 'Hebrew servant/slave'",
                "meaning": "ʿEved (servant/slave) with ʿivrî (Hebrew) specifies a fellow Israelite in voluntary or debt-imposed servitude — not permanent chattel slavery. The temporal limit (6 years, release in the 7th) and the protections provided distinguish this from the slavery Israel experienced in Egypt."
            },
            {
                "term": "rātsaḥ",
                "language": "Hebrew",
                "verse": "Exodus 21:13",
                "words_used": "רָצַח (rātsaḥ) — 'to murder'",
                "meaning": "The sixth commandment's specific word for murder — killing with premeditation and malice — distinguished from killing in war, capital punishment, or accident. The law here carefully distinguishes rātsaḥ from accidental killing, providing cities of refuge for the latter (cf. Num. 35). God is concerned with intention, not just outcome."
            },
            {
                "term": "ʿayin taḥat ʿayin",
                "language": "Hebrew",
                "verse": "Exodus 21:24",
                "words_used": "עַיִן תַּחַת עַיִן (ʿayin taḥat ʿayin) — 'eye in place of eye'",
                "meaning": "Taḥat ('under/in place of') signals proportional substitution: the punishment stands in place of the injury, equivalent but not excessive. This principle caps vengeance at proportionality — a radical limit in cultures where the powerful could demand unlimited retaliation. Jesus transcends rather than abolishes it in Matt. 5:38-39."
            },
            {
                "term": "marzēaḥ from mōʿēd",
                "language": "Hebrew",
                "verse": "Exodus 21:13",
                "words_used": "צָדָה (tsādāh) — 'to lie in wait / to plan'",
                "meaning": "This verb describes premeditation — deliberately plotting a killing as opposed to accidental or heat-of-passion killing. The presence or absence of tsādāh is the legal distinction between murder (capital crime) and manslaughter (city of refuge). Intention has always been morally significant in biblical jurisprudence."
            }
        ],
        "moral_lessons": [
            "Law reflects the character of the lawgiver — Israel's laws protecting servants and limiting retaliation reveal a God who cares about the vulnerable.",
            "Proportional justice is a biblical moral value: both over-punishment and under-punishment violate God's character.",
            "Intention shapes moral responsibility; the distinction between murder and manslaughter shows God evaluates the heart, not just the outcome.",
            "The servant who freely chooses to remain demonstrates that covenant love can transform obligation into chosen devotion.",
            "Protection of the weak against the strong is not a modern innovation but a consistent thread from Sinai through the New Testament."
        ],
        "application": "Practice the principle-to-case reasoning of the Book of the Covenant: when you face an ethical situation not covered directly by Scripture, identify the underlying principle (protect the vulnerable, seek proportional justice, honor life), then reason carefully and prayerfully about how it applies to your specific case. Don't look for your exact situation in the text — learn to think biblically.",
        "prayer": "God of justice, You are not indifferent to the vulnerable, the servant, the injured, or the oppressed. You wrote their protection into Your covenant from the beginning. Give us eyes to see the vulnerable in our communities, courage to protect them, and wisdom to pursue justice that is proportional and merciful. Make us people who reflect Your character — just, compassionate, and fierce against exploitation. In Christ, who absorbed the just penalty we owed. Amen.",
        "key_points": [
            "The Book of the Covenant (Exodus 21-23) applies Decalogue principles to specific communal situations.",
            "Hebrew servants are released after six years, applying the Sabbath principle to social relationships.",
            "Female servants in potential marriage arrangements have specific dignity-protections: food, clothing, and status cannot be denied.",
            "Murder (with premeditation) is capital; manslaughter (unintentional) is handled by cities of refuge.",
            "Kidnapping, striking, or cursing parents are also capital offenses, reflecting the high value placed on life and family order.",
            "Lex talionis ('eye for eye') is a cap on vengeance, not a license for it — punishment must be proportional and cannot exceed the injury.",
            "Christ fulfills lex talionis by absorbing the punishment we deserved and offering forgiveness as the currency of His community."
        ],
        "study_questions": [
            "How do the servant laws in Exodus 21:1-11 differ from chattel slavery? What principles in these laws protect human dignity even within an institution of servitude?",
            "The law distinguishes murder from manslaughter based on premeditation (v.13). What does this tell us about how God evaluates human actions — does intention matter?",
            "Jesus quotes 'eye for eye' in Matthew 5:38-39 and seems to replace it with 'turn the other cheek.' Is He abolishing lex talionis or fulfilling it? What is the difference?",
            "The servant who voluntarily chooses permanent service through the doorpost ceremony (v.6) is a picture of chosen love. How does this image illuminate what it means to call yourself a 'servant of Christ'?",
            "In what ways do these ancient laws embed permanent moral principles about protecting the vulnerable that apply across all cultures and eras?"
        ],
        "tags": ["exodus", "book-of-covenant", "case-law", "servants", "lex-talionis", "proportional-justice", "murder", "manslaughter", "dignity", "social-law", "sabbath-year"]
    }
]


def get_or_create_batch(conn):
    cur = conn.cursor()
    batch_uuid = str(uuid.uuid4())
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    cur.execute("""
        INSERT INTO commentary_generation_batches
        (uuid, collection_id, batch_name, generator_type, language_code, started_at, status)
        VALUES (?, ?, ?, 'ai', 'en', ?, 'draft')
    """, (batch_uuid, COLLECTION_ID, f"Exodus 17-21 batch {now}", now))
    conn.commit()
    return cur.lastrowid, batch_uuid


def save_commentary(conn, batch_id, batch_uuid, commentary):
    cur = conn.cursor()
    chapter = commentary["chapter"]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

    # Check if already exists
    cur.execute("""
        SELECT id, content FROM commentary_entries
        WHERE collection_id=? AND book_id=? AND chapter=? AND language_code='en'
        AND reference_scope='chapter' AND deleted_at IS NULL
    """, (COLLECTION_ID, BOOK_ID, chapter))
    existing = cur.fetchone()
    if existing:
        content = existing[1] or ""
        if len(content) > 200:
            return "skipped", existing[0]

    entry_uuid = str(uuid.uuid4())
    key_points_json = json.dumps(commentary["key_points"])
    study_questions_json = json.dumps(commentary["study_questions"])
    tags_json = json.dumps(commentary.get("tags", []))
    word_count = len(commentary["content"].split())

    if existing:
        cur.execute("""
            UPDATE commentary_entries SET
                generation_batch_id=?, title=?, summary=?, content=?, application=?,
                prayer=?, key_points=?, study_questions=?, theological_perspective=?,
                word_count=?, updated_at=?
            WHERE id=?
        """, (
            batch_id, commentary["title"], commentary["summary"], commentary["content"],
            commentary["application"], commentary["prayer"],
            key_points_json, study_questions_json,
            THEOLOGICAL_PERSPECTIVE, word_count, now, existing[0]
        ))
        conn.commit()
        return "updated", existing[0]
    else:
        cur.execute("""
            INSERT INTO commentary_entries
            (uuid, collection_id, generation_batch_id, book_id, chapter,
             reference_scope, title, summary, content, application, prayer,
             key_points, study_questions, language_code, theological_perspective,
             status, is_ai_generated, ai_generation_batch_uuid, word_count,
             sync_status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, 'chapter', ?, ?, ?, ?, ?, ?, ?, 'en', ?, 'draft', 1, ?, ?, 'local', ?, ?)
        """, (
            entry_uuid, COLLECTION_ID, batch_id, BOOK_ID, chapter,
            commentary["title"], commentary["summary"], commentary["content"],
            commentary["application"], commentary["prayer"],
            key_points_json, study_questions_json,
            THEOLOGICAL_PERSPECTIVE, batch_uuid, word_count, now, now
        ))
        conn.commit()
        return "inserted", cur.lastrowid


def save_json(commentary):
    os.makedirs(GENERATED_DIR, exist_ok=True)
    chapter = commentary["chapter"]
    filename = f"{GENERATED_DIR}/{chapter:02d}.json"

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    entry_uuid = str(uuid.uuid4())

    data = {
        "uuid": entry_uuid,
        "collection_name": COLLECTION_NAME,
        "author_type": AUTHOR_TYPE,
        "language_code": LANGUAGE_CODE,
        "theological_perspective": THEOLOGICAL_PERSPECTIVE,
        "status": "draft",
        "book_id": BOOK_ID,
        "book": BOOK_NAME,
        "chapter": chapter,
        "title": commentary["title"],
        "summary": commentary["summary"],
        "content": commentary["content"],
        "chapter_overview": commentary["chapter_overview"],
        "original_language_notes": commentary["original_language_notes"],
        "moral_lessons": commentary["moral_lessons"],
        "application": commentary["application"],
        "prayer": commentary["prayer"],
        "key_points": commentary["key_points"],
        "study_questions": commentary["study_questions"],
        "tags": commentary.get("tags", []),
        "sources": [],
        "created_at": now,
        "updated_at": now
    }

    # Verify no forbidden keys
    forbidden = {"is_ai_generated", "model_name", "prompt_version"}
    assert not (set(data.keys()) & forbidden), f"Forbidden keys found: {set(data.keys()) & forbidden}"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Verify it parses back
    with open(filename, "r", encoding="utf-8") as f:
        parsed = json.load(f)
    assert not (set(parsed.keys()) & forbidden), "Forbidden keys in parsed JSON"

    return filename


def update_progress(conn, last_chapter):
    cur = conn.cursor()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    next_chapter = last_chapter + 1
    if next_chapter > 40:  # Exodus has 40 chapters
        next_book_id = 3
        next_book = "Leviticus"
        next_chapter = 1
    else:
        next_book_id = BOOK_ID
        next_book = BOOK_NAME

    cur.execute("""
        UPDATE commentary_generation_progress
        SET current_book_id=?, current_chapter=?,
            last_completed_book_id=?, last_completed_chapter=?,
            updated_at=?
        WHERE collection_id=? AND language_code='en'
    """, (next_book_id, next_chapter, BOOK_ID, last_chapter, now, COLLECTION_ID))
    conn.commit()

    progress = {
        "next_book_id": next_book_id,
        "next_book": next_book,
        "next_chapter": next_chapter,
        "last_completed_book_id": BOOK_ID,
        "last_completed_book": BOOK_NAME,
        "last_completed_chapter": last_chapter,
        "completed": False,
        "updated_at": now
    }
    with open("commentary_generation_progress.json", "w") as f:
        json.dump(progress, f, indent=2)

    return progress


def append_log(batch_uuid, chapters_generated, chapters_skipped, db_rows_inserted, files_written, start_ref, end_ref):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    log_entry = {
        "timestamp": now,
        "generation_batch_id": batch_uuid,
        "start_reference": start_ref,
        "end_reference": end_ref,
        "chapters_generated": chapters_generated,
        "chapters_skipped": chapters_skipped,
        "db_rows_inserted": db_rows_inserted,
        "files_written": files_written
    }
    with open("commentary_generation_log.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")


def main():
    conn = sqlite3.connect(DB_PATH)
    batch_id, batch_uuid = get_or_create_batch(conn)

    chapters_generated = 0
    chapters_skipped = 0
    db_rows_inserted = 0
    files_written_list = []

    for commentary in COMMENTARIES:
        chapter = commentary["chapter"]
        action, entry_id = save_commentary(conn, batch_id, batch_uuid, commentary)
        if action == "skipped":
            chapters_skipped += 1
            print(f"  SKIPPED: {BOOK_NAME} {chapter} (already exists with content)")
        else:
            filename = save_json(commentary)
            files_written_list.append(filename)
            db_rows_inserted += 1
            chapters_generated += 1
            print(f"  {action.upper()}: {BOOK_NAME} {chapter} -> {filename}")

    last_chapter = COMMENTARIES[-1]["chapter"]
    progress = update_progress(conn, last_chapter)

    start_ref = f"{BOOK_NAME} {COMMENTARIES[0]['chapter']}"
    end_ref = f"{BOOK_NAME} {last_chapter}"
    append_log(batch_uuid, chapters_generated, chapters_skipped, db_rows_inserted, len(files_written_list), start_ref, end_ref)

    conn.close()

    print(f"\nDone.")
    print(f"  Generated: {chapters_generated}, Skipped: {chapters_skipped}")
    print(f"  DB rows inserted/updated: {db_rows_inserted}")
    print(f"  Files written: {files_written_list}")
    print(f"  Next: {progress['next_book']} {progress['next_chapter']}")


if __name__ == "__main__":
    main()
