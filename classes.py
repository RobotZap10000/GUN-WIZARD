#importing CHANGE CHANGE
import pygame, sys
from pygame.locals import *
import random, time
import variables as v
import groups as g
import functions as func
import texts as txt
from math import atan2, degrees
import random

#initializing
pygame.init()
vec = pygame.math.Vector2 #2 = 2D
vec3 = pygame.math.Vector3

#game window
displaysurface = pygame.display.set_mode((v.WIDTH, v.HEIGHT))
        
#Get angle
def GetAngle(startx, starty, endx, endy): #start, end
    #Getting angle
    dx = startx - endx
    dy = starty - endy
    rads = atan2(dy, dx)
    degs = round(degrees(rads))

    #Apply angle
    return degs + 90 #AND SO STARTS THE SPAGHETTI CODE

#HUD element
class HUD(pygame.sprite.Sprite):
    def __init__(self, target, size, color, originxy, unit, margin=20):
        super().__init__()
        self.target = target
        self.target.huds.append(self)
        self.size = vec(size)
        self.surf = pygame.Surface(self.size)
        self.color = color
        self.surf.fill(color)
        self.originxy = originxy
        self.rect = self.surf.get_rect(topleft = originxy)
        self.unit = unit
        self.text = None
        self.symbol = None
        self.background = None
        g.all_sprites.add(self)
        g.HUD.add(self)

        self.bg_margin = margin
        self.bg_width = round(self.size[0] + self.bg_margin)
        self.bg_height = round(self.size[1] + self.bg_margin)
        self.background = pygame.Surface((self.bg_width, self.bg_height))
        self.background.fill((20, 20, 20))
        self.background_rect = self.background.get_rect(topleft = (self.originxy[0] - self.bg_margin /2, self.originxy[1] - self.bg_margin/2))

    def build_background(self, margin):
        # self.bg_margin = margin
        # self.bg_width = round(self.size[0] + self.bg_margin)
        # self.bg_height = round(self.size[1] + self.bg_margin)
        # self.background = pygame.Surface((self.bg_width, self.bg_height))
        # self.background.fill((20, 20, 20))
        # self.background_rect = self.background.get_rect(topleft = (self.originxy[0] - self.bg_margin /2, self.originxy[1] - self.bg_margin/2))
        pass

    def update(self):
        if self.unit == "player_health":
            #CHANGE BAR LENGTH
            if not v.DEAD:
                self.surf = pygame.Surface((self.size[0]*(self.target.health / self.target.maxhealth), self.size[1]))
            else:
                self.surf = pygame.Surface((0, self.size[1]))
            self.surf.fill(self.color)
            self.rect = self.surf.get_rect(topleft = self.originxy)
            self.symbol = txt.Text(txt.font_icon, "✚ ", v.WHITE, (0, 0))
            self.symbol.rect.midleft = (self.originxy[0] + 25, self.originxy[1] + self.size[1]/2)
            self.text = txt.Text(txt.font_lvlselect, str(self.target.health), v.WHITE, (0, 0))
            self.text.rect.midleft = self.symbol.rect.midright
           # self.build_background(20)

        if self.unit == "player_mana":
            #CHANGE BAR LENGTH
            if self.target.buff != None:
                self.target.mana = 100
                self.color = v.MAGENTA
                self.text = txt.Text(txt.font_icon, "∞", v.WHITE, (0, 0))
            else:
                self.text = txt.Text(txt.font_lvlselect, str(round(self.target.mana)), v.WHITE, (0, 0))
            if not v.DEAD:
                self.surf = pygame.Surface((self.size[0]*(self.target.mana / 100), self.size[1]))
            self.surf.fill(self.color)
            self.rect = self.surf.get_rect(topleft = self.originxy)
            self.symbol = txt.Text(txt.font_icon, "★ ", v.WHITE, (0, 0))
            self.symbol.rect.midleft = (self.originxy[0] + 25, self.originxy[1] + self.size[1]/2)
            # self.text = txt.Text(txt.font_lvlselect, str(round(self.target.mana)), v.WHITE, (0, 0))
            self.text.rect.midleft = self.symbol.rect.midright
            #self.build_background(20)
            #RENDER TEXT
            #BLIT TEXT ONTO SURF
        
        if self.unit == "player_weapon":
            if self.target.weapon == 1:
                if self.target.buff == "manaboost":
                    self.color = v.PURPLE
                else:
                    self.color = v.GREEN
                self.text = txt.Text(txt.font_lvlselect, "MAGIC", v.BLACK, self.rect.center)
            elif self.target.weapon == 2:
                if self.target.buff == "manaboost":
                    self.color = v.BLUE
                else:
                    self.color = v.RED
                self.text = txt.Text(txt.font_lvlselect, "FLAME", v.BLACK, self.rect.center)
            elif self.target.weapon == 3:
                if self.target.buff == "manaboost":
                    self.color = v.ORANGE
                else:
                    self.color = v.YELLOW
                self.text = txt.Text(txt.font_lvlselect, "BOMB", v.BLACK, self.rect.center)
            else:
                self.color = v.MAGENTA
                self.text = txt.Text(txt.font_lvlselect, "???", v.BLACK, self.rect.center)
            self.surf.fill(self.color)
            
            if self.target.firedelay > 0:
                self.surf.set_alpha(128)
            else:
                self.surf.set_alpha(255)

        if self.unit == "boss_health":
            self.totalhealth = self.target.health
            self.totalhealth += sum(limb.health for limb in g.boss_limbs)
            #CHANGE BAR LENGTH
            if self.totalhealth > 0:
                self.surf = pygame.Surface((self.size[0]*(self.totalhealth / 4000), self.size[1]))
            else:
                self.surf = pygame.Surface((0, self.size[1]))
                self.target.health = 0
            self.surf.fill(self.color)
            self.rect = self.surf.get_rect(topleft = self.originxy)
            self.symbol = txt.Text(txt.font_icon, "☠ ", v.WHITE, (0, 0))
            # self.symbol.rect.midleft = (self.originxy[0] + 25, self.originxy[1] + self.size[1]/2)
            # self.text = txt.Text(txt.font_lvlselect, str(self.totalhealth), v.WHITE, (0, 0))
            self.text = txt.Text(txt.font_lvlselect, "BOSS", v.WHITE, (0, 0))
            self.text.rect.center = self.background_rect.center
            self.symbol.rect.midright = self.text.rect.midleft
            # self.text.rect.midleft = self.symbol.rect.midright
        
        self.build_background(20)

            



