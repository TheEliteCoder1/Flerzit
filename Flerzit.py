"""
A Data Visualizer Program that allows you to create Webs and Member Objects.
"""
import pygame
pygame.init()
import graphics
from tkinter import Tk
import tkinter.filedialog
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename
import flerzit_sc
import pygame_menu
from pygame_menu import locals
from copyweb import CopyWebDialog
from field_edit import FieldEditDialog
import os

sw, sh = 800, 500
fileHandle = None
screen_title = "Flerzit" 
screen = pygame.display.set_mode((sw, sh), pygame.RESIZABLE)
pygame.display.set_caption(screen_title)
pygame.display.set_icon(pygame.image.load("flerzit-icon.png"))
clock = pygame.time.Clock()
fps = 200
run = True
# GUI Components
menuBarOptions = {
    "File":["Open", "Save"],
    "Export":["PNG"]
}
open_formats = [('JSON file','*.json')]
export_formats = [('PNG', '*.png')]
menuBar = graphics.MenuBar(screen, menuBarOptions, 25)
web = None

visualScriptMenuTheme = pygame_menu.themes.THEME_DARK.copy()
visualScriptMenuTheme.widget_font = pygame_menu.font.FONT_NEVIS
visualScriptMenuTheme.title_font_size = 30
visualScriptMenuTheme.widget_font_size = 25
visualScriptMenuTheme.widget_border_color = (192,192,192)
visualScriptMenuTheme.widget_font = pygame_menu.font.FONT_MUNRO
visualScriptMenuTheme.title_font = pygame_menu.font.FONT_NEVIS
visualScriptMenuTheme.title_font_shadow = True
visualScriptMenu = pygame_menu.Menu('VisualScript', width=600, height=sh, position=(100, 100, True), theme=visualScriptMenuTheme)
buttons = []
visualScriptToggleBtn = graphics.ToggleButton(screen, 8, 33, 150, 35, (106, 209, 4), (205,0,0), 5, 12, help_text='Editor:')
reloadButton = graphics.Button(screen, 8, 72, 150, 35, (205,0,0), "Reload", border_width=5, border_radius=12, font_size=20)
copyButton = graphics.Button(screen, 8, 111, 150, 37, (0,206,209), "Copy", border_width=5, border_radius=12, font_size=20)
inspectButton = graphics.ToggleButton(screen, 8, 152, 150, 37, (106, 209, 4), (205,0,0), 5, 12, help_text="Inspector: ", font_size=18)
showVisualScriptMenu = visualScriptToggleBtn.is_on
inspectMode = inspectButton.is_on
buttons = [visualScriptToggleBtn, reloadButton, copyButton, inspectButton]
starting_margin = max([button.width for button in buttons])
other_objects = [button for button in buttons]
inspectorRect = None
inspectorText = None

