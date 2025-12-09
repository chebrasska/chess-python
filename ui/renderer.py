import pygame
import os


class ChessRenderer:
    def __init__(self, screen, config=None):
        self.screen = screen
        self.WINDOW_WIDTH = config.WINDOW_WIDTH
        self.WINDOW_HEIGHT = config.WINDOW_HEIGHT
        self.BOARD_SIZE = config.BOARD_SIZE
        self.SQUARE_SIZE = config.SQUARE_SIZE
        self.LIGHT_SQUARE = config.LIGHT_SQUARE
        self.DARK_SQUARE = config.DARK_SQUARE
        self.HIGHLIGHT_COLOR = config.HIGHLIGHT_COLOR
        self.VALID_MOVE_COLOR = config.VALID_MOVE_COLOR
        self.CHECK_COLOR = (255, 0, 0, 100)
        self.BACKGROUND_COLOR = getattr(config, 'BACKGROUND_COLOR', (50, 50, 50))

        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)

        self.piece_images = self.load_piece_images()

    def load_piece_images(self):
        images = {}

        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(current_dir)
        assets_dir = os.path.join(project_dir, 'assets', 'sprites')

        piece_types = ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']
        colors = ['white', 'black']

        for color in colors:
            images[color] = {}
            for piece_type in piece_types:
                filename = f"{color}_{piece_type}.png"
                filepath = os.path.join(assets_dir, filename)

                if os.path.exists(filepath):
                    image = pygame.image.load(filepath).convert_alpha()
                    image_size = int(self.SQUARE_SIZE * 0.8)
                    image = pygame.transform.smoothscale(image, (image_size, image_size))
                    images[color][piece_type] = image

        return images

    def get_board_position(self, mouse_pos):
        """Преобразует координаты мыши в координаты доски"""
        board_x = (self.screen.get_width() - self.BOARD_SIZE * self.SQUARE_SIZE) // 2
        board_y = (self.screen.get_height() - self.BOARD_SIZE * self.SQUARE_SIZE) // 2

        rel_x = mouse_pos[0] - board_x
        rel_y = mouse_pos[1] - board_y

        if 0 <= rel_x < self.BOARD_SIZE * self.SQUARE_SIZE and \
                0 <= rel_y < self.BOARD_SIZE * self.SQUARE_SIZE:
            col = rel_x // self.SQUARE_SIZE
            row = rel_y // self.SQUARE_SIZE
            return int(row), int(col)
        return None, None

    def draw_board(self, board):
        board_x = (self.screen.get_width() - self.BOARD_SIZE * self.SQUARE_SIZE) // 2
        board_y = (self.screen.get_height() - self.BOARD_SIZE * self.SQUARE_SIZE) // 2

        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                color = self.LIGHT_SQUARE if (row + col) % 2 == 0 else self.DARK_SQUARE
                rect = pygame.Rect(
                    board_x + col * self.SQUARE_SIZE,
                    board_y + row * self.SQUARE_SIZE,
                    self.SQUARE_SIZE,
                    self.SQUARE_SIZE
                )
                pygame.draw.rect(self.screen, color, rect)

    def draw_pieces(self, board):
        board_x = (self.screen.get_width() - 8 * self.SQUARE_SIZE) // 2
        board_y = (self.screen.get_height() - 8 * self.SQUARE_SIZE) // 2

        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece:
                    # Пробуем нарисовать изображение
                    if (piece.color in self.piece_images and
                            piece.piece_type in self.piece_images[piece.color]):

                        image = self.piece_images[piece.color][piece.piece_type]
                        if isinstance(image, pygame.Surface):
                            # Это изображение
                            image_rect = image.get_rect(center=(
                                board_x + col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                                board_y + row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                            ))
                            self.screen.blit(image, image_rect)

    def highlight_square(self, square):
        row, col = square
        board_x = (self.screen.get_width() - 8 * self.SQUARE_SIZE) // 2
        board_y = (self.screen.get_height() - 8 * self.SQUARE_SIZE) // 2

        rect = pygame.Rect(
            board_x + col * self.SQUARE_SIZE,
            board_y + row * self.SQUARE_SIZE,
            self.SQUARE_SIZE,
            self.SQUARE_SIZE
        )

        # Создаем поверхность с альфа-каналом для полупрозрачности
        highlight_surface = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pygame.SRCALPHA)
        highlight_surface.fill(self.HIGHLIGHT_COLOR)
        self.screen.blit(highlight_surface, rect)

    def highlight_moves(self, moves):
        board_x = (self.screen.get_width() - 8 * self.SQUARE_SIZE) // 2
        board_y = (self.screen.get_height() - 8 * self.SQUARE_SIZE) // 2

        for row, col in moves:
            rect = pygame.Rect(
                board_x + col * self.SQUARE_SIZE,
                board_y + row * self.SQUARE_SIZE,
                self.SQUARE_SIZE,
                self.SQUARE_SIZE
            )

            # Создаем поверхность с альфа-каналом для полупрозрачности
            highlight_surface = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pygame.SRCALPHA)
            highlight_surface.fill(self.VALID_MOVE_COLOR)
            self.screen.blit(highlight_surface, rect)

            # Рисуем круг в центре клетки
            center_x = rect.x + self.SQUARE_SIZE // 2
            center_y = rect.y + self.SQUARE_SIZE // 2
            radius = self.SQUARE_SIZE // 6

            pygame.draw.circle(self.screen, (0, 100, 0, 150), (center_x, center_y), radius, 3)

    def draw_game_info(self, game):
        # Рисуем информацию о текущем игроке
        player_text = f"Ходят: {'Белые' if game.current_player == 'white' else 'Черные'}"
        text = self.small_font.render(player_text, True, (255, 255, 255))
        self.screen.blit(text, (20, 20))

        # Рисуем информацию о шахе
        if hasattr(game, 'is_in_check'):
            opponent = 'black' if game.current_player == 'white' else 'white'

    def draw_game_over(self, winner):
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        if winner:
            texts = [
                "Игра окончена!",
                f"Победили {'Белые' if winner == 'white' else 'Черные'}!",
                "Король взят!"
            ]
        else:
            texts = [
                "Игра окончена!",
                f"Победили {'Белые' if winner == 'white' else 'Черные'}!",
            ]

        # Рисуем текст
        for i, text_line in enumerate(texts):
            text = self.font.render(text_line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 - 100 + i * 60))
            self.screen.blit(text, text_rect)

        # Кнопка "Новая игра"
        button_rect = pygame.Rect(self.WINDOW_WIDTH // 2 - 100,
                                  self.WINDOW_HEIGHT // 2 + 80,
                                  200, 50)
        pygame.draw.rect(self.screen, (50, 150, 50), button_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 3)

        button_text = self.small_font.render("Новая игра", True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=button_rect.center)
        self.screen.blit(button_text, button_text_rect)

        # Кнопка "Вернуться в меню"
        menu_button_rect = pygame.Rect(self.WINDOW_WIDTH // 2 - 100,
                                       self.WINDOW_HEIGHT // 2 + 150,
                                       200, 50)
        pygame.draw.rect(self.screen, (150, 50, 50), menu_button_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), menu_button_rect, 3)

        menu_button_text = self.small_font.render("Вернуться в меню", True, (255, 255, 255))
        menu_button_text_rect = menu_button_text.get_rect(center=menu_button_rect.center)
        self.screen.blit(menu_button_text, menu_button_text_rect)

        return button_rect, menu_button_rect
