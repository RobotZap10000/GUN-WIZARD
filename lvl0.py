#importing CHANGE CHANGE
import pygame#, sys
from pygame.locals import *
import random#, time
import variables as v
import texts as txt
import groups as g
import classes as cls
import functions as func

#initializing
pygame.init()
vec = pygame.math.Vector2 #2 = 2D


#TXT1 = txt.Text(txt.font_subtitle, "BRUH", v.GREEN, (0, 0))

#Starting map
def StartMap():

    func.PlayMusic("notmymusic2.wav")

    # # LEGACY LEVEL
    # #New method of classes cls.MapObject(size, color, originxy, group)
    # #ADD IN DRAW ORDER FROM BACKGROUND TO FOREGROUND
    # #Bottom floor
    # PT1 = cls.MapObject((v.WIDTH*3, 150), v.RED, (v.WIDTH/2, v.HEIGHT-75), (g.floors, g.world_objects, g.proj_collidables))
    # #Bounding walls
    # WL1 = cls.MapObject((500, 1700), v.RED, (-v.WIDTH, 250), (g.walls, g.world_objects, g.proj_collidables))
    # WL2 = cls.MapObject((500, 1700), v.RED, (v.WIDTH*2, 250), (g.walls, g.world_objects, g.proj_collidables))
    # CL1 = cls.MapObject((v.WIDTH*3, 400), v.RED, (v.WIDTH/2, -600), (g.floors, g.world_objects, g.proj_collidables))
    

    # #Thing 1
    # FLR1 = cls.MapObject((200, 24), v.RED, (300, 776), (g.floors, g.world_objects, g.proj_collidables))
    # WALL1 = cls.MapObject((24, 200), v.BLUE, (212, 664), (g.walls, g.world_objects, g.proj_collidables))
    # CLN1 = cls.MapObject((200, 24), v.CYAN, (300, 552), (g.ceilings, g.world_objects, g.proj_collidables))
    # #Thing 2 BOX PLEASE?????
    # CLN2 = cls.MapObject((200, 24), v.CYAN, (700, 776), (g.ceilings, g.world_objects, g.proj_collidables))
    # WALL2 = cls.MapObject((24, 152), v.BLUE, (612, 688), (g.walls, g.world_objects, g.proj_collidables))
    # WALL3 = cls.MapObject((24, 152), v.BLUE, (788, 688), (g.walls, g.world_objects, g.proj_collidables))
    # FLR2 = cls.MapObject((200, 24), v.RED, (700, 600), (g.floors, g.world_objects, g.proj_collidables))
    # #Thing 3 maybe this time
    # CLN3 = cls.MapObject((200, 24), v.CYAN, (1220, 776), (g.ceilings, g.world_objects, g.proj_collidables))
    # WALL4 = cls.MapObject((24, 152), v.BLUE, (1308, 688), (g.walls, g.world_objects, g.proj_collidables))
    # WALL5 = cls.MapObject((24, 152), v.BLUE, (1132, 688), (g.walls, g.world_objects, g.proj_collidables))
    # FLR3 = cls.MapObject((200, 24), v.RED, (1220, 600), (g.platforms, g.world_objects))


    # #TEXT???? 
    # TUT_TXT1 = cls.MapText(size=(500, 200), color=v.BLUE, text=TXT1)

    # #Initial level gen
    # for x in range(random.randint(5, 6)):
    #     pl = cls.MapObject((random.randint(100, 200), 24), v.GREEN, (random.randint(0 ,v.WIDTH-200), (random.randint(300 , v.HEIGHT-300))), (g.platforms, g.world_objects))

    # #Tutorial level
    PT1 = cls.MapObject((v.WIDTH*2, 200), v.RED, (700, v.HEIGHT-100), (g.floors, g.world_objects, g.proj_collidables))
    PT4 = cls.MapObject((v.WIDTH, 200), v.RED, (4000, v.HEIGHT-100), (g.floors, g.world_objects, g.proj_collidables))
    CLN7 = cls.MapObject((v.WIDTH*2, 280), v.RED, (700, v.HEIGHT+140), (g.ceilings, g.world_objects, g.proj_collidables))
    CLN8 = cls.MapObject((v.WIDTH, 280), v.RED, (4000, v.HEIGHT+140), (g.ceilings, g.world_objects, g.proj_collidables))
    WALL1 = cls.MapObject((200, 5000), v.RED, (0, 2500), (g.walls, g.world_objects, g.proj_collidables))
    WALL2 = cls.MapObject((200, v.HEIGHT-380), v.RED, (v.WIDTH, v.HEIGHT/2-190), (g.walls, g.world_objects, g.proj_collidables))
    CLN4 = cls.MapObject((200, 20), v.RED, (v.WIDTH, 700), (g.ceilings, g.world_objects, g.proj_collidables))
    WALL3 = cls.MapObject((200, 5000), v.RED, (3800, 2500), (g.walls, g.world_objects, g.proj_collidables))
    CLN1 = cls.MapObject((v.WIDTH*3, 200), v.RED, (v.WIDTH/2, -100), (g.ceilings, g.world_objects, g.proj_collidables))

    PT2 = cls.MapObject((1500, 20), v.RED, (750, 210), (g.floors, g.world_objects, g.proj_collidables))
    WALL3 = cls.MapObject((1500, 20), v.RED, (750, 230), (g.walls, g.world_objects, g.proj_collidables))
    CLN2 = cls.MapObject((1500, 20), v.RED, (750, 250), (g.ceilings, g.world_objects, g.proj_collidables))

    TUT_TXT1 = txt.Text(txt.font_subtitle, "PRESS A OR D", v.GREEN, (0,0))
    TUT_BOX1 = cls.MapText(color=v.PURPLE, text=TUT_TXT1, originxy=(965, 350))
    TUT_TXT2 = txt.Text(txt.font_subtitle, "TO MOVE AROUND", v.GREEN, (0,0))
    TUT_BOX2 = cls.MapText(color=v.PURPLE, text=TUT_TXT2, originxy=(965, 450))

    PT3 = cls.MapObject((1500, 20), v.RED, (1200, 550), (g.floors, g.world_objects, g.proj_collidables))
    CLN3 = cls.MapObject((1500, 20), v.RED, (1200, 590), (g.ceilings, g.world_objects, g.proj_collidables))
    WALL4 = cls.MapObject((1500, 20), v.RED, (1200, 570), (g.walls, g.world_objects, g.proj_collidables))

    WALL5 = cls.MapObject((60, 840), v.RED, (2600, v.HEIGHT-80), (g.walls, g.world_objects, g.proj_collidables))
    WALL6 = cls.MapObject((60, 840), v.RED, (3050, v.HEIGHT-80), (g.walls, g.world_objects, g.proj_collidables))
    PT8 = cls.MapObject((60, 20), v.RED, (2600, 570), (g.floors, g.world_objects, g.proj_collidables))
    PT9 = cls.MapObject((60, 20), v.RED, (3050, 570), (g.floors, g.world_objects, g.proj_collidables))
    CLN5 = cls.MapObject((54, 20), v.RED, (2597, 1430), (g.ceilings, g.world_objects, g.proj_collidables))
    CLN6 = cls.MapObject((54, 20), v.RED, (3053, 1430), (g.ceilings, g.world_objects, g.proj_collidables))

    TUT_TXT3 = txt.Text(txt.font_subtitle, "PRESS W TO JUMP", v.GREEN, (0,0))
    TUT_BOX3 = cls.MapText(color=v.PURPLE, text=TUT_TXT3, originxy=(2300, 470))
    TUT_TXT4 = txt.Text(txt.font_subtitle, "AND HOLD TO JUMP", v.GREEN, (0,0))
    TUT_BOX4 = cls.MapText(color=v.PURPLE, text=TUT_TXT4, originxy=(2300, 570))
    TUT_TXT5 = txt.Text(txt.font_subtitle, "HIGHER", v.GREEN, (0,0))
    TUT_BOX5 = cls.MapText(color=v.PURPLE, text=TUT_TXT5, originxy=(2300, 670))

    TUT_TXT6 = txt.Text(txt.font_subtitle, "HOLD S TO FALL", v.GREEN, (0,0))
    TUT_BOX6 = cls.MapText(color=v.PURPLE, text=TUT_TXT6, originxy=(3400, 70))
    TUT_TXT7 = txt.Text(txt.font_subtitle, "THROUGH GREEN", v.GREEN, (0,0))
    TUT_BOX7 = cls.MapText(color=v.PURPLE, text=TUT_TXT7, originxy=(3400, 170))
    TUT_TXT8 = txt.Text(txt.font_subtitle, "PLATFORMS", v.GREEN, (0,0))
    TUT_BOX8 = cls.MapText(color=v.PURPLE, text=TUT_TXT8, originxy=(3400, 270))

    PT5 = cls.MapObject((402, 20), v.GREEN, (2825, 570), (g.platforms, g.world_objects))
    PT6 = cls.MapObject((402, 20), v.GREEN, (2825, 1000), (g.platforms, g.world_objects))
    PT7 = cls.MapObject((402, 20), v.GREEN, (2825, 1430), (g.platforms, g.world_objects))
    
    #ADD FLR AND CLN TO TIPS

    PT8 = cls.MapObject((v.WIDTH*3, 200), v.RED, (2900, 3500), (g.floors, g.world_objects, g.proj_collidables))
    NME1 = cls.Enemy((2500, 3400), ai=2, aggro=0, deaggro=0, dmg_mel=0)

    TUT_TXT9 = txt.Text(txt.font_subtitle, "PRESS 1, 2 OR 3", v.GREEN, (0,0))
    TUT_BOX9 = cls.MapText(color=v.PURPLE, text=TUT_TXT9, originxy=(3400, 3000))
    TUT_TXT10 = txt.Text(txt.font_subtitle, "TO SWAP BETWEEN", v.GREEN, (0,0))
    TUT_BOX10 = cls.MapText(color=v.PURPLE, text=TUT_TXT10, originxy=(3400, 3100))
    TUT_TXT11 = txt.Text(txt.font_subtitle, "YOUR ATTACKS", v.GREEN, (0,0))
    TUT_BOX11 = cls.MapText(color=v.PURPLE, text=TUT_TXT11, originxy=(3400, 3200))

    TUT_TXT12 = txt.Text(txt.font_subtitle, "USE YOUR CURSOR", v.GREEN, (0,0))
    TUT_BOX12 = cls.MapText(color=v.PURPLE, text=TUT_TXT12, originxy=(2500, 2900))
    TUT_TXT13 = txt.Text(txt.font_subtitle, "TO AIM AND PRESS", v.GREEN, (0,0))
    TUT_BOX13 = cls.MapText(color=v.PURPLE, text=TUT_TXT13, originxy=(2500, 3000))
    TUT_TXT14 = txt.Text(txt.font_subtitle, "LMB TO FIRE", v.GREEN, (0,0))
    TUT_BOX14 = cls.MapText(color=v.PURPLE, text=TUT_TXT14, originxy=(2500, 3100))

    WALL7 = cls.MapObject((60, 500), v.RED, (1000, 3150), (g.walls, g.proj_collidables, g.world_objects))
    PT10 = cls.MapObject((60, 20), v.RED, (1000, 2890), (g.floors, g.proj_collidables, g.world_objects))
    PT11 = cls.MapObject((200, 20), v.GREEN, (1400, 3000), (g.platforms, g.world_objects))
    PT12 = cls.MapObject((200, 20), v.GREEN, (1800, 3200), (g.platforms, g.world_objects))
    PT13 = cls.MapObject((200, 20), v.GREEN, (600, 3000), (g.platforms, g.world_objects))
    PT14 = cls.MapObject((200, 20), v.GREEN, (600, 1750), (g.platforms, g.world_objects))
    NME2 = cls.Enemy((600, 1750), ai=2, aggro=0, deaggro=0, dmg_mel=0)

    TUT_TXT15 = txt.Text(txt.font_subtitle, "HOLD RMB TO", v.GREEN, (0,0))
    TUT_BOX15 = cls.MapText(color=v.PURPLE, text=TUT_TXT15, originxy=(600, 2400))
    TUT_TXT16 = txt.Text(txt.font_subtitle, "LOOK FARTHER", v.GREEN, (0,0))
    TUT_BOX16 = cls.MapText(color=v.PURPLE, text=TUT_TXT16, originxy=(600, 2500))
    TUT_TXT17 = txt.Text(txt.font_subtitle, "<-- SHOOT ME", v.GREEN, (0,0))
    TUT_BOX17 = cls.MapText(color=v.PURPLE, text=TUT_TXT17, originxy=(1000, 1700))








    
    # #Player
    P1 = cls.Player(spawn=(300, 200), vic_cond="NME_KILLED")

    # #Tutorial level limits
    CENTER = cls.MapObject((30, 30), v.MAGENTA, (0, 0), (g.debug, g.world_objects, g.map_center))
    SCREENFOCUS = cls.MapObject((30, 30), v.PURPLE, (P1.rect.center), (g.debug, g.focus))
    SCREENFOCUS.target = P1
    SCROLL_BOTTOM = cls.MapObject((30, 30), v.CYAN, (v.WIDTH/2, 3000), (g.debug, g.world_objects, g.bottom_scroll_limits))
    SCROLL_TOP = cls.MapObject((30, 30), v.CYAN, (v.WIDTH/2, 500), (g.debug, g.world_objects, g.top_scroll_limits))
    SCROLL_LEFT = cls.MapObject((30, 30), v.CYAN, (1000, v.HEIGHT/2), (g.debug, g.world_objects, g.left_scroll_limits))
    SCROLL_RIGHT = cls.MapObject((30, 30), v.CYAN, (2800, v.HEIGHT/2), (g.debug, g.world_objects, g.right_scroll_limits))

    # LEGACY LEVEL LIMITS
    # CENTER = cls.MapObject((30, 30), v.MAGENTA, (v.WIDTH/2, v.HEIGHT-148), (g.debug, g.world_objects, g.map_center))
    # SCREENFOCUS = cls.MapObject((30, 30), v.PURPLE, (P1.rect.center), (g.debug, g.focus))
    # SCREENFOCUS.target = P1
    # SCROLL_BOTTOM = cls.MapObject((30, 30), v.CYAN, (v.WIDTH/2, v.HEIGHT-600), (g.debug, g.world_objects, g.bottom_scroll_limits))
    # SCROLL_TOP = cls.MapObject((30, 30), v.CYAN, (v.WIDTH/2, 0), (g.debug, g.world_objects, g.top_scroll_limits))
    # SCROLL_LEFT = cls.MapObject((30, 30), v.CYAN, (-v.WIDTH+850, v.HEIGHT/2), (g.debug, g.world_objects, g.left_scroll_limits))
    # SCROLL_RIGHT = cls.MapObject((30, 30), v.CYAN, (v.WIDTH*2-550, v.HEIGHT/2), (g.debug, g.world_objects, g.right_scroll_limits))

    # Map triggers
    # TRG1 = cls.MapObject((20, 20), v.ORANGE, (500, 500), (g.world_objects, g.debug, g.triggers))
    # TRG1.function = func.Victory
    # TRG1.surf.set_alpha(128)

    if v.DEBUG:
        for debug in g.debug:
            g.all_sprites.add(debug)

    DRAWCHECK = cls.MapObject((v.WIDTH, v.HEIGHT), v.BLACK, (v.WIDTH/2, v.HEIGHT/2) , (g.draw_checks, g.draw_checks))