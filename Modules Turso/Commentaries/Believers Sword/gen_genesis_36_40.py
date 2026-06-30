#!/usr/bin/env python3
"""Generate Genesis chapters 36-40 commentaries."""

import sqlite3, json, uuid, os, datetime, pathlib

DB_PATH = "believers_sword_commentaries.db"
GEN_DIR = pathlib.Path("generated/01-genesis")
GEN_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = "commentary_generation_log.jsonl"
PROGRESS_FILE = "commentary_generation_progress.json"
COLLECTION_ID = 1
BATCH_UUID = str(uuid.uuid4())

COMMENTARIES = [
    {
        "book_id": 1,
        "book": "Genesis",
        "chapter": 36,
        "title": "Genesis 36 — The Generations of Esau: Nations from the Rejected Line and the Sovereignty Behind the Ledger",
        "summary": "Genesis 36 catalogues the descendants of Esau/Edom in detail: his wives, his sons, the chiefs of Edom, the kings of Edom before any king ruled Israel, and the chiefs of Seir the Horite. The chapter is a genealogical digression from the Jacob-Joseph narrative, but its theological weight is substantial: God keeps His promise to Esau too, and the nations emerging from him are real, with kings and borders, long before Israel has either.",
        "content": """Genesis 36 is one of the Bible's great genealogical chapters — dense with names, easy to skim, and often skipped. But its placement, content, and theological function are deliberate. Having closed the Jacob narrative at the death of Isaac (35:29), the author pauses before Joseph's story to account fully for Esau's line. This is the pattern of Genesis: the non-elect line is dismissed with a complete genealogy before the narrative zooms in on the covenant heir. Ishmael's genealogy (25:12–18) precedes Isaac's story; Esau's genealogy here precedes Joseph's story. The Bible is careful to show that God's non-election of Esau does not mean Esau is nothing.

The chapter opens with the customary formula: "These are the generations of Esau (that is, Edom)" (v. 1). Esau is Edom — the reddish, rugged terrain of the territory he occupied southeast of Canaan, and the people who descended from him. The name Edom ("red") may recall the red stew of 25:30 or simply describe the land's iron-rich soil. Either way, Esau has become a people and a geography.

Esau's wives are listed (vv. 2–3): Adah daughter of Elon the Hittite, Oholibamah daughter of Anah the Hivite, and Basemath daughter of Ishmael. A comparison with chapter 26 and 28 shows discrepancies in wives' names between this chapter and the earlier narrative (e.g., in 26:34 Esau's wives are listed with different names). Scholars note that the ancient world frequently used multiple names or that editors have harmonized different source traditions. The discrepancy is real, but it does not affect the theological point: Esau married Canaanite women (a grief to his parents, 26:35) and one Ishmaelite woman. His household was mixed — outside the pure Abrahamic line.

His sons (vv. 4–5): Eliphaz from Adah, Reuel from Basemath, Jeush, Jalam, and Korah from Oholibamah. Five sons — and from Eliphaz will come Amalek (v. 12), Israel's perpetual enemy, through a concubine Timna. Amalek is a footnote here; he will fill pages in Exodus, Numbers, Deuteronomy, Judges, and 1 Samuel. The entire career of Amalek as Israel's harasser, and Saul's fatal failure to destroy him, traces genealogically to this verse.

The chiefs (alluphim) of Esau are listed in verses 15–19 — the clan-chiefs of the Edomite confederacy. The word alluph is usually translated "chief" or "duke" and refers to a tribal leader of a thousand-strong clan unit. Fourteen chiefs from Esau's sons. Then the Horite chiefs (vv. 20–30), the indigenous population of Seir whom Esau's descendants displaced or absorbed (Deut. 2:12,22). The Horites are pre-Edomite, and their genealogy is included because the Edomite nation is partly Horite by mixture. Again: precision and completeness.

The most theologically loaded section is verses 31–39: "These are the kings who reigned in the land of Edom, before any king reigned over the Israelites." Eight kings are listed, each from different lineages (not dynastic succession), each dying without passing the throne to a son. This is a list of Edom's pre-Israelite monarchs — and its theological significance is enormous. Edom had kings before Israel did. Esau's descendants were organized politically and royally long before Jacob's descendants. This inverts human expectations: the rejected line appears to prosper first. But the list ends: eight kings, and no dynasty. None established an enduring kingdom; none ruled father to son. When Israel finally receives its king (Saul, then David), Edom will become Israel's vassal (2 Sam. 8:14). The nations that appear first in strength often do not endure.

The very existence of this chapter is a testimony to God's general grace. God promised Abraham that from him would come "a multitude of nations" (17:4–5), and Esau's progeny are part of that multiplication. God said to Rebekah about the twins, "Two nations are in your womb" (25:23). Chapter 36 is the fulfillment of the "two nations" for Esau. His line is real, substantial, and recognized — not annihilated, not cursed into nothing. They have chiefs, kings, and territory. God's covenant with the elect (Abraham-Isaac-Jacob) does not cancel God's general blessing on those outside the covenant line. Esau was not saved by the covenant promises, but he was not abandoned by the creating God either.

The chapter also quietly prepares for the Joseph narrative. By placing Esau's complete record here, the author signals closure: Esau's story is done; his descendants are accounted for. What remains is the question of Jacob's descendants — and specifically, how twelve sons become twelve tribes and eventually a nation. Genesis 37 turns immediately to Joseph, and the narrative never looks back at Esau again until the prophets (especially Obadiah and Malachi) will take up the Edom-Israel relationship. The great genealogical chapter is thus a hinge — it closes one story and opens another, while reminding the reader that God operates on a larger canvas than any single elect line.""",
        "chapter_overview": "Genesis 36 lists the descendants of Esau (Edom): his wives, sons, the clan-chiefs of Edom, the pre-Edomite Horite chiefs, and the eight kings of Edom who ruled before any king reigned over Israel. The chapter closes the Esau narrative before turning to Joseph's story, demonstrating that God kept His promise to make Esau a great nation even outside the covenant line.",
        "original_language_notes": [
            {
                "term": "אַלּוּף (alluph)",
                "language": "Hebrew",
                "verse": 15,
                "words_used": ["alluph", "alluphe"],
                "meaning": "Chief, clan-leader, or duke — from the root for a thousand (eleph), meaning a leader of a thousand-person clan unit. Used 13 times in this chapter alone. The word describes the sub-royal tribal heads of Edom's confederate structure, different from a king (melek)."
            },
            {
                "term": "אֱדוֹם (Edom)",
                "language": "Hebrew",
                "verse": 1,
                "words_used": ["Edom"],
                "meaning": "Red — the name Esau is given and the territory he inhabits southeast of Canaan, known for its red sandstone landscape. Connected to the red (adom) stew of 25:30. Edom becomes the national name of Esau's descendants throughout the Hebrew Bible."
            },
            {
                "term": "מֶלֶךְ (melek)",
                "language": "Hebrew",
                "verse": 31,
                "words_used": ["melek", "melakhim"],
                "meaning": "King — the chapter's most provocative word in context. 'These are the kings who reigned in Edom before any king reigned over Israel.' The kings of Edom predate Israel's monarchy by generations. The observation points to God's longer timeline: early advantage does not mean ultimate blessing."
            }
        ],
        "moral_lessons": "God's election of some does not mean abandonment of others — Esau receives national prosperity and kings. Genealogies in Scripture are not filler; they are theology in list form, showing God's faithfulness across generations. Amalek, Israel's enduring enemy, traces to a single concubine in this list — small beginnings have long consequences. Human organizational achievement (kings, chiefs, borders) is not the same as covenant blessing. The rejected line's early success should not cause the covenant people to lose faith in God's longer arc.",
        "application": "When God's people appear to lag behind the world — when ungodly nations seem to prosper while believers struggle — Genesis 36 provides a corrective. Esau had kings when Israel had none. But the covenant promise, not the temporary ledger of power, is what endures. Trust God's faithfulness over long timelines, not short ones. Also: small compromises (Esau's Canaanite marriages) shape entire generational legacies. And don't skip the genealogies — in them, God is accounting for every person in His story.",
        "prayer": "Lord, You are faithful to Your promises across generations I cannot see. When the ungodly seem to prosper and Your covenant people seem weak, give me faith to trust Your longer arc. Teach me that You account for every life — even those outside the covenant receive Your general grace. Keep me faithful to my own calling, trusting that Your election is not cruelty toward those You have not chosen, but specific love toward those You have. Help me not to compromise with what You have called me to leave behind. Amen.",
        "key_points": [
            "Genesis 36 records the complete genealogy of Esau/Edom — the non-elect twin — before the Joseph narrative begins.",
            "God fulfilled His promise to make Esau a great nation: chiefs, kings, and territory are all documented.",
            "Edom had eight kings before Israel had any king — demonstrating that temporal prosperity does not equal covenant blessing.",
            "Amalek, Israel's greatest early enemy, descends from Esau's grandson through a concubine Timna.",
            "The genealogical pattern of Genesis (Ishmael before Isaac, Esau before Joseph) signals closure of one line before focusing on the covenant heir.",
            "God's election of the covenant line (Abraham-Isaac-Jacob) does not eliminate His general blessing on those outside it."
        ],
        "study_questions": [
            "Why does Genesis devote an entire chapter to Esau's descendants? What does this say about the scope of God's concern?",
            "What is theologically significant about the statement 'before any king reigned over Israel' in verse 31?",
            "How does Amalek's appearance in this genealogy explain later events in Exodus and 1 Samuel?",
            "What does the pattern of Genesis (non-elect line fully chronicled, then set aside before covenant line continues) teach about biblical narrative structure?",
            "How should Genesis 36 shape how we view people who are outside the covenant community today?"
        ],
        "tags": ["Genesis", "Esau", "Edom", "genealogy", "election", "God's sovereignty", "nations", "Amalek", "kings of Edom"],
        "sources": ["Genesis 36", "Genesis 25:12-18", "Genesis 25:30", "Genesis 26:34-35", "Deuteronomy 2:12", "2 Samuel 8:14", "Obadiah 1"]
    },
    {
        "book_id": 1,
        "book": "Genesis",
        "chapter": 37,
        "title": "Genesis 37 — Joseph the Dreamer: Favoritism, Envy, and the God Who Hides Providence in a Pit",
        "summary": "Jacob loves Joseph above all his sons and gives him a distinctive robe. Joseph dreams twice of his brothers bowing to him and reports both dreams to his family, deepening his brothers' hatred. Jacob sends Joseph to check on his brothers in Dothan. The brothers see him coming and plot to kill him; Reuben persuades them to throw him in a pit instead. When Ishmaelite/Midianite traders pass, Judah suggests selling Joseph for twenty pieces of silver. The brothers dip Joseph's robe in goat's blood and show it to Jacob, who mourns inconsolably. Joseph is taken to Egypt and sold to Potiphar, captain of Pharaoh's guard.",
        "content": """Genesis 37 is one of the most carefully crafted narratives in all of Scripture. It launches what is often called "the Joseph story" — a novella-length, psychologically rich account of betrayal, exile, suffering, and providential reversal that occupies the final quarter of Genesis (chs. 37–50). But chapter 37 is not simply a story about sibling rivalry. It is the first chapter in a sustained theological argument about how God works in and through human evil to accomplish purposes no human would choose or see coming.

The chapter opens with an abrupt marker: "Jacob lived in the land of his father's sojournings, in the land of Canaan" (v. 1). This is a reset — Jacob is settled, in Canaan, at the end of the patriarchal wandering. Then immediately: "These are the generations of Jacob. Joseph, being seventeen years old, was pasturing the flock with his brothers" (v. 2). The formula "these are the generations" (toledot) appears ten times in Genesis, each time introducing a major section. Here, the "generations of Jacob" are dominated by Joseph. The son becomes the narrative.

Jacob's favoritism is stated immediately and without apology: "Israel loved Joseph more than any other of his sons, because he was the son of his old age. And he made him a robe of many colors" (v. 3). The "robe of many colors" (Hebrew: kuttoneth passim) is debated — it may mean a long-sleeved robe, a richly ornamented garment, or a multicolored coat. Whatever its precise form, it was a garment that marked Joseph as set apart — exempt from labor, marked for leadership, visually distinguished from his brothers. It is the emblem of favoritism, and its consequences are immediate: "But when his brothers saw that their father loved him more than all his brothers, they hated him and could not speak peaceably to him" (v. 4). Favoritism poisons family systems. Jacob, who had been the victim of parental favoritism (Isaac preferred Esau, Rebekah preferred Jacob), now becomes its perpetrator. The pattern of partial love in the patriarchal family has not been healed; it has been transmitted.

Joseph's dreams (vv. 5–11) are the theological core of the chapter. In the first dream, the brothers' sheaves bow to Joseph's sheaf. In the second, the sun, moon, and eleven stars bow to Joseph. The dreams are transparent — Joseph's eventual authority over his brothers (and even, symbolically, his parents) is announced. Joseph reports both dreams to his family, and the text is careful not to tell us his motive. Is he naive? Arrogant? Obedient to a prompting he doesn't understand? The text doesn't say. The brothers' hatred increases; even Jacob rebukes him — but then "his father kept the saying in mind" (v. 11). Jacob's rebuke does not erase his recognition that something may be here. He has seen divine dreams before (28:12).

The plot turns at verse 12. Jacob sends Joseph to check on his brothers in Shechem — the very place of Dinah's assault and the massacre of chapter 34. The choice to send the favored son, alone, to where his brothers are herding in a location already marked by family trauma is Jacob's act of catastrophic parental blindness. A man in Dothan redirects Joseph (vv. 15–17); the brothers have moved further north. When they see him coming, "they conspired against him to kill him" (v. 18). "Here comes this dreamer," they say (v. 19) — the Hebrew is "master of dreams" (ba'al ha-halomot). They plan to kill him, throw him in a pit, and say a wild animal ate him. "Then we will see what will become of his dreams" (v. 20). The irony of the statement is enormous: they intend their murder of Joseph to refute his dreams. Instead, their actions will become the very mechanism by which the dreams come true.

Reuben intervenes — not from moral clarity, but from complex motives. He tells the brothers not to shed blood but to throw him in an empty pit. Reuben "planned to rescue him from their hand to restore him to his father" (v. 22). His partial rescue fails; he will disappear from the scene before the sale happens and return to find an empty pit. When they strip Joseph of his robe and throw him in, they "sat down to eat" (v. 25) — a chilling detail of how compartmentalized human cruelty can be. Then a caravan of Ishmaelites/Midianites appears, and Judah has a new idea: "What profit is it if we kill our brother and conceal his blood? Come, let us sell him to the Ishmaelites, and let not our hand be upon him, for he is our brother, our own flesh" (vv. 26–27). Judah's argument is simultaneously merciful and mercenary: don't murder him, but profit from him. The brothers agree and sell Joseph for twenty pieces of silver.

The Midianites/Ishmaelites question (vv. 25–28) is one of the classic text-critical puzzles of Genesis: sometimes the traders are called Ishmaelites, sometimes Midianites. Most likely the terms overlap — Midianites who are part of an Ishmaelite trading confederacy, or the terms used interchangeably for the same group of desert traders. The theological point is unaffected: Joseph is sold as a commodity by his own brothers.

The deception of Jacob (vv. 31–35) is devastating. The brothers dip Joseph's robe in goat's blood — the same animal used to deceive Isaac (27:9–16 — Jacob used goat skins and goat meat to deceive his blind father). Now the sons use a goat's blood to deceive their father Jacob. The deceiver is deceived with the same instrument he used. Jacob "recognized it and said, 'It is my son's robe. A fierce animal has devoured him. Joseph is without doubt torn to pieces'" (v. 33). He refuses all comfort, mourning his son for years. "I shall go down to Sheol to my son, mourning" (v. 35). His grief is total, extended, and self-consuming — partly because it is built on a lie.

The chapter ends with a single transitional verse: "Meanwhile the Midianites had sold him in Egypt to Potiphar, an officer of Pharaoh, the captain of the guard" (v. 36). Joseph is already in Egypt. The reader knows more than Jacob: Joseph is alive. Joseph is in Potiphar's house. God has not said a single word in this chapter — not one divine speech, not one angelic appearance, not one theophany. God is absent from the surface of the text and working beneath every event. This is the theological signature of the Joseph story: God works through, not around, human evil. The pit, the sale, the deception — none of it happens outside God's sovereign hand, but none of it is excused by that sovereignty either. The brothers are guilty. The dreams are coming true. The dreamer is in Egypt. And God has not spoken a word.""",
        "chapter_overview": "Jacob favors Joseph above his sons and gives him a special robe, generating his brothers' hatred. Joseph reports two dreams predicting his authority over his family. Jacob sends him to check on his brothers in Dothan; his brothers conspire to kill him, but Reuben redirects them to throw him in a pit instead. Judah proposes selling Joseph to passing Ishmaelite traders for twenty silver pieces. The brothers dip his robe in goat's blood to deceive Jacob, who mourns inconsolably. Joseph is sold in Egypt to Potiphar, Pharaoh's captain of the guard.",
        "original_language_notes": [
            {
                "term": "כְּתֹנֶת פַּסִּים (kuttoneth passim)",
                "language": "Hebrew",
                "verse": 3,
                "words_used": ["kuttoneth", "passim"],
                "meaning": "The famous 'coat of many colors' — though passim may refer to 'long sleeves' (reaching the palms/wrists) rather than color. The same term appears in 2 Samuel 13:18-19 for the robe worn by Tamar, a king's virgin daughter. Whatever its form, it marked Joseph as set apart for honor rather than labor — a robe of rank and favoritism."
            },
            {
                "term": "בַּעַל הַחֲלֹמוֹת (ba'al ha-halomot)",
                "language": "Hebrew",
                "verse": 19,
                "words_used": ["ba'al", "ha-halomot"],
                "meaning": "'Master of dreams' or 'dreamer' — used mockingly by the brothers. Ba'al (lord/master/owner) + halomot (dreams). The irony is dense: by calling him 'master of dreams' in contempt, they unknowingly name what he actually is. His mastery of dreams — their interpretation — will eventually save Egypt and fulfill the very predictions they despise."
            },
            {
                "term": "שְׁאוֹל (Sheol)",
                "language": "Hebrew",
                "verse": 35,
                "words_used": ["Sheol"],
                "meaning": "The realm of the dead in Hebrew thought — not hell in the NT sense, but the underworld where all the dead are gathered. Jacob says 'I will go down to Sheol to my son, mourning' — expressing that he expects to die in unrelieved grief. The word shaal may relate to 'to ask/inquire,' as the realm that swallows without returning answers. Jacob's use of it reveals the depth of his despair."
            }
        ],
        "moral_lessons": "Parental favoritism, however understandable, produces devastating family fractures — Jacob suffered from it and then repeated it. Our sin-patterns do not automatically end with us. Human evil does not operate outside God's sovereign plan — but this does not excuse the evil. The brothers' jealousy, deception, and cruelty are their own sin. God's providence is not an alibi for human wickedness. Joseph's dreams came from God; sharing them may have been naive or unwise. Not every revelation needs to be immediately broadcast. Judah's 'merciful' compromise — sell him rather than kill him — is still a grave sin. Lesser evil is still evil. Grief built on a lie (Jacob's mourning) is a form of suffering the deceiver inflicts on the innocent.",
        "application": "When we are thrown into a pit by people we trusted — siblings, friends, colleagues — the Joseph story invites us to believe that God is present even where He is silent. The chapter with no divine speech is not a chapter without divine action. When you are the victim of family jealousy, organizational betrayal, or systemic injustice, remember: the pit is not the end of the story; it is the first chapter of a longer arc. For those who have perpetuated favoritism or family fracture: acknowledge the damage done. For those building families or teams: favoritism — even when motivated by love — poisons community. Equal regard is not natural; it is cultivated by obedience to the God who loves all His children.",
        "prayer": "Lord, You are present even when You are silent. In the pits where I have been thrown — by family, by circumstance, by my own failures — You are working beneath every event. Give me faith to trust Your providence when I cannot see it. Deliver me from the jealousy that destroys. Deliver me from the favoritism that fractures. And when I am the dreamer in the pit, help me not to lose the dream. In Jesus' name, who was Himself betrayed for silver pieces and counted dead before He rose, Amen.",
        "key_points": [
            "Jacob's favoritism for Joseph — expressed in the distinctive robe — causes his brothers' hatred, repeating the pattern of partiality he himself experienced as a child.",
            "Joseph's two dreams predict his authority over his family; his brothers' hatred intensifies when they hear them.",
            "God does not speak once in Genesis 37 — yet He is working through every event: the pit, the sale, the transfer to Egypt.",
            "The brothers sell Joseph for twenty pieces of silver — the price of a slave — and deceive their father with goat's blood, the same animal used when Jacob deceived Isaac.",
            "The deception returns to Jacob: the deceiver is deceived. The pattern of generational sin is explicit.",
            "Joseph arrives in Egypt at Potiphar's house — positioned exactly where God's plan requires, despite the evil that brought him there."
        ],
        "study_questions": [
            "What does Jacob's favoritism for Joseph reveal about the long-term effects of his own upbringing? How do parental patterns repeat across generations?",
            "Why does God not speak or appear in Genesis 37? What does His silence teach us about how He works?",
            "Compare the brothers' use of goat's blood to deceive Jacob with Jacob's use of goat skins to deceive Isaac. What does this parallel suggest?",
            "Judah proposes selling Joseph rather than killing him, calling him 'our brother, our own flesh.' Is this mercy or moral compromise? Why?",
            "How do Joseph's dreams — mocked as 'master of dreams' — begin to be fulfilled through the very actions taken to prevent them?"
        ],
        "tags": ["Genesis", "Joseph", "dreams", "favoritism", "betrayal", "brothers", "providence", "pit", "Potiphar", "Egypt", "Judah", "Reuben"],
        "sources": ["Genesis 37", "Genesis 27:9-16", "Genesis 28:12", "Genesis 34", "2 Samuel 13:18-19", "Matthew 26:15", "Acts 7:9"]
    },
    {
        "book_id": 1,
        "book": "Genesis",
        "chapter": 38,
        "title": "Genesis 38 — Judah and Tamar: The Scarlet Thread of Righteousness in a Broken Line",
        "summary": "Chapter 38 interrupts the Joseph narrative with the story of Judah and Tamar. Judah leaves his brothers, marries a Canaanite woman, and has three sons: Er, Onan, and Shelah. Er marries Tamar but is wicked and God kills him. Onan refuses to fulfill levirate duty to Tamar and God kills him too. Judah withholds Shelah, fearing he will also die. Judah's wife dies. Tamar, understanding she has been denied her rights, disguises herself as a prostitute and sleeps with Judah. When her pregnancy is discovered, Judah orders her burned; she produces his seal and staff as proof. Judah confesses 'She is more righteous than I.' Tamar gives birth to twins: Perez and Zerah. Perez is in the line of David and Jesus.",
        "content": """Genesis 38 is one of the most jarring narrative insertions in Scripture. Joseph has just been sold into Egypt at the end of chapter 37; Potiphar has just purchased him. We expect chapter 38 to follow Joseph into Potiphar's house. Instead, the text turns entirely away from Egypt and Joseph, and gives us a dark, morally complex story about Judah and his Canaanite entanglement — a story that at first seems to have nothing to do with God's plan, and turns out to be directly in the center of it.

The interruption is intentional. Judah will be the brother who saves Joseph's life (37:26) and later the brother who offers himself as surety for Benjamin (44:33). He is being developed as a character. And Tamar's story is not an embarrassing footnote to the Joseph narrative — it is the story that keeps the line of Judah alive, and from Judah's line comes David, and from David's line comes Jesus (Matt. 1:3; Ruth 4:18–22). The "interruption" is the continuation of the most important story in the Bible.

Judah separates from his brothers and makes his home near an Adullamite named Hirah (v. 1). He marries the daughter of a Canaanite man named Shua — unnamed throughout the chapter, a detail that underlines the text's discomfort with the relationship. Three sons: Er, Onan, and Shelah. Judah takes Tamar as a wife for Er, his firstborn. "But Er, Judah's firstborn, was wicked in the sight of the LORD, and the LORD put him to death" (v. 7). The text gives no detail about Er's wickedness — just the fact and its consequence. The LORD acts immediately, decisively, and without explanation. Er's sin is not described; his death is.

Levirate duty (from Latin levir, "husband's brother") is the obligation in ancient Israelite and Near Eastern law for a surviving brother to marry his deceased brother's widow and father a child who will carry the dead brother's name and inherit his estate. Onan is the next-in-line. He is required to perform this duty. His refusal is strategic: "Onan knew that the offspring would not be his. So whenever he went in to his brother's wife he would waste the semen on the ground, so as not to give offspring to his brother" (v. 9). This is not primarily a text about contraception; it is about Onan's deliberate exploitation of Tamar (he has the sexual benefits of the marriage) while refusing her the legal protection and inheritance-rights that levirate duty would provide for her and the dead brother's name. His sin is against his brother's name and Tamar's legal security. "What he did was wicked in the sight of the LORD, and he put him to death also" (v. 10). Two sons dead; both by divine judgment.

Judah's response to Shelah is fear-driven and dishonest: "Then Judah said to his daughter-in-law Tamar, 'Remain a widow in your father's house, till Shelah my son grows up' — for he feared that he would die, like his brothers" (v. 11). Judah is afraid to lose his third son. The fear is understandable. But his solution is to put Tamar in indefinite waiting — legally bound to the family (she cannot marry outside the levirate structure while Shelah lives) but practically abandoned by it. He has no intention of giving her Shelah. He is effectively condemning Tamar to childlessness and legal limbo to protect himself.

Time passes. Judah's wife dies. He goes to Timnah for sheep-shearing. Tamar hears he is coming and devises her plan. She removes her widow's garments, covers herself with a veil, and sits at the entrance to Enaim on the road to Timnah. "When Judah saw her, he thought she was a prostitute, for she had covered her face" (v. 15). He proposes to her; she asks for his seal, cord, and staff as a pledge until he can send payment. He agrees. She conceives by him. Judah sends the payment via Hirah, but no one knows of a local "cult prostitute" or any woman at that spot. He decides to let the matter drop to avoid embarrassment.

Three months later: Tamar is pregnant. The news reaches Judah: "Tamar your daughter-in-law has been immoral. Moreover, she is pregnant by immorality" (v. 24). Judah's response is immediate and severe: "Bring her out, and let her be burned" (v. 24). He has the legal authority of the father-in-law and is ready to execute her. Then Tamar produces the seal, cord, and staff: "By the man to whom these belong, I am pregnant. Please identify — whose are these?" (v. 25).

Judah's response is the theological climax of the chapter: "She is more righteous than I, since I did not give her to my son Shelah" (v. 26). The confession is extraordinary. Judah — the one who ordered her burned moments ago — acknowledges his own greater guilt. "More righteous than I" (Hebrew: tsadqah mimmeni — "she is righteous from/beyond me"). He does not claim she acted rightly in every sense; he acknowledges that in the context of their competing obligations, she was in the right and he was in the wrong. He had denied her the levirate right. She had done what she did to secure what was legally hers. The confession is genuine and costly.

Tamar gives birth to twins — again, twins, as in the Jacob/Esau birth. The midwife ties a scarlet thread on the hand that appears first, naming him Zerah. But the hand withdraws, and the other child is born first. He is named Perez (Hebrew: perets, meaning "breach" or "breaking through"). Perez — the twin who breaks through — is in the genealogy of David (Ruth 4:18–22) and of Jesus (Matt. 1:3). The scarlet thread on Zerah's wrist will echo in Rahab's scarlet cord (Josh. 2:18) — another story of an outsider woman who secures her family through unconventional means and ends up in the line of the Messiah.

What is Genesis 38 doing theologically? Several things. First, it shows the moral condition of the patriarchal family without the lens of God's covenant: Judah, left to his own devices, makes Canaanite alliances, produces wicked sons, withholds justice from a widow, and solicits a "prostitute" — all within a few years of leaving his brothers. The covenant people, apart from God's active governance, drift rapidly. Second, it demonstrates that God's redemptive line does not wait for perfect people. Perez is born of a morally irregular union — and he is in the direct line to Christ. God is not embarrassed by the instruments He uses. Third, Tamar herself is a model of courageous, righteous advocacy for what was legally and morally owed to her. She risks death to secure her rights and her deceased husband's legacy. Matthew lists her by name in the genealogy of Jesus (Matt. 1:3) — one of only five women named there, all of whom have irregular stories. The genealogy is a statement that God's grace works through every kind of human story.""",
        "chapter_overview": "Judah separates from his brothers, marries a Canaanite woman, and has three sons. His first two sons, Er and Onan, are killed by God for wickedness. Judah withholds his third son Shelah from Tamar, leaving her in legal limbo. When Judah's wife dies, Tamar disguises herself and sleeps with Judah, who believes her to be a cult prostitute. When her pregnancy is discovered, Judah orders her execution; she reveals his own seal and staff as evidence. Judah confesses his greater guilt. Tamar bears twins: Perez and Zerah. Perez is an ancestor of David and Jesus.",
        "original_language_notes": [
            {
                "term": "צָדְקָה מִמֶּנִּי (tsadqah mimmeni)",
                "language": "Hebrew",
                "verse": 26,
                "words_used": ["tsadqah", "mimmeni"],
                "meaning": "'She is more righteous than I' — literally 'she is righteous from/out of me.' The comparative form (mimmeni, 'than I') makes this a confessional statement. Tsadqah comes from the root tsadak (righteousness, rightness, being in the right). Judah uses the legal-ethical term — she has the stronger legal/moral claim in this situation. This is one of the most direct confessions of personal guilt in Genesis."
            },
            {
                "term": "פֶּרֶץ (Perets)",
                "language": "Hebrew",
                "verse": 29,
                "words_used": ["Perez", "Perets"],
                "meaning": "'Breach' or 'breaking through' — from the root paratz (to break through, burst forth, spread abroad). Perez breaks through the birth canal ahead of Zerah despite the midwife's marking. The name becomes significant: Perez is in the Davidic line (Ruth 4:18-22) and appears in Matthew 1:3 in Jesus' genealogy. 'Breaking through' in an unexpected way is his name and his destiny."
            },
            {
                "term": "חוֹטָם (khotem) / פְּתִיל (pethil)",
                "language": "Hebrew",
                "verse": 18,
                "words_used": ["khotem", "pethil"],
                "meaning": "Seal (signet ring or cylinder seal, used to authenticate documents) and cord (the string from which it hung). Judah's seal was his legal identity — his 'signature.' By leaving these as pledge with Tamar, he has given her irrefutable proof of his identity. The items are evidence in the ancient world equivalent to a signed contract. Tamar uses them not to shame Judah but to spare her own life."
            }
        ],
        "moral_lessons": "Judah's story shows how quickly God's people drift when separated from the community of faith and accountability. Tamar's righteousness is a model of courageous advocacy for what is legally and morally owed — she secured justice for herself and her dead husband's name at personal risk. God's redemptive line moves through imperfect, irregular, morally complicated people — this is not license for sin, but grace for reality. The one who sentences others to death may himself be the greater transgressor. Judah's immediate willingness to condemn Tamar — before the evidence — is a caution against condemning others before full accounting. True repentance involves acknowledging specific wrongdoing, not just general failure.",
        "application": "Judah's separation from his brothers and descent into compromise is a parable for spiritual isolation: distance from covenant community accelerates moral drift. Are there areas of your life where you have 'gone down from your brothers' — separated yourself from accountability and drifted? Tamar teaches that demanding justice for the voiceless and the wronged is not rebellion — it is righteousness. And Judah's confession teaches that acknowledging our greater guilt, even at cost to our pride, is the beginning of restoration. Matthew's genealogy reminds us that no one's past disqualifies them from God's redemptive story.",
        "prayer": "Lord, I am humbled by the grace You show in using broken lives for Your purposes. Like Judah, I have withheld what others were owed and then hastened to condemn them. Forgive me. Like Tamar, there are times I need courage to stand for what is right even when the system fails me. Give me that courage. And remind me that the line of Your redemption passes through every kind of human mess — not because You approve of sin, but because Your grace is greater than any human failure. Thank You for a Savior who comes from exactly this kind of family. Amen.",
        "key_points": [
            "Judah's separation from his brothers leads to Canaanite intermarriage and rapid moral decline, illustrating the danger of spiritual isolation.",
            "God kills Er and Onan for wickedness — the text does not explain Er's sin but specifies Onan's: exploiting Tamar's levirate situation while denying her its benefits.",
            "Judah withholds Shelah from Tamar out of fear, consigning her to legal limbo — a violation of justice he refuses to acknowledge.",
            "Tamar's bold plan secures what Judah had denied her; her righteousness is formally acknowledged even by her accuser.",
            "Judah's confession 'She is more righteous than I' is one of the most direct admissions of personal guilt in Genesis.",
            "Perez — born of this irregular union — is in the direct genealogy of David and Jesus (Ruth 4:18-22; Matt. 1:3), showing God's grace working through every human story."
        ],
        "study_questions": [
            "Why is Genesis 38 placed in the middle of the Joseph narrative? What does its placement suggest about its theological importance?",
            "What specifically was Onan's sin? Why does the text frame it as covenant-breaking rather than simply a contraceptive act?",
            "In what sense is Tamar 'more righteous than' Judah? What legal and moral claims was she asserting?",
            "Matthew 1:3 names Tamar in the genealogy of Jesus. What does her inclusion — along with Rahab, Ruth, and Bathsheba — say about the nature of Jesus' lineage?",
            "How does Judah's willingness to condemn Tamar without full investigation reflect a pattern of hypocrisy the New Testament warns about (cf. John 8:1-11)?"
        ],
        "tags": ["Genesis", "Judah", "Tamar", "levirate", "Perez", "righteousness", "genealogy of Jesus", "Er", "Onan", "confession", "redemption"],
        "sources": ["Genesis 38", "Ruth 4:18-22", "Matthew 1:3", "Deuteronomy 25:5-10", "Joshua 2:18", "John 8:1-11"]
    },
    {
        "book_id": 1,
        "book": "Genesis",
        "chapter": 39,
        "title": "Genesis 39 — Joseph in Potiphar's House: The Presence of God in the Place of Unjust Suffering",
        "summary": "Joseph arrives in Egypt and is sold to Potiphar, captain of Pharaoh's guard. God is with Joseph and causes him to prosper; Potiphar recognizes God's blessing and makes Joseph overseer of all his household. Potiphar's wife repeatedly propositions Joseph, who refuses on grounds of loyalty to Potiphar and faithfulness to God. She seizes his garment when he flees; she uses it as false evidence, accusing Joseph of assault. Potiphar imprisons Joseph. Even in prison, God is with Joseph; the prison warden makes him overseer of all the prisoners, and everything Joseph does prospers.",
        "content": """Genesis 39 is the chapter of divine presence in impossible circumstances. It answers, implicitly, the question that ends chapter 37: What happens to a seventeen-year-old dreamer who is unjustly sold into slavery in a foreign country? The answer Genesis gives is not comfort or rescue — not yet. The answer is: "The LORD was with Joseph" (v. 2). The phrase appears four times in the chapter (vv. 2, 3, 21, 23), and it is the theological spine of everything that follows.

Joseph arrives in Egypt and is purchased by Potiphar — an Egyptian whose title is "officer of Pharaoh, captain of the guard" (v. 1). The word for officer (saris) can mean eunuch or court official; the latter is more likely here since Potiphar has a wife. He is a military man with royal connections — a powerful owner for a slave who has just traveled from Canaan in chains.

The text immediately asserts what matters most: "The LORD was with Joseph, and he became a successful man, and he was in the house of his Egyptian master" (v. 2). The word translated "successful" (matsliach) comes from the root tsalach — to prosper, to advance, to break through. God's presence manifests in Joseph's visible competence and success. Potiphar notices — and specifically notices the divine source: "His master saw that the LORD was with him and that the LORD caused all that he did to succeed in his hands" (v. 3). A pagan Egyptian recognizes the LORD (YHWH) at work in Joseph's life. This is a pattern throughout Joseph's story: pagans (Potiphar, the prison warden, Pharaoh's cupbearer, Pharaoh himself) recognize God's hand on Joseph before Israel's own family does.

Potiphar makes Joseph overseer of his household — a position of extraordinary trust. "From the time that he made him overseer in his house and over all that he had, the LORD blessed the Egyptian's house for Joseph's sake; the blessing of the LORD was on all that he had, in house and field" (v. 5). The blessing is not confined to Joseph; it extends to Potiphar's entire household. The pattern of Genesis: where God's covenant person goes, blessing flows to the surrounding environment (12:3). Abraham blessed Pharaoh, Isaac blessed Abimelech, Jacob blessed Laban. Joseph blesses Potiphar — even as a slave.

Potiphar trusts Joseph completely: "he had no concern about anything but the food he ate" (v. 6) — a standard ancient expression of total household delegation. "Joseph was handsome in form and appearance" (v. 6b) — the same phrase used for Rachel (29:17). This physical detail is not incidental; it sets up the temptation.

Potiphar's wife "cast her eyes on Joseph and said, 'Lie with me'" (v. 7). The proposition is blunt. Joseph's refusal (vv. 8–9) is a model of ethical reasoning: "My master has trusted me with everything. He has withheld nothing from me except you, because you are his wife. How then can I do this great wickedness and sin against God?" Two reasons: loyalty to Potiphar (covenant fidelity, gratitude, stewardship) and fear of God (the deeper ground). The second reason is the more important one. Joseph does not merely say "Potiphar would be hurt" — he says "I would sin against God." His ethics are theocentric, not merely relational. He speaks to her "day after day" she persists; "day after day" he refuses to be with her or be near her (v. 10).

The false accusation follows a moment of opportunity: Joseph enters the house when no other men are present. She grabs his garment. He flees, leaving it in her hand. His flight (vv. 11–12) is the right action — complete removal from temptation, even at cost (the garment). Paul's echo: "Flee from sexual immorality" (1 Cor. 6:18); "Flee youthful passions" (2 Tim. 2:22). The garment in her hand becomes the evidence for her accusation. She calls the men of the house first, then Potiphar, and tells the same story twice: Joseph "came in to me to lie with me," she cried, he fled, and he left his garment.

Joseph's garment has now been used against him twice: the brothers used his robe as evidence of his "death" to deceive Jacob (37:31–33); now Potiphar's wife uses his cloak as evidence of assault to deceive Potiphar. His clothing is the instrument of his betrayal — first by family, then by an employer's wife. In both cases, the accusation is false. In both cases, Joseph suffers unjustly. In neither case does God intervene before the suffering occurs.

Potiphar's response is interesting: "his anger was kindled" (v. 19) — but the text does not say he believed his wife completely. He could have had Joseph executed; a slave accused of assaulting his master's wife would typically face death. Instead, Potiphar puts Joseph in the prison "where the king's prisoners were confined" (v. 20) — the royal prison, not a common jail. This placement is significant: it is the prison connected to Pharaoh's household, which means it is also where Pharaoh's cupbearer and baker will later be imprisoned (ch. 40). Potiphar's measured response — prison instead of execution — may reflect some doubt about his wife's account.

The chapter ends with the same structure as it began: "But the LORD was with Joseph and showed him steadfast love and gave him favor in the sight of the keeper of the prison" (v. 21). God's steadfast love (Hebrew: hesed — covenant faithfulness, loyal love) is the theological keyword. Hesed is the word used for God's covenant obligation to Israel; its appearance here applies covenant language to Joseph even in a pagan prison. The prison warden delegates everything to Joseph, just as Potiphar had delegated everything to Joseph. "The keeper of the prison paid no attention to anything that was in Joseph's hand, because the LORD was with him. And whatever he did, the LORD made it succeed" (v. 23).

The structure is deliberate: slave → overseer of household → falsely accused → prisoner → overseer of prison. Each station is a descent in human terms; in divine terms, each station is a positioning. God is preparing Joseph not by exempting him from unjust suffering but by working through it. The prison is the next staging ground, not the final destination. And the warden's trust — full delegation to Joseph within the prison — is the exact preparation Joseph needs to be noticed by Pharaoh's officers (ch. 40), which will lead to Pharaoh's attention (ch. 41). God's providence in Genesis 39 is not spectacular; it is structural. Every humiliation has a purpose.""",
        "chapter_overview": "Joseph is purchased by Potiphar, Pharaoh's captain of the guard. God is with Joseph, causing his work to prosper; Potiphar recognizes divine blessing and makes Joseph overseer of his entire household. Potiphar's wife repeatedly propositions Joseph, who refuses citing loyalty to Potiphar and faithfulness to God. When she seizes his garment as he flees, she uses it as false evidence of assault. Potiphar imprisons Joseph in the royal prison. Even there, God is with Joseph; the warden delegates full authority to him.",
        "original_language_notes": [
            {
                "term": "יְהוָה הָיָה אֶת יוֹסֵף (YHWH hayah et Yosef)",
                "language": "Hebrew",
                "verse": 2,
                "words_used": ["YHWH", "hayah", "et", "Yosef"],
                "meaning": "'The LORD was with Joseph' — the phrase recurs four times (vv. 2, 3, 21, 23). It is a theological statement about divine presence, not merely good fortune. YHWH (the covenant name, personal and relational) is specifically with Joseph — the same presence promised to the patriarchs ('I will be with you,' 26:3; 28:15). This presence is the explanation for Joseph's competence, favor, and resilience."
            },
            {
                "term": "חֶסֶד (hesed)",
                "language": "Hebrew",
                "verse": 21,
                "words_used": ["hesed"],
                "meaning": "Steadfast love, covenant faithfulness, loyal love — the most theologically rich word in Hebrew for God's relational commitment. Its appearance here ('the LORD showed him hesed') applies the covenant-loyalty term to Joseph in prison. Hesed is not sentimental; it is God's unbreakable commitment to His people rooted in who He is, not in their circumstances. It is the anchor of Joseph's story."
            },
            {
                "term": "מַצְלִיחַ (matsliach)",
                "language": "Hebrew",
                "verse": 3,
                "words_used": ["matsliach"],
                "meaning": "Causing to prosper, making successful — from the root tsalach (to advance, to break through, to succeed). The causative form implies God is the agent who makes Joseph succeed. The same root appears in v. 23: 'whatever he did, YHWH made it succeed (matsliach).' Success in the Joseph story is consistently attributed to God, not to Joseph's native talent — though his talent is evident."
            }
        ],
        "moral_lessons": "God's presence does not exempt us from injustice — it sustains us through it. Joseph was faithful and was imprisoned anyway; faithfulness does not guarantee immediate vindication. The call to flee temptation (not negotiate with it, not manage it at close range, but flee) is illustrated with full narrative force. Joseph's refusal is grounded in God-fearing ethics, not merely pragmatic calculation. False accusations against the righteous are real — and God's presence remains with the accused. Every unjust demotion in Joseph's story becomes a providential positioning. What looks like a dead end is often a doorway.",
        "application": "When you have done everything right and suffered unjustly anyway — when your faithfulness resulted in loss, your integrity cost you your position, your garment was used against you — Genesis 39 says: the LORD is with you there. In the prison. Not despite the prison, but in it. This is not cheap comfort; it is the testimony of Joseph's story. Be faithful where you are. Serve fully in the season you're in, not the one you want to be in. Flee what must be fled; delegate fully what you have been trusted with. And trust that what looks like a career-ending injustice may be a providential positioning for something you cannot yet see.",
        "prayer": "Lord, Your presence is my prosperity — not comfort from difficulty, but companionship through it. When I face false accusations, unjust punishment, or suffering I did not deserve, remind me that You were with Joseph in the pit and in the prison. Give me the integrity to flee what must be fled, even at personal cost. Give me the faithfulness to serve fully in whatever station I am in. And give me eyes to see that every unjust descent may be a providential staging for something only You can see. In the name of Jesus, who suffered the ultimate unjust accusation and was faithful to the end, Amen.",
        "key_points": [
            "'The LORD was with Joseph' appears four times in the chapter — it is the theological engine of the entire narrative.",
            "God's presence in Joseph's life is visible to Potiphar, a pagan Egyptian — unbelievers can recognize divine blessing on God's people.",
            "Joseph's refusal of Potiphar's wife is grounded in theocentric ethics: 'How can I sin against God?' — not merely pragmatic fear of Potiphar.",
            "His garment is used as false evidence — the second time his clothing has been weaponized against him (after the brothers in ch. 37).",
            "Potiphar's choice of royal prison rather than execution suggests possible doubt about his wife's account; this placement prepares Joseph for Pharaoh's notice.",
            "Joseph's prison authority mirrors his household authority — each unjust demotion is a providential positioning in God's larger plan."
        ],
        "study_questions": [
            "The phrase 'the LORD was with Joseph' appears four times in chapter 39. What does divine 'presence' mean concretely in this chapter? What does it produce?",
            "Joseph gives two reasons for refusing Potiphar's wife: loyalty to Potiphar and fear of God. Why is the second reason more foundational?",
            "What is the significance of Joseph fleeing rather than staying to argue his virtue? How does this compare to Paul's advice in 1 Corinthians 6:18?",
            "How does Potiphar's measured response (prison, not death) become part of God's providential arrangement?",
            "In what sense is each 'demotion' in Joseph's story (slavery, then prison) actually a promotion within God's plan?"
        ],
        "tags": ["Genesis", "Joseph", "Potiphar", "temptation", "false accusation", "divine presence", "hesed", "faithfulness", "providence", "suffering"],
        "sources": ["Genesis 39", "Genesis 37:31-33", "1 Corinthians 6:18", "2 Timothy 2:22", "Psalm 105:17-19", "Romans 8:28"]
    },
    {
        "book_id": 1,
        "book": "Genesis",
        "chapter": 40,
        "title": "Genesis 40 — Dreams in the Dungeon: God's Gift of Interpretation and the Long Wait for Deliverance",
        "summary": "Two of Pharaoh's officers — his chief cupbearer and chief baker — offend him and are imprisoned in the royal prison where Joseph is held. Both men dream on the same night and are troubled because no one can interpret their dreams. Joseph, noticing their distress, offers to interpret and declares that interpretation belongs to God. He correctly interprets the cupbearer's dream (three days to restoration) and the baker's dream (three days to execution by hanging). Both interpretations come true. But the chief cupbearer forgets Joseph, and Joseph remains in prison for two more years.",
        "content": """Genesis 40 is a chapter of interpretive gifts and painful delays. Joseph has been in prison for an unspecified time when two new prisoners arrive from Pharaoh's court: the chief cupbearer and the chief baker. Their arrival is providential — they are the human links in a chain that will eventually bring Joseph before Pharaoh — but the chapter does not resolve itself in rescue. It resolves in waiting. Two years of waiting. Joseph does everything right in this chapter, and he goes back to his cell with nothing changed. The chapter's theology is not about triumph but about faithfulness in the long delay.

The two officers "offended their lord the king of Egypt" (v. 1) — the nature of their offense is not specified, perhaps deliberately. Ancient Near Eastern courts were full of intrigue; the ambiguity is realistic. They are placed in the royal prison — the same house where Joseph is confined — "and the captain of the guard charged Joseph with them, and he attended them" (v. 4). Potiphar is the captain of the guard (39:1). The man who imprisoned Joseph is also the man who assigns Joseph to care for these prisoners. The text is deliberately ironic: the instrument of Joseph's captivity is also the instrument of the connection that will eventually free him.

One night — the same night — both men dream. They wake troubled. Joseph sees their anxiety and asks: "Why are your faces downcast today?" (v. 7). This is pastoral attentiveness — Joseph notices the emotional state of those he serves. He is not inward-focused despite his own unjust circumstances. The men explain: "We have had dreams, and there is no one to interpret them" (v. 8). In Egypt, dreams were taken seriously as divine communications, and professional dream-interpreters (wise men, magicians) served the court. Without access to these professionals, the prisoners are distressed.

Joseph's response is theologically precise: "Do not interpretations belong to God? Please tell them to me" (v. 8). He does not claim his own interpretive skill; he immediately refers the gift upward. This is the pattern throughout the Joseph story: his abilities are acknowledged as divine rather than personal. In chapter 41, he will say the same to Pharaoh: "It is not in me; God will give Pharaoh a favorable answer" (41:16). The consistent attribution of interpretive ability to God, rather than self-promotion, is part of Joseph's character — and part of why God can entrust him with increasing authority. He does not steal credit for gifts he did not generate.

The cupbearer's dream (vv. 9–11): a vine with three branches that blossomed, produced clusters, and were pressed into Pharaoh's cup, which he put in Pharaoh's hand. Joseph's interpretation: the three branches are three days; within three days Pharaoh will restore the cupbearer to his position. Joseph adds a personal request: "Only remember me, when it is well with you, and please do me the kindness to mention me to Pharaoh, and so get me out of this place" (v. 14). He describes his situation accurately: "I was indeed stolen out of the land of the Hebrews, and here also I have done nothing that they should put me into the pit" (v. 15). Joseph knows he is innocent; he is clear-eyed about the injustice. He asks for advocacy — a reasonable, human request.

The baker, encouraged by the favorable interpretation, presents his dream (vv. 16–17): three baskets on his head, the top basket full of baked goods, and birds eating from the basket. Joseph's interpretation is grim: the three baskets are three days; within three days Pharaoh will lift the baker's head — from him — and hang him on a tree, and birds will eat his flesh. The contrast with the cupbearer's interpretation is precise: both involve a "lifting" of the head, but the cupbearer's lifting is promotion, and the baker's lifting is decapitation. Joseph does not soften the message to spare the baker's feelings. He delivers both interpretations truthfully — the favorable and the terrible.

Both interpretations come true on the third day — Pharaoh's birthday. The cupbearer is restored to his position. The baker is executed. The accuracy of interpretation, down to the three-day timing, confirms that Joseph's gift is genuinely divine.

And then: "Yet the chief cupbearer did not remember Joseph, but forgot him" (v. 23). The sentence is devastating in its simplicity. Two more years pass (41:1) before Joseph is remembered. Psalm 105:17–19 reflects on this period: "He had sent a man ahead of them, Joseph, who was sold as a slave. His feet were hurt with fetters; his neck was put in a collar of iron; until what he had said came to pass, the word of the LORD tested him." The prison is not a mistake or a detour — it is a testing. The delay in the cupbearer's memory is not a failure of Providence — it is Providence operating on a timeline Joseph cannot see.

What is Joseph doing during these two years? The text does not say. We are not given a narrative of patient endurance or increasing despair. We are given silence — and then the next chapter begins with "After two whole years, Pharaoh dreamed." The silence of the two years is the chapter's most powerful statement. Joseph waited. He continued to serve. He continued to do his work in the prison. And he waited longer than any of his requests or hopes required him to wait. The waiting is not rewarded quickly. It is rewarded rightly.

The theological question Genesis 40 raises is not "why didn't the cupbearer remember?" but "what is God doing in the delay?" The answer, from the vantage of chapter 41: God was waiting for the moment when Pharaoh himself would dream — when not merely a prisoner but Egypt's king would need an interpreter — so that Joseph's gift would be used at the highest possible level, with the greatest possible consequence. The two-year delay ensures that Joseph does not escape prison through the cupbearer's influence (which would have placed him back in Egyptian society at a low level) but is brought before Pharaoh himself (which places him at the highest level). God's delays are not oversights. They are calibrations.""",
        "chapter_overview": "Pharaoh's chief cupbearer and baker are imprisoned in the royal prison where Joseph is held. Both dream on the same night and are troubled. Joseph, noticing their distress, declares that interpretation belongs to God and interprets both dreams correctly: the cupbearer will be restored in three days; the baker will be executed in three days. Both come true. Joseph asks the cupbearer to remember him before Pharaoh, but the cupbearer forgets him. Joseph waits in prison for two more years.",
        "original_language_notes": [
            {
                "term": "הֲלוֹא לֵאלֹהִים פִּתְרֹנִים (halo le'Elohim pitronim)",
                "language": "Hebrew",
                "verse": 8,
                "words_used": ["halo", "le'Elohim", "pitronim"],
                "meaning": "'Do not interpretations belong to God?' — a rhetorical question expecting 'yes.' The word pitronim (interpretations) comes from patar (to interpret, to solve, to open). The same root gives us pithron (the interpretation itself, used in vv. 12, 18). Joseph's deflection of interpretive credit to God is theologically significant: he establishes immediately that the gift is not his own skill but God's revelation."
            },
            {
                "term": "שַׂר הַמַּשְׁקִים / שַׂר הָאוֹפִים (sar ha-mashkim / sar ha-ophim)",
                "language": "Hebrew",
                "verse": 2,
                "words_used": ["sar", "ha-mashkim", "ha-ophim"],
                "meaning": "Chief cupbearer / chief baker — sar (officer, chief, prince) + mashkim (those who give drink) and ophim (those who bake). These were not mere servants but high-ranking court officials controlling the king's food and drink supply — roles of enormous trust in an ancient court where poisoning was a constant political threat. Their offense against Pharaoh was therefore grave."
            },
            {
                "term": "שָׁכַח (shakhach)",
                "language": "Hebrew",
                "verse": 23,
                "words_used": ["shakhach"],
                "meaning": "'Forgot' — to forget, to neglect, to overlook. The word appears twice in the final verse: 'did not remember Joseph, but forgot him.' The doubling emphasizes completeness of forgetfulness. Psalm 105:19 says the word of the LORD 'tested' (tsaraph — refined, as metal by fire) Joseph during this period. The forgetting is not accidental in God's economy — it is the duration required for God's larger plan."
            }
        ],
        "moral_lessons": "God's timetable and ours are never the same, and His delays are not His failures. Joseph's gift was given at the right moment — to the right people — to eventually reach the right ears. Faithfulness in small acts of pastoral care (noticing the cupbearer's troubled face, asking a question) opens the doors God has prepared. Never claim credit for gifts that come from God — Joseph's consistent attribution of interpretation to God is a model of humility that God entrusts with greater authority. When those we serve forget us, God does not. The two years of the cupbearer's forgetfulness are not wasted — they are calibrated.",
        "application": "Are you waiting longer than expected for a door you were sure God was opening? Joseph's two-year wait after the cupbearer's restoration is a theology of the long delay: God's timing is perfect; your moment has not been forgotten, it is being calibrated. Serve faithfully where you are. Notice the people around you — their downcast faces, their unspoken distress. Use whatever gift God has given you in the station you're in, not the one you wish you were in. And when your gift operates correctly and nothing immediately changes, hold the same posture Joseph held: trust the giver more than the gift's immediate outcome.",
        "prayer": "Lord, teach me to trust Your timing. I confess that my waiting often becomes impatience, and my delays become accusation against Your goodness. Remind me of Joseph in the dungeon — faithful for two full years after the door seemed to open and then close again. Give me pastoral eyes to notice those around me who are troubled, and give me grace to point them to You as the source of any gift I have. And when those who should remember me forget me, remind me that You do not forget. Your word over my life will come to pass at the right time. In Jesus' name, Amen.",
        "key_points": [
            "Joseph's statement 'Do not interpretations belong to God?' establishes a theological posture of humility he maintains throughout his story.",
            "Joseph notices the cupbearer and baker's distress and asks about it — pastoral attentiveness in the midst of his own unjust suffering.",
            "Both interpretations come true exactly as Joseph stated, confirming the divine source of his gift.",
            "Joseph's request to the cupbearer — 'remember me' — is a legitimate, human appeal for advocacy that goes unanswered for two years.",
            "The cupbearer's forgetting is not a narrative mistake; it is the calibration that ensures Joseph reaches Pharaoh (ch. 41) rather than a lower station.",
            "The two-year wait after the correct interpretation is the chapter's deepest theology: God's faithfulness operates on a timeline we cannot see."
        ],
        "study_questions": [
            "Why does Joseph attribute interpretation to God rather than claiming the skill as his own? What does this consistent posture produce in his character and career?",
            "Compare the cupbearer's and baker's dreams and interpretations. What do they share, and what is the key difference? Why does Joseph deliver the unfavorable interpretation without softening it?",
            "Joseph says he was 'stolen from the land of the Hebrews' and has 'done nothing' to deserve prison. Is this self-pity, accurate advocacy, or both? How should we understand honest complaint in prayer and relationship?",
            "What is the significance of the two-year delay after the correct interpretation? What does it reveal about how God uses time?",
            "Psalm 105:19 says Joseph was 'tested' during this period. What is the content of the test? What is being refined in him?"
        ],
        "tags": ["Genesis", "Joseph", "dreams", "cupbearer", "baker", "interpretation", "prison", "waiting", "divine timing", "faithfulness", "providence"],
        "sources": ["Genesis 40", "Genesis 41", "Psalm 105:17-19", "Daniel 2:28", "Romans 8:28"]
    }
]

