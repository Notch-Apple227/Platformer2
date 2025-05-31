import pygame as pg


class Button(pg.sprite.Sprite):

    def __init__(self, pos=(0, 0), phobj=None, animimages=None):
        """
        animimages = dict(animstate: (animimages, gameframes per animframe))
        (hover,held,idle states)
        """
        pg.sprite.Sprite.__init__(self)
        self.func = lambda *args, **kwargs: print("No function")
        self.image, self.rect = phobj, phobj.get_rect()
        self.place(pos)
        self.animstates = ["idle", "idle"]
        self.animimages = animimages
        self.animindex = 0
        self.animframespassed = 0
        self.hover = False
        self.held = False
        self.click = False
        self.funcargs = ()
        self.funckwargs = {}

    def place(self, point):
        self.rect.topleft = point

    def getstate(self):
        mpos = pg.mouse.get_pos()
        lclicked = pg.mouse.get_pressed()[0]
        self.click = False

        if self.rect.collidepoint(mpos):
            self.hover = True
        else:
            self.hover = False
        if self.hover and lclicked:
            self.held = True
        if self.held and not self.hover:
            self.held = False
        if self.held and not lclicked:
            self.click = True
            self.held = False

    def setfunc(self, func):
        self.func = func

    def setargs(self, *args, **kwargs):
        self.funcargs = args
        self.funckwargs = kwargs

    def update(self, *args, **kwargs):
        self.getstate()
        if self.click:
            self.func(*(args or self.funcargs), **(kwargs or self.funckwargs))
