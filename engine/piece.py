
class Piece:
    def __init__(self, piece_type, color):
        self.piece_type = piece_type
        self.color = color
        self.has_moved = False

    def copy(self):
        new_piece = Piece(self.piece_type, self.color)
        new_piece.has_moved = self.has_moved
        return new_piece

    def __repr__(self):
        return f"{self.color} {self.piece_type}"
