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


# #Starting map LEGACY
# def StartMap():

#     #New method of classes cls.MapObject(size, color, originxy, group)
#     #ADD IN DRAW ORDER FROM BACKGROUND TO FOREGROUND
#     #Bottom floor
#     PT1 = cls.MapObject((v.WIDTH*3, 150), v.RED, (v.WIDTH/2, v.HEIGHT-75), (g.floors, g.world_objects, g.proj_collidables))
#     #Bounding walls
#     WL1 = cls.MapObject((500, 1700), v.RED, (-v.WIDTH, 250), (g.walls, g.world_objects, g.proj_collidables))
#     WL2 = cls.MapObject((500, 1700), v.RED, (v.WIDTH*2, 250), (g.walls, g.world_objects, g.proj_collidables))
#     CL1 = cls.MapObject((v.WIDTH*3, 400), v.RED, (v.WIDTH/2, -600), (g.floors, g.world_objects, g.proj_collidables))

#     #Enemies WOOO
#     NME1 = cls.Enemy((1220, 500))
#     NME2 = cls.Enemy((620, 500))
#     NME3 = cls.Enemy((120, 500))

#     #Player and collision shadow
#     P1 = cls.Player()
    
    
    

#     #Initial level gen
#     for x in range(random.randint(5, 6)):
#         pl = cls.MapObject((random.randint(100, 200), 24), v.GREEN, (random.randint(0 ,v.WIDTH-200), (random.randint(300 , v.HEIGHT-300))), (g.platforms, g.world_objects))

#     #Debug thingy
#     CENTER = cls.MapObject((30, 30), v.MAGENTA, (v.WIDTH/2, v.HEIGHT-148), (g.debug, g.world_objects, g.map_center))
#     SCREENFOCUS = cls.MapObject((30, 30), v.PURPLE, (v.WIDTH/2, v.HEIGHT/2), (g.debug, g.focus))
#     SCREENFOCUS.target = P1
#     SCROLL_BOTTOM = cls.MapObject((30, 30), v.CYAN, (v.WIDTH/2, v.HEIGHT-300), (g.debug, g.world_objects, g.bottom_scroll_limits))
#     SCROLL_TOP = cls.MapObject((30, 30), v.CYAN, (v.WIDTH/2, -300), (g.debug, g.world_objects, g.top_scroll_limits))
#     SCROLL_LEFT = cls.MapObject((30, 30), v.CYAN, (-v.WIDTH+700, v.HEIGHT/2), (g.debug, g.world_objects, g.left_scroll_limits))
#     SCROLL_RIGHT = cls.MapObject((30, 30), v.CYAN, (v.WIDTH*2-700, v.HEIGHT/2), (g.debug, g.world_objects, g.right_scroll_limits))

#     #TRG1 = cls.MapObject((20, 20), v.ORANGE, (500, 500), (g.world_objects, g.debug, g.triggers))
#     #TRG1.function = func.Victory
#     #TRG1.surf.set_alpha(128)

#     if v.DEBUG:
#         for debug in g.debug:
#             g.all_sprites.add(debug)

#     DRAWCHECK = cls.MapObject((v.WIDTH, v.HEIGHT), v.BLACK, (v.WIDTH/2, v.HEIGHT/2) , (g.draw_checks, g.draw_checks))

