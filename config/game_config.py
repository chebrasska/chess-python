class GameConfig:
    def __init__(self):
        # Основные настройки
        self.GAME_TITLE = "Шахматы"
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 800
        self.BOARD_SIZE = 8
        self.SQUARE_SIZE = min(self.WINDOW_WIDTH, self.WINDOW_HEIGHT) // self.BOARD_SIZE
        self.FPS = 60

        # Цвета
        self.LIGHT_SQUARE = (240, 217, 181)
        self.DARK_SQUARE = (181, 136, 99)
        self.HIGHLIGHT_COLOR = (255, 255, 0, 128)
        self.VALID_MOVE_COLOR = (0, 255, 0, 100)
        self.BACKGROUND_COLOR = (50, 50, 50)

        # Настройки игры
        self.INITIAL_TIME = 600