#Player
class Player(pygame.sprite.Sprite):
    def __init__(self, size=(v.PLAYERWIDTH, v.PLAYERHEIGHT), spawn=(v.WIDTH/2,v.HEIGHT-150), speed=v.ACC, color=v.YELLOW, jumpvel=v.JUMPVEL, gravity=v.GRAVITY, team="players", health=100, vic_cond=None, buff=None):
        super().__init__()
        self.size = size
        self.surf = pygame.Surface(self.size)
        self.surf.fill(color)
        self.alpha = 255
        self.rect = self.surf.get_rect(midbottom = spawn)
        self.speed = speed
        self.jumpvel = jumpvel
        self.gravity = gravity
        self.jumping = False
        self.dropping = False
        self.jumpprompt = False
        self.standing = True
        self.wall = False
        self.ceiling = False
        self.firerate = 0 #What is this used for?
        self.firedelay = 0 #In ticks
        self.aim = 0
        self.weapon = 1
        self.knockback = True
        self.iframes = 50
        self.immunity = 0
        self.stun = 0
        self.team = team
        self.maxhealth = health
        self.health = self.maxhealth
        self.mana = 100
        self.manawait = 240
        self.lastfired = self.manawait
        self.vic_cond = vic_cond
        self.buff = buff
        self.huds = []
        self.regen_cycle_len = 12
        self.regen_cycle = self.regen_cycle_len
        g.players.add(self)
        g.all_sprites.add(self)
        g.world_objects.add(self)
        g.knockback.add(self)
        HUDHEALTH = HUD(self, (300, 80), v.RED, (50, v.HEIGHT - 130), "player_health")
        HUDMANA = HUD(self, (300, 80), v.BLUE, (50, v.HEIGHT-260), "player_mana")
        HUDWEAPON = HUD(self, (200, 100), v.YELLOW, (50, v.HEIGHT-410), "player_weapon")

        #Player physics
        self.pos = vec(self.rect.midbottom)
        self.vel = vec(0,0)
        self.kb_vel = vec(0,0)
        self.kb_rot = 0
        self.acc = vec(0,0)

        #Fix scrolling issue? IF ONLY
        self.lastpos = vec((v.WIDTH/2,v.HEIGHT-150))
        self.currentpos = vec((v.WIDTH/2,v.HEIGHT-150))
        self.truevel = vec(0, 0)
        self.offset = vec(0, 0)

        #Player collision shadow
        PLAYERCOLLISION = Collision_Shadow(self)

    #Player movement
    def move(self):
        self.acc = vec(0, self.gravity)

        if self.stun <= 0:
            self.pressed_keys = pygame.key.get_pressed()

            if v.CONTROLS:
                if self.pressed_keys[K_a]: #OPTIMISE
                    self.acc.x = -self.speed
                if self.pressed_keys[K_d]:
                    self.acc.x = self.speed

            self.acc.x += self.vel.x * v.FRIC
        self.vel += self.acc 
        self.pos += round(self.vel) #+ 0.5 * self.acc)

        if self.vel.x > -0.1 and self.vel.x < 0.1:
            self.vel.x = 0

        self.rect.midbottom = self.pos
        self.currentpos = vec(self.pos)
        self.truevel = vec(self.currentpos - self.lastpos)

        #self.kb_vel / 1.02

    #Player collision
    def update(self):

        self.immunity -= 1
        self.immunity = max(self.immunity, 0)

        self.stun -= 1
        self.stun = max(self.stun, 0)

        self.lastfired += 1
        self.lastfired = min(self.lastfired, self.manawait)

            
        self.mana += (self.lastfired / self.manawait)
        self.mana = round(self.mana, 1)
        self.mana = min(max(self.mana, 0), 100)

        self.lastpos = vec(self.pos)

        if self.firedelay > 0:
            self.firedelay -= 1

        #Self damage

        #Explosions
        if self.immunity == 0:
            self.hitsexp = pygame.sprite.spritecollide(self.collision, g.explosions, False)
            if self.hitsexp:
                if self not in self.hitsexp[0].affected:
                    if self.hitsexp[0].dmg != 0:
                        #RESET KB VEC ROT
                        self.kb_vel = self.kb_vel.rotate(self.kb_rot * -1)
                        self.kb_angle = GetAngle(self.hitsexp[0].pos.x, self.hitsexp[0].pos.y, self.pos.x, self.pos.y - self.size[1]/2)
                        self.kb_rot = self.kb_angle
                        self.kb_vel = vec(0, self.hitsexp[0].kb[0])
                        self.kb_vel = self.kb_vel.rotate(self.kb_rot)
                        self.vel += self.kb_vel
                        self.hitsexp[0].affected.append(self)
                        self.health -= self.hitsexp[0].dmg
                        self.health = round(self.health)
                        
                        self.immunity = self.iframes
                        self.stun = self.hitsexp[0].kb[1]
                        self.collision.move()
        
        #Enemy melee
        
        if self.immunity == 0:
            self.hitsenemy = pygame.sprite.spritecollide(self.collision, g.enemies, False)
            if self.hitsenemy:
                if self.hitsenemy[0].kb[0] > 0:
                    #RESET KB VEC ROT
                    self.kb_vel = self.kb_vel.rotate(self.kb_rot * -1)
                    self.kb_angle = GetAngle(self.hitsenemy[0].pos.x, self.hitsenemy[0].pos.y - self.hitsenemy[0].size[1]/2, self.pos.x, self.pos.y - self.size[1]/2)
                    self.kb_rot = self.kb_angle
                    self.kb_vel = vec(0, self.hitsenemy[0].kb[0])
                    self.kb_vel = self.kb_vel.rotate(self.kb_rot)
                    self.vel = vec(0, 0)
                    if self.hitsenemy[0].kb[2]:
                        if self.hitsenemy[0].stun <= 0:
                            self.vel += self.hitsenemy[0].vel
                    self.vel += self.kb_vel
                    self.stun = self.hitsenemy[0].kb[1]
                    self.collision.move()

                if self.hitsenemy[0].melee_dmg > 0:
                    self.health -= self.hitsenemy[0].melee_dmg
                    self.health = round(self.health)
                    self.immunity = self.iframes

                elif self.hitsenemy[0].melee_dmg < 0:
                    self.health -= self.hitsenemy[0].melee_dmg
                    self.health = min(self.health, 100)
                    self.hitsenemy[0].collision.kill()
                    self.hitsenemy[0].kill()

                else:
                    self.immunity = 10

        #Enemy projectiles
        if self.immunity == 0:
            self.hitsproj = pygame.sprite.spritecollide(self, g.projectiles, False)
            if self.hitsproj:
                if self.hitsproj[0].team != self.team:
                    #RESET KB VEC ROT
                    self.kb_vel = self.kb_vel.rotate(self.kb_rot * -1)
                    self.kb_angle = GetAngle(self.hitsproj[0].pos.x, self.hitsproj[0].pos.y, self.pos.x, self.pos.y - self.size[1]/2)
                    self.kb_rot = self.kb_angle
                    self.kb_vel = vec(0, self.hitsproj[0].kb[0])
                    self.kb_vel = self.kb_vel.rotate(self.kb_rot)
                    self.vel += self.kb_vel
                    self.health -= self.hitsproj[0].dmg
                    self.health = round(self.health)
                    
                    self.immunity = self.iframes
                    self.stun = self.hitsproj[0].kb[1]
                    self.collision.move()

                    if not self.hitsproj[0].flame:
                        if self.hitsproj[0].explosive:
                            EXPLSN = Explosion(self.hitsproj[0], self.hitsproj[0].explosive[0], self.hitsproj[0].explosive[1], self.hitsproj[0].explosive[2], self.hitsproj[0].explosive[3], self.hitsproj[0].explosive[4],self.hitsproj[0].explosive[5],) #(self, target, size=50, maxsize=150, life=30, dmg=20, kb=40, stun=30)
                        self.hitsproj[0].kill()


        #Transparency
        if self.immunity > 0:
            if self.alpha != 128:
                self.alpha = 128
                self.surf.set_alpha(self.alpha)
        else:
            if self.alpha != 255:
                self.alpha = 255
                self.surf.set_alpha(self.alpha)
            
                
        
        #if TICK > 0:
            
        self.rect = self.surf.get_rect()
        self.hitsplatform = pygame.sprite.spritecollide(self.collision, g.platforms, False)
        self.hitsfloor = pygame.sprite.spritecollide(self.collision, g.floors, False)
        self.hitswall = pygame.sprite.spritecollide(self.collision, g.walls, False)
        self.hitsceiling = pygame.sprite.spritecollide(self.collision, g.ceilings, False)
        self.hitstrg = pygame.sprite.spritecollide(self.collision, g.triggers, False)

        #numba = 0 i hate this so much
        self.standing = False
        self.wall = False
        self.ceiling = False
        
        if self.hitsplatform:
            if not self.dropping:
                if self.vel.y > 0:
                    if self.pos.y < self.hitsplatform[0].rect.bottom:
                        self.pos.y = self.hitsplatform[0].rect.top + 1 #Using hits[0] checks the first collision in the list that’s returned.
                        self.vel.y = 0
                        self.kb_vel.y = 0
                        self.jumping = False
                        self.standing = True
                        self.collision.move()

        if self.hitsfloor:
            if self.vel.y > 0:
                if self.pos.y < self.hitsfloor[0].rect.bottom:
                    self.pos.y = self.hitsfloor[0].rect.top + 1#Using hits[0] checks the first collision in the list that’s returned.
                    self.vel.y = 0
                    self.kb_vel.y = 0
                    self.jumping = False
                    self.standing = True
                    self.collision.move()

        

        if self.hitswall:
            #if hitsceiling:
            #    if hitswall[0].rect.bottom == hitsceiling[0].rect.top:
            #        if self.rect.top < hitsceiling[0].rect.top:
            #            numba += 1
            if self.hitsceiling:
                if self.hitswall[0].rect.bottom <= self.hitsceiling[0].rect.top:
                    if self.vel.y > 0:
        
                        if self.vel.x >= 0:
                            if self.pos.x < self.hitswall[0].rect.right:
                                self.pos.x = self.hitswall[0].rect.left - (self.size[0] / 2)
                                self.vel.x = 0
                                self.kb_vel.x = 0
                                self.wall = True
                                self.collision.move()
                        if self.vel.x < 0:
                            if self.pos.x > self.hitswall[0].rect.left:
                                self.pos.x = self.hitswall[0].rect.right + (self.size[0] / 2)
                                self.vel.x = 0
                                self.kb_vel.x = 0
                                self.wall = True
                                self.collision.move()
            else:
                if self.vel.x >= 0:
                    if self.pos.x < self.hitswall[0].rect.right:
                        self.pos.x = self.hitswall[0].rect.left - (self.size[0] / 2)
                        self.vel.x = 0
                        self.kb_vel.x = 0
                        self.wall = True
                        self.collision.move()
                if self.vel.x < 0:
                    if self.pos.x > self.hitswall[0].rect.left:
                        self.pos.x = self.hitswall[0].rect.right + (self.size[0] / 2)
                        self.vel.x = 0
                        self.kb_vel.x = 0
                        self.wall = True
                        self.collision.move()

        if self.hitsceiling:
            if self.vel.y < 0:
                self.pos.y = self.hitsceiling[0].rect.bottom + self.size[1]
                self.vel.y = 0
                self.kb_vel.y = 0
                self.ceiling = True
                self.collision.move()

        if self.hitstrg:
            if self.hitstrg[0].function_param != None:
                self.hitstrg[0].function(self.hitstrg[0].function_param)
            else:
                self.hitstrg[0].function()
            self.hitstrg[0].kill()
        

        #Autojumping
        if self.jumpprompt == True:
            #if v.CONTROLS:
            self.jump()
            # self.jumpprompt = False

        

        #Death
        if self.health <= 0:
            self.health = 0
            self.collision.kill()
            self.kill()
            v.DEAD = True
        else:
            if self.buff != None:
                if self.regen_cycle > 0:
                    self.regen_cycle -= 1
                else:
                    self.health += 1
                    self.health = min(self.health, self.maxhealth)
                    self.regen_cycle = self.regen_cycle_len


    #Player jumping
    def jump(self):
        #if TICK > 0:
        if self.hitsplatform and not self.jumping:
            if self.rect.bottom < self.hitsplatform[0].rect.top:
                self.jumping = True
                self.vel.y = self.jumpvel

        if self.hitsfloor: #Fun bug, maybe use later?
            if self.rect.bottom < self.hitsfloor[0].rect.top:
                self.jumping = True
                self.vel.y = self.jumpvel

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def shoot(self):
        if self.firedelay == 0:

            #Getting mouse position
            mousePos = vec(pygame.mouse.get_pos())
            
            #Apply player aim
            self.aim = GetAngle(self.rect.centerx, self.rect.centery, mousePos.x, mousePos.y)

            #Fire!
            #(self, size, color, acc, graviwty, rot, vel, maxvel, inherit, life, shooter, firerate, knockback, flame)
        
            if self.weapon == 1:
                if self.buff == "manaboost":
                    PLAYERMAGIC = Projectile((50, 50), v.PURPLE, None, None, self.aim, (0, 40), None, None, 180, self, 8, (2, 10), cost=0, dmg=6)
                    self.lastfired = 0

                elif self.mana >= 6: 
                    PLAYERMAGIC = Projectile((50, 50), v.GREEN, None, None, self.aim, (0, 30), None, None, 180, self, 12, (2, 10), cost=6, dmg=6)
                    self.lastfired = 0

            if self.weapon == 2:
                if self.buff == "manaboost":
                    PLAYERFLAME = Projectile((30, 30), v.BLUE, None, (0, -0.1), self.aim, (0, 20), None, (self.vel.x*1.5, self.vel.y), 30, self, 3, (0, 0), cost=0, dmg=10, flame=True)
                    PLAYERFLAME = Projectile((30, 30), v.BLUE, None, (0, -0.1), self.aim + 20, (0, 20), None, (self.vel.x*1.5, self.vel.y), 30, self, 3, (0, 0), cost=0, dmg=10, flame=True)
                    PLAYERFLAME = Projectile((30, 30), v.BLUE, None, (0, -0.1), self.aim - 20, (0, 20), None, (self.vel.x*1.5, self.vel.y), 30, self, 3, (0, 0), cost=0, dmg=10, flame=True)
                    self.lastfired = 0
                elif self.mana >= 0.6:
                    PLAYERFLAME = Projectile((30, 30), v.RED, None, (0, -0.1), self.aim + (random.randint(-4, 4)), (0, 10), None, (self.vel.x*1.5, self.vel.y), 30, self, 3, (0, 0), cost=3, dmg=6, flame=True)
                    self.lastfired = 0

            if self.weapon == 3:
                if self.buff == "manaboost":
                    PLAYERBOMB = Projectile((80, 80), v.ORANGE, None, (0, 1), self.aim, (0, 20), None, self.vel, 30, self, 60, (5, 0), cost=0, dmg=10, explosive=(100, 400, 60, 20, 40, 30)) #(self, target, size=50, maxsize=150, life=30, dmg=20, kb=40, stun=30)
                    self.lastfired = 0

                elif self.mana >= 40:
                    PLAYERBOMB = Projectile((50, 50), v.YELLOW, None, (0, 1), self.aim, (0, 20), None, self.vel, 120, self, 20, (5, 0), cost=40, dmg=10, explosive=(50, 150, 30, 20, 40, 30)) #(self, target, size=50, maxsize=150, life=30, dmg=20, kb=40, stun=30)
                    self.lastfired = 0

    def spawnboss(self):
        for center in g.map_center:
            boss_spawn = vec(center.rect.center) - (0, 225)
        BOSS = Boss(boss_spawn)
                
    
