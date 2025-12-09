import pygame


class HUD:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 32)

    def draw(self, game):
        text = f"Ходят: {'Белые' if game.current_player == 'white' else 'Черные'}"
        text_surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, (650, 50))

