import os, sys, json, time, requests, re
import config

# Pre-crafted master curriculum for The Dionysian Abyss channel
NIETZSCHE_CURRICULUM = [
    {
        "id": "ep_1",
        "topic": "Friedrich Nietzsche on the Nature of Women, Love, and the Mask of Truth",
        "focus": "A profound philosophical exploration into Nietzsche's provocative aphorisms on the psychology of the sexes, the illusion of romantic possession, the pathos of distance, and why he declared that truth itself is a woman.",
        "thumbnail_title_1": "THE ENIGMA OF WOMAN",
        "thumbnail_title_2": "TRUTH & DESIRE",
        "thumbnail_hook": "Why Truth Refuses to be Possessed",
        "acts": [
            ("Act 1: Supposing Truth is a Woman — The Philosophy of the Mask", "Unpacking the preface to Beyond Good and Evil, the nature of dogmatism, and the art of veiling."),
            ("Act 2: The Will to Power in Love — Possession vs. Devotion", "Romantic passion as the instinct of possession, the illusion of selflessness, and the longing for an equal adversary."),
            ("Act 3: Nature, Sentimentality, and Modern Illusions", "Nietzsche's critique of domestic pacification, superficial equality, and the loss of instinctual tension."),
            ("Act 4: The Pathos of Distance — The Sacred Tension of the Sexes", "Zarathustra's riddles, why intimacy without distance breeds contempt, and the necessity of danger and play."),
            ("Act 5: Amor Fati — Embracing the Untamed Will", "Transcending resentment, accepting the tragic beauty of human nature, and loving fate as it is.")
        ]
    },
    {
        "id": "ep_2",
        "topic": "The Psychology of Resentment: How the Weak Conquered the Strong",
        "focus": "An inquiry into Nietzsche's Genealogy of Morals, slave morality, and the subterranean poison of ressentiment.",
        "thumbnail_title_1": "THE HIDDEN POISON",
        "thumbnail_title_2": "OF RESENTMENT",
        "thumbnail_hook": "How Envy Became Morality",
        "acts": [
            ("Act 1: The Birth of Master and Slave Morality", "Noble values versus reactive morality."),
            ("Act 2: The Subterranean Venom of Ressentiment", "How repressed vengeance mutates into virtue."),
            ("Act 3: The Ascetic Ideal and Guilt", "The fabrication of conscience and self-punishment."),
            ("Act 4: The Modern Herd", "The triumph of comfort over greatness."),
            ("Act 5: The Antidote: Sovereign Individuality", "Forging an aristocratic spirit beyond herd affirmation.")
        ]
    },
    {
        "id": "ep_3",
        "topic": "Amor Fati and The Eternal Return: The Ultimate Test of Greatness",
        "focus": "The heaviest burden of Nietzsche's thought: living a life you would wish to repeat an infinite number of times.",
        "thumbnail_title_1": "THE GREATEST WEIGHT",
        "thumbnail_title_2": "THE ETERNAL RETURN",
        "thumbnail_hook": "Could You Relive Your Life Forever?",
        "acts": [
            ("Act 1: The Demon in the Loneliest Loneliness", "The thought experiment that shatters mediocrity."),
            ("Act 2: Beyond Regret and Remorse", "Why wishing away your suffering destroys your strength."),
            ("Act 3: Amor Fati: Loving Fate Unconditionally", "The tragic affirmative joy of the Dionysian."),
            ("Act 4: The Cycle of Time", "Cosmic recurrence and the sanctity of the present moment."),
            ("Act 5: The Heroic Affirmation of Existence", "Singing yes to all of life.")
        ]
    }
]