#Player collision shadow:
class Collision_Shadow(pygame.sprite.Sprite):
    def __init__(self, target):
        super().__init__()
        self.target = target
        self.surf = pygame.Surface(self.target.size)
        self.rect = self.surf.get_rect()
        self.surf.fill(v.ORANGE)
        self.rect.midtop = vec(self.target.rect.midtop)
        self.target.collision = self
        g.debug.add(self)
        #g.all_sprites.add(self)
        g.collisions.add(self)
        g.world_objects.add(self)

    def move(self):
        self.surf = pygame.Surface(((self.target.size[0]+abs(self.target.vel.x)),(self.target.size[1]+abs(self.target.vel.y))))
        self.rect = self.surf.get_rect()
                
        if self.target.vel.y >= 0: 
            if self.target.vel.x >= 0:
                self.rect.topleft = vec(((self.target.pos.x-(self.target.size[0] / 2)), (self.target.pos.y-self.target.size[1])))
            if self.target.vel.x < 0:
                self.rect.topright = vec(((self.target.pos.x+(self.target.size[0] / 2)), (self.target.pos.y-self.target.size[1])))

        if self.target.vel.y < 0:
            if self.target.vel.x >= 0:
                self.rect.bottomleft = vec(((self.target.pos.x-(self.target.size[0] / 2)), (self.target.pos.y)))
            if self.target.vel.x < 0:
                self.rect.bottomright = vec(((self.target.pos.x+(self.target.size[0] / 2)), (self.target.pos.y)))
            
        self.surf.fill(v.ORANGE)

    def update(self):
        pass

