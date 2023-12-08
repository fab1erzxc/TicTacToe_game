import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Global constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300
LINE_WIDTH = 6

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("TicTacToe")

# Define colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Define font
font = pygame.font.SysFont(None, 40)

# Game state variables
clicked = False
player = 1
pos = (0, 0)
marker = []
game_over = False
winner = 0

# Setup a rectangle for the "Play Again" option
again_rect = Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2, 160, 50)

# Create an empty 3 x 3 list to represent the grid
for x in range(3):
    row = [0] * 3
    marker.append(row)


def draw_board():
    """Draw the Tic Tac Toe board on the screen."""
    bg = (255, 255, 210)
    grid = (50, 50, 50)
    screen.fill(bg)
    for x in range(1, 3):
        pygame.draw.line(screen, grid, (0, 100 * x), (SCREEN_WIDTH, 100 * x), LINE_WIDTH)
        pygame.draw.line(screen, grid, (100 * x, 0), (100 * x, SCREEN_HEIGHT), LINE_WIDTH)


def draw_markers():
    """Draw the X and O markers on the board."""
    x_pos = 0
    for x in marker:
        y_pos = 0
        for y in x:
            if y == 1:
                pygame.draw.line(screen, RED, (x_pos * 100 + 15, y_pos * 100 + 15),
                                 (x_pos * 100 + 85, y_pos * 100 + 85), LINE_WIDTH)
                pygame.draw.line(screen, RED, (x_pos * 100 + 15, y_pos * 100 + 85),
                                 (x_pos * 100 + 85, y_pos * 100 + 15), LINE_WIDTH)
            if y == -1:
                pygame.draw.circle(screen, BLUE, (x_pos * 100 + 50, y_pos * 100 + 50), 38, LINE_WIDTH)
            y_pos += 1
        x_pos += 1


def check_game_over():
    """Check if the game is over and determine the winner."""
    global game_over, winner

    x_pos = 0
    for x in marker:
        # Check columns
        if sum(x) == 3:
            winner = 1
            game_over = True
        if sum(x) == -3:
            winner = 2
            game_over = True
        # Check rows
        if marker[0][x_pos] + marker[1][x_pos] + marker[2][x_pos] == 3:
            winner = 1
            game_over = True
        if marker[0][x_pos] + marker[1][x_pos] + marker[2][x_pos] == -3:
            winner = 2
            game_over = True
        x_pos += 1

    # Check diagonals
    if marker[0][0] + marker[1][1] + marker[2][2] == 3 or marker[2][0] + marker[1][1] + marker[0][2] == 3:
        winner = 1
        game_over = True
    if marker[0][0] + marker[1][1] + marker[2][2] == -3 or marker[2][0] + marker[1][1] + marker[0][2] == -3:
        winner = 2
        game_over = True

    # Check for a draw
    if not game_over:
        draw = True
        for row in marker:
            for i in row:
                if i == 0:
                    draw = False
        if draw:
            game_over = True
            winner = 0


def draw_game_over(winner):
    """Draw the game-over screen with the winner or a draw."""
    if winner != 0:
        win_text = "Player " + str(winner) + " wins!"
    elif winner == 0:
        win_text = "Draw!"

    end_img = font.render(win_text, True, BLUE)
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60, 200, 50))
    screen.blit(end_img, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))

    again_text = "Play Again?"
    again_img = font.render(again_text, True, BLUE)
    pygame.draw.rect(screen, GREEN, again_rect)
    screen.blit(again_img, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 10))


# Main game loop
run = True
while run:
    # Draw board and markers
    draw_board()
    draw_markers()

    # Event loop
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if game_over is False:
            # Check for mouse click
            if event.type == MOUSEBUTTONDOWN and not clicked:
                clicked = True
            if event.type == MOUSEBUTTONUP and clicked:
                clicked = False
                pos = pygame.mouse.get_pos()
                cell_x = pos[0] // 100
                cell_y = pos[1] // 100
                if marker[cell_x][cell_y] == 0:
                    marker[cell_x][cell_y] = player
                    player *= -1
                    check_game_over()

    # Check if the game has been won
    if game_over:
        draw_game_over(winner)
        # Check for mouse click to see if we clicked on "Play Again"
        if event.type == MOUSEBUTTONDOWN and not clicked:
            clicked = True
        if event.type == MOUSEBUTTONUP and clicked:
            clicked = False
            pos = pygame.mouse.get_pos()
            if again_rect.collidepoint(pos):
                # Reset variables
                game_over = False
                player = 1
                pos = (0, 0)
                marker = []
                # Create an empty 3 x 3 list to represent the grid
                for x in range(3):
                    row = [0] * 3
                    marker.append(row)

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