def now_iso():
    return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

def save_to_db(conn, commentary, collection_id, batch_uuid):
    cur = conn.cursor()
    # Check duplicate
    cur.execute("""
        SELECT id, LENGTH(content) FROM commentary_entries
        WHERE collection_id=? AND book_id=? AND chapter=? AND language_code='en'
              AND reference_scope='chapter' AND deleted_at IS NULL
    """, (collection_id, commentary['book_id'], commentary['chapter']))
    row = cur.fetchone()
    if row and row[1] > 200:
        return 'skipped', None

    entry_uuid = str(uuid.uuid4())
    key_points_json = json.dumps(commentary['key_points'])
    study_questions_json = json.dumps(commentary['study_questions'])
    tags_json = json.dumps(commentary['tags'])
    sources_json = json.dumps(commentary['sources'])
    oln_json = json.dumps(commentary['original_language_notes'])
    chapter_overview = commentary.get('chapter_overview', '')
    moral_lessons = commentary.get('moral_lessons', '')
    word_count = len(commentary['content'].split())
    ts = now_iso()

    if row:
        cur.execute("""
            UPDATE commentary_entries SET
                uuid=?, generation_batch_id=NULL, title=?, summary=?, content=?,
                application=?, prayer=?, key_points=?, study_questions=?,
                theological_perspective='evangelical', status='draft',
                is_ai_generated=1, ai_model_name='claude-sonnet-4-6',
                ai_model_provider='anthropic', ai_generation_batch_uuid=?,
                word_count=?, updated_at=?
            WHERE id=?
        """, (entry_uuid, commentary['title'], commentary['summary'],
              commentary['content'], commentary['application'],
              commentary['prayer'], key_points_json, study_questions_json,
              batch_uuid, word_count, ts, row[0]))
        entry_id = row[0]
        action = 'updated'
    else:
        cur.execute("""
            INSERT INTO commentary_entries
            (uuid, collection_id, book_id, chapter, verse_start, verse_end,
             reference_scope, title, summary, content, application, prayer,
             key_points, study_questions, language_code, theological_perspective,
             status, is_ai_generated, ai_model_name, ai_model_provider,
             ai_generation_batch_uuid, word_count, created_at, updated_at)
            VALUES (?,?,?,?,NULL,NULL,'chapter',?,?,?,?,?,?,?,'en','evangelical','draft',
                    1,'claude-sonnet-4-6','anthropic',?,?,?,?)
        """, (entry_uuid, collection_id, commentary['book_id'], commentary['chapter'],
              commentary['title'], commentary['summary'], commentary['content'],
              commentary['application'], commentary['prayer'],
              key_points_json, study_questions_json,
              batch_uuid, word_count, ts, ts))
        entry_id = cur.lastrowid
        action = 'inserted'
    conn.commit()
    return action, entry_uuid

