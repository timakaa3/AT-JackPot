import pygame
import random
import sys

# --- ИНИЦИАЛИЗАЦИЯ ---
pygame.init()

# Създаване на фулскрийн прозорец
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()  # Взима текущата резолюция
pygame.display.set_caption("Wordle (Fullscreen Edition)")

# Цветове
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (83, 141, 78)
YELLOW = (181, 159, 59)
GRAY = (120, 124, 126)
DARK_GRAY = (60, 60, 60)

# Шрифтове
FONT = pygame.font.Font(None, 80)  # Увеличен за фулскрийн
LARGE_FONT = pygame.font.Font(None, 100)


import requests

x = requests.get('https://random-word-api.herokuapp.com/word?length=5')
import json

# Decode the byte string and parse the JSON
WORDS = json.loads(x.content.decode('utf-8'))
WORD = str((WORDS[0]).upper())

# Списък с думи
# WORDS2 = [
#     "apple", "grape", "table", "chair", "house", "happy", "music", "tiger", "plane", "laugh",
#     "beach", "dance", "light", "cloud", "stone", "sword", "bread", "earth", "water", "flame",
#     "heart", "dream", "storm", "night", "sunny", "shiny", "lucky", "magic", "ocean", "river",
#     "green", "black", "white", "brown", "chess", "check", "spoon", "knife", "plant", "grass",
#     "birds", "horse", "piano", "viola", "guitar", "flute", "notes", "opera", "comic", "novel",
#     "pages", "story", "write", "paper", "words", "speak", "smile", "happy", "laugh", "jolly",
#     "clown", "train", "track", "wagon", "wheel", "glass", "metal", "brick", "stone", "steel",
#     "cloud", "storm", "winds", "chill", "polar", "solar", "space", "orbit", "light", "shine",
#     "earth", "venus", "mercy", "comet", "aster", "flame", "ember", "frost", "snowy",
#     "ocean", "whale", "shark", "coral", "beach", "tides", "waves", "bloom", "leave", "trees",
#     "petal", "roses", "daisy", "lilac", "cacti", "vines", "shade", "roots", "trunk", "flora",
#     "cloud", "rainy", "humid", "chill", "storm", "flood", "quake", "shaky", "drown", "windy",
#     "blaze", "smoke", "flame", "ember", "crash", "blast", "thump", "drone", "pulse", "sting",
#     "vivid", "sight", "sharp", "brisk", "clear", "focus", "shade", "depth", "wider", "close",
#     "sense", "nerve", "brain", "skull", "spine", "limbs", "hands", "flesh", "bones", "veins",
#     "minds", "think", "logic", "smart", "witty", "funny", "noble", "brave", "famed", "glory",
#     "honor", "valet", "royal", "crown", "sword", "guard", "night", "castle", "walls", "moats",
#     "enemy", "duels", "arrow", "flint", "rocks", "brick", "tiles", "paint", "carve", "etchy",
#     "write", "draft", "novel", "story", "tales", "poems", "rhyme", "verse", "stanza", "prose",
#     "speak", "voice", "shout", "whisp", "mutter", "silent", "quiet", "noise", "crowd", "buzzy",
#     "chirp", "whale", "growl", "gruff", "laugh", "smile", "happy", "jolly", "gleam", "twink",
#     "shine", "glint", "glow", "flare", "blink", "twist", "curve", "angle", "point", "cross",
#     "slant", "archs", "peaks", "cliff", "slope", "ridge", "valle", "caves", "tunne", "hills",
#     "plains", "meads", "grass", "herbs", "vines", "roots", "flora", "fauna", "beast", "wolfy",
#     "lions", "tiger", "panda", "horse", "zebra", "oxens", "camel", "sheep", "lambs", "deers",
#     "bears", "moles", "otter", "seals", "whale", "shark", "eagle", "falco", "vulture", "crane",
#     "swan", "ducks", "geese", "stork", "heron", "raven", "crows", "finch", "dove", "robin",
#     "parrot", "hawk", "swans", "piper", "flute", "horns", "bugle", "music", "opera", "melod",
#     "choir", "voice", "notes", "lyric", "verse", "poems", "books", "novel", "drama", "plays",
#     "stage", "actor", "scena", "curta", "write", "penne", "inked", "paint", "brush", "image",
#     "draws", "color", "shade", "blend", "tones", "tints", "stain", "photo", "click", "flash",
#     "scene", "vista", "landy", "plain", "meads", "ridge", "valle", "glace", "frost", "crisp",
#     "chill", "wintr", "snowy", "blizz", "storm", "quake", "shock", "blast", "sound", "noise",
#     "waves", "echoe", "chirp", "tweet", "whale", "growl", "laugh", "smile", "mirth", "gleam",
#     "twink", "shine", "glint", "glow", "flare", "blink", "twist", "curve", "angle", "point",
#     "cross", "slant", "archs", "peaks", "cliff", "slope", "ridge", "valle", "caves", "tunne",
#     "hills", "plains", "meads", "grass", "herbs", "vines", "roots", "flora", "fauna", "beast",
#     "wolfy", "lions", "tiger", "panda", "horse", "zebra", "oxens", "camel", "sheep", "lambs",
#     "deers", "bears", "moles", "otter", "seals", "whale", "shark", "eagle", "falco", "vultur",
#     "crane", "swan", "ducks", "geese", "stork", "heron", "raven", "crows", "finch", "dove",
#     "robin", "parrot", "hawk", "swans", "piper", "flute", "horns", "bugle", "music", "opera",
#     "melod", "choir", "voice", "notes", "lyric", "verse", "poems", "books", "novel", "drama",
#     "plays", "stage", "actor", "scena", "curta", "write", "penne", "inked", "paint", "brush",
#     "image", "draws", "color", "shade", "blend", "tones", "tints", "stain", "photo", "click",
#     "flash", "scene", "vista", "landy", "plain", "meads", "ridge", "valle", "glace", "frost"
# ]
# WORD2 = random.choice(WORDS).upper()

