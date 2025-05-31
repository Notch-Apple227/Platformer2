import os
from __physics__ import *
if not pg.font:
    print("Warning, fonts disabled")
if not pg.mixer:
    print("Warning, sound disabled")

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")


def load_image(name, colorkey=None, scale=1):
    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname)
    image = image.convert()

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    if scale != 1:
        image = pg.transform.scale(image, size)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()


def newload_image(path, colorkey=None, scale=1):
    image = pg.image.load(path)
    image = image.convert()

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    if scale != 1:
        image = pg.transform.scale(image, size)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image


def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()
    if name is None:
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    sound = pg.mixer.Sound(fullname)

    return sound

def newload_sound(path = None):
    class NoneSound:
        def play(self):
            pass

    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()
    if path is None:
        return NoneSound()
    sound = pg.mixer.Sound(path)

    return sound


class Vector(pg.Vector2):
    pol = 0
    def __init__(self,x,y):

        pg.Vector2.__init__(self)
        self.x = x
        self.y = y


class Playerunanim(pg.sprite.Sprite):

    maxxvel = 15 * 16
    maxfallvel = 7 * 16
    moveaccel = 60 * 16
    grndfriction = Vector(60 * 16, 0)
    jumpvel = 25 * 16
    coyoteframe = 5

    def __init__(self,velocity = Vector(0,0),accel = Vector(0,0), phobj = None,animimages = None,keys = (pg.K_UP,pg.K_DOWN,pg.K_LEFT,pg.K_RIGHT)):
        """
        animimages = dict(animstate: (animimages, gameframes per animframe))
        """
        pg.sprite.Sprite.__init__(self)
        self.image,self.rect = phobj, phobj.get_rect()
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.velocity = velocity
        self.accel = accel
        self.staticcollideside = []
        self.dynamiccollideside = []
        self.collidable = True
        self.subpixel = 0,0                       # rect.move takes int so only int speed possible DEBUG
        self.isgrndfriction = False
        self.grndfrictionside = []
        self.lookingside = "right"
        self.upkey,self.downkey,self.leftkey,self.rightkey = keys
        self.dashkey = pg.K_x
        self.shouldfric = True
        self.movingdir = []
        self.ingrav = False
        self.shouldjumpboost = False
        self.animstates = ["right_idle","right_idle"]
        self.animimages = animimages
        self.animindex = 0
        self.animframespassed = 0
        self.jumped = False
        self.dashing = False

    def calcnewpos(self, dt):
        self.velocity.x += self.accel.x*dt
        self.velocity.y += self.accel.y*dt
        dx =  + self.velocity.x * dt + self.subpixel[0]
        dy =  - self.velocity.y * dt + self.subpixel[1]    # - y coz y not follow cartesian way
        ddx = dx%2
        ddy = dy%2
        dx -= ddx
        dy -= ddy
        self.subpixel = ddx,ddy
        #return rect.move(dx,dy)
        return dx,dy
    '''def movelr(self):
        if self.movingdir[-1] == "left":
            if "right" in self.moveacceldir:
                self.moveacceldir.remove("right")
            if "left" not in self.moveacceldir and abs(self.velocity.x) <= self.maxxvel:
                self.moveacceldir.append("left")
            elif "left" in self.moveacceldir and abs(self.velocity.x) > self.maxxvel:
                self.moveacceldir.remove("left")
            if "left" in self.moveacceldir and abs(self.velocity.x) <= self.maxxvel:
                self.accel.x -= 20*20

        if self.movingdir[-1] == "right":
            if "left" in self.moveacceldir:
                self.moveacceldir.remove("left")
            if "right" not in self.moveacceldir and abs(self.velocity.x) <= self.maxxvel:
                self.moveacceldir.append("right")
            elif "right" in self.moveacceldir and abs(self.velocity.x) > self.maxxvel:
                self.moveacceldir.remove("right")
            if "right" in self.moveacceldir and abs(self.velocity.x) <= self.maxxvel:
                self.accel.x += 20*20'''

    def move(self,events,keypress):
        for event in events:
            if event.type == pg.KEYUP:
                #if event.key == self.upkey:
                #    self.accel.y = 0
                #if event.key == self.downkey:
                #    self.accel.y = 0
                if event.key == self.leftkey:
                    if "left" in self.movingdir:
                        self.accel.x += self.moveaccel
                        self.movingdir.remove("left")
                if event.key == self.rightkey:
                    if "right" in self.movingdir:
                        self.accel.x -= self.moveaccel
                        self.movingdir.remove("right")

        if keypress[self.leftkey]:
            if self.velocity.x > -self.maxxvel:
                if "left" not in self.movingdir:
                    self.accel.x -= self.moveaccel
                    self.movingdir.append("left")
            elif "left" in self.movingdir:
                self.accel.x += self.moveaccel
                self.movingdir.remove("left")

        if keypress[self.rightkey]:
            if self.velocity.x < self.maxxvel:
                if "right" not in self.movingdir:
                    self.accel.x += self.moveaccel
                    self.movingdir.append("right")
            elif "right" in self.movingdir:
                self.accel.x -= self.moveaccel
                self.movingdir.remove("right")

        if (not keypress[self.leftkey] and not keypress[self.rightkey]) or (self.velocity.x > self.maxxvel or self.velocity.x < -self.maxxvel) :
            self.shouldfric = True
        else:
            self.shouldfric = False

        self.shouldjumpboost = False
        self.jumped = False

        if keypress[self.rightkey]:
            self.lookingside = "right"
            self.shouldjumpboost = True
        elif keypress[self.leftkey]:
            self.lookingside = "left"
            self.shouldjumpboost = True

        if keypress[self.upkey] and "bottom" in self.staticcollideside:
            self.jump()
            self.jumped = True

        if keypress[self.dashkey]:
            self.dash()

    def jump(self):
        self.velocity.y = self.jumpvel
        if self.shouldjumpboost:
            if self.lookingside == "right":
                self.velocity.x += 20
            elif self.lookingside == "left":
                self.velocity.x -= 20

    def dash(self):
        self.velocity.x += 120

    def collision(self, rect=None, line=None, point=None):

        if not(rect or line or point):
            pass
        elif rect:
            coll = self.rect.colliderect(rect)
            if self.collidable and coll:
                self.collidable = False
                return coll
            if not self.collidable and not coll:
                self.collidable = True
                return coll

        elif line:
            coll = bool(self.rect.clipline(line))
            if self.collidable and coll:
                self.collidable = False
                return coll
            if not (self.collidable) and not (coll):
                self.collidable = True
                return coll
        elif point:
            coll = self.rect.collidepoint(point)
            if self.collidable and coll:
                self.collidable = False
                return coll
            if not (self.collidable) and not (coll):
                self.collidable = True
                return coll

    def place(self, point):
        self.rect.topleft = point


    def animate(self):
        if self.animimages:                               # check to animate or not
            if "transition" in self.animstates[1]:        # for transition animation, name: state1transitionstate2
                if self.animstates[0] != self.animstates[1]:
                    if self.animstates[0].split('_')[-1] == self.animstates[1].split('_')[-1]:         #left and right version of same transition state
                        self.image = self.animimages[self.animstates[1]][0][self.animindex]
                        self.animstates[0] = self.animstates[1]

                    else:
                        self.animindex = 0
                        self.animframespassed = 0
                    self.image = self.animimages[self.animstates[1]][0][self.animindex]
                    self.animstates[0] = self.animstates[1]

                if self.animstates[0]:
                    self.animframespassed += 1
                    if self.animframespassed >= self.animimages[self.animstates[0]][1]:
                        self.animindex += 1
                        self.image = self.animimages[self.animstates[0]][0][self.animindex]
                        if self.animindex == len(self.animimages[self.animstates[0]][0])-1:
                            self.animstates[1] = self.animstates[0].split("transition_")[1]
                            self.animindex = 0
                        self.animframespassed = 0

            else:
                if self.animstates[0] != self.animstates[1]:
                    self.animindex = 0
                    self.animframespassed = 0
                    self.image = self.animimages[self.animstates[1]][0][self.animindex]
                    self.animstates[0] = self.animstates[1]

                if self.animstates[0]:            
                    self.animframespassed +=1
                    if self.animframespassed >= self.animimages[self.animstates[0]][1]:
                        self.animindex +=1
                        if self.animindex == len(self.animimages[self.animstates[0]][0]):
                            self.animindex = 0
                        self.image = self.animimages[self.animstates[0]][0][self.animindex]
                        self.animframespassed -=  self.animimages[self.animstates[0]][1]

    def update(self, dt, staticblklist,events,keypress):
        self.move(events,keypress)
        dx,dy = self.calcnewpos(dt)
        moveandcollide(self, staticblklist, dx,dy)
        self.staticcollideside = staticcollside(self,staticblklist)
        #self.dynamiccollideside = dynamiccollside(self, dnamblklst)
        applygrndfricrtion(self,keypress)
        applygrav(self)
        #self.rect = newrect
        self.animate()