#Basic enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, originxy, size=(70,120), color=v.MAGENTA, speed=v.ACC*0.8, jumpvel=v.JUMPVEL*0.9, gravity=v.GRAVITY, health=60, ai=0, aggro=1000, deaggro=2000, dmg_mel=20, kb=(10, 20, True), team="enemy", flag="count_death", kb_immune=False, world_collide=True, cycle_len=240, tag=None, buff=None):
        super().__init__()
        self.size = size
        self.color = color
        self.surf = pygame.Surface(self.size)
        self.surf.fill(self.color)
        self.spawn = originxy
        self.rect = self.surf.get_rect(midbottom = self.spawn)
        self.speed = speed
        self.jumpvel = jumpvel
        self.gravity = gravity
        self.kb = kb
        self.iframes = 1
        self.proj_immunity = 0
        self.exp_immunity = 0
        self.stun = 0
        self.team = team
        self.cycle_len = cycle_len
        self.cycle = self.cycle_len
        self.aggrostate = False
        self.aggro = aggro
        self.deaggro = deaggro
        self.aggrolen = 30
        self.aggroleft = self.aggrolen
        self.maxhealth = health
        self.health = self.maxhealth
        self.melee_dmg = dmg_mel
        self.ai = ai
        self.flag = flag
        self.kb_immune = kb_immune
        self.world_collide = world_collide
        self.limbs = pygame.sprite.Group()
        self.huds = []
        self.target = None
        self.tag = tag
        self.buff = buff
        g.all_sprites.add(self)
        g.world_objects.add(self)
        g.enemies.add(self)
        g.knockback.add(self)

        #Enemy collision shadow
        NMECOL = Collision_Shadow(self)

        #Enemy physics
        self.pos = vec(originxy)
        self.vel = vec(0,0)
        self.kb_vel = vec(0, 0)
        self.kb_rot = 0
        self.acc = vec(0,0)

        self.jumping = False
        self.dropping = False
        self.jumpprompt = False

        #Enemy movement
    def move(self):
        self.acc = vec(0, self.gravity)

        self.dropping = False

        
        if self.stun <= 0:
            self.pressed_keys = pygame.key.get_pressed()
            
            if v.BRAIN:
                if self.ai == 0:
                    if self.aggrostate:
                        if self.cycle > 90:
                            for player in g.players:
                                if self.pos.x > player.pos.x: #OPTIMISE
                                    self.acc.x = -self.speed
                                else:
                                    self.acc.x = self.speed

                                if self.jumpvel != 0:
                                    if self.pos.y > player.pos.y:
                                        #CHECK IF ENEMY CAN REACH PLAYER WITH JUMP, THEN:
                                        if abs(player.pos.x - self.pos.x) < (abs(self.jumpvel) / self.gravity * (v.ACC*0.8) * 10):
                                            self.jump()
                                    else:
                                        self.cancel_jump()
                                        self.dropping = True

            if self.pressed_keys[K_g]: #OPTIMISE
                self.acc.x = -self.speed
            if self.pressed_keys[K_j]:
                self.acc.x = self.speed

            self.acc.x += self.vel.x * v.FRIC
            
        self.vel += self.acc
        self.pos += round(self.vel) #+ 0.5 * self.acc)

        if self.vel.x > -0.1 and self.vel.x < 0.1:
            self.vel.x = 0

        self.rect.midbottom = self.pos
        self.currentpos = vec(self.pos)
        
    #Enemy aggro and firing intervals
    def brain(self):
        for player in g.players:
            if v.BRAIN:
                if self.aggroleft > 0:
                    self.aggroleft -= 1
                else:
                    self.aggroleft = self.aggrolen

                self.playerdiff = vec(self.pos - player.pos)
                if self.deaggro != 0:
                    if not self.aggrostate:
                        if abs(self.playerdiff.length()) < self.aggro:
                            self.aggrostate = True
                            self.cycle = self.cycle_len
                    else:
                        if abs(self.playerdiff.length()) > self.deaggro:
                            self.aggrostate = False
                else:
                    self.aggrostate = True
                        
                if self.aggrostate:
                    if self.cycle > 0:
                        self.cycle -= 1
                    else:
                        self.cycle = self.cycle_len

                    if self.ai == 0:

                        if self.cycle == 30:
                            #Apply player aim
                            self.aim = GetAngle(self.pos.x, self.pos.y, player.pos.x, player.pos.y)
                            self.shoot()

                        if self.cycle == 50:
                            #Apply player aim
                            self.aim = GetAngle(self.pos.x, self.pos.y, player.pos.x, player.pos.y)
                            self.shoot()

                        if self.cycle == 70:
                            #Apply player aim
                            self.aim = GetAngle(self.pos.x, self.pos.y, player.pos.x, player.pos.y)
                            self.shoot()

                    if self.ai == 1:
                        if self.cycle > 120:
                            self.aim = GetAngle(self.pos.x, self.pos.y, player.pos.x, player.pos.y)
                            self.shoot()

                    
    #Fire!              
    def shoot(self):
        NMEMAGIC = Projectile((50, 50), v.PURPLE, (0, 1), None, self.aim, (0, 10), 30, None, 180, self, 0, (10, 10),dmg=15, noclip=True)

        
    #Enemy collision
    def update(self):

        
            
        if self.health <= 0:
            if self.tag == "BOSS":
                if not v.CUTSCENE:
                    self.health = 0
                    func.Cutscene(1)

            else:
                self.health = 0
                for player in g.players:
                    healthdrop = False

                    if self not in g.boss_limbs:
                        if player.health < 100:
                            rng = random.randint(0, 1)
                            if rng == 0: 
                                healthdrop = True
                        if player.health <= 50:
                            healthdrop = True
                    else:
                        healthdrop = True
                    
                    if healthdrop:
                        HEALTHPACK = Enemy(self.pos, size=(50, 50), color=v.HEALTHGREEN, health=999, ai=2, dmg_mel=-30, kb=(0, 0, False), flag="dont_count")
                self.collision.kill()
                if self.tag != None:
                    for limb in g.boss_limbs:
                        limb.collision.kill()
                        limb.kill()
                for hud in self.huds:
                    hud.kill()
                if self.target != None:
                    self.target.limbs.remove(self)
                self.kill()
                
                self.deathcounting = 0
                for entity in g.enemies:
                    if entity.flag == "count_death":
                        self.deathcounting += 1
                if self.deathcounting == 0:
                    for player in g.players:
                        if player.vic_cond == "NME_KILLED":
                            func.Victory()
            

        if self.proj_immunity > 0:
            self.proj_immunity -= 1

        if self.exp_immunity > 0:
            self.exp_immunity -= 1

        if self.stun > 0:
            self.stun -= 1

        

        #if TICK > 0:

        #Self damage
        if self.buff == None:
            #Explosions
            if self.exp_immunity == 0:
                self.hitsexp = pygame.sprite.spritecollide(self.collision, g.explosions, False)
                if self.hitsexp:
                    if self not in self.hitsexp[0].affected:
                        if self.hitsexp[0].kb[0] != 0:
                            if not self.kb_immune:
                            #RESET KB VEC ROT
                                self.kb_vel = self.kb_vel.rotate(self.kb_rot * -1)
                                self.kb_angle = GetAngle(self.hitsexp[0].pos.x, self.hitsexp[0].pos.y, self.pos.x, self.pos.y - self.size[1]/2)
                                self.kb_rot = self.kb_angle
                                self.kb_vel = vec(0, self.hitsexp[0].kb[0])
                                self.kb_vel = self.kb_vel.rotate(self.kb_rot)
                                self.vel += self.kb_vel
                                self.stun = self.hitsexp[0].kb[1]
                                self.collision.move()

                            self.health -= self.hitsexp[0].dmg
                            self.health = round(self.health)
                            self.exp_immunity = self.iframes
                            self.hitsexp[0].affected.append(self)
                            

            #Projectiles
            if self.proj_immunity == 0:
                self.hitsproj = pygame.sprite.spritecollide(self, g.projectiles, False)
                if self.hitsproj:
                    if self.hitsproj[0].team != self.team:
                        if self.hitsproj[0].flame and self not in self.hitsproj[0].affected or not self.hitsproj[0].flame:
                            if not self.kb_immune:
                                #RESET KB VEC ROT
                                self.kb_vel = self.kb_vel.rotate(self.kb_rot * -1)
                                self.kb_angle = GetAngle(self.hitsproj[0].pos.x, self.hitsproj[0].pos.y, self.pos.x, self.pos.y - self.size[1]/2)
                                self.kb_rot = self.kb_angle
                                self.kb_vel = vec(0, self.hitsproj[0].kb[0])
                                self.kb_vel = self.kb_vel.rotate(self.kb_rot)
                                self.vel += self.kb_vel
                                self.stun = self.hitsproj[0].kb[1]
                                self.collision.move()
                            
                            self.proj_immunity = self.iframes
                            self.health -= self.hitsproj[0].dmg
                            self.health = round(self.health)

                            if not self.hitsproj[0].flame:
                                if self.hitsproj[0].explosive:
                                    EXPLSN = Explosion(self.hitsproj[0], self.hitsproj[0].explosive[0], self.hitsproj[0].explosive[1], self.hitsproj[0].explosive[2], self.hitsproj[0].explosive[3], self.hitsproj[0].explosive[4],self.hitsproj[0].explosive[5],) #(self, target, size=50, maxsize=150, life=30, dmg=20, kb=40, stun=30) 
                                self.hitsproj[0].kill()
                            else:
                                self.hitsproj[0].affected.append(self)

        if self.world_collide:
            
            self.rect = self.surf.get_rect()
            self.hitsplatform = pygame.sprite.spritecollide(self.collision, g.platforms, False)
            self.hitsfloor = pygame.sprite.spritecollide(self.collision, g.floors, False)
            self.hitswall = pygame.sprite.spritecollide(self.collision, g.walls, False)
            self.hitsceiling = pygame.sprite.spritecollide(self.collision, g.ceilings, False)

            #numba = 0 i hate this so much
            self.standing = False
            self.wall = False
            self.ceiling = False
            
            if self.hitsplatform:
                if not self.dropping:
                    if self.vel.y > 0:
                        if self.pos.y < self.hitsplatform[0].rect.bottom:
                            self.pos.y = self.hitsplatform[0].rect.top + 1 #Using hits[0] checks the first collision in the list that’s returned.
                            self.vel.y = 0
                            self.kb_vel.y = 0
                            self.jumping = False
                            self.standing = True
                            self.collision.move()

            if self.hitsfloor:
                if self.vel.y > 0:
                    self.pos.y = self.hitsfloor[0].rect.top + 1#Using hits[0] checks the first collision in the list that’s returned.
                    self.vel.y = 0
                    self.kb_vel.y = 0
                    self.jumping = False
                    self.standing = True
                    self.collision.move()

            if self.hitsceiling:
                if self.vel.y < 0:
                    self.pos.y = self.hitsceiling[0].rect.bottom + self.size[1]
                    self.vel.y = 0
                    self.kb_vel.y = 0
                    self.ceiling = True
                    self.collision.move()

            if self.hitswall:
                #if hitsceiling:
                #    if hitswall[0].rect.bottom == hitsceiling[0].rect.top:
                #        if self.rect.top < hitsceiling[0].rect.top:
                #            numba += 1
                if self.hitsceiling:
                    if self.hitswall[0].rect.bottom <= self.hitsceiling[0].rect.top:
                        if self.vel.y > 0:
            
                            if self.vel.x >= 0:
                                if self.pos.x < self.hitswall[0].rect.right:
                                    self.pos.x = self.hitswall[0].rect.left - (self.size[0] / 2)
                                    self.vel.x = 0
                                    self.kb_vel.x = 0
                                    self.wall = True
                                    self.collision.move()
                            if self.vel.x < 0:
                                if self.pos.x > self.hitswall[0].rect.left:
                                    self.pos.x = self.hitswall[0].rect.right + (self.size[0] / 2)
                                    self.vel.x = 0
                                    self.kb_vel.x = 0
                                    self.wall = True
                                    self.collision.move()
                else:
                    if self.vel.x >= 0:
                        if self.pos.x < self.hitswall[0].rect.right:
                            self.pos.x = self.hitswall[0].rect.left - (self.size[0] / 2)
                            self.vel.x = 0
                            self.kb_vel.x = 0
                            self.wall = True
                            self.collision.move()
                    if self.vel.x < 0:
                        if self.pos.x > self.hitswall[0].rect.left:
                            self.pos.x = self.hitswall[0].rect.right + (self.size[0] / 2)
                            self.vel.x = 0
                            self.kb_vel.x = 0
                            self.wall = True
                            self.collision.move()
            

        #Autojumping
        if self.jumpprompt == True:
            self.jump()

    #Enemy jumping
    def jump(self):
        if self.hitsplatform and not self.jumping:
            if self.rect.bottom < self.hitsplatform[0].rect.top:
                self.jumping = True
                self.vel.y = self.jumpvel

        if self.hitsfloor: #Fun bug, maybe use later?
            if self.rect.bottom < self.hitsfloor[0].rect.top:
                self.jumping = True
                self.vel.y = self.jumpvel

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

        #Firing delay
        #if self.firedelay > 0:
        #    self.firedelay -= 1

