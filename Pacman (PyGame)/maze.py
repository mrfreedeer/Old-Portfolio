import pygame
import json
import math
import collections.abc
from pygame.locals import *
from sys import exit


red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)

class Jugador(pygame.sprite.Sprite):
    def __init__(self,ancho, alto, dock, tile, startx, starty, path):
        pygame.sprite.Sprite.__init__(self)
        self._startx = startx
        self._starty = starty
        self._d = dock
        self._t = tile
        self._width = ancho
        self._height = alto
        self.image = path
        self.rect = self.image.get_rect()
        self.rect.x = startx
        self.rect.y = starty
        self.x = 0
        self.y = 0
        self.posx = startx
        self.posy = starty
        self._lives = 3
    def reset(self):
        self.rect.x = self._startx
        self.rect.y = self._starty
        self.x = 0
        self.y = 0
        self.posx = self._startx
        self.posy = self._starty
        self.updatemain(pygame.K_LEFT)


    def update(self, mazesprites, width):
        ls_col = pygame.sprite.spritecollide(self, mazesprites, False)
        cols = False
        for colision in ls_col:
            cols = True
            if self.x> 0:
                self.rect.right = colision.rect.left
            if self.x< 0:
                self.rect.left = colision.rect.right
        self.posx = self.rect.x

        for colision in ls_col:
            if self.y > 0:
                self.rect.bottom = colision.rect.top
            if self.y < 0:
                self.rect.top = colision.rect.bottom
        self.posy = self.rect.y

        if self.posx < (self._d[0] - self._t + 5):
            self.posx =  self._d[0] + self._t * (width -1)
            self.rect.x = self._d[0] + self._t * (width -1)
        if self.posx > self._d[0] + self._t * (width)  :
            self.posx = self.rect.x = self._d[0]
    def crashed(self, object):
        return pygame.sprite.collide_rect(self, object)
    def die(self, deathimages, pantalla):
         imageind = 0
         while imageind <= 6:
             pygame.draw.rect(pantalla, black, (self.posx, self.posy, self._width, self._height) )
             pantalla.blit(deathimages[imageind],(self.rect.x, self.rect.y))
             pygame.display.flip()
             pygame.time.delay(100)
             imageind += 1
         magic = pygame.Surface((self._t, self._t))
         pantalla.blit(magic, (self.rect.x, self.rect.y))
         self._lives -= 1
         self.reset()

    def Right(self):
        return 1
    def Up(self):
        return 2
    def Left(self):
        return 3
    def Down(self):
        return 4
    def updatemain(self, mantain):        #Ajusta solamente la dirección del movimiento
        if mantain == pygame.K_RIGHT:   #del jugador (arriba, abajp, etc)
            self.x = 5

        elif mantain == pygame.K_LEFT:
            self.x = -5
        elif mantain == pygame.K_UP:
            self.y = -5
        elif mantain == pygame.K_DOWN:
            self.y = 5

        if mantain == pygame.K_DOWN or mantain == pygame.K_UP:
            self.x = 0
        elif mantain == pygame.K_LEFT or mantain == pygame.K_RIGHT:
            self.y = 0
    def movement(self, key, speed):   #Maneja el movimiento del jugador
        if key == pygame.K_RIGHT:   #para actualizarlo en caso de que la
            self.rect.x += speed      #tecla oprimida cambie
            self.posx += speed
        if key == pygame.K_LEFT:
            self.rect.x -= speed
            self.posx -= speed
        if key == pygame.K_UP:
            self.rect.y -= speed
            self.posy -= speed
        if key == pygame.K_DOWN:
            self.rect.y += speed
            self.posy += speed

    def changedir(self, key, jp):   #Reajusta la dirección de la sombra del jugador
        if key == pygame.K_RIGHT:
            move = True
            self.x = 5
            self.y = 0
            self.rect.x = jp.rect.x + 1
            self.rect.y = jp.rect.y
        elif key == pygame.K_LEFT:
            move = True
            self.x = -5
            self.y = 0
            self.rect.x = jp.rect.x - 1
            self.rect.y = jp.rect.y
        elif key == pygame.K_UP:
            move = True
            self.y = -5
            self.x = 0
            self.rect.x = jp.rect.x
            self.rect.y = jp.rect.y - 1
        elif key == pygame.K_DOWN:
            move = True
            self.y = 5
            self.x = 0
            self.rect.x = jp.rect.x
            self.rect.y = jp.rect.y + 1


class Wall (pygame.sprite.Sprite):
    def __init__(self, x, y, tilesize):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((tilesize, tilesize))
        self.image.fill(blue)
        self.rect = self.image.get_rect(x = x, y = y)
class Xline (pygame.sprite.Sprite):
    def __init__(self, x, y, tilesize):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((tilesize, 1))
        self.image.fill(blue)
        self.rect = self.image.get_rect(x = x, y = y)
class Yline (pygame.sprite.Sprite):
    def __init__(self, x, y, length):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1, length))
        self.image.fill(blue)
        self.rect = self.image.get_rect(x = x, y = y)


