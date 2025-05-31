import pygame as pg

'''lvldata = open(".\\data\\map.lvl","ab+")
pickle.dump(((300,460),(720,480)),lvldata)
lvldata.seek(0)
lvldata.seek(0,2)
print(lvldata.tell())'''
'''lvldata = open(".\\data\\map.lvl","ab+")
pickle.dump(((0,580),(1220,620)),lvldata)
lvldata.seek(0)
lvldata.seek(0,2)
print(lvldata.tell())'''
'''lvldata = open(".\\data\\map.lvl","ab+")
pickle.dump(((12*20,-400),(13*20,400)),lvldata)
lvldata.seek(0)
lvldata.seek(0,2)
print(lvldata.tell())'''
g = pg.Vector2(0,-30*16)
grndfriction = pg.Vector2(28*16,0)
'''def staticcollside(player, staticrectlist, newrect):
    colllist = []
    bottomcoll = False
    topcoll = False
    leftcoll = False
    rightcoll = False

    # + - 4 to remove overlap
    for rect in staticrectlist:

        #player.rect.top = newrect.top
        playerbtmline = ((player.rect.bottomleft[0]+1,player.rect.bottomleft[1]), (player.rect.bottomright[0]-1,player.rect.bottomright[1]))
        playertopline = ((player.rect.topleft[0]+1,player.rect.topleft[1]), (player.rect.topright[0]-1,player.rect.topright[1]))
        #playerbtmline = (player.rect.bottomleft,player.rect.bottomright)
        #playertopline = (player.rect.topleft, player.rect.topright)
        topcoll = bool(rect.clipline(playertopline))
        bottomcoll = bool(rect.clipline(playerbtmline))

        if "bottom" not in colllist and bottomcoll:
            colllist.append("bottom")
        if  "top" not in colllist and topcoll :
            colllist.append("top")
        if bottomcoll:
            player.place((player.rect.left, rect.top - player.rect.height))
            if player.velocity.y < 0:
                player.velocity.y = 0
        if topcoll:
            player.place((player.rect.left, rect.bottom))
            if player.velocity.y > 0:
                player.velocity.y = 0


        #player.rect.left = newrect.left
        playerrightline = ((player.rect.bottomright[0],player.rect.bottomright[1]-1), (player.rect.topright[0],player.rect.topright[1]+1))
        playerleftline = ((player.rect.bottomleft[0],player.rect.bottomleft[1]-1), (player.rect.topleft[0],player.rect.topleft[1]+1))
        #playerrightline = (player.rect.topright,player.rect.bottomright)
        #playerleftline = (player.rect.topleft, player.rect.bottomleft)
        leftcoll = bool(rect.clipline(playerleftline))
        rightcoll = bool(rect.clipline(playerrightline))

        if "left" not in colllist and leftcoll :
            colllist.append("left")
        if "right" not in colllist and rightcoll:
            colllist.append("right")
        if leftcoll:
            print("left")
            player.place((rect.right, player.rect.top))
            if player.velocity.x < 0:
                player.velocity.x = 0
        if rightcoll:
            print("right")
            player.place((rect.left - player.rect.width, player.rect.top))
            if player.velocity.x > 0:
                player.velocity.x = 0

    return colllist'''
def staticcollside(player, staticrectlist : list[pg.rect.Rect]):
    colllist = []
    playerbtmline = ((player.rect.bottomleft[0] + 1, player.rect.bottomleft[1]),(player.rect.bottomright[0] - 1, player.rect.bottomright[1]))
    playertopline = ((player.rect.topleft[0] + 1, player.rect.topleft[1]-1), (player.rect.topright[0] - 1, player.rect.topright[1]-1))
    playerrightline = ((player.rect.bottomright[0], player.rect.bottomright[1] - 1),(player.rect.topright[0], player.rect.topright[1] + 1))
    playerleftline = ((player.rect.bottomleft[0]-1, player.rect.bottomleft[1]-1), (player.rect.topleft[0]-1, player.rect.topleft[1]+1))
    for rect in staticrectlist:
        if bool(rect.clipline(playerleftline)):
            colllist.append("left")
            break
    for rect in staticrectlist:
        if bool(rect.clipline(playerrightline)):
            colllist.append("right")
            break
    for rect in staticrectlist:
        if bool(rect.clipline(playerbtmline)):
            colllist.append("bottom")
            break
    for rect in staticrectlist:
        if bool(rect.clipline(playertopline)):
            colllist.append("top")
            break

    return colllist


def moveandcollide(player, staticrectlist, dx,dy):

    xrem = dx
    if dx != 0: moveperframex = (dx/abs(dx))*2
    while xrem != 0:
        newrect = player.rect.move(moveperframex,0)
        if newrect.collidelist(staticrectlist) +1:
            player.velocity.x = 0
            break
        player.rect = newrect
        xrem -= moveperframex

    yrem = dy
    if dy != 0: moveperframey = (dy / abs(dy))*2
    while yrem != 0:
        newrect = player.rect.move(0, moveperframey)
        if newrect.collidelist(staticrectlist) +1:
            player.velocity.y = 0
            break
        player.rect = newrect
        yrem -= moveperframey



'''def onblock(player, blockrectlist):

    playerbtmline = (player.rect.bottomleft, player.rect.bottomright)
    for blockrect in blockrectlist:
        #coll = False
        coll = bool(blockrect.clipline(playerbtmline))
        blockrecttop = blockrect.top
        #coll = "bottom" in staticcollside(player, blockrectlist)
        if coll:
            player.place((player.rect.left, blockrecttop - player.rect.height))
            if player.velocity.y<0:
                player.velocity.y = 0
    #print()'''

