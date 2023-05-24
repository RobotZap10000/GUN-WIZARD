import pygame
from pygame.locals import *
import variables as v
import groups as g
import platform as pyplatform

pygame.init()

#game clock
FramePerSec = pygame.time.Clock()

#game window
displaysurface = pygame.display.set_mode((v.WIDTH, v.HEIGHT))

#Text fonts 
font_debug = pygame.font.SysFont("Verdana", 20)
font_icon = pygame.font.Font("FreeSerif.ttf", 50)
font_version = pygame.font.SysFont("Verdana", 20)
font_title = pygame.font.Font("upheavtt.ttf", 250)
font_subtitle = pygame.font.Font("upheavtt.ttf", 60)
font_lvlselect = pygame.font.Font("upheavtt.ttf", 50)
font_lvlselectbig = pygame.font.Font("upheavtt.ttf", 90)

#Class for text
class Text():
    def __init__(self, font, string, color, rect, textlist=None, rectlist=None):
        #super().__init__()
        self.color = color
        self.text = font.render(string, True, self.color)
        self.width, self.height = font.size(string)
        self.rect = self.text.get_rect(center = rect)
        if textlist != None:
            textlist.append(self.text)
            rectlist.append(self.rect)


#Title screen text ONLY DEFINED ONCE
title_texts = []
title_rects = []

title_text = Text(font_title, "GUN WIZARD", v.TITLEGREEN, (v.WIDTH/2, v.HEIGHT/2-20), title_texts, title_rects)
subtitle_text = Text(font_subtitle, "PRESS ANY KEY TO START", v.TITLEGREEN, (v.WIDTH/2, v.HEIGHT/2+90), title_texts, title_rects)

#Level select text
#Text(font, string, color, rect, textlist, rectlist)
lvl_select_texts = []
lvl_select_rects = []

#Level select
titletext = Text(font_title, "GUN WIZARD", v.TITLEGREEN, (v.WIDTH/2, v.HEIGHT/5), lvl_select_texts, lvl_select_rects)
text0 = Text(font_lvlselectbig, "SELECT A LEVEL:", v.TITLEGREEN, (v.WIDTH/2, v.HEIGHT/5+110), lvl_select_texts, lvl_select_rects)
#IF INCOMPATIBLE
    #WARNING TEXT
incompatible = 0

#Python version
if pyplatform.python_version() == "3.11.2":
    python_version_text = Text(font_version, "Python " + pyplatform.python_version(), v.TITLEGREEN, (0, 0), lvl_select_texts, lvl_select_rects)
else:
    python_version_text = Text(font_version, "Python " + pyplatform.python_version(), v.RED, (0, 0), lvl_select_texts, lvl_select_rects)
    incompatible = 1

python_version_text.rect.bottomright = (v.WIDTH, v.HEIGHT - 20)

#Pygame version
if pygame.__version__ == "2.2.0":
    pygame_version_text = Text(font_version, "Pygame " + pygame.__version__, v.TITLEGREEN, (0, 0), lvl_select_texts, lvl_select_rects)
else:
    pygame_version_text = Text(font_version, "Pygame " + pygame.__version__, v.RED, (0, 0), lvl_select_texts, lvl_select_rects)
    incompatible = 1

if incompatible == 1:
    incomp_text = Text(font_version, "!WARNING! May be incompatible with installed version", v.RED, (0, 0), lvl_select_texts, lvl_select_rects)
    incomp_text.rect.bottomright = (v.WIDTH, v.HEIGHT - 40)

pygame_version_text.rect.bottomright = (v.WIDTH, v.HEIGHT)

#Pause menu text
pause_text = font_title.render("PAUSED", True, v.RED)
pause_rect = pause_text.get_rect(center=(v.WIDTH/2, (v.HEIGHT/2-100)))

#Death menu text
death_text = font_title.render("YOU DIED!", True, v.RED)
death_rect = death_text.get_rect(center=(v.WIDTH/2, (v.HEIGHT/2-100)))

#Victory text
victory_text = font_title.render("VICTORY!", True, v.TITLEGREEN)
victory_rect = victory_text.get_rect(center=(v.WIDTH/2, (v.HEIGHT/2)))

#Text drawing
def DrawText(textlist, rectlist):
    for text, rect in zip(textlist, rectlist):
        displaysurface.blit(text, rect)

