import pygame, sys
from pygame.locals import *
import variables as v
import groups as g
import texts as txt
import classes as cls
import functions as func

#TODO
    #Make button activate on release X
    #Add text to button X
    #Add conditional transparency to button X

# Configuration
pygame.init()

displaysurface = pygame.display.set_mode((v.WIDTH, v.HEIGHT))

def bruh():
    print("BRUH")
    
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
lvl0_button = Button((500, 80), (v.WIDTH/2, v.HEIGHT/5+300), func.Startlvl0, txt.font_lvlselect, "TUTORIAL", v.TITLEGREEN, (v.BUTTONGRAY, 255), (v.RED, 255), (v.BUTTONORANGE, 255), g.lvl_select_buttons)
lvl1_button = Button((500, 80), (v.WIDTH/2, v.HEIGHT/5+400), func.Startlvl1, txt.font_lvlselect, "NME", v.TITLEGREEN, (v.BUTTONGRAY, 255), (v.RED, 255), (v.BUTTONORANGE, 255), g.lvl_select_buttons)
lvl2_button = Button((500, 80), (v.WIDTH/2, v.HEIGHT/5+500), func.Startlvl2, txt.font_lvlselect, "BOSS", v.TITLEGREEN, (v.BUTTONGRAY, 255), (v.RED, 255), (v.BUTTONORANGE, 255), g.lvl_select_buttons)
lvlselect_back = Button((300, 100), (v.WIDTH/9*3, v.HEIGHT/7*6), func.ReturnToTitle, txt.font_lvlselectbig, "BACK", v.TITLEGREEN, (v.BUTTONGRAY, 255), (v.RED, 255), (v.BUTTONORANGE, 255), g.lvl_select_buttons)
lvlselect_quit = Button((300, 100), (v.WIDTH/9*6, v.HEIGHT/7*6), func.QuitGame, txt.font_lvlselectbig, "QUIT", v.TITLEGREEN, (v.BUTTONGRAY, 255), (v.RED, 255), (v.BUTTONORANGE, 255), g.lvl_select_buttons)

#In-game pause menu
resumegame_button = Button((500, 80), (v.WIDTH/2, v.HEIGHT/5+400), func.TogglePause, txt.font_lvlselect, "RESUME GAME", v.TITLEGREEN, (v.BUTTONGRAY, 255), (v.RED, 255), (v.BUTTONORANGE, 255), g.pause_menu_buttons)
pause_restart_level_button = Button((500, 80), (v.WIDTH/2, v.HEIGHT/5+500), func.RestartLvl, txt.font_lvlselect, "RESTART LEVEL", v.TITLEGREEN, (v.BUTTONGRAY, 255), (v.RED, 255), (v.BUTTONORANGE, 255), g.pause_menu_buttons)
return_to_lvlselect_button = Button((500, 80), (v.WIDTH/2, v.HEIGHT/5+600), func.ReturnToLvlSelect, txt.font_lvlselect, "QUIT TO MAIN MENU", v.TITLEGREEN, (v.BUTTONGRAY, 255), (v.RED, 255), (v.BUTTONORANGE, 255), g.pause_menu_buttons)
pausemenu_quit_button = Button((500, 80), (v.WIDTH/2, v.HEIGHT/5+700), func.QuitGame, txt.font_lvlselect, "QUIT TO DESKTOP", v.TITLEGREEN, (v.BUTTONGRAY, 255), (v.RED, 255), (v.BUTTONORANGE, 255), g.pause_menu_buttons)

#Death screen menu
death_restart_level_button = Button((500, 80), (v.WIDTH/2, v.HEIGHT/5+400), func.RestartLvl, txt.font_lvlselect, "RESTART LEVEL", v.TITLEGREEN, (v.BUTTONGRAY, 255), (v.RED, 255), (v.BUTTONORANGE, 255), g.death_menu_buttons)
death_return_to_lvlselect_button = Button((500, 80), (v.WIDTH/2, v.HEIGHT/5+500), func.ReturnToLvlSelect, txt.font_lvlselect, "QUIT TO MAIN MENU", v.TITLEGREEN, (v.BUTTONGRAY, 255), (v.RED, 255), (v.BUTTONORANGE, 255), g.death_menu_buttons)
deathmenu_quit_button = Button((500, 80), (v.WIDTH/2, v.HEIGHT/5+600), func.QuitGame, txt.font_lvlselect, "QUIT TO DESKTOP", v.TITLEGREEN, (v.BUTTONGRAY, 255), (v.RED, 255), (v.BUTTONORANGE, 255), g.death_menu_buttons)

#Use class inheritance here?
darkened_screen = cls.MapObject((v.WIDTH, v.HEIGHT), v.BLACK, (v.WIDTH/2, v.HEIGHT/2), g.screens)
darkened_screen.surf.set_alpha(128)
g.all_sprites.remove(darkened_screen)

def DrawLvlSelect():
    for button in g.lvl_select_buttons:
        button.process()

def DrawPauseMenu():
    if not v.DEAD or v.VICTORY:
        if v.PAUSED == True:
            displaysurface.blit(darkened_screen.surf, darkened_screen.rect)
            for button in g.pause_menu_buttons:
                button.process()

def DrawDeathMenu():
    if v.DEAD and not v.VICTORY:
        v.PAUSED = False
        displaysurface.blit(darkened_screen.surf, darkened_screen.rect)
        for button in g.death_menu_buttons:
            button.process()