#Starting map NEW
def StartMap():

    func.PlayMusic("notmymusic3.wav")

    #Bounding area
    CLN1 = cls.MapObject((4100, 150), v.RED, (2000, 0), (g.ceilings, g.world_objects, g.proj_collidables))
    WALL1 = cls.MapObject((500, 5200), v.RED, (0, 2000), (g.walls, g.world_objects, g.proj_collidables))
    WALL2 = cls.MapObject((500, 5200), v.RED, (4260, 2000), (g.walls, g.world_objects, g.proj_collidables))
    PT2 = cls.MapObject((4100, 150), v.RED, (2000, 4500), (g.floors, g.world_objects, g.proj_collidables))

    #Top floor
    PT1 = cls.MapObject((3480, 150), v.RED, (1750, v.HEIGHT-75), (g.floors, g.world_objects, g.proj_collidables))
    CLN2 = cls.MapObject((3500, 150), v.RED, (1750, v.HEIGHT+75), (g.ceilings, g.world_objects, g.proj_collidables))
    WALL3 = cls.MapObject((200, 770), v.RED, (3400, 815), (g.walls, g.world_objects, g.proj_collidables))
    PT3 = cls.MapObject((200, 20), v.RED, (3400, 420), (g.floors, g.world_objects, g.proj_collidables))
    #2 BLOCKS
    PT5 = cls.MapObject((200, 24), v.RED, (2500, 562), (g.floors, g.world_objects, g.proj_collidables))
    WALL5 = cls.MapObject((200, 152), v.RED, (2500, 650), (g.walls, g.world_objects, g.proj_collidables))
    CLN5 = cls.MapObject((200, 24), v.RED, (2500, 738), (g.ceilings, g.world_objects, g.proj_collidables))

    PT6 = cls.MapObject((200, 24), v.RED, (1980, 562), (g.floors, g.world_objects, g.proj_collidables))
    WALL5 = cls.MapObject((200, 152), v.RED, (1980, 650), (g.walls, g.world_objects, g.proj_collidables))
    CLN6 = cls.MapObject((200, 24), v.RED, (1980, 738), (g.ceilings, g.world_objects, g.proj_collidables))

    PT27 = cls.MapObject((200, 24), v.GREEN, (3000, 500), (g.world_objects, g.platforms))

    MAP_TXT2 = txt.Text(txt.font_subtitle, "DEATH TO THE NME", v.GREEN, (0,0))
    TXT_BOX2 = cls.MapText(color=v.PURPLE, text=MAP_TXT2, originxy=(980, 700))

    #1 NME
    NME1 = cls.Enemy((2240, 800)) #ADD AGRRO RANGES


    #Second floor
    PT1 = cls.MapObject((3480, 150), v.RED, (2600, 2400), (g.floors, g.world_objects, g.proj_collidables))
    CLN3 = cls.MapObject((3500, 150), v.RED, (2450, 2550), (g.ceilings, g.world_objects, g.proj_collidables))
    WALL5 = cls.MapObject((200, 770), v.RED, (800, 2200), (g.walls, g.world_objects, g.proj_collidables))
    PT5 = cls.MapObject((200, 40), v.RED, (800, 1805), (g.floors, g.world_objects, g.proj_collidables))

    #BATHTUB (1 NME)
    WALL6 = cls.MapObject((50, 770), v.RED, (1500, 2000), (g.walls, g.world_objects, g.proj_collidables))
    PT7 = cls.MapObject((50, 20), v.RED, (1500, 1615), (g.floors, g.world_objects, g.proj_collidables))

    WALL7 = cls.MapObject((50, 770), v.RED, (3500, 2000), (g.walls, g.world_objects, g.proj_collidables))
    PT8 = cls.MapObject((50, 20), v.RED, (3500, 1615), (g.floors, g.world_objects, g.proj_collidables))

    #MANY PLATFORMS
    PT9 = cls.MapObject((150, 24), v.GREEN, (3800, 2000), (g.platforms, g.world_objects))
    PT10 = cls.MapObject((150, 24), v.GREEN, (3200, 1800), (g.platforms, g.world_objects))
    # PT11 = cls.MapObject((150, 24), v.GREEN, (2500, 1700), (g.platforms, g.world_objects))
    PT12 = cls.MapObject((150, 24), v.GREEN, (1800, 1800), (g.platforms, g.world_objects))
    PT13 = cls.MapObject((150, 24), v.GREEN, (2950, 2100), (g.platforms, g.world_objects))
    PT14 = cls.MapObject((150, 24), v.GREEN, (2050, 2100), (g.platforms, g.world_objects))
    PT15 = cls.MapObject((150, 24), v.GREEN, (1150, 2100), (g.platforms, g.world_objects))
    WALL8 = cls.MapObject((50, 770), v.RED, (2500, 1500), (g.walls, g.world_objects, g.proj_collidables))
    CLN7 = cls.MapObject((50, 20), v.RED, (2500, 1890), (g.ceilings, g.world_objects, g.proj_collidables))

    NME2 = cls.Enemy((2950, 1700)) #AGGRO DEAGGRO
    NME3 = cls.Enemy((2050, 1700)) #AGGRO DEAGGRO


    #Third floor
    PT1 = cls.MapObject((3480, 75), v.RED, (1750, 4067), (g.floors, g.world_objects, g.proj_collidables))
    WALL4 = cls.MapObject((200, 1030), v.RED, (3390, 3655), (g.walls, g.world_objects, g.proj_collidables))
    PT4 = cls.MapObject((200, 20), v.RED, (3390, 3135), (g.floors, g.world_objects, g.proj_collidables))
    CLN4 = cls.MapObject((3480, 75), v.RED, (1750, 4132), (g.ceilings, g.world_objects, g.proj_collidables))

    #BASIN OF DOOM (3 NMEs)
    #EVEN MORE PLATFORMS
    PT16 = cls.MapObject((300, 24), v.GREEN, (1150, 3500), (g.platforms, g.world_objects))
    # PT17 = cls.MapObject((300, 24), v.GREEN, (1850, 3500), (g.platforms, g.world_objects))
    PT18 = cls.MapObject((300, 24), v.GREEN, (2550, 3500), (g.platforms, g.world_objects))
    PT19 = cls.MapObject((300, 24), v.GREEN, (800, 3200), (g.platforms, g.world_objects))
    PT20 = cls.MapObject((300, 24), v.GREEN, (1500, 3200), (g.platforms, g.world_objects))
    PT21 = cls.MapObject((300, 24), v.GREEN, (2200, 3200), (g.platforms, g.world_objects))
    PT22 = cls.MapObject((300, 24), v.GREEN, (2900, 3200), (g.platforms, g.world_objects))
    PT23 = cls.MapObject((300, 24), v.GREEN, (800, 3800), (g.platforms, g.world_objects))
    PT24 = cls.MapObject((300, 24), v.GREEN, (1500, 3800), (g.platforms, g.world_objects))
    PT25 = cls.MapObject((300, 24), v.GREEN, (2200, 3800), (g.platforms, g.world_objects))
    PT26 = cls.MapObject((300, 24), v.GREEN, (2900, 3800), (g.platforms, g.world_objects))
    WALL8 = cls.MapObject((50, 1070), v.RED, (1850, 2950), (g.walls, g.world_objects, g.proj_collidables))
    CLN8 = cls.MapObject((50, 20), v.RED, (1850, 3485), (g.ceilings, g.world_objects, g.proj_collidables))

    NME4 = cls.Enemy((1150, 3450))
    NME5 = cls.Enemy((2550, 3450))
    NME6 = cls.Enemy((1850, 3900))
    

    #Bottom floor
    # EXIT DOOR
    #DECO
    #TEXT
    MAP_TXT1 = txt.Text(txt.font_subtitle, "EXIT", v.GREEN, (0,0))
    TXT_BOX1 = cls.MapText(color=v.PURPLE, text=MAP_TXT1, originxy=(500, 4250))

    #Player and collision shadow
    P1 = cls.Player()

    #Debug thingy
    CENTER = cls.MapObject((0, 0), v.MAGENTA, (0, 0), (g.debug, g.world_objects, g.map_center))
    SCREENFOCUS = cls.MapObject((30, 30), v.PURPLE, (v.WIDTH/2, v.HEIGHT-75), (g.debug, g.focus))
    SCREENFOCUS.target = P1
    SCROLL_BOTTOM = cls.MapObject((30, 30), v.CYAN, (v.WIDTH/2, 4000), (g.debug, g.world_objects, g.bottom_scroll_limits))
    SCROLL_TOP = cls.MapObject((30, 30), v.CYAN, (v.WIDTH/2, 500), (g.debug, g.world_objects, g.top_scroll_limits))
    SCROLL_LEFT = cls.MapObject((30, 30), v.CYAN, (1000, v.HEIGHT/2), (g.debug, g.world_objects, g.left_scroll_limits))
    SCROLL_RIGHT = cls.MapObject((30, 30), v.CYAN, (v.WIDTH*2-700, v.HEIGHT/2), (g.debug, g.world_objects, g.right_scroll_limits))


    TRG1 = cls.MapObject((200, 175), v.ORANGE, (500, 4350), (g.world_objects, g.debug, g.triggers))
    TRG1.function = func.Victory
    TRG1.surf.set_alpha(128)
    TRG1.function_param = None

    if v.DEBUG:
        for debug in g.debug:
            g.all_sprites.add(debug)

    DRAWCHECK = cls.MapObject((v.WIDTH, v.HEIGHT), v.BLACK, (v.WIDTH/2, v.HEIGHT/2) , (g.draw_checks, g.draw_checks))