# Master 20-minute spoken script for Episode 1
EPISODE_1_SCRIPT = [
    # --- ACT 1: Supposing Truth is a Woman ---
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Welcome into the quiet depths of The Dionysian Abyss. Today, we step beyond the comforting shores of conventional morality and enter one of the most provocative, misunderstood, and psychologically piercing corridors of Friedrich Nietzsche's philosophy. We turn our gaze toward a question that haunted his ink: the nature of women, the psychology of love, and the profound metaphor of truth as a veiled mystery."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "In the opening words of his 1886 masterpiece, Beyond Good and Evil, Nietzsche strikes the intellectual world with an electrifying aphorism. He writes: 'Supposing truth is a woman — what then? Is there not ground for suspecting that all philosophers, in so far as they have been dogmatists, have understood women badly? That the gruesome seriousness, the clumsy importunity with which they have hitherto been in the habit of approaching truth, have been inept and improper means for winning a woman?'"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Consider the audacity of this image. For centuries, Western thought had treated truth as an object — a stone to be unearthed, a mathematical formula to be grasped, or a logical fortress to be conquered through blunt force and pedantic certainty. The dogmatic philosopher marched toward truth like an unrefined suitor, demanding that she surrender her secrets unconditionally, without subtlety, without modesty, and without charm."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "And what was the result? She never let herself be caught. Truth recoiled from their clumsy advances. To Nietzsche, truth is not a dry proposition sitting in an academic classroom; truth possesses the living, elusive, and capricious nature of feminine psychology. Truth loves the mask. Truth demands reverence for the surface, for distance, for irony, and for the veil."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "In the preface to The Gay Science, Nietzsche reflects on the ancient Greeks, whom he admired above all other peoples. He observes that the Greeks were superficial — out of profundity. They knew when to stop boldly at the surface, at the fold, at the skin, to adore appearance, to believe in forms, tones, words, in the whole Olympus of appearance. Those Greeks were superficial out of sheer depth."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Nietzsche asks us: Is not truth precisely like a woman who has reasons not to let us see her reasons? Perhaps her very name is Baubo, the mythical figure of shameless concealment. When we attempt to strip away every illusion in search of naked certainty, we do not discover wisdom; we destroy the very enchantment that makes life possible. To understand women, as to understand truth, one must master the art of the veil."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Modern culture often prides itself on radical transparency, on tearing down all formality and unmasking every sentiment until only anatomical facts and sociological data remain. But Nietzsche cautions us that when everything is exposed under the harsh fluorescent light of utilitarian scrutiny, beauty withers. Mystery is not an error to be corrected; mystery is the fertile soil from which genuine passion and philosophical depth spring."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "In aphorism sixty of The Gay Science, Nietzsche writes poetically about the magic of woman as an action at a distance: 'The magic and the most powerful effect of women is, to speak the language of the philosophers, an effect at a distance, an actio in distans: but this requires first of all and above all — distance!' When we stand upon a rocky cliff by the tempestuous ocean and watch a solitary sailboat glide peacefully across the foam, we imagine that aboard that ship dwells tranquility and silent grace. Yet aboard the ship, there is noise, creaking wood, and exhausting labor. The enchantment belongs entirely to the distance from which we behold it."
    },

    # --- ACT 2: The Will to Power in Love ---
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "We now descend deeper, into the turbulent waters of romance and desire. What is love, when viewed through the unsparing lens of the Will to Power? In aphorism fourteen of The Gay Science, Nietzsche delivers a critique of romantic love that strips away the romantic poetry of his contemporaries and exposes the instinctual machinery beneath."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Nietzsche writes: 'Our love of our neighbor — is it not a craving for new property? And likewise our love of knowledge, of truth, and in general any desire for novelties? We gradually become tired of the old, of what is safely possessed, and we stretch out our hands again; even the most beautiful landscape in which we have lived for three months is no longer certain of our love, and some distant coast attracts our greed.'"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "He continues: 'The possessor grows weary of what he owns. Even the greatest gift of another human being can become familiar and stale. What we call romantic love is at bottom the most unrestrained thirst for possession. The lover wants unconditional, sole possession of the person longed for. He wants equally unconditional power over her soul as over her body; he wants to be loved alone, and to dwell and reign in the other soul as the highest and most desirable of all things.'"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Notice how radically this overturns the popular delusion that romantic love is an act of self-sacrifice or unselfish altruism. To Nietzsche, love in its raw psychological reality is the purest expression of the impulse to conquer. The lover wishes to exclude the whole world from a precious domain. He becomes a dragon guarding his hoard, vigilant, jealous, and demanding."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Yet, Nietzsche does not condemn this drive as evil. Unlike the moralist who recoils in horror at human selfishness, Nietzsche recognizes that every vital force in nature is driven by the desire to expand, to master, and to incorporate. What he warns against is the hypocrisy of calling this possessive hunger holy or unselfish."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Is there, then, any love that transcends mere ownership? Nietzsche concedes that on the rarest occasions, two beings may arrive at a love where possession is transformed into a mutual, shared elevation — a shared thirst for a higher ideal that stands above them both. But he calls this love by its ancient name: friendship. For Nietzsche, profound friendship between two equal, sovereign souls is far rarer and nobler than the blinding frenzy of sexual infatuation."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "In Human, All Too Human, he offers this piercing criterion for marriage: 'When entering into a marriage, one ought to ask oneself the question: do you believe you are going to enjoy talking with this woman into your old age? Everything else in marriage is transitory, but most of the time you are together will be devoted to conversation.' How few romances survive the test of shared silence and intellectual dialogue."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Nietzsche draws a sharp psychological line between two types of desire: the impoverished love that seeks to fill an internal void, and the overflowing love that springs from abundance. The impoverished soul clings to the beloved out of fear, turning the partner into a domestic possession or emotional crutch. But the sovereign soul, rich in inner strength, loves as the sun shines — not because it seeks warmth from the earth, but because it has an excess of radiant energy that must be bestowed upon the world."
    },

    # --- ACT 3: Nature, Sentimentality, and Modern Illusions ---
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "We arrive now at what is undeniably the most controversial aspect of Nietzsche's writings: his fiery polemic against the modern egalitarian view of the sexes. In Beyond Good and Evil, in the chapter titled 'Our Virtues,' Nietzsche observed the beginnings of European feminist movements with grave skepticism. To comprehend his stance without prejudice, we must understand the fundamental premises of his philosophy of nature."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Nietzsche believed that life is fundamentally hierarchical, dynamic, and characterized by tension between opposing forces. Just as electricity requires positive and negative poles to generate a current, human culture and erotic vitality require distinct, complementary polarities. When modern ideology demands that men and women become identical in psychology, ambitions, and temperament, it does not elevate them; it neutralizes the voltage of existence."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "He argued that the true power of woman historically lay not in imitation of masculine traits, but in her unique psychological mastery, her command of subtleties, her aesthetic intuition, and her sovereignty over emotional life. When woman is taught to abandon her distinct domain in order to compete in the bureaucratic arena of the modern state, Nietzsche claimed she surrenders her most formidable weapons."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "He wrote: 'To be mistaken in the fundamental problem of man and woman, to deny here the profoundest antagonism and the necessity for an eternally hostile tension, to dream perhaps of equal rights, equal education, equal claims and obligations: that is a typical sign of shallow-mindedness.' For Nietzsche, equality is the creed of the herd, an instinct born of fatigue and the desire for frictionless ease."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "He feared that modern democracy was producing the 'Last Man' — the creature of comfort who seeks only warmth, harmlessness, and mutual safety, boasting that 'we have invented happiness,' while blinking blankly at the abyss. In such a society, relationships degenerate into contractual business partnerships or cohabitation based on mutual coddling, where no one challenges the other to greatness or bears the magnificent suffering of passion."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Nietzsche observed that nature is neither sentimental nor fair. Nature does not care for our moral abstractions or democratic declarations. Nature operates by eternal laws of generation, struggle, instinct, and creative differentiation. When we pretend that biology and psychology can be rewritten by committee, we do not liberate human nature; we alienate it from its primal roots."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Modern psychology frequently treats conflict as pathology, promising therapeutic techniques to eradicate all friction and doubt. Yet Nietzsche reminds us that human character is not forged in a greenhouse of unconditional affirmation. The great oaks and cedars of the soul grow strong only because they have withstood the howling winds of the mountaintops. When we sanitize relationships of all productive struggle and primal tension, we produce not peace, but emotional atrophy."
    },

    # --- ACT 4: The Pathos of Distance ---
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "In his prophetic poetic work, Thus Spoke Zarathustra, Nietzsche speaks through the voice of the solitary wanderer. In the chapter 'On Little Old and Young Women,' Zarathustra shares riddles that have puzzled commentators for over a century. He proclaims: 'Everything in woman is a riddle, and everything in woman hath one solution: it is called pregnancy. For the woman, the man is a means: the end is always the child. But what is the woman for the man?'"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Zarathustra answers with words that shock the conventional ear: 'Two different things wanteth the true man: danger and play. Therefore wanteth he woman, as the most dangerous plaything.' Let us not commit the vulgar error of interpreting this metaphor as trivial amusement. When Nietzsche speaks of 'play,' he invokes the solemn, perilous play of the artist, the warrior, and the philosopher dancing upon the edge of a precipice."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Danger and play are the exact antithesis of domestic security and bureaucratic routine. To enter into a relationship with a woman of profound depth is to invite an elemental force into one's life — a force that cannot be domesticized without losing its majesty. The genuine man seeks in woman a counterpart who refuses to be subdued, who keeps him vigilant, who challenges his vanity, and who reminds him of the untamed wilderness of existence."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "This brings us to Nietzsche's concept of the 'pathos of distance' — the aristocratic feeling of difference, the preservation of personal sovereignty, and the refusal to blur boundaries. Familiarity, when unmediated by respect, breeds contempt. When two lovers demand total transparency, when they eradicate every boundary in the name of emotional intimacy, the magnetic attraction inevitably collapses."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Nietzsche understood that desire feeds upon the unsaid, upon the territory yet unconquered, upon the secret garden of the soul that can never be fully mapped. The tragedy of modern romance is that it confuses closeness with possession. In wanting to know everything, modern lovers destroy the horizon that inspired them to voyage across the sea in the first place."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "As Zarathustra remarks: 'Let your love be your honor! Little else understandeth woman of honor. But let this be your honor: always to love more than ye are loved, and never to be the second.' To love without demanding an exact accounting of affection, to bestow greatness from one's own abundance rather than begging for affirmation — this is the noble ideal."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "In Nietzsche's mythic imagination, the ultimate union is not a bourgeois contract, but the cosmic dance between Dionysus, the god of overflowing creative chaos, and Ariadne, the labyrinthine soul who holds the golden thread. To enter the labyrinth of another human heart requires courage, for at its center lies not comforting answers, but the Minotaur of our own deepest fears and instincts. Only the dancer who knows how to move lightly with gravity can navigate the labyrinth without losing his soul."
    },

    # --- ACT 5: Amor Fati — Embracing the Untamed Will ---
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "As we draw toward the culmination of our meditation, we must ask: What is the ultimate lesson of Nietzsche's reflections for the seeker of wisdom today? Why did this lonely, sickly philosopher in the Swiss Alps, who never married and whose heart was shattered by Lou Andreas-Salomé, write so intensely about the interplay between man, woman, and truth?"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "The answer lies at the very summit of Nietzsche's mature philosophy: the principle of Amor Fati — the love of fate. Nietzsche did not construct a philosophy of bitter grievance or cynical withdrawal. Despite his immense physical agony, his crushing solitude, and the rejection he experienced from the women he admired, he refused to poison his spirit with ressentiment."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "In Ecce Homo, he writes: 'My formula for greatness in a human being is Amor Fati: that one wants nothing to be different, not forward, not backward, not in all eternity. Not merely bear what is necessary, still less conceal it — all idealism is mendacity in the face of what is necessary — but love it.' To love reality not only in its gentle and comforting moments, but in its cruel, incomprehensible, and ecstatic wildness."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "When we apply Amor Fati to human relationships, it demands that we abandon our childish demands for a frictionless paradise. The tension between the masculine and feminine, the heartache of unrequited longing, the friction of incompatible wills, and the tragic gulf between two subjective souls are not defects of the universe. They are the very canvas upon which the beauty and heroic depth of life are painted."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "To look upon woman, upon love, and upon human nature without the rose-tinted glasses of sentimental morality, and yet still pronounce a resounding 'Yes' — this is the highest mark of the Dionysian spirit. The weak person encounters complexity and demands that it be simplified into safe moral dogmas. The strong person gazes into the chaotic abyss, welcomes the riddle, and finds in the struggle the very reason to sing."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Remember the words of Zarathustra: 'Man is a rope, tied between beast and Overman — a rope over an abyss. A dangerous across, a dangerous on-the-way, a dangerous looking-back, a dangerous trembling and stopping. What is great in man is that he is a bridge and not an end.' In love as in philosophy, we are not meant to remain stagnant; we are called to overcome ourselves."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "To live as a free spirit means to renounce the comfort of easy answers. It means refusing to blame the world, refusing to blame the opposite sex, and refusing to harbor rancor against fate. The noble spirit takes full responsibility for his interpretation of reality. If life is a tragic riddle, then let us be worthy of the riddle. Let us greet each morning with the fiery resolve of Zarathustra, who declared: 'Was that life? Well then! Once more!'"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Treat truth with the elegance and discretion she deserves. Do not rush to tear the veil from the sacred. Cultivate in yourself the courage to bear distance, the strength to love without subjugation, and the wisdom to embrace the eternal riddle of human nature. For only those who have dared to walk along the edge of the abyss can truly behold the magnificence of the stars."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Thank you for walking this path of deep contemplation with us in The Dionysian Abyss. If these timeless reflections have stirred your mind, honor the journey: subscribe to our channel, share your thoughts in the comments below, and carry the torch of philosophical courage into your life. Until our next descent — Amor Fati."
    }
]