def save_changes():
    # Collect Data from Editor, and save to file
    global web
    line_colors_dict = {}
    for relationship_type, color in web.visualScript["line_colors_dict"].items():
        key = relationship_type
        value = visualScriptMenu.get_widget(f"line_color_{relationship_type}").get_value()
        line_colors_dict[key] = value
    legend_dict = {}
    for relationship_type, relation in web.visualScript["legend_dict"].items():
        key = relationship_type
        value = visualScriptMenu.get_widget(f'legend_relation_{relationship_type}').get_value()
        legend_dict[key] = value
    title = visualScriptMenu.get_widget("title").get_value()
    text_color = visualScriptMenu.get_widget("text_color").get_value()
    member_space_between_texts = visualScriptMenu.get_widget("member_space_between_texts").get_value()
    legend_space_between_texts = visualScriptMenu.get_widget("legend_space_between_texts").get_value()
    member_horizontal_origin = visualScriptMenu.get_widget("member_horizontal_origin").get_value()
    member_vertical_origin = visualScriptMenu.get_widget("member_vertical_origin").get_value()
    member_font = visualScriptMenu.get_widget("member_font").get_value()
    title_font = visualScriptMenu.get_widget("title_font").get_value()
    legend_font = visualScriptMenu.get_widget("legend_font").get_value()
    legend_font_size = visualScriptMenu.get_widget("legend_font_size").get_value()
    member_font_size = visualScriptMenu.get_widget("member_font_size").get_value()
    member_vertical_padding = visualScriptMenu.get_widget("member_vertical_padding").get_value()
    member_horizontal_padding = visualScriptMenu.get_widget("member_horizontal_padding").get_value()
    member_vertical_margin = visualScriptMenu.get_widget("member_vertical_margin").get_value()
    member_horizontal_margin = visualScriptMenu.get_widget("member_horizontal_margin").get_value()
    members_per_row = visualScriptMenu.get_widget("members_per_row").get_value()
    member_space_between_columns = visualScriptMenu.get_widget("member_space_between_columns").get_value()
    member_color = visualScriptMenu.get_widget("member_color").get_value()
    title_font_size = visualScriptMenu.get_widget("title_font_size").get_value()
    title_font_color = visualScriptMenu.get_widget("title_font_color").get_value()
    background_color = visualScriptMenu.get_widget("background_color").get_value()
    border = int(visualScriptMenu.get_widget("border").get_value())
    border_radius = visualScriptMenu.get_widget("border_radius").get_value()
    legend_margin_top = visualScriptMenu.get_widget("legend_margin_top").get_value()
    legend_color = visualScriptMenu.get_widget("legend_color").get_value()
    legend_border_width = visualScriptMenu.get_widget("legend_border_width").get_value()
    legend_border_width = visualScriptMenu.get_widget("legend_border_width").get_value()
    legend_border_radius = visualScriptMenu.get_widget("legend_border_radius").get_value()
    legend_margin_left = visualScriptMenu.get_widget("legend_margin_left").get_value()
    legend_border = int(visualScriptMenu.get_widget("legend_border").get_value())
    border_width = visualScriptMenu.get_widget("border_width").get_value()
    border_color = visualScriptMenu.get_widget("border_color").get_value()
    line_width = visualScriptMenu.get_widget("line_width").get_value()
    legend_border_color = visualScriptMenu.get_widget("legend_border_color").get_value()
    legend_vertical_padding = visualScriptMenu.get_widget("legend_vertical_padding").get_value()
    legend_horizontal_padding = visualScriptMenu.get_widget("legend_horizontal_padding").get_value()
    title_margin_top = visualScriptMenu.get_widget("title_margin_top").get_value()
    title_horizontal_alignment = visualScriptMenu.get_widget("title_horizontal_alignment").get_index()
    title_bold = int(visualScriptMenu.get_widget("title_bold").get_value())
    title_italic = int(visualScriptMenu.get_widget("title_italic").get_value())
    title_underline = int(visualScriptMenu.get_widget("title_underline").get_value())
    visualScript = {
        "title":title,
        "member_space_between_texts":member_space_between_texts,
        "legend_space_between_texts":legend_space_between_texts,
        "line_colors_dict":line_colors_dict,
        "legend_dict":legend_dict,
        "text_color":text_color,
        "member_horizontal_origin":member_horizontal_origin, 
        "member_vertical_origin":member_vertical_origin,
        "member_font":member_font,
        "title_font":title_font,
        "legend_font":legend_font,
        "legend_font_size":legend_font_size,
        "member_font_size":member_font_size,
        "member_vertical_padding":member_vertical_padding,
        "member_horizontal_padding":member_horizontal_padding,
        "member_vertical_margin":member_vertical_margin,
        "member_horizontal_margin":member_horizontal_margin,
        "members_per_row":members_per_row,
        "member_space_between_columns":member_space_between_columns,
        "member_color":member_color,
        "title_font_size":title_font_size,
        "title_font_color":title_font_color,
        "title_margin_top":title_margin_top,
        "title_horizontal_alignment":title_horizontal_alignment,
        "title_bold":title_bold,
        "title_italic":title_italic,
        "title_underline":title_underline,
        "background_color":background_color,
        "border":border,
        "border_radius":border_radius,
        "legend_margin_top":legend_margin_top,
        "legend_color":legend_color,
        "legend_border_width":legend_border_width,
        "legend_border_radius":legend_border_radius,
        "legend_border":legend_border,
        "border_width":border_width,
        "border_color":border_color,
        "line_width":line_width,
        "legend_margin_left":legend_margin_left,
        "legend_border_color":legend_border_color,
        "legend_vertical_padding":legend_vertical_padding,
        "legend_horizontal_padding":legend_horizontal_padding
    }
    web = flerzit_sc.create_map_from_json(fileHandle)
    web.visualScript = visualScript
    web.save(fileHandle, overwrite=True)

smp_line_colors_dict = {
    0:(0,0,0)
}

smp_legend_dict = {
    0:"relationship"
}