# Променливи за играта
guesses = []
current_guess = ""
max_attempts = 6
attempts = 0
running = True
game_over = False

# --- ФУНКЦИИ ---
def draw_board():
    """Рисува игралното поле и центрира думите."""
    screen.fill(WHITE)
    
    # Изчисляване на отместването за центриране
    box_size = WIDTH // 12
    start_x = (WIDTH - (box_size * 5)) // 2
    start_y = (HEIGHT - (max_attempts * box_size * 1.2)) // 2

    # Рисуване на въведените думи
    for row, guess in enumerate(guesses):
        colors = check_guess(guess)
        for col, letter in enumerate(guess):
            pygame.draw.rect(screen, colors[col], (start_x + col * box_size, start_y + row * box_size * 1.2, box_size, box_size))
            text_surface = FONT.render(letter, True, BLACK)
            text_rect = text_surface.get_rect(center=(start_x + col * box_size + box_size // 2, start_y + row * box_size * 1.2 + box_size // 2))
            screen.blit(text_surface, text_rect)
    
    # Рисуване на текущата дума
    if not game_over:
        for col, letter in enumerate(current_guess):
            pygame.draw.rect(screen, DARK_GRAY, (start_x + col * box_size, start_y + attempts * box_size * 1.2, box_size, box_size))
            text_surface = FONT.render(letter, True, WHITE)
            text_rect = text_surface.get_rect(center=(start_x + col * box_size + box_size // 2, start_y + attempts * box_size * 1.2 + box_size // 2))
            screen.blit(text_surface, text_rect)

    # Ако играта е приключила, покажи тайната дума
    if game_over:
        result_text = f"The word was: {WORD}"
        text_surface = LARGE_FONT.render(result_text, True, BLACK)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        screen.blit(text_surface, text_rect)

    pygame.display.update()

    if game_over:
        pygame.time.wait(3000)
        pygame.quit()

def check_guess(guess):
    """Връща списък с цветовете за буквите в думата."""
    colors = [GRAY] * 5
    word_list = list(WORD)

    # Проверка за зелени букви
    for i in range(5):
        if guess[i] == WORD[i]:
            colors[i] = GREEN
            word_list[i] = None  # Изчиства буквата, за да не се ползва два пъти

    # Проверка за жълти букви
    for i in range(5):
        if colors[i] == GRAY and guess[i] in word_list:
            colors[i] = YELLOW
            word_list[word_list.index(guess[i])] = None

    return colors

# --- ИГРОВИ ЦИКЪЛ ---
while running:
    draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over:
            continue  # Ако играта е свършила, игнорирай входа

        # Въвеждане на букви
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and len(current_guess) == 5:
                if attempts < max_attempts:
                    guesses.append(current_guess)
                    if current_guess == WORD:
                        game_over = True
                    current_guess = ""
                    attempts += 1
                    if attempts == max_attempts:
                        game_over = True
            elif event.key == pygame.K_BACKSPACE:
                current_guess = current_guess[:-1]
            elif len(current_guess) < 5 and event.unicode.isalpha():
                current_guess += event.unicode.upper()

# След като играта свърши, покажи думата за 3 секунди, преди прозорецът да се затвори
draw_board()

pygame.time.wait(3000)
pygame.quit()
sys.exit()