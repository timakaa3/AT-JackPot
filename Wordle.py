import random

# ANSI escape codes for colored output
GREEN = "\033[42m\033[30m"  # Green background, black text
YELLOW = "\033[43m\033[30m"  # Yellow background, black text
GRAY = "\033[47m\033[30m"    # White background, black text (for gray effect)
RESET = "\033[0m"            # Reset to default terminal colors

WORDS = [
    "apple", "grape", "table", "chair", "house", "happy", "music", "tiger", "plane", "laugh",
    "beach", "dance", "light", "cloud", "stone", "sword", "bread", "earth", "water", "flame",
    "heart", "dream", "storm", "night", "sunny", "shiny", "lucky", "magic", "ocean", "river",
    "green", "black", "white", "brown", "chess", "check", "spoon", "knife", "plant", "grass",
    "birds", "horse", "piano", "viola", "guitar", "flute", "notes", "opera", "comic", "novel",
    "pages", "story", "write", "paper", "words", "speak", "smile", "happy", "laugh", "jolly",
    "clown", "train", "track", "wagon", "wheel", "glass", "metal", "brick", "stone", "steel",
    "cloud", "storm", "winds", "chill", "polar", "solar", "space", "orbit", "light", "shine",
    "earth", "venus", "mercy", "jupiter", "comet", "aster", "flame", "ember", "frost", "snowy",
    "ocean", "whale", "shark", "coral", "beach", "tides", "waves", "bloom", "leaves", "trees",
    "petal", "roses", "daisy", "lilac", "cacti", "vines", "shade", "roots", "trunk", "flora",
    "cloud", "rainy", "humid", "chill", "storm", "flood", "quake", "shaky", "drown", "windy",
    "blaze", "smoke", "flame", "ember", "crash", "blast", "thump", "drone", "pulse", "sting",
    "vivid", "sight", "sharp", "brisk", "clear", "focus", "shade", "depth", "wider", "close",
    "sense", "nerve", "brain", "skull", "spine", "limbs", "hands", "flesh", "bones", "veins",
    "minds", "think", "logic", "smart", "witty", "funny", "noble", "brave", "famed", "glory",
    "honor", "valet", "royal", "crown", "sword", "guard", "knight", "castle", "walls", "moats",
    "enemy", "duels", "arrow", "flint", "rocks", "brick", "tiles", "paint", "carve", "etchy",
    "write", "draft", "novel", "story", "tales", "poems", "rhyme", "verse", "stanza", "prose",
    "speak", "voice", "shout", "whisp", "mutter", "silent", "quiet", "noise", "crowd", "buzz",
    "chirp", "whale", "growl", "gruff", "laugh", "smile", "happy", "jolly", "gleam", "twink",
    "shine", "glint", "glow", "flare", "blink", "twist", "curve", "angle", "point", "cross",
    "slant", "archs", "peaks", "cliff", "slope", "ridge", "valle", "caves", "tunne", "hills",
    "plains", "meads", "grass", "herbs", "vines", "roots", "flora", "fauna", "beast", "wolfy",
    "lions", "tiger", "panda", "horse", "zebra", "oxens", "camel", "sheep", "lambs", "deers",
    "bears", "moles", "otter", "seals", "whale", "shark", "eagle", "falco", "vulture", "crane",
    "swan", "ducks", "geese", "stork", "heron", "raven", "crows", "finch", "dove", "robin",
    "parrot", "hawk", "swans", "piper", "flute", "horns", "bugle", "music", "opera", "melod",
    "choir", "voice", "notes", "lyric", "verse", "poems", "books", "novel", "drama", "plays",
    "stage", "actor", "scena", "curta", "write", "penne", "inked", "paint", "brush", "image",
    "draws", "color", "shade", "blend", "tones", "tints", "stain", "photo", "click", "flash",
    "scene", "vista", "landy", "plain", "meads", "ridge", "valle", "glace", "frost", "crisp",
    "chill", "wintr", "snowy", "blizz", "storm", "quake", "shock", "blast", "sound", "noise",
    "waves", "echoe", "chirp", "tweet", "whale", "growl", "laugh", "smile", "mirth", "gleam",
    "twink", "shine", "glint", "glow", "flare", "blink", "twist", "curve", "angle", "point",
    "cross", "slant", "archs", "peaks", "cliff", "slope", "ridge", "valle", "caves", "tunne",
    "hills", "plains", "meads", "grass", "herbs", "vines", "roots", "flora", "fauna", "beast",
    "wolfy", "lions", "tiger", "panda", "horse", "zebra", "oxens", "camel", "sheep", "lambs",
    "deers", "bears", "moles", "otter", "seals", "whale", "shark", "eagle", "falco", "vultur",
    "crane", "swan", "ducks", "geese", "stork", "heron", "raven", "crows", "finch", "dove",
    "robin", "parrot", "hawk", "swans", "piper", "flute", "horns", "bugle", "music", "opera",
    "melod", "choir", "voice", "notes", "lyric", "verse", "poems", "books", "novel", "drama",
    "plays", "stage", "actor", "scena", "curta", "write", "penne", "inked", "paint", "brush",
    "image", "draws", "color", "shade", "blend", "tones", "tints", "stain", "photo", "click",
    "flash", "scene", "vista", "landy", "plain", "meads", "ridge", "valle", "glace", "frost"
]


# Pick a random word
secret_word = random.choice(WORDS)

# Max attempts
attempts = 6

print("🎯 Welcome to Wordle (Python Edition)!")
print("Guess the 5-letter word. You have 6 attempts.")

def check_guess(guess, secret_word):
    result = [""] * 5  # Store formatted letters
    secret_letter_count = {}  # Track letter counts in the secret word

    # Count occurrences of each letter in secret_word
    for letter in secret_word:
        secret_letter_count[letter] = secret_letter_count.get(letter, 0) + 1

    # First pass: Check for correct positions (GREEN)
    for i in range(5):
        if guess[i] == secret_word[i]:
            result[i] = f"{GREEN} {guess[i].upper()} {RESET}"  # Green box
            secret_letter_count[guess[i]] -= 1  # Reduce available count

    # Second pass: Check for correct letters in the wrong position (YELLOW)
    for i in range(5):
        if result[i] == "" and guess[i] in secret_letter_count and secret_letter_count[guess[i]] > 0:
            result[i] = f"{YELLOW} {guess[i].upper()} {RESET}"  # Yellow box
            secret_letter_count[guess[i]] -= 1  # Reduce available count

    # Third pass: Mark incorrect letters (GRAY)
    for i in range(5):
        if result[i] == "":
            result[i] = f"{GRAY} {guess[i].upper()} {RESET}"  # Gray box

    return " ".join(result)

# Game loop
for attempt in range(1, attempts + 1):
    guess = input(f"Attempt {attempt}/{attempts}: ").lower()

    # Validate input
    if len(guess) != 5 or not guess.isalpha():
        print("❌ Enter a valid 5-letter word!")
        continue

    # Check the guess
    feedback = check_guess(guess, secret_word)
    print(feedback)

    if guess == secret_word:
        print("🎉 Congratulations! You guessed the word!")
        break
else:
    print(f"😢 Out of attempts! The word was: {secret_word}")