class ChessGame:
    def __init__(self):
        from engine.board import ChessBoard
        from engine.move_validator import MoveValidator

        self.board = ChessBoard()
        self.move_validator = MoveValidator(self.board)
        self.current_player = 'white'
        self.move_history = []
        self.game_over = False
        self.winner = None

    def reset_game(self):
        self.board.initialize_board()
        self.current_player = 'white'
        self.move_history = []
        self.game_over = False
        self.winner = None

    def get_valid_moves(self, row, col):
        piece = self.board.get_piece(row, col)
        if piece and piece.color == self.current_player:
            return self.move_validator.get_valid_moves(piece, row, col, self.current_player)
        return []

    def make_move(self, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        piece = self.board.get_piece(start_row, start_col)
        if not piece or piece.color != self.current_player:
            return False

        valid_moves = self.get_valid_moves(start_row, start_col)
        if (end_row, end_col) not in valid_moves:
            return False

        target_piece = self.board.get_piece(end_row, end_col)
        move_info = {
            'start': start_pos,
            'end': end_pos,
            'piece': piece,
            'captured': target_piece,
            'promotion': None
        }

        self.board.move_piece(start_pos, end_pos)

        if target_piece and target_piece.piece_type == 'king':
            self.game_over = True
            self.winner = self.current_player
            self.move_history.append(move_info)
            return True

        if piece.piece_type == 'pawn' and (end_row == 0 or end_row == 7):
            self.board.promote_pawn(end_pos, 'queen')
            move_info['promotion'] = 'queen'

        self.move_history.append(move_info)

        opponent = 'black' if self.current_player == 'white' else 'white'

        if self.is_checkmate(opponent):
            self.game_over = True
            self.winner = self.current_player
        elif self.is_stalemate(opponent):
            self.game_over = True
            self.winner = None

        if not self.game_over:
            self.current_player = opponent

        return True

    def is_in_check(self, color):
        return self.move_validator.is_king_in_check(color)

    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False

        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == color:
                    valid_moves = self.move_validator.get_valid_moves(piece, row, col, color)
                    if valid_moves:
                        return False

        return True

    def is_stalemate(self, color):
        if self.is_in_check(color):
            return False

        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == color:
                    valid_moves = self.move_validator.get_valid_moves(piece, row, col, color)
                    if valid_moves:
                        return False

        return True

    def undo_move(self):
        if not self.move_history:
            return

        move_info = self.move_history.pop()
        self.game_over = False
        self.winner = None

        self.board.move_piece(move_info['end'], move_info['start'])

        if move_info['captured']:
            self.board.set_piece(move_info['end'], move_info['captured'])

        if move_info['promotion']:
            piece = self.board.get_piece(move_info['start'])
            if piece:
                piece.piece_type = 'pawn'

        self.current_player = 'black' if self.current_player == 'white' else 'white'
