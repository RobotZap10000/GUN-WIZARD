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
    if v.MUSIC_ENABLED:
        pygame.mixer.music.stop()

    # # LEGACY LEVEL
    # #New method of classes cls.MapObject(size, color, originxy, group)
    # #ADD IN DRAW ORDER FROM BACKGROUND TO FOREGROUND
    # #Bottom floor
    # PT1 = cls.MapObject((v.WIDTH*3, 150), v.RED, (v.WIDTH/2, v.HEIGHT-75), (g.floors, g.world_objects, g.proj_collidables))
    # # # #Bounding walls
    # WL1 = cls.MapObject((500, 1700), v.RED, (-v.WIDTH, 250), (g.walls, g.world_objects, g.proj_collidables))
    # WL2 = cls.MapObject((500, 1700), v.RED, (v.WIDTH*2, 250), (g.walls, g.world_objects, g.proj_collidables))
    # CL1 = cls.MapObject((v.WIDTH*3, 400), v.RED, (v.WIDTH/2, -600), (g.ceilings, g.world_objects, g.proj_collidables))

    # PT2 = cls.MapObject((500, 24), v.GREEN, (0, 250), (g.platforms, g.world_objects))
    # PT3 = cls.MapObject((500, 24), v.GREEN, (v.WIDTH, 250), (g.platforms, g.world_objects))
    
    # PT4 = cls.MapObject((500, 24), v.GREEN, (-700, 650), (g.platforms, g.world_objects))


    # #Boss

    # BOSS = cls.Boss((2000, 700))



    # BOSS ARENA
    PT3 = cls.MapObject((v.WIDTH*5, 150), v.RED, (-830, 2950), (g.floors, g.world_objects, g.proj_collidables))
    CLN2 = cls.MapObject((v.WIDTH*5, 700), v.RED, (-830, 1150), (g.ceilings, g.world_objects, g.proj_collidables))
    WALL4 = cls.MapObject((500, 1700), v.RED, (-v.WIDTH-2660, 2195), (g.walls, g.world_objects, g.proj_collidables))
    WALL5 = cls.MapObject((500, 1700), v.RED, (v.WIDTH+1000, 2195), (g.walls, g.world_objects, g.proj_collidables))

    PT4 = cls.MapObject((500, 24), v.GREEN, (-v.WIDTH-830, 2200), (g.platforms, g.world_objects))
    PT5 = cls.MapObject((500, 24), v.GREEN, (-v.WIDTH-1830, 2200), (g.platforms, g.world_objects))
    PT6 = cls.MapObject((500, 24), v.GREEN, (-v.WIDTH-1330, 2550), (g.platforms, g.world_objects))
    PT10 = cls.MapObject((500, 24), v.GREEN, (-v.WIDTH-330, 2550), (g.platforms, g.world_objects))
    PT12 = cls.MapObject((500, 24), v.GREEN, (-v.WIDTH+170, 2200), (g.platforms, g.world_objects))

    PT7 = cls.MapObject((500, 24), v.GREEN, (v.WIDTH*1.5-830, 2200), (g.platforms, g.world_objects))
    PT8 = cls.MapObject((500, 24), v.GREEN, (v.WIDTH*1.5-1830, 2200), (g.platforms, g.world_objects))
    PT9 = cls.MapObject((500, 24), v.GREEN, (v.WIDTH*1.5-1330, 2550), (g.platforms, g.world_objects))
    PT11 = cls.MapObject((500, 24), v.GREEN, (v.WIDTH*1.5-2330, 2550), (g.platforms, g.world_objects))
    PT13 = cls.MapObject((500, 24), v.GREEN, (v.WIDTH*1.5-2830, 2200), (g.platforms, g.world_objects))

    
    # STARTING TUNNEL

    PT1 = cls.MapObject((v.WIDTH, 50), v.RED, (300, 800), (g.world_objects, g.proj_collidables, g.floors))
    WALL1 = cls.MapObject((1050, 500), v.RED, (1750, 600), (g.walls, g.world_objects, g.proj_collidables))
    CLN1 = cls.MapObject((6500, 1050), v.RED, (0, 0), (g.world_objects, g.proj_collidables, g.ceilings))
    WALL2 = cls.MapObject((3050, 1000), v.RED, (-2525, 1000), (g.walls, g.world_objects, g.proj_collidables))
    WALL3 = cls.MapObject((1050, 675), v.RED, (-135, 1162), (g.walls, g.world_objects, g.proj_collidables))
    PT2 = cls.MapObject((340, 50), v.RED, (-830, 800), (g.world_objects, g.floors, g.proj_collidables, g.props))

    #POWERUP
    MAP_TXT1 = txt.Text(txt.font_subtitle, "POWERUP", v.GREEN, (0,0))
    TXT_BOX1 = cls.MapText(color=v.PURPLE, text=MAP_TXT1, originxy=(-830, 600))
    POWERUP = cls.Enemy((-830, 715), size=(70, 70), color=v.BLUE, gravity=0, ai=2, dmg_mel = -100, flag="dont_count", kb_immune=True, kb=(0, 0, False))
    TRG1 = cls.MapObject((70, 70), v.ORANGE, (-830, 680), (g.world_objects, g.debug, g.triggers))
    TRG1.function = func.Cutscene
    TRG1.function_param = 0
    TRG1.surf.set_alpha(128)

    #Boss

    # BOSS = cls.Boss((-830, 2650))
    

    # #Player
    P1 = cls.Player(spawn=(v.WIDTH/2, 800))

     # LEGACY LEVEL LIMITS
    CENTER = cls.MapObject((30, 30), v.MAGENTA, (-830, 2875), (g.debug, g.world_objects, g.map_center))
    SCREENFOCUS = cls.MapObject((30, 30), v.PURPLE, (P1.rect.center), (g.debug, g.focus))
    SCREENFOCUS.target = P1
    SCROLL_BOTTOM = cls.MapObject((30, 30), v.CYAN, (v.WIDTH/2, 2485), (g.debug, g.world_objects, g.bottom_scroll_limits))
    SCROLL_TOP = cls.MapObject((30, 30), v.ORANGE, (v.WIDTH/2, v.HEIGHT/2+100), (g.debug, g.world_objects, g.top_scroll_limits))
    SCROLL_LEFT = cls.MapObject((30, 30), v.CYAN, (-v.WIDTH-1830, v.HEIGHT/2), (g.debug, g.world_objects, g.left_scroll_limits))
    SCROLL_RIGHT = cls.MapObject((30, 30), v.CYAN, (v.WIDTH+170, v.HEIGHT/2), (g.debug, g.world_objects, g.right_scroll_limits))

    if v.DEBUG:
        for debug in g.debug:
            g.all_sprites.add(debug)

    DRAWCHECK = cls.MapObject((v.WIDTH, v.HEIGHT), v.BLACK, (v.WIDTH/2, v.HEIGHT/2) , (g.draw_checks, g.draw_checks))