#Boss enemy TORSO
class Boss(Enemy):
    def __init__(self, originxy):
        Enemy.__init__(self, originxy, size=(500, 500), color=v.ORANGE, speed=0.5, jumpvel=0, gravity=0, health=1000, dmg_mel=5, kb=(20, 20, True), kb_immune=True, world_collide=False, deaggro=0, cycle_len=3000, tag="BOSS", buff="immune")
        BOSSARM_LEFT = Boss_Arm((0, 0), self, "left")
        BOSSARM_RIGHT = Boss_Arm((0, 0), self, "right")
        BOSSHEAD = Boss_Head((0,0), self)
        BOSSHEALTH_HUD = HUD(self, (1500, 70), v.RED, (240, 25), "boss_health")
        self.shake = vec(0, 0)
        self.aim = 0
        self.fric = -0.01
        self.cycle = 0

    def shoot(self):
        BOSSLASER = Projectile((50, 50), v.RED, None, None, self.aim, (0, 40), None, None, 60, self, 0, (10, 20), dmg=15, noclip=True)

    def brain(self):
        if self.health != 0:
            if v.BRAIN:
                if self.cycle < self.cycle_len:
                    self.cycle += 1
                else:
                    self.cycle = 0

    def aiming(self):
        for player in g.players:
            self.aim = GetAngle(self.rect.centerx, self.rect.centery, (player.pos.x + player.vel.x * 20), player.pos.y)

    def move(self):
        
        for player in g.players:
            for center in g.map_center:
                if v.BRAIN:
                    if self.health != 0:
                        if len(g.boss_limbs) != 0:
                            # FOLLOWING PLAYER
                            if self.cycle < 300:
                                if self.pos.x > player.pos.x: #OPTIMISE
                                    self.acc.x = -self.speed
                                    
                                else:
                                    self.acc.x = self.speed
                                # self.fric = -0.01

                            # RETURNING TO MAP CENTER
                            elif self.cycle < 600:
                                if self.pos.x - center.rect.centerx > 50:
                                    self.acc.x = -self.speed
                                elif self.pos.x - center.rect.centerx < -50:
                                    self.acc.x = self.speed
                                else:
                                    self.pos.x = center.rect.centerx
                                    self.vel.x = 0
                                    self.cycle = 600
                            
                            # MOVING AROUND
                            elif self.cycle < 690:
                                self.acc.x = -self.speed

                            elif self.cycle < 880:
                                self.acc.x = self.speed

                            elif self.cycle < 1050:
                                self.acc.x = -self.speed

                            elif self.cycle < 1350:
                                if self.pos.x > player.pos.x: #OPTIMISE
                                    self.acc.x = -self.speed
                                    
                                else:
                                    self.acc.x = self.speed


                            elif self.cycle < 1650:
                                if self.pos.x - center.rect.centerx > 50:
                                    self.acc.x = -self.speed
                                elif self.pos.x - center.rect.centerx < -50:
                                    self.acc.x = self.speed
                                else:
                                    self.pos.x = center.rect.centerx
                                    self.vel.x = 0
                                    self.cycle = 1650

                            elif self.cycle < 2010:
                                self.vel.x = 0

                            else:
                                self.cycle = 0

                        else:
                            if self.pos.x > player.pos.x: #OPTIMISE
                                self.acc.x = -self.speed
                                
                            else:
                                self.acc.x = self.speed

                            if self.cycle > 60:
                                self.cycle = 0

                            if self.cycle == 30:
                                self.aiming()
                                self.buff = None

                            if self.cycle > 30:
                                self.shoot()
                    else:
                        if v.CUTSCENE_TIME > 570:
                            self.shakevalue = 5
                        else:
                            self.shakevalue = 20
                            if v.CUTSCENE_TIME % 2 == 0:
                                BOSSEXPLOSION = Explosion(self, dmg=0, kb=0, stun=0, cutscene=True)
                        self.pos -= self.shake
                        self.shake = vec(random.randint(-self.shakevalue, self.shakevalue), random.randint(-self.shakevalue, self.shakevalue))
                        self.pos += self.shake
                        self.acc = vec(0, 0)
                        self.vel = vec(0, 0)



                self.acc.x += self.vel.x * self.fric
                
                self.vel += self.acc
                self.pos += round(self.vel) #+ 0.5 * self.acc)

                if self.vel.x > -0.1 and self.vel.x < 0.1:
                    self.vel.x = 0

                self.rect.midbottom = self.pos
                self.currentpos = vec(self.pos)

    def explode(self):
        FINALEXP = Explosion(self, size=500, maxsize=750, life=60, dmg=0, kb=0, stun=0, color=v.YELLOW)
        for f in g.focus:
            f.target = FINALEXP


