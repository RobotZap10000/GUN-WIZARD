import pygame, sys
from pygame.locals import *
import random, time
import variables as v
import texts as txt
import groups as g
#import menus as menu
import lvl0
import lvl1
import lvl2

pygame.init()
vec = pygame.math.Vector2

MUSIC_END = pygame.USEREVENT+1

#Playing music
def PlayMusic(music):
    if v.MUSIC_ENABLED:
        if v.MUSIC != music:
            v.MUSIC = music
            pygame.mixer.music.load(v.MUSIC)
            pygame.mixer.music.play(-1)

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
    PlayMusic("notmymusic1.wav")
    KillAll()
    v.GAMESTATE = 0
    v.PAUSED = False
    pygame.mouse.set_visible(0)
    v.LEVEL = None

#Return to level select screen
def ReturnToLvlSelect():
    PlayMusic("notmymusic1.wav")
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

def Startlvl2():
    for entity in g.all_sprites:
        entity.kill()
    for entity in g.debug:
        entity.kill()
    lvl2.StartMap()
    v.LEVEL = 2
    v.GAMESTATE = 2
    v.CONTROLS = 1
    v.VICTORY = False
    v.DEAD = False
    pygame.mouse.set_visible(1)

levellist = [
    Startlvl0,
    Startlvl1,
    Startlvl2
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
    if v.MUSIC_ENABLED:
        pygame.mixer.music.stop()
        v.MUSIC = "notmymusic5.wav"
        pygame.mixer.music.load(v.MUSIC)
        pygame.mixer.music.play(1)
    ToggleControls()
    v.VICTORY = True

def VictoryCheck():
    if v.VICTORY:
        v.VICTORY_TIME -= 1
        if v.VICTORY_TIME <= 0:
            if v.MUSIC_ENABLED:
                pygame.mixer.music.stop()
            v.LEVEL += 1
            v.VICTORY = False
            v.VICTORY_TIME = v.VICTORY_DUR
            if v.LEVEL + 1 > len(levellist):
                ReturnToLvlSelect()
            else:
                RestartLvl()

def Cutscene(type):
    if type == 0:
        if v.MUSIC_ENABLED:
            v.MUSIC = "notmymusic4.1.wav"
            pygame.mixer.music.load(v.MUSIC)
            pygame.mixer.music.play(1)
            pygame.mixer.music.set_endevent(MUSIC_END)
        ToggleControls()
        v.CUTSCENE = True
        for player in g.players:
            player.buff = "manaboost"
        for prop in g.props:
            g.floors.remove(prop)

    if type == 1:
        if v.MUSIC_ENABLED:
            v.MUSIC = "notmymusic4.3.wav"
            pygame.mixer.music.load(v.MUSIC)
            pygame.mixer.music.play(1)
        ToggleControls()
        v.CUTSCENE = True
        for focus in g.focus:
            for boss in g.enemies:
                if boss.tag == "BOSS":
                    focus.target = boss

    v.CUTSCENE_TYPE = type
    v.CUTSCENE_TIME = v.CUTSCENE_DUR[v.CUTSCENE_TYPE]

def CutsceneCheck():
    if v.CUTSCENE:
        v.CUTSCENE_TIME -= 1
        if v.CUTSCENE_TYPE == 0:
            if v.CUTSCENE_TIME <= 0:
                ToggleControls()
                v.CUTSCENE = False
                v.CUTSCENE_TIME = v.CUTSCENE_DUR[v.CUTSCENE_TYPE]
                PlayMusic("notmymusic4.2.wav")
                for player in g.players:
                    player.spawnboss()
                if v.MUSIC_ENABLED:
                    pygame.mixer.music.set_endevent(MUSIC_END)

        if v.CUTSCENE_TYPE == 1:
            if v.CUTSCENE_TIME == 330:
                for boss in g.enemies:
                    if boss.tag == "BOSS":
                        for exp in g.explosions:
                            exp.kill()
                        boss.explode()
                        boss.collision.kill()
                        boss.kill()
                for limb in g.boss_limbs:
                    limb.collision.kill()
                    limb.kill()
                for hud in g.HUD:
                    if hud.unit == "boss_health":
                        hud.kill()

            elif v.CUTSCENE_TIME <= 0:
                Victory()
                ToggleControls()
                for player in g.players:
                    for focus in g.focus:
                        focus.target = player
                v.CUTSCENE = False
                v.CUTSCENE_TIME = v.CUTSCENE_DUR[v.CUTSCENE_TYPE]


def ForceCutscene():
    if v.CUTSCENE:
        ToggleControls()
        v.CUTSCENE = False
        v.CUTSCENE_TIME = v.CUTSCENE_DUR
        PlayMusic("notmymusic4.2.wav")
        for player in g.players:
            player.spawnboss()
        if v.MUSIC_ENABLED:
            pygame.mixer.music.set_endevent()


            

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

