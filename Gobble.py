"""
Gobblet Jr. Game Implementation

This module implements the Gobblet Jr. board game using Pygame.
Players take turns placing or moving pieces on a 3x3 board,
with the goal of getting 3 in a row.
"""

import sys
import pygame

# Initialize pygame
pygame.init()

#Globals
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1000
BOARD_SIZE = 3
SQUARE_SIZE = 150
BOARD_OFFSET_X = (SCREEN_WIDTH - BOARD_SIZE * SQUARE_SIZE) // 2
BOARD_OFFSET_Y = 200
PIECE_SIZES = ["small", "medium", "large"]
PIECE_RADIUS = {"small": 25, "medium": 40, "large": 55}

# Updated color scheme
L_BLU = (134, 214, 254)
D_BLU = (66, 120, 255)
VD_BLU = (31, 38, 107)
BG_COL = (52, 68, 140)
WHITE = (255, 255, 255)
GREY = (42, 43, 66)

# Map colors to game elements
COLORS = {
    "P1": D_BLU,            # First player color
    "P2": L_BLU,            # Second player color
    "board": VD_BLU,        # Board background
    "line": WHITE,          # Grid lines
    "text": WHITE,          # Text color
    "highlight": WHITE,     # Selection highlight
    "background": BG_COL    # Screen background
}

# Create the screen
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gobblet Jr.")


class Piece:
    """
    Represents a game piece with a color and size.

    Attributes:
        color (str): The color of the piece ('P1' or 'P2')
        size (str): The size of the piece ('small', 'medium', or 'large')
        radius (int): The visual radius of the piece
        on_board (bool): Whether the piece is currently on the board
        position (tuple): The (row, col) position of the piece on the board
    """
    def __init__(self, color, size):
        """Initialize a new piece with the given color and size."""
        self.color = color
        self.size = size
        self.radius = PIECE_RADIUS[size]
        self.on_board = False
        self.position = None

    def draw(self, x_pos, y_pos):
        """Draw the piece at the specified position."""
        pygame.draw.circle(SCREEN, COLORS[self.color], (x_pos, y_pos), self.radius)
        pygame.draw.circle(SCREEN, GREY, (x_pos, y_pos), self.radius, 2)  # Border

    def can_cover(self, other_piece):
        """Check if this piece can cover another piece."""
        if other_piece is None:
            return True
        size_index = PIECE_SIZES.index(self.size)
        other_size_index = PIECE_SIZES.index(other_piece.size)
        return size_index > other_size_index