#Boss enemy arm
class Boss_Arm(Enemy):
    def __init__(self, originxy, target, facing="left"):
        Enemy.__init__(self, originxy, world_collide=False, size=(70, 300), color=v.TITLEGREEN, gravity=0, jumpvel=0, health=1000, kb=(5, 30, False))
        self.target = target
        g.boss_limbs.add(self)
        self.facing = facing

    def move(self):
        if self.facing == "left":
            self.margin = (-500, 0)
        elif self.facing == "right":
            self.margin = (500, 0)
        else:
            self.margin = (0, 0)
        self.pos = self.target.pos + self.margin
        self.rect.midbottom  = self.pos

    def brain(self):
        if self.target.cycle < 600:
            pass

        elif self.target.cycle < 1050:
            if self.target.cycle % 15 == 0:
                self.shoot()

        elif self.target.cycle < 1650:
            pass

        elif self.target.cycle < 2010:
            if self.target.cycle % 30 == 0:
                    self.aiming("bottom")
                    self.shoot(1, "bottom")

                    self.aiming("top")
                    self.shoot(1, "top")

    def aiming(self, origin):
        self.origin = self.rect.centery

        if origin == "top":
            self.origin = self.pos.y - self.size[1]

        if origin == "bottom":
            self.origin = self.pos.y

        for player in g.players:
            self.aim = GetAngle(self.pos.x, self.origin, player.pos.x, player.pos.y)

        

    def shoot(self, type=None, origin=None):
    #     BOSSMAGIC = Projectile((50, 50), v.PURPLE, (0, 1), None, self.aim, (0, 10), 30, None, 180, self, 0, (10, 10),dmg=15, noclip=True, originxy=(self.rect.midbottom))
    #     BOSSMAGIC = Projectile((50, 50), v.PURPLE, (0, 1), None, self.aim+180, (0, 10), 30, None, 180, self, 0, (10, 10),dmg=15, noclip=True, originxy=(self.rect.midtop))
        if type == None:
            BOSSBOMB = Projectile((75, 75), v.YELLOW, None, (0, v.GRAVITY), 180, (0, 20), None, None, 180, self, 0, (10, 30), explosive=(50, 200, 30, 30, 50, 30), originxy=self.rect.midtop, dmg=30)
        else:
            if origin == None:
                BOSSMAGIC = Projectile((50, 50), v.PURPLE, None, None, self.aim, (0, 30), None, None, 180, self, 12, (2, 10), dmg=10)
            elif origin == "top":
                BOSSMAGIC = Projectile((50, 50), v.PURPLE, None, None, self.aim, (0, 30), None, None, 180, self, 12, (2, 10), dmg=10, originxy=self.rect.midtop)
            elif origin == "bottom":
                BOSSMAGIC = Projectile((50, 50), v.PURPLE, None, None, self.aim, (0, 30), None, None, 180, self, 12, (2, 10), dmg=10, originxy=self.rect.midbottom)


