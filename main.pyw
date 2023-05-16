#importing
import pygame, sys
from pygame.locals import *
import random, time
import variables as v
import texts as txt
import groups as g
import menus as menu
import classes as cls
import lvl0
import platform as pyplatform

#Version checking
#3.11.2
#2.2.0
if pyplatform.python_version() == "3.11.2":
    print("Python fully compatible.")
else:
    print("!WARNING! Python version may be incompatible!")

if pygame.__version__ == "2.2.0":
    print("Pygame fully compatible.")
else:
    print("!WARNING! Pygame version may be incompatible!")


#initializing
pygame.init()
vec = pygame.math.Vector2 #2 = 2D

#Hiding cursor
pygame.mouse.set_visible(0)

#game clock
FramePerSec = pygame.time.Clock()

#game window
displaysurface = pygame.display.set_mode((v.WIDTH, v.HEIGHT))
pygame.display.set_caption("GUN WIZARD")

def QuitGame():
    pygame.quit()
    sys.exit()

def KillAll():
    for entity in g.all_sprites:
        entity.kill()
    for entity in g.debug:
        entity.kill()

def ReturnToTitle():
    KillAll()
    v.GAMESTATE = 0
    v.PAUSED = False
    pygame.mouse.set_visible(0)

def TogglePause():
    v.PAUSED = not v.PAUSED

def ToggleDebug():
    v.DEBUG = not v.DEBUG
    if v.DEBUG:
        for entity in g.debug:
            g.all_sprites.add(entity)
    else:
        for entity in g.debug:
            g.all_sprites.remove(entity)

def ReturnToLvlSelect():
    KillAll()
    v.GAMESTATE = 1
    v.PAUSED = False
    pygame.mouse.set_visible(1)

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


def LimitScroll():
    for f in g.focus:
        MousePos = vec(pygame.mouse.get_pos())
        if v.MOUSECAM == True:
            f.mousefocusx = (f.target.rect.centerx - MousePos.x) / v.MOUSECAMLIMIT#SOME VALUE
            f.mousefocusy = (f.target.rect.centery - MousePos.y) / v.MOUSECAMLIMIT
        else:
            f.mousefocusx = 0
            f.mousefocusy = 0
         
        for left in g.left_scroll_limits:
            for right in g.right_scroll_limits:
                f.rect.centerx = max(left.rect.centerx + 150, min(f.target.rect.centerx - f.mousefocusx, right.rect.centerx - 150))
        for top in g.top_scroll_limits:
            for bottom in g.bottom_scroll_limits:
                f.rect.centery = max(top.rect.centery + 300, min(f.target.rect.centery - f.mousefocusy, bottom.rect.centery - 300))
    
    
#Button function mapping
menu.lvlselect_quit.function = QuitGame
menu.lvlselect_back.function = ReturnToTitle

menu.resumegame_button.function = TogglePause
menu.return_to_lvlselect_button.function = ReturnToLvlSelect
menu.pausemenu_quit_button.function = QuitGame

#Game loop

