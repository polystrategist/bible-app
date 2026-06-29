#!/usr/bin/env python3
"""Generate commentaries for Genesis 16-20."""
import sqlite3, json, uuid, os, datetime, pathlib

DB_PATH = "believers_sword_commentaries.db"
GENERATED_DIR = pathlib.Path("generated")
PROGRESS_JSON = "commentary_generation_progress.json"
LOG_FILE = "commentary_generation_log.jsonl"
COLLECTION_ID = 1
BATCH_UUID = str(uuid.uuid4())

CHAPTERS = [
    {
        "book_id": 1,
        "book": "Genesis",
        "chapter": 16,
        "title": "Genesis 16 — Hagar, the God Who Sees, and the Limits of Human Planning",
        "summary": "Sarai's impatience leads to a plan that brings immediate conflict and lasting consequences. Yet in the wilderness God finds Hagar, the forgotten servant, and reveals Himself as El Roi — the God who sees the unseen.",
        "content": """Genesis 16 is a sobering chapter that traces the collision between human impatience and divine promise. Ten years have passed since Abram received God's covenant in chapter 15, and Sarai has not conceived. Rather than waiting on God, Sarai proposes a culturally accepted but spiritually hazardous solution: giving her Egyptian servant Hagar to Abram as a secondary wife, so that through Hagar a surrogate heir might be born.

Abram listens to Sarai's voice (v. 2), a phrase that deliberately echoes Adam listening to Eve in Genesis 3:17. The parallel is intentional — both men accepted a plan that bypassed God's direction and produced painful consequences. Abram's compliance was not passive; the text notes he took Hagar after ten years in Canaan (v. 3), underlining that this was a deliberate act, not an impulsive moment.

When Hagar conceives, the relational fabric tears. Hagar looks on Sarai with contempt (v. 4); Sarai blames Abram (v. 5); Abram deflects responsibility (v. 6); and Sarai treats Hagar harshly until she flees. Human schemes to solve divine delays consistently produce this cycle: short-term relief, long-term rupture.

But the chapter's theological center is not the sin — it is the God who pursues. The Angel of the LORD finds Hagar by a spring of water on the way to Shur (v. 7). The verb "found" is remarkable: Hagar did not seek God; God sought her. She is a foreign woman, a slave, fleeing through the desert — and God comes to her personally. He calls her by name, asks where she has come from and where she is going (v. 8), the same care God extends to humanity in the garden (Gen. 3:9).

God's instructions are both gracious and honest. He commands her to return and submit (v. 9), not because her mistreatment was acceptable, but because her destiny and her son's destiny are bound to this household. God then promises that her offspring will be so numerous they cannot be counted (v. 10) — language nearly identical to the promise given to Abram (Gen. 15:5). Hagar receives a direct covenant word from God, making her one of the very few women in the Old Testament to do so.

The announcement about Ishmael (vv. 11–12) is complex. His name means "God hears" — El has heard your affliction (v. 11). His character, described as a "wild donkey of a man," is not a curse but a description of a fierce, independent, desert-dwelling people. His descendants will dwell in hostility with all his brothers (v. 12), a word fulfilled in the centuries of tension between Israel and the surrounding Arabian peoples.

Hagar's response is the theological climax: she names God El Roi, "the God who sees" (v. 13). Her declaration — "Truly here I have seen him who looks after me" — is one of the most extraordinary moments in Genesis. A slave woman, in the wilderness, gives God a new name. The spring is named Beer-lahai-roi: the well of the Living One who sees me (v. 14). This name preserved the witness of divine care for generations.

Ishmael is born when Abram is 86 (v. 16). Though not the child of promise, Ishmael is not forgotten by God. He too will father a great nation (17:20). Genesis 16 reminds us that God's redemptive purposes are not derailed by human impatience, but those purposes unfold on God's timetable, not ours. The chapter also stands as a rebuke to any theology that treats the poor, the foreign, and the forgotten as outside God's concern. El Roi sees them all.""",
        "chapter_overview": "Sarai gives Hagar to Abram; conflict erupts when Hagar conceives and despises Sarai; Hagar flees but is found by the Angel of the LORD who promises her a son named Ishmael and instructs her to return; Hagar names God El Roi — the God who sees.",
        "original_language_notes": [
            {"term": "שִׁפְחָה (shiphchah)", "language": "Hebrew", "verse": 1, "words_used": ["shiphchah"], "meaning": "Female servant or maidservant; a lower-status household slave. Hagar's designation throughout highlights her vulnerability and Sarai's power over her."},
            {"term": "עִנִּי (anni)", "language": "Hebrew", "verse": 11, "words_used": ["anni"], "meaning": "Affliction, suffering, or misery. The Angel tells Hagar that God has 'heard your affliction' — the same root appears in the Exodus account when God sees Israel's affliction (Ex. 3:7), linking the two deliverances."},
            {"term": "יִשְׁמָעֵאל (Yishmael)", "language": "Hebrew", "verse": 11, "words_used": ["Yishmael"], "meaning": "'God hears' — from shama (to hear) + El (God). The name is a permanent testimony that God attended to Hagar's cry even before Ishmael was born."},
            {"term": "אֵל רֳאִי (El Roi)", "language": "Hebrew", "verse": 13, "words_used": ["El", "Roi"], "meaning": "'The God who sees' or 'God of seeing.' From ra'ah (to see). Hagar's name for God is unique in the entire Old Testament — no one else bestows this name, making her declaration remarkable."},
            {"term": "פֶּרֶא אָדָם (pere adam)", "language": "Hebrew", "verse": 12, "words_used": ["pere", "adam"], "meaning": "'Wild donkey of a man' — pere refers to the onager, a wild desert donkey prized for its freedom and strength. The description is not an insult but a portrait of an untamed, independent man who lives by his own rules."}
        ],
        "moral_lessons": [
            "Human impatience with God's timing produces schemes that bypass faith and create lasting harm.",
            "Deflecting blame — as both Abram and Sarai do — compounds sin rather than resolving it.",
            "God's vision extends to the forgotten, the marginalized, and the foreigner. No one is outside his sight.",
            "Suffering does not mean God is absent; El Roi sees every wilderness and every tear.",
            "Even consequences of our failures do not put us beyond God's compassion and care."
        ],
        "application": "When God's promises seem delayed, the pressure to 'help God along' with our own solutions is real and ancient. Genesis 16 invites us to examine where we are substituting strategy for trust. It also calls us to see people the way God sees Hagar — not as background characters in someone else's story, but as individuals God pursues by name. Ask: Is there someone in your life who feels unseen? How might you be the human instrument of El Roi's care?",
        "prayer": "Father, forgive us for the times we have grown impatient with your timing and engineered our own solutions. Remind us that you are El Roi — the God who sees — not only us, but every overlooked, forgotten, and suffering person around us. Give us the grace to wait on your promises and the compassion to extend your sight to those whom the world passes by. In Jesus' name, Amen.",
        "key_points": [
            "Sarai's plan to use Hagar as a surrogate heir reflects cultural practice but bypasses faith in God's promise.",
            "The relational breakdown between Sarai, Hagar, and Abram illustrates how human schemes produce conflict.",
            "The Angel of the LORD finds Hagar in the wilderness — God initiates care for the forgotten.",
            "God promises Hagar a son, Ishmael, whose name means 'God hears' — her affliction was not ignored.",
            "Hagar names God El Roi ('the God who sees'), a unique divine name given by a foreign slave woman.",
            "Beer-lahai-roi ('well of the Living One who sees me') memorializes God's personal attention to Hagar.",
            "Ishmael's wild and independent character sets the stage for Israel's later relationship with Arabian peoples."
        ],
        "study_questions": [
            "Why does the narrator compare Abram listening to Sarai (v. 2) to language used earlier in Genesis? What pattern is being identified?",
            "How does God's interaction with Hagar challenge any assumption that God's covenant concern is exclusively for the 'chosen' family?",
            "What does El Roi — the God who sees — mean for your own wilderness moments when you feel unseen?",
            "God tells Hagar to return and submit (v. 9). How do we understand this command in light of her mistreatment? What does it reveal about God's longer purposes?",
            "Ishmael is not the child of promise, yet God blesses and sees him. How does this shape our understanding of God's universal care?",
            "In what areas of your life are you currently tempted to 'help God along' rather than trust his timing?"
        ],
        "tags": ["Hagar", "Ishmael", "El Roi", "covenant", "faith", "impatience", "God sees", "wilderness", "promise"],
        "sources": []
    },
    {
        "book_id": 1,
        "book": "Genesis",
        "chapter": 17,
        "title": "Genesis 17 — El Shaddai, the Covenant of Circumcision, and New Names",
        "summary": "Thirteen years after Ishmael's birth, God appears to Abram as El Shaddai and establishes the covenant of circumcision. Both Abram and Sarai receive new names marking their new identities, and God confirms that the promised son will come through Sarah, not Hagar.",
        "content": """Thirteen years of silence follow Ishmael's birth (compare 16:16 with 17:1). God does not speak. This long pause is not divine absence but divine patience — allowing Abram time to settle into Ishmael as the apparent heir before God redirects. When God does appear, He opens with a name never used before in Scripture: El Shaddai (v. 1).

El Shaddai is traditionally rendered "God Almighty," though the Hebrew root shaddai is debated. It may relate to shadad (powerful, forceful) or shad (mountain, the immovable). The name appears concentrated in the patriarchal narratives (Gen. 17:1; 28:3; 35:11; 43:14; 48:3; 49:25) and in Job, where it describes God's overwhelming sovereign power over human limitations. The name suits this moment perfectly: Abram is now 99, Sarai is 89, and the biological possibility of conception has long passed. El Shaddai is precisely the God who operates beyond what biology can explain.

God's command is straightforward: "Walk before me, and be blameless" (v. 1). The Hebrew tamim (blameless, whole, complete) does not mean sinless perfection but wholehearted, undivided devotion. It is the same word used of Noah (6:9). God calls Abram to a life of uninterrupted, authentic covenant faithfulness.

The covenant is now expanded. Previously God promised land and descendants (ch. 12, 15). Now He adds:
- Abram's name becomes Abraham (father of a multitude of nations, v. 5)
- Abraham will be the father of kings (v. 6)
- The covenant extends to his offspring throughout all generations (v. 7)
- The land of Canaan is given as an everlasting possession (v. 8)
- Circumcision is established as the sign of the covenant (vv. 9–14)
- Sarai's name becomes Sarah (princess, v. 15)
- Sarah specifically will bear the promised son (v. 16)

The name changes are theologically significant. In the ancient Near East, renaming signified a fundamental change of identity and destiny. God does not merely tweak Abram's circumstances — He redefines who Abram is. The addition of the Hebrew letter heh (ה) to both names (Abram → Abraham; Sarai → Sarah) is often linked to the divine name YHWH, as if God is breathing His own identity into theirs.

Abraham's response to the promise of a son through Sarah is laughter (v. 17). He falls on his face and laughs — not derisive unbelief but astonished, overwhelmed wonder. "Shall a child be born to a man who is a hundred years old?" The laughter is humanly reasonable. Abraham's next words reveal a tender pastoral heart: "Oh that Ishmael might live before you!" (v. 18). He intercedes for the son he has loved for thirteen years, asking that Ishmael too be included in the blessing.

God's answer is gracious but definitive. Ishmael will be blessed — twelve princes and a great nation (v. 20). But the covenant will be established with Isaac, the son Sarah will bear in one year (vv. 19, 21). The name Isaac (Yitzchak, "he laughs") preserves the memory of Abraham's astonished response and, later, Sarah's laughter (18:12). Laughter becomes the name of promise.

Circumcision (vv. 9–14, 23–27) is instituted as the covenant sign. Every male in Abraham's household is to be circumcised — including the 99-year-old Abraham himself and his 13-year-old son Ishmael. It is a sign in the body, permanent and inescapable, marking out those who belong to this covenant community. In the New Testament, Paul reinterprets circumcision as pointing to the circumcision of the heart (Rom. 2:28–29; Col. 2:11–12), fulfilled in the transforming work of Christ and the Spirit.

Abraham's immediate obedience (v. 23 — "that very day") is a model of covenant faithfulness. He does not delay, calculate, or negotiate. When El Shaddai commands, Abraham acts on the same day. This is the "walk before me and be blameless" made visible in obedience.""",
        "chapter_overview": "God appears to 99-year-old Abram as El Shaddai, reaffirms and expands the covenant, renames Abram to Abraham and Sarai to Sarah, institutes circumcision as the covenant sign, and promises that Sarah will bear Isaac within a year. Abraham laughs in wonder and intercedes for Ishmael.",
        "original_language_notes": [
            {"term": "אֵל שַׁדַּי (El Shaddai)", "language": "Hebrew", "verse": 1, "words_used": ["El", "Shaddai"], "meaning": "Traditionally 'God Almighty.' The name emphasizes God's power to accomplish what is humanly impossible. It appears predominantly in patriarchal and wisdom literature contexts (Genesis and Job), always in settings of impossible promise or overwhelming divine power."},
            {"term": "תָּמִים (tamim)", "language": "Hebrew", "verse": 1, "words_used": ["tamim"], "meaning": "'Blameless, whole, complete, without defect.' Used of sacrificial animals without defect and of morally wholehearted people. The call to walk tamim is a call to undivided covenant faithfulness, not sinless perfection."},
            {"term": "אַבְרָהָם (Abraham)", "language": "Hebrew", "verse": 5, "words_used": ["Abraham"], "meaning": "Expanded from Abram ('exalted father') to Abraham ('father of a multitude'). The name change — incorporating heh (ה) — signals a new covenant identity. Abraham's name now declares his destiny before it is visible."},
            {"term": "שָׂרָה (Sarah)", "language": "Hebrew", "verse": 15, "words_used": ["Sarah"], "meaning": "'Princess' or 'noblewoman.' The change from Sarai (possibly the same meaning in an archaic form) to Sarah formalizes her role as the covenant mother. Her renamed identity precedes the birth of her son."},
            {"term": "יִצְחָק (Yitzchak)", "language": "Hebrew", "verse": 19, "words_used": ["Yitzchak"], "meaning": "'He laughs' — from tzachak (to laugh). The name captures Abraham's astonished laughter at the promise (v. 17) and anticipates Sarah's laughter in chapter 18. The name of promise is laughter — God delights to give joy where there was only impossibility."}
        ],
        "moral_lessons": [
            "God's timing is not our timing; long silences from heaven do not indicate abandonment.",
            "El Shaddai — God Almighty — is the God of the impossible. No biological, financial, or circumstantial limitation can bind him.",
            "New identity in God precedes the fulfillment of promise. We are named by what God sees, not by what we currently experience.",
            "Circumcision, and by extension all covenant signs, are meant to be permanently embedded in ordinary life, not separated from it.",
            "Obedience to God's commands is often immediate and costly; Abraham's same-day obedience is the pattern."
        ],
        "application": "Genesis 17 invites us to receive new names — to see ourselves through God's declaration rather than our circumstances. Many believers carry the weight of old names: failure, barren, forgotten, too old, too late. El Shaddai's message is that He specializes in exactly these situations. Where do you need to hear God rename you? Where have you laughed at impossibility and needed to hear 'this time next year'? Covenant signs also call us to examine whether our faith is embodied — visible, tangible, costly — not merely intellectual agreement.",
        "prayer": "El Shaddai, God of the impossible, we confess that we often size your promises by our own limitations. Forgive us. Rename us by your word, not by our failures. Give us the faith to receive new names, to obey immediately and fully, and to intercede for those around us even as Abraham interceded for Ishmael. May we walk before you and be blameless. In the name of Jesus, who is the yes to every promise, Amen.",
        "key_points": [
            "God appears as El Shaddai — God Almighty — after 13 years of silence, perfectly timing His next revelation.",
            "Abram's name is changed to Abraham ('father of a multitude'), embedding his destiny in his identity.",
            "The covenant is expanded: land, offspring, kings, and an everlasting relationship across all generations.",
            "Circumcision is established as the permanent bodily sign of covenant membership.",
            "Sarai becomes Sarah, affirming her role as covenant mother and princess.",
            "Abraham laughs in astonished wonder at the promise of a son at 100 years old.",
            "God confirms Isaac — not Ishmael — as the covenant heir, while still blessing Ishmael with 12 princes.",
            "Abraham obeys 'that very day' — same-day obedience marking wholehearted covenant faithfulness."
        ],
        "study_questions": [
            "Why does God wait 13 years after Ishmael's birth to speak again? What might the silence have accomplished in Abraham?",
            "What does the name El Shaddai communicate that was particularly needed at this moment in Abraham's life?",
            "How does receiving a new name from God (Abram → Abraham, Sarai → Sarah) relate to what happens in baptism and the Christian life?",
            "Abraham laughs in verse 17 and God does not rebuke him. What does this suggest about how God receives our honest emotional responses?",
            "Circumcision was a permanent, bodily, costly sign of covenant. What does it mean that our covenant signs (baptism, communion) are also embodied rather than merely mental?",
            "How does God's blessing of Ishmael alongside the covenant through Isaac help us understand God's care for those outside the direct line of redemptive history?"
        ],
        "tags": ["El Shaddai", "circumcision", "covenant", "Abraham", "Sarah", "Isaac", "new name", "obedience", "faith"],
        "sources": []
    },
    {
        "book_id": 1,
        "book": "Genesis",
        "chapter": 18,
        "title": "Genesis 18 — Three Visitors, a Promise of Laughter, and Bold Intercession",
        "summary": "Three mysterious visitors come to Abraham at Mamre. One reaffirms that Sarah will bear a son within a year; Sarah laughs in disbelief and is gently rebuked. The LORD then reveals His intent toward Sodom, and Abraham engages in one of Scripture's most remarkable intercessory dialogues.",
        "content": """Genesis 18 is one of the richest chapters in the Old Testament, weaving together hospitality, divine presence, prophetic promise, and covenant intercession in a single afternoon's encounter.

The scene opens with Abraham sitting at the entrance to his tent during the heat of the day (v. 1). This small detail establishes the setting: it is midday, the worst time for desert travel, when no guests would normally arrive. Three men appear, and Abraham's response is extravagant. He runs from the tent entrance (v. 2), bows to the ground, and immediately addresses the central figure: "My lord, if I have found favor in your sight, do not pass by your servant" (v. 3). Abraham's hospitality is instinctive and lavish — water for feet, rest under the tree, bread for refreshment.

The meal prepared is strikingly generous: a choice calf (not just goat), fine meal cakes baked quickly, curds, and milk (vv. 6–8). Abraham stands nearby while they eat — the posture of an attentive servant. The ancient world understood hospitality as a sacred obligation; Abraham embodies it as a spiritual discipline.

The identity of the visitors becomes clear progressively. The text opens noting "the LORD appeared to him" (v. 1). The three "men" are angelic or divine beings; by verse 13, one of them is explicitly "the LORD" (YHWH). Many early Christian readers saw the three visitors as a prefiguration of the Trinity; Jewish interpreters understood them as the LORD with two angels. What is beyond dispute is that Abraham was, as the writer of Hebrews notes, entertaining angels without knowing it (Heb. 13:2).

The central promise is repeated and sharpened: "I will surely return to you about this time next year, and Sarah your wife shall have a son" (v. 10). Sarah is listening behind the tent entrance. Her laughter (v. 12) is internal — not a public laugh of mockery but a private, instinctive laugh of incredulity. "After I am worn out, and my lord is old, shall I have pleasure?" Her reasoning is human and honest. She considers her biological state: past menopause, aged. The LORD hears the private laughter and addresses it: "Why did Sarah laugh?" (v. 13). When confronted, Sarah denies it out of fear (v. 15). The LORD's reply is one of Scripture's most arresting: "No, but you did laugh." There is no anger in the response — it is a gentle, knowing correction, leaving no room for self-deception.

The chapter pivots at verse 16. The men prepare to leave toward Sodom. God pauses and discloses His reasoning to Abraham in an almost tender soliloquy: "Shall I hide from Abraham what I am about to do?" (v. 17). The answer implied is no — because Abraham is God's friend and the father of the nation through whom all nations will be blessed. The covenant relationship creates intimacy; intimacy creates disclosure. God tells His plans to His friends.

The announcement about Sodom (vv. 20–21) — "Because the outcry against Sodom and Gomorrah is great and their sin is very grave, I will go down to see" (v. 21) — sets up the intercession. God's "going down to see" is anthropomorphic language communicating that divine judgment is deliberate and fully informed, not rash or ignorant.

Abraham's intercession (vv. 22–33) is one of Scripture's most astonishing passages. He approaches and "stood before the LORD" — a reversal, since the text just noted "the LORD stood before Abraham" (v. 22). Abraham intercedes with remarkable boldness: "Will you indeed sweep away the righteous with the wicked?" (v. 23). He begins at fifty righteous people and negotiates down to ten. Each time, God affirms: yes, if ten righteous are found, the city will be spared.

The intercession reveals several essential truths about prayer and God's character:
1. God is just: He will not destroy the righteous with the wicked.
2. God invites persistence: Abraham returns six times and God does not rebuke the boldness.
3. Intercession matters: God does not dismiss the conversation but engages it fully.
4. The limits of intercession are not God's patience but the actual righteous: Abraham stops at ten, perhaps knowing Lot's household was the maximum he could confidently count.
5. This chapter anticipates New Testament intercession: Jesus stands before the Father on behalf of sinners, and Christians are called to pray persistently for cities and people facing judgment.

The chapter closes without resolution — the question of Sodom's fate hangs open, answered in chapter 19. But what chapter 18 has established is the extraordinary privilege of covenant friendship with God: a friendship in which God shares His plans, hears His friend's bold requests, and takes those requests seriously.""",
        "chapter_overview": "Three divine visitors appear to Abraham at Mamre; Abraham shows extravagant hospitality; the LORD promises Isaac within a year and Sarah laughs privately in disbelief; God reveals His plan against Sodom to Abraham; Abraham intercedes boldly, negotiating from fifty down to ten righteous people.",
        "original_language_notes": [
            {"term": "וַיָּרָץ (va-yaratz)", "language": "Hebrew", "verse": 2, "words_used": ["va-yaratz"], "meaning": "'And he ran.' The verb emphasizes haste. At 99 years old, Abraham runs to greet strangers. The urgency communicates that hospitality was not merely obligatory for Abraham — it was joyful and immediate."},
            {"term": "צְחֹק (tzechok)", "language": "Hebrew", "verse": 12, "words_used": ["tzechok"], "meaning": "'Laughter' — from tzachak, the same root as Isaac's name. Sarah's laughter here is private and incredulous. The word echoes Genesis 17:17 (Abraham's laughter) and anticipates the naming of Isaac, transforming laughter from doubt into joy."},
            {"term": "הֲיִפָּלֵא מֵיהוָה דָּבָר (hayipale me-YHWH davar)", "language": "Hebrew", "verse": 14, "words_used": ["hayipale", "me-YHWH", "davar"], "meaning": "'Is anything too hard/wonderful for the LORD?' Pala means to be extraordinary, surpassing, beyond ordinary capacity. This rhetorical question — echoed in Jeremiah 32:27 and Luke 1:37 — is one of Scripture's great declarations of divine omnipotence."},
            {"term": "צַעֲקַת (tza'akat)", "language": "Hebrew", "verse": 20, "words_used": ["tza'akat"], "meaning": "'Outcry' — used for the cry of the oppressed demanding justice (cf. Ex. 3:7, 9 for Israel's cry in Egypt). The word implies that innocent victims in Sodom were crying out to God for rescue and justice."},
            {"term": "הַשֹּׁפֵט כָּל הָאָרֶץ (ha-shofet kol ha-aretz)", "language": "Hebrew", "verse": 25, "words_used": ["ha-shofet", "kol", "ha-aretz"], "meaning": "'The Judge of all the earth.' Abraham's appeal to God's justice grounds his intercession in God's own character. He is not demanding something foreign to God — he is asking God to act consistently with who God is."}
        ],
        "moral_lessons": [
            "Extravagant hospitality is a spiritual discipline, not merely a social nicety — Abraham runs to serve strangers.",
            "God hears our private thoughts and laughter; there is no inner life hidden from Him.",
            "Covenant friendship with God includes the extraordinary privilege of being told His plans and of interceding for others.",
            "Bold, persistent, structured intercession is not presumption — God invites and honors it.",
            "The righteous influence their cities through prayer; the church's greatest contribution to its culture is intercession."
        ],
        "application": "Genesis 18 raises two practical challenges: hospitality and intercession. On hospitality: do we see strangers as interruptions or as potential messengers of God's grace? Abraham entertained angels while treating them as ordinary guests. On intercession: are we bringing our cities, nations, and communities before God with Abraham's bold persistence? The intercessory prayer of Genesis 18 is not a formula but a portrait — of a person who knows God's character well enough to appeal to it, and who loves people enough to stand between them and judgment.",
        "prayer": "LORD, teach us to practice hospitality that sees the sacred in the stranger. Teach us to intercede with Abraham's boldness — not demanding what is unjust, but appealing to your justice and mercy for those who face judgment. Where we have laughed in private disbelief, meet us with your gentle question and remind us that nothing is too wonderful for you. In Christ's name, Amen.",
        "key_points": [
            "Abraham's extravagant hospitality in the heat of midday models the sacred duty of welcoming the stranger.",
            "Three divine visitors (including YHWH) come to Abraham — he does not realize who they are until revelation comes.",
            "The promise of Isaac is repeated with a one-year timeframe, sharpening the covenant's imminence.",
            "Sarah's private laughter in disbelief is heard by God — nothing escapes His notice.",
            "God's rhetorical question, 'Is anything too hard for the LORD?', becomes a foundational declaration of divine power.",
            "God reveals His plan for Sodom to Abraham because of their covenant friendship.",
            "Abraham intercedes boldly six times, negotiating from fifty to ten righteous — and God engages each appeal.",
            "The intercession is grounded in God's own character as the just Judge of all the earth."
        ],
        "study_questions": [
            "Why does God reveal His plan for Sodom to Abraham before acting? What does this reveal about the nature of covenant friendship with God?",
            "How does Abraham's hospitality (running, bowing, preparing a feast) reflect his character and his relationship with God?",
            "Sarah's laughter was private, yet God heard it. How should this awareness shape your prayer life and inner thought life?",
            "What does the question 'Is anything too hard for the LORD?' mean for a situation you are currently facing that seems impossible?",
            "Abraham grounds his intercession in God's character ('Shall not the Judge of all the earth do what is just?'). What does this teach about how to pray for others facing judgment or crisis?",
            "What does Abraham's persistent intercession down to ten righteous people suggest about the power of even a small community of the righteous within a city?"
        ],
        "tags": ["hospitality", "intercession", "Sarah", "laughter", "Sodom", "God's justice", "prayer", "divine friendship", "promise"],
        "sources": []
    },
    {
        "book_id": 1,
        "book": "Genesis",
        "chapter": 19,
        "title": "Genesis 19 — Sodom's Judgment, Lot's Rescue, and the Grace That Escaped",
        "summary": "Two angels come to Sodom, are received by Lot, and the men of the city demand them. After Lot and his family are rescued, fire and sulfur destroy Sodom and Gomorrah. Lot's wife looks back and becomes a pillar of salt. Lot ends in a cave; from incest with his daughters come Moab and Ammon.",
        "content": """Genesis 19 is one of Scripture's most disturbing chapters — violent, dark, and morally complex from beginning to end. It is not a comfortable text. Yet it stands as a canonical record of divine justice against unrepentant wickedness, of grace extended to those who barely deserved it, and of what Jesus Himself would later point to as a warning about the day of judgment (Luke 17:28–30).

The two angels who accompanied the LORD to Abraham's tent (ch. 18) arrive at Sodom in the evening. Lot, sitting at the city gate (v. 1) — a position of civic importance, suggesting some status — sees them and immediately offers hospitality. His offer echoes Abraham's in chapter 18, but the contrast is stark: Abraham invited strangers from an open tent in the country; Lot nervously insists that these visitors must not spend the night in the city square, as if he knows what will happen to them if they do (v. 2–3).

The night scene is horrifying. All the men of Sodom — young and old, from every part of the city (v. 4) — surround Lot's house and demand the visitors so they can "know" them sexually (v. 5). The Hebrew yada used here carries sexual connotation, as it does in 4:1 and 4:17. The text states "all the men" — indicating a thoroughgoing corruption that left no righteous male presence in the city. Abraham's intercession went down to ten righteous; there were not even ten.

Lot goes out to reason with the mob (v. 6), which itself shows some courage. But his proposed solution — offering his two virgin daughters to the crowd (v. 8) — is indefensible by any standard. Lot's moral compromise is profound: the culture of Sodom has distorted even his protective instincts. He prioritizes hospitality obligations over his daughters. The text records this without editorial commentary, but the horror is unmistakable, and later Scripture does not gloss over Lot's failures.

The angels intervene decisively: they strike the crowd with blindness (v. 11) and call Lot to gather his family and flee. Lot goes to his sons-in-law, but they think he is joking (v. 14). When morning comes, the angels urgently press Lot to leave, and he "lingered" (v. 16). The Hebrew vatmahah is a remarkable word — Lot hesitates even as divine judgment is imminent. The text is explicit: "the LORD being merciful to him" — God's compassion seizes him and drags him out of the city.

The escape instructions are specific: flee to the hills, do not look back, do not stop anywhere (v. 17). Lot negotiates even here, asking to go to the small city of Zoar rather than the hills (vv. 18–22). Remarkably, God grants the request — yet further evidence of grace extended to a man whose faith was minimal.

Fire and sulfur rain from the LORD out of heaven on Sodom and Gomorrah (v. 24). The destruction is complete: the cities, the plain, all the inhabitants, and all the vegetation (v. 25). Archaeological evidence suggests the cities of the plain were located near the southern end of the Dead Sea; the geological record shows catastrophic disruption consistent with the biblical account, though the exact correspondence remains debated. What Scripture emphasizes is the agent of destruction: it came from the LORD — this is divine judgment, not merely natural disaster.

Lot's wife looks back (v. 26) and becomes a pillar of salt. Jesus references her in Luke 17:32: "Remember Lot's wife." Her backward look was more than physical disobedience — it was a heart still attached to what God was destroying. Salt in the ancient Near East could signify both preservation (that which endures) and desolation (the land cursed with salt, Deut. 29:23). Her fate is a warning: grace extended is not grace deserved, and those who look back toward judgment risk being caught in it.

Abraham rises early the next morning and looks toward Sodom from afar (v. 27–28). He sees the smoke rising like the smoke of a furnace — a phrase recalling the theophanic smoke at Sinai (Ex. 19:18). The intercessor watches the result of the judgment he prayed to limit.

The final section (vv. 30–38) is disturbing. Lot, fearing Zoar, goes to the hills anyway — the very destination he had refused. Living in a cave with his daughters, the daughters — believing they are the last humans alive — give their father wine and sleep with him on successive nights. From these unions come Moab and Ammon, neighboring peoples who will have a complex and often hostile relationship with Israel throughout the Old Testament. The narrative does not vindicate the daughters' logic or action; it records the origin of these peoples and underscores the devastating downstream consequences of Lot's spiritual compromise. He raised daughters in Sodom, and Sodom's desperation shaped their thinking.""",
        "chapter_overview": "Two angels arrive at Sodom; Lot hosts them; the men of Sodom surround the house demanding the visitors for sexual violence; the angels strike the crowd blind; Lot and his family are dragged out before fire and sulfur destroy Sodom and Gomorrah; Lot's wife looks back and becomes a pillar of salt; Lot's daughters sleep with him in a cave and conceive Moab and Ammon.",
        "original_language_notes": [
            {"term": "יָדַע (yada)", "language": "Hebrew", "verse": 5, "words_used": ["yada"], "meaning": "'To know' — used here as a euphemism for sexual relations (cf. Gen. 4:1). The demand of the men of Sodom is unambiguous sexual violation. The same word is used in v. 8 when Lot refers to his daughters 'who have not known a man,' confirming the sexual sense throughout this passage."},
            {"term": "וַיִּתְמַהְמַהּ (va-yitmahemah)", "language": "Hebrew", "verse": 16, "words_used": ["va-yitmahemah"], "meaning": "'And he lingered/hesitated.' A rare intensive form conveying repeated or prolonged delay. The intensified form emphasizes that Lot was deeply reluctant to leave even with destruction imminent. The grace of God is visible in the fact that the angels physically took him by the hand and pulled him out."},
            {"term": "גָּפְרִית וָאֵשׁ (gafrit va-esh)", "language": "Hebrew", "verse": 24, "words_used": ["gafrit", "va-esh"], "meaning": "'Sulfur and fire' — gafrit (sulfur/brimstone) is associated with the smell of divine judgment throughout the Old Testament (Deut. 29:23; Ps. 11:6; Isa. 34:9). The phrase sulfur and fire from the LORD out of heaven emphasizes that this was divine agency, not merely geological catastrophe."},
            {"term": "נְצִיב מֶלַח (netziv melach)", "language": "Hebrew", "verse": 26, "words_used": ["netziv", "melach"], "meaning": "'A pillar of salt.' Netziv can mean a garrison, a standing post, or a monumental pillar. Salt in this context signals total desolation and preservation of judgment's memory. Jesus' reference to Lot's wife in Luke 17:32 ('Remember Lot's wife') treats her fate as a perpetual warning about attachment to what God is judging."},
            {"term": "מוֹאָב / בֶּן עַמִּי (Moab / Ben Ammi)", "language": "Hebrew", "verse": 37, "words_used": ["Moab", "Ben-Ammi"], "meaning": "Moab means 'from my father' (a transparent reference to the incestuous origin). Ben Ammi means 'son of my people/kinsman.' These origin etymologies embed the shame of their origins within their very names, though God will later extend remarkable grace to individuals from these nations (e.g., Ruth the Moabite)."}
        ],
        "moral_lessons": [
            "Persistent, unrepentant wickedness invites divine judgment. Sodom was not destroyed impulsively but after outcry had reached heaven and investigation confirmed the report.",
            "God is merciful even in judgment — Lot, who lingered and barely trusted, was physically dragged to safety by divine mercy.",
            "Attachment to what God is judging — Lot's wife's backward gaze — is spiritually fatal. Grace must be embraced forward, not mourned backward.",
            "The moral and spiritual environment we inhabit shapes us: Lot raised daughters in Sodom and their crisis response reflected the moral poverty of that city.",
            "Hospitality, even imperfect hospitality, placed Lot in the path of rescue. His one act of welcome secured his salvation from the city."
        ],
        "application": "Jesus uses Lot's wife as a warning for the last days: people will be absorbed in ordinary life until judgment comes suddenly, and those whose hearts are still in what is being destroyed will be caught in it. Genesis 19 asks us: Where is our heart attached? Are we lingering in what God calls us to leave? Are there patterns of life, relationships, or habits that we hesitate to release even when God calls us forward? The mercy that saves us is also the mercy that insists we move — and move decisively.",
        "prayer": "LORD, have mercy on us as you had mercy on Lot — even when we linger. Help us not to be like Lot's wife, whose heart remained where her feet should have left. Give us the grace to move forward from what you are judging, to trust your rescue completely, and to not look back with longing at what you have condemned. For the sake of your Son who endured judgment so we could escape it, Amen.",
        "key_points": [
            "Lot's hospitality in Sodom echoes Abraham's, but under far darker circumstances — he fears what the city will do to the visitors.",
            "The men of Sodom, young and old, demand the visitors for sexual violation — the city's corruption is total.",
            "Lot's offer of his daughters to the mob reveals how profoundly Sodom had distorted his moral judgment.",
            "The angels blind the crowd and urgently press Lot to flee — Lot lingers, and God's mercy physically drags him out.",
            "Fire and sulfur from the LORD destroy Sodom, Gomorrah, and all the plain — divine judgment, not merely disaster.",
            "Lot's wife looks back and becomes a pillar of salt — Jesus cites her as a warning for the last days.",
            "Abraham watches the smoke from afar, the intercessor witnessing the outcome of his prayer.",
            "Lot's daughters, shaped by Sodom's culture, produce Moab and Ammon through incest — downstream consequences of moral compromise."
        ],
        "study_questions": [
            "Why does the text emphasize that 'all the men' of Sodom surrounded the house? What does this tell us about the scale and depth of the city's corruption?",
            "Lot lingered even as destruction was imminent, and God's mercy physically removed him. What does this teach us about divine grace operating in our weakness?",
            "Jesus says in Luke 17:32, 'Remember Lot's wife.' What is He warning His disciples about? How does this apply to discipleship in any generation?",
            "How does the environment Lot chose for his family (Sodom) affect what we see in his daughters' thinking in the cave? What does this say about the communities we raise our children in?",
            "Abraham interceded for Sodom (ch. 18) but the city was still destroyed. How do we understand the limits of intercessory prayer in light of human wickedness?",
            "Both Ruth (a Moabite) and Naamah (an Ammonite, mother of Rehoboam) appear in the lineage and history of Israel. How does God's use of these despised nations' descendants reveal something about grace?"
        ],
        "tags": ["Sodom", "judgment", "Lot", "rescue", "grace", "Lot's wife", "fire and sulfur", "Moab", "Ammon", "consequences"],
        "sources": []
    },
    {
        "book_id": 1,
        "book": "Genesis",
        "chapter": 20,
        "title": "Genesis 20 — Abraham in Gerar: The Wife-Sister Ruse Revisited",
        "summary": "Abraham travels to Gerar and again passes Sarah off as his sister. God warns King Abimelech in a dream, who returns Sarah untouched. Abraham intercedes for Abimelech's household, and God restores fertility to the women of Gerar — a foreshadowing of Isaac's imminent arrival.",
        "content": """Genesis 20 is sometimes dismissed as an awkward repetition of Genesis 12:10–20, where Abraham passed Sarah off as his sister in Egypt. But its placement immediately before Isaac's birth (ch. 21) and its theological depth make it indispensable. The chapter exposes a recurring weakness in Abraham, demonstrates God's sovereign protection of the covenant promise, and introduces a remarkable portrait of a pagan king who acts more righteously than the patriarch.

Abraham journeys from Mamre (the site of chapter 18's divine visit) southward to the Negeb and then to Gerar (v. 1). Gerar was a Philistine city-state near the coast of Canaan, ruled by Abimelech. There, Abraham instructs Sarah — again — to say she is his sister (v. 2). The same plan that endangered her in Egypt is repeated in Canaan. Abimelech takes Sarah into his household.

God intervenes with immediate directness: He comes to Abimelech in a dream at night and tells him "You are a dead man because of the woman you have taken, for she is a man's wife" (v. 3). The bluntness is remarkable — no warning, just the verdict and the reason. Abimelech protests with equal directness: he has not touched Sarah (v. 4). He appeals to his integrity and his clean hands (v. 5).

God's response is theologically striking: "Yes, I know that you have done this in the integrity of your heart, and it was I who kept you from sinning against me. Therefore I did not let you touch her" (v. 6). God affirms Abimelech's moral innocence while simultaneously claiming credit for preserving it. This is a profound theological statement: God can work through the integrity of a pagan ruler to accomplish His purposes, and God's sovereign protection can prevent a sin from occurring even before it is committed. The verb "I kept you" (chashakti) means I restrained, withheld, or held back — God intervened not after the fact but in the process.

God then commands Abimelech to return Sarah and instructs him that Abraham is a prophet (v. 7). This is the first use of the word prophet (nabi) in the Bible. Abraham's prophetic role is not primarily predictive speech but intercessory standing — he will pray for you and you shall live. The prophet's core function in this instance is intercession.

Abimelech rises early and tells his servants (v. 8). Their fear is immediate. He then confronts Abraham: "What did you do to us? What sin have I committed against you, that you have brought on me and my kingdom a great sin?" (v. 9). The irony is acute: the pagan king delivers a moral rebuke to the father of faith. Abraham's explanation reveals the complexity underneath his deception: he thought there was no fear of God in this place (v. 11), and Sarah is technically his half-sister — same father, different mother (v. 12). He has been practicing this deception since they left Haran (v. 13).

Abraham's fear-driven dishonesty is understandable but not excusable. He presumed the worst about Abimelech without evidence. He endangered Sarah and the entire covenant by the same scheme twice. His assumption — "there is no fear of God in this place" — was proven wrong by the very man who feared God's verdict in a dream and rose early to obey it. The pagan acted with more transparent piety than the patriarch.

Abimelech's response is magnanimous: he restores Sarah, gives Abraham sheep, oxen, servants, and silver (vv. 14–16), and invites Abraham to settle anywhere in his land (v. 15). He gives Sarah a thousand pieces of silver as a vindication before all who are with her — a public declaration of her honor.

Abraham then prays for Abimelech (v. 17), and God heals Abimelech, his wife, and female slaves so they could bear children, "for the LORD had closed all the wombs of the house of Abimelech because of Sarah, Abraham's wife" (v. 18). This closing and reopening of wombs is a narrative bracket: the barrenness theme that has haunted Abraham and Sarah throughout their story (11:30; 16:1; 17:17; 18:11) now becomes the very thing God demonstrates He can restore — just as He is about to restore Sarah's womb in chapter 21.

The chapter is a study in contrasts — Abimelech's integrity vs. Abraham's fear, Abraham's presumption vs. God's sovereign protection — and a gentle preparation for the reader: if God can open the wombs of Abimelech's household by Abraham's prayer, He can certainly open Sarah's.""",
        "chapter_overview": "Abraham journeys to Gerar and passes Sarah off as his sister; Abimelech takes her but is warned by God in a dream that she is Abraham's wife; Abimelech returns Sarah untouched with gifts; Abraham intercedes for Abimelech; God heals the closed wombs of Abimelech's household — a preview of what He will do for Sarah.",
        "original_language_notes": [
            {"term": "נָבִיא (navi)", "language": "Hebrew", "verse": 7, "words_used": ["navi"], "meaning": "'Prophet' — the first occurrence of this word in the Bible. In this context it refers not primarily to one who predicts the future but to one who stands in a special relationship with God and intercedes on behalf of others. Abraham's prophetic identity is defined here by his intercessory function."},
            {"term": "חָשַׂכְתִּי (chashakti)", "language": "Hebrew", "verse": 6, "words_used": ["chashakti"], "meaning": "'I restrained / I withheld / I kept back.' From chashak — to withhold, to spare. God's statement that He restrained Abimelech from sinning reveals divine prevenient action: God prevented a sin before it occurred, protecting both Abimelech's integrity and the covenant promise simultaneously."},
            {"term": "תֻּמַּת לְבָבְךָ (tumat levavecha)", "language": "Hebrew", "verse": 6, "words_used": ["tumat", "levavecha"], "meaning": "'The integrity/wholeness of your heart.' Tam means complete, whole, blameless — the same root as tamim in 17:1. God affirms that Abimelech's heart was whole before Him in this matter. The word used of Abimelech is the very word God used when commanding Abraham to walk before Him."},
            {"term": "כֶּסֶף (keseph)", "language": "Hebrew", "verse": 16, "words_used": ["keseph"], "meaning": "'Silver' — here specifically 1,000 pieces given as a vindication payment. In ancient Near Eastern legal contexts, silver compensated for dishonor and served as public restitution. Abimelech's gift publicly restores Sarah's reputation — a form of ancient justice."},
            {"term": "עָצַר (atsar)", "language": "Hebrew", "verse": 18, "words_used": ["atsar"], "meaning": "'To shut, close, restrain.' 'The LORD had closed (atsar) all the wombs.' The same verb is used in 1 Samuel 1:5–6 for Hannah's barrenness. The closing and opening of wombs in this passage directly previews what God is about to do for Sarah — the ultimate resolution of the barrenness theme."}
        ],
        "moral_lessons": [
            "Fear-driven deception in a believer can expose others to harm and damage one's witness before the very people we assumed were godless.",
            "God's sovereign protection does not require our cooperation — He can guard His promises despite our failures.",
            "Presuming the worst about those who do not share our faith is a failure of perception: Abimelech feared God more visibly in this episode than Abraham did.",
            "Even when believers fail, God remains faithful to His promises — the covenant was not cancelled by Abraham's deception.",
            "Intercession can bring healing even to those we have wronged: Abraham's prayer for Abimelech restores what his sin disrupted."
        ],
        "application": "Genesis 20 is an uncomfortable mirror. Abraham is the man of faith — the one with the covenant, the one who prayed boldly in chapter 18 — and yet here he compromises out of fear and endangers his wife to protect himself. The chapter asks: Are there patterns of fear-driven behavior in your life that you have repeated more than once? Are you presuming that people around you do not fear God, only to be surprised by their integrity? And can you intercede for those you have wronged, as Abraham prayed for Abimelech? The grace of this chapter is that God's purposes were not derailed by Abraham's failure — but neither were the consequences avoided entirely.",
        "prayer": "Father, forgive us for the ways we let fear override faith and lead us into patterns of deception or compromise. Forgive us for presuming the worst about others — for assuming that those outside our community have no fear of you. Protect the promises you have made to us even when our failures threaten them, and grant us the humility to intercede for those we have wronged. In Jesus' name, Amen.",
        "key_points": [
            "Abraham repeats the wife-sister deception used in Egypt — revealing a persistent fear-driven pattern despite his covenant history with God.",
            "Abimelech is warned by God in a dream with direct, urgent language: 'You are a dead man.'",
            "God affirms Abimelech's integrity while claiming credit for keeping him from sinning — a profound example of prevenient divine protection.",
            "The first use of the word 'prophet' (navi) in the Bible applies to Abraham, defined here by his intercessory role.",
            "Abimelech rebukes Abraham morally — the pagan king acts with more visible fear of God than the covenant patriarch.",
            "Abraham's explanation reveals the deception was a long-standing practice since leaving Haran — habitual, not impulsive.",
            "Abimelech's generous restitution publicly restores Sarah's honor with silver and an open invitation to his land.",
            "God closes and then reopens the wombs of Abimelech's household — a narrative preview of what He will do for Sarah in chapter 21."
        ],
        "study_questions": [
            "Why does Abraham repeat a scheme that already failed in Egypt? What does this suggest about deeply rooted patterns of fear even in mature believers?",
            "God tells Abimelech 'I know you acted with integrity' and 'I restrained you.' What does God's protection of Abimelech's integrity reveal about divine prevenient grace?",
            "Abimelech rises early, summons his servants, and they are all afraid (v. 8). How does this response compare to Abraham's fear-driven behavior in the same chapter?",
            "The word 'prophet' first appears in the Bible here, applied to Abraham in his intercessory role. How does this definition of prophecy as intercession shape your understanding of prophetic ministry?",
            "Abraham assumed 'there is no fear of God in this place' (v. 11). How should this corrected assumption shape how we approach and speak about people outside the church?",
            "The closing of Abimelech's household's wombs (v. 18) directly precedes Isaac's birth (ch. 21). How does God use this episode to prepare the reader for the fulfillment of the promise?"
        ],
        "tags": ["Abraham", "Abimelech", "deception", "fear", "prophet", "intercession", "God's faithfulness", "prevenient grace", "Gerar"],
        "sources": []
    }
]

