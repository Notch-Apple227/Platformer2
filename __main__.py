import os
import threading
from __init__ import *
import pickle
from UI import *
import math
import time
pg.init()


class Animobj:

    def __init__(self,gameframesperframe,*args):
        self.gfpf = gameframesperframe
        self.images = args


class Resource:

    def __init__(self, foldername,filename, filetype, **kwargs):
        """
        filetype = ["image","sound","level"]
        """
        #if specargs is None:
        #   specargs = {}
        self.type = filetype
        self.folder = foldername
        self.mainfolder = ''
        if self.type == "image":
            self.mainfolder = "imgs"
        elif self.type == "sound":
            self.mainfolder = "sfxs"
        elif self.type == "level":
            self.mainfolder = "lvls"
        self.path = os.path.join(data_dir,self.mainfolder, self.folder,filename)
        self.specargs = kwargs

    def load(self):
        if self.type == "image":
            return newload_image(self.path,**self.specargs)

        if self.type == "sound":
            return newload_sound(self.path)

        if self.type == "level":
            return open(self.path,"ab+")


class Resourcehandler:

    def __init__(self):
        self.imgs = {}
        self.sfxs = {}
        self.lvls = {}
        self.animdicts = {}

    def addimg(self,name,image):
        self.imgs[name] = image

    def addsfx(self,name,sfx):
        self.sfxs[name] = sfx

    def addlvl(self, name, lvl):
        self.lvls[name] = lvl

    def addanimdict(self, name, animdict):
        self.animdicts[name] = animdict



flag = pg.SCALED #| pg.FULLSCREEN
screen = pg.display.set_mode((480, 270), flags=flag)
clock = pg.time.Clock()

#thread events

loadfin = threading.Event()

# Handlers

handler = Resourcehandler()

# Loaders

allloadbarrier = threading.Barrier(1, action=lambda: print("barrier broken"))
loaderlocals = threading.local()

handler.addlvl("map",Resource("level1","map.lvl","level").load())

def imageloader():
    writ = pg.font.Font(None, 64)
    loaderlocals.imgdir = os.path.join(data_dir, "imgs")
    loaderlocals.ress = []  # list[name,imgres]
    for folname in os.listdir(loaderlocals.imgdir):
        loaderlocals.ress.extend([(fname.split(".")[0], Resource(folname, fname, "image")) for fname in
                                  os.listdir(os.path.join(loaderlocals.imgdir, folname))])

    for namereso in loaderlocals.ress:
        screen.fill("BLACK")
        srf = writ.render(f"Loading {namereso[0]}",0,"BLUE","WHITE")
        screen.blit(srf,(112,100))
        handler.addimg(namereso[0], namereso[1].load())
        pg.display.flip()
        time.sleep(0.1)



    allloadbarrier.wait()
    loadfin.set()

def loadingscreen():

    imagethread = threading.Thread(target=imageloader)
    imagethread.start()

    while True:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False

        if loadfin.is_set():
            break



    handler.imgs["xph"].set_colorkey(handler.imgs["xph"].get_at((0,0)),pg.RLEACCEL)
    for im in handler.imgs:
        if "jump" in im:
            handler.imgs[im].set_colorkey(handler.imgs[im].get_at((0,0)),pg.RLEACCEL)


    print("AFTER")
    #print(handler.__dict__)
    #handler.addimg("xph",Resource("Player","xph.png","image",colorkey = -1, scale = 0.5).load())
    #xres = Resource("x.png","image",colorkey = -1, scale = 0.5)
    #global blockph,xph,bph,xrimages,xlimages,p1animdict
    #blockph = load_image("blocksmallnew16.png")[0]
    #xph = load_image("x.png", scale=0.5, colorkey=-1)[0]
    #xph = xres.load()
    bph = load_image("block.png")[0]

    #xrimages = [pg.transform.rotate(handler.imgs['xph'], i) for i in range(0, -90, -5)]
    xrimages = [handler.imgs[f"jump{z}"] for z in range(1,13)]
    rightanimobj = Animobj(3,*xrimages)
    #xrimages = [handler.imgs[z] if "jump" in z else   for z in sorted([im for im in handler.imgs])]

    xlimages = [pg.transform.flip(im,True,False) for im in xrimages]
    leftanimobj = Animobj(3, *xlimages)

    rjumpimages = [pg.transform.scale_by(handler.imgs['xph'], math.sin(math.radians(i))) for i in range(45,135,5)]
    rjumpanimobj = Animobj(2, *rjumpimages)

    ljumpimages = [pg.transform.flip(im,True,False) for im in rjumpimages]
    ljumpanimobj = Animobj(2, *ljumpimages)

    righttojump = [pg.transform.scale_by(handler.imgs['xph'], math.sin(math.radians(i))) for i in range(90,30,-10)]
    rtojumpanimobj = Animobj(3, *righttojump)

    lefttojump = [pg.transform.flip(im,True,False) for im in righttojump]
    ltojumpanimobj = Animobj(3, *lefttojump)

    ridleanimobj = Animobj(60, *[handler.imgs['xph']])
    lidleanimobj = Animobj(60, *[pg.transform.flip(handler.imgs["xph"],True,False)])

    p1animdict = {"move_right": rightanimobj, "move_left": leftanimobj,
                  "right_idle": ridleanimobj,
                  "left_idle": lidleanimobj,
                  "right_jump": rjumpanimobj,
                  "left_jump" : ljumpanimobj,
                  "transition_right_jump": rtojumpanimobj,"transition_left_jump": ltojumpanimobj}
    handler.addanimdict("p1animdict",p1animdict)


