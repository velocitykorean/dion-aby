import os, sys, json, time, requests, re
import config

# Pre-crafted master curriculum for The Dionysian Abyss channel (Friedrich Nietzsche masterworks)
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
        "focus": "An in-depth inquiry into Nietzsche's On the Genealogy of Morals, slave morality, and the subterranean poison of ressentiment.",
        "thumbnail_title_1": "THE HIDDEN POISON",
        "thumbnail_title_2": "OF RESENTMENT",
        "thumbnail_hook": "How Envy Became Morality",
        "acts": [
            ("Act 1: The Birth of Master and Slave Morality", "Noble values versus reactive morality, good and bad versus good and evil."),
            ("Act 2: The Subterranean Venom of Ressentiment", "How repressed impotence and vengeance mutate into counterfeit virtue."),
            ("Act 3: The Ascetic Ideal and Guilt", "The historical origins of bad conscience, debtor-creditor memory, and self-punishment."),
            ("Act 4: The Modern Herd and the Last Man", "The triumph of comfort, safetyism, and egalitarian mediocrity."),
            ("Act 5: The Antidote: Sovereign Individuality", "The capacity to forget, the pathos of distance, and heroic self-sovereignty.")
        ]
    },
    {
        "id": "ep_3",
        "topic": "Amor Fati and The Eternal Return: The Heaviest Weight",
        "focus": "The supreme crucible of Nietzsche's thought: the demon's test of the Eternal Recurrence and the passionate love of fate.",
        "thumbnail_title_1": "THE GREATEST WEIGHT",
        "thumbnail_title_2": "THE ETERNAL RETURN",
        "thumbnail_hook": "Could You Relive Your Life Forever?",
        "acts": [
            ("Act 1: The Demon in the Loneliest Loneliness", "The thought experiment that shatters superficial escapism."),
            ("Act 2: Beyond Regret and Remorse", "Why wishing away your suffering destroys your armor; the unity of woe and joy."),
            ("Act 3: Amor Fati: Loving Fate Unconditionally", "The tragic affirmative joy of the Dionysian; necessity as beauty."),
            ("Act 4: The Cycle of Time", "Cosmic recurrence and the supreme aesthetic responsibility of each moment."),
            ("Act 5: The Heroic Affirmation of Existence", "Singing yes to all of life: 'Was that life? Once more!'")
        ]
    },
    {
        "id": "ep_4",
        "topic": "The Death of God and the Crisis of Nihilism: Overcoming the Abyss",
        "focus": "The collapse of universal dogmas, the madman's lamp in the marketplace, and forging meaning without cosmic crutches.",
        "thumbnail_title_1": "THE DEATH OF GOD",
        "thumbnail_title_2": "OVERCOMING NIHILISM",
        "thumbnail_hook": "What Happens When Truth Dies?",
        "acts": [
            ("Act 1: The Madman in the Marketplace", "Lighting lanterns in the bright morning; the murder of absolute truth."),
            ("Act 2: The Unraveling of the Horizon", "Who gave us the sponge to wipe away the entire horizon?"),
            ("Act 3: Passive vs. Active Nihilism", "Despair and resignation versus destruction as creative liberation."),
            ("Act 4: The Modern Substitutes", "Ideological dogmas, secular religions, and false idols."),
            ("Act 5: The Dawn of Self-Creation", "Becoming gods ourselves to be worthy of the deed.")
        ]
    },
    {
        "id": "ep_5",
        "topic": "Thus Spoke Zarathustra: The Three Metamorphoses and The Overman",
        "focus": "The evolutionary ascent of the human spirit from the bearing camel, to the roaring lion, to the sacred child.",
        "thumbnail_title_1": "THE OVERMAN",
        "thumbnail_title_2": "BEYOND MEDIOCRITY",
        "thumbnail_hook": "Are You a Bridge or an End?",
        "acts": [
            ("Act 1: The Camel: Bearing the Sacred Burden", "The stage of obedience, learning, and carrying heavy weights in the desert."),
            ("Act 2: The Lion: The Great 'Thou Shalt Not'", "Conquering the great dragon of moral obligation with the sacred 'I will'."),
            ("Act 3: The Child: The Sacred 'Yes'", "Innocence, play, a self-propelling wheel, and the creation of new values."),
            ("Act 4: Man as a Rope Over an Abyss", "Danger, overcoming, and why man is a bridge toward the Overman."),
            ("Act 5: The Laughter of Zarathustra", "Transcending gravity with philosophical dance and radiant lightness.")
        ]
    },
    {
        "id": "ep_6",
        "topic": "The Will to Power: The Secret Driving Engine of Life",
        "focus": "Beyond Darwinian survival: life as an insatiable desire to discharge strength, expand, and overcome resistance.",
        "thumbnail_title_1": "WILL TO POWER",
        "thumbnail_title_2": "THE DRIVE OF LIFE",
        "thumbnail_hook": "Why Survival is Not Enough",
        "acts": [
            ("Act 1: Beyond Survival: Life as Overcoming", "Critique of Darwin; life seeks not mere persistence, but expansion of power."),
            ("Act 2: The Psychology of Self-Mastery", "Power over oneself as the highest and rarest form of the Will to Power."),
            ("Act 3: Noble vs. Vulgar Power", "Cruelty as weakness; grace and magnanimity as the overflowing of strength."),
            ("Act 4: Sublimation: Turning Instincts into Art", "Channeling raw primitive drives into philosophy, science, and beauty."),
            ("Act 5: The Universe as Creative Chaos", "The cosmos as a sea of energetic forces clashing and renewing for eternity.")
        ]
    },
    {
        "id": "ep_7",
        "topic": "Apollo and Dionysus: Order, Ecstasy, and the Secret of Greek Tragedy",
        "focus": "The eternal conflict and divine marriage between the Apollonian dream of beauty and the Dionysian drunken revelry.",
        "thumbnail_title_1": "ORDER & ECSTASY",
        "thumbnail_title_2": "APOLLO & DIONYSUS",
        "thumbnail_hook": "The Secret Tension of Genius",
        "acts": [
            ("Act 1: The Two Art Deities of Greece", "Apollo the sculptor and radiant dreamer; Dionysus the god of wine and primordial unity."),
            ("Act 2: The Principium Individuationis", "The fragile boat on the raging sea; breaking through the illusion of separation."),
            ("Act 3: The Birth of Tragedy", "How Greek tragedy reconciled cosmic terror with sublime aesthetic ecstasy."),
            ("Act 4: The Death of Tragedy by Socrates", "Rationalism, optimism, and the pacification of instinctual life."),
            ("Act 5: Reawakening the Dionysian", "Infusing modern rationalism with untamed artistic ecstasy.")
        ]
    },
    {
        "id": "ep_8",
        "topic": "The Free Spirit: Solitude, Masks, and Independent Thinking",
        "focus": "The psychology of the thinker who dares to separate from his tribe, love the high mountains, and wear the mask.",
        "thumbnail_title_1": "THE FREE SPIRIT",
        "thumbnail_title_2": "SACRED SOLITUDE",
        "thumbnail_hook": "Why the Herd Fears Lone Thinkers",
        "acts": [
            ("Act 1: The Great Separation", "Breaking the chains of ancestral duty, custom, and herd comfort."),
            ("Act 2: The Art of the Mask", "Why profound minds must veil their deepest convictions in a superficial world."),
            ("Act 3: The Ice and High Mountains", "Cultivating intellectual rigor where the air is cold and the horizon wide."),
            ("Act 4: The Dangers of Solitude", "Overcoming madness, despair, and the temptation to return to the warm herd."),
            ("Act 5: The Joy of the Open Sea", "Setting sail across uncharted intellectual oceans with boundless courage.")
        ]
    }
]


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

