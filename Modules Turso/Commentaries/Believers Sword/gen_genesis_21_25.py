#!/usr/bin/env python3
"""Generate commentaries for Genesis 21-25."""
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
        "chapter": 21,
        "title": "Genesis 21 — Isaac Born, Ishmael Sent Away, and the Covenant at Beersheba",
        "summary": "The LORD does for Sarah exactly what He promised — Isaac is born. The presence of Ishmael threatens the inheritance, and God commands Hagar and Ishmael to be sent away, again providing for Hagar in the wilderness. The chapter closes with Abraham's covenant with Abimelech at Beersheba.",
        "content": """Genesis 21 opens with one of the Bible's most joyful announcements: "The LORD visited Sarah as he had said, and the LORD did to Sarah as he had promised. And Sarah conceived and bore Abraham a son in his old age at the time of which God had spoken to him" (vv. 1–2). Three parallel verbs — visited, said, promised — underscore that this birth is entirely the fulfillment of God's specific, personal word. Nothing is left to chance or natural explanation. God said it; God did it.

Abraham calls his son Isaac (Yitzchak — "he laughs") as God commanded (v. 3). He circumcises him on the eighth day (v. 4), faithful to the covenant sign of chapter 17. Every detail confirms that this is the covenant child. Abraham is one hundred years old at Isaac's birth (v. 5), and Sarah's response is a burst of theological joy: "God has made laughter for me; everyone who hears will laugh over me" (v. 6). The laughter that began in private incredulity (17:17; 18:12) has now become public joy shared by all who hear. God transformed her laughter from disbelief to delight.

Sarah's question — "Who would have said to Abraham that Sarah would nurse children?" (v. 7) — is rhetorical worship. No human prediction could have imagined this. It celebrates the impossibility made reality by divine power. The chapter earlier closed Abimelech's household wombs (20:18); now it opens Sarah's womb at ninety. God is the Lord of reproduction, of life, of the impossible.

The conflict in the household surfaces at Isaac's weaning feast (v. 8). Weaning in the ancient world typically occurred around age two to three, making Isaac approximately that age and Ishmael around fifteen to seventeen. Sarah sees Ishmael "laughing" (metzachek, v. 9) — the same root as Isaac's name. The Hebrew is ambiguous: was Ishmael mocking Isaac? Playing? Paul in Galatians 4:29 interprets this as persecution ("he who was born according to the flesh was persecuting him who was born according to the Spirit"). Whatever the precise action, Sarah perceives a threat to Isaac's inheritance and demands Hagar and Ishmael be cast out.

Abraham is deeply distressed on account of his son (v. 11). Thirteen years of relationship with Ishmael created genuine paternal love. God's instruction is clear: "Listen to whatever Sarah says to you, for through Isaac shall your offspring be named" (v. 12). This is not an endorsement of Sarah's tone but a confirmation of the covenantal reality: Isaac is the heir. God adds a promise: Ishmael too will become a nation, because he is Abraham's son (v. 13).

Abraham rises early (v. 14) — again the characteristic of obedient action — takes bread and a skin of water, and sends Hagar and Ishmael away. The brevity of the description emphasizes the pain. They wander in the wilderness of Beersheba. When the water is gone, Hagar places Ishmael under a bush and sits nearby, unable to watch him die (vv. 15–16). Her cry is the cry of a mother who has lost hope.

God hears the voice of the boy (v. 17). The Angel of God calls from heaven — the same divine messenger who found Hagar in chapter 16 — and asks "What troubles you, Hagar?" God says He has heard the voice of the boy where he is. Hagar is told to lift up the boy and hold him by the hand (v. 18). Then God opens her eyes and she sees a well of water (v. 19). The well was there; the provision was already in place. What changed was Hagar's perception, opened by God.

Ishmael grows up in the wilderness of Paran, becomes an expert archer, and his mother takes a wife for him from Egypt (vv. 20–21). God was with the boy — the same phrase used of Joseph in chapter 39. The covenant runs through Isaac, but God's general providential care extends to Ishmael.

The chapter closes with Abraham's covenant with Abimelech at Beersheba (vv. 22–34). Abimelech acknowledges that God is with Abraham in all he does (v. 22) — a pagan king testifying to what is visibly evident. They swear an oath at a well Abraham had dug, confirming ownership over the water source. Abraham plants a tamarisk tree and calls on the name of the LORD, the Everlasting God (El Olam, v. 33). Beersheba means "well of the oath" or "well of seven" — and it becomes a foundational location in the patriarchal narratives. The covenant with Abimelech is not merely political; it is Abraham's public acknowledgment that God is present and trustworthy in all of life.""",
        "chapter_overview": "Isaac is born; Sarah's laughter turns from disbelief to joy; conflict over Ishmael leads to Hagar and Ishmael being sent away; God provides water in the wilderness for Hagar and Ishmael; Ishmael grows to become an archer; Abraham makes a covenant with Abimelech at Beersheba and calls on El Olam.",
        "original_language_notes": [
            {"term": "פָּקַד (paqad)", "language": "Hebrew", "verse": 1, "words_used": ["paqad"], "meaning": "'Visited, attended to, appointed.' The LORD paqad Sarah — a word that carries the weight of deliberate, sovereign attention. God does not merely allow Sarah to conceive; He actively attends to her situation. The same word describes God visiting Israel in Egypt (Ex. 3:16; 4:31)."},
            {"term": "מְצַחֵק (metzachek)", "language": "Hebrew", "verse": 9, "words_used": ["metzachek"], "meaning": "A piel (intensive) participle from tzachak (to laugh), the same root as Isaac's name. This causative/intensive form can imply mocking, playing, or celebrating. Paul interprets it as persecution (Gal. 4:29). The ambiguity may be intentional — Ishmael's laughter threatens to usurp Isaac's laughter."},
            {"term": "אֵל עוֹלָם (El Olam)", "language": "Hebrew", "verse": 33, "words_used": ["El", "Olam"], "meaning": "'The Everlasting God' or 'God of eternity.' Olam means long duration, eternity, or that which is beyond the horizon. This divine name appears here for the first time in Scripture and anchors God's covenant faithfulness to His eternal nature — He keeps promises forever because He is forever."},
            {"term": "בְּאֵר שֶׁבַע (Beer Sheva)", "language": "Hebrew", "verse": 31, "words_used": ["Beer", "Sheva"], "meaning": "'Well of seven' or 'Well of the oath.' Sheva can mean both seven (referring to the seven lambs used in the oath ceremony) and oath (from shava, to swear). The double meaning is deliberate, embedding both the event and the number seven (completeness/covenant) into the place name."},
            {"term": "וַיִּפְקַח אֱלֹהִים אֶת עֵינֶיהָ (va-yiftach Elohim et eineiha)", "language": "Hebrew", "verse": 19, "words_used": ["va-yiftach", "Elohim", "et", "eineiha"], "meaning": "'And God opened her eyes.' The well was already there — what God provided was perception. The phrase is used in Scripture for spiritual sight-giving: Balaam's eyes opened to see the angel (Num. 22:31), Elisha's servant's eyes opened to see the angelic army (2 Kings 6:17). Divine provision often precedes our ability to perceive it."}
        ],
        "moral_lessons": [
            "God's promises are fulfilled precisely as stated, on His timetable, not ours — Sarah's impossibility became reality at exactly the time God appointed.",
            "Covenantal joy is public and contagious; what God does in one life becomes testimony for all who hear.",
            "Obedience often requires painful action (Abraham sending Ishmael away) even when God's word is clear; obedience is not always emotionally easy.",
            "God hears cries in wilderness places — Hagar and Ishmael were not forgotten even when abandoned by human plans.",
            "Divine provision may already be present but invisible until God opens our eyes; prayer often recalibrates our perception to see what is already there."
        ],
        "application": "Genesis 21 holds two kinds of promise: the promise of God's faithfulness to what He has spoken (Isaac's birth) and the promise of God's care for those who are pushed to the margins (Hagar's well). Both are needed. Where in your life has God's specific promise been fulfilled in a way that made you want to shout 'Who would have said it?' And where are you or someone you know in a Hagar-moment — water gone, hope depleted — needing God to open eyes to a provision that is already in place?",
        "prayer": "Lord God, Everlasting God, thank you that your promises are not forgotten. Thank you that what you say, you do — that what seemed impossible becomes the occasion for your greatest joy. Open our eyes today to the wells you have placed in our wilderness. Hear the cries of those who are depleted and forgotten. And multiply the joy of what you have done for us so that everyone who hears will laugh with us. In Jesus' name, Amen.",
        "key_points": [
            "Isaac's birth is explicitly attributed to the LORD's visitation and faithful fulfillment of His specific promise.",
            "Sarah's laughter transforms from private incredulity to public worship — joy shared with all who hear.",
            "Ishmael's 'laughing' (metzachek) provokes the crisis that separates the covenant heir from Hagar's son.",
            "God instructs Abraham to send Hagar and Ishmael away, confirming Isaac as covenant heir while promising Ishmael a nation.",
            "In the wilderness, God hears Ishmael's voice and opens Hagar's eyes to a well already present — provision preceding perception.",
            "Abimelech testifies that God is with Abraham, reflecting Abraham's visible covenant blessing before pagans.",
            "Abraham calls on El Olam (the Everlasting God) at Beersheba — anchoring his covenant relationship to God's eternal nature.",
            "Beersheba becomes a foundational location, its name encoding both the number of covenant and the act of swearing."
        ],
        "study_questions": [
            "Why does the narrator repeat three times in verse 1 that God did what He said? What is this emphasis communicating to readers who wait on promises?",
            "How does Isaac's birth as laughter-turned-joy explain the New Testament concept that believers are 'children of the promise, like Isaac' (Gal. 4:28)?",
            "What does it reveal about Abraham's heart that he was deeply distressed about Ishmael even though God had commanded the separation?",
            "The well was already there — God opened Hagar's eyes to see it. Can you think of a time when God opened your perception to see provision that was already in place?",
            "Abimelech tells Abraham, 'God is with you in all that you do' (v. 22). What behaviors or characteristics in Abraham's life would have made this visible to a pagan king?",
            "How does Abraham calling on El Olam — the Everlasting God — at Beersheba relate to the promises being made across generations?"
        ],
        "tags": ["Isaac", "Sarah", "Hagar", "Ishmael", "El Olam", "Beersheba", "promise fulfilled", "covenant", "laughter", "provision"],
        "sources": []
    },
    {
        "book_id": 1,
        "book": "Genesis",
        "chapter": 22,
        "title": "Genesis 22 — The Binding of Isaac and the God Who Provides",
        "summary": "God tests Abraham by commanding him to offer Isaac as a burnt offering on Mount Moriah. Abraham obeys, but at the last moment God provides a ram as a substitute. The chapter is Scripture's most profound portrait of obedient faith and God's provision — YHWH Yireh — and anticipates Christ's sacrifice.",
        "content": """Genesis 22 stands alone in the Old Testament. It has been called the Akedah (the Binding), and it is one of Scripture's most theologically dense and emotionally intense narratives. Jewish readers, Christian theologians, and skeptical critics have all recognized that something extraordinary is happening here. For the believer, it is the Old Testament's clearest preview of the cross.

The chapter opens with three words that alter everything: "After these things God tested Abraham" (v. 1). The word tested (nissah) is crucial. This was not temptation toward sin; it was a divine examination of the faith that had been growing in Abraham across decades. The reader knows it is a test. Abraham does not. He hears only the command: "Take your son, your only son Isaac, whom you love, and go to the land of Moriah, and offer him there as a burnt offering" (v. 2). Each successive phrase intensifies the demand: your son — your only son — Isaac — whom you love. God does not minimize what He is asking. He names the love that makes the sacrifice incomprehensible.

Abraham's response is immediate. He rises early in the morning (v. 3), the third time in Genesis that early rising marks obedient urgency (cf. 19:27; 21:14). He does not argue, delay, or negotiate as he did in chapter 18 over Sodom. He saddles his donkey, takes wood, his two servants, and Isaac, and departs for Moriah.

The journey takes three days (v. 4) — three days of silence, of walking toward an altar where Abraham will kill the son of promise. What was Abraham thinking across those three days? The New Testament provides the answer: Hebrews 11:17–19 states that Abraham "considered that God was able even to raise him from the dead, from which, figuratively speaking, he did receive him back." Abraham's obedience was not blind or disconnected from theology. It was anchored in resurrection faith — if God could give Isaac in the first place, God could give him back from death.

At the foot of the mountain, Abraham tells the servants: "Stay here with the donkey; I and the boy will go over there and worship and come back to you" (v. 5). We. Both of us. Come back. Either this is a masterful cover story or Abraham genuinely expected them both to return. The latter is consistent with Hebrews 11.

The walk up the mountain carries unbearable pathos. Isaac carries the wood; Abraham carries the fire and the knife — the instruments of sacrifice (v. 6). Isaac calls out "Father" and Abraham answers "Here I am, my son" — the same words Abraham spoke to God at the chapter's opening (v. 1). Then the question every reader has been dreading: "Behold, the fire and the wood, but where is the lamb for a burnt offering?" Abraham's answer is prophetic: "God will provide for himself the lamb for a burnt offering, my son" (v. 8). He spoke with more truth than he may have known.

They arrive at the place God had appointed. Abraham builds an altar, arranges the wood, binds Isaac, and lays him on the altar (v. 9). Isaac is no longer an infant; he is old enough to carry wood up a mountain. Jewish tradition places him at 25–37 years old. His cooperation is implied in the text — there is no mention of struggle or escape. The son submits to the father's will, as Christ submitted to the Father (John 10:17–18; Phil. 2:8).

Abraham stretches out his hand and takes the knife (v. 10). At this moment — the last possible moment, the moment of no return — the Angel of the LORD calls from heaven: "Abraham, Abraham!" The repetition of the name signals urgency and intimacy (cf. "Moses, Moses" Ex. 3:4; "Samuel, Samuel" 1 Sam. 3:10). "Do not lay your hand on the boy or do anything to him, for now I know that you fear God, seeing you have not withheld your son, your only son, from me" (v. 12).

Abraham looks up and sees a ram caught in a thicket by its horns (v. 13). The ram is the substitute; it dies in Isaac's place. Abraham offers it as a burnt offering in the place of his son. He names the place YHWH Yireh — "the LORD will provide" or "the LORD sees/will see." The name carries a double meaning in Hebrew (yireh = will see or will provide), connecting back to El Roi of chapter 16. The Lord who sees is the Lord who provides; divine vision produces divine provision.

The theological weight of this chapter extends in multiple directions:

1. **Christological typology**: The parallels with Christ's sacrifice are numerous and deliberately drawn by the New Testament. Isaac is the beloved, only son (v. 2; cf. John 3:16). He carries the wood of his own sacrifice (v. 6; cf. John 19:17). He submits to the father. There is a three-day journey (v. 4; cf. the resurrection on the third day). The lamb provided by God (v. 8; cf. John 1:29, "Behold the Lamb of God"). A mountain in Jerusalem — Moriah is identified with the Temple Mount in 2 Chronicles 3:1. But the great difference is that God stops Abraham's hand; He did not stop His own. "He who did not spare his own Son but gave him up for us all" (Rom. 8:32). YHWH Yireh ultimately names the cross.

2. **The nature of faith**: Abraham's faith was not passive or intellectual — it cost him everything. James 2:21–23 cites this event as the proof of Abraham's righteousness: "Faith was active along with his works, and faith was completed by his works." True faith produces costly obedience.

3. **Opposition to child sacrifice**: The surrounding Canaanite culture practiced child sacrifice to their gods. This chapter may be read as a definitive statement: Israel's God does not ultimately demand this. He provides the substitute. The test established that YHWH is the God who provides, not the God who consumes.""",
        "chapter_overview": "God commands Abraham to sacrifice Isaac on Mount Moriah; Abraham obeys and travels three days; at the last moment God stops him and provides a ram as a substitute; Abraham names the place YHWH Yireh; God reconfirms the covenant blessing because Abraham did not withhold his only son.",
        "original_language_notes": [
            {"term": "נִסָּה (nissah)", "language": "Hebrew", "verse": 1, "words_used": ["nissah"], "meaning": "'Tested, proved, tried.' From nasah — a divine testing that reveals and confirms the quality of faith, not a temptation toward sin. The same root is used for Israel's testing in the wilderness (Ex. 15:25; Deut. 8:2). God tests to prove and establish, not to destroy."},
            {"term": "יֶחֱזוּ (yechezu) / יִרְאֶה (yireh)", "language": "Hebrew", "verse": 14, "words_used": ["yireh"], "meaning": "YHWH Yireh — 'The LORD will provide' or 'The LORD will see/be seen.' Yireh is the future of ra'ah (to see). The double meaning (seeing = providing) connects to El Roi of chapter 16 and suggests that divine seeing is always active provision — God does not observe passively but acts on what He sees."},
            {"term": "יָחִיד (yachid)", "language": "Hebrew", "verse": 2, "words_used": ["yachid"], "meaning": "'Only, unique, sole.' Your only son. Yachid appears also in Psalm 22:20 ('my only life') and Zechariah 12:10 ('as one mourns for an only son'). John 3:16 uses the Greek equivalent monogenes for Christ — 'his one and only Son' — directly echoing the Akedah."},
            {"term": "הַמַּאֲכֶלֶת (ha-maakheleth)", "language": "Hebrew", "verse": 6, "words_used": ["ha-maakheleth"], "meaning": "'The knife' — a word derived from akhal (to eat), literally 'the eating instrument,' a large sacrificial knife for slaughtering animals. Its use for Isaac's near-sacrifice makes the intention unmistakable and the substitution all the more dramatic."},
            {"term": "בְּהַר יְהוָה יֵרָאֶה (behar YHWH yera'eh)", "language": "Hebrew", "verse": 14, "words_used": ["behar", "YHWH", "yera'eh"], "meaning": "'On the mountain of the LORD it shall be provided/seen.' The passive form (niphal of ra'ah) implies that the LORD makes Himself seen or makes provision seen. The saying became proverbial — pointing to the hill of God's provision, later identified with Moriah, where Solomon's Temple was built and where Christ was crucified."}
        ],
        "moral_lessons": [
            "God tests faith not to destroy us but to reveal, prove, and strengthen what He has already built in us.",
            "Obedient faith acts before it fully understands — Abraham rose early and moved without explanation or negotiation.",
            "Resurrection faith enables costly obedience; Abraham could give Isaac because he believed God could raise him.",
            "God's provision arrives at the last moment — not because He was late, but because the fullness of the test required the fullness of the surrender.",
            "The substitute sacrifice is God's answer to human guilt and obligation; this is the grammar of the atonement."
        ],
        "application": "What is the 'Isaac' in your life — the gift you love more than the Giver, the thing you would find it most costly to surrender? Genesis 22 is not a call to morbid self-denial; it is a call to hold our greatest gifts with open hands, trusting the God who gave them. The chapter also presses us toward the cross: we understand what Abraham was asked to do, but God did not stop His own hand. He gave His only Son. YHWH Yireh has provided — completely, finally, at Golgotha.",
        "prayer": "Lord, you did not withhold your own Son for us. Forgive us for the gifts we clutch and the Isaacs we refuse to surrender. Give us resurrection faith — the confidence that what you give you can restore, and that your provision always arrives in time. Thank you for the ram caught in the thicket, and thank you even more for the Lamb of God who takes away the sin of the world. In His name, Amen.",
        "key_points": [
            "God tests Abraham — not tempts — calling for the sacrifice of Isaac, the son of promise, using the most emotionally piercing language: 'your son, your only son, whom you love.'",
            "Abraham's early rising and immediate obedience reflect faith matured through decades of covenant relationship.",
            "The three-day journey and Abraham's statement 'we will come back' suggest he expected God to raise Isaac — resurrection faith (Heb. 11:19).",
            "Isaac's submission as he carries the wood up the mountain prefigures Christ carrying the cross.",
            "At the final moment, the Angel of the LORD stops Abraham: 'Now I know that you fear God, seeing you have not withheld your son.'",
            "God provides a ram as substitute — the first full substitutionary sacrifice in the patriarchal narrative.",
            "YHWH Yireh — the LORD will provide/see — names the mountain and becomes a prophetic declaration pointing to Christ.",
            "The covenant blessing is reconfirmed and deepened: Abraham's seed will bless all nations because he did not withhold his son."
        ],
        "study_questions": [
            "The narrator tells us it is a 'test' before Abraham knows it. How does this omniscient perspective shape how we read the narrative and how we read our own difficult experiences?",
            "Hebrews 11:19 says Abraham reasoned that God could raise Isaac from the dead. How does resurrection faith change the nature of costly obedience?",
            "What are the specific parallels between Isaac and Christ in this chapter? Where does the type break down, and what does that break reveal?",
            "Why does God stop at the last possible moment — the knife raised — rather than intervening earlier? What is accomplished by pressing to the limit of surrender?",
            "How does YHWH Yireh name both this moment and the cross? What does it mean that the same God who saw Abraham's need sees ours?",
            "What is the 'Isaac' you find hardest to surrender to God? What would it look like to place that gift on the altar with open hands?"
        ],
        "tags": ["Akedah", "Isaac", "sacrifice", "YHWH Yireh", "obedience", "faith", "substitute", "typology", "cross", "resurrection"],
        "sources": []
    },
    {
        "book_id": 1,
        "book": "Genesis",
        "chapter": 23,
        "title": "Genesis 23 — Sarah's Death and Abraham's First Foothold in the Promised Land",
        "summary": "Sarah dies at 127 years old at Hebron. Abraham, still a foreigner in Canaan, negotiates with the Hittites to purchase the cave of Machpelah as a burial site — his first legally owned piece of the promised land. The chapter reveals Abraham's faith, dignity, and the first concrete claim on the inheritance.",
        "content": """Genesis 23 is the Bible's most detailed account of a real estate transaction in the ancient Near East. It reads slowly and procedurally by modern standards — but that is precisely its point. Every detail matters, and what seems like background information is in fact the narrative recording a moment of extraordinary theological significance: Abraham, the man of promise, purchases his first permanent foothold in the land God promised him.

Sarah lived 127 years (v. 1). She is the only woman in the Bible whose age at death is recorded, underscoring her singular importance in redemptive history. She died at Kiriath-arba, that is, Hebron, in the land of Canaan (v. 2). The place name is deliberate: she dies in the promised land. Abraham comes to mourn and to weep for her (v. 2) — the brevity of this description should not mask the depth of grief. Sarah was the partner of Abraham's entire adult life, the mother of the covenant child, the woman who laughed in wonder when God made the impossible possible.

Abraham addresses the Hittites (v. 3) as "a sojourner and foreigner among you." The words are legally significant: Abraham has no claim to the land under existing arrangements. He cannot simply bury his wife — he must negotiate. He requests "property among you for a burying place" (v. 4). The Hittites respond with remarkable courtesy, calling him "a prince of God among us" (v. 6) — precisely the recognition Abimelech had offered earlier (21:22). Even Canaan's inhabitants can see that God's hand is on Abraham.

The Hittites offer him the choice of their tombs (v. 6). Abraham bows (v. 7) and specifically requests the cave of Machpelah, belonging to Ephron son of Zohar (v. 9). The negotiations are conducted at the gate of the city — the public, legal space for transactions in the ancient Near East (v. 10). Ephron, in the custom of Near Eastern courtesy, offers the field and cave as a gift (v. 11). Abraham refuses — critically. He insists on paying full price: "Let me give you money for the field. Accept it from me, so that I may bury my dead there" (v. 13).

Why refuse the gift? Because a gift can be recalled; a purchase cannot be disputed. Abraham is purchasing legal, permanent ownership of this ground. This is wisdom, not merely stubbornness. The land of promise will one day belong to his descendants not merely because God said so, but because their father paid for it in public, before witnesses.

Ephron names his price: four hundred shekels of silver (v. 15). This is substantial — enough to purchase a significant property. Abraham does not negotiate the price. He weighs the silver before the Hittites (v. 16), and the transaction is complete. The field of Machpelah — including the field, cave, all trees within the borders — is transferred to Abraham (vv. 17–18). The legal language is meticulous, as it would be in any ancient deed of ownership.

Abraham buries Sarah in the cave of Machpelah east of Mamre, in the land of Canaan (v. 19). The final verse is almost liturgical in its repetition: the field and cave "were made over to Abraham as property for a burying place by the Hittites" (v. 20). The covenant promise has its first tangible expression: the patriarchs will all be buried here (Abraham in 25:9; Isaac and Rebekah in 49:31; Jacob and Leah in 49:31). When Jacob in Egypt instructs his sons to bury him "with my fathers in the cave in the field of Machpelah" (49:29–32), he is holding onto the promise by holding onto the plot of land.

The Machpelah purchase is a monument to patient, practical, legally grounded faith. Abraham does not seize the land. He does not pray for miraculous possession. He navigates the existing legal and cultural systems with integrity and wisdom to secure what he needs. His grief does not immobilize him; his faith does not make him reckless. He weeps and then he acts — purchasing ground for the dead, trusting that the living promise will eventually fill the land.""",
        "chapter_overview": "Sarah dies at 127 in Hebron; Abraham mourns and then negotiates with the Hittites for a burial plot; he insists on purchasing — not receiving as a gift — the cave of Machpelah at full price (400 shekels of silver); this becomes the first legally owned piece of the promised land, where Sarah is buried.",
        "original_language_notes": [
            {"term": "גֵּר וְתוֹשָׁב (ger ve-toshav)", "language": "Hebrew", "verse": 4, "words_used": ["ger", "ve-toshav"], "meaning": "'Sojourner and foreigner/resident alien.' Ger means a temporary resident; toshav means a settled inhabitant. Together they describe Abraham's ambiguous legal status — he lives in the land but holds no legal claim to it. This self-description is the legal basis for his purchase request."},
            {"term": "נְשִׂיא אֱלֹהִים (nesi Elohim)", "language": "Hebrew", "verse": 6, "words_used": ["nesi", "Elohim"], "meaning": "'Prince of God' or 'mighty prince.' Nesi means one who is lifted up, a chief or leader. The Hittites honor Abraham with a title that acknowledges divine backing. The phrase shows that even those outside the covenant can perceive God's hand on the covenant people."},
            {"term": "שֶׁקֶל כֶּסֶף (shekel keseph)", "language": "Hebrew", "verse": 15, "words_used": ["shekel", "keseph"], "meaning": "'Shekel of silver.' A shekel was approximately 11 grams of silver, though weights varied by era and region. 400 shekels was a very significant sum — by comparison, Joseph was sold for 20 shekels (37:28) and Jeremiah later purchased a field for 17 shekels (Jer. 32:9). The full price signals Abraham's commitment to legal, undisputed ownership."},
            {"term": "עֹבֵר לַסֹּחֵר (over la-socher)", "language": "Hebrew", "verse": 16, "words_used": ["over", "la-socher"], "meaning": "'Current to the merchant' or 'according to the going merchant rate.' This technical commercial phrase confirms that Abraham paid market value, not a special rate. The transaction is transparent and commercially legitimate, suitable for legal documentation."},
            {"term": "מַעְפֵּלָה (Machpelah)", "language": "Hebrew", "verse": 9, "words_used": ["Machpelah"], "meaning": "Possibly from kapal (to double) — 'the double cave.' The cave may have had two chambers, or the name signals completeness and depth. Machpelah near Hebron is identified today with the Cave of the Patriarchs (Ibrahimi Mosque), a site holy to Jews, Christians, and Muslims."}
        ],
        "moral_lessons": [
            "Grief and faith are not opposites — Abraham weeps fully and then acts faithfully within the same chapter.",
            "Practical wisdom serves faith: Abraham's insistence on purchase rather than gift secured the legal foundation for the covenant's territorial claim.",
            "Integrity in ordinary transactions — business dealings, negotiations, paying full price — is a form of covenant faithfulness.",
            "The land of promise begins with a burial plot: faith holds the whole through the part, and the dead are buried where the living will one day inherit.",
            "Even those outside the covenant can honor and perceive God's work in the lives of His people."
        ],
        "application": "Genesis 23 is a chapter about grieving well and acting wisely. It models that faith does not skip past sorrow — Abraham mourns fully — but also does not stay in paralysis. He moves from tears to practical, legal action that serves the covenant's long-term future. For us, this means that the ordinary business of life — negotiations, purchases, legal arrangements — can be conducted with the same integrity and forward-looking faith. Our grief over loss does not cancel our responsibility to act wisely for those who come after us.",
        "prayer": "Father, we thank you that you are the God of the living and the dead, and that even burial grounds are held within your covenant purposes. Help us to grieve honestly without losing sight of the promises. Give us wisdom in the ordinary transactions of life to act with integrity and with an eye toward the inheritance you have promised us. In Christ's name, Amen.",
        "key_points": [
            "Sarah's age at death (127) is uniquely recorded — only hers among all biblical women — marking her singular covenant importance.",
            "Abraham mourns fully before acting, modeling that grief and faith coexist without contradiction.",
            "He identifies as 'sojourner and foreigner' — legally landless despite decades in Canaan — making his purchase necessary and strategic.",
            "The Hittites honor Abraham as 'a prince of God,' recognizing divine favor even from outside the covenant.",
            "Abraham refuses Ephron's gift and insists on full payment of 400 shekels — securing undisputable legal ownership.",
            "The transaction is conducted publicly at the city gate, with meticulous legal language, establishing permanent title.",
            "Machpelah becomes the patriarchal burial site — a down-payment on the promised land held by faith through death.",
            "The chapter models that the covenant's territorial promises are pursued through patience and legal integrity, not seizure."
        ],
        "study_questions": [
            "Why is Sarah's age at death recorded — a detail given to no other woman in the Bible? What does this suggest about her place in redemptive history?",
            "Why does Abraham refuse Ephron's gift of the land and insist on paying full price? What principle about ownership, faith, and integrity does this reveal?",
            "The Hittites call Abraham 'a prince of God.' How does a believer's conduct in ordinary life — including commercial negotiations — serve as a witness to those outside the faith?",
            "Genesis 23 is primarily about death, burial, and a real estate transaction. How does it function as an act of faith in the covenant promises?",
            "How does Abraham's practice of grief — mourning, then rising to act — model healthy, faith-filled responses to loss for us today?",
            "In what ways is the cave of Machpelah a symbol of patience in faith? What 'burial plots' are you holding in faith while waiting for the larger inheritance?"
        ],
        "tags": ["Sarah", "death", "burial", "Machpelah", "Hebron", "faith", "Hittites", "Ephron", "promised land", "grief"],
        "sources": []
    },
    {
        "book_id": 1,
        "book": "Genesis",
        "chapter": 24,
        "title": "Genesis 24 — Finding a Bride for Isaac: Providence, Prayer, and Partnership",
        "summary": "Abraham sends his servant to find a wife for Isaac from among his own people in Mesopotamia. The servant prays for a specific sign and Rebekah appears, fulfilling it precisely. The chapter is the Bible's longest narrative about a single event and a masterclass in discerning divine providence through prayer and attentiveness.",
        "content": """Genesis 24 is the longest chapter in Genesis and one of the longest single-episode narratives in the entire Old Testament. Its length is its message: God's sovereign direction of the smallest details of daily life — a woman drawing water, a servant's prayer, a camel kneeling — is worthy of extended, unhurried telling. This is a chapter about providence: the meticulous, intimate, daily outworking of God's covenant purposes.

Abraham, now old and full of years (v. 1), calls his most trusted servant — almost certainly Eliezer of Damascus (15:2) — and binds him with the most solemn oath available in the ancient world: swear by placing your hand under my thigh (v. 2), invoking the covenant of circumcision (ch. 17) and the reproductive future it symbolized. The mission: find a wife for Isaac not from the Canaanites but from Abraham's own kindred in Mesopotamia (vv. 3–4).

Abraham's reasoning is theological: to take Isaac back to the homeland would compromise the land promise (v. 6). God will send His angel before you (v. 7). Abraham speaks with confidence about divine guidance even before the journey begins — this is faith that has earned its certainty through decades of covenant walk.

The servant's prayer at the well in Nahor (vv. 12–14) is one of the Old Testament's greatest models of petition:
- He addresses God by covenant name and relationship: "O LORD, God of my master Abraham"
- He asks for specific guidance: "Grant me success today"
- He presents a specific, testable sign: the woman who offers water not only to him but to his camels
- The sign is not arbitrary: offering water to ten camels would require extensive, selfless labor (a camel drinks 25–40 gallons after a long journey). The servant is asking for a sign of extraordinary, proactive generosity.

Before he has finished praying, Rebekah comes out with her jar (v. 15). The timing is exquisite. She is described: beautiful in appearance, a virgin (v. 16). She draws water for the servant (v. 18) and then immediately, without being asked, adds: "I will draw water for your camels also, until they have finished drinking" (v. 19). She empties her jar and runs to draw more water — the very sign, performed with enthusiasm, before the servant has articulated the test.

The servant watches in silence (v. 21) — the Hebrew says he was "staring at her in silence, to know whether the LORD had prospered his journey." He gives her a gold ring and bracelets and asks who she is. She is Rebekah, daughter of Bethuel, son of Milcah and Nahor — Abraham's brother (v. 24). She is from Abraham's own family. The servant bows his head and worships the LORD (v. 26): "Blessed be the LORD, the God of my master Abraham, who has not forsaken his steadfast love and his faithfulness."

The servant's retelling of the story to Laban and Bethuel (vv. 34–49) doubles the narrative — but not wasted words. The repetition shows how the servant presents the case, what he emphasizes, and how he interprets the providence he witnessed. He recounts prayer, sign, fulfillment. Laban and Bethuel's response is theological: "The thing has come from the LORD; we cannot speak to you bad or good" (v. 50). Even the pagan household recognizes divine direction.

Rebekah's own consent is asked (v. 58): "Will you go with this man?" Her answer — "I will go" — is one of Scripture's most decisive one-line commitments. She goes with the servant, with her nurse, with attendants. They bless her with words that echo Abraham's blessing: "May your offspring possess the gate of those who hate them" (v. 60).

The meeting of Rebekah and Isaac (vv. 62–67) is tender and economical. Isaac goes out to meditate in the field at evening (v. 63). He looks up and sees camels coming. Rebekah looks up, sees Isaac, and asks who the man is. When told it is her future husband, she covers herself with a veil (v. 65). The servant tells Isaac everything. Isaac brings her into his mother Sarah's tent, and he loved her (v. 67). After the long grief of Sarah's death (ch. 23), Isaac is comforted.

The chapter is a sustained meditation on God's providence operating through human prayer, attentiveness, and response. The servant did not passively wait for a burning bush; he prayed specifically and watched carefully. Rebekah did not passively sit at home; she went to the well, drew water, and said yes to a journey she had not planned. Isaac was not passively waiting without meaning; he was meditating. Providence rarely involves humans as passive recipients — it usually involves attentive, prayerful, responsive agents.""",
        "chapter_overview": "Abraham sends his servant to find a wife for Isaac from his own kindred; the servant prays for a specific sign at the well; Rebekah fulfills the sign precisely before the prayer is finished; after consultation with her family, Rebekah consents to go; the servant brings her back and Isaac marries her, finding comfort after his mother's death.",
        "original_language_notes": [
            {"term": "חֶסֶד וֶאֱמֶת (chesed ve-emet)", "language": "Hebrew", "verse": 27, "words_used": ["chesed", "ve-emet"], "meaning": "'Steadfast love and faithfulness.' This paired phrase is one of the Old Testament's great covenant expressions (cf. Ps. 25:10; 85:10; John 1:14 — 'grace and truth' reflects the same pairing). The servant's worship when he finds Rebekah credits God's covenant fidelity: His love and truth are what guided the servant's steps."},
            {"term": "לְפָגְעִים (lefag'im)", "language": "Hebrew", "verse": 63, "words_used": ["lashu'ach"], "meaning": "The text says Isaac went out to 'meditate' (Hebrew: lashuach / siyach). The word suggests reflective musing, perhaps prayer or contemplation. The evening hour and the field setting give this meeting a sacred atmosphere: Isaac encounters his future wife while in a posture of prayerful reflection."},
            {"term": "נַעֲרָה (na'arah)", "language": "Hebrew", "verse": 16, "words_used": ["na'arah"], "meaning": "'Girl, young woman.' The term specifies Rebekah's age and social status. The emphasis on her being a virgin (betulah) alongside na'arah confirms her eligibility and the character of the match. The description emphasizes her suitability for the covenant role she will fill."},
            {"term": "לְכָה אִתָּנוּ (lechah ittanu)", "language": "Hebrew", "verse": 58, "words_used": ["lechah", "ittanu"], "meaning": "'Go with us.' The request for Rebekah's own consent is theologically significant in a patriarchal culture. Her one-word reply (elech — 'I will go') echoes the brevity and decisiveness of Abraham's own departure in 12:1–4. She leaves family and homeland, as Abraham did, following a summons from the God she is beginning to know."},
            {"term": "מֵהָאֱלֹהִים יָצָא הַדָּבָר (me-ha-Elohim yatza ha-davar)", "language": "Hebrew", "verse": 50, "words_used": ["me-ha-Elohim", "yatza", "ha-davar"], "meaning": "'The thing has come from God.' Bethuel and Laban's statement acknowledges that what has happened exceeds human arrangement — the precise fulfillment of the prayer sign compelled theological recognition even from a family that did not share Abraham's covenant."}
        ],
        "moral_lessons": [
            "Providence works through prayerful preparation and attentive action, not passive waiting — the servant prayed specifically and watched carefully.",
            "Specific prayer invites specific answers; vague petition produces vague discernment.",
            "Character revealed in small acts — Rebekah's generous service of water — is the true qualification for great covenant roles.",
            "Consenting with decisiveness to God's calling ('I will go') mirrors Abraham's own obedience and becomes its own form of faith.",
            "Gratitude and worship after receiving guidance reinforces the habit of noticing God's hand in daily events."
        ],
        "application": "Genesis 24 is a chapter for everyone navigating major decisions, relational transitions, or the question of 'where is God in this?' The servant's model is clear: bring the specific request to God in prayer, articulate a specific sign you are looking for, then watch attentively with expectation. When the sign comes, worship before you act further. Providence is not a vague sense that things will work out — it is the specific, careful guidance of a God who attends to camels and water jars and evening meditations. What specific prayer are you bringing to a specific well today?",
        "prayer": "LORD, God of our fathers, grant us success today. Show us your steadfast love and faithfulness in the specific paths we must walk. Give us the wisdom to ask clearly, the attention to see your answers, and the decisiveness to say 'I will go' when you make the way clear. Thank you that you guide our steps to the right wells and the right moments. In Jesus' name, Amen.",
        "key_points": [
            "Abraham swears his servant by the most solemn available oath, showing the gravity of the covenant marriage mission.",
            "Abraham expresses confidence that God's angel will go before the servant — faith grounded in covenant history.",
            "The servant's prayer is specific: a named sign of character (extraordinary generosity with water) to identify the right woman.",
            "Rebekah fulfills the sign precisely — and before the servant finishes praying — through enthusiastic, selfless service.",
            "The servant watches in silence to discern the LORD's answer, modeling attentive, prayerful observation.",
            "He worships immediately upon confirmation — 'Blessed be the LORD' — before even speaking to Rebekah's family.",
            "Rebekah's own consent is sought, and her one-word answer ('I will go') mirrors Abraham's decisive call-response.",
            "Isaac and Rebekah's meeting at evening, as he meditates in the field, is tender and suffused with a sacred quality."
        ],
        "study_questions": [
            "Why does Abraham make the servant swear this specific oath (hand under thigh)? What does the solemnity reveal about Abraham's view of covenant marriage?",
            "The servant's prayer requests a specific, observable sign of character rather than a miraculous vision. What does this model for how we bring specific requests to God?",
            "Rebekah's service of water is described in detail — running, emptying jars, drawing for all ten camels. What does this level of generous initiative reveal about the kind of character God was looking for?",
            "Why does the servant stand in silence watching while Rebekah draws water? What is the theology of attentive waiting for confirmation?",
            "Even Laban and Bethuel, who were not in Abraham's covenant, recognized 'the thing has come from the LORD' (v. 50). What does this reveal about the visibility of divine providence to those outside faith?",
            "Rebekah's 'I will go' echoes Abraham's going in Genesis 12. How does her decision to leave home for an unseen husband parallel the life of faith?"
        ],
        "tags": ["Rebekah", "Isaac", "providence", "prayer", "servant", "marriage", "guidance", "chesed", "sign", "faith"],
        "sources": []
    },
    {
        "book_id": 1,
        "book": "Genesis",
        "chapter": 25,
        "title": "Genesis 25 — Abraham's End, Ishmael's Line, and the Birth of Jacob and Esau",
        "summary": "Abraham dies at 175, buried at Machpelah by Isaac and Ishmael together. The descendants of Ishmael are listed. Rebekah conceives after Isaac's intercession; twins struggle in the womb; God prophecies that the older will serve the younger. Esau sells his birthright to Jacob for bread and lentil stew.",
        "content": """Genesis 25 closes one patriarchal story (Abraham's) and opens two more (Ishmael's lineage and Jacob-Esau's rivalry). It is a transitional chapter of great elegance — death, genealogy, birth, and prophetic oracle woven into a narrative about the passing of one generation's faith to the next.

Abraham takes another wife, Keturah (v. 1), producing six sons who become the ancestors of various Arabian peoples (vv. 2–4). The text is careful to note that Abraham gave all he had to Isaac (v. 5) while giving gifts to the sons of his concubines and sending them eastward, away from Isaac (v. 6). The covenant passes through one specific line; Abraham's other sons receive provision but not the promise.

Abraham lives 175 years and "breathed his last and died in a good old age, an old man and full of years, and was gathered to his people" (v. 8). The phrase "full of years" suggests a life lived to completion, not cut short. The most moving detail is who buries him: "Isaac and Ishmael his sons buried him in the cave of Machpelah" (v. 9). The two half-brothers, separated by a mother's rivalry and a divine directive (ch. 21), stand together at their father's grave. There is something profoundly human and healing in this moment.

After Abraham's death, God blesses Isaac (v. 11). The covenant blessing does not require Abraham's presence to continue — it is YHWH's to give and YHWH's to sustain. Isaac settles at Beer-lahai-roi (v. 11) — the well where God appeared to Hagar, the well of "the Living One who sees me." Isaac's choice of residence at this sacred site may indicate spiritual sensitivity to covenant history.

The genealogy of Ishmael (vv. 12–18) is handled with respect. His twelve princes (v. 16) fulfill God's specific promise in 17:20. Ishmael lives 137 years and is gathered to his people (v. 17). The Ishmaelites "settled from Havilah to Shur, which is opposite Egypt" — across the Sinai peninsula and into Arabia. The text notes they "settled over against all his kinsmen" (v. 18), fulfilling the prophecy of 16:12. Ishmael's line is honorably remembered even as the narrative moves forward without them.

The story of Jacob and Esau begins with a problem now familiar in Genesis: Rebekah is barren (v. 21). Isaac "prayed to the LORD for his wife because she was barren, and the LORD granted his prayer and Rebekah his wife conceived" (v. 21). Isaac's intercessory prayer for Rebekah is the seed of the covenant's next generation. Prayer, not human strategy, opens the womb.

The pregnancy is immediately turbulent: the children struggle together within her (v. 22), and Rebekah's anguished question — "If it is thus, why is this happening to me?" — is answered by direct divine oracle (v. 23):

"Two nations are in your womb,
and two peoples from within you shall be divided;
the one shall be stronger than the other,
the older shall serve the younger."

This oracle (vv. 23) overturns ancient expectation. The firstborn inheritance the elder — this is universal cultural law. But God announces before birth that the covenant line will run through the younger. This is a sovereign election that is entirely unearned and unanticipated. Paul cites this passage in Romans 9:10–12 to demonstrate that God's election is not based on human works or merit but on the call of God who purposes before birth.

The twins emerge: Esau first (red and hairy; the name "Esau" may relate to Hebrew words for "rough/hairy"; Seir and Edom later identify his descendants by the red color). Jacob comes second, holding Esau's heel — giving rise to his name Ya'akov (heel-grabber, or one who supplants/follows at the heel). The brothers' natures diverge: Esau is a skilled hunter, a man of the field, Isaac's favorite; Jacob is quiet, dwelling in tents (possibly a shepherd), Rebekah's favorite.

The birthright episode (vv. 29–34) is both comic and tragic. Esau comes in from the field famished and smells the red lentil stew Jacob is cooking. He demands it: "Let me eat some of that red stuff, for I am exhausted" (v. 30). Jacob responds with an entrepreneur's eye for opportunity: "Sell me your birthright now" (v. 31). Esau's reasoning is devastating in its short-sightedness: "I am about to die; of what use is a birthright to me?" (v. 32). He sells his future for a present meal.

The narrator's theological verdict is sharp: "Thus Esau despised his birthright" (v. 34). The birthright carried covenant privileges — double inheritance, priestly family leadership, and above all, the specific line through which God's covenant would run. Esau traded the eternal for the immediate; the spiritual for the physical; the future for the moment. The New Testament draws on this episode directly: "See to it that no one fails to obtain the grace of God... that no one is sexually immoral or unholy like Esau, who sold his birthright for a single meal" (Heb. 12:15–16).""",
        "chapter_overview": "Abraham dies at 175 and is buried at Machpelah by Isaac and Ishmael together; God blesses Isaac who settles at Beer-lahai-roi; Ishmael's twelve sons are listed; Rebekah, barren, conceives after Isaac's prayer; God's oracle reveals the older will serve the younger; Esau and Jacob are born; Esau sells his birthright for lentil stew.",
        "original_language_notes": [
            {"term": "וַיִּגְוַע וַיָּמָת (va-yigva va-yamot)", "language": "Hebrew", "verse": 8, "words_used": ["va-yigva", "va-yamot"], "meaning": "'He breathed his last and died.' Gava specifically describes the final exhalation of breath — giving up the spirit. The phrase 'gathered to his people' (ne'esaf el amav) that follows indicates a belief in continuing existence after death, rejoining those who have died before. This is one of the Old Testament's earliest expressions of afterlife expectation."},
            {"term": "יִתְרוֹצְצוּ (yitrotzatzu)", "language": "Hebrew", "verse": 22, "words_used": ["yitrotzatzu"], "meaning": "'They struggled/crushed one another.' From ratzatz (to crush, oppress). The intensive reflexive form suggests violent, repeated struggling. The word is strong — this was not gentle movement but a violent contest even in the womb, foreshadowing the brothers' conflict throughout their lives."},
            {"term": "רַב יַעֲבֹד צָעִיר (rav ya'avod tza'ir)", "language": "Hebrew", "verse": 23, "words_used": ["rav", "ya'avod", "tza'ir"], "meaning": "'The elder shall serve the younger.' The divine oracle reverses natural order. Paul reads this in Romans 9 as an example of divine election: 'though they were not yet born and had done nothing either good or bad... not because of works but because of him who calls.' The oracle establishes God's sovereign freedom in covenant election."},
            {"term": "יַעֲקֹב (Ya'akov)", "language": "Hebrew", "verse": 26, "words_used": ["Ya'akov"], "meaning": "'He takes by the heel' or 'he supplants.' From akev (heel). The name captures the birth event (grasping Esau's heel) and anticipates Jacob's character as one who supplants and outmaneuvers. God will later rename him Israel — one who strives with God — transforming the meaning of his identity."},
            {"term": "וַיִּבֶז עֵשָׂו אֶת הַבְּכֹרָה (va-yivez Esav et ha-bechorah)", "language": "Hebrew", "verse": 34, "words_used": ["va-yivez", "Esav", "et", "ha-bechorah"], "meaning": "'And Esau despised his birthright.' Bazah means to treat as contemptible, to hold in contempt. This is not merely casual disregard — it is active contempt for what is sacred. The narrator's theological verdict is clear and final: Esau saw the birthright and considered it worthless."}
        ],
        "moral_lessons": [
            "Covenant blessing passes faithfully from one generation to the next, sustained not by human presence but by God's ongoing faithfulness.",
            "Isaac and Ishmael's joint burial of Abraham pictures that even divided families can be reunited in honoring the dead — and in God's mercy.",
            "Prayer is the proper response to barrenness and blocked promises; Isaac's intercession opens Rebekah's womb.",
            "God's sovereign election overturns human assumptions — the younger serves, the unexpected is chosen, the improbable is promised.",
            "Trading long-term covenant privilege for short-term relief is the pattern of spiritual loss; every generation faces its own version of Esau's lentil stew."
        ],
        "application": "Genesis 25 presents two sharply contrasted postures toward the covenant: Isaac who intercedes and waits (twenty years of barrenness before the twins are born, v. 26), and Esau who despises and trades away what he cannot see for what he can eat. The question for every reader is: which posture is mine? Where am I trading the eternal for the immediate? Where do I need to pray persistently over a twenty-year barrenness rather than engineer a short-term solution? And do I value what God has placed in my hands — the covenant privileges of relationship with Him, His Word, His community — or do I treat them as things I can exchange when hungry?",
        "prayer": "Father, keep us from Esau's despising and Jacob's grasping. Give us Isaac's patience and interceding faith. Help us to hold the birthright — the covenant privileges of knowing you, walking with you, bearing your name — as the supreme treasure that cannot be traded for any present comfort. And teach us to trust your sovereign purposes, even when they overturn our expectations of who you will use and how. In Jesus' name, Amen.",
        "key_points": [
            "Abraham dies at 175 'full of years' — a life lived to completion; Isaac and Ishmael bury him together at Machpelah.",
            "Ishmael's twelve sons fulfill God's specific promise, and he is listed with dignity before the narrative moves to Isaac.",
            "God blesses Isaac and the covenant continues beyond Abraham — sustained by God, not by Abraham's presence.",
            "Rebekah is barren; Isaac intercedes for twenty years; prayer opens the womb, not strategy.",
            "The twins' struggling in the womb prompts Rebekah's anguished question and God's oracle: 'the older shall serve the younger.'",
            "The oracle is unconditional and sovereign — before birth, before deeds — establishing God's freedom in election.",
            "Esau and Jacob's contrasting natures foreshadow the conflict of the nations they will father.",
            "Esau sells his birthright for lentil stew, and the narrator's verdict is 'he despised his birthright' — a pattern Hebrews warns all believers to avoid."
        ],
        "study_questions": [
            "Isaac and Ishmael bury Abraham together. What does this moment of unity among divided brothers suggest about grief, family, and God's grace?",
            "Isaac prays for Rebekah for twenty years before the twins are born (compare v. 20 and v. 26). What does persisting in prayer for twenty years teach us about intercessory faith?",
            "God's oracle ('the elder shall serve the younger') comes before birth and before any deeds. How does Paul's use of this in Romans 9 shape our understanding of divine election?",
            "Jacob is described as quiet, dwelling in tents — and yet the oracle already favored him before his character was known. What does this suggest about how God chooses?",
            "What specific covenant privileges did the 'birthright' include? Why was Esau's trade so catastrophically foolish?",
            "What is your equivalent of 'lentil stew' — the present comfort that tempts you to undervalue your spiritual inheritance? How do you guard against Esau's contempt?"
        ],
        "tags": ["Abraham's death", "Ishmael", "Jacob", "Esau", "birthright", "election", "prayer", "barrenness", "covenant", "Isaac"],
        "sources": []
    }
]

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
    content = row[1] or ""
    return len(content) >= 200

