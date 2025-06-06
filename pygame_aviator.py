import pygame
import random
import sys

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

WIDTH, HEIGHT = screen.get_size()
font = pygame.font.SysFont("Arial", 36)
big_font = pygame.font.SysFont("Arial", 72)
small_font = pygame.font.SysFont("Arial", 24)

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

balance = 10000.00
bet = 0.0
crashed = False
cash_out = False
cash_out_multiplier = None
has_cashed_out = False

multiplier = 1.00
multiplier_speed = 0.005
running = False
history = []  # (multiplier, is_cash_out, used_bet)
crash_history = []
show_cash_out_text = False
input_mode = True
input_text = ""
stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)] for _ in range(100)]

def load_rocket_image():
    try:
        rocket_path = r"C:\Python_Workspace\PycharmProjects\pythonProject\AT_JACKPOT\images\rocket.png"
        rocket_image = pygame.image.load(rocket_path)
        return rocket_image
    except:
        return None

def create_rocket_sprite():
    rocket = pygame.Surface((80, 60), pygame.SRCALPHA)
    pygame.draw.ellipse(rocket, (200, 200, 255), (15, 25, 50, 15))
    pygame.draw.polygon(rocket, (255, 255, 255), [(65, 30), (78, 25), (78, 35)])
    pygame.draw.polygon(rocket, (150, 150, 255), [(20, 40), (35, 55), (50, 40)])
    pygame.draw.polygon(rocket, (150, 150, 255), [(20, 20), (35, 5), (50, 20)])
    pygame.draw.polygon(rocket, (255, 100, 0), [(15, 28), (5, 20), (5, 40), (15, 35)])
    pygame.draw.polygon(rocket, (255, 255, 0), [(15, 30), (3, 25), (3, 35), (15, 32)])
    return rocket

rocket_image = load_rocket_image()
plane = pygame.transform.scale(rocket_image, (80, 60)) if rocket_image else create_rocket_sprite()

def get_crash_color(multiplier):
    if multiplier <= 1.0: return (173, 216, 230)
    elif multiplier <= 1.5: return (135, 206, 235)
    elif multiplier <= 2.0: return (100, 149, 237)
    elif multiplier <= 3.0: return (255, 215, 0)
    elif multiplier <= 5.0: return (255, 165, 0)
    elif multiplier <= 10.0: return (255, 69, 0)
    else: return (255, 0, 0)

def get_crash_point():
    r = random.random()
    if r < 0.003: return round(random.uniform(100, 200), 2)
    elif r < 0.02: return round(random.uniform(20, 100), 2)
    elif r < 0.07: return round(random.uniform(10, 20), 2)
    elif r < 0.25: return round(random.uniform(2, 10), 2)
    elif r < 0.65: return round(random.uniform(1.10, 2.00), 2)
    else: return round(random.uniform(1.01, 1.10), 2)

def draw_gradient_background():
    for y in range(HEIGHT):
        color = (int(10 + y * 0.05), int(10 + y * 0.07), int(20 + y * 0.1))
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

def draw_stars():
    for star in stars:
        pygame.draw.circle(screen, WHITE, (star[0], star[1]), star[2])
        star[0] -= star[2]
        if star[0] < 0:
            star[0] = WIDTH
            star[1] = random.randint(0, HEIGHT)
            star[2] = random.randint(1, 3)

def draw_text(text, size, x, y, color=WHITE):
    font_obj = pygame.font.SysFont("Arial", size)
    text_surface = font_obj.render(text, True, color)
    screen.blit(text_surface, (x, y))

crash_point = get_crash_point()
current_bet = 0.0

while True:
    draw_gradient_background()
    draw_stars()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if input_mode:
                if event.key == pygame.K_RETURN:
                    try:
                        bet = float(input_text.replace(",", "."))
                        if 0 < bet <= balance:
                            input_mode = False
                            input_text = ""
                        else:
                            input_text = ""
                    except:
                        input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode.isdigit() or event.unicode in [".", ","]:
                    input_text += event.unicode
            else:
                if event.key == pygame.K_SPACE and not running:
                    if bet > 0 and balance >= bet:
                        current_bet = bet
                        multiplier = 1.00
                        crash_point = get_crash_point()
                        running = True
                        crashed = False
                        cash_out = False
                        has_cashed_out = False
                        show_cash_out_text = False

                if event.key == pygame.K_RETURN and running and not crashed and not has_cashed_out:
                    cash_out = True
                    has_cashed_out = True
                    show_cash_out_text = True
                    cash_out_multiplier = multiplier
                    profit = round(current_bet * (multiplier - 1), 2)
                    balance += profit
                    history.append((round(cash_out_multiplier, 2), True, current_bet))

                if event.key == pygame.K_s and not running:
                    input_mode = True

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    if input_mode:
        draw_text("Enter bet (S to edit): ", 36, 50, 50)
        draw_text(input_text + " лв", 36, 50, 100, GREEN)
    else:
        draw_text(f"Balance: {balance:.2f} лв", 36, 50, 50)
        draw_text(f"Bet: {bet:.2f} лв", 36, 50, 100)

    if running and not crashed:
        multiplier += multiplier_speed * multiplier
        if multiplier >= crash_point:
            crashed = True
            running = False
            crash_history.append(round(multiplier, 2))
            if not has_cashed_out:
                history.append((round(multiplier, 2), False, current_bet))
                balance -= current_bet

    if crashed and not has_cashed_out:
        draw_text(f"CRASHED AT {multiplier:.2f}x", 48, WIDTH // 2 - 150, HEIGHT // 2 - 100, RED)

    if show_cash_out_text:
        draw_text(f"CASHED OUT at {cash_out_multiplier:.2f}x", 48, WIDTH // 2 - 200, HEIGHT // 2 - 100, GREEN)

    if running:
        plane_x = int(WIDTH // 2 + (multiplier * 15))
        plane_y = int(HEIGHT // 2 - (multiplier * 10))
        plane_x = min(plane_x, WIDTH // 2 + 300)
        plane_y = max(plane_y, HEIGHT // 2 - 300)
        screen.blit(plane, (plane_x, plane_y))

    draw_text(f"{multiplier:.2f}x", 72, WIDTH // 2 - 80, 20, WHITE)

    hx = WIDTH - 300
    draw_text("History:", 24, hx, 50)
    for i, (mult, is_cash_out, used_bet) in enumerate(history[-10:][::-1]):
        if is_cash_out:
            color = GREEN
            label = f"OUT (+{used_bet * (mult - 1):.2f} лв)"
        else:
            color = RED
            label = f"CRASH (-{used_bet:.2f} лв)"
        draw_text(f"{mult:.2f}x {label}", 20, hx, 80 + i * 25, color)

    if crash_history:
        draw_text("Crash History:", 20, 50, 200)
        crash_y = 230
        for i, mult in enumerate(crash_history[-5:]):
            crash_color = get_crash_color(mult)
            crash_x = 50 + i * 80
            pygame.draw.circle(screen, crash_color, (crash_x + 25, crash_y + 15), 20)
            pygame.draw.circle(screen, BLACK, (crash_x + 25, crash_y + 15), 20, 2)
            text_surface = small_font.render(f"{mult:.1f}", True, BLACK)
            text_rect = text_surface.get_rect(center=(crash_x + 25, crash_y + 15))
            screen.blit(text_surface, text_rect)

    keys_info = "[S] Set Bet   [SPACE] Start   [ENTER] Cash Out   [ESC] Exit"
    draw_text(keys_info, 24, 20, HEIGHT - 40, WHITE)

    pygame.display.flip()
    clock.tick(60)
