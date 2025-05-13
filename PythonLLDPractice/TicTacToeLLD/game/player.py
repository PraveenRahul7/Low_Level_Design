from .playing_piece import PlayingPiece


class Player:
    """Represents a player in the game."""
    def __init__(self, name: str, piece: PlayingPiece):
        self.name = name
        self.piece = piece

    def get_playing_piece(self):
        return self.piece

    def get_name(self):
        return self.name