#Title screen drawing
def DrawTitleScreen():

    displaysurface.fill(v.BLACK)
    DrawText(title_texts, title_rects)

def DrawLevelSelect():

    displaysurface.fill(v.BLACK)
    DrawText(lvl_select_texts, lvl_select_rects)

#Debugmenu text and drawing DEFINED EVERY FRAME
#Text(font, string, color, rect, textlist, rectlist)
def DrawDebugMenu():
    if v.DEBUG == True:

        debugvars = []
        debugvar_rects = []
        
        #FPS counter
        #v.FRAMESCOUNTED = str(FramePerSec.get_fps()) #str((round(FramePerSec.get_fps(), 1)))
        fpscounter = Text(font_debug, "FPS: " + str(v.FRAMESCOUNTED), v.TITLEGREEN  , (0, 0), debugvars, debugvar_rects)
        fpscounter.rect.topleft = (0, 0)

        if v.GAMESTATE == 2:

            for player in g.players:

                #Player screen coordinates
                playerscreencoords = Text(font_debug, "Player-to-screen [x, y]: " + str(round(player.pos)), v.TITLEGREEN, (0, 20), debugvars, debugvar_rects)
                playerscreencoords.rect.topleft = (0, 20)
                        
                #Player true coords
                for entity in g.map_center:
                    calcx = player.pos[0] - entity.rect.centerx
                    calcy = (player.pos[1] - entity.rect.centery - 0) * -1 #MAY CAUSE BUGS
                truepos = (round(calcx), round(calcy))
                playerlevelcoords = Text(font_debug, "Player-to-level [x, y]: " + str(truepos), v.TITLEGREEN, (0, 0), debugvars, debugvar_rects)
                playerlevelcoords.rect.topleft = (0, 40)

                #Player velocity
                playervel = Text(font_debug, "Player velocity [x, y]: " + str(round(player.vel, 2)), v.TITLEGREEN, (0, 0), debugvars, debugvar_rects)
                playervel.rect.topleft = (0, 60)

                #Player standing
                playerstanding = Text(font_debug, "Player standing [Boolean]: " + str(player.standing), v.TITLEGREEN, (0, 0), debugvars, debugvar_rects)
                playerstanding.rect.topleft = (0, 80)

                #Player-Wall
                playertowall = Text(font_debug, "Player-to-wall [Boolean]: " + str(player.wall), v.TITLEGREEN, (0, 0), debugvars, debugvar_rects)
                playertowall.rect.topleft = (0, 100)
                
                #Player lastpos
                playerlastpos = Text(font_debug, "Player last position [x, y]: " + str(round(player.lastpos)), v.TITLEGREEN, (0, 0), debugvars, debugvar_rects)
                playerlastpos.rect.topleft = (0, 120)

                #Player truevel
                playertruevel = Text(font_debug, "Player true velocity [x, y]: " + str(round(player.truevel, 2)), v.TITLEGREEN, (0, 0), debugvars, debugvar_rects)
                playertruevel.rect.topleft = (0, 140)

                #Player weapon
                playerweapon = Text(font_debug, "Current weapon: " + str(player.weapon), v.TITLEGREEN, (0, 0), debugvars, debugvar_rects)
                playerweapon.rect.topleft = (0, 160)

                playerhealth = Text(font_debug, "Player health: " + str(player.health), v.TITLEGREEN, (0, 0), debugvars, debugvar_rects)
                playerhealth.rect.topleft = (0, 180)

                playermana = Text(font_debug, "Player mana: " + str(player.mana), v.TITLEGREEN, (0, 0), debugvars, debugvar_rects)
                playermana.rect.topleft = (0, 200)

                playerlastfire = Text(font_debug, "Last fired: " + str(player.lastfired), v.TITLEGREEN, (0, 0), debugvars, debugvar_rects)
                playerlastfire.rect.topleft = (0, 220)
                
        DrawText(debugvars, debugvar_rects)

def DrawPauseMenu():
    if v.PAUSED == True:
        displaysurface.blit(pause_text, pause_rect)

def DrawDeathMenu():
    if v.DEAD and not v.VICTORY:
        displaysurface.blit(death_text, death_rect)


def DrawVictoryText():
    if v.VICTORY:
        displaysurface.blit(victory_text, victory_rect)