def save_json(commentary):
    book_slug = commentary['book'].lower().replace(' ', '-')
    book_id_str = str(commentary['book_id']).zfill(2)
    chapter_str = str(commentary['chapter']).zfill(2)
    dir_path = pathlib.Path(f"generated/{book_id_str}-{book_slug}")
    dir_path.mkdir(parents=True, exist_ok=True)
    file_path = dir_path / f"{chapter_str}.json"

    ts = now_iso()
    data = {
        "uuid": str(uuid.uuid4()),
        "collection_name": "Believers Sword Commentaries",
        "author_type": "ai",
        "language_code": "en",
        "theological_perspective": "evangelical",
        "status": "draft",
        "book_id": commentary['book_id'],
        "book": commentary['book'],
        "chapter": commentary['chapter'],
        "title": commentary['title'],
        "summary": commentary['summary'],
        "content": commentary['content'],
        "chapter_overview": commentary.get('chapter_overview', ''),
        "original_language_notes": commentary['original_language_notes'],
        "moral_lessons": commentary.get('moral_lessons', ''),
        "application": commentary['application'],
        "prayer": commentary['prayer'],
        "key_points": commentary['key_points'],
        "study_questions": commentary['study_questions'],
        "tags": commentary['tags'],
        "sources": commentary['sources'],
        "created_at": ts,
        "updated_at": ts
    }
    # Verify forbidden keys absent
    forbidden = {'is_ai_generated', 'model_name', 'prompt_version'}
    for k in forbidden:
        data.pop(k, None)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Verify parses and no forbidden keys
    with open(file_path, 'r', encoding='utf-8') as f:
        parsed = json.load(f)
    for k in forbidden:
        assert k not in parsed, f"Forbidden key {k} found in {file_path}"

    return str(file_path)

