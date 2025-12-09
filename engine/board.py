
from engine.piece import Piece
class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.initialize_board()

    def initialize_board(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]

        # Белые фигуры
        pieces = [
            ('rook', 7, 0), ('knight', 7, 1), ('bishop', 7, 2), ('queen', 7, 3),
            ('king', 7, 4), ('bishop', 7, 5), ('knight', 7, 6), ('rook', 7, 7)
        ]
        for piece_type, row, col in pieces:
            self.set_piece((row, col), Piece(piece_type, 'white'))

        for col in range(8):
            self.set_piece((6, col), Piece('pawn', 'white'))

        # Черные фигуры
        pieces = [
            ('rook', 0, 0), ('knight', 0, 1), ('bishop', 0, 2), ('queen', 0, 3),
            ('king', 0, 4), ('bishop', 0, 5), ('knight', 0, 6), ('rook', 0, 7)
        ]
        for piece_type, row, col in pieces:
            self.set_piece((row, col), Piece(piece_type, 'black'))

        for col in range(8):
            self.set_piece((1, col), Piece('pawn', 'black'))

    def get_piece(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None

    def set_piece(self, pos, piece):
        row, col = pos
        if 0 <= row < 8 and 0 <= col < 8:
            self.board[row][col] = piece

    def remove_piece(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            piece = self.board[row][col]
            self.board[row][col] = None
            return piece
        return None

    def move_piece(self, start_pos, end_pos):
        start_row, start_col = start_pos

        piece = self.get_piece(start_row, start_col)
        if piece:
            self.set_piece(end_pos, piece)
            self.remove_piece(start_row, start_col)

            if piece.piece_type in ['king', 'rook']:
                piece.has_moved = True

    def promote_pawn(self, pos, piece_type):
        row, col = pos
        piece = self.get_piece(row, col)
        if piece and piece.piece_type == 'pawn':
            piece.piece_type = piece_type

    def is_empty(self, row, col):
        return self.get_piece(row, col) is None

    def is_opponent_piece(self, row, col, color):
        piece = self.get_piece(row, col)
        return piece is not None and piece.color != color

    def get_king_position(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and piece.piece_type == 'king' and piece.color == color:
                    return row, col
        return None
