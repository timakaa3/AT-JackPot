import pygame
import sys
import requests
import json

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Wordle (Fullscreen Edition)")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (83, 141, 78)
YELLOW = (181, 159, 59)
GRAY = (120, 124, 126)
DARK_GRAY = (60, 60, 60)

FONT = pygame.font.Font(None, 60)
LARGE_FONT = pygame.font.Font(None, 90)

box_size = WIDTH // 16  # по-малки квадратчета

def fetch_word():
    try:
        x = requests.get('https://random-word-api.herokuapp.com/word?length=5')
        WORDS = json.loads(x.content.decode('utf-8'))
        return WORDS[0].upper()
    except:
        return "ERROR"

def check_guess(guess, word):
    colors = [GRAY] * 5
    word_list = list(word)

    for i in range(5):
        if guess[i] == word[i]:
            colors[i] = GREEN
            word_list[i] = None

    for i in range(5):
        if colors[i] == GRAY and guess[i] in word_list:
            colors[i] = YELLOW
            word_list[word_list.index(guess[i])] = None

    return colors

def game_loop():
    secret_word = fetch_word()
    guesses = []
    current_guess = ""
    attempts = 0
    max_attempts = 6
    game_over = False
    won = False

    while True:
        screen.fill(WHITE)
        start_x = (WIDTH - (box_size * 5)) // 2
        start_y = HEIGHT // 20  # по-нагоре

        for row, guess in enumerate(guesses):
            colors = check_guess(guess, secret_word)
            for col, letter in enumerate(guess):
                pygame.draw.rect(screen, colors[col], (
                    start_x + col * box_size,
                    start_y + row * box_size,
                    box_size, box_size
                ))
                text_surface = FONT.render(letter, True, BLACK)
                text_rect = text_surface.get_rect(center=(
                    start_x + col * box_size + box_size // 2,
                    start_y + row * box_size + box_size // 2
                ))
                screen.blit(text_surface, text_rect)

        if not game_over:
            for col, letter in enumerate(current_guess):
                pygame.draw.rect(screen, DARK_GRAY, (
                    start_x + col * box_size,
                    start_y + attempts * box_size,
                    box_size, box_size
                ))
                text_surface = FONT.render(letter, True, WHITE)
                text_rect = text_surface.get_rect(center=(
                    start_x + col * box_size + box_size // 2,
                    start_y + attempts * box_size + box_size // 2
                ))
                screen.blit(text_surface, text_rect)

        if game_over:
            result_text = f"The word was: {secret_word}"
            result_surface = LARGE_FONT.render(result_text, True, BLACK)
            result_rect = result_surface.get_rect(center=(WIDTH // 2, HEIGHT - 150))
            screen.blit(result_surface, result_rect)

            play_text = "Press ENTER to play again or ESC to quit"
            play_surface = FONT.render(play_text, True, BLACK)
            play_rect = play_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            screen.blit(play_surface, play_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if game_over:
                    if event.key == pygame.K_RETURN:
                        return
                    continue

                if event.key == pygame.K_RETURN and len(current_guess) == 5:
                    if attempts < max_attempts:
                        guesses.append(current_guess)
                        if current_guess == secret_word:
                            game_over = True
                            won = True
                        current_guess = ""
                        attempts += 1
                        if attempts == max_attempts and not won:
                            game_over = True
                elif event.key == pygame.K_BACKSPACE:
                    current_guess = current_guess[:-1]
                elif len(current_guess) < 5 and event.unicode.isalpha():
                    current_guess += event.unicode.upper()

while True:
    game_loop()
