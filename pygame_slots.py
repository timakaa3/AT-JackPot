import pygame
import random
import sys
import os
import time

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Slot Machine – Final Version")
clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 34)
big_font = pygame.font.SysFont("arial", 52, bold=True)

IMAGE_FOLDER = "C:/Python_Workspace/PycharmProjects/pythonProject/AT_JACKPOT/images"

symbol_names = ["cherry", "lemon", "plums", "orange", "bell", "seven", "star"]
symbol_weights = {
    "cherry": 40,
    "lemon": 35,
    "plums": 30,
    "orange": 25,
    "bell": 10,
    "seven": 3,
    "star": 1
}
symbol_payouts = {
    "cherry": {"3x": 2, "2x": 0.5},
    "lemon": {"3x": 3, "2x": 0.5},
    "plums": {"3x": 4, "2x": 1},
    "orange": {"3x": 5, "2x": 1},
    "bell": {"3x": 12, "2x": 4},
    "seven": {"3x": 40, "2x": 15},
    "star": {"3x": 100, "2x": 25, "1x": 10}
}
symbols = {}
for name in symbol_names:
    path = os.path.join(IMAGE_FOLDER, f"{name}.png")
    if not os.path.exists(path):
        print(f"Missing image: {path}")
        sys.exit()
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, (180, 180))
    symbols[name] = image

balance = 10000
bet = 100
reels = ["cherry", "lemon", "plums"]
message = ""
spinning = False
final_result = []
highlight = []

durations = [3.0, 1.8, 0.8]
AUTO_DELAY_MS = [1500, 1200, 400]
speed_names = ["Slow", "Normal", "Fast"]
speed_index = 1

auto_spin = False
auto_delay_active = False
auto_timer = 0
stop_auto_after_spin = False

