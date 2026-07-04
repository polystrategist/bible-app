#!/usr/bin/env python3
"""Generate Leviticus 12-16 commentaries for Believers Sword."""

import sqlite3
import json
import uuid
import os
from datetime import datetime, timezone

DB_PATH = "believers_sword_commentaries.db"
PROGRESS_JSON = "commentary_generation_progress.json"
LOG_FILE = "commentary_generation_log.jsonl"
GENERATED_DIR = "generated"
COLLECTION_ID = 1
COLLECTION_NAME = "Believers Sword Commentaries"
LANGUAGE_CODE = "en"
BOOK_ID = 3
BOOK = "Leviticus"
BOOK_SLUG = "leviticus"
BOOK_DIR = f"03-{BOOK_SLUG}"

BATCH_UUID = str(uuid.uuid4())
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

COMMENTARIES = [
    {
        "chapter": 12,
        "title": "Purification After Childbirth",
        "summary": "Leviticus 12 prescribes the ritual purification process required of a woman after giving birth, outlining periods of uncleanness and the sacrificial offerings that restore her to full ceremonial standing within the covenant community.",
        "content": """Leviticus 12 addresses what might seem to modern readers an unusual intersection of life's greatest joy—the birth of a child—and ritual impurity. Yet this chapter sits within a carefully constructed theology of holiness that ultimately points toward the depths of the human condition and the grace of God's provision for cleansing.

The chapter establishes two phases of purification following childbirth. After the birth of a son, the mother is unclean for seven days (mirroring the creation week), then enters a further thirty-three days of purification. After the birth of a daughter, the periods are doubled: fourteen days of uncleanness and sixty-six days of purification. The reason for this distinction is not stated explicitly, and interpreters have offered various explanations, but the doubling may reflect the fact that a daughter will herself one day undergo these same processes of womanhood.

At the heart of this chapter is not condemnation of childbirth—which Genesis 1:28 celebrates as a divine blessing—but rather an acknowledgment of the profound connection between physical processes and Israel's holiness framework. The blood associated with childbirth, like menstrual blood, belonged to the domain of life and death that required careful handling in the presence of a holy God. This was not a moral failing but a ritual state requiring prescribed resolution.

The offering required at the end of the purification period reveals God's gracious accommodation to economic reality. The standard offering was a burnt offering (a young pigeon or turtledove) alongside a sin offering. But the law explicitly provides an alternative for the poor: if the woman cannot afford a lamb, two turtledoves or two young pigeons would suffice. This provision, sometimes called the "poor offering," appears here in its first canonical context. The grace of God never prices out the faithful—access to atonement and restoration was not reserved for the wealthy.

This chapter takes on profound New Testament significance through Mary and Joseph. Luke 2:22–24 records that after Jesus' birth, his parents brought him to the Temple to fulfill the requirements of Leviticus 12, and notably, they offered "a pair of turtledoves or two young pigeons"—the offering of the poor. The eternal Son of God entered the world in a family too humble to afford a lamb, yet he himself would become the Lamb who replaces all other offerings. The irony is stunning: the One who would render the sacrificial system obsolete was himself presented according to its requirements by a family who could only afford its least costly option.""",
        "chapter_overview": "Leviticus 12 prescribes purification rites for mothers after childbirth, establishing periods of ritual uncleanness and mandating specific sacrificial offerings—including a gracious provision for the poor—to restore the woman to full covenant standing.",
        "original_language_notes": [
            {
                "term": "טָמֵא (tame')",
                "language": "Hebrew",
                "verse": "12:2",
                "words_used": ["unclean", "impure"],
                "meaning": "Ritually impure, defiled. Tame' is the standard Hebrew term for ritual uncleanness and appears throughout the Levitical purity system. It does not carry the moral weight of sin (het) but describes a state that disqualifies a person from participation in Israel's worship. The concept operates within a symbolic framework where life, blood, and bodily processes are carefully ordered in relation to God's holiness. Tame' can be contracted by contact with death, bodily discharges, certain animals, or other listed conditions—and each has a corresponding purification procedure."
            },
            {
                "term": "קָרְבָּן (qorban)",
                "language": "Hebrew",
                "verse": "12:8",
                "words_used": ["offering", "gift"],
                "meaning": "That which is brought near, an offering. Qorban derives from the root qarab (to draw near, approach) and encompasses the range of sacrificial gifts brought to the Lord. The word appears here implicitly in the term for offering (the burnt offering and sin offering). The concept emphasizes that sacrifice is fundamentally about approach—the worshiper drawing near to a holy God through a prescribed mediating gift. Jesus criticizes the Pharisees' abuse of qorban in Mark 7:11, showing the word was still in active use in Second Temple Judaism."
            },
            {
                "term": "חַטָּאת (hatta't)",
                "language": "Hebrew",
                "verse": "12:6",
                "words_used": ["sin offering", "purification offering"],
                "meaning": "Sin offering, purification offering. From the root hata' (to sin, miss the mark), hatta't in Leviticus refers to the offering that addresses impurity and sin—particularly unintentional violations and ritual states. Modern scholarship often prefers 'purification offering' since it clarifies that this sacrifice removes defilement from both persons and the sanctuary, not merely in a moral guilt sense. For the new mother, the hatta't addresses her ritual state, not moral wrongdoing. The concept foreshadows Christ's work as our purification offering (2 Cor. 5:21)."
            },
            {
                "term": "טָהֳרָה (tohorah)",
                "language": "Hebrew",
                "verse": "12:4",
                "words_used": ["purification", "cleansing"],
                "meaning": "Purification, cleanness. From the root taher (to be clean, pure), tohorah refers to the state or process of ritual cleansing. The 'blood of purification' (v. 4–5) describes the ongoing process the new mother experiences following the initial period of uncleanness. When the days of purification are complete and the offerings are made, the priest declares her tahor (clean) and she is fully restored to covenant community life. The movement from tame' to tahor through time and sacrifice is a recurring pattern throughout Leviticus that the New Testament authors see fulfilled in Christ."
            }
        ],
        "moral_lessons": "Leviticus 12 teaches that God's grace meets human need at every economic level—the poor have equal access to atonement. It demonstrates that physical life and spiritual standing are interconnected in God's design, and that restoration always follows prescribed periods of separation. The chapter also reminds us that God cares for the vulnerable: new mothers were given protected time for recovery, a form of divine pastoral care embedded in law.",
        "application": "Christians reading this chapter are freed from its ceremonial requirements while invited to appreciate its spiritual architecture. We see in its poverty provision that God never bars access to his grace based on wealth. We see in the purification period a rhythm of rest and restoration that speaks to the physical realities of human life. Most importantly, we see through Mary's offering (Luke 2:24) that Jesus entered fully into the world of covenant obligation, not to condemn it but to fulfill it—and through him, all who trust in him are declared clean before God without any animal offering at all.",
        "prayer": "Lord, thank you that your grace has always been accessible to the poor and the humble. Thank you that Mary's poverty offering reminds us that your own Son came not in the wealth of heaven but in the humility of a family that could only afford two birds. As you declared the new mother clean through sacrifice, so declare us clean through the blood of Christ, your perfect Lamb. Teach us to rest in the purification he has accomplished, and may we walk in the cleanness that only he can give. Amen.",
        "key_points": [
            "Childbirth created a ritual state of uncleanness, not a moral failing, requiring prescribed purification.",
            "Purification periods differed for sons (40 days total) and daughters (80 days total).",
            "God graciously provided a 'poor person's offering' of two turtledoves/pigeons when a lamb was unaffordable.",
            "Mary used the poor offering after Jesus' birth (Luke 2:24), revealing the humble circumstances of the incarnation.",
            "The hatta't (sin/purification offering) removed ritual defilement and restored the mother to full covenant standing.",
            "Jesus fulfills all purification requirements, making believers permanently clean before God."
        ],
        "study_questions": [
            "Why do you think God embedded a 'poor person's offering' provision into the purification law? What does this reveal about God's character?",
            "How does Luke 2:22-24 connect to Leviticus 12, and what is significant about Mary and Joseph's use of the poverty offering?",
            "What is the difference between ritual uncleanness (tame') and moral sin in Leviticus? How does understanding this distinction change how you read this chapter?",
            "In what ways does the pattern of uncleanness → purification period → sacrifice → restoration foreshadow the gospel?",
            "How should the realities of physical life (childbirth, illness, death) shape the way we approach worship and community?"
        ],
        "tags": ["purification", "childbirth", "offerings", "ritual purity", "poverty provision", "Mary", "incarnation", "atonement"],
        "sources": ["Leviticus 12:1-8", "Luke 2:22-24", "2 Corinthians 5:21", "Genesis 1:28", "Mark 7:11"]
    },
    {
        "chapter": 13,
        "title": "Diagnosing the Unclean: Skin Diseases and Defiling Mold",
        "summary": "Leviticus 13 establishes detailed priestly procedures for diagnosing and responding to skin diseases and mold in fabric, with the priest functioning as a spiritual physician whose decisions protect the holiness and health of the covenant community.",
        "content": """Leviticus 13 is the longest chapter in Leviticus and one of the most procedurally detailed in all of Torah. It reads almost like a medical handbook, specifying the signs by which a priest was to examine and diagnose skin conditions (traditionally translated 'leprosy' but encompassing a range of skin diseases) and later, mold or fungus in fabric. While this may appear far removed from devotional literature, the chapter carries rich theological significance that the New Testament develops fully.

The governing principle throughout the chapter is that the priest—not a physician in the modern sense—served as the authority for diagnosing ritual purity. This reflects Leviticus's fundamental concern: the holiness of God's dwelling among his people. Disease and decay are associated in this priestly framework with the corruption and mortality that entered the world through sin. The priest's role was to maintain the boundaries of the holy camp.

The diagnostic criteria for skin conditions are careful and graduated. A suspicious condition prompts a seven-day quarantine, then re-examination. Conditions that spread are declared unclean; those that heal or remain confined may be clean. This measured approach prevented hasty exclusion and built in opportunities for healing and re-evaluation. The humanity of the system is often overlooked—it was not automatic exile but a careful assessment process.

The social consequences of a declaration of uncleanness were severe (vv. 45-46): torn clothes, disheveled hair, covered upper lip, and the cry "Unclean! Unclean!"—a public warning that communicated both the person's status and protected others. The unclean person was required to live outside the camp. This exclusion was not merely punitive; it protected the community and preserved the symbolic holiness of the camp where God dwelt.

The fabric section (vv. 47-59) applies similar logic to garments and woven material. Mold or 'leprous disease' in fabric was a defiling condition requiring inspection, quarantine, and if necessary, destruction of the item. The principle extended the concern for holiness beyond persons to the material culture of the community.

The New Testament places Jesus in direct confrontation with the system of Leviticus 13. The Gospels record Jesus healing multiple lepers (Matt. 8:1-4; Luke 17:11-19), and remarkably, he often touched them before healing—reversing the normal flow of contamination. Instead of the leper making Jesus unclean through contact, Jesus's holiness made the leper clean. This was a profound enacted parable: the One who is himself the holiness of God cannot be defiled; rather, he purifies whatever he touches. Jesus then sends the healed man to the priest to fulfill the Levitical requirements (Lev. 14), honoring the law while demonstrating his power to transcend its limitations.""",
        "chapter_overview": "Leviticus 13 provides comprehensive priestly diagnostic procedures for skin diseases and mold in fabric, establishing a system that protected the covenant community's ritual holiness while reflecting the broader theological reality that corruption and mortality require divine intervention for cleansing.",
        "original_language_notes": [
            {
                "term": "צָרַעַת (tsara'at)",
                "language": "Hebrew",
                "verse": "13:2",
                "words_used": ["leprosy", "leprous disease", "infectious skin disease"],
                "meaning": "A skin disease condition requiring priestly examination. Tsara'at is often translated 'leprosy' in older versions, but modern scholarship recognizes it covers a range of skin conditions—not necessarily Hansen's disease (clinical leprosy). The term can describe conditions in humans (Lev. 13), fabric (13:47-59), and even buildings (14:33-53). This wider usage suggests tsara'at is primarily a ritual category—a type of creeping corruption—rather than a specific medical diagnosis. It occurs notably in Miriam (Num. 12), Gehazi (2 Kgs. 5), and Uzziah (2 Chr. 26) in contexts connected to sin or judgment."
            },
            {
                "term": "בָּדַד (badad)",
                "language": "Hebrew",
                "verse": "13:46",
                "words_used": ["alone", "apart", "isolated"],
                "meaning": "To be alone, separated, isolated. Badad describes the enforced isolation of the person declared unclean by tsara'at. Outside the camp, alone—this is the most severe form of social exclusion in ancient Israel. The same root appears in Lamentations 1:1 ('How lonely sits the city'), describing Jerusalem's desolation after the Babylonian conquest. The leper's condition of forced isolation becomes a picture of sin's ultimate consequence: separation from community and from God. Jesus reverses this when he deliberately draws near to lepers (Matt. 8:1-4)."
            },
            {
                "term": "טָמֵא טָמֵא (tame' tame')",
                "language": "Hebrew",
                "verse": "13:45",
                "words_used": ["Unclean! Unclean!", "I am unclean"],
                "meaning": "The doubled cry of the diagnosed person: 'Unclean! Unclean!' The repetition may be emphatic (intensifying the declaration) or may reflect a formal cry—the person had to announce their status repeatedly as a public health warning. This self-declaration was both humiliating and protective of others. It has been suggested the cry was also a form of self-exclusion: the person acknowledged their own state and their exclusion from the holy community. The theological resonance is powerful—human beings apart from God are in a state requiring this same honest acknowledgment."
            },
            {
                "term": "נֶגַע (nega')",
                "language": "Hebrew",
                "verse": "13:3",
                "words_used": ["disease", "infection", "plague", "mark", "affliction"],
                "meaning": "A blow, mark, affliction, plague. Nega' is the general term for the disease conditions in Leviticus 13-14, used for both skin conditions and fabric mold. From the root naga' (to touch, strike), nega' evokes something that has struck or marked a person. The word appears 78 times in Leviticus 13-14 alone, emphasizing the pervasive concern with this class of conditions. Outside Leviticus, nega' describes plagues sent by God (Gen. 12:17; Ps. 91:10) and the 'stripes' of the Suffering Servant (Isa. 53:8), creating a rich theological echo connecting disease, divine judgment, and redemptive suffering."
            }
        ],
        "moral_lessons": "Leviticus 13 teaches that corruption must be honestly identified, not covered up. The priest's role—careful examination, quarantine when uncertain, and decisive declaration—models a pattern of discernment that applies to spiritual life. The chapter also shows that God's response to human fragility involves procedure and process, not hasty condemnation. The requirement to cry 'Unclean!' reflects the importance of honest self-awareness before God: we cannot receive cleansing if we refuse to acknowledge our need.",
        "application": "While Christians are not bound by these ceremonial laws, the principles remain spiritually instructive. We live in a world marked by corruption—physical, moral, and spiritual—and the gospel offers the ultimate diagnosis (all have sinned, Rom. 3:23) and the ultimate cure (cleansed by Christ's blood). We should be honest about sin in our own lives rather than hiding it, knowing that Christ touches the unclean not to be defiled but to heal. We should also exercise discernment in our communities—not harsh exclusion, but the kind of careful, loving examination that honors both truth and grace.",
        "prayer": "Lord, we acknowledge that we too cry 'Unclean!'—not only outwardly but in the depths of our hearts. We cannot heal ourselves or declare ourselves pure. But Jesus, the great High Priest, came near to us in our corruption and made us whole. Teach us the honesty of Leviticus 13—to see ourselves as we truly are before you—and give us faith to believe that the One who touched lepers still touches us. Thank you that in Christ, we are declared clean. Amen.",
        "key_points": [
            "Tsara'at (skin disease) in Leviticus encompasses various skin conditions, not necessarily clinical leprosy, functioning as a ritual category of corruption.",
            "The priest served as the diagnostic authority, balancing careful examination, quarantine periods, and decisive judgment.",
            "A declared unclean person faced severe social isolation—torn clothes, disheveled hair, exclusion from the camp—reflecting sin's consequences.",
            "The required cry 'Unclean! Unclean!' combined public warning with honest self-declaration.",
            "The chapter extends tsara'at to fabric/mold, showing holiness concerns extended to all areas of community life.",
            "Jesus reversed the normal dynamic: instead of lepers defiling him, his holiness cleansed them—fulfilling and transcending the law."
        ],
        "study_questions": [
            "What does the priest's role as diagnostic authority in Leviticus 13 reveal about how God structured the connection between physical and spiritual health in Israel?",
            "Why do you think the 'unclean' person was required to publicly cry out their own status? What spiritual truth might this embody?",
            "How does Jesus's practice of touching lepers (Matt. 8:1-4) radically reinterpret the purity laws of Leviticus 13?",
            "What does it mean for Christians today that 'all have sinned' (Rom. 3:23) is the universal diagnosis that Leviticus 13 symbolically represents?",
            "The chapter applies purity principles to fabric as well as people. How should we think about holiness in the material and cultural dimensions of our lives?"
        ],
        "tags": ["skin disease", "leprosy", "purity", "priest", "diagnosis", "isolation", "Jesus heals lepers", "holiness", "corruption"],
        "sources": ["Leviticus 13:1-59", "Matthew 8:1-4", "Luke 17:11-19", "Romans 3:23", "Isaiah 53:8", "Numbers 12", "Lamentations 1:1"]
    },
    {
        "chapter": 14,
        "title": "The Ritual of Restoration: Cleansing the Healed Leper",
        "summary": "Leviticus 14 describes the elaborate two-stage restoration ceremony for a person healed from skin disease, featuring the dramatic two-bird ritual and multiple offerings over eight days, concluding with rites for cleansing mold-afflicted houses—together forming one of Scripture's richest typological pictures of Christ's atoning work.",
        "content": """If Leviticus 13 is the diagnosis, Leviticus 14 is the cure—or rather, the restoration. This chapter describes the elaborate process by which a person healed from tsara'at was ceremonially cleansed and reintegrated into the covenant community. The procedures here are among the most theologically rich in all of Leviticus, containing imagery that the New Testament authors would see as foreshadowing the death and resurrection of Christ.

The restoration unfolds in two stages. The first occurs outside the camp (v. 3): a priest goes out to meet the healed person at the boundary of the community. This detail is already significant—the priest comes to where the excluded person is, a gracious outreach that reversed the exile. The priest inspects and confirms the healing, then conducts the two-bird ceremony.

The two-bird ritual (vv. 4-7) is among the most arresting in all of Leviticus. Two living birds are taken, along with cedar wood, scarlet yarn, and hyssop. One bird is killed over fresh running water in a clay pot, and its blood is used to sprinkle the healed person seven times. Then the living bird is dipped in the blood of the dead bird and released. The healed person washes, shaves, and is pronounced clean—then may re-enter the camp, though he must remain outside his tent for seven more days.

The symbolism is layered and profound. The two birds, one killed and one set free covered in blood, suggest what theologians would later call substitution and release: one bird dies so the other can go free, and the freed bird carries the blood of the dead bird into the open air. The parallels to Christ's death and resurrection are striking: Jesus died (like the first bird) and rose (like the second bird released), and through his blood our guilt is carried away. The cedar, hyssop, and scarlet yarn appear again at the crucifixion setting (hyssop was used to offer Jesus vinegar at the cross, John 19:29) and in Psalm 51:7 ("Purge me with hyssop and I shall be clean").

The second stage of restoration (vv. 10-20) occurs on the eighth day and takes place at the sanctuary. The healed person brings multiple offerings and is anointed with blood and oil—on the right ear lobe, the right thumb, and the right big toe. This anointing mirrors exactly the consecration of the priests in Leviticus 8 (covering hearing, hands, and walk—the whole life of service). The healed leper, fully restored, was consecrated afresh as a member of the holy community—welcomed not merely back but re-commissioned.

Again, a poverty provision appears: if the person cannot afford the full offering, reduced sacrifices are accepted (vv. 21-32). God's grace has no economic barrier.

The chapter concludes (vv. 33-53) with procedures for mold in houses, applying similar logic to dwellings. In the New Testament era, the household is the church (the new temple), and spiritual mold—false teaching, persistent sin—requires the same kind of careful inspection, quarantine, and if necessary, dismantling (cf. 1 Cor. 5:6-7).""",
        "chapter_overview": "Leviticus 14 describes the two-stage restoration of a healed person: a dramatic two-bird ceremony outside the camp followed by an eight-day process at the sanctuary involving multiple offerings and priestly anointing, restoring the person to full covenant membership—a profound typological preview of Christ's death, resurrection, and the believer's complete restoration.",
        "original_language_notes": [
            {
                "term": "דְּרוֹר (deror)",
                "language": "Hebrew",
                "verse": "14:7",
                "words_used": ["set free", "let go", "release"],
                "meaning": "Release, freedom, liberty. Used here for the release of the living bird after it is dipped in the blood of the slain bird. The same word appears in Leviticus 25:10 ('proclaim liberty throughout the land') on the Year of Jubilee, and in Isaiah 61:1 ('to proclaim liberty to the captives')—the text Jesus reads in Luke 4:18 to inaugurate his ministry. The connection is theologically profound: the release of the blood-covered bird in the leper's restoration ceremony is structurally identical to the proclamation of liberty—freedom achieved through blood, granted freely."
            },
            {
                "term": "אֵזוֹב (ezov)",
                "language": "Hebrew",
                "verse": "14:4",
                "words_used": ["hyssop"],
                "meaning": "Hyssop, a small aromatic plant used in purification rituals. Ezov appears in the Passover (Exod. 12:22, used to apply blood to doorposts), Psalm 51:7 ('Purge me with hyssop and I shall be clean'), and at the crucifixion (John 19:29, where a sponge soaked in vinegar is put on a hyssop branch for Jesus). This consistent connection between hyssop and blood-applied cleansing across the entire canon suggests it was a recognized symbol of purification through sacrifice."
            },
            {
                "term": "אָשָׁם (asham)",
                "language": "Hebrew",
                "verse": "14:12",
                "words_used": ["guilt offering", "reparation offering"],
                "meaning": "Guilt offering, reparation offering. The asham was offered in cases involving violation of sacred property or uncertain guilt. Its use in the leper's restoration is unusual—most purification rites do not include an asham. Its presence here may suggest that tsara'at had a punitive dimension in some cases (cf. Miriam, Uzziah, Gehazi) or that the full restoration of the formerly unclean required addressing any lingering 'debt' to holiness. Isaiah's Servant Song uses the root asham: 'when his soul makes an offering for sin/guilt (asham)' (Isa. 53:10)—a direct connection to Christ's atoning work."
            },
            {
                "term": "אֶרֶז (erez)",
                "language": "Hebrew",
                "verse": "14:4",
                "words_used": ["cedar wood"],
                "meaning": "Cedar wood. Cedar was associated with incorruption and durability (Solomon's Temple was built of cedar, 1 Kgs. 6). Its use in the purification ceremony alongside hyssop (a humble herb) creates a contrast: the durable and incorrupt (cedar) paired with the cleansing (hyssop). Together they may symbolize the comprehensive restoration of the one who was afflicted—enduring life paired with genuine cleansing."
            }
        ],
        "moral_lessons": "Leviticus 14 teaches that true restoration is both complete and costly. The healed person was not merely tolerated back into the community but fully reintegrated through a layered process of ceremony, offering, and anointing. God does not half-restore—he fully restores. The chapter also teaches that grace meets need at every economic level, and that the priest's role is to welcome back the restored, not to continue excluding them.",
        "application": "The two-bird ritual speaks powerfully to the Christian understanding of atonement: one dies so the other may go free, bearing the blood of the dead as it soars into open sky. This is the gospel in symbol: Christ died in our place, and we go free, marked by his blood. The anointing of ear, thumb, and toe is a call to full consecration—hearing God's word, working his will, and walking his path. Christians who have been 'cleansed' through Christ are not merely forgiven but re-commissioned for holy service, welcomed not as probationers but as members of his household.",
        "prayer": "Father, we marvel at the beauty of this ancient ceremony and how it foreshadows the death and resurrection of your Son. Like the bird released over open fields, we have been set free—covered in the blood of the One who died in our place. Like the healed leper anointed at the sanctuary, we have been re-commissioned for holy living. Help us live as those truly restored: with ears attuned to your word, hands extended in your service, and feet walking your path. All glory to the Lamb who was slain. Amen.",
        "key_points": [
            "Restoration occurred in two stages: outside the camp (immediate ceremonial cleansing) and at the sanctuary (full reintegration on the eighth day).",
            "The two-bird ceremony—one slain, one released bearing the blood—is a profound type of Christ's death and resurrection.",
            "Cedar, scarlet yarn, and hyssop appear across multiple purification contexts, connecting to Passover, Psalm 51, and the crucifixion.",
            "The anointing of the right ear lobe, thumb, and big toe mirrors priestly consecration—the healed person is fully re-commissioned.",
            "A poverty provision allowed reduced offerings, ensuring restoration was accessible to all.",
            "The chapter's mold-in-house procedures extend holiness principles to community dwellings, with New Testament parallels to church discipline."
        ],
        "study_questions": [
            "The priest goes outside the camp to meet the healed leper before examining him. What does this detail reveal about God's posture toward those who have been excluded and healed?",
            "Trace the two-bird ritual: one dies, one is released covered in blood. How does this foreshadow the gospel? What aspects of Christ's work does each bird represent?",
            "Why do you think the healed leper received the same anointing (ear, thumb, toe) as the priests at their ordination? What does this say about the nature of full restoration?",
            "Hyssop appears in Passover, Psalm 51, this chapter, and at the crucifixion. What does its repeated appearance across these contexts suggest about biblical typology?",
            "How does Leviticus 14's 'poverty provision' (vv. 21-32) inform our understanding of how God views socioeconomic barriers in worship and restoration?"
        ],
        "tags": ["restoration", "two birds", "atonement", "anointing", "typology", "Christ", "purification", "leper", "redemption", "consecration"],
        "sources": ["Leviticus 14:1-57", "John 19:29", "Psalm 51:7", "Isaiah 53:10", "Isaiah 61:1", "Luke 4:18", "Leviticus 25:10", "1 Kings 6", "1 Corinthians 5:6-7"]
    },
    {
        "chapter": 15,
        "title": "Bodily Discharges and the Holiness of Human Frailty",
        "summary": "Leviticus 15 addresses the ritual impurity caused by various bodily discharges—both pathological and natural—establishing purification procedures that acknowledge human physical frailty while maintaining the holiness required for life in God's presence, and pointing forward to Jesus's power to cleanse the most persistent human uncleanness.",
        "content": """Leviticus 15 is perhaps the most intimate chapter of Leviticus, addressing bodily discharges and their ritual implications. Like Leviticus 12, it may seem distant from what we consider 'spiritual' literature, but it belongs to the same comprehensive vision of holiness that governed every dimension of Israelite life. The chapter reveals a God who cares about the whole person—body and soul—and who does not distance himself from human physical reality.

The chapter addresses four categories. Two are pathological (abnormal male discharge, vv. 2-15; abnormal female discharge, vv. 25-30) and two are natural (male emission, vv. 16-18; female menstrual discharge, vv. 19-24). All four create ritual impurity—not moral sin, but a ritual state requiring resolution before the person can participate in Israel's worship.

The pathological cases carry greater weight: they require seven days of cleanness after the discharge ends, a prescribed washing, and a two-bird sacrifice (identical in structure to the post-childbirth offering). The natural cases require washing, waiting, and the passage of time—typically resolved the same evening. The graduated response reflects proportionality: greater ongoing disruption to normal bodily function creates more serious ritual implications.

The theological principle at work throughout is that human bodies are not autonomous. They belong to a created order over which God has established patterns and rhythms, and whose disruptions require attention and remedy. The holiness framework did not despise the body—which God created good (Gen. 1:31)—but recognized that in a fallen world, bodily life is marked by impermanence and mortality that must be carefully managed in the presence of a perfectly holy God.

The reason given at the close of the chapter is explicit (v. 31): God is separating the Israelites from their impurity "lest they die in their uncleanness by defiling my tabernacle." This was not arbitrary. The tabernacle was the dwelling place of the living God; approaching it in a state of uncleanness could be fatal (cf. Nadab and Abihu, Lev. 10). The purification laws were acts of divine mercy—protecting Israel from the dangerous consequences of unregulated access to the holy.

The most powerful New Testament echo of Leviticus 15 comes in Mark 5:25-34 and Luke 8:43-48: the woman who had 'a discharge of blood for twelve years.' Her condition under Leviticus 15 meant twelve years of chronic ritual impurity—unable to fully participate in worship, touching others transferred impurity, a social and spiritual isolation nearly as severe as leprosy. Yet in a crowd, she reached out and touched the hem of Jesus's garment. Jesus did not recoil or become unclean. He turned and said, 'Your faith has made you well.' In that moment, he healed not only her body but restored her full place in the covenant community—and he did it by contact, not quarantine.""",
        "chapter_overview": "Leviticus 15 establishes purification procedures for both pathological and natural bodily discharges, reflecting the holiness framework that governed all of Israelite life and pointing forward to Jesus's revolutionary healing of a woman whose chronic discharge had rendered her ritually impure for twelve years.",
        "original_language_notes": [
            {
                "term": "זָב (zav)",
                "language": "Hebrew",
                "verse": "15:2",
                "words_used": ["discharge", "flow", "issue", "man with a discharge"],
                "meaning": "One who has a discharge, a flow. Zav (masculine) and zavah (feminine, v. 25) are the technical terms for persons experiencing abnormal discharges. The root zub means to flow, ooze, leak—and is also used in 'land flowing with milk and honey' (where abundance flows freely). In the case of bodily discharge, the same root describes a condition that must be brought under the holiness protocols. The zav's condition was severe: whoever he touched, whatever he sat or lay on, transferred impurity—a kind of 'contamination radius' that required constant vigilance."
            },
            {
                "term": "נִדָּה (niddah)",
                "language": "Hebrew",
                "verse": "15:19",
                "words_used": ["menstrual impurity", "her period", "menstruation"],
                "meaning": "Menstrual separation, the state of menstrual impurity. Niddah derives from a root meaning to remove or separate, reflecting the temporary separation required during menstruation. The niddah state lasted seven days and was one of the most frequently encountered forms of ritual impurity for Israelite women. Ezekiel uses niddah metaphorically for Israel's spiritual unfaithfulness (Ezek. 36:17), and the rabbis developed extensive tractates on niddah practice. The concept reflects how Israel's entire life was ordered by rhythms of separation and reintegration that pointed to the holy God in their midst."
            },
            {
                "term": "שָׁכַב (shakav)",
                "language": "Hebrew",
                "verse": "15:4",
                "words_used": ["lies", "bed", "sleeps on"],
                "meaning": "To lie down, to sleep. Used here for anything the zav lies on, which becomes unclean. The verb is common and covers both sleep and sexual relations (a euphemism throughout the OT). Its use here in the context of contagious impurity emphasizes how the zav's condition affected even resting—there was no neutral space in his environment. The comprehensive reach of impurity across furniture, clothing, and persons illustrates how seriously the holiness system took the management of unclean states."
            },
            {
                "term": "מִקְוֶה (miqveh)",
                "language": "Hebrew",
                "verse": "15:13",
                "words_used": ["running water", "flowing water", "collection of water"],
                "meaning": "A gathering of water, a pool; specifically flowing or 'living' water (mayim hayyim, v. 13). Most purification rites required bathing in water, ideally flowing water, which carried the impurity away. The miqveh became the cornerstone of Jewish ritual bath practice—the immersion pool required to transition from impure to pure states. The miqveh tradition underlies John the Baptist's baptism in the Jordan (running, living water), itself connected to the idea of ritual cleansing. Christian baptism inherits this tradition while transforming it: not symbolic removal of ritual impurity but real participation in Christ's death and resurrection."
            }
        ],
        "moral_lessons": "Leviticus 15 teaches that human physical life in all its frailty and complexity belongs within the care of God's ordering. It teaches that impurity requires acknowledgment and remedy rather than denial, and that God provides specific, accessible means of restoration. The chapter also teaches the comprehensive reach of holiness: it extends to the most private and personal dimensions of life, not as an invasion but as a protection.",
        "application": "Christians reading Leviticus 15 are freed from its ceremonial requirements through Christ, but the chapter's spiritual logic speaks powerfully. The woman with the chronic discharge (Mark 5) shows that Jesus reaches into the most socially marginalized, physically intimate dimensions of human brokenness and restores people completely. No condition—however personal, however long-standing, however embarrassing—lies beyond his power to heal and restore. The miqveh tradition also reminds us that baptism is not merely symbolic: it is a real act of cleansing tied to the living water of the Spirit (John 7:38).",
        "prayer": "Lord, you are not squeamish about the fullness of human life. You wrote laws about our most intimate physical realities, and you sent your Son to touch the untouchable and heal the unhealable. Like the woman who had suffered for twelve years, we press through the crowd with our persistent uncleanness—physical, emotional, spiritual—and reach out to touch your hem. You do not recoil. You heal. Thank you that in Christ there is no discharge, no flow, no condition that can separate us from your love. Amen.",
        "key_points": [
            "Leviticus 15 addresses four categories: pathological male discharge, natural male emission, normal female menstruation, and pathological female discharge.",
            "Pathological conditions required more extensive purification (seven days, washing, two-bird sacrifice) than natural processes (washing, waiting until evening).",
            "The holiness framework was not anti-body but recognized that fallen bodily life required management in God's holy presence.",
            "The stated purpose (v. 31) was protection: preventing Israel from dying by defiling the tabernacle where God dwelt.",
            "The woman with the twelve-year discharge (Mark 5) embodied what this chapter describes—and Jesus healed her through touch, reversing the normal flow of impurity.",
            "The miqveh (ritual bath) tradition underlying this chapter informed Jewish and Christian baptismal practice."
        ],
        "study_questions": [
            "Why do you think God included such detailed laws about bodily functions in the Torah? What does this reveal about the scope of holiness in God's design?",
            "The chapter states its purpose in verse 31: to prevent Israel from dying by defiling God's tabernacle. How does understanding this protective intent change how you read the purity laws?",
            "The woman in Mark 5 had lived with a condition described in Leviticus 15 for twelve years. What was her life like socially and spiritually under these laws? What was the significance of Jesus healing her through touch?",
            "How does the concept of miqveh (ritual immersion in living water) connect to John the Baptist's ministry and Christian baptism?",
            "What conditions in your own life—physical, emotional, or spiritual—feel most like the chronic discharge of Leviticus 15? How does the woman's story speak to those areas?"
        ],
        "tags": ["bodily discharge", "purity", "menstruation", "holiness", "human frailty", "healing", "woman with blood issue", "baptism", "miqveh", "restoration"],
        "sources": ["Leviticus 15:1-33", "Mark 5:25-34", "Luke 8:43-48", "John 7:38", "Ezekiel 36:17", "Genesis 1:31"]
    },
    {
        "chapter": 16,
        "title": "The Day of Atonement: Israel's Most Sacred Day",
        "summary": "Leviticus 16 describes Yom Kippur—the Day of Atonement—Israel's most solemn annual ceremony in which the high priest alone entered the Holy of Holies to make atonement for the entire nation, incorporating the remarkable scapegoat ritual that carried Israel's sins away, all of which the book of Hebrews identifies as the supreme type of Christ's once-for-all sacrifice.",
        "content": """Leviticus 16 stands at the theological center of the entire Pentateuch. It describes Yom Kippur—the Day of Atonement—the single most important day in Israel's liturgical calendar, when the high priest entered the Holy of Holies to make atonement for the whole nation. What unfolds in this chapter is nothing less than God's most elaborate pre-Christian demonstration of the atoning work his Son would accomplish.

The chapter opens by connecting back to the deaths of Nadab and Abihu (Lev. 10:1-2), who died for unauthorized entry into the holy place. God's first word to Aaron after their deaths is both warning and provision: the high priest may enter the Most Holy Place, but only once a year, only after elaborate preparation, and only behind a cloud of incense that would shield him from the divine glory. The holy God is unapproachably dangerous in himself; he provides the terms of safe approach.

Aaron's preparatory rituals are extensive. He must bathe entirely, dress in plain white linen (not the magnificent high priestly robes of Exodus 28—this was a day of humility, not display), and offer a bull for his own sin and his family's before he can serve as mediator for the people. No one may be in the tent of meeting when he enters (v. 17). This is the loneliest moment in Israel's liturgical year: the high priest, utterly alone, bearing the sins of the nation.

The centerpiece of the ritual involves two goats. Lots are cast to determine which goat will be 'for the LORD' (a sacrifice) and which will be 'for Azazel' (the scapegoat). The first goat is slaughtered, and its blood is brought into the Holy of Holies and sprinkled on and before the mercy seat (the kapporet, vv. 14-15). The blood of atonement was brought into the very presence of God—the life given in the place where God's glory dwelt.

The second goat—the scapegoat—is perhaps the most memorable image in the chapter. Aaron lays both hands on the living goat and confesses over it all the iniquities, transgressions, and sins of Israel. The goat then carries all their sins into the wilderness, to 'a remote area' (or 'to Azazel'—the meaning of this term is debated, but it is clearly a place of utter removal). The sin is not merely covered—it is removed, sent away, placed on another.

The two-goat ritual embodies two complementary aspects of atonement: the first goat demonstrates that sin requires the payment of life (blood must be shed); the second goat demonstrates that sin is taken away from the people, not merely suppressed. Both aspects find their fulfillment in Christ, who by one sacrifice 'has perfected for all time those who are being sanctified' (Heb. 10:14).

The book of Hebrews (chapters 9-10) develops Leviticus 16 at length. Christ is both the High Priest and the sacrifice: he enters not the earthly Holy of Holies 'made with hands' but into heaven itself, into the very presence of God (Heb. 9:24), 'not by means of the blood of goats and calves but by means of his own blood, thus securing an eternal redemption' (Heb. 9:12). And where the Levitical high priest had to repeat this ceremony every year (proof that the former sacrifices could not truly take away sin, Heb. 10:3-4), Christ entered once for all—his single sacrifice achieving what all the Yom Kippur ceremonies could only symbolize.

The Day of Atonement ends with the entire community observing a sabbath of complete rest and self-denial. Israel waited in humility while their representative alone bore their cause before God. The congregation's posture—waiting, fasting, trusting—is the posture of faith itself.""",
        "chapter_overview": "Leviticus 16 prescribes the annual Day of Atonement ceremony, in which the high priest alone entered the Holy of Holies to atone for Israel's sins through elaborate sacrificial rites and the remarkable scapegoat ritual—a ceremony that the New Testament (especially Hebrews 9-10) presents as the most complete Old Testament type of Christ's once-for-all atoning sacrifice.",
        "original_language_notes": [
            {
                "term": "כִּפֻּר (kippur)",
                "language": "Hebrew",
                "verse": "16:30",
                "words_used": ["atonement", "make atonement", "Day of Atonement"],
                "meaning": "Atonement, covering, propitiation. Yom Kippur (Day of Atonement) takes its name from this word. The root kaphar means to cover, appease, make atonement. Debate continues over whether the primary meaning is 'to cover' (sin is hidden) or 'to wipe away' (sin is removed) or 'to ransom' (sin is paid for). The range of uses suggests all three ideas: the kapporet (mercy seat, same root) is the place where blood is applied, covering the ark containing the law. Kippur appears 16 times in this chapter, making it the densest concentration of atonement language in the Bible."
            },
            {
                "term": "כַּפֹּרֶת (kapporet)",
                "language": "Hebrew",
                "verse": "16:2",
                "words_used": ["mercy seat", "atonement cover", "cover"],
                "meaning": "The cover of the ark of the covenant, the place where the blood of atonement was sprinkled. Often translated 'mercy seat' (KJV, following Luther's Gnadenstuhl) or 'atonement cover' (NIV). The LXX renders it hilasterion (propitiation, place of propitiation)—the same word Paul uses in Romans 3:25 for Jesus: 'God put forward [Christ] as a propitiation (hilasterion) by his blood.' The kapporet was thus the precise typological counterpart of Christ himself: the place where atoning blood was applied in God's very presence."
            },
            {
                "term": "עֲזָאזֵל (azazel)",
                "language": "Hebrew",
                "verse": "16:8",
                "words_used": ["Azazel", "scapegoat", "goat of removal"],
                "meaning": "The term for the goat sent away carrying Israel's sins. The precise meaning of azazel is debated: it may mean 'the goat that departs/escapes' (hence 'scapegoat'), or it may be a place name (a rocky wilderness location), or possibly a demonic being to whom the sins are symbolically returned. The most likely reading is that azazel refers to complete removal—the sin-bearing goat is sent to a place of total absence, utter separation from the community. The theological point is clear regardless of the etymology: Israel's sins were not merely covered but removed, sent away into the wilderness of no return."
            },
            {
                "term": "סָמַךְ (samakh)",
                "language": "Hebrew",
                "verse": "16:21",
                "words_used": ["lay hands on", "press hands on", "lean hands on"],
                "meaning": "To lay, press, or lean hands on. The act of Aaron pressing both hands on the scapegoat's head was the act of transference: the sins of Israel were symbolically placed upon the goat. Samakh appears throughout Leviticus for the worshiper laying hands on the head of the sacrifice before it is killed—an act of identification and substitution. The action anticipates what Isaiah 53 describes: 'the LORD has laid on him the iniquity of us all' (Isa. 53:6), using a different verb but the same theological concept of sin-transference."
            }
        ],
        "moral_lessons": "Leviticus 16 teaches that sin is genuinely serious—it requires elaborate atonement, the shedding of blood, and the removal of guilt from the community. It teaches that access to a holy God is mediated through a representative (the high priest), and that atonement must be both divinely provided and humanly received through faith and self-humbling. It also teaches that genuine atonement removes sin entirely—not merely covers it—a promise fulfilled only in Christ.",
        "application": "Yom Kippur was Israel's annual reminder that their standing before God was not based on their performance but on a sacrifice made on their behalf. Every year the ceremony declared: you are still sinners, but God has provided atonement. Christ's single sacrifice declares the same thing once and for all: we are sinners, but God has provided permanent atonement in his Son. Christians need not observe Yom Kippur—Christ has fulfilled it—but we do well to meditate on its imagery: the high priest alone before God bearing our cause, the blood applied to the mercy seat, the scapegoat carrying our guilt into the wilderness of no return. This is the gospel in ceremony.",
        "prayer": "Holy God, we would not dare approach you on our own. Even the high priest could only enter your presence once a year, behind incense, with atoning blood. But you have opened the way through your Son, our Great High Priest, who entered once for all into the true Holy of Holies with his own blood and secured our eternal redemption. We receive this atonement by faith—our hands symbolically on his head, our sins transferred to the One who bore them away. On this side of the cross, Yom Kippur is not a trembling hope but a confident reality. Thank you for the blood that speaks better things than Abel's. Amen.",
        "key_points": [
            "Yom Kippur (Day of Atonement) was Israel's most solemn annual ceremony, occurring once per year on the tenth day of the seventh month.",
            "The high priest alone entered the Holy of Holies, dressed in plain white linen, after bathing and offering a bull for his own sins.",
            "The two-goat ritual: one goat sacrificed (blood brought into the Holy of Holies), one goat sent into the wilderness bearing Israel's confessed sins (the scapegoat).",
            "The kapporet (mercy seat/atonement cover) was the place where atoning blood was applied—Paul identifies Jesus as the hilasterion (same concept) in Romans 3:25.",
            "Hebrews 9-10 presents Christ as both High Priest and sacrifice who entered heaven itself once for all, achieving what Yom Kippur could only symbolize annually.",
            "The entire nation observed a 'sabbath of complete rest' and self-denial, trusting in their representative's work before God—the posture of faith."
        ],
        "study_questions": [
            "Why do you think the high priest had to wear plain white linen instead of his magnificent robes on this one day? What does this tell us about the Day of Atonement?",
            "The two-goat ritual embodies two aspects of atonement: payment (first goat) and removal (scapegoat). How do both aspects find their fulfillment in Christ?",
            "Hebrews 9:12 says Christ entered 'not by means of the blood of goats and calves but by means of his own blood.' What makes Christ's sacrifice categorically different from the Yom Kippur ceremony?",
            "Paul calls Jesus a hilasterion (Romans 3:25)—the same Greek word the LXX uses for the kapporet (mercy seat). What does this identification mean for our understanding of Christ's atonement?",
            "The entire community waited in fasting and self-humbling while the high priest alone entered the Holy of Holies. How does this image of waiting trust connect to the Christian life of faith?"
        ],
        "tags": ["Day of Atonement", "Yom Kippur", "scapegoat", "mercy seat", "high priest", "atonement", "blood", "Christ", "Hebrews", "typology", "sacrifice", "Holy of Holies"],
        "sources": ["Leviticus 16:1-34", "Hebrews 9:1-28", "Hebrews 10:1-18", "Romans 3:25", "Isaiah 53:6", "Leviticus 10:1-2"]
    }
]