EPISODE_2_SCRIPT = [
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Welcome into the solemn sanctuary of The Dionysian Abyss. Today, we confront what is perhaps Friedrich Nietzsche's most devastating, incisive, and dangerous psychological excavation: the subterranean origin of our moral instincts, the revolt of the herd, and the venomous psychological engine known as ressentiment."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "In his 1887 work, On the Genealogy of Morals, Nietzsche dared to ask a question that academic philosophy had avoided for millennia: Under what conditions did man invent those value judgments, good and evil? And what value do they themselves possess? Have they hitherto hindered or fostered human prosperity? Are they a sign of fullness and vitality, or a symptom of sickness and exhaustion?"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Nietzsche begins by looking into the deep etymological roots of ancient languages \u2014 Greek, Latin, and Old Germanic. He discovers that in all ancient noble societies, the concept of 'good' was never invented by those to whom goodness was shown. It was the noble, the powerful, the high-ranking, and the high-minded who felt and established themselves and their actions as good \u2014 that is, of the first rank \u2014 in contradistinction to all the low, low-minded, common, and plebeian."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "To the aristocratic spirit, 'good' was synonymous with nobility, beauty, courage, and physical triumph. And what was their concept of the opposite? It was simply 'bad' \u2014 meaning common, clumsy, unrefined, or unfortunate. The noble did not hate the commoner; he merely looked upon him with a gentle, pitying indifference, the pathos of distance."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "The noble mode of valuation develops from a triumphant affirmation of itself: 'We the noble, we the good, we the beautiful, we the happy!' It says 'Yes' to itself spontaneously, and only subsequently seeks out an antithesis in order to affirm its own greatness even more gratefully and triumphantly."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "But then, Nietzsche reveals, a historic catastrophe took place \u2014 what he termed the slave revolt in morality. A priestly caste and a subjugated class of people, impotent to conquer their masters on the battlefield, suffered from a profound and festering grievance. Unable to act outwardly, their vengeance turned inward and mutated into something entirely new."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "The slave morality does not begin with a proud self-affirmation. Its very beginning is a reactive 'No' to what is different, what is 'other,' what is 'not itself.' This radical reversal of the evaluating gaze \u2014 this necessary direction toward the outside instead of back onto oneself \u2014 is the very essence of ressentiment."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "In slave morality, the original concept of the noble master \u2014 the strong, proud, self-asserting beast \u2014 was re-labeled as 'Evil.' And only after constructing this demonized image of the enemy did the slave conclude: 'Therefore, whoever is the opposite of this monster is good. And that is us: the meek, the powerless, the humble, and the obedient.'"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Let us examine the exact anatomy of this psychological venom. What is ressentiment? It is not mere anger, nor is it an ordinary burst of hatred. A healthy predator or an aristocratic warrior feels anger, strikes his foe, and in the next moment forgets it, laughing into the wind."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "True ressentiment belongs exclusively to the impotent. It is the emotion of the creature who is too weak to strike back, too fearful to challenge power openly, and too cowardly to bear the weight of his own mediocrity. He swallows his humiliation. He retreats into dark, humid cellars and broods over his grievances year after year."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Nietzsche writes with venomous clarity: 'While the noble man lives in trust and openness with himself, the man of ressentiment is neither upright nor naive nor honest and straightforward with himself. His mind loves hiding places, secret paths and back doors; everything covert strikes him as his world, his security, his refreshment; he understands how to keep silent, how not to forget, how to wait, how to make temporary self-depreciation and humiliation into an art.'"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Consider how modern society operates. Is it not filled with individuals who cloak their personal envy in the sacred language of universal justice? When an individual cannot achieve excellence, he does not admire those who do; he seeks to tear them down to his own level. He calls his cowardice 'gentleness,' his inability to take revenge 'forgiveness,' his cowering submission 'patience,' and his helplessness 'virtue.'"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "In the dark workshops of ressentiment, human weakness was sanctified. The sick forged a counterfeit currency where the inability to live passionately was rebranded as moral purity. They declared: 'Blessed are the meek, for they shall inherit the earth.' And in doing so, they created a cultural atmosphere where any display of sovereign strength, pride, or greatness was viewed with suspicion and guilt."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Nietzsche invites us to listen to the whispers of this underworld: 'These cellar animals are full of revenge and hatred; what are they making of revenge and hatred? Have you ever heard these words? If you only trusted their words, would you suspect you were surrounded by creatures of pure ressentiment?' They answer: 'No, we are not vengeful. We simply long for the triumph of justice, and we pray for the eternal damnation of the strong.'"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "This psychological inversion represents the greatest triumph of spiritual warfare in history. The weak conquered the strong not by overpowering their bodies, but by poisoning their minds \u2014 by convincing the noble that their very strength was a sin against which they must repent."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Having dismantled the triumph of the herd, Nietzsche takes us deeper into the subterranean origin of guilt and the ascetic ideal. Where does the human conscience come from? Has man always possessed this inner court that whispers self-condemnation into the stillness of the night?"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Nietzsche answers with chilling historical precision: No. Conscience was not placed in human breast by a benevolent deity. Conscience was burned into human memory through fire, blood, and physical agony. Throughout prehistory, promises and debts were enforced through the infliction of physical suffering upon the debtor."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "The oldest and most primitive relationship between human beings was the relationship between buyer and seller, creditor and debtor. When a man failed to pay his debt, the contract permitted the creditor to cut a proportionate piece of flesh from the debtor's body. Pain was the most powerful mnemonic aid in human history: 'A thing must be burned in so that it stays in the memory.'"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "When nomadic human beings were finally enclosed within the walls of civilized society, their wild, aggressive animal instincts \u2014 the instinct to hunt, to conquer, to overpower, to destroy \u2014 were suddenly outlawed by state laws and civic peace. What happens to a wild predator when you cage him and deny him any prey?"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "He does not cease to be a predator. All instincts that do not discharge themselves outwardly turn inward! This is what Nietzsche calls the internalization of man: the entire internal world, previously as thin as a membrane, expanded and acquired depth, breadth, and height in the same measure as outward discharge was inhibited."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Denied an external enemy, man turned his claws upon himself. He made his own soul into a torture chamber. He declared his own natural vitality, his animal desires, his pride, and his sexual instincts to be filthy and corrupt. This self-inflicted laceration \u2014 this horrifying will to mistreat one's own nature \u2014 is the birth of bad conscience and moral guilt."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "And who stepped forward to manage this terrible sickness? The ascetic priest. The priest entered the sickroom of humanity and offered a catastrophic diagnosis: 'You suffer, my friend? You are tormented by your own soul? The fault is yours alone! You are guilty before the divine!' Instead of curing the wound, the priest deepened it, offering salvation only through further self-renunciation, fasting, and mortification of the flesh."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "We now emerge into the daylight of our own century. What is the legacy of this historical victory of ressentiment? Look around you at the landscape of modern culture. We live in an era that worships the herd above all things."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "In Thus Spoke Zarathustra, Nietzsche delivered his prophetic warning of the Last Man \u2014 the ultimate product of centuries of domestic pacification and moral leveling. Zarathustra cried out to the crowd: 'The earth has become small, and upon it hops the Last Man, who maketh all things small. His species is indelible like that of the ground-flea; the Last Man liveth longest.'"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "What are the characteristics of the Last Man? He has invented comfort as his supreme idol. He boasts of his enlightened equality: 'No shepherd and one herd! Everyone wants the same, everyone is the same: whoever feels differently goes voluntarily into the madhouse.' He takes pride in having eliminated all friction, all danger, and all deep suffering from existence."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "The Last Man has his little pleasure for the day and his little pleasure for the night, but he honors health above all else. He works, for work is an entertainment; but he takes care lest the entertainment should become troublesome. He no longer becomes poor or rich: both are too burdensome. 'We have discovered happiness,' say the Last Men, and they blink."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "How terrifyingly accurate this prophecy has proved to be. Modern democratic culture is consumed by an obsession with safetyism, emotional fragility, and the systematic suppression of exceptional individuals. Anyone who dares to stand out, to speak with unapologetic brilliance, or to demand greatness is immediately dragged back by the envy of the collective."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Ressentiment has now become institutionalized. It masquerades as social justice, as institutional bureaucracy, and as algorithmic conformity. It teaches human beings to identify as victims, for in the church of ressentiment, the victim is the only one who holds undisputed moral authority."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Yet, Nietzsche reminds us that all great human achievements \u2014 from the temples of Greece to the symphonies of Beethoven, from the philosophical heights to scientific breakthroughs \u2014 were forged not by herds seeking comfort, but by solitary individuals willing to suffer, to conquer, and to rise above the common denominator of their age."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "We arrive at the final, triumphant summit of our meditation. Having diagnosed the disease, what is the Nietzschean cure? How does the free spirit cleanse his bloodstream of the subterranean poison of ressentiment?"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "The first step is absolute psychological honesty. You must have the courage to inspect your own dark cellar. Where in your life are you masquerading your weakness as virtue? Where are you resenting the success, beauty, or strength of others because you lack the discipline to achieve it yourself?"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Nietzsche tells us that the sovereign individual is defined by one supreme capacity: the ability to forget. The noble man does not store insults in his soul; he does not nurse grudges for years. When stung by an adversary, he reacts immediately or casts it aside with a single shrug: 'An insult does not stick to a noble soul; it slides away like rain from a polished shield.'"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "To harbor resentment is to drink poison and expect your enemy to perish. It chains your attention to those you despise, allowing them to dictate your emotional reality from afar. The free spirit severs this chain with a clean blow. He does not waste his precious vitality in reactive battles against the herd."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "As Nietzsche writes in Ecce Homo: 'To be unable to take one's enemies, one's accidents, one's misdeeds seriously for very long \u2014 that is the sign of strong, full natures in whom there is an excess of re-forming, re-creating, healing formative power, which also makes one forget.'"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Instead of tearing down those who are above you, strive to elevate your own spirit. Cultivate what Nietzsche called the Pathos of Distance \u2014 the quiet dignity of standing alone, unconcerned with the praise or blame of the masses. Value your own internal standards above all external metrics of approval."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Do not demand that the world become soft so that you may avoid discomfort. Welcome resistance. Welcome hardship. For just as the diamond requires immense tectonic pressure to crystalize, the sovereign human soul requires adversity to discover the full magnitude of its power."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Walk out of the damp, resentful cellars into the cold mountain air. Say 'Yes' to your own life, with all its chaotic desires, tragic struggles, and boundless potential. Let the herd have their comforts and their small virtues; as for you \u2014 dare to be sovereign, dare to be dangerous, and dare to love your fate without compromise."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Thank you for descending with us into The Dionysian Abyss. If this inquiry into the psychology of ressentiment has illuminated the corridors of your mind, subscribe to our channel, share your reflections in the comments below, and walk forward with unbroken intellectual courage. Until our next descent \u2014 Amor Fati."
    }
]