class Player(Playerunanim):
    def __init__(self, velocity=Vector(0, 0), accel=Vector(0, 0), phobj=None, animimages=None,
                 keys=(pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT)):
        super().__init__(velocity, accel, phobj, animimages, keys)

    def setanimstate(self):
        if self.jumped:
            self.animstates[1] = f"transition_{self.lookingside}_jump"
        if "transition" in self.animstates[1] and "jump" in self.animstates[1]:
            self.animstates[1] = f"transition_{self.lookingside}_jump"

        if "jump" in self.animstates[0] and "transition" not in self.animstates[0]:
            self.animstates[1] = f"{self.lookingside}_jump"

        if "bottom" in self.staticcollideside:
            if abs(self.velocity.x) <= 0.1:
                self.animstates[1] = f"{self.lookingside}_idle"
            else:
                self.animstates[1] = f"move_{self.lookingside}"
                
    
    def update(self, dt, staticblklist,events,keypress):
        self.move(events,keypress)
        dx,dy = self.calcnewpos(dt)
        moveandcollide(self, staticblklist, dx,dy)
        self.staticcollideside = staticcollside(self,staticblklist)
        #self.dynamiccollideside = dynamiccollside(self, dnamblklst)
        applygrndfricrtion(self,keypress)
        applygrav(self)
        #self.rect = newrect
        self.setanimstate()
        self.animate()
        


