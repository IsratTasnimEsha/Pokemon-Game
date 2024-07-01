import pygame
import sys
import random

# Pygame initialization
pygame.init()

# Game constants
WIDTH, HEIGHT = 800, 600
WINDOW_SIZE = (WIDTH, HEIGHT)
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.SysFont("comicsansms", 30)

# Initialize Pygame window
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Minimax Battle Game")

# Game State Variables
player1_hp = 100
player2_hp = 100
player1_power_up_points = 3  # Number of times Player 1 can power up
player2_power_up_points = 3  # Number of times Player 2 can power up
player1_defense_active = False
player2_defense_active = False
current_turn = 1  # Player 1 starts first

# Game Actions
ATTACK = 1
DEFENSE = 2
POWER_UP = 3

# Player Action Buttons
button_width, button_height = 200, 50
button_x = WIDTH // 2 - button_width // 2
attack_button_rect = pygame.Rect(button_x, HEIGHT - 200, button_width, button_height)
defense_button_rect = pygame.Rect(button_x, HEIGHT - 130, button_width, button_height)
power_up_button_rect = pygame.Rect(button_x, HEIGHT - 60, button_width, button_height)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def evaluate_game_state():
    # Simple evaluation based on player HP
    if player1_hp <= 0:
        return -1  # Player 2 wins
    elif player2_hp <= 0:
        return 1   # Player 1 wins
    else:
        return 0   # Game continues

def minimax(state, depth, maximizing_player):
    if depth == 0 or game_over():
        return evaluate_game_state()

    if maximizing_player:
        max_eval = -float('inf')
        for move in possible_moves():
            eval = minimax(move, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in possible_moves():
            eval = minimax(move, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval

def make_ai_move():
    best_move = None
    best_eval = -float('inf')

    # Iterate over all possible moves and evaluate them using Minimax
    for move in possible_moves():
        eval = minimax(move, 3, False)  # Evaluate the move using a depth-limited Minimax approach
        if eval > best_eval:
            best_eval = eval
            best_move = move

    return best_move

def possible_moves():
    moves = []
    # Generate all possible moves based on current game state
    for action in [ATTACK, DEFENSE, POWER_UP]:
        if current_turn == 1:
            # Player 1's turn
            if action == ATTACK:
                moves.append((player1_hp - random.randint(5, 20), player2_hp, False, player1_power_up_points - 1, 2))
            elif action == DEFENSE:
                moves.append((player1_hp, player2_hp, True, player1_power_up_points, 2))
            elif action == POWER_UP and player1_power_up_points > 0:
                moves.append((player1_hp + random.randint(10, 20), player2_hp, False, player1_power_up_points - 1, 2))
        else:
            # Player 2's turn
            if action == ATTACK:
                moves.append((player1_hp, player2_hp - random.randint(5, 20), player1_defense_active, player2_power_up_points - 1, 1))
            elif action == DEFENSE:
                moves.append((player1_hp, player2_hp, False, player2_power_up_points, 1))
            elif action == POWER_UP and player2_power_up_points > 0:
                moves.append((player1_hp, player2_hp + random.randint(10, 20), False, player2_power_up_points - 1, 1))
    return moves

def game_over():
    return player1_hp <= 0 or player2_hp <= 0

def handle_player_move(action):
    global player1_hp, player2_hp, player1_defense_active, player2_defense_active, player1_power_up_points, player2_power_up_points, current_turn

    if current_turn == 1:
        # Player 1's turn
        if action == ATTACK:
            if not player2_defense_active:
                player2_hp -= random.randint(5, 20)
            else:
                player2_hp -= random.randint(1, 5)
        elif action == DEFENSE:
            player1_defense_active = True
        elif action == POWER_UP:
            player1_hp += random.randint(10, 20)
            player1_power_up_points -= 1
    else:
        # Player 2's turn
        if action == ATTACK:
            if not player1_defense_active:
                player1_hp -= random.randint(5, 20)
            else:
                player1_hp -= random.randint(1, 5)
        elif action == DEFENSE:
            player2_defense_active = True
        elif action == POWER_UP:
            player2_hp += random.randint(10, 20)
            player2_power_up_points -= 1

    current_turn = 3 - current_turn  # Switch turns between 1 and 2

def draw_buttons():
    pygame.draw.rect(window, RED if current_turn == 1 else WHITE, attack_button_rect)
    draw_text("Attack", font, BLACK, window, attack_button_rect.centerx, attack_button_rect.centery)

    pygame.draw.rect(window, RED if current_turn == 1 else WHITE, defense_button_rect)
    draw_text("Defense", font, BLACK, window, defense_button_rect.centerx, defense_button_rect.centery)

    pygame.draw.rect(window, RED if current_turn == 1 else WHITE, power_up_button_rect)
    draw_text("Power Up", font, BLACK, window, power_up_button_rect.centerx, power_up_button_rect.centery)

def main():
    global player1_hp, player2_hp, player1_defense_active, player2_defense_active, player1_power_up_points, player2_power_up_points, current_turn

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if attack_button_rect.collidepoint(mouse_x, mouse_y):
                    handle_player_move(ATTACK)
                elif defense_button_rect.collidepoint(mouse_x, mouse_y):
                    handle_player_move(DEFENSE)
                elif power_up_button_rect.collidepoint(mouse_x, mouse_y):
                    handle_player_move(POWER_UP)

        if current_turn == 2 and not game_over():
            # AI's turn
            ai_move = make_ai_move()
            handle_player_move(ai_move[4])

        window.fill(WHITE)
        draw_text(f"Player 1 HP: {player1_hp}", font, BLACK, window, WIDTH // 4, HEIGHT // 2 - 50)
        draw_text(f"Player 2 HP: {player2_hp}", font, BLACK, window, WIDTH * 3 // 4, HEIGHT // 2 - 50)

        draw_buttons()

        if game_over():
            winner = "Player 1 wins!" if player2_hp <= 0 else "Player 2 wins!"
            draw_text(winner, font, RED if player2_hp <= 0 else GREEN, window, WIDTH // 2, HEIGHT // 2)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
