import pygame
import sys
import random
import pickle
import os
from datetime import datetime

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 600, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Blocker!")

# Define colors
colors = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'green': (0, 255, 0),
    'red': (255, 0, 0),
    'yellow': (255, 255, 0),
    'blue': (0, 0, 255),
    'orange': (255, 165, 0),
    'purple': (160, 32, 240),
    'cyan': (0, 255, 255),
    'dark_green': (0, 100, 0)
}
car_colors = [colors['red'], colors['blue'], colors['green'], colors['yellow'], colors['orange'], colors['purple'], colors['cyan']]

# Prompt for customization
print("Welcome to Blocker!")
player_name = input("What's your name? ")
block_color_input = input("What color would you like to make your Block? (Available: green, dark_green, blue, red) ").lower()
block_color = colors.get(block_color_input, colors['green'])
mode = input("Dark Mode or Light Mode? (dark/light) ").lower()
background_color = colors['black'] if mode == 'dark' else colors['white']
text_color = colors['white'] if mode == 'dark' else colors['black']

# Game settings
lane_height = screen_height // 10
frog_size = 30  # Block size is twice as large
frog_speed = lane_height 
start_position = [screen_width // 2, screen_height - lane_height // 2 - frog_size // 2]
frog_pos = start_position.copy()
initial_car_speed = 4  # Starting out more difficult
car_speed = initial_car_speed
initial_spawn_rate = 30  # Cars spawn more frequently
spawn_rate = initial_spawn_rate
cars = []
level = 1
score = 0
top_scores = []

# FPS and Fonts
clock = pygame.time.Clock()
fps = 60
font = pygame.font.SysFont("arial", 20)

# Score File
score_file = "top_scores.pkl"

def load_scores():
    if os.path.exists(score_file):
        with open(score_file, "rb") as f:
            return pickle.load(f)
    return []

def save_score(player_name, score):
    new_score_entry = {"name": player_name, "score": score, "date": datetime.now().strftime("%Y-%m-%d")}
    top_scores = load_scores()
    top_scores.append(new_score_entry)
    top_scores.sort(key=lambda x: x["score"], reverse=True)
    top_scores = top_scores[:10]  # Keep only top 10 scores
    with open(score_file, "wb") as f:
        pickle.dump(top_scores, f)

def draw_ui():
    level_text = font.render(f"Level: {level}", True, text_color)
    score_text = font.render(f"Score: {score}", True, text_color)
    screen.blit(level_text, (5, 5))
    screen.blit(score_text, (5, 25))

def reset_game():
    global frog_pos, cars, car_speed, spawn_rate, level, score
    frog_pos = start_position.copy()
    cars = []
    car_speed += 1  # Increase car speed more significantly
    spawn_rate = max(15, spawn_rate - 5)  # Increase spawn rate, but not less than every 15 frames
    score += 100  # Bonus for completing a level
    level += 1

def draw_frog():
    pygame.draw.rect(screen, block_color, (*frog_pos, frog_size, frog_size))

def move_frog(direction):
    global score
    if direction == "UP" and frog_pos[1] > 0:
        frog_pos[1] -= frog_speed
        score += 10
    elif direction == "DOWN" and frog_pos[1] < screen_height - frog_size:
        frog_pos[1] += frog_speed
        score -= 10
    elif direction == "LEFT" and frog_pos[0] > 0:
        frog_pos[0] -= frog_speed
    elif direction == "RIGHT" and frog_pos[0] < screen_width - frog_size:
        frog_pos[0] += frog_speed

def spawn_cars():
    if random.randint(1, spawn_rate) == 1:  # Randomly spawn cars based on spawn_rate
        lane = random.randint(1, 8)
        color = random.choice(car_colors)  # Randomly select a color
        car = {"rect": pygame.Rect(screen_width, lane_height * lane - 40, 80, 40), "speed": car_speed, "color": color}  # Adjust size and add color
        cars.append(car)

def move_cars():
    for car in cars:
        car["rect"].x -= car["speed"]
        if car["rect"].x < -80:  # Adjust for new size
            cars.remove(car)

def draw_cars():
    for car in cars:
        pygame.draw.rect(screen, car["color"], car["rect"])  # Use the car's color


def check_collisions():
    frog_rect = pygame.Rect(*frog_pos, frog_size, frog_size)
    for car in cars:
        if frog_rect.colliderect(car["rect"]):
            return True
    return False

def check_victory():
    return frog_pos[1] <= lane_height // 2

def game_loop():
    global frog_pos, level, car_speed, spawn_rate, score, top_scores
    running = True
    top_scores = load_scores()
    game_start_time = pygame.time.get_ticks()  # Get the start time of the game

    while running:
        screen.fill(background_color)

        current_time = pygame.time.get_ticks()
        if current_time - game_start_time < 2000:  # Wait for 2 seconds before starting to spawn cars
            draw_ui()
            draw_frog()
            pygame.display.flip()
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_frog("UP")
                elif event.key == pygame.K_DOWN:
                    move_frog("DOWN")
                elif event.key == pygame.K_LEFT:
                    move_frog("LEFT")
                elif event.key == pygame.K_RIGHT:
                    move_frog("RIGHT")

        spawn_cars()
        move_cars()
        draw_cars()
        draw_frog()
        draw_ui()

        if check_collisions():
            save_score(player_name, score)
            print(f"Game Over! Your score was: {score}.")
            running = False
        
        if check_victory():
            reset_game()

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
