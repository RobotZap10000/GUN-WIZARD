#importing CHANGE CHANGE
import pygame
from pygame.locals import *

#pygame.init()

#Sprite groups

#Drawing group
all_sprites = pygame.sprite.Group() 

#Drawing check
draw_checks = pygame.sprite.Group()

#Collision groups
platforms = pygame.sprite.Group()
players = pygame.sprite.Group()
floors = pygame.sprite.Group()
walls = pygame.sprite.Group()
ceilings = pygame.sprite.Group()
triggers = pygame.sprite.Group()
props = pygame.sprite.Group()

#Projectile groups
projectiles = pygame.sprite.Group()
proj_collidables = pygame.sprite.Group()

#Explosion groups
explosions = pygame.sprite.Group()

#Enemy groups
enemies = pygame.sprite.Group()
boss_limbs = pygame.sprite.Group()

#Knockback groups
knockback = pygame.sprite.Group()

#Screen scrolling group
world_objects = pygame.sprite.Group()
#world_beings = pygame.sprite.Group()

#Debug group
debug = pygame.sprite.Group()
focus = pygame.sprite.Group()
map_center = pygame.sprite.Group()
collisions = pygame.sprite.Group()
left_scroll_limits = pygame.sprite.Group()
right_scroll_limits = pygame.sprite.Group()
top_scroll_limits = pygame.sprite.Group()
bottom_scroll_limits = pygame.sprite.Group()

#Button groups
lvl_select_buttons = []
pause_menu_buttons = []
death_menu_buttons = []

#HUD groups
HUD = pygame.sprite.Group()

#Dark screen(?)
screens = pygame.sprite.Group()

#Map texts
map_texts = []
