import pygame, pathlib
pygame.init()
pygame.font.init()

def draw_text(screen: pygame.Surface, text: str,
    font_file: str,
    font_size: int, color: tuple, pos: tuple, backg=None):
    font = pygame.font.Font(pathlib.Path(font_file), font_size)
    if backg == None:
        t = font.render(text, True, color)
    t = font.render(text, True, color, backg)
    textRect = t.get_rect()
    textRect.center = pos
    screen.blit(t, textRect)

def get_text_width(text: str, font_file: str, font_size: int) -> pygame.Rect:
    font = pygame.font.Font(pathlib.Path(font_file), font_size)
    t = font.render(text, 1, (0,0,0))
    textRect = t.get_rect()
    width = textRect.width
    return width
    

class DataBox:
    def __init__(self, screen: pygame.Surface, horizontal_padding, vertical_padding, x, y, data: list, font_size: int, font_file: str, text_color: tuple, text_background=None):
        self.screen = screen
        self.x = x
        self.y = y
        self.data = data
        self.draw_scale = font_size
        self.horizontal_padding = horizontal_padding
        self.vertical_padding = vertical_padding
        self.font_file = font_file
        self.text_color = text_color
        self.font_size = self.draw_scale
        self.text_background = text_background
        self.width = get_text_width(max(self.data), self.font_file, self.font_size)*self.horizontal_padding
        self.box_rect = pygame.Rect(self.x, self.y-self.draw_scale, self.width, len(self.data)*self.draw_scale*self.vertical_padding)

    def draw(self, color: tuple, border_radius=None, outline=False, outline_width=1,
            outline_color=(0,0,0)):
        if border_radius:
            border_radius = border_radius
        if outline == True:
            pygame.draw.rect(self.screen, color, self.box_rect, width=0, border_radius=border_radius) # draws rectangle
            pygame.draw.rect(self.screen, outline_color, self.box_rect, outline_width, border_radius) # draws outline
        elif outline == False:
            pygame.draw.rect(self.screen, color, self.box_rect) # draws only rectangle
            
        # Drawing Text Elements
        for i, element in enumerate(self.data):
            text_x = self.box_rect.x + self.box_rect.width / 2
            text_y = self.box_rect.y + self.draw_scale * (2*i) if i != 0 else self.box_rect.y + self.draw_scale + outline_width
            if i > 0:
                text_y = text_y + self.draw_scale + outline_width
            draw_text(self.screen, element, self.font_file, self.font_size, self.text_color, (text_x, text_y), self.text_background)


class ColoredDataBox:
    def __init__(self, screen: pygame.Surface, horizontal_padding, vertical_padding, x, y, data: list, font_size: int, font_file: str, text_colors: list, text_background=None):
        self.screen = screen
        self.x = x
        self.y = y
        self.data = data
        self.draw_scale = font_size
        self.horizontal_padding = horizontal_padding
        self.vertical_padding = vertical_padding
        self.font_file = font_file
        self.text_colors = text_colors
        self.font_size = self.draw_scale
        self.text_background = text_background
        self.width = get_text_width(max(self.data), self.font_file, self.font_size)*self.horizontal_padding
        self.box_rect = pygame.Rect(self.x, self.y-self.draw_scale, self.width, len(self.data)*self.draw_scale*self.vertical_padding)

    def draw(self, color: tuple, border_radius=None, outline=False, outline_width=1,
            outline_color=(0,0,0)):
        if border_radius:
            border_radius = border_radius
        if outline == True:
            pygame.draw.rect(self.screen, color, self.box_rect, width=0, border_radius=border_radius) # draws rectangle
            pygame.draw.rect(self.screen, outline_color, self.box_rect, outline_width, border_radius) # draws outline
        elif outline == False:
            pygame.draw.rect(self.screen, color, self.box_rect) # draws only rectangle
            
        # Drawing Text Elements
        for i, element in enumerate(self.data):
            text_x = self.box_rect.x + self.box_rect.width / 2
            text_y = self.box_rect.y + self.draw_scale * (2*i) if i != 0 else self.box_rect.y + self.draw_scale + outline_width
            if i > 0:
                text_y = text_y + self.draw_scale + outline_width
            draw_text(self.screen, element, self.font_file, self.font_size, self.text_colors[i], (text_x, text_y), self.text_background)