def get_or_create_collection(cur):
    cur.execute("SELECT id FROM commentary_collections WHERE slug='believers-sword-commentaries'")
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        "INSERT INTO commentary_collections (name, slug, language_code, description) VALUES (?,?,?,?)",
        (COLLECTION_NAME, "believers-sword-commentaries", "en", "Believers Sword Bible Commentaries")
    )
    return cur.lastrowid

def chapter_exists(cur, collection_id, book_id, chapter):
    cur.execute(
        """SELECT id, content FROM commentary_entries
           WHERE collection_id=? AND book_id=? AND chapter=? AND language_code='en'
           AND reference_scope='chapter' AND deleted_at IS NULL""",
        (collection_id, book_id, chapter)
    )
    row = cur.fetchone()
    if not row:
        return False
    content = row[1] or ""
    return len(content) > 500

def insert_entry(cur, collection_id, data, chapter):
    entry_uuid = str(uuid.uuid4())
    key_points_json = json.dumps(data["key_points"])
    study_questions_json = json.dumps(data["study_questions"])
    word_count = len(data["content"].split())
    cur.execute(
        """INSERT INTO commentary_entries
           (uuid, collection_id, book_id, chapter, verse_start, verse_end,
            reference_scope, title, summary, content, application, prayer,
            key_points, study_questions, language_code, theological_perspective,
            status, is_ai_generated, word_count, created_at, updated_at)
           VALUES (?,?,?,?,NULL,NULL,?,?,?,?,?,?,?,?,?,?,?,1,?,?,?)""",
        (entry_uuid, collection_id, BOOK_ID, chapter, "chapter",
         data["title"], data["summary"], data["content"],
         data["application"], data["prayer"],
         key_points_json, study_questions_json,
         LANGUAGE_CODE, "evangelical", "draft", word_count, NOW, NOW)
    )
    return entry_uuid, cur.lastrowid

