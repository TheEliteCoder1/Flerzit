"""
A Data Illustration Program that represents Web-Like Relationships between every member.
"""
import iostream
import graphics
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
    def __init__(self):
        """To initialize a Web, all you will need is a name."""
        self.name = 'Blank'
        self.data = []

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
            "name":self.name,
            "data":new_member_data
        }
        save_json_data(filepath, data, overwrite)

    def load(self, filepath):
        """Loads the Map from a JSON file."""
        new_data = []
        data = load_json_data(filepath)
        if data != None:
            self.name = data["name"]
            for member in data["data"]:
                m = Member()
                m.relationships = member["relationships"]
                m.data = member["data"]
                new_data.append(m)
            self.data = new_data
        else:
            raise FileNotFoundError


def display_web(file_path, sw, sh, line_colors_dict: dict, legend_dict: dict,
               text_color: typing.Tuple[int, int, int] = (0,0,0), member_origin=60,
               member_font="default_font.ttf", title_font="default_font.ttf", legend_font="default_font.ttf",
               legend_font_size=18, member_font_size=18, member_vertical_padding=2.3, member_horizontal_padding=1.3, 
               member_horizontal_margin=150, legend_vertical_padding=2.3, legend_horizontal_padding=1.3, 
               member_vertical_margin=50, members_per_row=3, member_space_between_columns=2,
               member_color: typing.Tuple[int, int, int] = (255,0,0), title_font_size=20, title_font_color: typing.Tuple[int, int, int] = (0,0,0),
               screen_color: typing.Tuple[int, int, int] = (255,255,255), border=True, border_radius=5, legend_color=(255,255,255), legend_border_color=(0,0,0), legend_border_width=3, legend_border_radius=7, legend_border=True,
               border_width=7, border_color: typing.Tuple[int, int, int] = (0,0,0), line_width=2, legend_margin_left=200, *args, **kwargs):
    """
    Displays a Web using Python graphics given a Web that was saved to a JSON file.
    """
    web = Web()
    web.load(file_path)
    screen_title = web.name
    screen = pygame.display.set_mode((sw, sh))
    pygame.display.set_caption(screen_title)
    clock = pygame.time.Clock()
    fps = 60
    data_box_list = []
    texts = []
    for member in web.data:
        text_list = []
        for key, value in member.data.items():
            text_list.append(f"{key}: {value}")
        texts.append(text_list)
    member_col, member_row = 0, 0
    for i, text in enumerate(texts):
        member_box = DataBox(screen, member_horizontal_padding, member_vertical_padding, member_horizontal_margin * member_col + member_origin, member_vertical_margin * member_row + member_origin, text, member_font_size, member_font, text_color)
        data_box_list.append(member_box)
        member_col += 1
        if member_col == members_per_row:
            member_row += member_space_between_columns
            member_col = 0

    # legend
    legend = []
    legend_texts = []
    for member in web.data:
        for relationship_type, relationship in member.relationships.items():
            if int(relationship_type) in list(line_colors_dict.keys()):
                color = line_colors_dict[int(relationship_type)]
                if int(relationship_type) in list(legend_dict.keys()):
                    text = legend_dict[int(relationship_type)]
                    legend.append({"color":color, "text":text})
                    legend_texts.append(text)
                else:
                    raise Exception(f"No Members have a relationship type of {relationship_type} or your color dictionary or yout legend dictionary or neither did  include {relationship_type}.")
            else:
                raise Exception(f"No Members have a relationship type of {relationship_type} or your color dictionary or yout legend dictionary or neither did  include {relationship_type}.")
        break
    legend_box = ColoredDataBox(screen, legend_horizontal_padding, legend_vertical_padding, sw-legend_margin_left, 50, legend_texts, legend_font_size, legend_font, [l["color"] for l in legend])
    member_idx = 0
    all_member_relationships = []
    for member in web.data:
        for relationship_type, relationship in member.relationships.items():
            line_start = (data_box_list[member_idx].box_rect.midleft[0], data_box_list[member_idx].box_rect.midleft[1]-5)
            line_end = (data_box_list[relationship].box_rect.midleft[0], data_box_list[relationship].box_rect.midleft[1]-5)
            if int(relationship_type) in list(line_colors_dict.keys()):
                color = line_colors_dict[int(relationship_type)]
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
        screen.fill(screen_color)
        # drawing title
        draw_text(screen, screen_title, title_font, title_font_size, title_font_color, (screen.get_width() / 2, 15))
    
        # drawing all relationships
        for relationship_line in all_member_relationships:
            pygame.draw.line(screen, relationship_line["color"], relationship_line["start"], relationship_line["end"], line_width)

        # drawing all members
        for member_box in data_box_list:
            if border != False:
                member_box.draw(member_color, border_radius, True, border_width, border_color)
            else:
                member_box.draw(member_color, outline=False)

        # drawing legend
        if legend_border != False:
            legend_box.draw(legend_color, legend_border_radius, True, legend_border_width, legend_border_color)
        else:
            legend_box.draw(legend_color, outline=False)

        # update the screen every frame
        pygame.display.update()
                
            