def update_progress(conn, book_id, book, chapter, completed=False):
    ts = now_iso()
    cur = conn.cursor()
    next_chapter = chapter + 1
    cur.execute("""
        UPDATE commentary_generation_progress
        SET last_completed_book_id=?, last_completed_chapter=?,
            current_book_id=?, current_chapter=?, updated_at=?
        WHERE id=1
    """, (book_id, chapter, book_id, next_chapter, ts))
    conn.commit()

    progress = {
        "next_book_id": book_id,
        "next_book": book,
        "next_chapter": next_chapter,
        "last_completed_book_id": book_id,
        "last_completed_book": book,
        "last_completed_chapter": chapter,
        "completed": completed,
        "updated_at": ts
    }
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

def append_log(batch_uuid, start_ref, end_ref, generated, skipped, inserted, files):
    entry = {
        "timestamp": now_iso(),
        "generation_batch_id": batch_uuid,
        "start_reference": start_ref,
        "end_reference": end_ref,
        "chapters_generated": generated,
        "chapters_skipped": skipped,
        "db_rows_inserted": inserted,
        "files_written": files,
        "errors": []
    }
    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(entry) + '\n')

def main():
    conn = sqlite3.connect(DB_PATH)

    generated_count = 0
    skipped_count = 0
    inserted_count = 0
    files_written = []
    errors = []

    last_book_id = None
    last_book = None
    last_chapter = None
    first_ref = None
    last_ref = None

    for c in COMMENTARIES:
        ref = f"{c['book']} {c['chapter']}"
        if first_ref is None:
            first_ref = ref
        last_ref = ref

        action, entry_uuid = save_to_db(conn, c, COLLECTION_ID, BATCH_UUID)

        if action == 'skipped':
            print(f"SKIP: {ref} (already exists with content)")
            skipped_count += 1
        else:
            file_path = save_json(c)
            files_written.append(file_path)
            print(f"{'INSERT' if action == 'inserted' else 'UPDATE'}: {ref} -> {file_path}")
            if action == 'inserted':
                inserted_count += 1
            generated_count += 1

        last_book_id = c['book_id']
        last_book = c['book']
        last_chapter = c['chapter']

        # Update progress after each chapter
        update_progress(conn, last_book_id, last_book, last_chapter)

    conn.close()
    append_log(BATCH_UUID, first_ref, last_ref, generated_count, skipped_count, inserted_count, files_written)

    print(f"\n=== SUMMARY ===")
    print(f"Range: {first_ref} — {last_ref}")
    print(f"Generated: {generated_count}, Skipped: {skipped_count}")
    print(f"DB rows inserted: {inserted_count}")
    print(f"Files written: {len(files_written)}")
    print(f"Next: Genesis 41")
    if errors:
        print(f"ERRORS: {errors}")

if __name__ == '__main__':
    main()
