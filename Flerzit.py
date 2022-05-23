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

sw, sh = 650, 500
fileHandle = None
params = None
screen_title = "Flerzit" 
screen = pygame.display.set_mode((sw, sh), pygame.RESIZABLE)
pygame.display.set_caption(screen_title)
pygame.display.set_icon(pygame.image.load("flerzit-icon.png"))
clock = pygame.time.Clock()
fps = 200
run = True
# GUI Components
menuBarOptions = {
    "File":["Open", "Save", "Save As"],
    "Export":["PNG"]
}
open_formats = [('JSON file','*.json')]
export_formats = [('PNG', '*.png')]
menuBar = graphics.MenuBar(screen, menuBarOptions, 25)
zoom = 2

def draw_program(screen):
    screen.fill((255,255,255))
    if params != None:
        flerzit_sc.draw_web(*params)
    menuBar.draw(text_style=graphics.TextStyle("fira.ttf", 20, color=(255,255,255)))
    
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

        if event.type == pygame.VIDEORESIZE:
            sw, sh = event.w, event.h
            screen = pygame.display.set_mode((sw, sh), pygame.RESIZABLE)
            # offseting ui on resize
            menuBar.bar_width = sw

        
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
                try:
                    params = flerzit_sc.open(screen, filename)
                    fileHandle = filename
                except:
                    tkinter.messagebox.showerror(title="Error", message="An error occured when trying to open the file.")
                window.destroy()
                menuBar.options = None
                menuBar.selected_option = None
            if menuBar.selected_option == "Save":
                print("s")
                menuBar.options = None
                menuBar.selected_option = None
            if menuBar.selected_option == "Save As":
                print("sa")
                menuBar.options = None
                menuBar.selected_option = None
            if menuBar.selected_option == "PNG":
                print("png")
                menuBar.options = None
                menuBar.selected_option = None

        if event.type == pygame.MOUSEWHEEL:
            print(event.button)
        
    draw_program(screen)
    pygame.display.update()

