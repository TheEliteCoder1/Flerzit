"""
A python scripting module of Flerzit.
"""
import iostream
import graphics
import random
import typing
from graphics import *
from iostream import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (10, 30, 255)


class Member:
    """A member of a Web."""
    def __init__(self):
        """No arguments are required to initialize a Member."""
        self.data = {}
        self.relationships = {}
        
    def change_value(self, field: str, new_value):
        """
        Changes the value of any field
        as long as that field exists in the member, otherwise
        the method will return None.
        """
        if field in self.data.keys():
            self.data[field] = new_value
        else:
            return None

    def add_field(self, field):
        """
        Creates a new field if that field dosen't already exist and sets the default value to None.
        If the key already exsits, the method will return None.
        """
        if not field in self.data.keys():
            self.data[field] = None
        else:
            return None

    def remove_field(self, field):
        """
        Removes a field if the field already exists, otherwise it will return Python's standard
        KeyError because it dosent exist in the data dictionary of the Member.
        """
        self.data.pop(field, None)

def Capture(display,name,pos,size): # (pygame Surface, String, tuple, tuple)
    image = pygame.Surface(size)  # Create image surface
    image.blit(display,(0,0),(pos,size))  # Blit portion of the display to the image
    pygame.image.save(image,name)  # Save the image to the disk**

class Web:
    """A Web consiting of diffrent Members that takes full control of thier relationships."""
    def __init__(self, name, line_colors_dict, legend_dict):
        self.name = name
        self.data = []
        self.visualScript = {
            "title":self.name,
            "line_colors_dict":line_colors_dict,
            "legend_dict":legend_dict,
            "text_color":(0,0,0),
            "member_horizontal_origin":60,
            "member_vertical_origin":60,
            "member_font":"default_font.ttf",
            "title_font":"default_font.ttf",
            "legend_font":"default_font.ttf",
            "legend_font_size":18,
            "member_font_size":18,
            "member_vertical_padding":2.3,
            "member_horizontal_padding":1.3,
            "member_vertical_margin":50,
            "member_horizontal_margin":124,
            "legend_vertical_padding":2.2,
            "legend_horizontal_padding":2.1,
            "legend_border_color":(0,0,0),
            "members_per_row":3,
            "member_space_between_columns":2,
            "legend_space_between_texts":1.1,
            "member_space_between_texts":1.1,
            "member_color":(255,0,0),
            "title_font_size":20,
            "title_font_color":(0,0,0),
            "background_color":(255,255,255),
            "border":True,
            "title_margin_top":60,
            "title_horizontal_alignment":"Center",
            "title_bold":False,
            "title_italic":False,
            "title_underline":False,
            "border_radius":5,
            "legend_color":(255,255,255),
            "legend_border_width":3,
            "legend_border_radius":7,
            "legend_border":True,
            "border_width":7,
            "border_color":(0,0,0),
            "line_width":2,
            "legend_margin_top":60,
            "legend_margin_left":200
        }
        
    def add_member(self, member: Member):
        """
        Adds a member to the data if the member dosen't already exists ; 
        otherwise the method will return None.
        """
        if not member in self.data:
            self.data.append(member)
        else:
            return None

    def remove_member(self, member: Member):
        """
        Removes a member from the data if the member already exists ; 
        otherwise the method will return None.
        """
        if member in self.data:
            self.data.remove(member)
        else:
            return None

    def add_relationship(self, member1: Member, member2: Member, relationship_idx: int):
        """
        Establishes a relationship between 2 members if they exist in the web.
        If the relatinship doesn't exist, a new one will be created.
        """
        if member1 in self.data and member2 in self.data:
            member1.relationships[relationship_idx] = self.data.index(member2)
            member2.relationships[relationship_idx] = self.data.index(member1)
        else:
            return None

    def save(self, filepath, overwrite=False):
        """Saves the Map to a JSON file."""
        new_member_data = []
        for member in self.data:
            json_member = {
                'relationships':member.relationships,
                'data':member.data
            }
            new_member_data.append(json_member)
        data = {
            "name":self.visualScript["title"],
            "data":new_member_data,
            'VisualScript':self.visualScript
        }
        save_json_data(filepath, data, overwrite)

    def load(self, filepath):
        """Loads the Map from a JSON file."""
        new_data = []
        data = load_json_data(filepath)
        if data != None:
            self.name = data["VisualScript"]["title"]
            for member in data["data"]:
                m = Member()
                m.relationships = member["relationships"]
                m.data = member["data"]
                new_data.append(m)
            self.data = new_data
            self.visualScript = data["VisualScript"]
        else:
            raise FileNotFoundError

