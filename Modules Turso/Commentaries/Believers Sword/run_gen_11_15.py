"""Generate Genesis 11-15 commentaries and insert into DB + write JSON backups."""
import sqlite3, json, os, uuid, datetime, pathlib

WORKSPACE = pathlib.Path(__file__).parent
DB_PATH = WORKSPACE / "believers_sword_commentaries.db"
GENERATED_DIR = WORKSPACE / "generated"
PROGRESS_JSON = WORKSPACE / "commentary_generation_progress.json"
LOG_JSONL = WORKSPACE / "commentary_generation_log.jsonl"

BATCH_UUID = str(uuid.uuid4())
NOW = datetime.datetime.utcnow().isoformat() + "Z"

# ── Commentary data ────────────────────────────────────────────────────────────

COMMENTARIES = [
    {
        "book_id": 1,
        "book": "Genesis",
        "chapter": 11,
        "title": "Genesis 11 — Babel, Pride, and the Scattering of Nations",
        "summary": (
            "Genesis 11 records humanity's united attempt to build a tower to the heavens "
            "and make a name for itself—a direct defiance of God's command to fill the earth. "
            "God responds by confusing their language and scattering them, turning human pride "
            "into the very diversity He intended. The chapter ends with the genealogy leading to Abram."
        ),
        "chapter_overview": (
            "Chapter 11 opens with a unified humanity speaking one language and settling in Shinar. "
            "Their project—a city and tower reaching heaven—was driven not by wonder but by pride and "
            "fear: 'lest we be scattered.' God descends, observes, and acts by confusing their speech, "
            "dispersing them across the earth. The second half provides the genealogy from Shem to Abram, "
            "a bridge to God's next great act of redemptive grace."
        ),
        "content": (
            "## What Genesis 11 Is About\n"
            "Genesis 11 captures the climax of early human rebellion: a global civilization that turned "
            "its collective energy toward self-glory rather than God's glory. The tower project was not "
            "merely architectural ambition—it was a theological statement: 'We will make a name for "
            "ourselves.' God's response was judgment and mercy simultaneously. Scattering was the "
            "consequence of pride, but it was also the fulfillment of God's original design for humanity "
            "to fill the earth.\n\n"
            "## Theological Themes\n"
            "- Human unity apart from God becomes a platform for collective sin\n"
            "- God sees every human project; nothing is hidden from Him\n"
            "- Babel is the anti-Eden: where Eden was about human vocation under God, "
            "Babel is about human autonomy without God\n"
            "- The scattering is judgment, but also sets the stage for Genesis 12's call of Abram, "
            "through whom all scattered nations will be blessed\n\n"
            "## Hebrew Word Notes\n"
            "- Bābel (בָּבֶל, Genesis 11:9): derived from bālal (בָּלַל), 'to confuse'; the name memorializes "
            "divine judgment on human pride.\n"
            "- šēm (שֵׁם, Genesis 11:4): 'name'; the builders wanted to make a šēm for themselves—a direct "
            "contrast with God's promise to make Abram's šēm great (Gen 12:2).\n"
            "- pûṣ (פּוּץ, Genesis 11:8-9): 'to scatter/disperse'; the very thing they feared became their "
            "judgment.\n\n"
            "## What We Can Learn\n"
            "- Collective pride is as dangerous as individual pride; communities can sin together.\n"
            "- The desire to 'make a name' is a warning sign whenever it replaces seeking God's name.\n"
            "- God's judgments often accomplish His purposes through human failure—Babel's scattering "
            "filled the earth as God commanded.\n\n"
            "## How This Chapter Points to Christ\n"
            "Babel is reversed at Pentecost. Where Babel produced confusion of languages as judgment, "
            "the Holy Spirit at Pentecost enabled every person to hear God's word in their own tongue "
            "as redemption. Christ gathers what Babel scattered. The tower builders sought a name; "
            "God has given Jesus the name above every name.\n\n"
            "## Believers Sword Reflection\n"
            "Genesis 11 warns the church that unity is only holy when it is unity under God's word and "
            "purpose. Any project—personal or communal—built on self-glory will be undone. True greatness "
            "comes from bearing God's name, not building our own."
        ),
        "moral_lessons": [
            "Collective ambition divorced from God leads to division, not unity.",
            "The desire for self-made greatness is a subtle but serious form of idolatry.",
            "God's judgments are never the end of the story; they set the stage for grace.",
            "What humanity fears most (scattering, obscurity) becomes what God uses most.",
        ],
        "application": (
            "Examine the projects and pursuits in your life. Are they building your name or God's? "
            "Submit your ambitions to God's purposes, and trust that He will make your life significant "
            "in ways that matter eternally. Seek to be part of what God is gathering rather than "
            "what pride builds."
        ),
        "prayer": (
            "Lord, expose every tower of pride in my heart. Teach me to seek Your name above my own, "
            "and to find my significance in belonging to You. May my life contribute to Your gathering "
            "of all peoples, not to my own monument. Amen."
        ),
        "key_points": [
            "Human unity outside of God's purposes produces collective sin.",
            "The tower builders feared scattering—the very thing that became their judgment.",
            "Babel (confusion) becomes the backdrop for Abraham's call to bless all nations.",
            "Babel is reversed at Pentecost: confusion becomes proclamation in every language.",
            "God descends to observe human works—He is never distant or unaware.",
        ],
        "study_questions": [
            "What was the real motivation behind building the tower, and what does it reveal about human nature?",
            "How does the word šēm ('name') connect Genesis 11 to Genesis 12?",
            "In what ways does Pentecost reverse the judgment of Babel?",
            "What personal or collective 'towers' might you be building for your own name rather than God's?",
        ],
        "original_language_notes": [
            {"term": "Bābel", "language": "Hebrew", "verse": "Genesis 11:9",
             "words_used": "בָּבֶל (Bābel)", "meaning": "Confusion or gateway of God; from bālal (to confuse); memorializes divine judgment on human pride at Shinar."},
            {"term": "šēm", "language": "Hebrew", "verse": "Genesis 11:4",
             "words_used": "שֵׁם (šēm)", "meaning": "Name, reputation, renown; the builders wanted to make a name for themselves—contrasted with God's promise to make Abram's name great."},
            {"term": "pûṣ", "language": "Hebrew", "verse": "Genesis 11:8-9",
             "words_used": "פּוּץ (pûṣ)", "meaning": "To scatter, disperse; God used the very thing they feared to fulfill His creational mandate that humanity fill the earth."},
            {"term": "bālal", "language": "Hebrew", "verse": "Genesis 11:7",
             "words_used": "בָּלַל (bālal)", "meaning": "To mix, confuse; God confused (bālal) their language, giving Babel its name and its lesson."},
        ],
        "tags": ["pride", "judgment", "nations", "language", "Babel", "Pentecost foreshadow", "Genesis"],
        "sources": ["Genesis 11:1-32", "Acts 2:1-11", "Philippians 2:9-11"],
    },
    {
        "book_id": 1,
        "book": "Genesis",
        "chapter": 12,
        "title": "Genesis 12 — The Call of Abram and the God Who Blesses",
        "summary": (
            "Genesis 12 is one of the most pivotal chapters in Scripture: God calls Abram from Ur, "
            "promises to make him a great nation, give him land, and bless all families of the earth "
            "through him. Abram obeys in faith. The chapter also shows his failure in Egypt, reminding "
            "readers that even heroes of faith are broken people who need God's grace."
        ),
        "chapter_overview": (
            "The chapter opens with God's sovereign, unconditional call to Abram: 'Go from your country.' "
            "The seven-fold blessing promises—a great nation, a great name, blessing to others, "
            "and cursing to those who curse him—frame the entire rest of Scripture. Abram obeys. "
            "He passes through Canaan, builds altars, and worships. But famine drives him to Egypt, "
            "where fear leads him to deceive Pharaoh about Sarai. God still protects and redeems, "
            "even in Abram's failure."
        ),
        "content": (
            "## What Genesis 12 Is About\n"
            "After Babel's judgment, God does not give up on humanity—He chooses one man through whom "
            "to reverse the curse and restore blessing to all peoples. The call of Abram is the beginning "
            "of God's redemptive plan. This chapter shows both the greatness of God's grace (an "
            "unconditional covenant) and the weakness of human faith (Abram lies in Egypt).\n\n"
            "## Theological Themes\n"
            "- Election: God chooses whom He will, not on merit but by grace\n"
            "- Covenant: the Abrahamic promise is unilateral and unconditional—God makes it\n"
            "- Mission: the call is not just for Abram's benefit—'all families of the earth' are in view\n"
            "- Failure and grace: Abram's deception in Egypt does not cancel the covenant\n\n"
            "## Hebrew Word Notes\n"
            "- bārak (בָּרַך, Genesis 12:2-3): 'to bless'; used five times in vv. 2-3, emphasizing that "
            "blessing is the dominant theme of the Abrahamic covenant.\n"
            "- gôy (גּוֹי, Genesis 12:2): 'nation, people group'; God will make Abram into a great gôy—"
            "startling since Abram had no children.\n"
            "- lēk-lěkā (לֶךְ-לְךָ, Genesis 12:1): 'go for yourself / go forth'; a strong personal "
            "command—this is a call that costs Abram everything familiar.\n\n"
            "## What We Can Learn\n"
            "- Obedient faith moves even when the destination is unknown.\n"
            "- God's purposes are bigger than one person or one nation—all families of the earth matter.\n"
            "- Failure does not disqualify us from God's plan; grace covers and restores.\n"
            "- Worship (building altars) should mark our journey through life's stages.\n\n"
            "## How This Chapter Points to Christ\n"
            "The Abrahamic blessing finds its ultimate fulfillment in Jesus Christ. Galatians 3:16 "
            "identifies the 'offspring' of Abraham as Christ. Through Him, every barrier Babel created "
            "is overcome, and all nations receive blessing. Abram's altar-worship foreshadows the "
            "worship Christ makes possible for all peoples.\n\n"
            "## Believers Sword Reflection\n"
            "Genesis 12 calls every believer to understand their life within God's redemptive story. "
            "You are not called merely to personal blessing but to be a conduit of blessing to others. "
            "The question is not only 'What is God doing for me?' but 'How am I blessing the families "
            "around me?'"
        ),
        "moral_lessons": [
            "Faith means obeying God's call even when the destination is not fully known.",
            "God's purposes are always larger than the individual—they encompass all nations.",
            "Worship (altars) should be built at every stage of the journey of faith.",
            "Fear-driven deception grieves God and harms others; trust in God's protection instead.",
        ],
        "application": (
            "Consider what God is calling you to leave behind in order to follow Him. Are you "
            "worshipping at each stage of your journey, or only when comfortable? Look for ways "
            "to be a blessing to the people God has placed around you—your family, community, "
            "and those from different backgrounds."
        ),
        "prayer": (
            "Faithful God, give me the courage of Abram to leave what is familiar and follow Your call. "
            "Make me a person through whom Your blessing flows to others. Forgive me for the times I "
            "choose fear over faith, and restore me by Your grace. Amen."
        ),
        "key_points": [
            "God's call to Abram is unconditional—it rests on God's purpose, not Abram's merit.",
            "The seven-fold blessing is God's answer to the curse that sin brought into the world.",
            "All families of the earth are the ultimate scope of God's redemptive plan.",
            "Abram's altar-building marks a life of worship amidst the journey.",
            "Abram's failure in Egypt does not nullify the covenant—grace covers human weakness.",
        ],
        "study_questions": [
            "What does God's unconditional call to Abram reveal about how God operates in redemption?",
            "How does the phrase 'all families of the earth will be blessed' shape your understanding of mission?",
            "What fears tempted Abram in Egypt, and what fears tempt you to compromise?",
            "How does Galatians 3:16 connect the Abrahamic promise to Jesus Christ?",
        ],
        "original_language_notes": [
            {"term": "lēk-lěkā", "language": "Hebrew", "verse": "Genesis 12:1",
             "words_used": "לֶךְ-לְךָ (lēk-lěkā)", "meaning": "Go for yourself / go forth; an emphatic personal command to leave country, kindred, and father's house—the call costs Abram everything familiar."},
            {"term": "bārak", "language": "Hebrew", "verse": "Genesis 12:2-3",
             "words_used": "בָּרַך (bārak)", "meaning": "To bless; used five times in two verses, making blessing the dominant note of the Abrahamic covenant and God's answer to the curse of sin."},
            {"term": "gôy", "language": "Hebrew", "verse": "Genesis 12:2",
             "words_used": "גּוֹי (gôy)", "meaning": "Nation, people group; God promises to make the childless Abram into a great nation—a staggering promise of divine power over impossibility."},
            {"term": "šēm", "language": "Hebrew", "verse": "Genesis 12:2",
             "words_used": "שֵׁם (šēm)", "meaning": "Name; God will make Abram's name great—what the Babel builders sought by their own effort, God freely gives to those who walk with Him."},
        ],
        "tags": ["faith", "call", "covenant", "Abraham", "blessing", "mission", "nations", "Genesis"],
        "sources": ["Genesis 12:1-20", "Galatians 3:8-16", "Hebrews 11:8-10"],
    },
    {
        "book_id": 1,
        "book": "Genesis",
        "chapter": 13,
        "title": "Genesis 13 — Generosity, Separation, and the Promise Renewed",
        "summary": (
            "Genesis 13 follows Abram's return from Egypt. Conflict arises between Abram's and Lot's "
            "herdsmen over land. Abram, trusting God's provision, generously gives Lot the first choice "
            "of land. Lot chooses the well-watered Jordan plain (near Sodom). God then reaffirms the "
            "covenant to Abram, promising all the land he can see in every direction."
        ),
        "chapter_overview": (
            "After the Egypt episode, Abram and Lot return to Canaan wealthy in livestock and silver. "
            "The abundance that God gave creates tension—the land cannot support both their flocks. "
            "Abram's response is remarkable: he defers to Lot, offering him first choice of the land. "
            "Lot's choice is driven by sight—the Jordan plain looks like Eden, like Egypt. "
            "But it is near Sodom. After Lot departs, God speaks to Abram again, enlarging the promise. "
            "Abram builds another altar, marking renewed worship."
        ),
        "content": (
            "## What Genesis 13 Is About\n"
            "Genesis 13 is a study in contrasts: Abram's faith-driven generosity versus Lot's "
            "sight-driven self-interest. Abram does not grasp; he entrusts the future to God. "
            "Lot chooses what looks good but moves closer to Sodom. The chapter ends with God expanding "
            "the covenant—Abram's trust is met with renewed promise.\n\n"
            "## Theological Themes\n"
            "- Generosity as an expression of faith: Abram can give because he trusts God to provide\n"
            "- The danger of choosing by sight alone: Lot saw 'like the garden of God'\n"
            "- God's faithfulness: the covenant is reaffirmed after a season of failure (Egypt)\n"
            "- Worship as a pattern: Abram builds another altar after receiving God's word\n\n"
            "## Hebrew Word Notes\n"
            "- rîb (רִיב, Genesis 13:7): 'strife, contention, lawsuit'; the conflict between herdsmen "
            "hints at the danger of wealth pulling people apart when God is not first.\n"
            "- nāśāʾ ʿênayim (נָשָׂא עֵינַיִם, Genesis 13:10): 'lift up the eyes'; Lot lifted his eyes "
            "and chose by what he saw—a choice made with human perception, not faith.\n"
            "- ʿōlām (עוֹלָם, Genesis 13:15): 'forever, eternity'; God promises the land to Abram "
            "and his offspring forever, grounding the covenant in divine permanence.\n\n"
            "## What We Can Learn\n"
            "- Trust in God frees us from the need to grasp what is ours; generosity flows from security in God.\n"
            "- Decisions driven by appearance and comfort often lead us toward moral danger.\n"
            "- God reaffirms His promises to faithful people; setbacks do not cancel His covenant.\n"
            "- Regular worship (altar-building) keeps us oriented toward God between major life events.\n\n"
            "## How This Chapter Points to Christ\n"
            "Abram's willingness to give up what was rightfully his foreshadows Christ, who did not "
            "grasp equality with God but humbled Himself for others' benefit (Philippians 2:6-7). "
            "The promise of the land 'to you and to your offspring forever' finds its ultimate "
            "fulfillment in the new creation, the inheritance of all who are in Christ.\n\n"
            "## Believers Sword Reflection\n"
            "Genesis 13 teaches that the person of faith does not need to fight for first place. "
            "When God is our portion, we can afford to be generous, to defer, to let others choose "
            "first—because our inheritance is secured by God's covenant, not our own maneuvering."
        ),
        "moral_lessons": [
            "Generosity is the fruit of genuine trust in God's provision.",
            "Choices made purely on the basis of outward appearance risk moving us toward moral danger.",
            "God's faithfulness to His covenant is not diminished by our failures or by conflict.",
            "Worship should be a regular practice, not only reserved for great moments.",
        ],
        "application": (
            "Where in your life are you grasping rather than trusting? Practice generosity this week—"
            "not because you have extra, but because you trust God is your Provider. Examine a major "
            "decision: are you choosing by what looks good, or by what God has said?"
        ),
        "prayer": (
            "Lord of all provision, loosen my grip on the things I fear to lose. Give me Abram's "
            "generosity that comes from trusting You completely. Guard me from choices driven by "
            "appearance rather than faith. Renew Your promises to my heart today. Amen."
        ),
        "key_points": [
            "Abram's generosity flows from faith—he trusts God to provide without grasping for the best.",
            "Lot chooses by sight, selecting proximity to Sodom's wealth and wickedness.",
            "God reaffirms the covenant after conflict and failure—He does not abandon His faithful.",
            "The promise is expanded: all the land in every direction, forever, to Abram and his offspring.",
            "Altar-building marks Abram's life as one of continual worship and renewal.",
        ],
        "study_questions": [
            "How does Abram's generosity in this chapter reflect his trust in God's promises?",
            "What dangers are revealed in Lot's choice to settle near Sodom?",
            "What does the phrase 'lifted up his eyes' suggest about the nature of Lot's decision-making?",
            "How does Philippians 2:6-7 illuminate Abram's posture of not grasping in this chapter?",
        ],
        "original_language_notes": [
            {"term": "rîb", "language": "Hebrew", "verse": "Genesis 13:7",
             "words_used": "רִיב (rîb)", "meaning": "Strife, contention; the conflict between herdsmen signals how abundance without godly wisdom produces division rather than community."},
            {"term": "nāśāʾ ʿênayim", "language": "Hebrew", "verse": "Genesis 13:10",
             "words_used": "נָשָׂא עֵינַיִם (nāśāʾ ʿênayim)", "meaning": "To lift up the eyes; Lot looked and chose based on what he saw—a visual, human-centered assessment rather than faith-based discernment."},
            {"term": "ʿōlām", "language": "Hebrew", "verse": "Genesis 13:15",
             "words_used": "עוֹלָם (ʿōlām)", "meaning": "Forever, eternity; God's land grant to Abram is permanent, grounding the covenant in divine permanence that no human choice can annul."},
            {"term": "qûm", "language": "Hebrew", "verse": "Genesis 13:17",
             "words_used": "קוּם (qûm)", "meaning": "Arise, walk through; God commands Abram to walk through the land in every direction as an act of faith-possession before legal ownership."},
        ],
        "tags": ["generosity", "faith", "covenant", "Abraham", "Lot", "choices", "worship", "Genesis"],
        "sources": ["Genesis 13:1-18", "Philippians 2:6-8", "Hebrews 11:9-10"],
    },
    {
        "book_id": 1,
        "book": "Genesis",
        "chapter": 14,
        "title": "Genesis 14 — War, Rescue, and the Priest-King Melchizedek",
        "summary": (
            "Genesis 14 records a regional war of kings in which Lot is taken captive. Abram responds "
            "with courage, marshaling his men to rescue Lot. After victory, Abram meets two kings: "
            "Melchizedek of Salem, who blesses him and receives tithes, and the king of Sodom, whose "
            "offer of spoils Abram refuses. The chapter reveals Abram as a man of valor, generosity, "
            "and unwavering loyalty to God Most High."
        ),
        "chapter_overview": (
            "A coalition of four kings defeats five kings, plundering Sodom and Gomorrah and capturing Lot. "
            "When Abram hears, he arms 318 trained men and pursues—winning against overwhelming odds. "
            "On return, he is met by Melchizedek, king of Salem (peace) and priest of God Most High, "
            "who brings bread and wine and pronounces blessing. Abram gives him a tithe. Then the king "
            "of Sodom offers Abram the plunder, but Abram refuses, unwilling to let any man claim credit "
            "for his wealth."
        ),
        "content": (
            "## What Genesis 14 Is About\n"
            "Genesis 14 shows Abram as a man of courageous action who rescues the vulnerable and "
            "refuses to compromise his testimony. The heart of the chapter is the encounter with "
            "Melchizedek—a mysterious priest-king who prefigures Christ's eternal priesthood. "
            "Abram's tithe to Melchizedek and his refusal of Sodom's offer together reveal a man "
            "whose security is entirely in God.\n\n"
            "## Theological Themes\n"
            "- Abram as protector of the vulnerable—love for Lot that transcends their separation\n"
            "- Melchizedek as a type of Christ: priest and king, offering bread and wine, blessing\n"
            "- The tithe as an act of worship acknowledging God's ownership of all\n"
            "- Integrity: refusing to let the world claim credit for what God provides\n\n"
            "## Hebrew Word Notes\n"
            "- Malkî-ṣedeq (מַלְכִּי-צֶדֶק, Genesis 14:18): 'my king is righteousness'; "
            "a name that becomes a title for Christ in Psalm 110:4 and Hebrews 7.\n"
            "- kōhēn (כֹּהֵן, Genesis 14:18): 'priest'; Melchizedek is the first person in Scripture "
            "called a priest, and he serves El ʿElyôn, God Most High.\n"
            "- El ʿElyôn (אֵל עֶלְיוֹן, Genesis 14:18-19): 'God Most High'; the name Abram also uses "
            "in v. 22, identifying YHWH with the God Melchizedek serves.\n\n"
            "## What We Can Learn\n"
            "- Courage to rescue others is a fruit of covenant relationship with God.\n"
            "- Worship and generosity (tithing) should mark victory, not just difficulty.\n"
            "- Integrity sometimes means refusing gifts the world offers so God alone gets the glory.\n"
            "- God raises up unexpected figures—like Melchizedek—to bless and instruct us.\n\n"
            "## How This Chapter Points to Christ\n"
            "Psalm 110:4 declares the Messiah to be 'a priest forever after the order of Melchizedek.' "
            "Hebrews 7 develops this extensively: Jesus is the ultimate Melchizedek, whose priesthood "
            "is eternal, whose name means righteousness and peace, who offered Himself as the true "
            "bread and wine, and through whom believers are blessed. Abram's tithe to Melchizedek "
            "becomes a statement about the supremacy of Christ's priesthood over the Levitical.\n\n"
            "## Believers Sword Reflection\n"
            "Genesis 14 challenges believers to be courageous on behalf of others, to worship in "
            "victory as well as in trial, and to refuse the world's credit for what God has done. "
            "When Melchizedek appears in our lives—unexpected blessing and affirmation from God's "
            "servants—receive it with gratitude and respond with generosity."
        ),
        "moral_lessons": [
            "Loyalty and courage to rescue others flow from a heart rooted in covenant love.",
            "Victory is an occasion for worship and generosity, not self-congratulation.",
            "Refusing the world's offer to take credit for God's blessing protects our testimony.",
            "God can use unexpected people and encounters to bless and affirm our faith.",
        ],
        "application": (
            "Is there someone in your life who needs you to act courageously on their behalf? "
            "Practice tithing and giving as an act of worship, especially after seasons of blessing. "
            "Examine whether you accept offers that would tie you to the world's system in ways "
            "that compromise your witness for God."
        ),
        "prayer": (
            "God Most High, possessor of heaven and earth, give me courage to fight for those who "
            "need rescue. Make me a giver in seasons of abundance, and guard my integrity so that "
            "no one but You gets the credit for my life's blessings. Thank You for the eternal "
            "High Priest, Jesus, who blesses me with righteousness and peace. Amen."
        ),
        "key_points": [
            "Abram's rescue of Lot demonstrates that covenant love does not end with separation.",
            "Melchizedek is the first priest in Scripture—a type of Christ's eternal priesthood.",
            "Abram's tithe acknowledges that victory and wealth come from God, not human power.",
            "Abram refuses Sodom's offer so God alone will be credited with his prosperity.",
            "Jesus is the ultimate Melchizedek: king of righteousness and peace, eternal priest.",
        ],
        "study_questions": [
            "What does Abram's response to Lot's capture reveal about his character and values?",
            "What is the significance of Melchizedek bringing out bread and wine?",
            "Why does Abram refuse the king of Sodom's offer, and what principle does this establish?",
            "How does Hebrews 7 use this chapter to argue for the supremacy of Christ's priesthood?",
        ],
        "original_language_notes": [
            {"term": "Malkî-ṣedeq", "language": "Hebrew", "verse": "Genesis 14:18",
             "words_used": "מַלְכִּי-צֶדֶק (Malkî-ṣedeq)", "meaning": "My king is righteousness; a name pointing to the righteousness of God's rule, fulfilled in Christ whom Psalm 110:4 identifies as a priest in this order."},
            {"term": "kōhēn", "language": "Hebrew", "verse": "Genesis 14:18",
             "words_used": "כֹּהֵן (kōhēn)", "meaning": "Priest; the first use of this title in Scripture, applied to Melchizedek who serves El ʿElyôn—God Most High."},
            {"term": "El ʿElyôn", "language": "Hebrew", "verse": "Genesis 14:18-19",
             "words_used": "אֵל עֶלְיוֹן (El ʿElyôn)", "meaning": "God Most High; the divine title Melchizedek uses in blessing Abram, which Abram then uses in v. 22 when refusing Sodom's king—equating YHWH with the Most High God."},
            {"term": "maʿăśēr", "language": "Hebrew", "verse": "Genesis 14:20",
             "words_used": "מַעֲשֵׂר (maʿăśēr)", "meaning": "Tithe, tenth; Abram gave Melchizedek a tenth of everything—the first tithe in Scripture, an act of worship acknowledging God's ownership of all."},
        ],
        "tags": ["courage", "rescue", "Melchizedek", "priesthood", "tithe", "integrity", "Abraham", "Genesis"],
        "sources": ["Genesis 14:1-24", "Psalm 110:4", "Hebrews 7:1-28"],
    },
    {
        "book_id": 1,
        "book": "Genesis",
        "chapter": 15,
        "title": "Genesis 15 — Faith Counted as Righteousness and the Covenant Confirmed",
        "summary": (
            "Genesis 15 is the theological heart of the Abrahamic narrative. God appears to Abram in "
            "a vision, promising him a son and descendants as numerous as the stars. Abram believes God, "
            "and God credits it to him as righteousness. The chapter climaxes in a formal covenant "
            "ceremony, with God alone passing through the sacrifice pieces—making the covenant "
            "unconditional and sealed by divine oath."
        ),
        "chapter_overview": (
            "God reassures Abram: 'Fear not, I am your shield; your reward is very great.' Abram "
            "voices his honest doubt—he has no child. God responds by taking him outside to count the "
            "stars and promising that his offspring will be equally uncountable. Abram believes, and "
            "God reckons it as righteousness. Then God makes a solemn covenant through a sacrifice ritual. "
            "In a deep sleep, Abram sees a smoking firepot and flaming torch pass through the pieces—"
            "God alone binds Himself to the promise."
        ),
        "content": (
            "## What Genesis 15 Is About\n"
            "Genesis 15 answers the question: on what basis does a sinful person stand before a holy "
            "God? The answer is faith—trusting God's word and promise. Abram's belief is credited as "
            "righteousness before circumcision, before the Law, and before any human merit. This is "
            "the foundation of the entire biblical theology of justification by faith.\n\n"
            "## Theological Themes\n"
            "- Justification by faith: credited righteousness apart from works\n"
            "- God as shield and great reward—all sufficiency is in Him\n"
            "- Honest prayer: Abram voices his doubt and God does not condemn him but answers\n"
            "- Unconditional covenant: God alone passes through, taking all obligation on Himself\n"
            "- Prophetic revelation: God reveals the 400 years in Egypt before they happen\n\n"
            "## Hebrew Word Notes\n"
            "- hāʾemîn (הֶאֱמִין, Genesis 15:6): 'he believed'; from the root ʾāman—to be firm, "
            "reliable, faithful; Abram's belief was a resting of his whole being on God's word.\n"
            "- ṣedāqāh (צְדָקָה, Genesis 15:6): 'righteousness'; God accounted Abram's faith as "
            "righteousness—this single verse is quoted by Paul in Romans 4 and Galatians 3 as "
            "the anchor of justification by faith.\n"
            "- berît (בְּרִית, Genesis 15:18): 'covenant'; the formal binding agreement; the phrase "
            "'cut a covenant' (kārat berît) reflects the sacrifice ritual through which parties "
            "passed, pledging their lives. Here God alone 'cut through.'\n\n"
            "## What We Can Learn\n"
            "- It is right to bring our honest doubts to God; He meets them with His word and promise.\n"
            "- Salvation has always been by faith—God's plan has never changed across the testaments.\n"
            "- God bears the obligation of the covenant so that its fulfillment rests on His faithfulness, not ours.\n"
            "- God's purposes are not defeated by delays; the 400-year slavery was known and overruled by Him.\n\n"
            "## How This Chapter Points to Christ\n"
            "Genesis 15:6 is the Old Testament's clearest statement of justification by faith, and "
            "the New Testament returns to it repeatedly. Paul argues in Romans 4 that Abram was "
            "justified before circumcision, proving that righteousness comes through faith in God's "
            "promise, not human achievement. The smoking firepot passing through the sacrifice pieces "
            "points to Christ, who passed through death on the cross to secure the new covenant—"
            "taking on Himself the covenant curse so we might receive the blessing.\n\n"
            "## Believers Sword Reflection\n"
            "Genesis 15 invites every believer to rest in the same truth that saved Abram: "
            "God's promise is reliable, and faith in that promise is counted as righteousness. "
            "You do not earn your standing before God—you receive it through trust. And the God "
            "who passed through the sacrifice alone is the God who bears the full weight of keeping "
            "every promise He has ever made."
        ),
        "moral_lessons": [
            "Honest doubt brought to God in prayer is answered with God's word, not condemnation.",
            "Faith—trusting God's word—has always been the basis of right standing before God.",
            "God's unconditional covenant means His faithfulness, not our performance, secures the promise.",
            "Knowing God as our shield and great reward frees us from anxiety about the future.",
        ],
        "application": (
            "Bring your honest doubts and longings to God today. Practice resting—not striving—"
            "for your right standing before God, since it comes through faith, not achievement. "
            "In whatever waiting season you are in, remember that God's purposes are not delayed; "
            "they are unfolding on His timeline."
        ),
        "prayer": (
            "Lord, I believe—help my unbelief. Thank You that my righteousness before You rests "
            "on Your faithfulness, not my performance. You passed through death so I could live. "
            "Anchor my soul in the covenant You sealed in the blood of Jesus. Amen."
        ),
        "key_points": [
            "Abram's belief in God's promise is credited to him as righteousness—the OT root of justification by faith.",
            "Honest doubt is not disqualifying; God met Abram's questions with the stars and His word.",
            "God alone passes through the covenant sacrifice—the obligation rests entirely on Him.",
            "This chapter is quoted in Romans 4 and Galatians 3 as the foundation of Paul's doctrine of faith.",
            "The 400-year prophecy shows God's sovereign foreknowledge encompasses even centuries of suffering.",
        ],
        "study_questions": [
            "What does it mean that God 'counted it to him as righteousness,' and why does this matter for salvation?",
            "How does Abram's honest questioning in vv. 2-3 model healthy prayer?",
            "Why is it significant that only God passes through the animal pieces in the covenant ceremony?",
            "How does Romans 4 use Genesis 15:6 to argue that justification by faith predates the Law?",
        ],
        "original_language_notes": [
            {"term": "hāʾemîn", "language": "Hebrew", "verse": "Genesis 15:6",
             "words_used": "הֶאֱמִין (hāʾemîn)", "meaning": "He believed, trusted, relied upon; from ʾāman (to be firm/reliable); Abram's act of faith was a stable resting of his whole being on God's word—the source of the English word 'amen.'"},
            {"term": "ṣedāqāh", "language": "Hebrew", "verse": "Genesis 15:6",
             "words_used": "צְדָקָה (ṣedāqāh)", "meaning": "Righteousness, right standing; God reckoned Abram's faith as righteousness—the single most-quoted OT verse in the NT letters, anchoring Paul's doctrine of justification by faith."},
            {"term": "berît", "language": "Hebrew", "verse": "Genesis 15:18",
             "words_used": "בְּרִית (berît)", "meaning": "Covenant, solemn binding agreement; the phrase kārat berît (cut a covenant) refers to the ritual of passing between cut animals, pledging life. Here God alone passes through, bearing the full covenant obligation."},
            {"term": "māgēn", "language": "Hebrew", "verse": "Genesis 15:1",
             "words_used": "מָגֵן (māgēn)", "meaning": "Shield, protector; God calls Himself Abram's shield—the divine warrior who defends His covenant partner from every threat."},
        ],
        "tags": ["faith", "righteousness", "justification", "covenant", "Abraham", "promise", "Genesis"],
        "sources": ["Genesis 15:1-21", "Romans 4:1-25", "Galatians 3:6-9", "Hebrews 11:11-12"],
    },
]

