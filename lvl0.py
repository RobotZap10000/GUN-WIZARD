#importing CHANGE CHANGE
import pygame#, sys
from pygame.locals import *
import random#, time
import variables as v
import texts as txt
import groups as g
import classes as cls

#initializing
pygame.init()
vec = pygame.math.Vector2 #2 = 2D


#Starting map
def StartMap():

    #New method of classes cls.MapObject(size, color, originxy, group)
    #ADD IN DRAW ORDER FROM BACKGROUND TO FOREGROUND
    #Bottom floor
    PT1 = cls.MapObject((v.WIDTH*3, 150), v.RED, (v.WIDTH/2, v.HEIGHT-75), (g.floors, g.world_objects, g.proj_collidables))

    #Thing 1
    FLR1 = cls.MapObject((200, 24), v.RED, (300, 776), (g.floors, g.world_objects, g.proj_collidables))
    WALL1 = cls.MapObject((24, 200), v.BLUE, (212, 664), (g.walls, g.world_objects, g.proj_collidables))
    CLN1 = cls.MapObject((200, 24), v.CYAN, (300, 552), (g.ceilings, g.world_objects, g.proj_collidables))
    #Thing 2 BOX PLEASE?????
    CLN2 = cls.MapObject((200, 24), v.CYAN, (700, 776), (g.ceilings, g.world_objects, g.proj_collidables))
    WALL2 = cls.MapObject((24, 152), v.BLUE, (612, 688), (g.walls, g.world_objects, g.proj_collidables))
    WALL3 = cls.MapObject((24, 152), v.BLUE, (788, 688), (g.walls, g.world_objects, g.proj_collidables))
    FLR2 = cls.MapObject((200, 24), v.RED, (700, 600), (g.floors, g.world_objects, g.proj_collidables))
    #Thing 3 maybe this time
    CLN3 = cls.MapObject((200, 24), v.CYAN, (1220, 776), (g.ceilings, g.world_objects, g.proj_collidables))
    WALL4 = cls.MapObject((24, 152), v.BLUE, (1308, 688), (g.walls, g.world_objects, g.proj_collidables))
    WALL5 = cls.MapObject((24, 152), v.BLUE, (1132, 688), (g.walls, g.world_objects, g.proj_collidables))
    FLR3 = cls.MapObject((200, 24), v.RED, (1220, 600), (g.platforms, g.world_objects, g.proj_collidables))

    #Enemies WOOO
    NME1 = cls.Enemy((1220, 500))
    #NME1COL = cls.Collision_Shadow(NME1)

    #NME2 = cls.Enemy((700, 500))
    #NME2COL = cls.Collision_Shadow(NME2)

    #Player and collision shadow
    P1 = cls.Player()
    
    
    

    #Initial level gen
    for x in range(random.randint(5, 6)):
        pl = cls.MapObject((random.randint(100, 200), 24), v.GREEN, (random.randint(0 ,v.WIDTH-200), (random.randint(300 , v.HEIGHT-300))), (g.platforms, g.world_objects))

    #Debug thingy
    CENTER = cls.MapObject((30, 30), v.MAGENTA, (v.WIDTH/2, v.HEIGHT-148), (g.debug, g.world_objects, g.map_center))
    SCREENFOCUS = cls.MapObject((30, 30), v.PURPLE, (v.WIDTH/2, v.HEIGHT/2), (g.debug, g.focus))
    SCREENFOCUS.target = P1
    SCROLL_BOTTOM = cls.MapObject((30, 30), v.CYAN, (v.WIDTH/2, v.HEIGHT-300), (g.debug, g.world_objects, g.bottom_scroll_limits))
    SCROLL_TOP = cls.MapObject((30, 30), v.CYAN, (v.WIDTH/2, -300), (g.debug, g.world_objects, g.top_scroll_limits))
    SCROLL_LEFT = cls.MapObject((30, 30), v.CYAN, (-v.WIDTH+700, v.HEIGHT/2), (g.debug, g.world_objects, g.left_scroll_limits))
    SCROLL_RIGHT = cls.MapObject((30, 30), v.CYAN, (v.WIDTH*2-700, v.HEIGHT/2), (g.debug, g.world_objects, g.right_scroll_limits))