visualScriptMenu.add.text_input("title: ", default='Default Title', textinput_id='title')
visualScriptMenu.add.color_input("text_color: ", color_type=pygame_menu.widgets.COLORINPUT_TYPE_RGB, default=(0,0,0), color_id='text_color')
visualScriptMenu.add.text_input("member_horizontal_origin: ", input_type=pygame_menu.locals.INPUT_INT, default=50, textinput_id="member_horizontal_origin")
visualScriptMenu.add.text_input("member_vertical_origin: ", input_type=pygame_menu.locals.INPUT_INT, default=60, textinput_id="member_vertical_origin")
visualScriptMenu.add.text_input("member_font: ", default='fonts/default_font.ttf', textinput_id='member_font')
visualScriptMenu.add.text_input("title_font: ", default='fonts/default_font.ttf', textinput_id='title_font')
visualScriptMenu.add.text_input("legend_font: ", default='fonts/default_font.ttf', textinput_id='legend_font')
visualScriptMenu.add.text_input("legend_font_size: ", input_type=pygame_menu.locals.INPUT_INT, default=18, textinput_id="legend_font_size")
visualScriptMenu.add.text_input("member_font_size: ", input_type=pygame_menu.locals.INPUT_INT, default=15, textinput_id="member_font_size")
visualScriptMenu.add.text_input("member_vertical_padding: ", input_type=pygame_menu.locals.INPUT_FLOAT, default=2.3, textinput_id="member_vertical_padding")
visualScriptMenu.add.text_input("member_horizontal_padding: ", input_type=pygame_menu.locals.INPUT_FLOAT, default=1.3, textinput_id="member_horizontal_padding")
visualScriptMenu.add.text_input("member_vertical_margin: ", input_type=pygame_menu.locals.INPUT_INT, default=50, textinput_id="member_vertical_margin")
visualScriptMenu.add.text_input("member_horizontal_margin: ", input_type=pygame_menu.locals.INPUT_INT, default=124, textinput_id="member_horizontal_margin")
visualScriptMenu.add.text_input("members_per_row: ", input_type=pygame_menu.locals.INPUT_INT, default=3, textinput_id="members_per_row")
visualScriptMenu.add.text_input("member_space_between_columns: ", input_type=pygame_menu.locals.INPUT_FLOAT, default=2, textinput_id="member_space_between_columns")
visualScriptMenu.add.text_input("member_space_between_texts: ", input_type=pygame_menu.locals.INPUT_FLOAT, default=1.1, textinput_id="member_space_between_texts")
visualScriptMenu.add.text_input("legend_space_between_texts: ", input_type=pygame_menu.locals.INPUT_FLOAT, default=1.1, textinput_id="legend_space_between_texts")
visualScriptMenu.add.color_input("member_color: ", color_type=pygame_menu.widgets.COLORINPUT_TYPE_RGB, default=(255,255,255), color_id='member_color')
visualScriptMenu.add.text_input("title_font_size: ", input_type=pygame_menu.locals.INPUT_INT, default=20, textinput_id="title_font_size")
visualScriptMenu.add.toggle_switch("title_bold: ", width=150, state_text=('Hide', 'Show'), state_text_font_size=25, toggleswitch_id='title_bold')
visualScriptMenu.add.toggle_switch("title_italic: ", width=150, state_text=('Hide', 'Show'), state_text_font_size=25, toggleswitch_id='title_italic')
visualScriptMenu.add.toggle_switch("title_underline: ", width=150, state_text=('Hide', 'Show'), state_text_font_size=25, toggleswitch_id='title_underline')
visualScriptMenu.add.text_input("title_margin_top: ", input_type=pygame_menu.locals.INPUT_INT, default=45, textinput_id="title_margin_top")
visualScriptMenu.add.dropselect("title_horizontal_alignment", items=[
    ('Center', 'Center'),
    ('Left', 'Left'),
    ('Right', 'Right')
], selection_box_width=173,  selection_box_height=80, selection_option_font_size=25, dropselect_id="title_horizontal_alignment")
visualScriptMenu.add.color_input("title_font_color: ", color_type=pygame_menu.widgets.COLORINPUT_TYPE_RGB, default=(255,255,255), color_id='title_font_color')
visualScriptMenu.add.color_input("background_color: ", color_type=pygame_menu.widgets.COLORINPUT_TYPE_RGB, default=(72,118,255), color_id='background_color')
visualScriptMenu.add.toggle_switch("border: ", width=150, state_text=('Hide', 'Show'), state_text_font_size=25, toggleswitch_id='border')
visualScriptMenu.add.text_input("border_radius: ", input_type=pygame_menu.locals.INPUT_INT, default=7, textinput_id="border_radius")
visualScriptMenu.add.text_input("legend_margin_top: ", input_type=pygame_menu.locals.INPUT_INT, default=60, textinput_id="legend_margin_top")
visualScriptMenu.add.color_input("legend_color: ", color_type=pygame_menu.widgets.COLORINPUT_TYPE_RGB, default=(255,255,255), color_id='legend_color')
visualScriptMenu.add.text_input("legend_border_width: ", input_type=pygame_menu.locals.INPUT_INT, default=3, textinput_id="legend_border_width")
visualScriptMenu.add.text_input("legend_border_radius: ", input_type=pygame_menu.locals.INPUT_INT, default=7, textinput_id="legend_border_radius")
visualScriptMenu.add.toggle_switch("legend_border: ", width=150, state_text=('Hide', 'Show'), state_text_font_size=25, toggleswitch_id='legend_border')
visualScriptMenu.add.text_input("border_width: ", input_type=pygame_menu.locals.INPUT_INT, default=3, textinput_id="border_width")
visualScriptMenu.add.text_input("line_width: ", input_type=pygame_menu.locals.INPUT_INT, default=2, textinput_id="line_width")
visualScriptMenu.add.color_input("border_color: ", color_type=pygame_menu.widgets.COLORINPUT_TYPE_RGB, default=(78,238,148), color_id='border_color')
visualScriptMenu.add.text_input("legend_margin_left: ", input_type=pygame_menu.locals.INPUT_INT, default=200, textinput_id="legend_margin_left")
visualScriptMenu.add.color_input("legend_border_color: ", color_type=pygame_menu.widgets.COLORINPUT_TYPE_RGB, default=(78,238,148), color_id='legend_border_color')
visualScriptMenu.add.text_input("legend_vertical_padding: ", input_type=pygame_menu.locals.INPUT_FLOAT, default=2.2, textinput_id="legend_vertical_padding")
visualScriptMenu.add.text_input("legend_horizontal_padding: ", input_type=pygame_menu.locals.INPUT_FLOAT, default=2.1, textinput_id="legend_horizontal_padding")
params = None
inspectorMember = None
    
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

        if event.type == pygame.VIDEORESIZE:
            sw, sh = event.w, event.h
            screen = pygame.display.set_mode((sw, sh), pygame.RESIZABLE)
            # offseting ui on resize
            menuBar.bar_width = sw
            visualScriptMenu.resize(600, sh, (sw, sh), position=(100, 100, True))
        
        if event.type == pygame.MOUSEMOTION:
            mpos = pygame.mouse.get_pos()
            menuBar.onhover(mpos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mpos = pygame.mouse.get_pos()
            menuBar.open_menu(mpos)
            menuBar.get_selected_option(mpos)
            
            if menuBar.selected_option == "Open":
                window = Tk()
                window.withdraw()
                window.attributes("-topmost", True)
                filename = askopenfilename(title="Open File", filetypes=open_formats)
                if filename:
                    # try:
                    params = flerzit_sc.open(screen, filename, starting_margin)
                    # except Exception as E:
                    #     tkinter.messagebox.showerror(title="Syntax Error.", message=f"An error occured when trying to open the file - Details: {E}.")
                    fileHandle = filename
                    web = params[2]
                    visualScript = web.visualScript
                    # Setting visualScript Values
                    for relationship_type, color in visualScript["line_colors_dict"].items():
                        try:
                            visualScriptMenu.add.color_input(f"Line Color - {relationship_type}: ", color_type=pygame_menu.widgets.COLORINPUT_TYPE_RGB, default=tuple(color), color_id=f'line_color_{relationship_type}')
                        except IndexError:
                            pass
                        visualScriptMenu.get_widget(f"line_color_{relationship_type}").set_value(tuple(visualScript["line_colors_dict"][relationship_type]))
                        
                    for relationship_type, relation in visualScript["legend_dict"].items():
                        try:
                            visualScriptMenu.add.text_input(f"Relation - {relationship_type}: ", default=relation, max_char=20, textinput_id=f'legend_relation_{relationship_type}')
                        except IndexError:
                            pass
                        visualScriptMenu.get_widget(f'legend_relation_{relationship_type}').set_value(visualScript["legend_dict"][relationship_type])
                    visualScriptMenu.get_widget("title").set_value(visualScript["title"])
                    visualScriptMenu.get_widget("member_space_between_texts").set_value(visualScript["member_space_between_texts"])
                    visualScriptMenu.get_widget("legend_space_between_texts").set_value(visualScript["legend_space_between_texts"])
                    visualScriptMenu.get_widget("text_color").set_value(tuple(visualScript["text_color"]))
                    visualScriptMenu.get_widget("member_horizontal_origin").set_value(visualScript["member_horizontal_origin"])
                    visualScriptMenu.get_widget("member_vertical_origin").set_value(visualScript["member_vertical_origin"])
                    visualScriptMenu.get_widget("member_font").set_value(visualScript["member_font"])
                    visualScriptMenu.get_widget("title_font").set_value(visualScript["title_font"])
                    visualScriptMenu.get_widget("title_margin_top").set_value(visualScript["title_margin_top"])
                    visualScriptMenu.get_widget("title_horizontal_alignment").set_value(visualScript["title_horizontal_alignment"])
                    visualScriptMenu.get_widget("title_bold").set_value(visualScript["title_bold"])
                    visualScriptMenu.get_widget("title_italic").set_value(visualScript["title_italic"])
                    visualScriptMenu.get_widget("title_underline").set_value(visualScript["title_underline"])
                    visualScriptMenu.get_widget("legend_font").set_value(visualScript["legend_font"])
                    visualScriptMenu.get_widget("legend_font_size").set_value(visualScript["legend_font_size"])
                    visualScriptMenu.get_widget("member_font_size").set_value(visualScript["member_font_size"])
                    visualScriptMenu.get_widget("member_vertical_padding").set_value(visualScript["member_vertical_padding"])
                    visualScriptMenu.get_widget("member_horizontal_padding").set_value(visualScript["member_horizontal_padding"])
                    visualScriptMenu.get_widget("member_vertical_margin").set_value(visualScript["member_vertical_margin"])
                    visualScriptMenu.get_widget("member_horizontal_margin").set_value(visualScript["member_horizontal_margin"])
                    visualScriptMenu.get_widget("members_per_row").set_value(visualScript["members_per_row"])
                    visualScriptMenu.get_widget("member_space_between_columns").set_value(visualScript["member_space_between_columns"])
                    visualScriptMenu.get_widget("member_color").set_value(tuple(visualScript["member_color"]))
                    visualScriptMenu.get_widget("title_font_size").set_value(visualScript["title_font_size"])
                    visualScriptMenu.get_widget("title_font_color").set_value(tuple(visualScript["title_font_color"]))
                    visualScriptMenu.get_widget("background_color").set_value(tuple(visualScript["background_color"]))
                    visualScriptMenu.get_widget("border").set_value(int(visualScript["border"])) # convert to int
                    visualScriptMenu.get_widget("border_radius").set_value(visualScript["border_radius"])
                    visualScriptMenu.get_widget("legend_margin_top").set_value(visualScript["legend_margin_top"])
                    visualScriptMenu.get_widget("legend_color").set_value(tuple(visualScript["legend_color"]))
                    visualScriptMenu.get_widget("legend_border_width").set_value(visualScript["legend_border_width"])
                    visualScriptMenu.get_widget("legend_border_radius").set_value(visualScript["legend_border_radius"])
                    visualScriptMenu.get_widget("legend_margin_left").set_value(visualScript["legend_margin_left"])
                    visualScriptMenu.get_widget("legend_border").set_value(int(visualScript["legend_border"])) # convert to int
                    visualScriptMenu.get_widget("border_width").set_value(visualScript["border_width"])
                    visualScriptMenu.get_widget("border_color").set_value(tuple(visualScript["border_color"]))
                    visualScriptMenu.get_widget("line_width").set_value(visualScript["line_width"])
                    visualScriptMenu.get_widget("legend_border_color").set_value(tuple(visualScript["legend_border_color"]))
                    visualScriptMenu.get_widget("legend_vertical_padding").set_value(visualScript["legend_vertical_padding"])
                    visualScriptMenu.get_widget("legend_horizontal_padding").set_value(visualScript["legend_horizontal_padding"])
                    try:
                        visualScriptMenu.add.button("Save", save_changes, button_id='Savebtn')
                    except IndexError:
                        pass
                window.destroy()
                for object in other_objects:
                    if not object.rect.collidepoint(mpos):
                        menuBar.options = None
                        menuBar.selected_option = None
                    else:
                        delattr(menuBar, "options_list")
            if menuBar.selected_option == "Save":
                window = Tk()
                window.withdraw()
                window.attributes("-topmost", True)
                if fileHandle != None:
                    try:
                        web.save(filepath=fileHandle, overwrite=True)
                        tkinter.messagebox.showinfo("Web Saved.", message="Your changes were saved.")
                    except Exception as E:
                        tkinter.messagebox.showerror(title="An Error Occured.", message=f"An error occured when trying to save the file. - Details: {E}")
                else:
                    tkinter.messagebox.showerror(title="No File Opened.", message="You must open a file first.")
                window.destroy()
                for object in other_objects:
                    if not object.rect.collidepoint(mpos):
                        menuBar.options = None
                        menuBar.selected_option = None

            # When inspect mode is turned on, we want to
            # use the `menuBar`, but not listen to `Button`
            if inspectMode != True:
                if menuBar.selected_option == "PNG":
                    print("png")
                    for object in other_objects:
                        if not object.rect.collidepoint(mpos):
                            menuBar.options = None
                            menuBar.selected_option = None
                # buttons handle
                if not (menuBar.options != None):
                    visualScriptToggleBtn.toggle(mpos)
                    showVisualScriptMenu = visualScriptToggleBtn.is_on
    
                if not (menuBar.options != None):
                    if reloadButton.clicked(mpos):
                        if fileHandle != None:
                            params = flerzit_sc.open(screen, fileHandle, starting_margin)
    
                if not (menuBar.options != None):
                    if copyButton.clicked(mpos):
                        window = Tk()
                        window.withdraw()
                        if fileHandle != None:
                            inputDialog = CopyWebDialog(window)
                            window.wait_window(inputDialog.top)
                            if hasattr(inputDialog, "copy_filename"):
                                fname, fext = os.path.splitext(inputDialog.copy_filename)
                                if fext == '.json': # has to be a json file
                                    try:
                                        web.save(filepath=inputDialog.copy_filename, overwrite=True)
                                        tkinter.messagebox.showinfo("Web Copied.", message=f"Your web was copied to '{inputDialog.copy_filename}'.")
                                    except Exception as E:
                                        tkinter.messagebox.showerror(title="An Error Occured.", message=f"An error occured when trying to save the file. - Details: {E}")
                                else:
                                    tkinter.messagebox.showerror(title="Copy Error.", message=f"Could not copy the file because it was not a json file. Hint: Add '.json' to the end of your file name.")
                        else:
                            tkinter.messagebox.showerror(title="No File Opened.", message="You must open a file first.")
                        window.destroy()
            else:
                # Inspect Mode
                if fileHandle != None:
                    # checking if field values were clicked
                    for menu_box in params[4]:
                        if hasattr(menu_box, "text_rects"): # checking if the text rects were drawn.
                            for text_rect in menu_box.text_rects:
                                if text_rect["rect"].collidepoint(mpos):
                                    inspectorRect = text_rect["rect"]
                                    inspectorText = text_rect["text"]
                                    inspectorMember = menu_box
                    

            if not (menuBar.options != None):
                inspectButton.toggle(mpos)
                inspectMode = inspectButton.is_on

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if inspectMode == True:
                    if inspectorRect != None:
                        window = Tk()
                        window.withdraw()
                        inputDialog = FieldEditDialog(window, inspectorText.partition(": ")[0])
                        window.wait_window(inputDialog.top)
                        if hasattr(inputDialog, "value"):
                            if len(inputDialog.value) > 0:
                                params[4][params[4].index(inspectorMember)].data[params[4][params[4].index(inspectorMember)].data.index(inspectorText)] = f"{inputDialog.key}: {inputDialog.value}"     
                                for member in params[2].data:
                                    if params[2].data.index(member) == params[4].index(inspectorMember):
                                        member.data[inputDialog.key] = inputDialog.value     
                        window.destroy()
                        
        
    screen.fill((255,255,255))
    if params != None:
        flerzit_sc.draw_web(*params)
    for button in buttons:
        button.draw(screen)
    menuBar.draw(text_style=graphics.TextStyle("fonts/fira.ttf", 20, color=(255,255,255)))
    if inspectorRect != None:
        pygame.draw.rect(screen, (0,206,209), inspectorRect, width=1)
    if showVisualScriptMenu == True:
        visualScriptMenu.enable()
    else:
        visualScriptMenu.disable()
    if visualScriptMenu.is_enabled():
        visualScriptMenu.update(events)
        visualScriptMenu.draw(screen)
    pygame.display.update()