def get_or_create_batch(conn):
    cur = conn.cursor()
    cur.execute("INSERT INTO commentary_generation_batches DEFAULT VALUES" if False else
                "SELECT 1")  # placeholder
    # Just use a timestamp-based batch reference
    return BATCH_UUID

def entry_exists(conn, collection_id, book_id, chapter):
    cur = conn.cursor()
    cur.execute("""
        SELECT id, content FROM commentary_entries
        WHERE collection_id=? AND book_id=? AND chapter=?
          AND language_code='en' AND reference_scope='chapter' AND deleted_at IS NULL
        LIMIT 1
    """, (collection_id, book_id, chapter))
    row = cur.fetchone()
    if row is None:
        return False
    # Check if content is shallow (less than 200 chars)
    content = row[1] or ""
    return len(content) >= 200

def insert_entry(conn, chap_data, batch_uuid):
    cur = conn.cursor()
    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"
    entry_uuid = str(uuid.uuid4())

    key_points_json = json.dumps(chap_data["key_points"])
    study_questions_json = json.dumps(chap_data["study_questions"])
    tags_json = json.dumps(chap_data["tags"])

    cur.execute("""
        INSERT INTO commentary_entries (
            uuid, collection_id, book_id, chapter,
            verse_start, verse_end, reference_scope,
            title, summary, content, application, prayer,
            key_points, study_questions,
            language_code, theological_perspective, status,
            is_ai_generated, ai_model_name, ai_generation_batch_uuid,
            word_count, sync_status, created_at, updated_at
        ) VALUES (
            ?, ?, ?, ?,
            NULL, NULL, 'chapter',
            ?, ?, ?, ?, ?,
            ?, ?,
            'en', 'evangelical', 'draft',
            1, 'claude-sonnet-4-6', ?,
            ?, 'local', ?, ?
        )
    """, (
        entry_uuid, COLLECTION_ID, chap_data["book_id"], chap_data["chapter"],
        chap_data["title"], chap_data["summary"], chap_data["content"],
        chap_data["application"], chap_data["prayer"],
        key_points_json, study_questions_json,
        batch_uuid,
        len(chap_data["content"].split()), now, now
    ))
    conn.commit()
    return entry_uuid, now

