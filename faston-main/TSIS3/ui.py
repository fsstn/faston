import pygame

class Button:
    def __init__(self, x, y, w, h, text, color=(200, 200, 200), hover_color=(150, 150, 150)):
        # set up the button's position, text, and colors
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        # draw the button, and change color if the mouse is over it
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(surface, current_color, self.rect)
        pygame.draw.rect(surface, (0,0,0), self.rect, 2)
        text_surf = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        # check if the button was clicked
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class TextInput:
    def __init__(self, x, y, w, h):
        # set up the text input box
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ""
        self.font = pygame.font.Font(None, 36)

    def handle_event(self, event):
        # handle key presses for typing
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isprintable() and len(self.text) < 15:
                self.text += event.unicode

    def draw(self, surface):
        # draw the box and the text inside it
        pygame.draw.rect(surface, (255, 255, 255), self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        text_surf = self.font.render(self.text, True, (0, 0, 0))
        surface.blit(text_surf, (self.rect.x + 10, self.rect.y + 10))