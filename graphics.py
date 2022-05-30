import pygame, pathlib, typing
from colorsys import rgb_to_hls, hls_to_rgb
pygame.init()
pygame.font.init()

FONTS = {
    "default":"fonts/default_font.ttf",
    "button":"fonts/opensans_extrabold.ttf",
    "ui":"fonts/fira.ttf",
    "minecraft":"fonts/minecraft.ttf"
}

def draw_text(screen: pygame.Surface, text: str,
    font_file: str,
    font_size: int, color: tuple, pos: tuple, backg=None, bold=False, italic=False, underline=False):
    if '.ttf' in font_file:
        font = pygame.font.Font(pathlib.Path(font_file), font_size)
    else:
        font = pygame.font.SysFont(font_file, font_size)
    font.set_bold(bold)
    font.set_italic(italic)
    font.set_underline(underline)
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

class TextNode:
    """Text Object Representation aside functional `draw_text`, without the position
    argument. Drawing method takes positional argument."""
    def __init__(self, screen: pygame.Surface, font_file: str, text: str, 
    font_size: int, color: tuple, background_color=None):
        self.screen = screen
        self.font_file = font_file
        self.text = text
        self.font_size = font_size
        self.color = color
        self.background_color = background_color

    def draw(self, pos):
        draw_text(screen=self.screen, font_file=self.font_file, text=self.text, font_size=self.font_size, color=self.color, backg=self.background_color, pos=pos)

        
class Label:
    """Text Object Representation aside functional `draw_text`. Comes with the position argument."""
    def __init__(self, screen: pygame.Surface, font_file: str, text: str, 
    font_size: int, color: tuple, pos: tuple, background_color=None):
        self.screen = screen
        self.font_file = font_file
        self.text = text
        self.font_size = font_size
        self.color = color
        self.pos = pos
        self.background_color = background_color
        
    def draw(self):
        """Draws Text To the Screen based on Attrs."""
        draw_text(self.screen, self.font_file, self.text, self.font_size, self.color, self.pos, self.background_color)

def adjust_color_lightness(r, g, b, factor):
    h, l, s = rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    l = max(min(l * factor, 1.0), 0.0)
    r, g, b = hls_to_rgb(h, l, s)
    return int(r * 255), int(g * 255), int(b * 255)

def darken_color(r, g, b, factor=0.1):
    return adjust_color_lightness(r, g, b, 1 - factor)

class Button:
    """A clickable object that performs an operation when clicked."""
    def __init__(self, screen, x, y, width, height, color, text: str, font_size: int, border_width=0, border_radius=0, border_color=(0,0,0)):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = color
        self.original_color = self.color
        self.darker_color = darken_color(*self.color, 0.4)
        self.text = TextNode(self.screen, FONTS["button"], text, font_size, (255,255,255), None)
        self.border_width = border_width
        self.border_radius = border_radius
        self.border_color = border_color

    def onhover(self, mpos):
        """Does something when mouse is hovering over button."""
        if self.rect.collidepoint(mpos):
            self.color = self.darker_color
        else:
            self.color = self.original_color

    def draw(self, screen):
        """Draws the button to the screen every frame."""
        screen = self.screen
        if self.border_width > 0: # wether we can even see the border
            pygame.draw.rect(screen, self.color, self.rect, border_radius=self.border_radius)
            pygame.draw.rect(screen, self.border_color, self.rect, width=self.border_width, border_radius=self.border_radius)
            pygame.draw.rect(screen, (0,0,0), self.rect, width=1, border_radius=self.border_radius)
        else:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=self.border_radius)

        if self.text != None:
            self.text.draw(pos=self.rect.center)

    def clicked(self, mpos):
        if self.rect.collidepoint(mpos):
            return True
        else:
            return False