def write_json_backup(chap_data, entry_uuid, created_at):
    book_id = chap_data["book_id"]
    book_slug = chap_data["book"].lower().replace(" ", "-")
    chapter = chap_data["chapter"]

    folder = GENERATED_DIR / f"{book_id:02d}-{book_slug}"
    folder.mkdir(parents=True, exist_ok=True)

    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

    payload = {
        "uuid": entry_uuid,
        "collection_name": "Believers Sword Commentaries",
        "author_type": "ai",
        "language_code": "en",
        "theological_perspective": "evangelical",
        "status": "draft",
        "book_id": book_id,
        "book": chap_data["book"],
        "chapter": chapter,
        "title": chap_data["title"],
        "summary": chap_data["summary"],
        "content": chap_data["content"],
        "chapter_overview": chap_data["chapter_overview"],
        "original_language_notes": chap_data["original_language_notes"],
        "moral_lessons": chap_data["moral_lessons"],
        "application": chap_data["application"],
        "prayer": chap_data["prayer"],
        "key_points": chap_data["key_points"],
        "study_questions": chap_data["study_questions"],
        "tags": chap_data["tags"],
        "sources": chap_data["sources"],
        "created_at": created_at,
        "updated_at": now
    }

    # Verify no forbidden keys
    forbidden = {"is_ai_generated", "model_name", "prompt_version"}
    assert not (forbidden & set(payload.keys())), f"Forbidden key found: {forbidden & set(payload.keys())}"

    json_path = folder / f"{chapter:02d}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    # Verify it parses back
    with open(json_path, "r", encoding="utf-8") as f:
        parsed = json.load(f)
    assert not (forbidden & set(parsed.keys())), "Forbidden key in parsed JSON"

    return str(json_path)

