from .enums import PieceType


class PlayingPiece:
    """Base class representing a playing piece on the board."""
    def __init__(self, piece_type: PieceType):
        self.piece_type = piece_type

    def get_piece_type(self):
        return self.piece_type


class PlayingPieceX(PlayingPiece):
    """Concrete class representing an 'X' piece."""
    def __init__(self):
        super().__init__(PieceType.X)


class PlayingPieceO(PlayingPiece):
    """Concrete class representing an 'O' piece."""
    def __init__(self):
        super().__init__(PieceType.O)