def save_json(data, chapter, entry_uuid):
    chapter_dir = os.path.join(GENERATED_DIR, BOOK_DIR)
    os.makedirs(chapter_dir, exist_ok=True)
    filename = os.path.join(chapter_dir, f"{chapter:02d}.json")
    output = {
        "uuid": entry_uuid,
        "collection_name": COLLECTION_NAME,
        "author_type": "ai",
        "language_code": LANGUAGE_CODE,
        "theological_perspective": "evangelical",
        "status": "draft",
        "book_id": BOOK_ID,
        "book": BOOK,
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
        "sources": data["sources"],
        "created_at": NOW,
        "updated_at": NOW
    }
    # Verify no forbidden keys
    forbidden = {"is_ai_generated", "model_name", "prompt_version"}
    assert not (forbidden & set(output.keys())), f"Forbidden keys found: {forbidden & set(output.keys())}"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    # Verify it parses back
    with open(filename, "r", encoding="utf-8") as f:
        parsed = json.load(f)
    assert not (forbidden & set(parsed.keys())), "Forbidden keys in parsed output"
    return filename

def update_progress(conn, next_chapter, last_chapter):
    # Determine what comes next
    if last_chapter >= 27:  # Leviticus has 27 chapters
        next_book_id = 4
        next_book = "Numbers"
        nc = 1
    else:
        next_book_id = BOOK_ID
        next_book = BOOK
        nc = next_chapter

    progress = {
        "next_book_id": next_book_id,
        "next_book": next_book,
        "next_chapter": nc,
        "last_completed_book_id": BOOK_ID,
        "last_completed_book": BOOK,
        "last_completed_chapter": last_chapter,
        "completed": False,
        "updated_at": NOW
    }
    with open(PROGRESS_JSON, "w") as f:
        json.dump(progress, f, indent=2)

    cur = conn.cursor()
    cur.execute("SELECT id FROM commentary_generation_progress LIMIT 1")
    row = cur.fetchone()
    if row:
        cur.execute(
            """UPDATE commentary_generation_progress SET
               next_book_id=?, next_book=?, next_chapter=?,
               last_completed_book_id=?, last_completed_book=?, last_completed_chapter=?,
               completed=0, updated_at=?""",
            (next_book_id, next_book, nc, BOOK_ID, BOOK, last_chapter, NOW)
        )
    else:
        cur.execute(
            """INSERT INTO commentary_generation_progress
               (next_book_id, next_book, next_chapter, last_completed_book_id,
                last_completed_book, last_completed_chapter, completed, updated_at)
               VALUES (?,?,?,?,?,?,0,?)""",
            (next_book_id, next_book, nc, BOOK_ID, BOOK, last_chapter, NOW)
        )
    conn.commit()
    return progress

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
    cur = conn.cursor()

    collection_id = get_or_create_collection(cur)
    conn.commit()

    generated_count = 0
    skipped_count = 0
    db_rows_inserted = 0
    files_written = []
    last_chapter = None
    start_ref = None

    for data in COMMENTARIES:
        chapter = data["chapter"]
        ref = f"{BOOK} {chapter}"
        if start_ref is None:
            start_ref = ref

        if chapter_exists(cur, collection_id, BOOK_ID, chapter):
            print(f"  SKIP: {ref} already exists with content")
            skipped_count += 1
            last_chapter = chapter
            continue

        entry_uuid, entry_id = insert_entry(cur, collection_id, data, chapter)
        conn.commit()
        db_rows_inserted += 1

        filepath = save_json(data, chapter, entry_uuid)
        files_written.append(filepath)
        generated_count += 1
        last_chapter = chapter
        print(f"  DONE: {ref} -> {filepath} (uuid={entry_uuid})")

    end_ref = f"{BOOK} {last_chapter}" if last_chapter else start_ref

    next_chapter = (last_chapter or 11) + 1
    progress = update_progress(conn, next_chapter, last_chapter)
    conn.close()

    append_log(
        batch_id=BATCH_UUID,
        start_ref=start_ref,
        end_ref=end_ref,
        generated=generated_count,
        skipped=skipped_count,
        inserted=db_rows_inserted,
        files=files_written
    )

    print(f"\n=== SUMMARY ===")
    print(f"Generated: {generated_count}, Skipped: {skipped_count}")
    print(f"DB rows inserted: {db_rows_inserted}")
    print(f"Files written: {files_written}")
    print(f"Next starting reference: {progress['next_book']} {progress['next_chapter']}")
    print(f"Batch UUID: {BATCH_UUID}")

if __name__ == "__main__":
    main()
