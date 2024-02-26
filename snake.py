import pygame
import time
import random
import sys
import json 

pygame.init()

# Screen dimensions
width, height = 600, 400
game_display = pygame.display.set_mode((width, height))

# Colors
colors = {
    'blue': (50, 153, 213),
    'red': (213, 50, 80),
    'green': (0, 255, 0),
    'yellow': (255, 255, 0),
    'pink': (255, 105, 180),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'orange': (255, 165, 0),
    'purple': (160, 32, 240)
}

# Initial setup
snake_block = 10
snake_speed = 15

clock = pygame.time.Clock()
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("bahnschrift", 25)
game_over_font = pygame.font.SysFont("bahnschrift", 70, bold=True)

def our_snake(snake_block, snake_list, snake_color):
    for x in snake_list:
        pygame.draw.rect(game_display, snake_color, [x[0], x[1], snake_block, snake_block])

def choose_color(option="background"):
    print(f"\nChoose your {option} color (type the color name or 'random' for a random color):")
    for color in colors:
        print(color, end=" ")
    color_input = input("\nColor: ").lower()
    if color_input == 'random':
        return random.choice(list(colors.values()))
    return colors.get(color_input, colors['black'])  # Default to black if an invalid color or 'random' is chosen

def your_score(score, show_score):
    if show_score:
        value = score_font.render("Your Score: " + str(score), True, colors['red'])
        game_display.blit(value, [0, 0])

def walls_wrap_around():
    choice = input("Do you want the walls to wrap around? (yes/no): ").lower()
    return choice == 'yes'

def load_leaderboard():
    try:
        with open("leaderboard.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_leaderboard(leaderboard):
    with open("leaderboard.json", "w") as f:
        json.dump(leaderboard, f)

def display_leaderboard():
    leaderboard = load_leaderboard()
    print("\nLeaderboard:")
    for entry in leaderboard:
        print(f"{entry['name']} - {entry['score']}")

def update_leaderboard(name, score):
    leaderboard = load_leaderboard()
    leaderboard.append({'name': name, 'score': score})
    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    leaderboard = leaderboard[:25]
    save_leaderboard(leaderboard)

def get_player_name():
    return input("Enter your name for the leaderboard: ")

def game_over_screen(score):
    game_display.fill(colors['black'])
    game_over_text = game_over_font.render("GAME OVER", True, colors['red'])
    text_rect = game_over_text.get_rect(center=(width / 2, height / 3))
    game_display.blit(game_over_text, text_rect)
    
    score_text = game_over_font.render(f"Your Score: {score}", True, colors['red'])
    score_rect = score_text.get_rect(center=(width / 2, height / 2))
    game_display.blit(score_text, score_rect)

    instructions_text = font_style.render("Press Q to Quit or R to Replay", True, colors['white'])
    instructions_rect = instructions_text.get_rect(center=(width / 2, height * 2 / 3))
    game_display.blit(instructions_text, instructions_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_r:
                    return 'replay'

def gameLoop():
    # Initial setup
    background_color = choose_color("background")
    snake_color = choose_color("snake")
    food_color = choose_color("food")
    show_score = input("Do you want to display the score? (yes/no): ").lower() == 'yes'
    wrap_around = walls_wrap_around()

    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over:
        while game_close:
            action = game_over_screen(Length_of_snake - 1)
            if action == 'replay':
                return 'replay'
            else:
                return 'quit'

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        # Snake movement
        x1 += x1_change
        y1 += y1_change

        if wrap_around:
            if x1 >= width: x1 = 0
            elif x1 < 0: x1 = width
            if y1 >= height: y1 = 0
            elif y1 < 0: y1 = height
        else:
            if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
                game_close = True

        game_display.fill(background_color)
        pygame.draw.rect(game_display, food_color, [foodx, foody, snake_block, snake_block])
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for segment in snake_List[:-1]:
            if segment == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List, snake_color)
        your_score(Length_of_snake - 1, show_score)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    # The game loop ends here
    final_score = Length_of_snake - 1
    if final_score > 0:
        player_name = get_player_name()
        update_leaderboard(player_name, final_score)
        display_leaderboard()
    
    return 'quit'


def main():
    action = 'replay'
    while action == 'replay':
        action = gameLoop()

main()