# ── DB helpers ─────────────────────────────────────────────────────────────────

def get_collection_id(cur):
    cur.execute("SELECT id FROM commentary_collections WHERE slug='believers-sword-commentaries' LIMIT 1")
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        "INSERT INTO commentary_collections (name, slug, language_code, description) VALUES (?,?,?,?)",
        ("Believers Sword Commentaries", "believers-sword-commentaries", "en",
         "Chapter-by-chapter evangelical commentaries for the Believers Sword app."),
    )
    return cur.lastrowid


def entry_exists(cur, collection_id, book_id, chapter):
    cur.execute(
        """SELECT id, content FROM commentary_entries
           WHERE collection_id=? AND book_id=? AND chapter=?
             AND language_code='en' AND reference_scope='chapter'
             AND deleted_at IS NULL LIMIT 1""",
        (collection_id, book_id, chapter),
    )
    row = cur.fetchone()
    if not row:
        return False
    content = row[1] or ""
    return len(content.strip()) > 200  # shallow check


def insert_entry(cur, collection_id, c):
    entry_uuid = str(uuid.uuid4())
    key_points_json = json.dumps(c["key_points"])
    study_questions_json = json.dumps(c["study_questions"])
    content = c["content"]
    word_count = len(content.split())
    cur.execute(
        """INSERT INTO commentary_entries
           (uuid, collection_id, book_id, chapter, verse_start, verse_end,
            reference_scope, title, summary, content, application, prayer,
            key_points, study_questions, language_code, theological_perspective,
            status, is_ai_generated, ai_model_name, ai_model_provider,
            ai_prompt_version, ai_confidence, word_count, sync_status)
           VALUES (?,?,?,?,NULL,NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            entry_uuid, collection_id, c["book_id"], c["chapter"],
            "chapter", c["title"], c["summary"], content,
            c["application"], c["prayer"],
            key_points_json, study_questions_json,
            "en", "Evangelical Christian", "draft",
            1, "claude-sonnet-4-6", "anthropic",
            "believers-sword-commentary-v2", 0.92,
            word_count, "local",
        ),
    )
    return entry_uuid


def write_json_backup(c, entry_uuid):
    book_slug = c["book"].lower().replace(" ", "-")
    folder_name = f"{c['book_id']:02d}-{book_slug}"
    out_dir = GENERATED_DIR / folder_name
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{c['chapter']:02d}.json"
    payload = {
        "uuid": entry_uuid,
        "collection_name": "Believers Sword Commentaries",
        "author_type": "ai_assisted",
        "language_code": "en",
        "theological_perspective": "Evangelical Christian",
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
        "updated_at": NOW,
    }
    # Verify no forbidden keys
    forbidden = {"is_ai_generated", "model_name", "prompt_version"}
    assert not (forbidden & set(payload.keys())), f"Forbidden key found: {forbidden & set(payload.keys())}"
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    # Verify it parses back
    json.loads(out_path.read_text())
    return str(out_path)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    collection_id = get_collection_id(cur)

    generated = 0
    skipped = 0
    files_written = []
    db_rows = 0
    start_ref = None
    end_ref = None

    for c in COMMENTARIES:
        ref = f"{c['book']} {c['chapter']}"
        if entry_exists(cur, collection_id, c["book_id"], c["chapter"]):
            print(f"  SKIP (exists): {ref}")
            skipped += 1
            if start_ref is None:
                start_ref = ref
            end_ref = ref
            continue

        entry_uuid = insert_entry(cur, collection_id, c)
        conn.commit()
        db_rows += 1

        json_path = write_json_backup(c, entry_uuid)
        files_written.append(json_path)
        generated += 1
        if start_ref is None:
            start_ref = ref
        end_ref = ref
        print(f"  OK: {ref} -> {json_path}")

    # Update progress
    last_c = COMMENTARIES[-1]
    progress = {
        "next_book_id": 1,
        "next_book": "Genesis",
        "next_chapter": last_c["chapter"] + 1,
        "last_completed_book_id": last_c["book_id"],
        "last_completed_book": last_c["book"],
        "last_completed_chapter": last_c["chapter"],
        "completed": False,
        "updated_at": NOW,
    }
    PROGRESS_JSON.write_text(json.dumps(progress, indent=2))

    # Update DB progress table
    cur.execute(
        """INSERT OR REPLACE INTO commentary_generation_progress
           (id, next_book_id, next_book, next_chapter, last_completed_book_id,
            last_completed_book, last_completed_chapter, completed, updated_at)
           VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            progress["next_book_id"], progress["next_book"], progress["next_chapter"],
            progress["last_completed_book_id"], progress["last_completed_book"],
            progress["last_completed_chapter"], 0, NOW,
        ),
    )
    conn.commit()
    conn.close()

    # Append log
    log_entry = {
        "timestamp": NOW,
        "generation_batch_id": BATCH_UUID,
        "start_reference": start_ref,
        "end_reference": end_ref,
        "chapters_generated": generated,
        "chapters_skipped": skipped,
        "db_rows_inserted": db_rows,
        "files_written": files_written,
    }
    with open(LOG_JSONL, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    print("\n=== SUMMARY ===")
    print(f"Range: {start_ref} – {end_ref}")
    print(f"Generated: {generated}, Skipped: {skipped}")
    print(f"DB rows inserted: {db_rows}")
    print(f"Files written: {len(files_written)}")
    print(f"Files: {files_written}")
    print(f"Next starting reference: Genesis {progress['next_chapter']}")


main()