def load_history_topics() -> list:
    past = []
    for fname in ["published_videos.json", "history.json"]:
        fpath = os.path.join(config.BASE_DIR, fname)
        if os.path.exists(fpath):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict) and item.get("topic"):
                                t = item["topic"].strip()
                                if t not in past:
                                    past.append(t)
            except Exception:
                pass
    return past

def generate_full_podcast_story(target_minutes: float = 20.0, topic: str = None, ep_num: int = 1) -> dict:
    """Generates the full story dialogue and chapter structure for the episode."""
    print(f"[StoryGenerator] Preparing script for Episode #{ep_num} (Target: {target_minutes:.1f} mins)...")

    # If Episode 1 or matching Nietzsche Women/Nature theme
    if ep_num == 1 or not topic:
        catalog_item = NIETZSCHE_CURRICULUM[0]
        dialogue = EPISODE_1_SCRIPT
    else:
        # Check if topic matches other catalog items
        match = next((item for item in NIETZSCHE_CURRICULUM if item["id"] == f"ep_{ep_num}"), None)
        if match:
            catalog_item = match
            dialogue = EPISODE_1_SCRIPT
        else:
            catalog_item = NIETZSCHE_CURRICULUM[0]
            dialogue = EPISODE_1_SCRIPT

    # Map chapters to dialogue turns
    total_turns = len(dialogue)
    turns_per_act = max(1, total_turns // 5)
    chapters = []
    for act_idx, act_info in enumerate(catalog_item["acts"]):
        start_turn = min(act_idx * turns_per_act, total_turns - 1)
        chapters.append({
            "act": act_idx + 1,
            "title": act_info[0],
            "description": act_info[1],
            "start_turn": start_turn,
            "start_time": 0.0
        })

    total_words = sum(len(t["text"].split()) for t in dialogue)
    print(f"[StoryGenerator] Dialogue assembled: {len(dialogue)} turns, {total_words} words.")
    est_duration_mins = (total_words / 130.0) + (len(dialogue) * config.PAUSE_BETWEEN_TURNS / 60.0)
    print(f"[StoryGenerator] Estimated spoken duration: ~{est_duration_mins:.1f} minutes.")

    return {
        "episode": ep_num,
        "topic": catalog_item["topic"],
        "focus": catalog_item["focus"],
        "thumbnail_title_1": catalog_item["thumbnail_title_1"],
        "thumbnail_title_2": catalog_item["thumbnail_title_2"],
        "thumbnail_hook": catalog_item["thumbnail_hook"],
        "chapters": chapters,
        "dialogue": dialogue
    }

def generate_metadata(topic: str, total_duration_sec: float, chapters: list, ep_num: int = 1) -> dict:
    """Formats YouTube title, timestamps description, tags, and metadata."""
    title = f"Friedrich Nietzsche on the Nature of Women, Love, and Truth | Full 20-Min Documentary (Ep. {ep_num:02d})"

    desc_lines = [
        f"Friedrich Nietzsche's most provocative and profound inquiry into the psychology of human nature, romantic desire, the enigma of women, and the philosophy of the veil.",
        "",
        "\"Supposing truth is a woman — what then? Is there not ground for suspecting that all philosophers have understood women badly?\"",
        " — Friedrich Nietzsche, Beyond Good and Evil (1886)",
        "",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "TIMESTAMPS & CHAPTERS:",
    ]

    for ch in chapters:
        sec = int(ch.get("start_time", 0.0))
        mm = sec // 60
        ss = sec % 60
        desc_lines.append(f"{mm:02d}:{ss:02d} - {ch['title']}")

    desc_lines.extend([
        "",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "ABOUT THE DIONYSIAN ABYSS:",
        "The Dionysian Abyss is a sanctuary of deep philosophical contemplation, intellectual courage, and psychological unmasking. We explore the timeless ideas of Friedrich Nietzsche, ancient Stoicism, existentialism, and the untamed will of human nature.",
        "",
        "Subscribe to join our philosophical circle: @TheDionysianAbyss",
        "",
        "RECOMMENDED NIETZSCHE READING:",
        "• Beyond Good and Evil (Prelude to a Philosophy of the Future)",
        "• The Gay Science (La Gaya Scienza)",
        "• Thus Spoke Zarathustra (A Book for All and None)",
        "• Human, All Too Human (A Book for Free Spirits)",
        "• Ecce Homo: How One Becomes What One Is",
        "",
        "#Nietzsche #Philosophy #HumanNature #BeyondGoodAndEvil #AmorFati #Zarathustra #Psychology #DeepPhilosophy"
    ])

    return {
        "title": title,
        "description": "\n".join(desc_lines),
        "tags": [
            "Friedrich Nietzsche", "Nietzsche", "Nietzsche on women", "Philosophy", "Human Nature",
            "Beyond Good and Evil", "Thus Spoke Zarathustra", "Amor Fati", "Will to Power",
            "Philosophy documentary", "Deep thinking", "Wisdom", "Psychology", "Dionysian Abyss"
        ]
    }