def levelloading():
    pass
def level():

    flag = pg.SCALED #| pg.FULLSCREEN
    #screen = pg.display.set_mode((1024, 512),flags=flag)
    pg.display.set_caption("GAME")
    dt = 0
    #clock = pg.time.Clock()
    t = 0


    '''blockph = load_image("blocksmallnew16.png")[0]
    xph = load_image("x.png",scale = 0.5,colorkey=-1)[0]
    bph = load_image("block.png")[0]
    xrimages = [pg.transform.rotate(xph,i) for i in range(0,-90,-5)]
    xlimages = [pg.transform.rotate(xph,-i) for i in range(0,-90,-5)]
    p1animdict = {"moveright": (xrimages,1),"moveleft": (xlimages,1), "idle": ([xph],60)}'''
    #pg.transform.scale_by(handler.imgs['bph'], 0.5)
    tempbtn = Button((70,100),phobj = pg.transform.scale_by(handler.imgs['bph'], 0.5))

    blklist = []
    staticrectlist = []


    #lvldata = open(".\\data\\map.lvl", "ab+")
    lvldata = handler.lvls['map']
    lvldata.seek(0,2)
    last = lvldata.tell()
    lvldata.seek(0)
    while lvldata.tell() < last:
        pt1, pt2 = pickle.load(lvldata)
        staticrectlist.append(Block.build(pt1, pt2, handler.imgs['blockph'], blklist))


    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((21, 40, 84))
    screen.blit(background, (0, 0))
    pg.display.flip()


    velo = Vector(0, 0)
    velo2 = Vector(140, -300)

    player = Player(velocity = velo, phobj = handler.imgs["xph"] ,animdict=handler.animdicts['p1animdict'],accel = pg.Vector2(0,0))
    player2 = Player(velocity = velo2, phobj = handler.imgs["xph"],accel = pg.Vector2(0,0),animdict = handler.animdicts['p1animdict'],keys = (pg.K_w,pg.K_s,pg.K_a,pg.K_d))
    player.place((100,200))
    player2.place((200,200))


    #flrrect = Block.build(pt1, pt2, "blocksmall.png", floorblklist)

    psprites = pg.sprite.Group(player,player2)
    blocksprites = pg.sprite.Group(blklist)
    btnsprites = pg.sprite.Group(tempbtn)
    allsprites = pg.sprite.Group(psprites,blocksprites)

    #staticrectlist.append(flrrect)
    pcam = Camera(player,[32,176],screen,((-5* unimulti,-20* unimulti),(175* unimulti,50* unimulti)),allsprites)
    #bgcam = Camera(player,[300,420],screen,((-500*20,-500*20),(500*20,500*20)),allsprites)

    def throwp(player):

        player.velocity.x += 400
        player.velocity.y += 800

    tempbtn.setfunc(throwp)
    tempbtn.setargs(player = player)

    running = True
    while running:
        events = pg.event.get()

        for event in events:
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                '''if event.key == pg.K_RIGHT:
                    player.animstates[1] = "moveright"
                if event.key == pg.K_LEFT:
                    player.animstates[1] = "moveleft"
            if event.type == pg.KEYUP:
                if event.key == pg.K_RIGHT:
                    player.animstates[1] = "idle"
                if event.key == pg.K_LEFT:
                    player.animstates[1] = "idle"
        if player.velocity.y>0:
            player.animstates[1] = "jump"'''


        keys = pg.key.get_pressed()

        
        psprites.update(dt, staticrectlist,events,keys)
        btnsprites.update()

        #if keys[pg.K_UP]:
        #    player.animstates[1] = "moverighttransitionjump"

       
        #psprites.draw(screen)
        #blocksprites.draw(screen)
        screen.blit(background, (0, 0))
        btnsprites.draw(screen)
        pcam.follow()
        pg.display.flip()
        dt = clock.tick(60)/1000
        t += dt


    pg.quit()


if __name__ == "__main__":
    loadingscreen()
    level()