while True:
    
    #Title screen
    if v.GAMESTATE == 0:

    #Event listener
        for event in pygame.event.get():
            if event.type == QUIT:
                QuitGame()

            #Checking for key press
            if event.type == pygame.KEYDOWN:    

                #debug menu
                if event.key == pygame.K_i:
                    #TOGGLE DEBUG
                    v.DEBUG = not v.DEBUG

                #Starting game   
                else:
                    ReturnToLvlSelect()

        #Title
        txt.DrawTitleScreen()

        #debug menu
        v.FRAMESCOUNTED = str((round(FramePerSec.get_fps(), 1))) #LAZY FIX
        txt.DrawDebugMenu()
        
        #Frame updating
        pygame.display.update()
        FramePerSec.tick(v.FPS)

    #Level select
    if v.GAMESTATE == 1:
        
        #Event listener
        for event in pygame.event.get():
            if event.type == QUIT:
                QuitGame()

            #Checking for key press
            if event.type == pygame.KEYDOWN:    

                #debug menu
                if event.key == pygame.K_i:
                    ToggleDebug()
                    #v.DEBUG = not v.DEBUG


        #Level select text
        txt.DrawLevelSelect()
        
        #Level select buttons
        menu.DrawLvlSelect()

        #debug menu
        v.FRAMESCOUNTED = str((round(FramePerSec.get_fps(), 1))) #LAZY FIX
        txt.DrawDebugMenu()
        
        #Frame updating
        pygame.display.update()
        FramePerSec.tick(v.FPS)
            
    #In-game ADD PER MAP?
    if v.GAMESTATE == 2:
        
        #Event listener
        for event in pygame.event.get():
            if event.type == QUIT:
                QuitGame()

            #Checking for key press
            if event.type == pygame.KEYDOWN:    
                if event.key == pygame.K_w:
                    for player in g.players:
                        player.jumpprompt = True

                if event.key == pygame.K_y:
                    for nme in g.enemies:
                        nme.jumpprompt = True
                    
                if event.key == pygame.K_s:
                    for player in g.players:
                        player.dropping = True

                if event.key == pygame.K_h:
                    for nme in g.enemies:
                        nme.dropping = True
                    
                #debugging
                if event.key == pygame.K_c:
                    v.FPS = 2
                    #pass                        #Use this if nothing needed

                #debugging
                if event.key == pygame.K_v:
                    v.FPS = 60
                    #pass

                if event.key == pygame.K_b:
                    v.BRAIN = not v.BRAIN

                #debugging
                if event.key == pygame.K_k:
                    #PLAYER DEATH
                    for player in g.players:
                        for f in g.focus:
                            f.rect.center = player.pos
                        player.kill()
                        player.collision.kill()
                        #pass

                if event.key == pygame.K_e:
                    for nme in g.enemies:
                        nme.kill()
                        nme.collision.kill()
                
                #debug menu
                if event.key == pygame.K_i:
                    ToggleDebug()
                    #v.DEBUG = not v.DEBUG

                #Returning to title screen
                if event.key == pygame.K_m:
                    ReturnToTitle()

                #Pausing
                if event.key == pygame.K_ESCAPE:
                    TogglePause()

                for player in g.players:
                    if event.key == pygame.K_1:
                        player.weapon = 1
                        player.firedelay = 10

                    if event.key == pygame.K_2:
                        player.weapon = 2
                        player.firedelay = 0
                        
                    if event.key == pygame.K_3:
                        player.weapon = 3
                        player.firedelay = 30
                        
            #Checking for key release
            if event.type == pygame.KEYUP:      
                if event.key == pygame.K_w:
                    for player in g.players:
                        player.jumpprompt = False
                        player.cancel_jump()

                if event.key == pygame.K_y:
                    for nme in g.enemies:
                        nme.jumpprompt = False
                        nme.cancel_jump()
                        
                if event.key == pygame.K_s:
                    for player in g.players:
                        player.dropping = False

                if event.key == pygame.K_h:
                    for nme in g.enemies:
                        nme.dropping = False
                    

        if v.PAUSED == False:
            
            #Player firing
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                for player in g.players:
                    player.shoot()
                        #TESTERPROJ = cls.Projectile((0, 0), 2, (0, 10), player.aim, 300)
                        #TESTERPROJ = cls.Projectile((0, 0.2), 2, (0, 0), player.aim, 300)
                        #TESTERPROJ = cls.Projectile((0, 0.1), 2, (0, 0), player.aim, 300)
                        #^Interesting bug, use for BOSS?

            if pygame.mouse.get_pressed(num_buttons=3)[2]:
                v.MOUSECAM = True
                v.CAMERASLACK = v.CAMERAROUGH
            else:
                v.MOUSECAM = False
                v.CAMERASLACK = v.CAMERASMOOTH
                        
            #Sprite updating
            for player in g.players:
                player.update()
                player.move()

            for nme in g.enemies:
                nme.update()
                nme.brain()
                nme.move()
                
            for proj in g.projectiles:
                proj.move()
                proj.collide()
                proj.update()

            for exp in g.explosions:
                exp.update()

            for entity in g.debug:
                entity.move()
            
            #ScrollScreen()
            ScrollScreen()
            LimitScroll()

        #Surface drawing
        displaysurface.fill(v.BGGRAY)

        for entity in g.all_sprites:
            displaysurface.blit(entity.surf, entity.rect)

        #Pause menu buttons
        menu.DrawPauseMenu()

        #Pause menu text
        txt.DrawPauseMenu()

        #debug menu
        v.FRAMESCOUNTED = str((round(FramePerSec.get_fps(), 1))) #LAZY FIX
        txt.DrawDebugMenu()

        #Frame updating
        pygame.display.update()
        FramePerSec.tick(v.FPS)
        v.TICK += 1

    
    






















        











        
    

