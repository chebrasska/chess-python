import pygame
import sys
from engine.game_engine import ChessGame
from ui.renderer import ChessRenderer
from ui.menu import MainMenu


def main():
    pygame.init()
    pygame.mixer.init()  # Инициализация звуковой системы

    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 800
    SQUARE_SIZE = WINDOW_HEIGHT // 8
    FPS = 60

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Шахматы")
    clock = pygame.time.Clock()

    game = ChessGame()

    class SimpleConfig:
        def __init__(self):
            self.WINDOW_WIDTH = WINDOW_WIDTH
            self.WINDOW_HEIGHT = WINDOW_HEIGHT
            self.BOARD_SIZE = 8
            self.SQUARE_SIZE = SQUARE_SIZE
            self.FPS = FPS
            self.LIGHT_SQUARE = (240, 217, 181)
            self.DARK_SQUARE = (181, 136, 99)
            self.HIGHLIGHT_COLOR = (255, 255, 0, 128)
            self.VALID_MOVE_COLOR = (0, 255, 0, 100)
            self.BACKGROUND_COLOR = (50, 50, 50)

    config = SimpleConfig()
    renderer = ChessRenderer(screen, config)
    menu = MainMenu(screen, config)

    current_state = "MENU"
    selected_square = None
    valid_moves = []
    game_over = False
    winner = None
    victory_sound_played = False  # Флаг, чтобы звук победы воспроизводился только один раз

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if current_state == "MENU":
                action = menu.handle_event(event)
                if action == "START_GAME":
                    current_state = "GAME"
                    game.reset_game()
                    game_over = False
                    winner = None
                    selected_square = None
                    valid_moves = []
                    victory_sound_played = False  # Сбрасываем флаг звука
                elif action == "QUIT":
                    pygame.quit()
                    sys.exit()

            elif current_state == "GAME" and not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    row, col = renderer.get_board_position(pos)

                    if row is not None and col is not None:
                        if selected_square:
                            move_result = game.make_move(selected_square, (row, col))
                            if move_result:
                                selected_square = None
                                valid_moves = []

                                if game.game_over:
                                    game_over = True
                                    winner = game.winner
                                    victory_sound_played = False  # Сбрасываем флаг при новой победе
                            else:
                                piece = game.board.get_piece(row, col)
                                if piece and piece.color == game.current_player:
                                    selected_square = (row, col)
                                    valid_moves = game.get_valid_moves(row, col)
                                else:
                                    selected_square = None
                                    valid_moves = []
                        else:
                            piece = game.board.get_piece(row, col)
                            if piece and piece.color == game.current_player:
                                selected_square = (row, col)
                                valid_moves = game.get_valid_moves(row, col)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        current_state = "MENU"
                        victory_sound_played = False  # Сбрасываем флаг звука
                    elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        game.undo_move()
                        game_over = False
                        winner = None
                        valid_moves = []
                        selected_square = None
                        victory_sound_played = False  # Сбрасываем флаг звука

            elif current_state == "GAME" and game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    new_game_rect, menu_rect = renderer.draw_game_over(winner)

                    if new_game_rect.collidepoint(pos):
                        game.reset_game()
                        game_over = False
                        winner = None
                        selected_square = None
                        valid_moves = []
                        victory_sound_played = False  # Сбрасываем флаг звука
                    elif menu_rect.collidepoint(pos):
                        current_state = "MENU"
                        victory_sound_played = False  # Сбрасываем флаг звука
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        current_state = "MENU"
                        victory_sound_played = False  # Сбрасываем флаг звука
                    elif event.key == pygame.K_SPACE:
                        game.reset_game()
                        game_over = False
                        winner = None
                        selected_square = None
                        valid_moves = []
                        victory_sound_played = False  # Сбрасываем флаг звука

        screen.fill(config.BACKGROUND_COLOR)

        if current_state == "MENU":
            menu.draw()
        elif current_state == "GAME":
            renderer.draw_board(game.board)

            if selected_square:
                renderer.highlight_square(selected_square)
                renderer.highlight_moves(valid_moves)

            renderer.draw_pieces(game.board)
            renderer.draw_game_info(game)

            if game_over:
                # Воспроизводим звук победы один раз
                if not victory_sound_played:
                    renderer.play_victory_sound()
                    victory_sound_played = True

                renderer.draw_game_over(winner)

        pygame.display.flip()
        clock.tick(FPS)


main()
