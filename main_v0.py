import chess
import chess.engine
import pygame
import time

# Initialize Stockfish engine (adjust path if needed)
# Replace with the actual path if different
engine_path = "D:/project_learn/Python/stockfish-windows-x86-64-avx2.exe"
engine = chess.engine.SimpleEngine.popen_uci(engine_path)
# Initialize Pygame
pygame.init()
screen_width = screen_height = 512  # Size of the board
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Chess Game with Stockfish")

# Board and square dimensions
board_size = 8
square_size = screen_width // board_size

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
light_square = (238, 238, 210)  # Light square color
dark_square = (118, 150, 86)  # Dark square color
selected_square_color = (255, 255, 0)  # Highlight color

# Initialize game state
board = chess.Board()
selected_square = None
player_color = chess.WHITE  # Set to chess.BLACK if you want to play as black

# Load chess piece images (replace with your own)
piece_images = {}
pieces = ['r', 'n', 'b', 'q', 'k', 'p',
          'R', 'N', 'B', 'Q', 'K', 'P']
imgs = {
    'r': 'b_rook',
    'n': 'b_knight',
    'b': 'b_bishop',
    'q': 'b_queen',
    'k': 'b_king',
    'p': 'b_pawn',
    'R': 'w_rook',
    'N': 'w_knight',
    'B': 'w_bishop',
    'Q': 'w_queen',
    'K': 'w_king',
    'P': 'w_pawn',
}
for piece in pieces:
    piece_images[piece] = pygame.image.load(f"assets/imgs/{imgs[piece]}.png")
    piece_images[piece] = pygame.transform.smoothscale(
        piece_images[piece], (screen_width // board_size, screen_width // board_size))


def get_possible_moves():
    row, col = selected_square
    # Convert row, col to the square notation (e.g., (0, 0) -> 'a8', (7, 7) -> 'h1')
    square = chess.square(col, 7 - row)

    # Get the piece at the given square
    piece = board.piece_at(square)

    if piece is None:
        return []

    # Get all legal moves
    legal_moves = board.legal_moves

    # Filter moves that start from the given square
    possible_moves = [
        move for move in legal_moves if move.from_square == square]

    return possible_moves


def highlight_moves():
    """Highlights the squares where the selected piece can legally move."""
    possible_moves = get_possible_moves()
    for move in possible_moves:
        col, row = chess.square_file(
            move.to_square), 7 - chess.square_rank(move.to_square)
        pygame.draw.circle(screen, (0, 255, 0),  # Green highlight color
                           (col * square_size + square_size // 2,
                            row * square_size + square_size // 2),
                           square_size // 4)  # Adjust size as needed


def draw_button(screen, text, x, y, width, height, color, hover_color, action=None):
    # --- Function to draw a button ---
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    font = pygame.font.Font(None, 20)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(
        center=((x + (width / 2)), (y + (height / 2))))
    screen.blit(text_surface, text_rect)


def reset_game():
    # --- Function to reset the game ---
    global board, selected_square, game_over
    board = chess.Board()
    selected_square = None
    game_over = False


def draw_board():
    for row in range(board_size):
        for col in range(board_size):
            color = light_square if (row + col) % 2 == 0 else dark_square
            pygame.draw.rect(screen, color, (col * square_size,
                             row * square_size, square_size, square_size))

            # Highlight selected square
            if selected_square is not None and (row, col) == selected_square:
                pygame.draw.rect(screen, selected_square_color, (col *
                                 square_size, row * square_size, square_size, square_size), 3)

            # Chess notation is flipped vertically
            piece = str(board.piece_at(chess.square(col, 7 - row)))
            if piece != 'None':
                image = piece_images[piece]
                screen.blit(image, (col * square_size, row * square_size))


def get_square_from_mouse(pos):
    x, y = pos
    col = x // square_size
    row = y // square_size
    return row, col


# Game loop
running = True
game_over = False
while running:
    # AI's turn

    if board.turn != player_color and not game_over:
        result = engine.play(
            board, chess.engine.Limit(time=1)  # Adjust thinking time as needed
        )
        board.push(result.move)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if board.turn == player_color:
                row, col = get_square_from_mouse(pygame.mouse.get_pos())
                square = chess.square(col, 7 - row)

                if selected_square is None:
                    if board.piece_at(square) is not None and board.color_at(square) == player_color:
                        selected_square = (row, col)
                        print('if 1')
                else:
                    move = chess.Move(chess.square(
                        selected_square[1], 7 - selected_square[0]), square)
                    if move in board.legal_moves:
                        board.push(move)
                        selected_square = None
                        print('if 2')
                    else:
                        selected_square = None
                        print('if 3')

        if board.is_checkmate():
            game_over = True
    if game_over:
        game_over = True  # Ensure we stay in the game over state
        screen.fill((200, 200, 200))  # Light gray background for game over

        font = pygame.font.Font(None, 36)
        if board.is_checkmate():
            text = f"Checkmate! {'White' if board.turn ==
                                 chess.BLACK else 'Black'} wins!"
        elif board.is_stalemate():
            text = "Draw by Stalemate!"
        else:
            text = "Game Over"  # Other draw conditions
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(
            center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(text_surface, text_rect)

        # Draw Restart button
        draw_button(screen, "Restart", screen_width // 2 - 50, screen_height // 2 + 50, 100, 50,
                    (255, 255, 255), (200, 200, 200), reset_game)
    # Draw the board and pieces
    if not game_over:
        draw_board()
    if selected_square:
        highlight_moves()
    pygame.display.flip()

# Quit Stockfish and Pygame
engine.quit()
pygame.quit()