def input_bet():
    global bet, auto_spin
    input_active = True
    user_text = ""
    while input_active:
        screen.fill((0, 0, 0))
        draw_text("Enter your bet:", WIDTH // 2, HEIGHT // 2 - 50, center=True, big=True)
        draw_text(user_text, WIDTH // 2, HEIGHT // 2 + 10, center=True, big=True)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_text.isdigit():
                        new_bet = int(user_text)
                        if 0 < new_bet <= balance:
                            bet = new_bet
                            input_active = False
                        else:
                            user_text = ""
                    else:
                        user_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.unicode.isdigit():
                    user_text += event.unicode

def draw_text(text, x, y, color=(255, 255, 255), center=False, big=False):
    surf = big_font.render(text, True, color) if big else font.render(text, True, color)
    rect = surf.get_rect()
    rect.center = (x, y) if center else (x, y)
    screen.blit(surf, rect)

def weighted_random_symbol():
    population = []
    for name, weight in symbol_weights.items():
        population.extend([name] * weight)
    return random.choice(population)

def spin_reels():
    return [weighted_random_symbol() for _ in range(3)]

def calculate_win(reels, bet):
    s1, s2, s3 = reels
    if reels.count("star") == 3:
        return bet * symbol_payouts["star"]["3x"]
    elif reels.count("star") == 2:
        return bet * symbol_payouts["star"]["2x"]
    elif reels.count("star") == 1 and len(set(reels)) == 3:
        return bet * symbol_payouts["star"]["1x"]
    if s1 == s2 == s3:
        return bet * symbol_payouts[s1]["3x"]
    if s1 == s2 and "2x" in symbol_payouts[s1]:
        return bet * symbol_payouts[s1]["2x"]
    return 0

def get_winning_positions(reels):
    s1, s2, s3 = reels
    if reels.count("star") == 3:
        return [0, 1, 2]
    elif reels.count("star") == 2:
        return [i for i, s in enumerate(reels) if s == "star"]
    elif reels.count("star") == 1:
        non_stars = [s for s in reels if s != "star"]
        if len(non_stars) == 2 and non_stars[0] == non_stars[1]:
            return [i for i, s in enumerate(reels) if s == non_stars[0] or s == "star"]
        return [i for i, s in enumerate(reels) if s == "star"]
    if s1 == s2 == s3:
        return [0, 1, 2]
    if s1 == s2:
        return [0, 1]
    return []

def animate_spin(result, duration):
    global reels, spinning, highlight
    start_time = time.time()
    interval = 0.05
    while time.time() - start_time < duration:
        screen.fill((10, 10, 30))
        for i in range(3):
            temp = weighted_random_symbol()
            x = WIDTH // 2 - 300 + i * 200
            y = HEIGHT // 2 - 100
            pygame.draw.rect(screen, (30, 30, 60), (x, y, 180, 180), border_radius=20)
            screen.blit(symbols[temp], (x + 10, y + 10))
        draw_ui()
        pygame.display.flip()
        time.sleep(interval)
    reels[:] = result
    highlight[:] = get_winning_positions(reels)
    spinning = False

def draw_ui():
    left = int(WIDTH * 0.12)
    top = int(HEIGHT * 0.06)
    spacing = 50
    draw_text(f"Balance: {int(balance)}", left, top)
    draw_text(f"Bet: {bet}", left, top + spacing)
    draw_text(f"Speed: {speed_names[speed_index]}", left, top + spacing * 2)
    draw_text(f"Auto Spin: {'ON' if auto_spin else 'OFF'}", left, top + spacing * 3)
    draw_text("←/→ Speed | SPACE Spin | A Auto | S Set Bet | ESC Exit", WIDTH // 2, HEIGHT - 50, center=True)
    draw_text(message, WIDTH // 2, HEIGHT // 2 + 150, center=True)

def draw_reels():
    for i in range(3):
        x = WIDTH // 2 - 300 + i * 200
        y = HEIGHT // 2 - 100
        rect = pygame.Rect(x, y, 180, 180)
        pygame.draw.rect(screen, (30, 30, 60), rect, border_radius=20)
        screen.blit(symbols[reels[i]], (x + 10, y + 10))
        if i in highlight:
            pygame.draw.rect(screen, (255, 255, 0), rect, 5, border_radius=20)

# Задаване на първоначален залог
input_bet()

running = True
while running:
    screen.fill((10, 10, 30))
    current_time = pygame.time.get_ticks()

    if auto_spin:
        if bet > balance:
            auto_spin = False
        elif not spinning and not auto_delay_active:
            final_result = spin_reels()
            spinning = True
            balance -= bet
            pygame.time.set_timer(pygame.USEREVENT, 10)

    if auto_delay_active and current_time - auto_timer >= AUTO_DELAY_MS[speed_index]:
        auto_delay_active = False
        if stop_auto_after_spin:
            auto_spin = False
            stop_auto_after_spin = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE and not auto_spin:
                if not spinning and bet <= balance:
                    final_result = spin_reels()
                    spinning = True
                    balance -= bet
                    pygame.time.set_timer(pygame.USEREVENT, 10)
            elif event.key == pygame.K_a:
                if auto_spin:
                    if spinning:
                        stop_auto_after_spin = True
                    else:
                        auto_spin = False
                else:
                    auto_spin = True
                    stop_auto_after_spin = False
            elif event.key == pygame.K_LEFT:
                speed_index = max(0, speed_index - 1)
            elif event.key == pygame.K_RIGHT:
                speed_index = min(2, speed_index + 1)
            elif event.key == pygame.K_s and not auto_spin and not spinning:
                input_bet()
        elif event.type == pygame.USEREVENT and spinning:
            animate_spin(final_result, durations[speed_index])
            win = calculate_win(final_result, bet)
            balance += win
            message = f"Win: {int(win)}" if win > 0 else "No win!"
            pygame.time.set_timer(pygame.USEREVENT, 0)
            spinning = False
            auto_delay_active = True
            auto_timer = pygame.time.get_ticks()

    if not spinning:
        draw_reels()
        draw_ui()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