class Invidot(pygame.sprite.Sprite):
    def __init__(self,x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5,5))
        self.image.fill(white)
        self.rect = self.image.get_rect(x = x, y = y)
    def modpos(self,x,y):
        self.rect.x = x
        self.rect.y = y

class Powerpellets(pygame.sprite.Sprite):
    def __init__(self, x, y, path):
        pygame.sprite.Sprite.__init__(self)
        self.image = path
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class MazeIterator(collections.abc.Iterator):
    def __init__(self, maze):
        self._m = maze
        self._posx = 0
        self._newposx = 0
        self._newposy = 0
        self._posy = 0
        self._invi = Invidot(maze._d[0] + (maze.getTile()/2), maze._d[1] + (maze.getTile()/2))
        self._addedsprites = []
        self._addedsprites.append(Wall(self._m._d[0], self._m._d[1] + 6 * self._m.getTile(), 3*self._m.getTile()))
        self._addedsprites.append(Wall(self._m._d[0], self._m._d[1] + 10 * self._m.getTile(), 3*self._m.getTile()))
        self._addedsprites.append(Wall(self._m._d[0] + ((self._m.getWidth() - 3)  * self._m.getTile()), self._m._d[1] + 6 * self._m.getTile(), 3*self._m.getTile()))
        self._addedsprites.append(Wall(self._m._d[0] + ((self._m.getWidth() - 3) * self._m.getTile()), self._m._d[1] + 10 * self._m.getTile(), 3*self._m.getTile()))
        y = 0
        while y < 3 :
            z = 0
            while z < 5:
                self._addedsprites.append(Wall(self._m._d[0] + ((6 + z) * self._m.getTile()), self._m._d[1] + ((8 + y) * self._m.getTile()), self._m.getTile()))
                z += 1
            y += 1
        for x in self._addedsprites:
            self._m.addToSprites(x)

    def __next__(self):
        if self._newposx != 0 and self._newposy != 0:
            self._invi.modpos(self._newposx, self._newposy)
        if self._posy < self._m._height:
            ls = pygame.sprite.spritecollideany(self._invi, self._m.getSprites())
            self._posx += .744
            if self._posx >= self._m.getWidth()-.744:
                self._posx = 0
                self._posy += 1
            self._newposx = (self._posx * self._m.getTile() + (self._m.getTile()/2)) + self._m._d[0]
            self._newposy = (self._posy * self._m.getTile() + (self._m.getTile()/2)) + self._m._d[1]

            if ls == None:
                return Invidot(self._invi.rect.x, self._invi.rect.y)
        else:
            for x in self._addedsprites:
                x.kill()
            raise StopIteration()


class Mazefactory(object):
    def getPart(self, kind, posx, posy, size, dock):
        if kind == '5':
            return(Xline(posy * size + dock[0], posx * size + dock[1] - 1, size))
        elif kind == '6':
            return(Xline(posy * size + dock[0], (posx + 1) * size + dock[1] + 1, size))
        elif kind == '7':
            return(Yline(posy * size + dock[0] - 1, posx * size + dock[1], size))
        elif kind == '8':
            return(Yline((posy + 1) * size + dock[0] + 1, posx * size + dock[1], size))
        elif kind == '9':
            return (Wall(posy * size + dock[0],  posx * size + dock[1], size))
        elif kind == '-':
            return(Xline(posy * size + dock[0], (posx + 1) * size + dock[1], size))
        elif kind == '+':
            return(Xline(posy * size + dock[0], posx * size + dock[1], size))
        elif kind == ',':
            return(Yline((posy + 1)  * size + dock[0], posx * size + dock[1], size))

    def getCorner(self,kind,posx,posy,size,dock):
        if kind == '1':
            return ((Xline(posy * size + dock[0], posx * size + dock[1] - 1, size)), (Yline(posy * size + dock[0] - 1, posx * size + dock[1], size)))
        elif kind == '2':
            return((Xline(posy * size + dock[0], posx * size + dock[1] - 1, size)),(Yline((1 + posy) * size + dock[0], posx * size + dock[1], size)))
        elif kind == '3':
            return ((Xline(posy * size + dock[0], (posx + 1) * size + dock[1], size)),(Yline(posy * size + dock[0] - 1, posx * size + dock[1], size)))
        elif kind == '4':
            return((Xline(posy * size + dock[0], (posx + 1) * size + dock[1], size)),(Yline((posy + 1) * size + dock[0], posx * size + dock[1], size)))

def readmaze(string):
    json_data = open(string).read().split("\n")
    return json_data

