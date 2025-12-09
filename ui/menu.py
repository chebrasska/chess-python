import pygame


class MainMenu:
    def __init__(self, screen, config=None):
        self.screen = screen
        self.WINDOW_WIDTH = config.WINDOW_WIDTH if config else 800
        self.WINDOW_HEIGHT = config.WINDOW_HEIGHT if config else 800

        self.font = pygame.font.Font(None, 64)
        self.small_font = pygame.font.Font(None, 36)

        self.buttons = [
            {"text": "Новая игра", "action": "START_GAME"},
            {"text": "Выход", "action": "QUIT"}
        ]

        self.update_button_positions()

    def update_button_positions(self):
        center_x = self.WINDOW_WIDTH // 2
        center_y = self.WINDOW_HEIGHT // 2

        for i, button in enumerate(self.buttons):
            button_rect = pygame.Rect(0, 0, 250, 60)
            button_rect.center = (center_x, center_y + i * 80)
            button["rect"] = button_rect

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            for button in self.buttons:
                if button["rect"].collidepoint(pos):
                    return button["action"]
        return None

    def draw(self):
        self.screen.fill((50, 50, 50))

        title = self.font.render("ШАХМАТЫ", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.WINDOW_WIDTH // 2, 200))
        self.screen.blit(title, title_rect)

        for button in self.buttons:
            pygame.draw.rect(self.screen, (50, 50, 150), button["rect"])
            pygame.draw.rect(self.screen, (255, 255, 255), button["rect"], 3)

            text = self.small_font.render(button["text"], True, (255, 255, 255))
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)
