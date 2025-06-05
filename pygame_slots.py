import pygame
import random
import sys
import os
import time

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Slot Machine – AutoSpin Enabled")
clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 34)
big_font = pygame.font.SysFont("arial", 52, bold=True)

IMAGE_FOLDER = "C:/Workspace/python_new/at_jackpot/slots_image"

symbol_names = ["cherry", "lemon", "plums", "orange", "bell", "seven", "star"]
symbol_weights = {
    "cherry": 30,
    "lemon": 25,
    "plums": 20,
    "orange": 15,
    "bell": 7,
    "seven": 3,
    "star": 2
}

symbols = {}
for name in symbol_names:
    path = os.path.join(IMAGE_FOLDER, f"{name}.png")
    if not os.path.exists(path):
        print(f"⚠️ Missing image: {path}")
        sys.exit()
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, (180, 180))  # по-големи символи
    symbols[name] = image

balance = 10000
bet = 100
reels = ["cherry", "lemon", "plums"]
message = ""
spinning = False
final_result = []

durations = [3.0, 1.8, 0.8]
speed_names = ["Slow", "Normal", "Fast"]
speed_index = 1

auto_spin = False
auto_timer = 0

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
    stars = reels.count("star")
    if stars == 3:
        return bet * 25
    elif stars == 2:
        return bet * 5
    elif stars == 1:
        non_stars = [s for s in reels if s != "star"]
        if len(non_stars) == 2 and non_stars[0] == non_stars[1]:
            sym = non_stars[0]
            if sym == "seven":
                return bet * 10 * 2
            elif sym == "bell":
                return bet * 5 * 2
            else:
                return bet * 3 * 2
        return bet * 3
    if s1 == s2 == s3:
        if s1 == "seven":
            return bet * 10
        elif s1 == "bell":
            return bet * 5
        else:
            return bet * 3
    if s1 == s2 and s1 != "star":
        return bet * 1
    return 0

def animate_spin(result, duration):
    global reels, spinning
    start_time = time.time()
    current = reels.copy()
    interval = 0.05

    while time.time() - start_time < duration:
        screen.fill((10, 10, 30))
        for i in range(3):
            current[i] = weighted_random_symbol()
            x = WIDTH // 2 - 300 + i * 200
            y = HEIGHT // 2 - 100
            pygame.draw.rect(screen, (30, 30, 60), (x, y, 180, 180), border_radius=20)
            screen.blit(symbols[current[i]], (x + 10, y + 10))
        draw_ui()
        pygame.display.flip()
        time.sleep(interval)

    reels[:] = result
    spinning = False

def draw_ui():
    left = int(WIDTH * 0.12)
    top = int(HEIGHT * 0.06)
    spacing = 50

    draw_text(f"Balance: {balance}", left, top)
    draw_text(f"Bet: {bet}", left, top + spacing)
    draw_text(f"Speed: {speed_names[speed_index]}", left, top + spacing * 2)
    draw_text(f"Auto Spin: {'ON' if auto_spin else 'OFF'}", left, top + spacing * 3)
    draw_text("←/→ Speed | SPACE Spin | A Auto | ESC Exit", WIDTH // 2, HEIGHT - 50, center=True)
    draw_text(message, WIDTH // 2, HEIGHT // 2 + 150, center=True)

running = True
while running:
    screen.fill((10, 10, 30))

    current_time = pygame.time.get_ticks()
    if auto_spin and not spinning and balance >= bet:
        if current_time - auto_timer > 500:
            final_result = spin_reels()
            spinning = True
            balance -= bet
            pygame.time.set_timer(pygame.USEREVENT, 10)
            auto_timer = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE and not auto_spin:
                if not spinning and balance >= bet:
                    final_result = spin_reels()
                    spinning = True
                    balance -= bet
                    pygame.time.set_timer(pygame.USEREVENT, 10)
            elif event.key == pygame.K_a:
                auto_spin = not auto_spin
            elif event.key == pygame.K_LEFT:
                speed_index = max(0, speed_index - 1)
            elif event.key == pygame.K_RIGHT:
                speed_index = min(2, speed_index + 1)
        elif event.type == pygame.USEREVENT and spinning:
            animate_spin(final_result, durations[speed_index])
            win = calculate_win(final_result, bet)
            balance += win
            message = f"Win: {win}" if win > 0 else "No win!"
            pygame.time.set_timer(pygame.USEREVENT, 0)

    if not spinning:
        for i in range(3):
            x = WIDTH // 2 - 300 + i * 200
            y = HEIGHT // 2 - 100
            pygame.draw.rect(screen, (30, 30, 60), (x, y, 180, 180), border_radius=20)
            screen.blit(symbols[reels[i]], (x + 10, y + 10))
        draw_ui()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
