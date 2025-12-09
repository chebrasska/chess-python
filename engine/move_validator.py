class MoveValidator:
    def __init__(self, board):
        self.board = board

    def get_valid_moves(self, piece, row, col, player_color):
        if piece.color != player_color:
            return []
        moves = self.get_all_possible_moves(piece, row, col)
        valid_moves = []
        for move_row, move_col in moves:
            valid_moves.append((move_row, move_col))

        return valid_moves

    def get_all_possible_moves(self, piece, row, col):
        if piece.piece_type == 'pawn':
            return self.get_pawn_moves(piece, row, col)
        elif piece.piece_type == 'rook':
            return self.get_rook_moves(piece, row, col)
        elif piece.piece_type == 'knight':
            return self.get_knight_moves(piece, row, col)
        elif piece.piece_type == 'bishop':
            return self.get_bishop_moves(piece, row, col)
        elif piece.piece_type == 'queen':
            return self.get_queen_moves(piece, row, col)
        elif piece.piece_type == 'king':
            return self.get_king_moves(piece, row, col)
        return []

    def get_pawn_moves(self, pawn, row, col):
        moves = []
        direction = -1 if pawn.color == 'white' else 1

        new_row = row + direction
        if 0 <= new_row < 8 and self.board.is_empty(new_row, col):
            moves.append((new_row, col))

            start_row = 6 if pawn.color == 'white' else 1
            if row == start_row and self.board.is_empty(new_row + direction, col):
                moves.append((new_row + direction, col))

        for dcol in [-1, 1]:
            new_col = col + dcol
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if self.board.is_opponent_piece(new_row, new_col, pawn.color):
                    moves.append((new_row, new_col))

                adjacent_piece = self.board.get_piece(row, new_col)
                if (adjacent_piece and adjacent_piece.piece_type == 'pawn' and
                        adjacent_piece.color != pawn.color):
                    moves.append((new_row, new_col))

        return moves

    def get_rook_moves(self, rook, row, col):
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + dr * i, col + dc * i
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break

                if self.board.is_empty(new_row, new_col):
                    moves.append((new_row, new_col))
                elif self.board.is_opponent_piece(new_row, new_col, rook.color):
                    moves.append((new_row, new_col))
                    break
                else:
                    break

        return moves

    def get_knight_moves(self, knight, row, col):
        moves = []
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if self.board.is_empty(new_row, new_col) or \
                        self.board.is_opponent_piece(new_row, new_col, knight.color):
                    moves.append((new_row, new_col))

        return moves

    def get_bishop_moves(self, bishop, row, col):
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + dr * i, col + dc * i
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break

                if self.board.is_empty(new_row, new_col):
                    moves.append((new_row, new_col))
                elif self.board.is_opponent_piece(new_row, new_col, bishop.color):
                    moves.append((new_row, new_col))
                    break
                else:
                    break

        return moves

    def get_queen_moves(self, queen, row, col):
        # Ферзь = ладья + слон
        rook_moves = self.get_rook_moves(queen, row, col)
        bishop_moves = self.get_bishop_moves(queen, row, col)
        return rook_moves + bishop_moves

    def get_king_moves(self, king, row, col):
        moves = []
        king_moves = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        for dr, dc in king_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if self.board.is_empty(new_row, new_col) or \
                        self.board.is_opponent_piece(new_row, new_col, king.color):
                    moves.append((new_row, new_col))

        return moves



    def is_king_in_check(self, color):
        """Проверяет, находится ли король под шахом"""
        king_pos = self.board.get_king_position(color)
        if not king_pos:
            return True  # Если короля нет - это мат (король взят)

        return self.is_square_attacked(king_pos[0], king_pos[1], color)

    def is_square_attacked(self, row, col, color, board=None):
        if board is None:
            board = self.board

        opponent_color = 'black' if color == 'white' else 'white'

        # Проверяем атаки пешками
        pawn_direction = 1 if color == 'white' else -1
        for dcol in [-1, 1]:
            attack_row = row + pawn_direction
            attack_col = col + dcol
            if 0 <= attack_row < 8 and 0 <= attack_col < 8:
                piece = board.get_piece(attack_row, attack_col)
                if piece and piece.piece_type == 'pawn' and piece.color == opponent_color:
                    return True

        # Проверяем атаки конями
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        for dr, dc in knight_moves:
            attack_row, attack_col = row + dr, col + dc
            if 0 <= attack_row < 8 and 0 <= attack_col < 8:
                piece = board.get_piece(attack_row, attack_col)
                if piece and piece.piece_type == 'knight' and piece.color == opponent_color:
                    return True

        # Проверяем атаки по прямым линиям
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            for i in range(1, 8):
                attack_row, attack_col = row + dr * i, col + dc * i
                if not (0 <= attack_row < 8 and 0 <= attack_col < 8):
                    break

                piece = board.get_piece(attack_row, attack_col)
                if piece:
                    if piece.color == opponent_color and piece.piece_type in ['rook', 'queen']:
                        return True
                    break

        # Проверяем атаки по диагоналям
        for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            for i in range(1, 8):
                attack_row, attack_col = row + dr * i, col + dc * i
                if not (0 <= attack_row < 8 and 0 <= attack_col < 8):
                    break

                piece = board.get_piece(attack_row, attack_col)
                if piece:
                    if piece.color == opponent_color and piece.piece_type in ['bishop', 'queen']:
                        return True
                    break

        # Проверяем атаки королем
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                attack_row, attack_col = row + dr, col + dc
                if 0 <= attack_row < 8 and 0 <= attack_col < 8:
                    piece = board.get_piece(attack_row, attack_col)
                    if piece and piece.piece_type == 'king' and piece.color == opponent_color:
                        return True

        return False