def create_map_from_json(filepath) -> Web:
    """
    Creates the Map from a JSON file.
    The funciton will return a map if the file exits,
    otherwise it will raise a FileNotFoundError.
    """
    new_data = []
    data = load_json_data(filepath)
    if data != None:
        w = Web(data["name"], data["VisualScript"]["line_colors_dict"], data["VisualScript"]["legend_dict"])
        for member in data["data"]:
            m = Member()
            m.relationships = member["relationships"]
            m.data = member["data"]
            new_data.append(m)
        w.data = new_data
        w.visualScript = data["VisualScript"]
        return w
    else:
        return None

def open(screen, file_path, starting_margin):
    "Displays a Web given a running Pygame window and a Web that was saved to a JSON file."
    web = create_map_from_json(file_path)
    screen_title = "Flerzit - " + file_path
    data_box_list = []
    texts = []
    for member in web.data:
        text_list = []
        if member != 'VisualScript':
            for key, value in member.data.items():
                text_list.append(f"{key}: {value}")
            texts.append(text_list)
    member_col, member_row = 0, 0
    for i, text in enumerate(texts):
        member_box = DataBox(screen, web.visualScript["member_horizontal_padding"], web.visualScript["member_vertical_padding"], web.visualScript["member_horizontal_margin"] * member_col + (starting_margin + web.visualScript["member_horizontal_origin"]), web.visualScript["member_vertical_margin"] * member_row + web.visualScript["member_vertical_origin"], text, web.visualScript["member_font_size"], web.visualScript["member_font"], web.visualScript["text_color"], web.visualScript["member_space_between_texts"])
        data_box_list.append(member_box)
        member_col += 1
        if member_col == web.visualScript["members_per_row"]:
            member_row += web.visualScript["member_space_between_columns"]
            member_col = 0

    # legend
    legend = []
    legend_texts = []
    for member in web.data:
        for relationship_type, relationship in member.relationships.items():
            if int(relationship_type) in [int(k) for k in web.visualScript["line_colors_dict"].keys()]:
                color = web.visualScript["line_colors_dict"][str(relationship_type)]
                if int(relationship_type) in [int(k) for k in web.visualScript["legend_dict"].keys()]:
                    text = web.visualScript["legend_dict"][str(relationship_type)]
                    legend.append({"color":color, "text":text})
                    legend_texts.append(text)
                else:
                    raise Exception(f"No Members have a relationship type of {relationship_type} or your color dictionary or yout legend dictionary or neither did include {relationship_type}.")
            else:
                raise Exception(f"No Members have a relationship type of {relationship_type} or your color dictionary or yout legend dictionary or neither did  include {relationship_type}.")
        break
    
    legend_box = ColoredDataBox(screen, web.visualScript["legend_horizontal_padding"], web.visualScript["legend_vertical_padding"], screen.get_width()-web.visualScript["legend_margin_left"], web.visualScript["legend_margin_top"], legend_texts, web.visualScript["legend_font_size"], web.visualScript["legend_font"], [l["color"] for l in legend], web.visualScript["legend_space_between_texts"])
    member_idx = 0
    all_member_relationships = []
    for member in web.data:
        for relationship_type, relationship in member.relationships.items():
            line_start = (data_box_list[member_idx].box_rect.midleft[0], data_box_list[member_idx].box_rect.midleft[1]-5)
            line_end = (data_box_list[relationship].box_rect.midleft[0], data_box_list[relationship].box_rect.midleft[1]-5)
            if int(relationship_type) in [int(k) for k in web.visualScript["line_colors_dict"].keys()]:
                color = web.visualScript["line_colors_dict"][str(relationship_type)]
                line = {"start":line_start, "end":line_end, "color":color}
                all_member_relationships.append(line)
            else:
                raise Exception(f"No Members have a relationship type of {relationship_type} or your color dictionary did not include {relationship_type}.")        

    return (screen, screen_title, web, all_member_relationships, data_box_list, legend_box, starting_margin)
    

