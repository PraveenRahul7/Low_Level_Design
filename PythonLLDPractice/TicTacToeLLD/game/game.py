# game/game.py

from .board import Board
from .player import Player
from .playing_piece import PlayingPieceX, PlayingPieceO
from PythonLLDPractice.TicTacToeLLD.utils.logger import *

class TicTacToeGame:
    """Main game controller."""
    def __init__(self):
        self.board = Board()
        self.players = [
            Player("Player 1", PlayingPieceX()),
            Player("Player 2", PlayingPieceO())
        ]
        self.current_turn = 0
        log_info("Game initialized with Player 1 (X) and Player 2 (O)")

    def switch_turn(self):
        """Switches the turn to the next player."""
        self.current_turn = 1 - self.current_turn
        log_info(f"Turn switched to {self.players[self.current_turn].get_name()}")

    def start_game(self):
        """Starts the game loop."""
        print("Starting Tic-Tac-Toe Game!")
        log_info("Game Started")
        self.board.print_board()

        while True:
            current_player = self.players[self.current_turn]
            print(f"{current_player.get_name()}'s turn ({current_player.get_playing_piece().get_piece_type().value})")

            try:
                row, col = map(int, input("Enter row and column (0, 1, 2): ").split())
            except ValueError:
                print("Invalid input! Please enter two integers.")
                continue

            if self.board.add_piece(row, col, current_player.get_playing_piece()):
                self.board.print_board()

                if self.board.is_winner(current_player.get_playing_piece()):
                    print(f"{current_player.get_name()} wins!")
                    log_info(f"{current_player.get_name()} wins the game!")
                    break
                elif self.board.is_full():
                    print("Game is a Draw!")
                    log_info("Game ended in a Draw.")
                    break
                else:
                    self.switch_turn()