class Boss_Head(Enemy):
    def __init__(self, originxy, target):
        Enemy.__init__(self, originxy, world_collide=False, size=(100, 100), color=v.BLUE, gravity=0, jumpvel=0, speed=0, health=1000)
        self.target = target
        g.boss_limbs.add(self)

    def move(self):
        self.margin = (0, -self.target.size[1]-0)
        self.pos = self.target.pos + self.margin
        self.rect.midbottom = self.pos

    def brain(self):
        if not v.DEAD:
            if self.target.cycle < 120:
                pass

            elif self.target.cycle == 120:
                self.aiming()

            elif self.target.cycle < 150:
                self.shoot()

            elif self.target.cycle < 240:
                pass

            elif self.target.cycle == 240:
                self.aiming()

            elif self.target.cycle < 270:
                self.shoot()

            elif self.target.cycle < 1050:
                pass

            elif self.target.cycle < 1170:
                pass

            elif self.target.cycle == 1170:
                self.aiming()

            elif self.target.cycle < 1200:
                self.shoot()

            elif self.target.cycle < 1290:
                pass

            elif self.target.cycle == 1290:
                self.aiming()

            elif self.target.cycle < 1320:
                self.shoot()

            elif self.target.cycle < 1650:
                pass

            elif self.target.cycle < 2010:
                if self.target.cycle % 30 == 0:
                    self.aiming()
                    self.shoot(1)


    def shoot(self, type=None):
        if type == None:
            BOSSLASER = Projectile((50, 50), v.RED, None, None, self.aim, (0, 40), None, None, 60, self, 0, (10, 20), dmg=20, noclip=True)
        else:
            BOSSMAGIC = Projectile((50, 50), v.PURPLE, None, None, self.aim, (0, 30), None, None, 180, self, 12, (2, 10), dmg=10)

    def aiming(self):
        for player in g.players:
            self.aim = GetAngle(self.pos.x, self.pos.y, (player.pos.x + player.vel.x * 20), player.pos.y)

#Scrollable map objects
class MapObject(pygame.sprite.Sprite):
    def __init__(self, size, color, originxy, groups): #Use dictionaries?
        super().__init__()
        self.surf = pygame.Surface(size)
        self.surf.fill(color)
        self.rect = self.surf.get_rect(center = originxy)
        if g.debug not in groups:
            g.all_sprites.add(self)
        if g.draw_checks in groups:
            g.all_sprites.remove(self)
        for name in groups:
            name.add(self)
            
        
    def move(self):
        pass

    def update(self):
        pass

    #def ChangeTarget(self, newtarget):
    #    self.target = newtarget

#Scrollable map text
class MapText(pygame.sprite.Sprite):
    def __init__(self, size="inherit_from_text", color=v.RED, text=txt.text0, originxy=(1000, 200)):
        super().__init__()
        self.text = text
        if size != "inherit_from_text":
            self.size = size
        else:
            self.size = (self.text.width, self.text.height)
        self.surf = pygame.Surface(self.size)
        self.color = color
        self.surf.fill(self.color)
        self.rendertext = self.text.text
        self.textwidth = self.rendertext.get_width()
        self.textheight = self.rendertext.get_height()
        self.rect = self.surf.get_rect(center = originxy)
        self.surf.blit(self.rendertext, (self.size[0]/2 - self.textwidth/2, self.size[1]/2 - self.textheight/2))
        g.all_sprites.add(self)
        g.map_texts.append(self)

        
    def move(self):
        pass

    def update(self):
        pass
        
        