def update_progress(conn, last_book_id, last_book, last_chapter):
    # Determine next
    book_chapters = {
        1: ("Genesis", 50), 2: ("Exodus", 40), 3: ("Leviticus", 27),
        4: ("Numbers", 36), 5: ("Deuteronomy", 34),
    }

    next_book_id = last_book_id
    next_chapter = last_chapter + 1

    if next_book_id in book_chapters and next_chapter > book_chapters[next_book_id][1]:
        next_book_id += 1
        next_chapter = 1

    next_book = book_chapters.get(next_book_id, ("Unknown", 0))[0]
    completed = (last_book_id >= 66)

    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

    # Update DB progress
    cur = conn.cursor()
    cur.execute("""
        UPDATE commentary_generation_progress
        SET current_book_id=?, current_chapter=?,
            last_completed_book_id=?, last_completed_chapter=?,
            updated_at=?
        WHERE id=1
    """, (next_book_id, next_chapter, last_book_id, last_chapter, now))
    conn.commit()

    # Update JSON
    progress = {
        "next_book_id": next_book_id,
        "next_book": next_book,
        "next_chapter": next_chapter,
        "last_completed_book_id": last_book_id,
        "last_completed_book": last_book,
        "last_completed_chapter": last_chapter,
        "completed": completed,
        "updated_at": now
    }
    with open(PROGRESS_JSON, "w") as f:
        json.dump(progress, f, indent=2)

    return next_book_id, next_book, next_chapter

