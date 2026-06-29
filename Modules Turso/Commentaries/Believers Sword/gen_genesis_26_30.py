#!/usr/bin/env python3
"""Generate high-quality commentaries for Genesis 26-30."""
import json, sqlite3, uuid, re
from datetime import datetime, timezone
from pathlib import Path

BASE = Path('/mnt/d/Projects/Personal/Believers-Sword/Modules Turso/Commentaries/Believers Sword')
DB = BASE / 'believers_sword_commentaries.db'
PROGRESS_JSON = BASE / 'commentary_generation_progress.json'
LOG = BASE / 'commentary_generation_log.jsonl'
GENERATED = BASE / 'generated'
COLLECTION_NAME = 'Believers Sword Commentaries'
COLLECTION_SLUG = 'believers-sword-commentaries'
LANG = 'en'
THEOLOGY = 'evangelical'

def now(): return datetime.now(timezone.utc).isoformat(timespec='microseconds').replace('+00:00', 'Z')
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

COMMENTARIES = {
    26: {
        "title": "Genesis 26 — Isaac Inherits the Covenant: Wells, Deception, and God's Unmistakable Blessing",
        "summary": "A famine drives Isaac toward Egypt, but God redirects him to remain in Canaan, reaffirming the Abrahamic covenant. Isaac repeats his father's sin of passing off his wife as his sister. God blesses Isaac with a hundredfold harvest, triggering conflict over wells. Abimelech eventually makes a covenant with Isaac at Beersheba, acknowledging that God is unmistakably with him.",
        "chapter_overview": "Isaac faces famine in Canaan, is told by God not to go to Egypt but to stay and receive the covenant blessings promised to Abraham. He dwells in Gerar, deceives Abimelech about Rebekah, is discovered, and is protected. God blesses him with an extraordinary harvest and flocks. Jealousy prompts the Philistines to stop up Abraham's wells. Isaac reopens them and digs new ones, finally settling at Beersheba where God appears again. Abimelech acknowledges God's blessing and makes a peace covenant. Esau's marriage to Hittite women grieves his parents.",
        "content": """Genesis 26 is the only chapter in the Bible devoted entirely to Isaac as the covenant bearer. Abraham is gone; Jacob has not yet taken center stage. Here Isaac stands alone in the covenant, and the chapter asks: will God's blessing hold? Will the covenant promises survive the second generation's weakness? The answer, emphatically, is yes — but the path is neither smooth nor free of Isaac's own failures.

The chapter opens with a familiar crisis: famine. Abraham had faced this before and gone to Egypt (ch. 12), and the result was damaging. Isaac begins to go to Egypt but God intercepts him at Gerar (vv. 1–2): "Do not go down to Egypt; dwell in the land of which I shall tell you." The divine directive is not a gentle suggestion but a sovereign redirection. God then delivers to Isaac the fullest restatement of the Abrahamic covenant since chapter 22 (vv. 3–5):

"I will be with you and will bless you, for to you and to your offspring I will give all these lands, and I will establish the oath that I swore to Abraham your father. I will multiply your offspring as the stars of heaven and will give to your offspring all these lands. And in your offspring all the nations of the earth shall be blessed, because Abraham obeyed my voice and kept my charge, my commandments, my statutes, and my laws."

Three things are striking in this reaffirmation. First, it is unconditional in its ultimate scope but grounded in Abraham's obedience as a historical demonstration of what covenant faithfulness looks like. Second, it is specifically tailored to Isaac: God says "I will be with you" — not merely a reference to Abraham's God, but a personal guarantee to Isaac himself. Third, it explicitly extends to "all the nations," embedding the universal dimension of blessing within this very particular covenant.

Settled in Gerar, Isaac repeats almost exactly the error of his father: he tells the Philistines that Rebekah is his sister because he fears being killed for her beauty (vv. 7–11). The repeated nature of this sin is uncomfortable — it stretches across two generations and two patriarchs. The biblical narrator does not soften it. Sin patterns are inheritable; spiritual weakness runs in families. Yet what is equally striking is God's protection despite the sin. Abimelech discovers the truth not through scandal but through observation ("Isaac was laughing with Rebekah his wife," v. 8 — a play on the name Isaac, from yitzchak, "he laughs"), and he immediately places a death penalty on anyone who harms them. God's protection operates even through a pagan king's conscience.

The agricultural blessings that follow are extraordinary: "And Isaac sowed in that land and reaped in the same year a hundredfold. The LORD blessed him, and the man became rich, and gained more and more until he became very wealthy" (vv. 12–13). The hundredfold harvest (me'ah she'arim) in a famine year is miraculous. It draws public attention because it cannot be explained naturally. The Philistines' response — stopping up Abraham's wells (v. 15) and Abimelech asking Isaac to leave (v. 16) — is the classic response of the world to the conspicuously blessed: envy and expulsion.

The well-opening narrative (vv. 17–25) is deceptively simple but theologically rich. Wells in the ancient Near East were vital infrastructure — life-giving, expensive to dig, fiercely contested. Abraham had dug these wells (v. 18); Isaac reopens them and gives them back their fathers' names. This is an act of covenant memory: Isaac is not starting fresh but reclaiming what was given. The disputes at Esek ("contention") and Sitnah ("enmity") give way to Rehoboth — "Spacious places" or "wide room." Isaac's commentary is: "For now the LORD has made room for us, and we shall be fruitful in the land" (v. 22). The progression from contention to spaciousness is a parable of perseverance.

At Beersheba God appears again (vv. 23–24): "Fear not, for I am with you and will bless you and multiply your offspring for my servant Abraham's sake." The repeated assurance "I am with you" (ani immach) is the covenant promise that animates the entire patriarchal narrative. It follows each generation and each crisis. Isaac builds an altar, calls on the name of YHWH, and pitches his tent — worship, prayer, and settled life together, as Abraham had done before him.

Abimelech's arrival (vv. 26–31) is the climactic acknowledgment of the chapter. The powerful come to the blessed: "We see plainly that the LORD has been with you" (v. 28). The pagan king cannot deny the evidence. The covenant of peace sealed with a feast demonstrates that God's blessing on His people ultimately draws the nations toward peace rather than toward permanent conflict. The chapter closes darkly (vv. 34–35): Esau's marriage to two Hittite women "made life bitter for Isaac and Rebekah." The covenant line's continued threat is not from outside armies but from within the family's own choices. Genesis keeps the tension alive.""",
        "original_language_notes": [
            {
                "term": "מֵאָה שְׁעָרִים (me'ah she'arim)",
                "language": "Hebrew",
                "verse": 12,
                "words_used": ["me'ah", "she'arim"],
                "meaning": "'A hundred gates' = hundredfold. The idiom describes a harvest yield one hundred times the amount sown. In a famine year this is unmistakably miraculous and makes YHWH's blessing visible to surrounding peoples. The phrase is grammatically unusual (literally 'a hundred measures/gates'), reinforcing its extraordinary character."
            },
            {
                "term": "אֲנִי עִמָּךְ (ani immach)",
                "language": "Hebrew",
                "verse": 24,
                "words_used": ["ani", "immach"],
                "meaning": "'I am with you.' This is the signature covenant assurance of the patriarchal narratives, spoken to Abraham, Isaac, Jacob, Joseph, and ultimately echoing in Immanuel (God with us). The phrase does not merely describe proximity but covenantal presence — YHWH's active power, protection, and faithfulness operating on behalf of the one addressed."
            },
            {
                "term": "רְחֹבֹות (Rechovot)",
                "language": "Hebrew",
                "verse": 22,
                "words_used": ["Rechovot"],
                "meaning": "'Wide places / spacious room.' From rachav (to be wide, broad). The name Isaac gives the third well memorializes God's provision of space after repeated conflict. His statement 'now the LORD has made room for us' uses the same root — ki-irtchiv YHWH lanu. The place name encodes a theological testimony: God ultimately provides room for His people."
            },
            {
                "term": "יִצְחָק מְצַחֵק (Yitzchak metzachek)",
                "language": "Hebrew",
                "verse": 8,
                "words_used": ["Yitzchak", "metzachek"],
                "meaning": "'Isaac was laughing/playing' (with Rebekah). The Hebrew pun is unmissable: Isaac (Yitzchak) was seen 'isaacking' (metzachek) with his wife. The same root describes what made Sarah laugh in 18:12 and what Isaac's name commemorates. The action Abimelech saw was intimate and affectionate — not the behavior of a brother — and the wordplay identifies the observer's insight through linguistic irony."
            },
            {
                "term": "מְרֹרַת רוּחַ (merorat ruach)",
                "language": "Hebrew",
                "verse": 35,
                "words_used": ["merorat", "ruach"],
                "meaning": "'Bitterness of spirit.' The phrase describes the grief Esau's Hittite wives caused Isaac and Rebekah. Marar means to be bitter (the root of 'Marah' in Exodus 15); ruach means breath/spirit. Together they paint deep emotional and spiritual anguish — a grief that went to the core. This anticipates the coming conflict over the blessing in ch. 27, where domestic pain becomes the seedbed of deception."
            }
        ],
        "moral_lessons": [
            "God's covenant is never merely inherited passively — each generation must personally encounter, receive, and respond to God's promises.",
            "The sins of fathers repeat in sons (Isaac's deception mirrors Abraham's), warning us that unconfessed patterns are passed on, not merely outgrown.",
            "God's blessing is publicly visible and draws inevitable attention — both grateful acknowledgment (Abimelech) and envious hostility (stopped-up wells).",
            "Perseverance through conflict — digging wells that keep being contested — eventually produces Rehoboth: the wide, spacious places God makes for His faithful.",
            "Esau's choice of wives (grieving his parents' spirit) demonstrates that spiritual insensitivity in domestic life has far-reaching consequences for the covenant family."
        ],
        "application": "Genesis 26 asks whether we will stay in the land God has called us to when famine comes — or flee to Egypt's immediate comfort. It also confronts us with the reality that spiritual patterns run in families. Where have you inherited a fear-driven deception from those who raised you? What wells has God dug in your history that others have stopped up — and have you dug them back open? The chapter's progression from Esek (contention) to Sitnah (enmity) to Rehoboth (spacious room) maps a real spiritual journey: persistent faithfulness eventually reaches the wide places. Finally, Abimelech's confession — 'We see plainly that the LORD has been with you' — raises the question: is God's blessing on your life visible enough to draw that kind of acknowledgment from those who do not share your faith?",
        "prayer": "Lord God, thank You that Your covenant is not exhausted in one generation but flows faithfully to our children and our children's children. Forgive us for the sin patterns we have inherited and failed to break. Give us the perseverance to keep digging wells even when others stop them up. Make room for us as You made room for Isaac, and let Your blessing on our lives be so evident that even those who do not know You are moved to acknowledge that You are with us. Through Jesus Christ, Amen.",
        "key_points": [
            "God redirects Isaac from Egypt to Canaan and reaffirms the full Abrahamic covenant — land, descendants, worldwide blessing — personalizing it to Isaac directly.",
            "Isaac repeats Abraham's deception about his wife, showing how sin patterns are transmitted across generations even in covenant families.",
            "A hundredfold harvest in a famine year makes God's blessing publicly undeniable and triggers both Philistine envy and eventual covenant recognition.",
            "The well-conflict sequence (Esek → Sitnah → Rehoboth) teaches that perseverance through contested blessing eventually reaches God-given spacious room.",
            "God appears again at Beersheba, repeating 'I am with you' — the signature covenant promise given to each patriarch personally.",
            "Abimelech seeks peace with Isaac because he recognizes God's unmistakable presence — the pagan king becomes a witness to YHWH's faithfulness.",
            "Esau's Hittite marriages cause bitter grief, foreshadowing the family conflict of chapter 27 and demonstrating that covenant faithfulness requires covenant marriages."
        ],
        "study_questions": [
            "God tells Isaac not to go to Egypt but to trust Him in the land of famine. Where is God currently calling you to stay and trust rather than flee to easier circumstances?",
            "Isaac repeats his father's sin of deception almost word for word. What inherited spiritual patterns — fears, habits, deceptions — do you recognize in yourself from your family of origin?",
            "The wells at Esek and Sitnah were contested, but Rehoboth was spacious. What 'wells' in your spiritual life keep being contested by others, and how does Isaac's perseverance encourage you?",
            "Abimelech, a pagan king, says 'We see plainly that the LORD has been with you.' What would someone observing your life say about whether God is visibly with you?",
            "What does the hundredfold harvest in a famine year teach about God's ability to bless in circumstances that seem to preclude blessing?",
            "How does God's personal word 'I am with you' (ani immach) function differently from a general theological truth about God's omnipresence? Why does it matter that God says this to Isaac personally?"
        ],
        "tags": ["Genesis", "Isaac", "covenant", "wells", "famine", "blessing", "Abimelech", "Beersheba", "Rebekah", "patriarchs"]
    },

    27: {
        "title": "Genesis 27 — The Stolen Blessing: Deception, Tears, and the Sovereignty That Overrules Sin",
        "summary": "Isaac, aged and blind, intends to give Esau the patriarchal blessing before dying. Rebekah overhears and engineers a deception: Jacob impersonates Esau and receives the blessing. When Esau returns, Isaac trembles with the realization that the blessing has gone irreversibly to Jacob. Esau weeps and plans to kill Jacob. Rebekah arranges Jacob's departure to Laban in Haran.",
        "chapter_overview": "Isaac summons Esau to receive the covenant blessing before Isaac dies. Rebekah hears and plans for Jacob to receive it instead. Jacob dresses in Esau's clothes and goat skins, brings food he has prepared, and deceives his blind father. Isaac gives Jacob the blessing of dew, grain, wine, lordship over brothers, and the Abrahamic promise. Esau returns, the deception is discovered, and Isaac trembles. Esau weeps, receives a lesser blessing of the sword and eventual freedom. He plans murder. Rebekah sends Jacob to her brother Laban.",
        "content": """Genesis 27 is the most dramatically tense chapter in the patriarchal narratives — a chapter that disturbs modern readers precisely because it shows God's sovereign purposes running through very human scheming, very real tears, and apparently irreversible deception. It is a chapter about blessing, loss, and the terrifying weight of words once spoken.

Isaac is old, his eyes dim (v. 1). The phrase "his eyes were too dim to see" (kahehu einav me-re'ot) is both physical description and dramatic setup: the man whose name means "laughter" is now not laughing, and the man whose life began with a miracle will pass the covenant blessing in the dark, literally and figuratively. He summons Esau, instructs him to hunt game and prepare the food Isaac loves, and plans to give him the blessing "before I die" (v. 4).

Rebekah hears every word (v. 5). What follows is her plan, and the text does not excuse it. She is the one who says: "Let your curse be on me, my son; only obey my voice" (v. 13). The reader is caught between the divine oracle of chapter 25 ("the older shall serve the younger") and the wrongness of achieving a divine end through human deception. The New Testament's treatment of this episode is instructive: Hebrews 11:20 credits Isaac's blessing of Jacob and Esau as an act of faith — focused on the blessing's content, not the method — while never endorsing the deception.

Jacob's impersonation is elaborate. He wears Esau's garments (carrying Esau's smell), puts goat skins on his hands and neck (simulating Esau's hairiness), and brings the prepared food. The scene at the bedside is harrowing in its specificity: Isaac suspects, asks twice "Who are you, my son?" (vv. 18, 24), touches the goat-skin hands ("The voice is Jacob's voice, but the hands are the hands of Esau," v. 22), smells the garments, and finally blesses him. The blessing itself (vv. 27–29) is profoundly covenantal:

"May God give you of the dew of heaven
and of the fatness of the earth
and plenty of grain and wine.
Let peoples serve you,
and nations bow down to you.
Be lord over your brothers,
and may your mother's sons bow down to you.
Cursed be everyone who curses you,
and blessed be everyone who blesses you!"

The final line is the Abrahamic formula (12:3) — Isaac is not merely distributing a personal inheritance; he is transmitting the Abrahamic covenant. Whatever the method, the substance of the blessing falls precisely where God had ordained.

Esau's return (vv. 30–40) is among the most emotionally shattering passages in the Bible. He comes in with his game, with joy, asking for the blessing — and "Isaac trembled very violently" (v. 33). The word is chared charadah gedolah meod — trembling he trembled a great trembling exceedingly. The doubled construction expresses overwhelming, visceral shock. Isaac immediately grasps what has happened and says, in one of the Bible's most theologically laden sentences: "I blessed him — yes, and he shall be blessed" (v. 33). Not: "I made a mistake, so we can cancel it." Not: "It was obtained by fraud, so it's void." The spoken word, once given with patriarchal authority, cannot be recalled. Isaac does not even try.

"When Esau heard the words of his father, he cried out with an exceedingly great and bitter cry and said to his father, 'Bless me, even me also, O my father!'" (v. 34). The Hebrew doubles the adjectives as it doubled Isaac's trembling: za'ak ze'akah gedolah u-marah ad meod — he cried a cry great and bitter exceedingly. The text is full of sound — weeping, pleading, anger. Esau weeps twice in this narrative (vv. 34, 38). The letter to the Hebrews later comments that "he found no chance to repent, though he sought it with tears" (Heb. 12:17) — not saying the tears were insincere, but that the moment of the blessing was genuinely past. Some things cannot be undone.

Isaac's blessing for Esau (vv. 39–40) is a realistic prognosis rather than a curse: "Away from the fatness of the earth shall your dwelling be... By your sword you shall live, and you shall serve your brother; but when you grow restless, you shall break his yoke from your neck." The Edomites (Esau's descendants) historically struggled with and intermittently threw off Israelite dominance (see 2 Kings 8:20–22). God did not abandon Esau — the blessing acknowledges a real future for his line — but the covenant line passes through Jacob.

The chapter ends with Esau's murderous intention and Rebekah's response. Her plan works: Jacob escapes. But the cost is high. Rebekah and Jacob are never reunited in the biblical narrative. The deception that preserves Jacob's life separates him from his mother permanently. Sin's consequences are not erased by God's sovereignty; they are taken up into His purposes while the human pain remains real.

Christologically, the chapter anticipates a greater exchange: Christ taking on what is ours (our curse, our guilt) so that we might receive what is His (the Father's blessing, the covenant inheritance). Paul alludes to this pattern: "Christ redeemed us from the curse of the law by becoming a curse for us" (Gal. 3:13). The stolen blessing of Genesis 27 becomes, in redemptive history, the freely given blessing of the new covenant — obtained not by Jacob's deception but by Christ's righteousness.""",
        "original_language_notes": [
            {
                "term": "כָּהֲתָה עֵינָיו מֵרְאֹת (kahehu einav me-re'ot)",
                "language": "Hebrew",
                "verse": 1,
                "words_used": ["kahehu", "einav", "me-re'ot"],
                "meaning": "'His eyes were too dim to see.' Kahah means to be faint, dim, or extinguished — used of eyes, lamps, and spirit. The dimming of Isaac's sight is the plot hinge of the entire chapter. It also carries ironic weight: the man God 'opened the eyes' of his parents to see His provision (ch. 22) now cannot see clearly enough to bestow the covenant correctly. Divine purposes are advanced through human limitation."
            },
            {
                "term": "חָרַד חֲרָדָה גְּדֹלָה מְאֹד (charad charadah gedolah meod)",
                "language": "Hebrew",
                "verse": 33,
                "words_used": ["charad", "charadah", "gedolah", "meod"],
                "meaning": "'He trembled a very great trembling.' The doubled noun-verb construction (figura etymologica) intensifies the emotion to its maximum. Charad can describe the terror of divine encounter, battle, or overwhelming revelation. Isaac's violent trembling shows he understands immediately that the blessing cannot be recalled — not merely because Esau is disappointed, but because God's word has been spoken and cannot return void."
            },
            {
                "term": "בְּרָכָה (berakah)",
                "language": "Hebrew",
                "verse": 36,
                "words_used": ["berakah"],
                "meaning": "'Blessing.' Central word of the chapter, appearing 22 times in vv. 1–40. In the ancient world a spoken patriarchal blessing was more than sentiment — it was a solemn declaration that released divine favor and ordered social structures. Once spoken over a person with covenantal authority, it was binding. Esau asks 'Is he not rightly named Jacob? For he has supplanted me (akavani) twice — he took away my birthright (bekhorah), and behold, now he has taken away my blessing (berakah).' The wordplay on bekhorah/berakah is deliberate: the birthright and the blessing go together."
            },
            {
                "term": "גַּם בָּרוּךְ יִהְיֶה (gam baruch yihyeh)",
                "language": "Hebrew",
                "verse": 33,
                "words_used": ["gam", "baruch", "yihyeh"],
                "meaning": "'Yes, and he shall be blessed.' Isaac's decisive statement after discovering the deception. He does not revoke, contest, or qualify. The word gam (also, even, yes) functions as emphatic affirmation. The passive participle baruch ('one who is blessed') followed by a future verb communicates settled, irrevocable reality. This sentence reveals that Isaac understands the blessing as belonging to the realm of divine speech, not merely human intention."
            },
            {
                "term": "אָרוּר כָּל מְקַלְלֶךָ וּמְבָרֲכֶיךָ בָּרוּךְ (arur kol mekallelcha u-mevaracheicha baruch)",
                "language": "Hebrew",
                "verse": 29,
                "words_used": ["arur", "mekallelcha", "mevaracheicha", "baruch"],
                "meaning": "'Cursed be everyone who curses you, and blessed be everyone who blesses you.' This formula echoes the Abrahamic blessing of 12:3 almost verbatim, confirming that Isaac is transmitting not merely personal favor but the Abrahamic covenant. The passive participles (arur = cursed one; baruch = blessed one) describe fixed states: one's relationship to Jacob-Israel determines one's covenantal standing before God."
            }
        ],
        "moral_lessons": [
            "God's sovereign purposes are not thwarted by human sin, but sin still carries real consequences — Rebekah loses Jacob permanently, Jacob spends years as an exile.",
            "The irreversibility of Isaac's spoken blessing reveals the weight of words: once given in covenant context, they cannot be recalled, only grieved over.",
            "Esau's tears demonstrate that sincere emotional regret is not the same as genuine repentance — the opportunity for the birthright and blessing was squandered long before (ch. 25:34).",
            "Family favoritism (Isaac favoring Esau, Rebekah favoring Jacob) becomes the soil in which deception grows; divided households divide covenant families.",
            "Even wrongly obtained blessings point to a greater truth: in Christ, those who deserve curse receive blessing through substitution — the One who had no sin became sin for us."
        ],
        "application": "Genesis 27 is deeply uncomfortable because it forces the question: can God accomplish His purposes through our sin? The answer is yes — and that is not a license to sin but a testimony to grace. Where in your life have you tried to 'help God along' with deception, manipulation, or strategic omission of truth? The chapter also confronts us with the weight of words. What blessings have you withheld from children, spouses, or friends that once spoken, might not be able to be given back? And for those who feel like Esau — who missed something they can never recover — the gospel offers what Esau could not receive: a blessing obtained not by human scheming but by Christ's perfect righteousness, freely given to those who come with empty hands.",
        "prayer": "Father, we confess that we too have sometimes taken what was not ours by deception, or manipulated situations to our advantage, believing we were securing Your will. Forgive us, and show us the real cost of those choices — the Esau-tears, the broken relationships, the years of exile. Thank You that in Christ, the curse we deserve has been borne by Another, and the blessing we could never earn has been freely given. Help us to speak blessing to those around us today — clearly, freely, unreservedly — as those who have themselves received what we did not deserve. Amen.",
        "key_points": [
            "Isaac's blind eyes set the stage for the deception — human weakness becomes the hinge on which divine purposes unexpectedly turn.",
            "Rebekah orchestrates the deception believing she is serving God's oracle from chapter 25, but the method is wrong even if the end was foreordained.",
            "Jacob impersonates Esau with remarkable specificity — smell, touch, food, voice — underscoring the deliberate and calculated nature of the deception.",
            "Isaac's blessing contains the Abrahamic formula ('cursed be everyone who curses you'), confirming the covenant is fully transmitted to Jacob.",
            "Isaac's 'violent trembling' at the discovery and his statement 'he shall be blessed' reveal that spoken covenant blessings carry divine weight beyond human intention.",
            "Esau's tears are genuine but come too late — Hebrews 12 uses this episode to warn believers not to treat covenant privileges as trivially tradeable.",
            "The chapter ends in exile and family rupture: God's purposes are advanced, but the human cost of deception is very real and lasting."
        ],
        "study_questions": [
            "Rebekah believed she was helping God fulfill His own prophecy (Gen 25:23). When is it right to act on a divine promise, and when is it presumptuous to 'help God along' through our own schemes?",
            "Isaac says 'Yes, and he shall be blessed' even after discovering the fraud. What does this reveal about the nature of covenant blessings vs. human intentions?",
            "Esau wept bitterly, yet Hebrews 12:17 says he 'found no chance to repent.' What is the difference between remorse and repentance? How does Esau's situation illustrate it?",
            "Family favoritism (Isaac loved Esau; Rebekah loved Jacob) created the soil for this deception. How does partiality damage a family spiritually?",
            "The New Testament applies the blessing/curse language of this chapter to Christ (Gal. 3:13). How does the 'stolen blessing' narrative anticipate the gospel?",
            "What words of blessing have you been slow to speak to those around you? What would it look like to be more generous and specific with encouragement and blessing today?"
        ],
        "tags": ["Genesis", "Jacob", "Esau", "Isaac", "Rebekah", "blessing", "deception", "covenant", "election", "sin"]
    },

    28: {
        "title": "Genesis 28 — Jacob's Ladder: The God Who Meets Fugitives and Fills Empty Places with His Presence",
        "summary": "Isaac sends Jacob to Paddan-aram to find a wife from Laban's family. Esau observes and takes an Ishmaelite wife to please his parents. Fleeing toward Haran, Jacob sleeps in the open field and dreams of a stairway between heaven and earth with angels ascending and descending. God stands above it and reaffirms the Abrahamic covenant directly to Jacob, promising presence, return, and blessing. Jacob wakes, makes a vow, and names the place Bethel — House of God.",
        "chapter_overview": "Isaac blesses Jacob and sends him to Laban to find a wife, forbidding him from Canaanite women. Esau, seeing his parents' displeasure, takes an Ishmaelite wife. Jacob departs and stops for the night at a certain place. He dreams of a stairway (sullam) reaching to heaven with angels on it and God above it. God speaks: 'I am the LORD, the God of Abraham your father and the God of Isaac. The land on which you lie I will give to you and to your offspring... I am with you.' Jacob wakes, anoints a stone pillar, names the place Bethel, and makes a conditional vow.",
        "content": """Genesis 28 is one of the most luminous chapters in the entire Bible. A guilty man, alone, without sanctuary or city, sleeping with a stone for a pillow, becomes the site of heaven's opening. The God of the universe does not wait for Jacob to arrive at a temple; He opens the temple to Jacob on a dark hillside in the middle of nowhere.

Jacob leaves Beersheba for Paddan-aram under a double commission: find a wife from Laban's household (vv. 1–2), and receive the Abrahamic blessing from Isaac's own lips before he leaves (v. 3–4). This second act — a formal, unambiguous covenant blessing given to Jacob by his father, this time without deception — legitimizes Jacob's position irrevocably. Whatever ambiguity surrounds chapter 27, chapter 28 removes it: Isaac blesses Jacob as the covenant bearer.

The short notice about Esau (vv. 6–9) is pointed. He sees Jacob blessed and sent, observes that Isaac disapproves of Canaanite wives, and responds by taking an Ishmaelite wife (Mahalath, daughter of Ishmael). The gesture is both too little and too late — he is trying to correct his error by addition rather than genuine repentance. It is the response of someone who understands rules but not the heart behind them.

Jacob journeys alone and comes to "a certain place" (makom) and spends the night there (v. 11). The word makom is unspecified — generic, unimportant. But this ordinary place becomes the location of the extraordinary. He takes a stone, sets it as a pillow, and sleeps. The dream that follows (vv. 12–15) is one of Scripture's most vivid divine visions:

"And behold, there was a ladder set up on the earth, and the top of it reached to heaven. And behold, the angels of God were ascending and descending on it! And behold, the LORD stood above it and said..."

The word sullam (translated "ladder" or "stairway") appears only here in the entire Hebrew Bible — a hapax legomenon — as if the language itself is stretched to describe what normal vocabulary cannot contain. Jewish and Christian interpreters have linked it to the ziggurat (temple-tower) form — a connection between earth and heaven — but the meaning is clear regardless: the barrier between the human and the divine has been penetrated. Traffic moves between heaven and earth. God is not distant.

God's words to Jacob (vv. 13–15) are the full Abrahamic covenant spoken directly and personally to a fugitive:

"I am the LORD, the God of Abraham your father and the God of Isaac. The land on which you lie I will give to you and to your offspring. Your offspring shall be like the dust of the earth, and you shall spread abroad to the west and to the east and to the north and to the south, and in you and your offspring shall all the families of the earth be blessed. Behold, I am with you and will keep you wherever you go, and will bring you back to this land. For I will not leave you until I have done what I have promised you."

Every element of the Abrahamic covenant is present: land (the very ground Jacob is lying on), offspring (innumerable), universal blessing, and the personal promise "I am with you." But the final phrase is unique to Jacob and this moment: "I will not leave you until I have done what I have promised you." God binds Himself to a fugitive's future with a promise of completion. The covenant is not abstract; it is chronological: it will be fulfilled, and God will be present every moment until it is.

Jacob wakes to one of Scripture's most awe-struck responses: "Surely the LORD is in this place, and I did not know it" (v. 16). The grammar is emphatic — surely, in this place, God was. He was not absent. Jacob was absent from awareness, and now awakened to a reality that had always been present. His next words: "How awesome is this place! This is none other than the house of God, and this is the gate of heaven" (v. 17). He calls it beit Elohim — "house of God" — a name that later applied to the Jerusalem temple, the tabernacle, and ultimately, in Christ, to the believer's body (1 Cor. 6:19). Every believer carries a Bethel; we are each the house of God, the site of heaven's opening.

Jacob rises early, takes the stone he used as a pillow, sets it up as a pillar (matseivah), pours oil on it, and names the place Bethel (v. 19). He then makes a vow (vv. 20–22) — a conditional vow, and this has troubled commentators: "If God will be with me... then the LORD shall be my God." Is this mere bargaining? The majority view is that Jacob is not doubting God's word but expressing his own dependence and responding to the covenant with a covenant: I will walk with You if You walk with me. The vow also includes returning a tithe (v. 22) — an acknowledgment that everything Jacob gains will be from God's hand.

Jesus explicitly connects this passage to Himself in John 1:51: "You will see heaven opened, and the angels of God ascending and descending on the Son of Man." Jesus is the sullam — the ladder, the stairway, the one connection between heaven and earth. All the traffic of heaven's grace flows through Him; all our prayers ascend through Him. What Jacob saw in a dream was a prophetic image of the Incarnation: God bridging the gap to a guilty, fleeing humanity.""",
        "original_language_notes": [
            {
                "term": "סֻלָּם (sullam)",
                "language": "Hebrew",
                "verse": 12,
                "words_used": ["sullam"],
                "meaning": "'Ladder / stairway.' A hapax legomenon — found only here in the entire Hebrew Bible. Its root may relate to salal (to heap up, build a way) or to the Akkadian simmiltu (stairway of a ziggurat). The word is stretched beyond ordinary vocabulary to describe something for which Hebrew had no regular word — a connection between earth and heaven. Its uniqueness signals the uniqueness of the vision itself. Jesus applies it to Himself in John 1:51."
            },
            {
                "term": "בֵּית אֱלֹהִים (Beit Elohim)",
                "language": "Hebrew",
                "verse": 17,
                "words_used": ["Beit", "Elohim"],
                "meaning": "'House of God.' Jacob's name for the place where heaven opened becomes the name Bethel. The phrase later describes the tabernacle, the temple, and in the New Testament, the community of believers (1 Tim. 3:15) and the individual believer (1 Cor. 6:19). Jacob's insight — that God's presence transforms an ordinary location into a divine dwelling — becomes a theological principle throughout Scripture: God sanctifies places by His presence, not places God by their sanctity."
            },
            {
                "term": "מַצֵּבָה (matseivah)",
                "language": "Hebrew",
                "verse": 18,
                "words_used": ["matseivah"],
                "meaning": "'Pillar / standing stone.' From natzav (to stand upright). A memorial stone set up to mark a significant encounter with God. Jacob anoints it with oil — an act of consecration. The same word is later sometimes condemned when standing stones became sites of pagan worship (Lev. 26:1), but here it is clearly a covenant memorial: 'God met me here.' The practice of marking divine encounters with physical memorials runs throughout the patriarchal period."
            },
            {
                "term": "אֵין זֶה כִּי אִם בֵּית אֱלֹהִים (ein zeh ki im beit Elohim)",
                "language": "Hebrew",
                "verse": 17,
                "words_used": ["ein", "zeh", "ki", "im", "beit", "Elohim"],
                "meaning": "'This is none other than the house of God.' The phrase uses ein + ki im (there is nothing but / this is nothing else than) for emphatic exclusivity. Jacob is not saying the place is one of several holy sites; he is saying it is categorically different from what he thought it was. The awe of the statement is total: this ordinary stopping place is the very house of God, the gate of heaven."
            },
            {
                "term": "עַד אֲשֶׁר אִם עָשִׂיתִי אֵת אֲשֶׁר דִּבַּרְתִּי לָךְ (ad asher im asiti et asher dibarti lach)",
                "language": "Hebrew",
                "verse": 15,
                "words_used": ["ad", "asher", "im", "asiti", "asher", "dibarti", "lach"],
                "meaning": "'Until I have done what I have promised you.' The clause uses ad (until) with a perfect tense verb — framing God's commitment in terms of definite, completed future action. The promise is not open-ended in the sense of uncertain; it is open-ended only in the sense of 'I am committed until it is finished.' This is one of the Bible's most personal expressions of divine faithfulness: God binds His presence to a fugitive until every covenant word is kept."
            }
        ],
        "moral_lessons": [
            "God is not confined to sacred buildings or holy cities — He meets guilty, fleeing people in anonymous wilderness locations, on their way to somewhere else.",
            "The gap between heaven and earth that Genesis 3 opened is not permanent: God can and does re-open heaven to speak, promise, and be present with His people.",
            "Awareness of God's presence is not automatic — Jacob had to be awakened to it. The practice of spiritual attentiveness — noticing where God is — must be cultivated.",
            "Every location where God's presence is encountered becomes holy — not by inherent virtue but by the reality of His dwelling there. Every believer is, in Christ, a Bethel.",
            "God's covenant promises are given to us personally, not only corporately. He says 'I am with you' to Jacob the individual, as He says it to each believer in Christ."
        ],
        "application": "Genesis 28 asks: where is your Bethel? In what ordinary place, at what unexpected moment, has God opened heaven to you and said 'I am with you'? The danger Jacob faced — sleeping through God's presence, moving on without naming the encounter — is our danger too. We may be in the middle of God's most significant work and fail to recognize it because we are looking for temples, not stones. Jesus's application of the sullam to Himself in John 1:51 is the key: He is the stairway, and every prayer, every scripture, every encounter in His name is an ascending-and-descending on that stairway. Use it. Name your Bethels. Build your pillars of memory. Return your tithes as acknowledgment that all you have comes from God's hand.",
        "prayer": "Lord God, You are the God who meets fugitives. You met Jacob at his lowest point — guilty, afraid, alone, sleeping on a stone — and opened heaven to him. Meet us in our own wilderness places. Teach us to recognize Your presence in ordinary moments, to wake with Jacob's words: 'Surely the LORD is in this place, and I did not know it.' Thank You that in Jesus, the stairway between heaven and earth stands permanently open, and the angels of grace ascend and descend freely. Help us to live as Bethels — houses of Your presence — wherever we go. Amen.",
        "key_points": [
            "Isaac's formal, deliberate blessing of Jacob in chapter 28 (without deception) settles the covenant question permanently: Jacob is the bearer of the Abrahamic promise.",
            "The sullam (ladder/stairway) is a hapax legomenon — a unique word for a unique vision, depicting the vertical connection between earth and heaven that Christ would ultimately embody.",
            "God's covenant speech to Jacob is the complete Abrahamic package — land, offspring, universal blessing, personal presence — spoken directly to a fugitive in the wilderness.",
            "The phrase 'I will not leave you until I have done what I have promised' is one of Scripture's most personal divine commitments, binding God's presence to the completion of every covenant word.",
            "Jacob's response — 'Surely the LORD is in this place' — models awakening to a divine presence that was always there but not perceived.",
            "Bethel ('house of God') becomes a paradigm: every place where God's presence is encountered is transformed into a sacred site of covenant memory.",
            "Jesus explicitly identifies Himself as the sullam in John 1:51, placing this dream at the center of a Christological trajectory through the entire Old Testament."
        ],
        "study_questions": [
            "Jacob was fleeing, guilty, and sleeping on a stone when God appeared. What does this tell us about the conditions God requires before He will meet with a person?",
            "The sullam (stairway) is described as 'set up on the earth' with 'its top reaching to heaven.' Jesus applies this image to Himself (John 1:51). How does Christ fulfill what the ladder pointed to?",
            "Jacob says 'Surely the LORD is in this place, and I did not know it.' Have you ever recognized God's presence in a situation only in retrospect? What helped you see it?",
            "God says 'I will not leave you until I have done what I have promised.' How does this specific formulation differ from a general assurance of God's presence? What does it mean for you personally?",
            "Jacob's vow in verses 20–22 is conditional ('If God will be with me...'). Is this genuine covenant response or spiritual bargaining? How do you evaluate it?",
            "What are the 'Bethels' in your own life — ordinary places and moments where God opened heaven to you? How do you honor and remember those encounters?"
        ],
        "tags": ["Genesis", "Jacob", "Bethel", "covenant", "angels", "ladder", "vision", "promise", "presence", "Christ"]
    },

    29: {
        "title": "Genesis 29 — Jacob in Haran: Love, Deception Returned, and the God Who Sees the Unloved",
        "summary": "Jacob arrives in Haran at a well and meets Rachel, instantly moved to roll the stone and water her flocks. He is welcomed by Laban and works seven years for Rachel, years that 'seemed to him but a few days' because of his love. On the wedding night Laban substitutes Leah, and Jacob discovers the deception in the morning. He works another seven years for Rachel. God opens Leah's womb and she bears four sons — Reuben, Simeon, Levi, and Judah — each name testifying to God's mercy on the unloved.",
        "chapter_overview": "Jacob arrives at a well near Haran and meets shepherds waiting for the stone to be rolled away. Rachel arrives with Laban's flock; Jacob rolls the stone alone and waters her sheep. He weeps, introduces himself, and Rachel runs to tell Laban. Jacob works seven years for Rachel, which feel like days because of his love. Laban gives Leah to Jacob on the wedding night; Jacob discovers in the morning. Laban explains the custom (older before younger). Jacob marries Rachel after the bridal week and works another seven years. God sees Leah's affliction and opens her womb: Reuben, Simeon, Levi, Judah.",
        "content": """Genesis 29 is a story of love at first sight, labor freely given, and deception tasting its own medicine — but at its heart it is a story about a woman no one wanted, whose names for her children become the most sustained theological reflection on divine grace in the entire patriarchal narrative.

Jacob arrives at a well in the east (v. 1). The well-scene is immediately reminiscent of the Genesis 24 scene — Abraham's servant also met Rebekah at a well. Wells in biblical narrative are liminal spaces, transitional sites where futures are determined. The shepherds explain they are waiting for all the flocks to gather before rolling the stone (v. 8) — whether from custom, safety, or communal obligation. When Rachel arrives (v. 9), Jacob acts with decisive, even impulsive energy: "Jacob went near and rolled the stone from the well's mouth alone" (v. 10). The emphasis on alone (levado) is significant — he lifts what normally requires many. Love makes extraordinary effort possible.

Jacob's response to Rachel is emotional and immediate: "Jacob kissed Rachel and wept aloud" (v. 11). The kissing was probably a greeting kiss among family members (he has just identified himself as her cousin), but the weeping is striking. The Hebrew is vayissa kolo vayevk — "he lifted his voice and wept." Commentators debate why: relief at journey's end? Overwhelmed at finding family? Moved by Rachel's beauty? The text does not specify — it simply records a man who has left everything weeping at the first kindness he receives. In an often stone-cold narrative world, it is a moment of touching vulnerability.

Laban's welcome is warm with potential self-interest: "You are my bone and my flesh!" (v. 14) — a familial covenant formula. Jacob works for Laban and at the end of a month Laban asks him what wages he wants. The proposal Jacob makes is itself remarkable: "I will serve you seven years for your younger daughter Rachel" (v. 18). He does not negotiate; he offers the maximum. The narrator's summation of those seven years is one of the most moving sentences in Scripture: "So Jacob served seven years for Rachel, and they seemed to him but a few days because of his love for her" (v. 20). Seven years of labor — heavy, real, physical — evaporated in the light of love. This is the Bible's most concise definition of what love does to time and to effort.

The wedding night deception (vv. 21–25) is the chapter's dramatic turning point. Laban gives a feast, and in the darkness of evening, brings Leah (not Rachel) to Jacob. "And in the morning, behold, it was Leah!" (v. 25) — the shock rendered with brilliant narrative compression. The man who fooled his blind father with goat skins and disguise wakes up to find that he himself has been substituted. The deceiver has been deceived, in the very category in which he sinned. Laban's explanation is cool and formulaic: "It is not so done in our place, to give the younger before the firstborn" (v. 26). The irony is exquisite: Jacob, who stole the firstborn's blessing by pretending to be the elder, is now defeated by the custom that the elder must go first.

Jacob serves seven more years for Rachel, and the text quietly notes: "He loved Rachel more than Leah" (v. 30). From the outset, the marital dynamic is asymmetric: two wives, one loved, one not. The Hebrew of verse 31 is stark: "When the LORD saw that Leah was hated (senuah)..." — the word is strong. The NIV renders it "not loved," but the Hebrew is the word for hatred. The contrast was that severe. And God's response to it is one of the most grace-filled acts in this chapter: "He opened her womb, but Rachel was barren" (v. 31).

The naming sequence that follows is the theological center of the chapter. Each of Leah's sons receives a name that is a statement about God's seeing, hearing, and mercy:

Reuben (v. 32): "The LORD has looked upon my affliction (ra'ah be-onyi) — surely now my husband will love me." Ra'ah YHWH — the LORD has seen. The name Re'uven encodes this: ra'ah (to see) + ben (son). God saw what no one else chose to see.

Simeon (v. 33): "Because the LORD has heard (shama) that I am hated, He has given me this son also." The name Shim'on comes from shama — to hear. God heard the unspoken prayer, the silent grief of the unloved wife.

Levi (v. 34): "Now this time my husband will be attached (yilaveh) to me." Levi from lavah — to be joined, to accompany. Leah still hopes for Jacob's love; the name expresses longing more than receipt.

Judah (v. 35): "This time I will praise (odeh) the LORD." The name Yehudah is from yadah — to praise, to give thanks with outstretched hands. Something shifts in Leah with Judah: she stops marking her births by Jacob's response and turns her gratitude directly to God. It is spiritual maturity earned through pain.

Judah is the fourth son, and from his line will come Israel's greatest kings, including David, and ultimately the Messiah (Gen. 49:10; Rev. 5:5). The unloved woman, the wife nobody chose, bears the child through whose line all blessing will come. The chapter does not announce this; it simply records it. But the reader who has followed the whole story knows: God chose the unloved one to carry the most important line. The tribe of Judah — the line of the Lion — begins not in triumph but in tears.""",
        "original_language_notes": [
            {
                "term": "לְבַדּוֹ (levado)",
                "language": "Hebrew",
                "verse": 10,
                "words_used": ["levado"],
                "meaning": "'Alone.' From bad (separation, isolation) + the third-person suffix. The emphasis on Jacob rolling the stone alone — when the shepherds had explained it normally required gathering all the flocks first — highlights the extraordinary effort love motivates. The same root appears in the phrase 'it is not good for man to be alone' (Genesis 2:18), connecting human longing for companionship with remarkable acts of service."
            },
            {
                "term": "רְאוּבֵן (Reuven) — רָאָה בְּעָנְיִי (ra'ah be-onyi)",
                "language": "Hebrew",
                "verse": 32,
                "words_used": ["ra'ah", "be-onyi", "Reuven"],
                "meaning": "'Reuben' encodes 'he has seen my affliction.' Ra'ah = to see (divine observation); onyi = my affliction/humiliation. Leah names her son from the phrase 'the LORD has seen (ra'ah YHWH) my affliction.' The name Re'uven plays on ra'ah + ben (son): 'see, a son!' The theological significance is enormous: God's primary response to Leah's neglect is to see her — divine attention to the overlooked is itself an act of grace."
            },
            {
                "term": "שָׁנוּאָה (senuah)",
                "language": "Hebrew",
                "verse": 31,
                "words_used": ["senuah"],
                "meaning": "'Hated.' Passive participle of sana (to hate), the full antonym of love. While English translations sometimes soften this to 'not loved' or 'unloved,' the Hebrew uses the strongest available word for the opposite of love. The same word appears in Deuteronomy 21:15 in the 'loved wife and hated wife' scenario. God's response to Leah being senuah is to open her womb — divine compassion flowing precisely toward those most rejected by others."
            },
            {
                "term": "יְהוּדָה (Yehudah) — אֹודֶה (odeh)",
                "language": "Hebrew",
                "verse": 35,
                "words_used": ["Yehudah", "odeh"],
                "meaning": "'Judah' and 'I will praise.' Odeh is the cohortative first-person of yadah (to praise, to give thanks with extended hands — also the root of 'to confess'). With Judah, Leah stops framing each birth around Jacob's expected response and turns her praise directly to YHWH. It is a moment of spiritual breakthrough. Yehudah (Judah) contains this praise: God's own name (Yah) embedded in Israel's most important tribe. From Judah comes David, and from David, Jesus."
            },
            {
                "term": "כְּיָמִים אֲחָדִים (ke-yamim achadim)",
                "language": "Hebrew",
                "verse": 20,
                "words_used": ["ke-yamim", "achadim"],
                "meaning": "'Like a few days.' Jacob's seven years of labor for Rachel are described as seeming like yamim achadim (a few days, literally 'several/unified days') in his love for her. The phrase captures love's compression of time and effort. The Septuagint translates it hōsei hēmeras oligas — 'as though a few days.' It is one of the most quoted biblical expressions of what genuine love does to sacrifice: it transforms years into days."
            }
        ],
        "moral_lessons": [
            "Jacob's seven years of labor for Rachel illustrate that genuine love is willing to pay an enormous price without complaint — love transforms sacrifice into joy.",
            "The deceiver Jacob is deceived by Laban in the same category of sin, demonstrating that God's justice is not always external punishment but often the natural return of what we have done.",
            "Leah's naming of her sons reveals a profound theology of suffering: God sees (Reuben), God hears (Simeon), the longing for attachment (Levi), and finally pure praise (Judah).",
            "God's opening of Leah's womb in response to being 'unloved' declares that He takes particular notice of those whom others overlook, reject, or deprive of dignity.",
            "The most important covenant line (Judah → David → Christ) passes through the woman no one wanted, showing that God's purposes operate through the least expected instruments."
        ],
        "application": "Genesis 29 speaks powerfully to those who feel like Leah — seen by no one, chosen by no one, wanted by no one. The chapter's good news is that God saw Leah when Jacob did not. He opened what was closed. He gave names to grief. And He embedded the greatest covenant line in history in the children of the unloved wife. If you have been Leah — marginalized, overlooked, the second choice — notice that your Reuben, your Simeon, your Levi, and your Judah may be waiting to be born. Let praise (odeh) come. And if you have been Jacob — capable of love but prone to treating people as means to your own ends — notice where your own deceptions have returned to you, and receive that justice as an invitation to grow.",
        "prayer": "Lord God, You saw Leah. You see all the Leahs — all who are unloved, overlooked, treated as second-best. You hear the silent grief, the uncried cry, the prayer that is too wounded to form words. Open what has been closed. Give names to the pain. And bring from the unloved the very thing the world needs most — the line of praise, the tribe of Judah, the song that only the broken can sing fully. Help us to love with Jacob's seven-year patience and to praise with Leah's final surrender. In Jesus, the Lion of Judah, Amen.",
        "key_points": [
            "Jacob's solo rolling of the stone for Rachel exemplifies love's capacity to do alone what others require a crowd for — and sets the tone for seven years given freely.",
            "Jacob's seven years feeling like 'a few days' is one of the Bible's most celebrated descriptions of love's transformation of sacrifice into joy.",
            "Laban's substitution of Leah for Rachel returns Jacob's own deception to him — he who deceived with disguise is himself substituted in the darkness.",
            "Laban's rationale ('the older must go before the younger') directly mirrors what Jacob violated in chapter 27, sharpening the irony of the returned deception.",
            "Leah's naming sequence (Reuben, Simeon, Levi, Judah) is a sustained theology of suffering: God sees, God hears, Leah longs to be joined, and finally Leah praises.",
            "The shift at Judah — 'this time I will praise the LORD' — marks spiritual maturity: moving from measuring God's gifts by human acceptance to praising Him directly.",
            "The tribe of Judah, from which David and Christ descend, begins in the womb of the unloved wife — a foundational testimony that God builds His greatest work through the least likely instruments."
        ],
        "study_questions": [
            "Jacob worked seven years for Rachel, and they seemed like 'a few days.' Have you ever experienced love or passion that made a long or difficult commitment feel light? What does this teach about motivation?",
            "Jacob deceived his father with false identity; Laban deceives Jacob with false identity. How does experiencing the return of our own sin shape character and repentance?",
            "Leah names each son in response to her emotional and spiritual state. Trace the arc from Reuben (God saw) to Judah (I will praise). What changed? What produced that change?",
            "God 'saw' Leah's affliction and opened her womb. In your own experience, where have you seen God pay special attention to someone who was being overlooked or rejected by others?",
            "The most important covenant line passes through Leah, not Rachel. What does this pattern (the unloved, the barren, the second-choice being instruments of greatest importance) reveal about how God works?",
            "Leah's longing for Jacob's love is never fully satisfied in this chapter. How do you hold together the reality that God comforts those who suffer with the reality that their earthly suffering is not immediately removed?"
        ],
        "tags": ["Genesis", "Jacob", "Rachel", "Leah", "Laban", "love", "deception", "Judah", "covenant", "twelve tribes"]
    },

    30: {
        "title": "Genesis 30 — The God Who Remembers: Children Born from Rivalry, Providence, and Unlikely Grace",
        "summary": "Rachel's jealousy of Leah's fertility prompts her to give Bilhah to Jacob; Bilhah bears Dan and Naphtali. Leah retaliates by giving Zilpah, who bears Gad and Asher. Leah exchanges mandrakes for a night with Jacob and bears Issachar, Zebulun, and Dinah. God finally 'remembers' Rachel and she conceives, bearing Joseph. Jacob asks Laban to leave; they negotiate wages. Jacob implements a selective breeding strategy with the flocks and becomes very wealthy, at Laban's expense.",
        "chapter_overview": "Rachel, barren and jealous of Leah, gives Bilhah to Jacob as a surrogate. Bilhah bears Dan and Naphtali. Leah, whose fertility had stopped, gives Zilpah, who bears Gad and Asher. Leah trades mandrakes to Rachel for a night with Jacob and conceives Issachar, then Zebulun, then Dinah. God remembers Rachel; she conceives and bears Joseph. Jacob requests to return home; Laban asks him to stay and name his wages. Jacob proposes a deal on speckled/spotted animals. Jacob uses peeled rods and selective breeding to build his flock; Laban's flocks diminish and Jacob's multiply.",
        "content": """Genesis 30 is, on the surface, a chapter of domestic strife, surrogate motherhood, fertility bargaining, and sheep-breeding strategy. But beneath the surface it is a chapter about the sovereignty of God over human reproduction, the naming of the twelve tribes of Israel, and the reminder that what God 'remembers' is never forgotten in the meantime.

Rachel opens the chapter with anguish: "Give me children, or I shall die!" (v. 1). The statement is hyperbolic but reveals real despair. Barrenness in the ancient Near East was social death — the absence of the most fundamental marker of womanhood and survival. Jacob's response is harder than we might expect: "Am I in the place of God, who has withheld from you the fruit of the womb?" (v. 2). Jacob is not being cruel but theologically accurate: fertility belongs to God's domain, not his. He cannot open a closed womb; only God can (as the narrative is about to demonstrate). Yet the statement lacks warmth, and Rachel's pain is real.

The surrogacy arrangement that follows (vv. 3–8) mirrors Sarah's arrangement with Hagar (ch. 16). Rachel gives her maidservant Bilhah to Jacob. The children born to Bilhah will be "born upon Rachel's knees" — a legal formula for adoption. Bilhah bears Dan (v. 6): Rachel says "God has judged me (dananni Elohim) and has also heard my voice and given me a son." Dan comes from din (to judge, to vindicate). The name is an assertion that Rachel's case has been heard in the divine court. Naphtali (v. 8) comes from Rachel's cry "With mighty wrestlings (naftulei Elohim — 'wrestlings of God') I have wrestled with my sister and have prevailed." The word naftulei appears related to pathal (to twist/wrestle) — the same root family that will mark Jacob's wrestling match in chapter 32.

Leah's response — giving her maidservant Zilpah — produces Gad (v. 11, "Good fortune!" from gad or perhaps troupes) and Asher (v. 13, "Happy am I!" from asher, the root of happiness). Leah's naming is exuberant and extroverted: she is celebrating publicly, aware that women are watching.

The mandrake episode (vv. 14–18) is simultaneously strange and touching. Leah's son Reuben finds mandrakes (dudaim) — plants associated in ancient lore with fertility — in the field. Rachel asks for them; Leah's bitter response reveals years of accumulated resentment: "Is it a small matter that you have taken away my husband? Would you take away my son's mandrakes also?" (v. 15). Rachel trades the mandrakes for a night with Jacob — a quiet reversal of power dynamics. Leah uses her trade aggressively: she goes out to meet Jacob and says "You must come in to me, for I have hired you" (v. 16). The language of hire (sachar) is the same root as Issachar's name — and Leah names him accordingly: "God has given me my wages (sachar) because I gave my servant to my husband" (v. 18). The naming is playful and theologically anchored simultaneously.

Zebulun (v. 20) receives a name from two roots: zaval (to honor, to dwell) — "God has endowed me with a good endowment; now my husband will honor/dwell with me." Then Leah bears a daughter, Dinah (v. 21) — named simply, without theological commentary, which becomes significant in chapter 34.

Then comes the pivot of the entire chapter: "Then God remembered Rachel, and God listened to her and opened her womb" (v. 22). The verb zakar — "to remember" — is one of the great covenantal verbs of the Hebrew Bible. When God "remembers," it is not a suggestion that He had forgotten; it is a declaration that He is now acting on what He has always known. He remembered Noah (8:1) and the waters receded. He remembered Abraham and rescued Lot. He will remember Israel in Egypt and send Moses (Ex. 2:24). Divine "remembering" is divine action, not divine recall. Rachel conceives and bears Joseph (v. 24). The name is a double pun: "God has taken away (asaph) my reproach" and "May the LORD add (yosef) to me another son." The name holds both relief and hope simultaneously.

Jacob's departure request (vv. 25–43) opens the final major narrative arc of the Haran episode. He wants to go home with his wives and children. Laban, who has observed how God has blessed him through Jacob's presence ("the LORD has blessed me because of you," v. 27), asks Jacob to name his wages. Jacob proposes to take the speckled, spotted, and dark-colored animals as his wages, with Laban keeping all the pure-colored ones. Laban immediately removes all the speckled animals three days' distance away — trying to rig the outcome.

What follows (vv. 37–43) is Jacob's selective breeding strategy using peeled rods placed in the water troughs during breeding season. Modern readers are puzzled by this — does the technique work scientifically? Probably not by itself. But the text makes clear in chapter 31:10–12 that God shows Jacob in a dream what the rams are doing — the outcome is divine, not merely strategic. Jacob's rods may be his human effort; God's direction of which animals breed is the actual cause. The result: "the man increased greatly and had large flocks, female servants and male servants, and camels and donkeys" (v. 43). The vocabulary of Genesis 12:16 (Abraham's wealth) echoes here — Jacob is becoming a patriarch in his own right.

The naming of the twelve patriarchs (Reuben, Simeon, Levi, Judah, Dan, Naphtali, Gad, Asher, Issachar, Zebulun, Dinah as daughter, and Joseph in ch. 30 — with Benjamin to come in ch. 35) is the quiet structural achievement of chapters 29–30. The twelve nations whose descendants will become Israel are born in this chapter — not in triumph, but in rivalry, longing, bargaining, and grief. God builds the architecture of salvation from the raw materials of human dysfunction.""",
        "original_language_notes": [
            {
                "term": "וַיִּזְכֹּר אֱלֹהִים (va-yizkor Elohim)",
                "language": "Hebrew",
                "verse": 22,
                "words_used": ["va-yizkor", "Elohim"],
                "meaning": "'And God remembered.' Zakar is one of the great covenantal verbs of the Hebrew Bible — not suggesting God forgot, but marking the moment when God's covenantal attention turns to active intervention. God 'remembered' Noah (8:1), Abraham/Lot (19:29), Rachel (30:22), and Israel in Egypt (Ex. 2:24). The verb is followed always by action: the waters recede, the city is spared, the womb opens, the exodus begins. Divine memory is divine movement."
            },
            {
                "term": "יוֹסֵף (Yosef)",
                "language": "Hebrew",
                "verse": 24,
                "words_used": ["Yosef"],
                "meaning": "'Joseph.' A double wordplay: (1) from asaph (to gather, take away) — Rachel says 'God has taken away (asaph) my reproach'; (2) from yasaf (to add, increase) — 'may the LORD add (yosef) another son to me.' The name encodes both relief from shame and hope for more. The two roots are different (alef vs. yod), but the name bridges both. Joseph's story in chapters 37–50 fulfills both dimensions: his shame is taken away and his family is multiplied."
            },
            {
                "term": "דּוּדָאִים (dudaim)",
                "language": "Hebrew",
                "verse": 14,
                "words_used": ["dudaim"],
                "meaning": "'Mandrakes.' The plant (Mandragora officinarum) was associated in ancient Near Eastern culture with fertility and love-magic. The word may be related to dod (beloved, love — also root of David). Mandrakes appear in Song of Solomon 7:13 as a symbol of desire. Rachel's bargaining for them reflects the desperation of barrenness. The irony is that Rachel trades the mandrakes but remains barren until v. 22 when God directly intervenes — the mandrakes do nothing; God does everything."
            },
            {
                "term": "נַפְתּוּלֵי אֱלֹהִים (naftulei Elohim)",
                "language": "Hebrew",
                "verse": 8,
                "words_used": ["naftulei", "Elohim"],
                "meaning": "'Mighty wrestlings' or 'wrestlings of God.' From pathal (to twist, to wrestle). The Hebrew intensifies human activity by using Elohim as a superlative — 'God-wrestlings' = supreme, intense wrestlings. Rachel understands her rivalry with Leah in cosmic terms. The same wrestling root appears in the Jacob-at-Peniel narrative (ch. 32), where 'Israel' is given because Jacob wrestled with God. Rachel's naming of Naphtali anticipates the defining spiritual crisis of Jacob's own life."
            },
            {
                "term": "שָׂכַר (sachar)",
                "language": "Hebrew",
                "verse": 18,
                "words_used": ["sachar"],
                "meaning": "'Wages / hire.' Leah names Issachar from this root: 'God has given me my wages (sachar) because I gave my servant to my husband.' The same root appears in v. 16 ('I have hired you') and anticipates Jacob's wage-negotiations with Laban in vv. 28–34. The entire second half of the chapter is structured around sachar — wages, what is earned, what is owed, what God gives as the ultimate provider. The economics of the chapter are theological."
            }
        ],
        "moral_lessons": [
            "Rachel's 'Give me children or I shall die' reveals that desperate longing, even from those who have much (she has Jacob's love), is not incompatible with faith — but it needs to be directed toward God, not toward Jacob.",
            "God's 'remembering' of Rachel teaches that the absence of God's immediate answer is not the absence of God's attention — His silence is not His forgetting.",
            "The surrogate-child competition between Rachel and Leah shows how rivalry distorts the gift: children become weapons in a competition rather than blessings received with gratitude.",
            "Leah's naming arc culminates in praise (Judah, ch. 29) and continues with economic metaphors (Issachar as wages, Zebulun as endowment) — her theology is earthy and honest.",
            "Jacob's flocks multiply not because of his rods but because of God's direction (as confirmed in 31:10–12) — human strategy and divine sovereignty are not competitors but partners, with sovereignty always primary."
        ],
        "application": "Genesis 30 challenges two errors simultaneously. The first is Rachel's error: demanding from a spouse what only God can give, and trading spiritual means (mandrakes) for things only divine action can produce. If you are in a season of barrenness — relational, spiritual, professional — the chapter's answer is not strategy, surrogacy, or mandrakes, but the God who remembers. The second error is Jacob's: believing his rod-strategy caused the outcome he needed. God revealed in a dream (31:10–12) that the breeding results were His, not Jacob's rods'. Our wisdom and effort matter — God uses them — but the outcomes belong to Him. Hold your strategies loosely; cling to the One who remembers.",
        "prayer": "Lord, You are the God who remembers. When we cry 'Give me what I need or I shall die,' remind us that You have heard us all along. Open what You have determined to open in Your time and Your way. Where we have tried to force Your hand with mandrakes — our own fertility strategies — forgive us and turn us back to simple trust. Let us name our children and our blessings after You: You have seen, You have heard, You have judged in my favor, I will praise You. Build Your purposes through our broken, competitive, ordinary households, just as You did in Haran. In Jesus' name, Amen.",
        "key_points": [
            "Rachel's 'Give me children or I shall die' and Jacob's response establish that fertility belongs to God's domain — a theological framework the rest of the chapter confirms.",
            "The surrogate births (Bilhah's Dan and Naphtali; Zilpah's Gad and Asher) complete the twelve tribal ancestral lines, all born from the messy combination of rivalry and longing.",
            "The mandrake episode reveals the futility of human fertility strategies: Rachel gets the mandrakes, Leah gets the pregnancy — God's sovereign action overrides the folk remedy.",
            "God 'remembering' Rachel (v. 22) is the covenantal pivot: divine zakar is always followed by divine action, not mere thought — He opens her womb.",
            "Joseph's double-meaning name (God has taken away my reproach / may He add another son) encodes both relief and future hope — a name that his story in chapters 37–50 will fully unpack.",
            "Jacob's breeding strategy is confirmed in chapter 31 to be divinely directed (God showed Jacob what to do in a dream), establishing that his prosperity is God's gift, not human cleverness.",
            "The twelve sons of Israel are fully named in chapters 29–30 (with Benjamin in ch. 35) — their origins in rivalry, love, grief, and divine remembering form the theological DNA of the nation."
        ],
        "study_questions": [
            "Rachel says 'Give me children or I shall die!' Jacob responds that he is not in God's place. Both are right in different ways. How do you hold together the honesty of expressing desperate need with the theology that only God can meet it?",
            "The mandrakes go to Rachel, but Leah gets pregnant. What does this reversal teach about the relationship between human strategies for receiving God's blessings and the actual source of those blessings?",
            "God 'remembered' Rachel after years of barrenness. What does it mean to trust in a God who 'remembers' — who has not forgotten you even in long seasons of unanswered prayer?",
            "Trace the naming of the sons (Reuben through Judah, Dan, Naphtali, Gad, Asher, Issachar, Zebulun, Joseph). What theology of God's character emerges from the cumulative meaning of all these names?",
            "Jacob believed his rod strategy was producing results; God reveals in 31:10–12 that He was directing it. In what areas of your life might you be crediting your own strategy for what God is actually doing?",
            "The twelve tribal ancestors are born in the middle of domestic competition, favoritism, and rivalry. What does this origin story suggest about the kind of material God is willing to work with to build His people?"
        ],
        "tags": ["Genesis", "Rachel", "Leah", "Jacob", "Joseph", "twelve tribes", "barrenness", "sovereignty", "remembrance", "providence"]
    }
}

