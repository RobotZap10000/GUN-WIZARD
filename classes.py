#importing CHANGE CHANGE
import pygame, sys
from pygame.locals import *
import random, time
import variables as v
import groups as g
from math import atan2, degrees

#initializing
pygame.init()
vec = pygame.math.Vector2 #2 = 2D
vec3 = pygame.math.Vector3
        
#Get angle
def GetAngle(startx, starty, endx, endy): #start, end, destination    
    #Getting angle
    dx = startx - endx
    dy = starty - endy
    rads = atan2(dy, dx)
    degs = round(degrees(rads))

    #Apply angle
    return degs + 90 #AND SO STARTS THE SPAGHETTI CODE

#Player
class Player(pygame.sprite.Sprite):
    def __init__(self, size=(v.PLAYERWIDTH, v.PLAYERHEIGHT), color=v.YELLOW, jumpvel=v.JUMPVEL, gravity=v.GRAVITY, team="players"):
        super().__init__()
        self.size = size
        self.surf = pygame.Surface(self.size)
        self.surf.fill(color)
        self.alpha = 255
        self.rect = self.surf.get_rect()
        self.jumpvel = jumpvel
        self.gravity = gravity
        self.jumping = False
        self.dropping = False
        self.jumpprompt = False
        self.standing = True
        self.wall = False
        self.ceiling = False
        self.firerate = 0 #12 #3 #In ticks
        self.firedelay = 0 #In ticks
        self.aim = 0
        self.weapon = 1
        self.knockback = True
        self.iframes = 50
        self.immunity = 0
        self.stun = 0
        self.team = team
        g.players.add(self)
        g.all_sprites.add(self)
        g.world_objects.add(self)
        g.knockback.add(self)

        #Player physics
        self.pos = vec((v.WIDTH/2,v.HEIGHT-150))
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

            if self.pressed_keys[K_a]: #OPTIMISE
                self.acc.x = -v.ACC
            if self.pressed_keys[K_d]:
                self.acc.x = v.ACC

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

        if self.immunity > 0:
            self.immunity -= 1

        if self.stun > 0:
            self.stun -= 1

        self.lastpos = vec(self.pos)

        #Self damage

        #Explosions
        if self.immunity == 0:
            self.hitsexp = pygame.sprite.spritecollide(self.collision, g.explosions, False)
            if self.hitsexp:
                if self not in self.hitsexp[0].affected:
                    if self.hitsexp[0].kb[0] != 0:
                        #RESET KB VEC ROT
                        self.kb_vel = self.kb_vel.rotate(self.kb_rot * -1)
                        self.kb_angle = GetAngle(self.hitsexp[0].pos.x, self.hitsexp[0].pos.y, self.pos.x, self.pos.y - self.size[1]/2)
                        self.kb_rot = self.kb_angle
                        self.kb_vel = vec(0, self.hitsexp[0].kb[0])
                        self.kb_vel = self.kb_vel.rotate(self.kb_rot)
                        self.vel += self.kb_vel
                        self.hitsexp[0].affected.append(self)
                        
                        self.immunity = self.iframes
                        self.stun = self.hitsexp[0].kb[1]
                        self.collision.move()
        
        #Enemy melee
        
        if self.immunity == 0:
            self.hitsenemy = pygame.sprite.spritecollide(self.collision, g.enemies, False)
            if self.hitsenemy:
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
                
                self.immunity = self.iframes
                self.stun = self.hitsenemy[0].kb[1]
                self.collision.move()

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
                    
                    self.immunity = self.iframes
                    self.stun = self.hitsproj[0].kb[1]
                    self.collision.move()

                    if not self.hitsproj[0].flame:
                        if self.hitsproj[0].explosive:
                            EXPLSN = Explosion(self.hitsproj[0])
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
        

        #Autojumping
        if self.jumpprompt == True:
            self.jump()

        #Firing delay
        if self.firedelay > 0:
            self.firedelay -= 1

        

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
            #(self, size, color, acc, gravity, rot, vel, maxvel, inherit, life, shooter, firerate, knockback, flame)
        
            if self.weapon == 1:
                PLAYERMAGIC = Projectile((50, 50), v.GREEN, (0, 0.5), None, self.aim, (0, 0), 20, None, 180, self, 12, (2, 10))

            if self.weapon == 2:
                PLAYERFLAME = Projectile((30, 30), v.RED, None, (0, -0.1), self.aim + (random.randint(-4, 4)), (0, 10), None, (self.vel.x*1.5, self.vel.y), 30, self, 3, (0, 10), flame=True)
                
            if self.weapon == 3:
                PLAYERBOMB = Projectile((50, 50), v.YELLOW, None, (0, 1), self.aim, (0, 20), None, self.vel, 120, self, 0, (5, 0),explosive=True)
                
    
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
    def __init__(self, originxy, ai=0):
        super().__init__()
        self.size = (70, 120)
        self.surf = pygame.Surface(self.size)
        self.surf.fill(v.MAGENTA)
        self.rect = self.surf.get_rect(midbottom = originxy)
        self.jumpvel = v.JUMPVEL
        self.gravity = v.GRAVITY
        self.kb = (10, 20, True)
        self.iframes = 5
        self.proj_immunity = 0
        self.exp_immunity = 0
        self.stun = 0
        self.team = "enemy"
        self.cycle_len = 240
        self.cycle = self.cycle_len
        self.aggrostate = False
        self.aggro = 1000
        self.deaggro = 1500
        self.aggrolen = 30
        self.aggroleft = self.aggrolen
        self.ai = ai
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
                                    self.acc.x = -v.ACC*0.8
                                else:
                                    self.acc.x = v.ACC*0.8

                                if self.pos.y > player.pos.y:
                                    #CHECK IF ENEMY CAN REACH PLAYER WITH JUMP, THEN:
                                    if abs(player.pos.x - self.pos.x) < (abs(self.jumpvel) / self.gravity * (v.ACC*0.8) * 10):
                                        self.jump()
                                else:
                                    self.cancel_jump()
                                    self.dropping = True

            if self.pressed_keys[K_g]: #OPTIMISE
                self.acc.x = -v.ACC
            if self.pressed_keys[K_j]:
                self.acc.x = v.ACC

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
                if not self.aggrostate:
                    if abs(self.playerdiff.length()) < self.aggro:
                        self.aggrostate = True
                        self.cycle = self.cycle_len
                else:
                    if abs(self.playerdiff.length()) > self.deaggro:
                        self.aggrostate = False
                        
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
        NMEMAGIC = Projectile((50, 50), v.PURPLE, (0, 1), None, self.aim, (0, 10), 30, None, 180, self, 0, (10, 10), noclip=True)

        
    #Enemy collision
    def update(self):

        if self.proj_immunity > 0:
            self.proj_immunity -= 1

        if self.exp_immunity > 0:
            self.exp_immunity -= 1

        if self.stun > 0:
            self.stun -= 1

        

        #if TICK > 0:

        #Self damage

        #Explosions
        if self.exp_immunity == 0:
            self.hitsexp = pygame.sprite.spritecollide(self.collision, g.explosions, False)
            if self.hitsexp:
                if self not in self.hitsexp[0].affected:
                    if self.hitsexp[0].kb[0] != 0:
                        #RESET KB VEC ROT
                        self.kb_vel = self.kb_vel.rotate(self.kb_rot * -1)
                        self.kb_angle = GetAngle(self.hitsexp[0].pos.x, self.hitsexp[0].pos.y, self.pos.x, self.pos.y - self.size[1]/2)
                        self.kb_rot = self.kb_angle
                        self.kb_vel = vec(0, self.hitsexp[0].kb[0])
                        self.kb_vel = self.kb_vel.rotate(self.kb_rot)
                        self.vel += self.kb_vel
                        self.hitsexp[0].affected.append(self)
                        
                        self.exp_immunity = self.iframes
                        self.stun = self.hitsexp[0].kb[1]
                        self.collision.move()

        #Projectiles
        if self.proj_immunity == 0:
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
                    
                    self.proj_immunity = self.iframes
                    self.stun = self.hitsproj[0].kb[1]
                    self.collision.move()

                    if not self.hitsproj[0].flame:
                        if self.hitsproj[0].explosive:
                            EXPLSN = Explosion(self.hitsproj[0])
                        self.hitsproj[0].kill()
            
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

    