class ToggleButton:
    """A clickable object that turns on or off when clicked."""
    def __init__(self, screen, x, y, width, height, on_color, off_color, border_width=0, border_radius=0, border_color=(0,0,0), font_size=20, help_text=None):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.on_color = on_color
        self.off_color = off_color
        self.is_on = False
        self.text = TextNode(self.screen, FONTS["button"], "Off", font_size, (255,255,255), None)
        self.border_width = border_width
        self.border_radius = border_radius
        self.border_color = border_color
        self.help_text = help_text

    def draw(self, screen):
        """Draws the ToggleButton to the screen every frame."""
        screen = self.screen
        if self.is_on == False:
            color = self.off_color
            self.text.text = self.help_text + " Off" if self.help_text != None else "Off" # sets the text of the toggle button depending on the state of `is_on`.
        elif self.is_on == True:
            color = self.on_color
            self.text.text = self.help_text + " On" if self.help_text != None else "On"

        if self.border_width > 0: # wether we can even see the border
            pygame.draw.rect(screen, color, self.rect, border_radius=self.border_radius)
            pygame.draw.rect(screen, self.border_color, self.rect, width=self.border_width, border_radius=self.border_radius)
            pygame.draw.rect(screen, (0,0,0), self.rect, width=1, border_radius=self.border_radius)
        else:
            pygame.draw.rect(self.screen, color, self.rect, border_radius=self.border_radius)

        self.text.draw(pos=self.rect.center)

    def toggle(self, mpos):
        """Toggles the Button to be On or Off."""
        if self.rect.collidepoint(mpos):
            self.is_on = not self.is_on

class DataBox:
    def __init__(self, screen: pygame.Surface, horizontal_padding, vertical_padding, x, y, data: list, font_size: int, font_file: str, text_color: tuple, member_space_between_texts, text_background=None):
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
        self.member_space_between_texts = member_space_between_texts
        self.width = get_text_width(max(self.data), self.font_file, self.font_size)*self.horizontal_padding
        self.height = len(self.data)*self.draw_scale*self.vertical_padding
        self.box_rect = pygame.Rect(self.x, self.y-self.draw_scale, self.width, self.height)
    
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
        self.text_rects = []
        for i, element in enumerate(self.data):
            text_x = self.box_rect.x + self.box_rect.width / 2
            text_y = self.box_rect.y + self.draw_scale * (self.member_space_between_texts*i) if i != 0 else self.box_rect.y + self.draw_scale + outline_width
            if i > 0:
                text_y = text_y + self.draw_scale + outline_width
            text_rect = get_text_rect(self.font_file, element, self.font_size, (text_x, text_y))
            self.text_rects.append({"rect":text_rect, "text":element})
            draw_text(self.screen, element, self.font_file, self.font_size, self.text_color, (text_x, text_y), self.text_background)
            

class ColoredDataBox:
    def __init__(self, screen: pygame.Surface, horizontal_padding, vertical_padding, x, y, data: list, font_size: int, font_file: str, text_colors: list, legend_space_between_texts, text_background=None):
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
        self.legend_space_between_texts = legend_space_between_texts
        self.width = get_text_width(max(self.data), self.font_file, self.font_size)*self.horizontal_padding
        self.box_rect = pygame.Rect(self.x, self.y-self.draw_scale, self.width, len(self.data)*self.draw_scale*self.vertical_padding)

    def draw(self, color: tuple, border_radius=None, outline=False, outline_width=1,
            outline_color=(0,0,0)):
        if border_radius:
            border_radius = border_radius
        if outline == True:
            pygame.draw.rect(self.screen, color, pygame.Rect(self.x, self.box_rect.y, self.box_rect.width, self.box_rect.height), width=0, border_radius=border_radius) # draws rectangle
            pygame.draw.rect(self.screen, outline_color, pygame.Rect(self.x, self.box_rect.y, self.box_rect.width, self.box_rect.height), outline_width, border_radius) # draws outline
        elif outline == False:
            pygame.draw.rect(self.screen, color, pygame.Rect(self.x, self.box_rect.y, self.box_rect.width, self.box_rect.height)) # draws only rectangle
            
        # Drawing Text Elements
        for i, element in enumerate(self.data):
            text_x = pygame.Rect(self.x, self.box_rect.y, self.box_rect.width, self.box_rect.height).x +  pygame.Rect(self.x, self.box_rect.y, self.box_rect.width, self.box_rect.height).width / 2
            text_y = pygame.Rect(self.x, self.box_rect.y, self.box_rect.width, self.box_rect.height).y + self.draw_scale * (self.legend_space_between_texts*i) if i != 0 else self.box_rect.y + self.draw_scale + outline_width
            if i > 0:
                text_y = text_y + self.draw_scale + outline_width
            draw_text(self.screen, element, self.font_file, self.font_size, self.text_colors[i], (text_x, text_y), self.text_background)

