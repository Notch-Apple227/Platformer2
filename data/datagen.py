lvl =\
'''\
bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
bb                                                                                                                                                                           bb
bb                                                                                                                                                                           bb
bb                                                                                                                                                                           bb
bb                                                                                                                                                                           bb
bb                                                                                                                                                                           bb                  
bb                                                                                                                                                                           bb                  
bb                                                                                                                                                                           bb
bb                                                                                                                                                                           bb
bb                                                                                                                                                                           bb
bb                                                                                                  bbbbbbbb                                                                 bb
bb                                                                                                                                                                           bb
bb                                                         bbb                                                                                                               bb
bb                                                                                                                             bbbbbb                                        bb
bb                                                                                                                                                                           bb
bb                                                                                                                                                                           bb
bb                                                                                       bb                                                                                  bb
bb                             bbbbbbb                                                                                                                                       bb
bb                                                                                                                                   bbbbbbb                                 bb
bb                                                                                                                                                                           bb
bb                                                bbbbbbbbbbb                                                                                                                bb
bb                                                                                                                                                                           bb
bb                                                                        bbbbb                                                                                              bb
bb                                                                            bbbbb                                                                                          bb
bb                     bbbb                                                       bbbbb                                                                                      bb
bb                                                                                                                                                                           bb
bb                                                                                              bbbbbbbbbbbbb                                       bb                bb     bb
bb                                       bbbbbbbbb                                              bbbbbbbbbbbbb                                         bb            bb       bb
bb                                                                                                                                                      bb        bb         bb
bb                                                                                                                                                        bbbbbbbb           bb
bb                                                                     bbbbbbbbbbbb                                                                                          bb
bb                                                                                                                                                                           bb
bb                                                                                                                                                                           bb
bb                                                                                                                                                                           bb
bb                                                                                                                                                                           bb
bb                                                                                                                                                                           bb
bb                                                                                                                                                                           bb  
bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb  
bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbE   
                                                                                                                                                                                 '''
# Y - 2
import pickle
blksize = 16
lvldata = open(".\\map.lvl","wb+")
lvllist = lvl.split('\n')
l = len(lvllist)
fixlen = len(lvllist[-2])
for li in range(l):
    lvllist[li] = lvllist[li]+ ' '*fixlen
firstx  = firsty = lastx = lasty = 0
y = 0
x = 0
doing = True
counting = False
making = False
switching = False
counted = []
'''counting = False
making = False
while y < l:

    while x < len(lvllist[y]):

        global firstx,lastx,firsty,lasty
        if lvllist[y][x] == 'b' and (not counting and not making):
            firstx = x
            firsty = y
            counting = True
            making = True
            x+=1
            continue
        if counting and (lvllist[y][x] == ' '):
            lastx = x
            counting = False
            x = firstx
            lasty = y
            y += 1
            break
        if making and not counting:
            if lvllist[y][x] != 'b':
                #pickle.dump(((firstx*blksize,firsty*blksize),(lastx*blksize,lasty*blksize)),lvldata)
                lvldata.writelines([f"(({firstx*blksize},{firsty*blksize}),({lastx*blksize},{lasty*blksize}))"])
                print('yes')
                y = firsty
                x = lastx
                making = False
                break
            else:
                xint = x
                xloop = x
                while xloop <= lastx:
                    if lvllist[y][xloop] == 'b':
                        xint = xloop
                        xloop += 1
                    else:
                        break
                lastx = xint
                lasty = y
                y += 1
                break
        x+=1
    y+=1'''
while doing:
    print(y,x)
    if lvllist[y][x] == 'E':
        print("last",(y,x))
        doing = False
    elif y == l-1 and not counting and not making and not switching:
        x+=1
        y = 0


    elif lvllist[y][x]=='b' and not counting and not making and not switching and ((y,x) not in counted):
        counting = True
        firstx = x
        firsty = y
        y+=1
    elif not counting and not making and not switching and (lvllist[y][x] == ' ' or ((y, x) in counted)):

        y+=1

    elif counting  and not switching and lvllist[y][x] == 'b' and ((y,x) not in counted):

        y+=1
    elif counting and not switching and (lvllist[y][x] == ' ' or ((y,x) in counted)):
        counting = False
        lasty = y
        switching = True
        y = firsty
        x+=1
    elif switching:
        lastx = x
        if (lvllist[y][x] == ' '  or ((y,x) in counted)):
            pickle.dump(((firstx*blksize,firsty*blksize),(lastx*blksize,lasty*blksize)),lvldata)
            #lvldata.writelines([f"(({firstx * blksize},{firsty * blksize}),({lastx * blksize},{lasty * blksize}))"])
            print("write")
            for ly in range(firsty,lasty):
                for lx in range(firstx,lastx):
                    counted.append((ly,lx))

            counting = False
            making = False
            switching = False
            x = 0
            y = 0
        else:
            switching = False
            making = True
            y+=1
    elif making and lvllist[y][x] == 'b' and ((y,x) not in counted and not (y == lasty)) :
        y+=1
    elif making and (lvllist[y][x] == ' ' or ((y,x) in counted) or y == lasty):
        lasty = y
        y = firsty
        x+=1
        making = False
        switching =  True
print(counted)

lvldata.close()