class Block(pg.sprite.Sprite):

    def __init__(self, phobj):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = phobj, phobj.get_rect()
        screen = pg.display.get_surface()
        self.area = screen.get_rect()

    def place(self, point):
        self.rect.bottomleft = point

    @staticmethod
    def build(point1: tuple, point2: tuple, phobj, blklist):
        rectlist = []
        tempblk = Block(phobj)

        for i in range(point1[0], point2[0], tempblk.image.get_size()[0]):
            for j in range(point1[1], point2[1], tempblk.image.get_size()[1]):
                blklist.append(Block(phobj))
                blklist[-1].place((i, j))
                rectlist.append(blklist[-1].rect)

        rect = rectlist[-1].unionall(rectlist)

        tempblk.kill()
        return rect


class Camera(pg.sprite.Sprite):
    def __init__(self, target : Playerunanim,playerdefpos, surface : pg.Surface, boundary : tuple[tuple[int,int],tuple[int,int]], AllEntities : pg.sprite.RenderPlain):
        pg.sprite.Sprite.__init__(self)
        self.leftboundary = boundary[0][0]
        self.topboundary = boundary[0][1]
        self.rightboundary = boundary[1][0]
        self.bottomboundary = boundary[1][1]
        self.target = target
        self.surface = surface
        self.rect = surface.get_rect()
        self.surfacerect = surface.get_rect()
        self.allentities = AllEntities
        self.defpos = playerdefpos
        self.changingpos = False
        self.csubpixel = [0,0]
        self.cvel = Vector(0,0)
        self.cmaxvel = Vector(0,0)
        self.caccel = Vector(0,0)


    def changetarget(self,target):
        self.target = target

    def follow(self):

        xdefpos = self.defpos[0]
        ydefpos = self.defpos[1]
        xcurpos = self.target.rect.x
        ycurpos = self.target.rect.y
        #global deltaxpos
        #global deltaypos
        #deltaxpos = (xcurpos - xdefpos)
        #deltaypos = (ycurpos - ydefpos)
        deltaxpos = (xcurpos - (self.rect.x + xdefpos))
        deltaypos = (ycurpos - (self.rect.y + ydefpos))
        newrect = self.rect.move(deltaxpos, deltaypos)
        self.rect.x = pg.math.clamp(newrect.x,self.leftboundary,self.rightboundary)
        '''if not(newrect.x < self.leftboundary) and not(newrect.x > self.rightboundary):
            self.rect.x = newrect.x'''
        '''elif newrect.x < self.leftboundary:
            #deltaxpos = self.leftboundary + xdefpos
            deltaxpos = 0
        elif newrect.x > self.rightboundary:
            #deltaxpos = self.rightboundary - (self.rect.width - xdefpos)
            deltaxpos = 0'''
        self.rect.y = pg.math.clamp(newrect.y,self.topboundary,self.bottomboundary)
        '''if not(newrect.y < self.topboundary) and not(newrect.y > self.bottomboundary):
            self.rect.y = newrect.y'''
        '''elif newrect.y < self.topboundary:
            deltaypos = 0
            #deltaypos = self.topboundary + ydefpos -170
        elif newrect.y > self.bottomboundary:
            #deltaypos = self.bottomboundary - ydefpos +170
            deltaypos = 0'''


        for entity in self.allentities:
            self.surface.blit(entity.image, (entity.rect.x - self.rect.x , entity.rect.y - self.rect.y))

    def changedefpos(self, newdefpos, mode, maxvel = Vector(300,0), accel = Vector(200,0), dt = 0.016):
        """mode 1: instantaneous
        mode 2: smooth
        mode 3: constant velocity
        """
        if not self.defpos == newdefpos:
            if not self.changingpos :
                if mode == 2:
                    self.changingpos = True
                    self.cmaxvel = maxvel
                    self.caccel = accel
                    self.cmaxvel.rotate_ip(self.cmaxvel.angle_to(Vector(newdefpos[0]-self.defpos[0],newdefpos[1]-self.defpos[1])))
                    self.caccel.rotate_ip(self.caccel.angle_to(Vector(newdefpos[0]-self.defpos[0],newdefpos[1]-self.defpos[1])))


                elif mode == 1:
                        self.defpos = newdefpos

            else:
                if mode == 2:
                    accelerating = True
                    decelerating = False
                    dis = (((newdefpos[0]-self.defpos[0])**2) + ((newdefpos[1]-self.defpos[1])**2))**(0.5)
                    if dis <= (self.cmaxvel.length_squared())/(2*self.caccel.length()):
                        accelerating = False
                        decelerating = True
                        if self.cmaxvel.as_polar()[1] == self.caccel.as_polar()[1]:
                            self.caccel.rotate_ip(180)


                    if accelerating and not self.cvel.x >= self.cmaxvel.x:
                        self.cvel.x += self.caccel.x * dt
                    if accelerating and not self.cvel.y >= self.cmaxvel.y:
                        self.cvel.y += self.caccel.y * dt

                    if decelerating:
                        self.cvel.x += self.caccel.x * dt
                        self.cvel.y += self.caccel.y * dt
                    dx = + self.cvel.x * dt #+ self.csubpixel[0]
                    dy = - self.cvel.y * dt #+ self.csubpixel[1]  # - y coz y not follow cartesian way
                    #ddx = dx - int(dx)
                   # ddy = dy - int(dy)
                    #self.subpixel = ddx, ddy
                    self.defpos[0] = self.defpos[0] + dx
                    self.defpos[1] = self.defpos[1] + dy
                    if newdefpos[0]-2<self.defpos[0]<newdefpos[0]+2 and newdefpos[1]-2<self.defpos[1]<newdefpos[1]+2  or self.cvel.length()<self.cmaxvel.length()/110:
                        self.changingpos = False
                        self.subpixel = [0,0]
                        self.cvel.x = self.cvel.y = 0
                        self.cmaxvel.x = self.cmaxvel.y = 0
                        self.caccel.x = self.caccel.y = 0
                        self.defpos = newdefpos










