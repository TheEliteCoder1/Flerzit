"""Example Web displaying the Changes in States of Matter."""
import flerzit
from flerzit import Web, Member, display_web

# Creating a Web
WEB = Web()
WEB.name = "Changes in the States of Matter"

Freezing = Member()
Melting = Member()
Sublimation = Member()
Deposition = Member()
Evaporation = Member()
Condensation = Member()

MEMBER_NAMES = ["Freezing","Melting","Sublimation","Deposition","Evaporation","Condensation"]
MEMBERS = [Freezing,Melting,Sublimation,Deposition,Evaporation,Condensation]

for i, member in enumerate(MEMBERS):
    member.add_field("Name")
    member.change_value("Name", MEMBER_NAMES[i])
    WEB.add_member(member)

# Adding Relationships
WEB.add_relationship(Freezing, Melting, 0)
WEB.add_relationship(Sublimation, Deposition, 0)
WEB.add_relationship(Evaporation, Condensation, 0)

WEB.save("States_Of_Matter.json", overwrite=True)

legend_dict = {
    0:"Opposite"
}

line_colors_dict = {
    0:(255,255,255)
}

display_web(
    file_path="States_Of_Matter.json", sw=840, sh=500,
    line_colors_dict=line_colors_dict, legend_dict=legend_dict,
    member_font_size=18, title_font_size=25, 
    border_color=flerzit.BLUE, border_width=3, border_radius=7, text_color=flerzit.BLACK, 
    screen_color=(0, 0, 0), title_font_color=flerzit.WHITE, member_color=flerzit.WHITE, member_origin=65,
    member_space_between_columns=3, member_horizontal_margin=200, legend_color=flerzit.BLACK, legend_font_size=20, 
    legend_vertical_padding=2.2, legend_horizontal_padding=2.1, legend_margin_left=160, legend_border_color=flerzit.BLUE, legend_border_width=3,
    legend_border_radius=7
)
