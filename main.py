import chess
import chess.engine
import pygame

# --- Constants ---
SCREEN_WIDTH = SCREEN_HEIGHT = 512
BOARD_SIZE = 8
SQUARE_SIZE = SCREEN_WIDTH // BOARD_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQUARE = (238, 238, 210)
DARK_SQUARE = (118, 150, 86)
SELECTED_SQUARE_COLOR = (255, 255, 0)

# --- Image Loading ---


def load_piece_images():
    """Loads chess piece images from the assets folder."""
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
        img_path = f"assets/imgs/{imgs[piece]}.png"
        piece_images[piece] = pygame.image.load(img_path)
        piece_images[piece] = pygame.transform.smoothscale(
            piece_images[piece], (SQUARE_SIZE, SQUARE_SIZE))
    return piece_images


PIECE_IMAGES = load_piece_images()

# --- Sound Classes ---


class Sound:
    def __init__(self):
        self.check_sound = pygame.mixer.Sound("./assets/sounds/check_sound.mp3")
        self.game_over_sound = pygame.mixer.Sound("./assets/sounds/gameover_sound.mp3")
        self.game_start_sound = pygame.mixer.Sound("./assets/sounds/start_sound.mp3")
        self.move_sound = pygame.mixer.Sound("./assets/sounds/move_sound.mp3")
        self.stalemate_sound = pygame.mixer.Sound("./assets/sounds/stalemate_sound.mp3")

# --- Game Classes ---


class Game:
    def __init__(self, engine_path, player_color=chess.WHITE):
        self.engine_path = engine_path
        self.engine = chess.engine.SimpleEngine.popen_uci(self.engine_path)
        self.board = chess.Board()
        self.player_color = player_color
        self.selected_square = None
        self.game_over = False
        self.sound = Sound()
        self.sound.game_start_sound.play()

    def reset(self):
        """Resets the game state."""
        self.sound.game_start_sound.play()
        self.board.reset()
        self.selected_square = None
        self.game_over = False

    def handle_mouse_click(self, pos):
        """Handles mouse clicks to select and move pieces."""
        if not self.game_over and self.board.turn == self.player_color:
            row, col = self.get_square_from_mouse(pos)
            square = chess.square(col, 7 - row)

            if self.selected_square is None:
                # Select a piece if it belongs to the current player
                if self.board.piece_at(square) is not None and self.board.color_at(square) == self.player_color:
                    self.selected_square = (row, col)
            else:
                # Try to make a move
                move = chess.Move(chess.square(
                    self.selected_square[1], 7 - self.selected_square[0]), square)
                if move in self.board.legal_moves:
                    self.board.push(move)
                    self.sound.move_sound.play()
                self.selected_square = None  # Deselect after making a move or invalid move attempt

    def get_square_from_mouse(self, pos):
        """Converts mouse coordinates to chessboard square coordinates."""
        x, y = pos
        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE
        return row, col

    def make_ai_move(self):
        """Makes a move using the Stockfish engine."""
        if not self.game_over and self.board.turn != self.player_color:
            result = self.engine.play(self.board, chess.engine.Limit(time=1))
            self.board.push(result.move)
            self.sound.move_sound.play()

    def update_game_state(self):
        """Checks for game over conditions."""
        if self.board.is_checkmate() or self.board.is_stalemate():
            self.game_over = True

    def draw(self, screen):
        """Draws the board, pieces, and game over messages."""
        self.draw_board(screen)
        if self.selected_square:
            self.highlight_moves(screen)

        if self.game_over:
            self.sound.game_over_sound.play()
            self.draw_game_over(screen)

    def draw_board(self, screen):
        """Draws the chessboard."""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                pygame.draw.rect(screen, color, (col * SQUARE_SIZE,
                                                 row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

                # Highlight selected square
                if self.selected_square is not None and (row, col) == self.selected_square:
                    pygame.draw.rect(screen, SELECTED_SQUARE_COLOR, (col *
                                     SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

                # Draw pieces
                piece = str(self.board.piece_at(chess.square(col, 7 - row)))
                if piece != 'None':
                    image = PIECE_IMAGES[piece]
                    screen.blit(image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def highlight_moves(self, screen):
        """Highlights legal moves for the selected piece."""
        if self.selected_square:
            possible_moves = self.get_possible_moves()
            for move in possible_moves:
                col, row = chess.square_file(
                    move.to_square), 7 - chess.square_rank(move.to_square)
                pygame.draw.circle(screen, (0, 255, 0),
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                    row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 4)

    def get_possible_moves(self):
        """Returns a list of legal moves for the selected piece."""
        if self.selected_square:
            row, col = self.selected_square
            square = chess.square(col, 7 - row)
            piece = self.board.piece_at(square)
            if piece is not None:
                legal_moves = self.board.legal_moves
                return [move for move in legal_moves if move.from_square == square]
        return []

    def draw_game_over(self, screen):
        """Draws a semi-transparent overlay with the game over message and a restart button."""

        # Create a semi-transparent surface to overlay on the board
        overlay = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((200, 200, 200, 128))  # Fill with gray, half transparent

        font = pygame.font.Font(None, 36)
        if self.board.is_checkmate():
            text = f"Checkmate! {
                'White' if self.board.turn == chess.BLACK else 'Black'} wins!"
        elif self.board.is_stalemate():
            text = "Draw by Stalemate!"
        else:
            text = "Game Over"

        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        overlay.blit(text_surface, text_rect)

        # Draw the Restart button on the overlay
        draw_button(overlay, "Restart", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50, 100, 50,
                    (255, 255, 255), (200, 200, 200), self.reset)

        # Blit (draw) the overlay onto the screen
        screen.blit(overlay, (0, 0))

    def draw_game_over_2(self, screen):
        """Draws the game over message and restart button."""
        screen.fill((200, 200, 200))
        font = pygame.font.Font(None, 36)
        if self.board.is_checkmate():
            text = f"Checkmate! {
                'White' if self.board.turn == chess.BLACK else 'Black'} wins!"
        elif self.board.is_stalemate():
            text = "Draw by Stalemate!"
        else:
            text = "Game Over"
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(text_surface, text_rect)

        # Restart Button
        draw_button(screen, "Restart", SCREEN_WIDTH // 2 - 50,
                    SCREEN_HEIGHT // 2 + 50, 100, 50,
                    (255, 255, 255), (200, 200, 200), self.reset)

# --- Helper Function ---


def draw_button(screen, text, x, y, width, height, color, hover_color, action=None):
    """Draws a button and handles click events."""
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


# --- Main Game Loop ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Chess Game with Stockfish")

    # Replace with your engine path
    engine_path = "D:/project_learn/Python/stockfish-windows-x86-64-avx2.exe"
    game = Game(engine_path)

    running = True
    while running:
        game.make_ai_move()  # AI's turn
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_mouse_click(pygame.mouse.get_pos())

        game.update_game_state()
        game.draw(screen)
        pygame.display.flip()

    game.engine.quit()
    pygame.quit()


if __name__ == "__main__":
    main()