EPISODE_3_SCRIPT = [
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Welcome into the sacred stillness of The Dionysian Abyss. Today, we stand upon the highest, most dizzying precipice of Friedrich Nietzsche's philosophy. We confront the thought of thoughts \u2014 an idea so terrifying, so demanding, and yet so intoxicating that it acts as the ultimate crucible for the human soul: the doctrine of the Eternal Return, and its ecstatic twin, Amor Fati."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "In August of 1881, while walking through the dense pine forests beside the lake of Silvaplana in the Swiss Alps, near a gigantic pyramidal block of stone, Nietzsche was seized by a sudden, overwhelming revelation. He described it as a thought six thousand feet beyond man and time."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "A year later, in aphorism three hundred and forty-one of The Gay Science, titled 'The Greatest Weight,' he gave this vision voice. He writes: 'What if some day or night a demon were to steal after you into your loneliest loneliness and say to you: \"This life as you now live it and have lived it, you will have to live once more and innumerable times more; and there will be nothing new in it, but every pain and every joy and every thought and sigh and everything unutterably small or great in your life will have to return to you, all in the same succession and sequence \u2014 even this spider and this moonlight between the trees, and even this moment and I myself.\"'"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "'The eternal hourglass of existence is turned upside down again and again, and you with it, speck of dust!' Nietzsche asks us: 'Would you not throw yourself down and gnash your teeth and curse the demon who spoke thus? Or have you once experienced a tremendous moment when you would have answered him: \"Thou art a god, and never have I heard anything more divine!\"'"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Consider the psychological gravity of this test. Nietzsche is not offering a comforting religious afterlife where your tears are wiped away, your mistakes erased, and your suffering rewarded with heavenly paradise. He is offering you nothing less than your exact, unedited life \u2014 with all its humiliating failures, chronic illnesses, heartbreaking betrayals, and quiet desperation \u2014 repeated infinitely throughout cosmic time."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "How does the ordinary person react to such a prospect? With absolute horror. Most human beings live in a perpetual state of postponement, consoling themselves with the illusion that tomorrow will be better, or that after death they will be redeemed. They treat the present moment as a mere waiting room for some future salvation."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "The thought of the Eternal Return shatters this escapism like a hammer hitting glass. It eliminates all excuses. It demands: If this current hour, this current decision, this current posture of your spirit were to echo for all eternity, would you be proud of it, or would you be crushed by shame?"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "It is the heaviest weight that can be placed upon human shoulders. Under its pressure, the weak, resentful, and half-hearted collapse into despair. But for the noble and resolute spirit, it becomes the greatest divine inspiration \u2014 the catalyst for an existence lived with heroic intensity."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "To understand how one can bear the weight of the Eternal Return, we must examine Nietzsche's fierce assault on the psychological diseases of regret, remorse, and guilt. Why do human beings spend so much of their brief existence wishing that the past had been different?"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "In Thus Spoke Zarathustra, in the chapter titled 'On Redemption,' Zarathustra confronts the tragic dilemma of human time: 'To redeem what is past, and to recreate all \"it was\" into a \"thus I willed it!\" \u2014 that alone should I call redemption.' But man's will is bound by the relentless forward march of time: 'Powerless against that which has been done, the will is an angry spectator of all that is past. The will cannot will backwards; that it cannot break time and time's desire, that is the will's loneliest affliction.'"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Because the average person cannot alter the past, his impotence mutates into gnawing remorse. He cries: 'If only I had chosen that other career! If only I had not married that person! If only I had avoided that illness or that catastrophe!' He views his past suffering as a meaningless wound, an accidental defect that ruined his destiny."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Nietzsche warns that remorse is a double evil. The initial mistake was an error; but to dwell upon it with self-flagellation adds a second, lingering poison to the soul. Remorse does not mend what was broken; it merely paralyzes the will to create in the present."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Furthermore, Nietzsche makes a profound observation about the interconnectedness of all existence. Nothing in life stands alone. Your greatest triumphs, your sharpest insights, your emotional depth, and your inner resilience were not produced by your comfortable days in the sun. They were chiseled into you by the very tragedies, betrayals, and agonies you wish to erase!"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "If you remove the wound, you remove the scar that gave your spirit its armor. If you eliminate the grief, you extinguish the profound empathy that made you human. As Nietzsche writes: 'Did you ever say Yes to a single joy? O my friends, then you have said Yes to all woe as well. For all things are bound together, linked together, enamored of each other.'"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "You cannot pick and choose from the tapestry of life as if it were a market stall. You cannot accept the flower while cursing the mud from which its roots drew nourishment. To reject any part of your history is to reject the whole of your becoming."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "The free spirit renounces the childish indulgence of remorse. He looks back upon his most excruciating hours not with bitterness, but with reverence \u2014 recognizing them as the harsh masters that forged his sovereignty."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Having dismantled remorse, we reach the glowing center of Nietzsche's ethical vision: the principle of Amor Fati \u2014 the love of fate. What does it mean to love fate, not merely with cold stoic endurance, but with ecstatic, Dionysian passion?"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Throughout the history of Western thought, various philosophies have preached resignation. Stoicism taught man to endure hardship with an immovable, stony countenance. Christianity taught man to bear his cross with the promise of future compensation. But Nietzsche rejected mere endurance as passive, tired, and lifeless."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "He writes in Ecce Homo: 'My formula for greatness in a human being is Amor Fati: that one wants nothing to be different, not forward, not backward, not in all eternity. Not merely bear what is necessary, still less conceal it \u2014 all idealism is mendacity in the face of what is necessary \u2014 but love it.'"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Consider the revolutionary radicalism of this statement. Nietzsche does not ask you to tolerate your fate; he asks you to love it. He asks you to look upon necessity \u2014 including sickness, betrayal, heartbreak, and death \u2014 not as hostile intruders upon your life, but as essential, harmonious notes in the grand, tragic symphony of existence."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Remember the conditions under which Nietzsche wrote these words. He was not a wealthy aristocrat relaxing in a sunlit villa. He was practically blind, afflicted with agonizing migraines that lasted for days, vomiting in dark hotel rooms across Europe, abandoned by his friends, rejected by the woman he loved, and ignored by the intellectual world of his era."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Yet from the very depths of his physical agony, he produced not bitter lamentations, but books vibrating with joy, gratitude, and golden laughter. In The Gay Science, he penned his famous New Year's resolution: 'I want to learn more and more to see as beautiful what is necessary in things; then I shall be one of those who make things beautiful. Amor Fati: let that be my love henceforth! I do not want to wage war against what is ugly. I do not want to accuse; I do not even want to accuse those who accuse. Looking away shall be my only negation. And all in all and on the whole: some day I wish to be only a Yes-sayer.'"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "This is the heroic affirmation that separates the Overman from the herd. The herd curses the storm and demands a universe without suffering. The noble spirit gazes into the tempest, throws open his arms, and shouts into the wind: 'Strike harder! For I am built to weather the hurricane!'"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Let us now contemplate the cosmic architecture of the Eternal Return. Whether Nietzsche intended this doctrine as a literal cosmological truth or as a supreme psychological thought experiment has been debated for more than a century by scholars across the world."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "In his unpublished notebooks from the eighteen-eighties, Nietzsche sketched scientific arguments for the recurrence of all things: If the universe consists of a finite amount of energy and matter, but extends across infinite time, then every possible combination, arrangement, and permutation of matter must inevitably occur, exhaust itself, and recur an infinite number of times."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Every word you speak at this moment, every leaf falling outside your window, every breath drawn by every living creature must return in the exact same sequence throughout eternity. But even if we treat the Eternal Return not as astrophysics, but as an existential mirror, its psychological power remains absolute."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "It asks you: How would your behavior change if you believed that your current actions were immortal? If every careless hour of procrastination, every cowardly compromise with your principles, and every mean-spirited word spoken in petty anger was not lost to the past, but carved permanently into the eternal bedrock of the cosmos?"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Most people live carelessly because they assume that time is a disposable river \u2014 that their past disappears into nothingness, leaving them free to waste today without consequence. But under the doctrine of the Eternal Return, every second is pregnant with eternity. The present moment is not a stepping stone to tomorrow; it is the absolute center of cosmic history."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "This realization transforms existence from a casual drift into an act of supreme aesthetic responsibility. It demands that you treat your life not as an accident to be endured, but as a masterwork of art to be sculpted with intention, courage, and uncompromising devotion."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "When you live under the shadow of the eternal hourglass, you no longer tolerate mediocrity in yourself. You do not waste precious hours begging for validation from the crowd. You live every day with such clarity, such passion, and such integrity that if the demon were to whisper in your ear tonight, you could smile and answer: 'Once more!'"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "We descend now toward the conclusion of our mountain journey. What is the ultimate invitation of Friedrich Nietzsche's philosophy for you, listening to these words in the quiet of this day?"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Nietzsche does not offer you an easy path. He does not promise that life will be fair, that virtue will be rewarded, or that sorrow will be abolished. On the contrary, he promises that the climb will be steep, that loneliness will often be your companion, and that the abyss will always gaze back into you."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Yet, he shows us that within the very heart of tragedy lies the source of incomparable human glory. The Dionysian spirit is the spirit that does not run from terror, but transforms terror into song. It is the joy of the dancer who knows that the stage will one day collapse, and yet dances with even greater elegance and fire because of that very knowledge."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Stop wishing for a life free of pain. Suffering is not your enemy; suffering is the chisel with which greatness carves your soul. When hardship strikes, do not ask: 'Why has this happened to me?' Ask instead: 'How shall I use this fire to temper my steel?'"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Embrace your fate completely. Love your victories, but love your defeats with equal intensity, for without them you would remain naive and untested. Love your loves, but love the heartbreaks that revealed the untamed depth of your longing. Love the light, but honor the darkness that allowed you to behold the brilliance of the stars."
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Stand tall before the eternal demon. Look into the infinite mirrors of time, and let your spirit proclaim the triumphant words of Zarathustra: 'Was that life? Well then! Once more!'"
    },
    {
        "speaker": "male",
        "name": "The Dionysian",
        "text": "Thank you for descending with us into The Dionysian Abyss. If these reflections on the Eternal Return and Amor Fati have stirred the quiet depths of your soul, subscribe to our channel, share this meditation with those who seek philosophical courage, and carry the torch of heroic affirmation into your life. Until our next descent \u2014 Amor Fati."
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

def generate_dynamic_story_ai(topic: str = None, ep_num: int = 1, past_topics: list = None) -> dict:
    """Uses Pollinations AI to dynamically generate a 100% original Nietzsche episode."""
    if past_topics is None:
        past_topics = load_history_topics()

    print(f"[StoryGenerator] Invoking AI for dynamic philosophical episode #{ep_num}...")
    headers = {"Content-Type": "application/json"}
    api_key = os.environ.get("POLLINATIONS_API_KEY")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    avoid_clause = f"AVOID repeating these already covered topics: {', '.join(past_topics)}" if past_topics else ""

    prompt = f"""You are Friedrich Nietzsche's intellectual heir and the lead philosopher for 'The Dionysian Abyss' channel.
Generate a master 20-minute spoken philosophical video episode (Episode #{ep_num}).
{avoid_clause}
Topic override: {topic if topic else 'Choose a profound, unexamined theme from Nietzsche (e.g. Master/Slave Morality, Beyond Good and Evil, Twilight of the Idols, Overcoming Nihilism, The Free Spirit)'}.

Return ONLY valid JSON matching this exact structure:
{{
  "topic": "Comprehensive Title of the Nietzsche Topic",
  "focus": "2-3 sentences explaining the core philosophical question.",
  "thumbnail_title_1": "2-4 WORDS HEADLINE 1 (e.g. THE WILL TO POWER)",
  "thumbnail_title_2": "2-4 WORDS HEADLINE 2 (e.g. DRIVE OF LIFE)",
  "thumbnail_hook": "Short curiosity question (e.g. Why Survival is Never Enough)",
  "acts": [
    ["Act 1: Title", "Summary"],
    ["Act 2: Title", "Summary"],
    ["Act 3: Title", "Summary"],
    ["Act 4: Title", "Summary"],
    ["Act 5: Title", "Summary"]
  ],
  "dialogue": [
    {{"speaker": "male", "name": "The Dionysian", "text": "Deep, poetic, aristocratic philosophical narration in the cadence of Nietzsche..."}}
  ]
}}
Ensure the dialogue contains at least 35 to 40 rich turns (~2,500 words total) divided evenly across the 5 acts.
"""

    try:
        r = requests.post(
            "https://text.pollinations.ai/",
            json={"messages": [{"role": "user", "content": prompt}], "jsonMode": True},
            headers=headers,
            timeout=90
        )
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, dict) and data.get("dialogue") and len(data["dialogue"]) >= 15:
                print(f"[StoryGenerator] AI successfully generated {len(data['dialogue'])} turns for '{data.get('topic')}'.")
                return data
    except Exception as e:
        print(f"[StoryGenerator] AI generation encountered issue ({e}). Proceeding to curriculum...")

    return None