class Board:
    """
    Represents the game board and manages piece placement.

    Attributes:
        grid (list): A 3D list representing the board state and piece stacks
    """
    def __init__(self):
        """Initialize an empty game board."""
        self.grid = [[[] for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def place_piece(self, piece, row, col):
        """
        Place a piece at the specified position if valid.

        Args:
            piece (Piece): The piece to place
            row (int): The row index
            col (int): The column index

        Returns:
            bool: True if the piece was successfully placed, False otherwise
        """
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            if not self.grid[row][col] or piece.can_cover(self.grid[row][col][-1]):
                piece.on_board = True
                piece.position = (row, col)
                self.grid[row][col].append(piece)
                return True
        return False

    def remove_piece(self, row, col):
        """
        Remove and return the top piece at the specified position.

        Args:
            row (int): The row index
            col (int): The column index

        Returns:
            Piece or None: The removed piece, or None if no piece was found
        """
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.grid[row][col]:
            piece = self.grid[row][col].pop()
            piece.on_board = False
            piece.position = None
            return piece
        return None

    def get_top_piece(self, row, col):
        """
        Get the top piece at the specified position without removing it.

        Args:
            row (int): The row index
            col (int): The column index

        Returns:
            Piece or None: The top piece, or None if no piece was found
        """
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.grid[row][col]:
            return self.grid[row][col][-1]
        return None

    def draw(self):
        """Draw the game board and all visible pieces."""
        # Draw board background
        pygame.draw.rect(SCREEN, COLORS["board"],
                        (BOARD_OFFSET_X - 10, BOARD_OFFSET_Y - 10,
                        BOARD_SIZE * SQUARE_SIZE + 20, BOARD_SIZE * SQUARE_SIZE + 20))

        # Draw grid lines
        for i in range(BOARD_SIZE + 1):
            # Vertical lines
            pygame.draw.line(SCREEN, COLORS["line"],
                            (BOARD_OFFSET_X + i * SQUARE_SIZE,
                             BOARD_OFFSET_Y),
                            (BOARD_OFFSET_X + i * SQUARE_SIZE,
                             BOARD_OFFSET_Y + BOARD_SIZE * SQUARE_SIZE),
                            3)
            # Horizontal lines
            pygame.draw.line(SCREEN, COLORS["line"],
                            (BOARD_OFFSET_X,
                             BOARD_OFFSET_Y + i * SQUARE_SIZE),
                            (BOARD_OFFSET_X + BOARD_SIZE * SQUARE_SIZE,
                             BOARD_OFFSET_Y + i * SQUARE_SIZE),
                            3)

        # Draw pieces on the board
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.grid[row][col]:
                    piece = self.grid[row][col][-1]  # Get the top piece
                    x_pos = BOARD_OFFSET_X + col * SQUARE_SIZE + SQUARE_SIZE // 2
                    y_pos = BOARD_OFFSET_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2
                    piece.draw(x_pos, y_pos)

    def check_win(self, color):
        """
        Check if the specified color has won the game.

        Args:
            color (str): The color to check ('P1' or 'P2')

        Returns:
            bool: True if the specified color has won, False otherwise
        """
        # Check rows
        for row in range(BOARD_SIZE):
            if all(self.grid[row][col] and self.grid[row][col][-1].color == color
                   for col in range(BOARD_SIZE)):
                return True

        # Check columns
        for col in range(BOARD_SIZE):
            if all(self.grid[row][col] and self.grid[row][col][-1].color == color
                   for row in range(BOARD_SIZE)):
                return True

        # Check diagonal
        if all(self.grid[i][i] and self.grid[i][i][-1].color == color
               for i in range(BOARD_SIZE)):
            return True

        # Check anti-diagonal
        if all(self.grid[i][BOARD_SIZE - 1 - i] and
               self.grid[i][BOARD_SIZE - 1 - i][-1].color == color
               for i in range(BOARD_SIZE)):
            return True

        return False

    def is_full(self):
        """
        Check if the board is full.

        Returns:
            bool: True if all positions have at least one piece, False otherwise
        """
        return all(len(self.grid[row][col]) > 0
                   for row in range(BOARD_SIZE)
                   for col in range(BOARD_SIZE))


class GobbletGame:
    """
    Manages the game state and controls the game flow.

    Attributes:
        board (Board): The game board
        players (list): The player colors
        current_player (int): The index of the current player
        selected_piece (Piece or None): The currently selected piece
        winner (str or None): The winning color, or None if no winner yet
        game_over (bool): Whether the game has ended
        reserve_pieces (dict): The pieces not yet on the board for each player
    """
    def __init__(self):
        """Initialize a new game."""
        self.board = Board()
        self.players = ["P1", "P2"]
        self.current_player = 0
        self.selected_piece = None
        self.winner = None
        self.game_over = False

        # Initialize pieces for each player (2 of each size)
        self.reserve_pieces = {
            "P1": [],
            "P2": []
        }

        for color in self.players:
            for size in PIECE_SIZES:
                for _ in range(2):  # 2 pieces of each size
                    self.reserve_pieces[color].append(Piece(color, size))

    def draw(self):
        """Draw the current game state."""
        SCREEN.fill(COLORS["background"])  # Set background color

        # Draw board
        self.board.draw()

        # Draw player turn information
        current_color = self.players[self.current_player]
        font = pygame.font.SysFont(None, 36)
        if self.game_over:
            if self.winner:
                text = f"{self.winner.capitalize()} wins!"
            else:
                text = "Game ends in a draw!"
        else:
            text = f"{current_color.capitalize()}'s turn"
        text_surface = font.render(text, True, COLORS["text"])
        SCREEN.blit(text_surface,
                   (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 50))

        # Draw reserve pieces
        self.draw_reserve_pieces()

        # Draw selection highlight
        if self.selected_piece:
            pygame.draw.circle(SCREEN, COLORS["highlight"],
                              self.get_piece_position(self.selected_piece),
                              self.selected_piece.radius + 5, 3)

        pygame.display.flip()

    def draw_reserve_pieces(self):
        """Draw the reserve pieces for both players."""
        # P1 player reserves (top)
        x_start = 100
        y_pos = 120
        spacing = 80
        for i, piece in enumerate(self.reserve_pieces["P1"]):
            if not piece.on_board:
                x_pos = x_start + i * spacing
                piece.draw(x_pos, y_pos)

        # P2 player reserves (bottom)
        y_pos = SCREEN_HEIGHT - 120
        for i, piece in enumerate(self.reserve_pieces["P2"]):
            if not piece.on_board:
                x_pos = x_start + i * spacing
                piece.draw(x_pos, y_pos)

    def get_piece_position(self, piece):
        """
        Get the screen position of a piece.

        Args:
            piece (Piece): The piece to locate

        Returns:
            tuple: The (x, y) screen coordinates of the piece
        """
        if piece.on_board and piece.position:
            row, col = piece.position
            return (BOARD_OFFSET_X + col * SQUARE_SIZE + SQUARE_SIZE // 2,
                    BOARD_OFFSET_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2)

        # For reserve pieces
        color = piece.color
        y_pos = 120 if color == "P1" else SCREEN_HEIGHT - 120
        x_start = 100
        spacing = 80

        for i, reserve_piece in enumerate(self.reserve_pieces[color]):
            if reserve_piece == piece:
                return (x_start + i * spacing, y_pos)

        return (0, 0)  # Default fallback

    def get_clicked_piece(self, pos):
        """
        Get the piece at the clicked position.

        Args:
            pos (tuple): The (x, y) screen coordinates of the click

        Returns:
            Piece or None: The clicked piece, or None if no piece was clicked
        """
        # Check reserve pieces first
        current_color = self.players[self.current_player]
        for piece in self.reserve_pieces[current_color]:
            if not piece.on_board:
                piece_pos = self.get_piece_position(piece)
                distance = ((pos[0] - piece_pos[0]) ** 2 +
                            (pos[1] - piece_pos[1]) ** 2) ** 0.5
                if distance <= piece.radius:
                    return piece

        # Check board pieces (only current player's pieces)
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board.get_top_piece(row, col)
                if piece and piece.color == current_color:
                    x_pos = BOARD_OFFSET_X + col * SQUARE_SIZE + SQUARE_SIZE // 2
                    y_pos = BOARD_OFFSET_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2
                    distance = ((pos[0] - x_pos) ** 2 + (pos[1] - y_pos) ** 2) ** 0.5
                    if distance <= piece.radius:
                        return piece

        return None

    def get_board_position(self, pos):
        """
        Convert screen coordinates to board grid position.

        Args:
            pos (tuple): The (x, y) screen coordinates

        Returns:
            tuple or None: The (row, col) board position, or None if outside the board
        """
        # Convert screen coordinates to board grid position
        if (BOARD_OFFSET_X <= pos[0] <= BOARD_OFFSET_X + BOARD_SIZE * SQUARE_SIZE and
            BOARD_OFFSET_Y <= pos[1] <= BOARD_OFFSET_Y + BOARD_SIZE * SQUARE_SIZE):

            col = (pos[0] - BOARD_OFFSET_X) // SQUARE_SIZE
            row = (pos[1] - BOARD_OFFSET_Y) // SQUARE_SIZE

            return row, col

        return None

    def handle_click(self, pos):
        """
        Handle mouse click events.

        Args:
            pos (tuple): The (x, y) screen coordinates of the click
        """
        if self.game_over:
            return

        # First, check if a board position was clicked
        board_pos = self.get_board_position(pos)

        # If we have a selected piece and clicked on the board
        if self.selected_piece and board_pos:
            row, col = board_pos

            # If the piece is on the board, pick it up
            if self.selected_piece.on_board:
                old_row, old_col = self.selected_piece.position
                self.board.remove_piece(old_row, old_col)

            # Try to place the piece
            if self.board.place_piece(self.selected_piece, row, col):
                self.selected_piece = None

                # Check for win
                if self.board.check_win(self.players[self.current_player]):
                    self.winner = self.players[self.current_player]
                    self.game_over = True
                elif self.board.is_full():
                    self.game_over = True
                else:
                    # Switch players
                    self.current_player = 1 - self.current_player
            else:
                # If piece was picked up from the board, put it back
                if hasattr(self.selected_piece, 'position') and self.selected_piece.position:
                    old_row, old_col = self.selected_piece.position
                    self.board.place_piece(self.selected_piece, old_row, old_col)
                self.selected_piece = None

            return

        # If no piece is selected or placement failed, try to select a piece
        piece = self.get_clicked_piece(pos)
        if piece:
            self.selected_piece = piece

    def run(self):
        """Run the game loop."""
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_click(event.pos)

            self.draw()
            clock.tick(60)


# Run the game
if __name__ == "__main__":
    game = GobbletGame()
    game.run()