'''def onblock(player, blockrect):
    playerbtmline = (player.rect.bottomleft, player.rect.bottomright)
    coll = bool(blockrect.clipline(playerbtmline))
    blockrecttop = blockrect.top
    #coll = "bottom" in staticcollside(player, blockrectlist)
    if coll:
        player.place((player.rect.left, blockrecttop - player.rect.height))
    #print()

    return coll'''


def dynamiccollside(player, dynamicspritelist):
    colllist = []

    # + - 4 to remove overlap
    playerbtmline = ((player.rect.bottomleft[0]+4,player.rect.bottomleft[1]), (player.rect.bottomright[0]-4,player.rect.bottomright[1]))
    playerleftline = ((player.rect.bottomleft[0],player.rect.bottomleft[1]-4), (player.rect.topleft[0],player.rect.topleft[1]+4))
    playerrightline = ((player.rect.bottomright[0],player.rect.bottomright[1]-4), (player.rect.topright[0],player.rect.topright[1]+4))
    playertopline = ((player.rect.topleft[0]+4,player.rect.topleft[1]), (player.rect.topright[0]-4,player.rect.topright[1]))
    for sprite in dynamicspritelist:

        if bool(sprite.rect.clipline(playerbtmline)) and "bottom" not in colllist:
            colllist.append("bottom")
        if bool(sprite.rect.clipline(playertopline)) and "top" not in colllist:
            colllist.append("top")
        if bool(sprite.rect.clipline(playerleftline)) and "left" not in colllist:
            colllist.append("left")
        if bool(sprite.rect.clipline(playerrightline)) and "right" not in colllist:
            colllist.append("right")

    return colllist


def applygrndfricrtion(player,keypress):
    error = player.grndfriction.x/(100)
    if "bottom" in player.staticcollideside and not player.isgrndfriction and player.shouldfric:
        if player.velocity.x == 0:
            pass
        elif player.velocity.x > 0:
            player.accel -= player.grndfriction
            player.isgrndfriction = True
            player.grndfrictionside.append("left")
        elif player.velocity.x < 0:
            player.accel += player.grndfriction
            player.isgrndfriction = True
            player.grndfrictionside.append("right")

    elif player.isgrndfriction and ((not ("bottom" in player.staticcollideside)) or (abs(player.velocity.x)<error)):
        if "left" in player.grndfrictionside:
            player.accel+= player.grndfriction
            player.grndfrictionside.remove("left")
            player.isgrndfriction = False
            if abs(player.velocity.x)<error:
                player.velocity.x = 0
        elif "right" in player.grndfrictionside:
            player.accel-= player.grndfriction
            player.grndfrictionside.remove("right")
            player.isgrndfriction = False
            if abs(player.velocity.x)<error:
                player.velocity.x = 0
    if player.velocity.x < 0 and "left" in player.grndfrictionside:
        player.accel+= player.grndfriction
        player.grndfrictionside.remove("left")
        player.isgrndfriction = False
        if abs(player.velocity.x)<error:
            player.velocity.x = 0
    elif player.velocity.x > 0 and "right" in player.grndfrictionside:
        player.accel-= player.grndfriction
        player.grndfrictionside.remove("right")
        player.isgrndfriction = False
        if abs(player.velocity.x)<error:
            player.velocity.x = 0
    if abs(player.velocity.x) < player.maxxvel and player.isgrndfriction:
        if "left" in player.grndfrictionside and keypress[player.rightkey]:
            player.accel+= player.grndfriction
            player.grndfrictionside.remove("left")
            player.isgrndfriction = False
            if abs(player.velocity.x)<error:
                player.velocity.x = 0
        elif "right" in player.grndfrictionside and keypress[player.leftkey]:
            player.accel-= player.grndfriction
            player.grndfrictionside.remove("right")
            player.isgrndfriction = False
            if abs(player.velocity.x)<error:
                player.velocity.x = 0

    if player.velocity.x > 0 and abs(player.velocity.x - player.maxxvel) < error:
        player.velocity.x = player.maxxvel
        if "left" in player.grndfrictionside and keypress[player.rightkey]:
            player.accel += player.grndfriction
            player.grndfrictionside.remove("left")
            player.isgrndfriction = False
    if player.velocity.x < 0 and abs(player.velocity.x + player.maxxvel) < error:
        player.velocity.x = -player.maxxvel
        if "right" in player.grndfrictionside and keypress[player.leftkey]:
            player.accel -= player.grndfriction
            player.grndfrictionside.remove("right")
            player.isgrndfriction = False

    if (not player.isgrndfriction and (keypress[player.leftkey] and keypress[player.rightkey])) and "bottom" in player.staticcollideside:
        if player.velocity.x == 0:
            pass
        elif player.velocity.x > 0:
            player.accel -= player.grndfriction
            player.isgrndfriction = True
            player.grndfrictionside.append("left")
        elif player.velocity.x < 0:
            player.accel += player.grndfriction
            player.isgrndfriction = True
            player.grndfrictionside.append("right")

 
def applygrav(player):
    if not "bottom" in player.staticcollideside and  not player.ingrav:
        player.accel += g
        player.ingrav = True
    elif "bottom" in player.staticcollideside and player.ingrav:
        player.accel -= g
        player.ingrav = False



