import pygame
import random
import time
import sys

pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Aviator Game")
clock = pygame.time.Clock()

# Цветове
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (180, 180, 180)
BLACK = (0, 0, 0)

# Зареждане на фон
try:
    bg_img = pygame.image.load(r"C:\Python_Workspace\PycharmProjects\pythonProject\AT_JACKPOT\space.png")
    bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
except:
    print("Background not found!")
    sys.exit()

# Самолет (стрелка)
plane_img = pygame.Surface((60, 40), pygame.SRCALPHA)
pygame.draw.polygon(plane_img, WHITE, [(30, 0), (0, 20), (60, 20)])
plane_img = pygame.transform.rotate(plane_img, 45)

# Променливи
balance = 100.0
bet = 0.0
bet_input = ""
entering_bet = True

game_active = False
cashed_out = False
cashout_multiplier = 0.0
start_time = None
multiplier = 1.0
history = []
show_result = False
center_reached = False

# Движение на самолет
plane_x = 100
plane_y = HEIGHT // 2
speed_x, speed_y = 3, 1.5

# Движение на фона
bg_scroll = 0
bg_speed = 2

def draw_text(text, x, y, size=36, color=WHITE):
    font = pygame.font.SysFont("Arial", size)
    screen.blit(font.render(text, True, color), (x, y))

def reset_game():
    global multiplier, game_active, cashed_out, cashout_multiplier
    global start_time, plane_x, plane_y, show_result, center_reached, bg_scroll
    global balance

    if balance >= bet:
        balance -= bet
    else:
        game_active = False
        return

    multiplier = 1.0
    game_active = True
    cashed_out = False
    cashout_multiplier = 0.0
    show_result = False
    center_reached = False
    start_time = time.time()
    plane_x, plane_y = 100, HEIGHT // 2
    bg_scroll = 0

running = True
while running:
    screen.fill(BLACK)
    screen.blit(bg_img, (bg_scroll, 0))
    screen.blit(bg_img, (bg_scroll + WIDTH, 0))
    bg_scroll -= bg_speed
    if bg_scroll <= -WIDTH:
        bg_scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and not game_active:
                entering_bet = True
                bet_input = ""

            if entering_bet:
                if event.key == pygame.K_RETURN:
                    try:
                        new_bet = float(bet_input)
                        if 0 < new_bet <= balance:
                            bet = new_bet
                            entering_bet = False
                            reset_game()
                    except:
                        bet_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    bet_input = bet_input[:-1]
                elif event.unicode.isdigit() or (event.unicode == "." and '.' not in bet_input):
                    bet_input += event.unicode

            elif game_active:
                if event.key == pygame.K_RETURN and not cashed_out:
                    cashed_out = True
                    cashout_multiplier = multiplier
                    balance += round(bet * cashout_multiplier, 2)
                    history.insert(0, (cashout_multiplier, True))
                    show_result = True

            elif not game_active:
                if event.key == pygame.K_SPACE and not entering_bet and bet > 0:
                    reset_game()

    if game_active:
        elapsed = time.time() - start_time
        multiplier = round(pow(1.01, elapsed * 10), 2)  

        raw_chance = 0.10 + (multiplier - 1) ** 1.1 * 0.025
        crash_chance = min(raw_chance, 0.85)
        if random.random() < crash_chance:
            game_active = False 
            history.insert(0, (multiplier, False))
            show_result = True

        if not center_reached:
            if plane_x < WIDTH // 2 and plane_y > HEIGHT // 3:
                plane_x += speed_x
                plane_y -= speed_y
            else:
                center_reached = True

    # Самолет
    screen.blit(plane_img, (plane_x, plane_y))

    # Информация
    draw_text(f"Balance: {balance:.2f} лв.", 30, 30)
    draw_text(f"Multiplier: x{multiplier:.2f}", WIDTH // 2 - 100, 50, 50, GREEN)

    # Статус
    if cashed_out:
        draw_text(f"Cashed Out at x{cashout_multiplier:.2f}", WIDTH // 2 - 180, HEIGHT // 2, 50, GREEN)
    elif show_result and not game_active:
        draw_text("CRASHED!", WIDTH // 2 - 100, HEIGHT // 2, 60, RED)

    # История
    draw_text("History:", WIDTH - 200, 30)
    for i, (m, win) in enumerate(history[:6]):
        draw_text(f"x{m:.2f}", WIDTH - 200, 70 + i * 30, 30, GREEN if win else RED)

    # Инструкции
    draw_text("ESC: Quit | S: Change Bet | SPACE: New Round | ENTER: Cash Out", 30, HEIGHT - 40, 28, GRAY)

    # Въвеждане на залог
    if entering_bet:
        draw_text(f"Enter bet (лв): {bet_input}", WIDTH // 2 - 150, HEIGHT // 2, 40, WHITE)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
