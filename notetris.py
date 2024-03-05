import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
BOARD_WIDTH, BOARD_HEIGHT = 10, 20
CELL_SIZE = 30

# Color Definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

COLORS = [
    (0, 255, 255),  # Cyan for I
    (255, 165, 0),  # Orange for L
    (0, 0, 255),    # Blue for J
    (255, 255, 0),  # Yellow for O
    (0, 255, 0),    # Green for S
    (255, 0, 0),    # Red for Z
    (128, 0, 128),  # Purple for T
]

# Tetromino shapes and their rotations
TETROMINOES = [
    [[(0, 1), (1, 1), (2, 1), (3, 1)], [(1, 0), (1, 1), (1, 2), (1, 3)]],  # I
    [[(0, 1), (1, 1), (2, 1), (2, 0)], [(1, 0), (1, 1), (1, 2), (2, 2)], [(0, 1), (1, 1), (2, 1), (0, 2)], [(1, 0), (1, 1), (1, 2), (0, 0)]],  # L
    [[(0, 1), (1, 1), (2, 1), (2, 2)], [(1, 0), (1, 1), (1, 2), (2, 0)], [(0, 1), (1, 1), (2, 1), (0, 0)], [(1, 0), (1, 1), (1, 2), (0, 2)]],  # J
    [[(1, 0), (2, 0), (1, 1), (2, 1)]],  # O
    [[(1, 1), (2, 1), (0, 2), (1, 2)], [(0, 0), (0, 1), (1, 1), (1, 2)]],  # S
    [[(0, 1), (1, 1), (1, 2), (2, 2)], [(1, 0), (1, 1), (0, 1), (0, 2)]],  # Z
    [[(1, 0), (0, 1), (1, 1), (2, 1)], [(1, 0), (1, 1), (1, 2), (2, 1)], [(0, 1), (1, 1), (2, 1), (1, 2)], [(1, 0), (0, 1), (1, 1), (1, 2)]]  # T
]

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Font for displaying text
font = pygame.font.Font(None, 24)  # Use Pygame's default font

class Tetromino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.rotation = 0
        self.x = BOARD_WIDTH // 2 - 2
        self.y = 0

    def image(self):
        return self.shape[self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

def create_board():
    return [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

def valid_position(board, tetromino):
    for x, y in tetromino.image():
        newX = x + tetromino.x
        newY = y + tetromino.y
        # Check if new position is within board boundaries
        if newX < 0 or newX >= BOARD_WIDTH or newY >= BOARD_HEIGHT:
            return False
        # Check if new position overlaps with existing tetrominoes on the board
        if newY >= 0 and board[newY][newX] != 0:  # Ensure newY is not negative to avoid list index out of range error
            return False
    return True


def add_to_board(board, tetromino):
    for x, y in tetromino.image():
        if y + tetromino.y >= 0:  # Only add parts of tetromino that are on the board
            board[y + tetromino.y][x + tetromino.x] = tetromino.color

def remove_line(board):
    new_board = [row for row in board if 0 in row]
    lines_cleared = BOARD_HEIGHT - len(new_board)
    for _ in range(lines_cleared):
        new_board.insert(0, [0 for _ in range(BOARD_WIDTH)])
    return new_board, lines_cleared

def draw_board(board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            color = COLORS[cell-1] if cell else BLACK
            pygame.draw.rect(screen, color, pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if cell:
                pygame.draw.rect(screen, WHITE, pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def draw_tetromino(tetromino):
    for x, y in tetromino.image():
        if y + tetromino.y >= 0:  # Only draw parts of tetromino that are on the board
            pygame.draw.rect(screen, COLORS[tetromino.color - 1],
                             pygame.Rect((tetromino.x + x) * CELL_SIZE, (tetromino.y + y) * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def spawn_tetromino():
    return Tetromino(random.choice(TETROMINOES), random.randint(1, len(COLORS)))

def show_start_screen():
    screen.fill(BLACK)
    draw_text("Welcome to NOTetris", (30, 20), WHITE)
    draw_text("Ready?", (50, 100), WHITE)
    draw_text("Move with left and right arrow", (30, 180), WHITE)
    draw_text("Rotate with up arrow", (50, 260), WHITE)
    draw_text("Press any key to start", (30, 340), WHITE)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def draw_text(text, position, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def main():
    show_start_screen()
    board = create_board()
    clock = pygame.time.Clock()
    current_tetromino = spawn_tetromino()
    level = 1
    lines_cleared = 0
    score = 0
    running = True
    fall_speed = 0.3 # Slower start
    last_fall_time = pygame.time.get_ticks()

    while running:
        screen.fill(BLACK)
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_tetromino.rotate()
                    if not valid_position(board, current_tetromino):
                        current_tetromino.rotate()  # Rotate back
                elif event.key == pygame.K_DOWN:
                    # Manual move down faster
                    if current_time - last_fall_time > 100:  # Quick response for moving down
                        current_tetromino.y += 1
                        if not valid_position(board, current_tetromino):
                            current_tetromino.y -= 1
                elif event.key == pygame.K_LEFT:
                    current_tetromino.x -= 1
                    if not valid_position(board, current_tetromino):
                        current_tetromino.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_tetromino.x += 1
                    if not valid_position(board, current_tetromino):
                        current_tetromino.x -= 1

        # Automatic move down based on fall speed
        if current_time - last_fall_time > fall_speed * 1000:
            last_fall_time = current_time
            current_tetromino.y += 1
            if not valid_position(board, current_tetromino):
                current_tetromino.y -= 1
                add_to_board(board, current_tetromino)
                board, cleared = remove_line(board)
                lines_cleared += cleared
                score += cleared * 100
                current_tetromino = spawn_tetromino()
                if not valid_position(board, current_tetromino):
                    draw_text("GAME OVER", (80, SCREEN_HEIGHT // 2), WHITE)
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    running = False

        if lines_cleared >= 10:
            level += 1
            lines_cleared = 0
            fall_speed *= 0.9  # Increase game speed as level goes up

        draw_board(board)
        draw_tetromino(current_tetromino)
        draw_text(f"Level: {level}", (220, 10), WHITE)
        draw_text(f"Score: {score}", (10, 10), WHITE)

        pygame.display.flip()
        clock.tick(30)  # Frame rate

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