#Projectile class?
class Projectile(pygame.sprite.Sprite):
    def __init__(self, size, color, acc, gravity, rot, vel, maxvel, inherit, life, shooter, firerate, kb, cost=20 ,dmg=1, flame=False, explosive=False, noclip=False, originxy=None):
        super().__init__()
        self.size = vec(size)
        self.surf = pygame.Surface(self.size)
        self.color = vec3(color)
        self.surf.fill(color)
        if originxy == None:
            self.originxy = (shooter.pos.x, shooter.pos.y - shooter.size[1]/2)
        else:
            self.originxy = originxy
        self.rect = self.surf.get_rect(center = self.originxy)
        if acc != None:
            self.acc = vec(acc)
        else:
            self.acc = vec(0, 0)
        self.maxvel = maxvel
        self.vel = vec(vel)
        self.kb_vel = vec(0, 0)
        self.kb_rot = 0
        self.kb = kb
        self.initdmg = dmg
        self.dmg = self.initdmg
        self.pos = vec(self.rect.center)
        self.life = life
        self.lifeleft = life
        if inherit != None:
            self.inherit = vec(inherit)
        else:
            self.inherit = vec(0, 0)
        if gravity != None:
            self.gravity = vec(gravity)
        else:
            self.gravity = vec(0, 0)
        self.shooter = shooter
        self.team = self.shooter.team
        self.flame = flame
        if self.flame:
            self.affected = []
        self.explosive = explosive
        self.noclip = noclip
        self.rotation = rot #270 #Clockwise
        self.trueacc = self.acc.rotate(self.rotation)
        self.truevel = self.vel.rotate(self.rotation)
        if not self.flame:
            self.truevel += self.inherit
        else:
            if self.inherit.x != 0:
                if self.truevel.x / self.inherit.x > 0:
                    self.truevel.x += self.inherit.x

            if self.inherit.y != 0:
                if self.truevel.y / self.inherit.y > 0:
                    self.truevel.y += self.inherit.y
        
        g.all_sprites.add(self)
        g.world_objects.add(self)
        g.projectiles.add(self)
        if shooter in g.players:
            shooter.firedelay = firerate #Caused funny bug with old NME
            shooter.mana -= cost

    def move(self):
        #CAUSED FUN BUG self.trueacc += self.vel * self.fric
        if self.flame == True:
            self.FlameExpand()
        if self.maxvel != None:
            if abs(round(vec.length(self.truevel))) > self.maxvel:
                self.trueacc = vec(0, 0)
                self.gravity = vec(0, 0)
        self.truevel += self.trueacc + self.gravity
        self.pos += self.truevel
        self.rect.center = self.pos

    def collide(self):
        if not self.noclip:
            hitsobj = pygame.sprite.spritecollide(self, g.proj_collidables, False)
            
            if hitsobj:
                #Create explosion
                if self.explosive:
                    #(self, target, size=50, maxsize=150, life=30, dmg=20, kb=40, stun=30)
                    EXPLSN = Explosion(self, self.explosive[0], self.explosive[1], self.explosive[2], self.explosive[3], self.explosive[4],self.explosive[5],) #(self, target, size=50, maxsize=150, life=30, dmg=20, kb=40, stun=30)
                self.kill()

    def update(self):
        self.hitsexp = pygame.sprite.spritecollide(self, g.explosions, False)
        if self.hitsexp:
            if self.hitsexp[0].kb[0] != 0:
                #RESET KB VEC ROT
                self.kb_vel = self.kb_vel.rotate(self.kb_rot * -1)
                self.kb_angle = GetAngle(self.hitsexp[0].pos.x, self.hitsexp[0].pos.y, self.pos.x, self.pos.y)
                self.kb_rot = self.kb_angle
                self.kb_vel = vec(0, self.hitsexp[0].kb[0])
                self.kb_vel = self.kb_vel.rotate(self.kb_rot)
                self.truevel = vec(0, 0)
                self.truevel += self.kb_vel
                self.trueacc = vec(0, 0)
                self.lifeleft = self.life
                self.team = self.hitsexp[0].target.team
        
        if self.lifeleft <= 0:
            if self.explosive:
                EXPLSN = Explosion(self, self.explosive[0], self.explosive[1], self.explosive[2], self.explosive[3], self.explosive[4],self.explosive[5],) #(self, target, size=50, maxsize=150, life=30, dmg=20, kb=40, stun=30)
            self.kill()
        else:
            self.lifeleft -= 1

    def FlameExpand(self):
        self.size += vec(70, 70)/self.life
        self.surf = pygame.Surface(self.size)
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(center = self.pos)
        self.alpha = 255 /self.life*self.lifeleft
        self.surf.set_alpha(self.alpha)
        if self.lifeleft <= self.life/3*2:
            self.dmg = self.initdmg/2


class Explosion(pygame.sprite.Sprite):
    def __init__(self, target, size=50, maxsize=150, life=30, dmg=20, kb=40, stun=30, cutscene=False, color=v.ORANGE):
        super().__init__()
        self.target = target
        self.size = vec(size, size)
        self.maxsize = vec(maxsize, maxsize)
        self.surf = pygame.Surface(self.size)
        if cutscene == False:
            self.rect = self.surf.get_rect(center = self.target.rect.center)
            self.color = color
        else:
            self.rect = self.surf.get_rect(center = vec(self.target.rect.center) + vec(random.randint(-250, 250), random.randint(-250, 250))) 
            self.color = v.YELLOW
        self.surf.fill(self.color)
        self.pos = vec(self.rect.center)
        self.life = life
        self.lifeleft = self.life
        self.initkb = kb #Bool = speed inheritance???????
        self.kb = (self.initkb, stun, True) 
        self.initstun = stun
        self.initdmg = dmg
        self.dmg = self.initdmg
        self.team = self.target.team
        self.pos = vec(self.rect.center)
        self.affected = []
        g.explosions.add(self)
        g.all_sprites.add(self)
        g.world_objects.add(self)
        
    def update(self):
        #Expand self
        #self.size += vec(100, 100)/self.life
        self.size += (self.maxsize - self.size)/2 * 0.2
        self.surf = pygame.Surface(self.size)
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(center = self.rect.center)
        self.alpha = 255 /self.life*self.lifeleft
        self.surf.set_alpha(self.alpha)
        
        if self.lifeleft <= 0:
            self.kill()
        else:
            self.lifeleft -= 1
            if self.lifeleft <= self.life * 2 / 3:
                self.kb = (self.initkb/2, self.initstun, True)
                self.dmg = self.initdmg/2
                if self.lifeleft <= self.life / 3:
                    self.kb = (0, 0, True)
                    self.dmg = 0
