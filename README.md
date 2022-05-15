# Flerzit
<p align="center"><img src="https://raw.githubusercontent.com/TheEliteCoder1/Flerzit/main/flerzit-icon.png"></p>

A Data Abstraction Program that allows you
to represent Relationships between every member in an Web
using nothing but Code!

Made with love using Python and Pygame.

<h3>Check out example.py for more info!<h3>
<img src="https://raw.githubusercontent.com/TheEliteCoder1/Flerzit/main/example.png">
<br>
    
```python
"""Example Web displaying a Family Tree."""
# importing the module
import flerzit
from flerzit import Web, Member, display_web

# Creating a Web
WEB = Web()
WEB.name = "Family Web"

# Creating Members
GreatGrandpa = Member()
GreatGrandma = Member()
Grandpa = Member()
Grandma = Member()
Mom = Member()
Dad = Member()
Me = Member()

MEMBERS = [GreatGrandma, GreatGrandpa, Grandma, Grandpa, Mom, Dad, Me]

# Since the fields are the same for each member we can iterate in this example.
# NOTE: the default value to each of these new fields is None or null in JSON.
# We can change them later in the JSON file, OR use the `Member.change_value`
# method.
for member in MEMBERS:
    member.add_field("Name")
    member.add_field("Age")

# Using `Member.change_value` method
for i, member in enumerate(MEMBERS):
    if i == 0:
        MEMBERS[i].change_value("Name", "Sue")
        MEMBERS[i].change_value("Age", 86)
    if i == 1:
        MEMBERS[i].change_value("Name", "Bob")
        MEMBERS[i].change_value("Age", 89)
    if i == 2:
        MEMBERS[i].change_value("Name", "Linda")
        MEMBERS[i].change_value("Age", 78)
    if i == 3:
        MEMBERS[i].change_value("Name", "Jeffrey")
        MEMBERS[i].change_value("Age", 79)
    if i == 4:
        MEMBERS[i].change_value("Name", "Sally")
        MEMBERS[i].change_value("Age", 42)
    if i == 5:
        MEMBERS[i].change_value("Name", "David")
        MEMBERS[i].change_value("Age", 45)
    if i == 6:
        MEMBERS[i].change_value("Name", "Bill")
        MEMBERS[i].change_value("Age", 18)
    
    
# Adding Members
for member in MEMBERS:
    WEB.add_member(member)

# Adding Relationships
WEB.add_relationship(GreatGrandma, GreatGrandpa, 0) # Index shows TYPE of relationship

WEB.add_relationship(GreatGrandma, Grandpa, 1)
WEB.add_relationship(GreatGrandma, Grandma, 2)

WEB.add_relationship(GreatGrandpa, Grandpa, 1)
WEB.add_relationship(GreatGrandpa, Grandma, 2)

WEB.add_relationship(Grandma, Grandpa, 0)

WEB.add_relationship(Grandma, Mom, 1)
WEB.add_relationship(Grandma, Dad, 2)

WEB.add_relationship(Grandpa, Mom, 1)
WEB.add_relationship(Grandpa, Dad, 2)

WEB.add_relationship(Mom, Dad, 0)

WEB.add_relationship(Mom, Me, 1)

# Saving our Web to  A JSON File
# NOTE: if you haven't created a 
# new file with this name, 
# set the overwrite argument to True.
WEB.save("Family_Web.json", overwrite=True)

# Display the Output graphically in Python
# A very customizeable API with defaults for everything 
# in case you dont want
# to mess with too many features :p

# One of the Mandatory Arguments is the `line_colors_dict`
# Each type of relationship you established using the relationship_idx
# parameter in the `add_relationship` method of the Web instance you made,
# they are the diffrent types of relationships.
# In this example we had assigned relationshipes to indexes 1, 2, and 0.
# Every relationship will be a line drawn in a certain color according to this
# dictionary.

line_colors_dict = {
    0:(255,0,0),
    1:(102, 255, 0),
    2:(0,0,255)
}

# Likewise the mandatory `legend_dict` argument also has the same
# behavior, except it manages labels in the legend of the WEB.

legend_dict = {
    0:"Spouse",
    1:"Child",
    2:"In-Law"
}

# There you go!
# You've sucessfully put a WEB together.
# Now, Run the file in your current directory and see the output
# Enjoy your Web and don't forget that it is a JSON file so it may be portable 
# to potential JavaScript Applications by parsing the file similiarly.

display_web(
    file_path="Family_Web.json", sw=660, sh=500,
    line_colors_dict=line_colors_dict, legend_dict=legend_dict,
    member_font_size=18, title_font_size=25, 
    border_color=(244, 255, 255), border_width=3, border_radius=7, text_color=flerzit.BLACK, 
    screen_color=(224, 255, 255), title_font_color=flerzit.BLACK, member_color=flerzit.WHITE, member_origin=65,
    member_space_between_columns=3, member_horizontal_margin=160, legend_color=flerzit.WHITE, legend_font_size=20, 
    legend_vertical_padding=2.2, legend_horizontal_padding=2.1, legend_margin_left=130, legend_border_color=flerzit.BLACK, legend_border_width=3,
    legend_border_radius=7
)
```
