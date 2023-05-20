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


#Starting map
def StartMap():

    #New method of classes cls.MapObject(size, color, originxy, group)
    #ADD IN DRAW ORDER FROM BACKGROUND TO FOREGROUND
    #Bottom floor
    PT1 = cls.MapObject((v.WIDTH*3, 150), v.RED, (v.WIDTH/2, v.HEIGHT-75), (g.floors, g.world_objects, g.proj_collidables))

    #Enemies WOOO
    NME1 = cls.Enemy((1220, 500))

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

    TRG1 = cls.MapObject((20, 20), v.ORANGE, (500, 500), (g.world_objects, g.debug, g.triggers))
    TRG1.function = func.Victory
    TRG1.surf.set_alpha(128)

    if v.DEBUG:
        for debug in g.debug:
            g.all_sprites.add(debug)

    DRAWCHECK = cls.MapObject((v.WIDTH, v.HEIGHT), v.BLACK, (v.WIDTH/2, v.HEIGHT/2) , (g.draw_checks, g.draw_checks))