class Builder(object):
    def __init__( self, mazelocation, free):
        self._mloc = mazelocation
        self._FREE = free
        self._m = readmaze(mazelocation)
        self._dotnum = 0

    def buildscreen(self):
        self._screensize = pygame.display.Info()
        self._p = pygame.display.set_mode([self._screensize.current_w,self._screensize.current_h])
        self._t = math.ceil(abs((self._screensize.current_h - self._FREE)) /(len(self._m) - 1) )
        self._psize = int(self._t)
        x = (self._screensize.current_w / 2 ) - (8.5 * self._t)
        y = (self._screensize.current_h / 2) - (11 * self._t) - 50
        self._DOCK = (x,y)
        self._startx = self._DOCK[0] + (8 * self._t)
        self._starty = self._DOCK[1] + 15 * self._t
        return self._p
    def getScreenwidth(self):
        return self._screensize.current_w
    def getScreenheight(self):
        return self._screensize.current_h
    def buildplayer(self, currentpac, startx = 0, starty = 0):
        if startx == 0 and starty == 0:
            return Jugador(self._psize,self._psize, self._DOCK, self._t, self._startx, self._starty, currentpac)
        else:
            return Jugador(self._psize,self._psize, self._DOCK, self._t, startx, starty, currentpac)
    def tilesize(self):
        return self._t
    def buildmaze(self):
        return Maze(self._mloc, self._FREE, self._screensize.current_h, self._DOCK, self._p)
    def playersize(self):
        return self._psize
    def dock(self):
        return self._DOCK
    def buildmagic(self):
        return pygame.Surface((self._t,3 * self._t))
    def builcpacdotmagic(self):
        return pygame.Surface((6,6))
    def buildpacdots(self, maze):
        pacdots = pygame.sprite.Group()

        for x in maze:
            if x!= None:
                pacdots.add(x)
                self._dotnum += 1
        return pacdots
    def buildpellets(self, image, m):
        ppellets = pygame.sprite.Group()
        ppelletpos = [(self._DOCK[0] + 0.2 * self._t, 2.75 * self._t)]
        ppelletpos.append((self._DOCK[0] + (m.getWidth() -.9)*self._t, 2.75 * self._t))
        ppelletpos.append((self._DOCK[0] + 0.2 * self._t, (15 + 2.75) * self._t))
        ppelletpos.append((self._DOCK[0] + (m.getWidth() -.9)*self._t, (15 + 2.75) * self._t))
        for x in ppelletpos:
            self._dotnum += 1
            ppellets.add(Powerpellets(x[0], x[1], image))
        return ppellets

    def buildscore(self):
        return Score(self._dotnum)
class Score(object):
    def __init__(self, pacnum):
        self._dotnum = pacnum
        self._consumed = 0
        self._ppellets = 4
    def consume(self):
        self._dotnum -= 1
        self._consumed += 1
    def bigconsume(self):
        if self._ppellets > 0:
            self._dotnum -= 1
            self._ppellets -= 1
            self._consumed += 1
    def getScore(self):
        return self._consumed * 10 + (4 - self._ppellets) * 50

class Life(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Maze(object):
    def __init__(self, string, free, height, DOCK, pantalla):
        self._d = DOCK
        self._p = pantalla
        self._mazemap = readmaze(string)
        self._width = len(self._mazemap[0])
        self._height = len(self._mazemap) - 1
        self._t = math.ceil(abs((height - free)) / self._height)
        self._sprites = pygame.sprite.Group()

    def getTile(self):
        return self._t
    def getWidth(self):
        return self._width

    def draw(self):
        corners = ['1','2','3','4']
        Factory = Mazefactory()
        for row in range(self._height):
            for col in range(self._width):
                if self._mazemap[row][col] in corners:
                    tuple = Factory.getCorner(self._mazemap[row][col], row, col, self._t, self._d)
                    for x in tuple:
                        self._sprites.add(x)
                elif self._mazemap[row][col] == '0':
                    pass
                elif self._mazemap[row][col]!='9':
                    x = Factory.getPart(self._mazemap[row][col], row, col, self._t, self._d)
                    self._sprites.add(x)
                else:
                    self._sprites.add(Factory.getPart(self._mazemap[row][col], row, col, self._t, self._d))

        z = Yline(self._d[0] - self._t - 5, self._d[1], self._t * self._height)
        z1 = Yline(self._d[0] + self._t * (self._width + 1) + 5, self._d[1], self._t * self._height)
        z2 = Xline(self._d[0] - self._t , self._d[1] + self._t * 9 - 1, self._t)
        z3 = Xline(self._d[0] - self._t , self._d[1] + self._t * 10, self._t)
        z4 = Xline(self._d[0] + self._t * (self._width ) , self._d[1] + self._t * 9 - 1, self._t)
        z5 = Xline(self._d[0] + self._t * (self._width ) , self._d[1] + self._t * 10, self._t)

        z6 = Xline(self._d[0] + 8 * self._t, self._d[1] + 8 * self._t, self._t)
        self._sprites.draw(self._p)
        self._sprites.add(z)
        self._sprites.add(z1)
        self._sprites.add(z2)
        self._sprites.add(z3)
        self._sprites.add(z4)
        self._sprites.add(z5)
        #_____________________________# Pared que bloquea Salida a Fantasmas
        #self._sprites.add(z6)
        #_____________________________#

    def crashed(self, object):
        ls = pygame.sprite.spritecollideany(object, self._sprites, False)
        if ls != None:
            return True
        else:
            return False

    def getSprites(self):
        return self._sprites
    def addToSprites(self, spr):
        self._sprites.add(spr)
    def __iter__(self):
        return MazeIterator(self)