def main():
    conn = sqlite3.connect(str(DB))
    conn.execute('PRAGMA foreign_keys=ON')
    cur = conn.cursor()

    # Get or create author
    row = cur.execute(
        "SELECT id FROM commentary_authors WHERE display_name=? AND author_type='ai' AND deleted_at IS NULL",
        ('Believers Sword AI Commentary Writer',)
    ).fetchone()
    if row:
        author_id = row[0]
    else:
        t = now()
        cur.execute(
            "INSERT INTO commentary_authors (uuid,display_name,author_type,biography,language_code,created_at,updated_at) VALUES (?,?,?,?,?,?,?)",
            (str(uuid.uuid4()), 'Believers Sword AI Commentary Writer', 'ai',
             'AI-assisted evangelical commentary prepared for offline-first Believers Sword study.', LANG, t, t)
        )
        author_id = cur.lastrowid

    # Get or create collection
    row = cur.execute(
        "SELECT id FROM commentary_collections WHERE slug=? AND language_code=? AND deleted_at IS NULL",
        (COLLECTION_SLUG, LANG)
    ).fetchone()
    if row:
        collection_id = row[0]
    else:
        t = now()
        cur.execute(
            """INSERT INTO commentary_collections
               (uuid,name,slug,description,collection_type,primary_author_id,language_code,theological_perspective,license,copyright_notice,is_offline_available,created_at,updated_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (str(uuid.uuid4()), COLLECTION_NAME, COLLECTION_SLUG,
             'Practical, reverent, evangelical Christian chapter commentaries for Believers Sword offline study.',
             'ai_generated', author_id, LANG, THEOLOGY, 'All rights reserved for project use.',
             'Generated for Believers Sword.', 1, t, t)
        )
        collection_id = cur.lastrowid

    # Create generation batch
    batch_uuid_str = str(uuid.uuid4())
    t = now()
    cur.execute(
        """INSERT INTO commentary_generation_batches
           (uuid,collection_id,batch_name,generator_type,model_name,model_provider,prompt_version,generation_parameters,language_code,started_at,status,created_at,updated_at)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (batch_uuid_str, collection_id, f'Genesis 26-30 batch {t}', 'ai',
         'claude-sonnet-4-6', 'anthropic', 'believers-sword-commentary-v2',
         json.dumps({'chapters_per_run': 5}), LANG, t, 'draft', t, t)
    )
    batch_id = cur.lastrowid

    BOOK_ID = 1
    BOOK = 'Genesis'
    book_slug = slug(BOOK)
    gen_dir = GENERATED / f'{BOOK_ID:02d}-{book_slug}'
    gen_dir.mkdir(parents=True, exist_ok=True)

    generated = 0
    skipped = 0
    rows_inserted = 0
    files_written = 0
    errors = []
    covered_chapters = []

    for chapter in [26, 27, 28, 29, 30]:
        # Check if already exists with non-shallow content
        existing = cur.execute(
            """SELECT id, content FROM commentary_entries
               WHERE collection_id=? AND book_id=? AND chapter=?
               AND language_code=? AND reference_scope='chapter' AND deleted_at IS NULL""",
            (collection_id, BOOK_ID, chapter, LANG)
        ).fetchone()

        if existing:
            content_len = len(existing[1]) if existing[1] else 0
            if content_len > 500:
                print(f"Skipping Genesis {chapter} — already exists (content length: {content_len})")
                skipped += 1
                covered_chapters.append(chapter)
                continue

        data = COMMENTARIES[chapter]
        entry_uuid = str(uuid.uuid4())
        t = now()

        key_points_json = json.dumps(data['key_points'], ensure_ascii=False)
        study_questions_json = json.dumps(data['study_questions'], ensure_ascii=False)
        word_count = len((data['content'] + ' ' + data['application'] + ' ' + data['prayer']).split())

        try:
            cur.execute(
                """INSERT INTO commentary_entries
                   (uuid,collection_id,author_id,generation_batch_id,book_id,chapter,
                    verse_start,verse_end,reference_scope,title,summary,content,
                    application,prayer,key_points,study_questions,language_code,
                    theological_perspective,status,is_ai_generated,ai_model_name,
                    ai_model_provider,ai_prompt_version,ai_generation_batch_uuid,
                    ai_confidence,word_count,created_at,updated_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (entry_uuid, collection_id, author_id, batch_id, BOOK_ID, chapter,
                 None, None, 'chapter', data['title'], data['summary'], data['content'],
                 data['application'], data['prayer'], key_points_json, study_questions_json,
                 LANG, THEOLOGY, 'draft', 1, 'claude-sonnet-4-6', 'anthropic',
                 'believers-sword-commentary-v2', batch_uuid_str, 0.95, word_count, t, t)
            )
            rows_inserted += 1
        except Exception as e:
            errors.append(f'DB insert Genesis {chapter}: {e}')
            print(f'ERROR inserting Genesis {chapter}: {e}')
            continue

        # Write backup JSON (no forbidden keys)
        backup = {
            'uuid': entry_uuid,
            'collection_name': COLLECTION_NAME,
            'author_type': 'ai',
            'language_code': LANG,
            'theological_perspective': THEOLOGY,
            'status': 'draft',
            'book_id': BOOK_ID,
            'book': BOOK,
            'chapter': chapter,
            'title': data['title'],
            'summary': data['summary'],
            'content': data['content'],
            'chapter_overview': data['chapter_overview'],
            'original_language_notes': data['original_language_notes'],
            'moral_lessons': data['moral_lessons'],
            'application': data['application'],
            'prayer': data['prayer'],
            'key_points': data['key_points'],
            'study_questions': data['study_questions'],
            'tags': data['tags'],
            'sources': [],
            'created_at': t,
            'updated_at': t,
        }

        # Verify no forbidden keys
        forbidden = {'is_ai_generated', 'model_name', 'prompt_version'}
        assert not forbidden.intersection(backup.keys()), f"Forbidden keys found: {forbidden.intersection(backup.keys())}"

        json_path = gen_dir / f'{chapter:02d}.json'
        json_path.write_text(json.dumps(backup, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

        # Verify it parses
        parsed = json.loads(json_path.read_text(encoding='utf-8'))
        assert not forbidden.intersection(parsed.keys()), "Forbidden keys in written JSON"

        files_written += 1
        generated += 1
        covered_chapters.append(chapter)
        print(f"Generated Genesis {chapter}: {data['title'][:60]}...")

    # Update progress
    next_chapter = 31
    next_book_id = 1
    t = now()

    progress_data = {
        'next_book_id': next_book_id,
        'next_book': BOOK,
        'next_chapter': next_chapter,
        'last_completed_book_id': BOOK_ID,
        'last_completed_book': BOOK,
        'last_completed_chapter': 30,
        'completed': False,
        'updated_at': t
    }
    PROGRESS_JSON.write_text(json.dumps(progress_data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    # Update DB progress
    prog_row = cur.execute(
        "SELECT id FROM commentary_generation_progress WHERE collection_id=? AND language_code=? AND deleted_at IS NULL",
        (collection_id, LANG)
    ).fetchone()
    if prog_row:
        cur.execute(
            """UPDATE commentary_generation_progress
               SET current_book_id=?, current_chapter=?, last_completed_book_id=?, last_completed_chapter=?,
                   target_book_id=66, target_chapter=22, chapters_per_batch=5,
                   generation_batch_id=?, updated_at=?
               WHERE id=?""",
            (next_book_id, next_chapter, BOOK_ID, 30, batch_id, t, prog_row[0])
        )
    else:
        cur.execute(
            """INSERT INTO commentary_generation_progress
               (uuid,collection_id,language_code,current_book_id,current_chapter,
                last_completed_book_id,last_completed_chapter,target_book_id,target_chapter,
                chapters_per_batch,status,generation_batch_id,created_at,updated_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (str(uuid.uuid4()), collection_id, LANG, next_book_id, next_chapter,
             BOOK_ID, 30, 66, 22, 5, 'draft', batch_id, t, t)
        )

    cur.execute(
        "UPDATE commentary_generation_batches SET completed_at=?, status=?, updated_at=? WHERE id=?",
        (t, 'draft', t, batch_id)
    )

    conn.commit()
    conn.close()

    # Write log
    log = {
        'timestamp': t,
        'generation_batch_id': batch_uuid_str,
        'start_reference': 'Genesis 26',
        'end_reference': 'Genesis 30',
        'chapters_generated': generated,
        'chapters_skipped': skipped,
        'db_rows_inserted': rows_inserted,
        'files_written': files_written,
        'errors': errors
    }
    with LOG.open('a', encoding='utf-8') as f:
        f.write(json.dumps(log, ensure_ascii=False) + '\n')

    print('\n=== RESULT ===')
    result = {
        'generated_range': 'Genesis 26–30',
        'chapters_generated': generated,
        'chapters_skipped': skipped,
        'db_rows_inserted': rows_inserted,
        'files_written': files_written,
        'next_starting_reference': f'{BOOK} {next_chapter}',
        'errors': errors
    }
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