class TextStyle:
    """Stores text style information without text, just the formatting."""
    def __init__(self, font_file: str, 
    font_size: int, color: tuple, background_color=None):
        self.font_file = font_file
        self.font_size = font_size
        self.color = color
        self.background_color = background_color


def get_text_rect(font_file, text, font_size, pos) -> pygame.Rect:
    """Returns the bounding rectangle of a text object drawn to the screen."""
    font = pygame.font.Font(font_file, font_size)
    t = font.render(text, 1, (0,0,0))
    textRect = t.get_rect()
    textRect.center = pos
    return textRect

class MenuBar:
    def __init__(self, screen: pygame.Surface, menu_options_dict: dict, bar_height: int, hover_color=(0,0,0), menu_hover_color=(255,255,255)):
        self.screen = screen
        self.x = 0
        self.y = 0
        self.bar_width = screen.get_width()
        self.menu_options_dict = menu_options_dict
        self.menu_names_list = [key for key in menu_options_dict.keys()]
        self.hovering_menu_title = None
        self.was_clicked = False
        self.hovering_option = None
        self.options = None
        self.selected_option = None
        self.bar_height = bar_height
        self.hover_color = hover_color
        self.menu_hover_color = menu_hover_color
        self.menu_space_factor = 10
        self.clicked = False

    def draw(self, bar_color=(131,139,139), text_style=TextStyle("fonts/fira.ttf", 20, (0,0,0), None), hide_options=False):
        # drawing the body of the menu bar.
        self.bar_rect = pygame.Rect(self.x, self.y, self.bar_width, self.bar_height)
        pygame.draw.rect(self.screen, bar_color, self.bar_rect)

        # drawing the menu titles.
        self.menu_titles = []
        for i in range(len(self.menu_names_list)):
            if i == 0:
                menu_title_x = self.bar_rect.x + 30
                menu_title_y = self.bar_rect.y/2+12
                menu_title = TextNode(self.screen, text_style.font_file, self.menu_names_list[i], text_style.font_size, text_style.color, text_style.background_color)
                menu_title_rect = get_text_rect(menu_title.font_file, menu_title.text, menu_title.font_size, (menu_title_x, menu_title_y))
                menu_options = self.menu_options_dict[self.menu_names_list[i]] # get the options by indexing with key
                first_x_y = (menu_title_x, menu_title_y)
            elif i > 0:
                menu_title_x = (first_x_y[0]*(i+1))+menu_title_rect.width + self.menu_space_factor
                menu_title_y = first_x_y[1]
                menu_title = TextNode(self.screen, text_style.font_file, self.menu_names_list[i], text_style.font_size, text_style.color, text_style.background_color)
                menu_title_rect = get_text_rect(menu_title.font_file, menu_title.text, menu_title.font_size, (menu_title_x, menu_title_y))
                menu_options = self.menu_options_dict[self.menu_names_list[i]] # get the options by indexing with key
            elif i == len(self.menu_names_list):
                menu_title_x = (first_x_y[0]*i)+menu_title_rect.width + self.menu_space_factor
                menu_title_y = first_x_y[1]
                menu_title = TextNode(self.screen, text_style.font_file, self.menu_names_list[i], text_style.font_size, text_style.color, text_style.background_color)
                menu_title_rect = get_text_rect(menu_title.font_file, menu_title.text, menu_title.font_size, (menu_title_x, menu_title_y))
                menu_options = self.menu_options_dict[self.menu_names_list[i]] # get the options by indexing with key
            self.menu_titles.append({"pos":(menu_title_x, menu_title_y), "title":menu_title, "rect":menu_title_rect, "options":menu_options, "index":i})

        # checking for the hovered menu titles.
        if self.hovering_menu_title != None:
            for i in range(len(self.menu_titles)):
                if self.menu_titles[i]["title"].text == self.hovering_menu_title.text:
                    self.menu_titles[i]["title"].color = self.hover_color
                    pygame.draw.rect(self.screen, self.menu_hover_color, self.menu_titles[i]["rect"])

        for i in range(len(self.menu_titles)):
            self.menu_titles[i]["title"].draw(self.menu_titles[i]["pos"])

        if self.options != None:
            self.options_list = [] # list with all gui elements of options.
            options = self.menu_options_dict[self.menu_titles[self.options["index"]]["title"].text]
            for i in range(len(options)):
                if i == 0:
                    option_x = self.menu_titles[self.options["index"]]["rect"].x
                    option_y = self.menu_titles[self.options["index"]]["rect"].y+self.bar_height
                    option_text = TextNode(self.screen, text_style.font_file, options[i], text_style.font_size, text_style.color, text_style.background_color)
                    option_text_rect = pygame.Rect(option_x, option_y, get_text_width(max(options, key=len), text_style.font_file, text_style.font_size), self.menu_titles[self.options["index"]]["rect"].height)
                    first_x_y = (option_x, option_y)
                elif i > 0:
                    option_x = first_x_y[0]
                    option_y = first_x_y[1]*(i+1)
                    option_text = TextNode(self.screen, text_style.font_file, options[i], text_style.font_size, text_style.color, text_style.background_color)
                    option_text_rect = pygame.Rect(option_x, option_y, get_text_width(max(options, key=len), text_style.font_file, text_style.font_size), self.menu_titles[self.options["index"]]["rect"].height)
                elif i == len(options):
                    option_x = first_x_y[0]
                    option_y = first_x_y[1]*(i)
                    option_text = TextNode(self.screen, text_style.font_file, options[i], text_style.font_size, text_style.color, text_style.background_color)
                    option_text_rect = pygame.Rect(option_x, option_y, get_text_width(max(options, key=len), text_style.font_file, text_style.font_size), self.menu_titles[self.options["index"]]["rect"].height)
                self.options_list.append({"pos":(option_x, option_y), "text":option_text, "rect":option_text_rect})


            if hasattr(self, "options_list"):
                for i in range(len(self.options_list)):
                    if self.hovering_option != None and self.options_list[i]["text"].text == self.hovering_option:
                        self.options_list[i]["text"].color = self.hover_color
                        pygame.draw.rect(self.screen, self.menu_hover_color, self.options_list[i]["rect"])
                    else:
                        pygame.draw.rect(self.screen, bar_color, self.options_list[i]["rect"])
                    pygame.draw.rect(self.screen, (0,0,0), self.options_list[i]["rect"], 1)
                    self.options_list[i]["text"].draw(self.options_list[i]["rect"].center)


    def onhover(self, mpos):
        """Performs an action if the mouse is hovering over one of the menus in the menu bar."""
        if hasattr(self, "menu_titles") and hasattr(self, "bar_rect") and hasattr(self, "options_list"):
            for i in range(len(self.menu_titles)):
                if self.menu_titles[i]["rect"].collidepoint(mpos) and self.bar_rect.collidepoint(mpos):
                    self.hovering_menu_title = self.menu_titles[i]["title"]
            for i in range(len(self.options_list)):
                if self.options_list[i]["rect"].collidepoint(mpos):
                    self.hovering_option = self.options_list[i]["text"].text

    def open_menu(self, mpos):
        """If any of the menus in the menu bar were clicked, we will display the options below."""
        if hasattr(self, "menu_titles"):
            for i in range(len(self.menu_titles)):
                if self.menu_titles[i]["rect"].collidepoint(mpos):
                    self.options = {"options":self.menu_titles[i]["options"], "index":i}

    def get_selected_option(self, mpos):
        """If any of the options of any of the menus in the menu bar were clicked, we will return the selected option."""
        if hasattr(self, "options_list"):
            for i in range(len(self.options_list)):
                if self.options_list[i]["rect"].collidepoint(mpos) and self.options != None:
                    self.selected_option = self.options_list[i]["text"].text