def draw_web(screen, screen_title, web, all_member_relationships, data_box_list, legend_box, starting_margin):
    # filling background color
    screen.fill(web.visualScript["background_color"])
    pygame.display.set_caption(screen_title)

    # calculate offset on resize
    legend_box.x = screen.get_width()-web.visualScript["legend_margin_left"]
    
    # drawing title
    options = ["Center", "Left", "Right"]
    if options[web.visualScript["title_horizontal_alignment"]] == "Center":
        draw_text(screen, web.visualScript["title"], web.visualScript["title_font"], web.visualScript["title_font_size"], web.visualScript["title_font_color"], (screen.get_width() / 2, web.visualScript["title_margin_top"]), bold=web.visualScript["title_bold"], italic=web.visualScript["title_italic"], underline=web.visualScript["title_underline"])
    elif options[web.visualScript["title_horizontal_alignment"]] == "Left":
        draw_text(screen, web.visualScript["title"], web.visualScript["title_font"], web.visualScript["title_font_size"], web.visualScript["title_font_color"], (web.visualScript["member_horizontal_margin"] + (starting_margin + web.visualScript["member_horizontal_origin"]), web.visualScript["title_margin_top"]), bold=web.visualScript["title_bold"], italic=web.visualScript["title_italic"], underline=web.visualScript["title_underline"])
    elif options[web.visualScript["title_horizontal_alignment"]] == "Right":
        draw_text(screen, web.visualScript["title"], web.visualScript["title_font"], web.visualScript["title_font_size"], web.visualScript["title_font_color"], ((web.visualScript["member_horizontal_margin"] * web.visualScript["members_per_row"] + (starting_margin + web.visualScript["member_horizontal_origin"])/2), web.visualScript["title_margin_top"]), bold=web.visualScript["title_bold"], italic=web.visualScript["title_italic"], underline=web.visualScript["title_underline"])
    # drawing all relationships
    for relationship_line in all_member_relationships:
        pygame.draw.line(screen, relationship_line["color"], relationship_line["start"], relationship_line["end"], web.visualScript["line_width"])

    # drawing all members
    for member_box in data_box_list:
        if web.visualScript["border"] != False:
            member_box.draw(web.visualScript["member_color"], web.visualScript["border_radius"], True, web.visualScript["border_width"], web.visualScript["border_color"])
        else:
            member_box.draw(web.visualScript["member_color"], outline=False)

    # drawing legend
    if web.visualScript["legend_border"] != False:
        legend_box.draw(web.visualScript["legend_color"], web.visualScript["legend_border_radius"], True, web.visualScript["legend_border_width"], web.visualScript["legend_border_color"])
    else:
        legend_box.draw(web.visualScript["legend_color"], outline=False)


