import pygame, sys
from pygame.locals import *
import random, time
import variables as v
import texts as txt
import groups as g
#import menus as menu
import lvl0
import lvl1

vec = pygame.math.Vector2

#Quitting game
def QuitGame():
    pygame.quit()
    sys.exit()

#Kill all sprites
def KillAll():
    for entity in g.all_sprites:
        entity.kill()
    for entity in g.debug:
        entity.kill()

#Return to title screen
def ReturnToTitle():
    KillAll()
    v.GAMESTATE = 0
    v.PAUSED = False
    pygame.mouse.set_visible(0)
    v.LEVEL = None

#Return to level select screen
def ReturnToLvlSelect():
    KillAll()
    v.GAMESTATE = 1
    v.PAUSED = False
    pygame.mouse.set_visible(1)
    v.LEVEL = None

#Toggle pause menu
def TogglePause():
    if not v.VICTORY:
        v.PAUSED = not v.PAUSED
        for button in g.pause_menu_buttons:
            button.pressing = False

#Toggle debug menu
def ToggleDebug():
    v.DEBUG = not v.DEBUG
    if v.DEBUG:
        for entity in g.debug:
            g.all_sprites.add(entity)
    else:
        for entity in g.debug:
            g.all_sprites.remove(entity)

#Scroll the screen in-game
def ScrollScreen():
    if len(g.players) > 0:
        for f in g.focus:
            if f.rect.center != (v.WIDTH/2, v.HEIGHT/2):
                offsetx = v.WIDTH/2 - f.rect.centerx
                offsety = v.HEIGHT/2 - f.rect.centery
                for entity in g.world_objects:
                    entity.rect.x += round(offsetx * v.CAMERASLACK)
                    entity.rect.y += round(offsety * v.CAMERASLACK)
                for player in g.players: #ATTEMPTED TO OPTIMISE, BREAKS COLLISION SHADOW
                    player.pos.x += round(offsetx * v.CAMERASLACK)
                    player.pos.y += round(offsety * v.CAMERASLACK)
                for proj in g.projectiles:
                    proj.pos.x += round(offsetx * v.CAMERASLACK)
                    proj.pos.y += round(offsety * v.CAMERASLACK)
                for nme in g.enemies:
                    nme.pos.x += round(offsetx * v.CAMERASLACK)
                    nme.pos.y += round(offsety * v.CAMERASLACK)
                for text in g.map_texts:
                    text.rect.x += round(offsetx * v.CAMERASLACK)
                    text.rect.y += round(offsety * v.CAMERASLACK)

#Tutorial button
def Startlvl0():
    for entity in g.all_sprites:
        entity.kill()
    for entity in g.debug:
        entity.kill()
    lvl0.StartMap()
    v.LEVEL = 0
    v.GAMESTATE = 2
    v.CONTROLS = 1
    v.VICTORY = False
    v.DEAD = False
    pygame.mouse.set_visible(1)

def Startlvl1():
    for entity in g.all_sprites:
        entity.kill()
    for entity in g.debug:
        entity.kill()
    lvl1.StartMap()
    v.LEVEL = 1
    v.GAMESTATE = 2
    v.CONTROLS = 1
    v.VICTORY = False
    v.DEAD = False
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

#Toggle player controls
def ToggleControls():
    v.CONTROLS = not v.CONTROLS
    if not v.CONTROLS:
        v.MOUSECAM = False
        for player in g.players:
            player.jumpprompt = False
            player.dropping = False

def Victory():
    ToggleControls()
    v.VICTORY = True

def VictoryCheck():
    if v.VICTORY:
        v.VICTORY_TIME -= 1
        if v.VICTORY_TIME <= 0:
            v.LEVEL += 1
            v.VICTORY = False
            v.VICTORY_TIME = v.VICTORY_DUR
            if v.LEVEL + 1 > len(levellist):
                ReturnToLvlSelect()
            else:
                RestartLvl()
            

def LimitScroll():
    for f in g.focus:
        MousePos = vec(pygame.mouse.get_pos())
        if v.MOUSECAM == True:
            f.mousefocusx = (f.target.rect.centerx - MousePos.x) / v.MOUSECAMLIMITX#SOME VALUE
            f.mousefocusy = (f.target.rect.centery - MousePos.y) / v.MOUSECAMLIMITY
        else:
            f.mousefocusx = 0
            f.mousefocusy = 0
         
        for left in g.left_scroll_limits:
            for right in g.right_scroll_limits:
                f.rect.centerx = max(left.rect.centerx, min(f.target.rect.centerx - f.mousefocusx, right.rect.centerx))
        for top in g.top_scroll_limits:
            for bottom in g.bottom_scroll_limits:
                f.rect.centery = max(top.rect.centery, min(f.target.rect.centery - f.mousefocusy, bottom.rect.centery))