def insert_entry(conn, chap_data, batch_uuid):
    cur = conn.cursor()
    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"
    entry_uuid = str(uuid.uuid4())
    key_points_json = json.dumps(chap_data["key_points"])
    study_questions_json = json.dumps(chap_data["study_questions"])
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
    forbidden = {"is_ai_generated", "model_name", "prompt_version"}
    assert not (forbidden & set(payload.keys())), f"Forbidden key: {forbidden & set(payload.keys())}"
    json_path = folder / f"{chapter:02d}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    with open(json_path, "r", encoding="utf-8") as f:
        parsed = json.load(f)
    assert not (forbidden & set(parsed.keys())), "Forbidden key in parsed JSON"
    return str(json_path)

def update_progress(conn, last_book_id, last_book, last_chapter):
    book_chapters = {1: ("Genesis", 50), 2: ("Exodus", 40)}
    next_book_id = last_book_id
    next_chapter = last_chapter + 1
    if next_book_id in book_chapters and next_chapter > book_chapters[next_book_id][1]:
        next_book_id += 1
        next_chapter = 1
    next_book = book_chapters.get(next_book_id, ("Unknown", 0))[0]
    completed = (last_book_id >= 66)
    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"
    cur = conn.cursor()
    cur.execute("""
        UPDATE commentary_generation_progress
        SET current_book_id=?, current_chapter=?,
            last_completed_book_id=?, last_completed_chapter=?,
            updated_at=?
        WHERE id=1
    """, (next_book_id, next_chapter, last_book_id, last_chapter, now))
    conn.commit()
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
            print(f"SKIP: {ref} already exists")
            chapters_skipped += 1
        else:
            print(f"GENERATING: {ref} — {chap['title']}")
            entry_uuid, created_at = insert_entry(conn, chap, BATCH_UUID)
            json_path = write_json_backup(chap, entry_uuid, created_at)
            chapters_generated += 1
            db_rows_inserted += 1
            files_written.append(json_path)
            print(f"  -> inserted UUID={entry_uuid[:8]}..., JSON: {json_path}")
        end_ref = ref
        last_book_id = book_id
        last_book = book
        last_chapter = chapter

    next_book_id, next_book, next_chapter = update_progress(conn, last_book_id, last_book, last_chapter)
    conn.close()
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
