import pygame
import random
import sys

pygame.init()

# Window
WIDTH, HEIGHT = 400, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
SKY_TOP = (120, 180, 250)
SKY_BOTTOM = (240, 250, 255)
GREEN = (70, 200, 90)
BROWN = (170, 120, 60)
YELLOW = (255, 230, 70)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.SysFont("arial", 26, bold=True)

# Game settings
bird_x = 80
bird_radius = 15
gravity = 0.5
jump_power = -10
pipe_width = 60
ground_height = 80

DIFFICULTIES = {
    "Easy": {"speed": 3, "gap": 180},
    "Medium": {"speed": 4, "gap": 150},
    "Hard": {"speed": 5, "gap": 120},
}

# Clouds
clouds = [{"x": random.randint(0, WIDTH),
           "y": random.randint(30, 180)} for _ in range(4)]

def draw_gradient():
    for y in range(HEIGHT):
        r = SKY_TOP[0] + (SKY_BOTTOM[0] - SKY_TOP[0]) * y // HEIGHT
        g = SKY_TOP[1] + (SKY_BOTTOM[1] - SKY_TOP[1]) * y // HEIGHT
        b = SKY_TOP[2] + (SKY_BOTTOM[2] - SKY_TOP[2]) * y // HEIGHT
        pygame.draw.line(win, (r, g, b), (0, y), (WIDTH, y))

def draw_clouds():
    for c in clouds:
        pygame.draw.circle(win, WHITE, (c["x"], c["y"]), 20)
        pygame.draw.circle(win, WHITE, (c["x"] + 20, c["y"] + 5), 18)
        pygame.draw.circle(win, WHITE, (c["x"] - 20, c["y"] + 5), 18)

        c["x"] -= 0.3
        if c["x"] < -50:
            c["x"] = WIDTH + random.randint(50, 150)
            c["y"] = random.randint(30, 180)

def create_pipe(gap):
    hole = random.randint(120, HEIGHT - 200)
    top = pygame.Rect(WIDTH, 0, pipe_width, hole)
    bottom = pygame.Rect(WIDTH, hole + gap, pipe_width, HEIGHT - ground_height)
    return {"top": top, "bottom": bottom, "passed": False}

def check_collision(bird_y, pipes):
    bird_rect = pygame.Rect(bird_x - bird_radius,
                            bird_y - bird_radius,
                            bird_radius * 2,
                            bird_radius * 2)

    for p in pipes:
        if bird_rect.colliderect(p["top"]) or bird_rect.colliderect(p["bottom"]):
            return True

    if bird_y <= 0 or bird_y >= HEIGHT - ground_height:
        return True

    return False

def draw_game(bird_y, pipes, score):
    draw_gradient()
    draw_clouds()

    # Ground
    pygame.draw.rect(win, BROWN, (0, HEIGHT - ground_height, WIDTH, ground_height))
    for x in range(0, WIDTH, 20):
        pygame.draw.circle(win, (130, 90, 50), (x + 10, HEIGHT - ground_height + 10), 6)

    # Pipes
    for p in pipes:
        pygame.draw.rect(win, GREEN, p["top"])
        pygame.draw.rect(win, GREEN, p["bottom"])

    # Bird
    pygame.draw.circle(win, YELLOW, (bird_x, int(bird_y)), bird_radius)
    pygame.draw.circle(win, BLACK, (bird_x + 5, int(bird_y - 5)), 3)

    # Score
    score_txt = font.render(f"Score: {score}", True, BLACK)
    win.blit(score_txt, (10, 10))

    pygame.display.update()

def draw_menu(title, buttons):
    draw_gradient()
    draw_clouds()

    title_surf = font.render(title, True, BLACK)
    win.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 120))

    btn_rects = []
    y = 220
    for text in buttons:
        rect = pygame.Rect(WIDTH//2 - 80, y, 160, 50)
        pygame.draw.rect(win, BLACK, rect, border_radius=10)
        surf = font.render(text, True, WHITE)
        win.blit(surf, (rect.x + 30, rect.y + 12))
        btn_rects.append((rect, text))
        y += 70

    pygame.display.update()
    return btn_rects

def choose_difficulty():
    while True:
        options = draw_menu("Select Difficulty", ["Easy", "Medium", "Hard"])
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for r, text in options:
                    if r.collidepoint(event.pos): return text

def game_over(score):
    while True:
        options = draw_menu(f"Game Over! Score: {score}", ["Retry", "Menu"])
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for r, text in options:
                    if r.collidepoint(event.pos): return text

def game_loop(speed, gap):
    bird_y = HEIGHT // 2
    velocity = 0
    pipes = []
    score = 0
    frame = 0

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                velocity = jump_power

        velocity += gravity
        bird_y += velocity

        if frame % 90 == 0:
            pipes.append(create_pipe(gap))

        for p in pipes:
            p["top"].x -= speed
            p["bottom"].x -= speed

            if not p["passed"] and p["top"].x + pipe_width < bird_x:
                score += 1
                p["passed"] = True

        pipes = [p for p in pipes if p["top"].x + pipe_width > 0]

        draw_game(bird_y, pipes, score)

        if check_collision(bird_y, pipes):
            choice = game_over(score)
            if choice == "Retry":
                return game_loop(speed, gap)
            else:
                return

        frame += 1

# MAIN LOOP
while True:
    diff = choose_difficulty()
    settings = DIFFICULTIES[diff]
    game_loop(settings["speed"], settings["gap"])