def generate_full_podcast_story(target_minutes: float = 20.0, topic: str = None, ep_num: int = 1) -> dict:
    """Generates the full story dialogue and chapter structure for the episode."""
    print(f"[StoryGenerator] Preparing script for Episode #{ep_num} (Target: {target_minutes:.1f} mins)...")
    past_topics = load_history_topics()

    # 1. Select matching or next unperformed curriculum catalog item
    catalog_item = None
    if topic:
        catalog_item = next((item for item in NIETZSCHE_CURRICULUM if item["topic"].lower() == topic.lower() or item["id"] == topic), None)

    if not catalog_item:
        # Check by ep_num if not yet performed
        ep_id = f"ep_{ep_num}"
        match_by_id = next((item for item in NIETZSCHE_CURRICULUM if item["id"] == ep_id), None)
        if match_by_id and match_by_id["topic"] not in past_topics:
            catalog_item = match_by_id

    if not catalog_item:
        # Find first unperformed curriculum item
        for item in NIETZSCHE_CURRICULUM:
            if item["topic"] not in past_topics:
                catalog_item = item
                break

    if not catalog_item:
        # If all curriculum items have been used, wrap or pick index
        curriculum_idx = (ep_num - 1) % len(NIETZSCHE_CURRICULUM)
        catalog_item = NIETZSCHE_CURRICULUM[curriculum_idx]

    # 2. Select or generate full dialogue
    dialogue = None
    if catalog_item["id"] == "ep_1":
        dialogue = EPISODE_1_SCRIPT
    elif catalog_item["id"] == "ep_2":
        dialogue = EPISODE_2_SCRIPT
    elif catalog_item["id"] == "ep_3":
        dialogue = EPISODE_3_SCRIPT
    else:
        # Try dynamic AI generation
        ai_story = generate_dynamic_story_ai(topic=catalog_item["topic"], ep_num=ep_num, past_topics=past_topics)
        if ai_story and ai_story.get("dialogue"):
            catalog_item["thumbnail_title_1"] = ai_story.get("thumbnail_title_1", catalog_item["thumbnail_title_1"])
            catalog_item["thumbnail_title_2"] = ai_story.get("thumbnail_title_2", catalog_item["thumbnail_title_2"])
            catalog_item["thumbnail_hook"] = ai_story.get("thumbnail_hook", catalog_item["thumbnail_hook"])
            dialogue = ai_story["dialogue"]

    # Fallback to rich script if AI was offline
    if not dialogue:
        dialogue = EPISODE_2_SCRIPT if (ep_num % 2 == 0) else EPISODE_3_SCRIPT

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