def append_log(batch_uuid, start_ref, end_ref, generated, skipped, inserted, files):
    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"
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
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

def main():
    conn = sqlite3.connect(DB_PATH)

    chapters_generated = 0
    chapters_skipped = 0
    db_rows_inserted = 0
    files_written = []
    start_ref = None
    end_ref = None
    last_book_id = None
    last_book = None
    last_chapter = None

    for chap in CHAPTERS:
        book_id = chap["book_id"]
        book = chap["book"]
        chapter = chap["chapter"]
        ref = f"{book} {chapter}"

        if start_ref is None:
            start_ref = ref

        if entry_exists(conn, COLLECTION_ID, book_id, chapter):
            print(f"SKIP: {ref} already exists with content")
            chapters_skipped += 1
        else:
            print(f"GENERATING: {ref} — {chap['title']}")
            entry_uuid, created_at = insert_entry(conn, chap, BATCH_UUID)
            json_path = write_json_backup(chap, entry_uuid, created_at)
            chapters_generated += 1
            db_rows_inserted += 1
            files_written.append(json_path)
            print(f"  -> DB row inserted, JSON written: {json_path}")

        end_ref = ref
        last_book_id = book_id
        last_book = book
        last_chapter = chapter

    # Update progress
    next_book_id, next_book, next_chapter = update_progress(conn, last_book_id, last_book, last_chapter)
    conn.close()

    # Log
    append_log(BATCH_UUID, start_ref, end_ref, chapters_generated, chapters_skipped, db_rows_inserted, files_written)

    print("\n=== RUN SUMMARY ===")
    print(f"Range: {start_ref} — {end_ref}")
    print(f"Generated: {chapters_generated}, Skipped: {chapters_skipped}")
    print(f"DB rows inserted: {db_rows_inserted}")
    print(f"Files written: {len(files_written)}")
    for f in files_written:
        print(f"  {f}")
    print(f"Next starting reference: {next_book} {next_chapter} (book_id={next_book_id})")

if __name__ == "__main__":
    main()
