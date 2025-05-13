# game/board.py

from PythonLLDPractice.TicTacToeLLD.game.playing_piece import PlayingPiece
from PythonLLDPractice.TicTacToeLLD.utils.logger import *

class Board:
    """Represents the game board and its operations."""
    def __init__(self, size=3):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        log_info(f"Board initialized with size {size}x{size}")

    def add_piece(self, row: int, col: int, piece: PlayingPiece):
        """Adds a piece to the board if the move is valid."""
        if self.is_valid_move(row, col):
            self.grid[row][col] = piece
            log_info(f"Piece {piece.get_piece_type().value} added at ({row}, {col})")
            return True
        else:
            log_error(f"Invalid Move at ({row}, {col})")
            print("Invalid Move! Try again.")
            return False

    def is_valid_move(self, row: int, col: int):
        """Checks if the move is valid (inside bounds and empty)."""
        return 0 <= row < self.size and 0 <= col < self.size and self.grid[row][col] is None

    def print_board(self):
        """Displays the current state of the board."""
        for row in self.grid:
            print("|".join([p.get_piece_type().value if p else " " for p in row]))
            print("-" * (self.size * 2 - 1))

    def is_winner(self, piece: PlayingPiece):
        """Checks if the given piece has a winning line on the board."""
        piece_type = piece.get_piece_type()

        # Check rows
        for row in self.grid:
            if all(cell and cell.get_piece_type() == piece_type for cell in row):
                return True

        # Check columns
        for col in range(self.size):
            if all(self.grid[row][col] and self.grid[row][col].get_piece_type() == piece_type for row in range(self.size)):
                return True

        # Check diagonals
        if all(self.grid[i][i] and self.grid[i][i].get_piece_type() == piece_type for i in range(self.size)):
            return True
        if all(self.grid[i][self.size - i - 1] and self.grid[i][self.size - i - 1].get_piece_type() == piece_type for i in range(self.size)):
            return True

        return False

    def is_full(self):
        """Checks if the board is full (draw condition)."""
        return all(cell is not None for row in self.grid for cell in row)