def generate_metadata(topic: str, total_duration_sec: float, chapters: list, ep_num: int = 1, story: dict = None) -> dict:
    """Formats dynamic YouTube title, timestamps description, tags, and metadata."""
    if story and story.get("focus"):
        focus_desc = story["focus"]
    else:
        focus_desc = f"Friedrich Nietzsche's profound philosophical inquiry into {topic}."

    clean_topic = topic.replace("Friedrich Nietzsche on ", "").replace("Friedrich Nietzsche: ", "")
    title = f"Friedrich Nietzsche: {clean_topic} | Deep Philosophical Exploration (Ep. {ep_num:02d})"
    if len(title) > 98:
        title = f"Friedrich Nietzsche: {clean_topic[:60]}... (Ep. {ep_num:02d})"

    desc_lines = [
        f"{focus_desc}",
        "",
        '"My formula for greatness in a human being is Amor Fati: that one wants nothing to be different, not forward, not backward, not in all eternity."',
        " — Friedrich Nietzsche, Ecce Homo (1888)",
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
        "• On the Genealogy of Morals (A Polemic)",
        "• The Gay Science (La Gaya Scienza)",
        "• Thus Spoke Zarathustra (A Book for All and None)",
        "• Twilight of the Idols (How to Philosophize with a Hammer)",
        "• Ecce Homo: How One Becomes What One Is",
        "",
        f"#Nietzsche #Philosophy #HumanNature #{clean_topic.split()[0]} #AmorFati #Zarathustra #Psychology #DeepPhilosophy"
    ])

    return {
        "title": title,
        "description": "\n".join(desc_lines),
        "tags": [
            "Friedrich Nietzsche", "Nietzsche", clean_topic, "Philosophy", "Human Nature",
            "On the Genealogy of Morals", "Beyond Good and Evil", "Thus Spoke Zarathustra", "Amor Fati", "Will to Power",
            "Philosophy documentary", "Deep thinking", "Wisdom", "Psychology", "Dionysian Abyss"
        ]
    }
