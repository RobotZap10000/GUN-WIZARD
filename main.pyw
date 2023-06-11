#importing
import pygame
from pygame.locals import *
import variables as v
import texts as txt
import groups as g
import menus as menu
import functions as func

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


#Game loop

while True:
    
    #Title screen
    if v.GAMESTATE == 0:

    #Event listener
        for event in pygame.event.get():
            if event.type == QUIT:
               func.QuitGame()

            #Checking for key press
            if event.type == pygame.KEYDOWN:    

                #debug menu
                if event.key == pygame.K_i:
                    #TOGGLE DEBUG
                    v.DEBUG = not v.DEBUG

                #Starting game   
                else:
                    func.ReturnToLvlSelect()

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
               func.QuitGame()

            #Checking for key press
            if event.type == pygame.KEYDOWN:    

                #debug menu
                if event.key == pygame.K_i:
                   func.ToggleDebug()
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
               func.QuitGame()

            #Checking for key press
            if event.type == pygame.KEYDOWN:
                if v.CONTROLS: 
                    for player in g.players:   
                        if event.key == pygame.K_w:
                                player.jumpprompt = True

                        if event.key == pygame.K_s:
                                player.dropping = True

                    for nme in g.enemies:
                        if event.key == pygame.K_h:
                                nme.dropping = True

                        if event.key == pygame.K_y:
                                nme.jumpprompt = True
                    
                #debugging
                if event.key == pygame.K_c:
                    # v.FPS = 2
                    pass                        #Use this if nothing needed

                #debugging
                if event.key == pygame.K_v:
                    # v.FPS = 60
                    pass

                if event.key == pygame.K_b:
                    v.BRAIN = not v.BRAIN
                
                #debug menu
                if event.key == pygame.K_i:
                   func.ToggleDebug()
                    #v.DEBUG = not v.DEBUG

                #Pausing
                if event.key == pygame.K_ESCAPE:
                    func.TogglePause()

                for player in g.players:
                    if event.key == pygame.K_1:
                        if player.weapon != 1:
                            player.weapon = 1
                            player.firedelay = 10

                    if event.key == pygame.K_2:
                        if player.weapon != 2:
                            player.weapon = 2
                            player.firedelay = 5
                        
                    if event.key == pygame.K_3:
                        if player.weapon != 3:
                            player.weapon = 3
                            player.firedelay = 30

            #Checking for key release
            if event.type == pygame.KEYUP:
                if v.CONTROLS:
                    for player in g.players:
                        if event.key == pygame.K_w:
                                player.jumpprompt = False
                                player.cancel_jump()
                        if event.key == pygame.K_s:
                                player.dropping = False

                for nme in g.enemies:
                    if event.key == pygame.K_y:
                            nme.jumpprompt = False
                            nme.cancel_jump()

                    if event.key == pygame.K_h:
                            nme.dropping = False

        if v.PAUSED == False:

            if v.CONTROLS:
            
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

            for hud in g.HUD:
                hud.update()
            
            #ScrollScreen()
            func.ScrollScreen()
            func.LimitScroll()

        #CHECK VICTORY
        func.VictoryCheck()
        func.CutsceneCheck()

        #Surface drawing
        displaysurface.fill(v.BGGRAY)

        for entity in g.all_sprites:
            if entity not in g.HUD:
                draw_check = pygame.sprite.spritecollide(entity, g.draw_checks, False)
                if draw_check:
                    displaysurface.blit(entity.surf, entity.rect)

        for hud in g.HUD:
            if hud.background != None:
                displaysurface.blit(hud.background, hud.background_rect)
            displaysurface.blit(hud.surf, hud.rect)
            if hud.symbol != None:
                displaysurface.blit(hud.symbol.text, hud.symbol.rect)
            if hud.text != None:
                displaysurface.blit(hud.text.text, hud.text.rect)

        #Pause menu buttons
        menu.DrawPauseMenu()
        menu.DrawDeathMenu()

        #Pause menu text
        txt.DrawPauseMenu()
        txt.DrawDeathMenu()

        #Victory text
        txt.DrawVictoryText()

        #debug menu
        v.FRAMESCOUNTED = str((round(FramePerSec.get_fps(), 1))) #LAZY FIX
        txt.DrawDebugMenu()

        #Frame updating
        pygame.display.update()
        FramePerSec.tick(v.FPS)

    
    






















        











        
    

