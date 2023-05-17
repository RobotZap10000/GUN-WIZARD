import pygame, sys
from pygame.locals import *
import variables as v
import groups as g
import texts as txt
import classes as cls
import lvl0
import lvl1

#TODO
    #Make button activate on release X
    #Add text to button X
    #Add conditional transparency to button X

# Configuration
pygame.init()

displaysurface = pygame.display.set_mode((v.WIDTH, v.HEIGHT))

def bruh():
    print("BRUH")

#Tutorial button
def Startlvl0():
    for entity in g.all_sprites:
        entity.kill()
    for entity in g.debug:
        entity.kill()
    lvl0.StartMap()
    v.LEVEL = 0
    v.GAMESTATE = 2
    pygame.mouse.set_visible(1)

def Startlvl1():
    for entity in g.all_sprites:
        entity.kill()
    for entity in g.debug:
        entity.kill()
    lvl1.StartMap()
    v.LEVEL = 1
    v.GAMESTATE = 2
    pygame.mouse.set_visible(1)

levellist = [
    Startlvl0,
    Startlvl1
]

def RestartLvl():
    if isinstance(v.LEVEL, int):
            levellist[v.LEVEL]()
            v.PAUSED = False
    else:
        raise Exception("Level number is NaN")
    
#Button class
class Button():
    def __init__(self, size, origin, function, font, text, textcolor, idle, hover, press, group):
        self.surf = pygame.Surface(size)
        self.rect = self.surf.get_rect(center = origin)
        self.function = function
        self.text = font.render(text, True, textcolor)
        self.textrect = self.text.get_rect(center = origin)
        self.pressing = False
        self.idle = idle
        self.hover = hover
        self.press = press
        group.append(self)

    def process(self):
        mousepos = pygame.mouse.get_pos()
        self.surf.fill(self.idle[0])
        self.surf.set_alpha(self.idle[1])
        if self.rect.collidepoint(mousepos):
            self.surf.fill(self.hover[0])
            self.surf.set_alpha(self.hover[1])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.surf.fill(self.press[0])
                self.surf.set_alpha(self.press[1])
                self.pressing = True
            else:
                if self.pressing == True:
                    self.function()
                    self.pressing = False
        else:
            self.pressing = False
                    
        displaysurface.blit(self.surf, self.rect)
        displaysurface.blit(self.text, self.textrect)

#Button(size, origin, function, font, text, textcolor, idle, hover, press, group)
#Level select menu
lvl0_button = Button((500, 80), (v.WIDTH/2, v.HEIGHT/5+300), Startlvl0, txt.font_lvlselect, "TUTORIAL", v.TITLEGREEN, (v.BUTTONGRAY, 255), (v.RED, 255), (v.BUTTONORANGE, 255), g.lvl_select_buttons)
lvl1_button = Button((500, 80), (v.WIDTH/2, v.HEIGHT/5+400), Startlvl1, txt.font_lvlselect, "LEVEL 1", v.TITLEGREEN, (v.BUTTONGRAY, 255), (v.RED, 255), (v.BUTTONORANGE, 255), g.lvl_select_buttons)
lvl2_button = Button((500, 80), (v.WIDTH/2, v.HEIGHT/5+500), bruh, txt.font_lvlselect, "BRUH", v.TITLEGREEN, (v.BUTTONGRAY, 255), (v.RED, 255), (v.BUTTONORANGE, 255), g.lvl_select_buttons)
lvlselect_back = Button((300, 100), (v.WIDTH/9*3, v.HEIGHT/7*6), bruh, txt.font_lvlselectbig, "BACK", v.TITLEGREEN, (v.BUTTONGRAY, 255), (v.RED, 255), (v.BUTTONORANGE, 255), g.lvl_select_buttons)
lvlselect_quit = Button((300, 100), (v.WIDTH/9*6, v.HEIGHT/7*6), bruh, txt.font_lvlselectbig, "QUIT", v.TITLEGREEN, (v.BUTTONGRAY, 255), (v.RED, 255), (v.BUTTONORANGE, 255), g.lvl_select_buttons)

#In-game pause menu
resumegame_button = Button((500, 80), (v.WIDTH/2, v.HEIGHT/5+400), bruh, txt.font_lvlselect, "RESUME GAME", v.TITLEGREEN, (v.BUTTONGRAY, 255), (v.RED, 255), (v.BUTTONORANGE, 255), g.pause_menu_buttons)
pause_restart_level_button = Button((500, 80), (v.WIDTH/2, v.HEIGHT/5+500), RestartLvl, txt.font_lvlselect, "RESTART LEVEL", v.TITLEGREEN, (v.BUTTONGRAY, 255), (v.RED, 255), (v.BUTTONORANGE, 255), g.pause_menu_buttons)
return_to_lvlselect_button = Button((500, 80), (v.WIDTH/2, v.HEIGHT/5+600), bruh, txt.font_lvlselect, "QUIT TO MAIN MENU", v.TITLEGREEN, (v.BUTTONGRAY, 255), (v.RED, 255), (v.BUTTONORANGE, 255), g.pause_menu_buttons)
pausemenu_quit_button = Button((500, 80), (v.WIDTH/2, v.HEIGHT/5+700), bruh, txt.font_lvlselect, "QUIT TO DESKTOP", v.TITLEGREEN, (v.BUTTONGRAY, 255), (v.RED, 255), (v.BUTTONORANGE, 255), g.pause_menu_buttons)

#Death screen menu
death_restart_level_button = Button((500, 80), (v.WIDTH/2, v.HEIGHT/5+400), RestartLvl, txt.font_lvlselect, "RESTART LEVEL", v.TITLEGREEN, (v.BUTTONGRAY, 255), (v.RED, 255), (v.BUTTONORANGE, 255), g.death_menu_buttons)
death_return_to_lvlselect_button = Button((500, 80), (v.WIDTH/2, v.HEIGHT/5+500), bruh, txt.font_lvlselect, "QUIT TO MAIN MENU", v.TITLEGREEN, (v.BUTTONGRAY, 255), (v.RED, 255), (v.BUTTONORANGE, 255), g.death_menu_buttons)
deathmenu_quit_button = Button((500, 80), (v.WIDTH/2, v.HEIGHT/5+600), bruh, txt.font_lvlselect, "QUIT TO DESKTOP", v.TITLEGREEN, (v.BUTTONGRAY, 255), (v.RED, 255), (v.BUTTONORANGE, 255), g.death_menu_buttons)

#Use class inheritance here?
darkened_screen = cls.MapObject((v.WIDTH, v.HEIGHT), v.BLACK, (v.WIDTH/2, v.HEIGHT/2), g.screens)
darkened_screen.surf.set_alpha(128)
g.all_sprites.remove(darkened_screen)

def DrawLvlSelect():
    for button in g.lvl_select_buttons:
        button.process()

def DrawPauseMenu():
    if len(list(g.players)) > 0:
        if v.PAUSED == True:
            displaysurface.blit(darkened_screen.surf, darkened_screen.rect)
            for button in g.pause_menu_buttons:
                button.process()

def DrawDeathMenu():
    if len(list(g.players)) == 0:
        v.PAUSED = False
        displaysurface.blit(darkened_screen.surf, darkened_screen.rect)
        for button in g.death_menu_buttons:
            button.process()