def display_web(file_path, sw, sh):
    """
    Displays a Web in a Python Window given a Web that was saved to a JSON file.
    Note: the python window is new and is created on the function call.
    """
    web = create_map_from_json(file_path)
    screen_title = "Flerzit - " + web.visualScript["title"]
    screen = pygame.display.set_mode((sw, sh))
    pygame.display.set_caption(screen_title)
    pygame.display.set_icon(pygame.image.load("flerzit-icon.png"))
    clock = pygame.time.Clock()
    fps = 60
    data_box_list = []
    texts = []
    for member in web.data:
        text_list = []
        if member != 'VisualScript':
            for key, value in member.data.items():
                text_list.append(f"{key}: {value}")
            texts.append(text_list)
    member_col, member_row = 0, 0
    for i, text in enumerate(texts):
        member_box = DataBox(screen, web.visualScript["member_horizontal_padding"], web.visualScript["member_vertical_padding"], web.visualScript["member_horizontal_margin"] * member_col + web.visualScript["member_horizontal_origin"], web.visualScript["member_vertical_margin"] * member_row + web.visualScript["member_vertical_origin"], text, web.visualScript["member_font_size"], web.visualScript["member_font"], web.visualScript["text_color"], web.visualScript["member_space_between_texts"])
        data_box_list.append(member_box)
        member_col += 1
        if member_col == web.visualScript["members_per_row"]:
            member_row += web.visualScript["member_space_between_columns"]
            member_col = 0

    # legend
    legend = []
    legend_texts = []
    for member in web.data:
        for relationship_type, relationship in member.relationships.items():
            if int(relationship_type) in [int(k) for k in web.visualScript["line_colors_dict"].keys()]:
                color = web.visualScript["line_colors_dict"][str(relationship_type)]
                if int(relationship_type) in [int(k) for k in web.visualScript["legend_dict"].keys()]:
                    text = web.visualScript["legend_dict"][str(relationship_type)]
                    legend.append({"color":color, "text":text})
                    legend_texts.append(text)
                else:
                    raise Exception(f"No Members have a relationship type of {relationship_type} or your color dictionary or yout legend dictionary or neither did include {relationship_type}.")
            else:
                raise Exception(f"No Members have a relationship type of {relationship_type} or your color dictionary or yout legend dictionary or neither did  include {relationship_type}.")
        break
    
    legend_box = ColoredDataBox(screen, web.visualScript["legend_horizontal_padding"], web.visualScript["legend_vertical_padding"], sw-web.visualScript["legend_margin_left"], 50, legend_texts, web.visualScript["legend_font_size"], web.visualScript["legend_font"], [l["color"] for l in legend], web.visualScript["legend_space_between_texts"])

    member_idx = 0
    all_member_relationships = []
    for member in web.data:
        for relationship_type, relationship in member.relationships.items():
            line_start = (data_box_list[member_idx].box_rect.midleft[0], data_box_list[member_idx].box_rect.midleft[1]-5)
            line_end = (data_box_list[relationship].box_rect.midleft[0], data_box_list[relationship].box_rect.midleft[1]-5)
            if int(relationship_type) in [int(k) for k in web.visualScript["line_colors_dict"].keys()]:
                color = web.visualScript["line_colors_dict"][str(relationship_type)]
                line = {"start":line_start, "end":line_end, "color":color}
                all_member_relationships.append(line)
            else:
                raise Exception(f"No Members have a relationship type of {relationship_type} or your color dictionary did not include {relationship_type}.")        
    run = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

                
        # coloring screen
        screen.fill(web.visualScript["background_color"])
        # drawing title
        draw_text(screen, screen_title, web.visualScript["title_font"], web.visualScript["title_font_size"], web.visualScript["title_font_color"], (screen.get_width() / 2, 35))
    
        # drawing all relationships
        for relationship_line in all_member_relationships:
            pygame.draw.line(screen, relationship_line["color"], relationship_line["start"], relationship_line["end"], web.visualScript["line_width"])

        # drawing all members
        for member_box in data_box_list:
            if web.visualScript["border"] != False:
                member_box.draw(web.visualScript["member_color"], web.visualScript["border_radius"], True, web.visualScript["border_width"], web.visualScript["border_color"])
            else:
                member_box.draw(web.visualScript["member_color"], outline=False)

        # drawing legend
        if web.visualScript["legend_border"] != False:
            legend_box.draw(web.visualScript["legend_color"], web.visualScript["legend_border_radius"], True, web.visualScript["legend_border_width"], web.visualScript["legend_border_color"])
        else:
            legend_box.draw(web.visualScript["legend_color"], outline=False)

        # update the screen every frame
        pygame.display.update()



                
            