#Scrollable map objects
class MapObject(pygame.sprite.Sprite):
    def __init__(self, size, color, originxy, groups): #Use dictionaries?
        super().__init__()
        self.surf = pygame.Surface(size)
        self.surf.fill(color)
        self.rect = self.surf.get_rect(center = originxy)
        if g.debug not in groups:
            g.all_sprites.add(self)
        for name in groups:
            name.add(self)
            
        
    def move(self):
        pass

    def update(self):
        pass

    #def ChangeTarget(self, newtarget):
    #    self.target = newtarget

#Projectile class?
class Projectile(pygame.sprite.Sprite):
    def __init__(self, size, color, acc, gravity, rot, vel, maxvel, inherit, life, shooter, firerate, kb, flame=False, explosive=False, noclip=False):
        super().__init__()
        self.size = vec(size)
        self.surf = pygame.Surface(self.size)
        self.color = vec3(color)
        self.surf.fill(color)
        self.rect = self.surf.get_rect(center = (shooter.pos.x, shooter.pos.y - shooter.size[1]/2))
        if acc != None:
            self.acc = vec(acc)
        else:
            self.acc = vec(0, 0)
        self.maxvel = maxvel
        self.vel = vec(vel)
        self.kb_vel = vec(0, 0)
        self.kb_rot = 0
        self.kb = kb
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
        shooter.firedelay = firerate

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
                    EXPLSN = Explosion(self)
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
                EXPLSN = Explosion(self)
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

class Explosion(pygame.sprite.Sprite):
    def __init__(self, target):
        super().__init__()
        self.target = target
        self.size = vec(50, 50)
        self.maxsize = vec(150, 150)
        self.surf = pygame.Surface(self.size)
        self.surf.fill(v.ORANGE)
        self.rect = self.surf.get_rect(center = self.target.rect.center)
        self.pos = vec(self.rect.center)
        self.life = 30
        self.lifeleft = self.life
        self.kb = (40, 30, False)
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
        self.surf.fill(v.ORANGE)
        self.rect = self.surf.get_rect(center = self.rect.center)
        self.alpha = 255 /self.life*self.lifeleft
        self.surf.set_alpha(self.alpha)
        
        if self.lifeleft <= 0:
            self.kill()
        else:
            self.lifeleft -= 1
            if self.lifeleft <= self.life * 2 / 3:
                self.kb = (20, 30, False)
                if self.lifeleft <= self.life / 3:
                    self.kb = (0, 0, False)
        
