import pygame
from pygame.locals import *
import math, os, sys
from sys import exit
def onBox(obj, DOCK, TILESIZE):
    if obj.rect.x >= int(DOCK[0] + 8 * TILESIZE) and obj.rect.x <= int(DOCK[0] + 9 * TILESIZE):
        if obj.rect.y >= int(DOCK[1] + 7 * TILESIZE) and obj.rect.y <= int(DOCK[1] + 8 * TILESIZE):
            return True
        else:
            return False
    else:
        return False
def cargar_imagen(nombre, size, transparent=False):
     try: imagen = pygame.image.load(nombre)
     except pygame.error as message:
          raise SystemExit(message)
     imagen = imagen.convert_alpha()
     imagen = pygame.transform.scale(imagen, (size,size))
     if transparent:
          color = imagen.get_at((0,0))
          imagen.set_colorkey(color, RLEACCEL)
     return imagen

class Ghost(pygame.sprite.Sprite):
    def __init__(self, size, dock, tile, startx, starty, mazesprites):
        pygame.sprite.Sprite.__init__(self)
        self._d = dock
        self._t = tile
        self._m = mazesprites
        self.state = 'start'       #estados: start, activo, debil, comido, parpadear
        self.stop = False
        self._activo = []           #lista que contiene las imagenes del estado activo del fantasma
        self._debil = []            #lista que contiene las imagenes del estado debil
        self._comido = []           #lista que contiene las imagenes del estado comido
        self.parpadeo = False       #cuando esta finalizando el estado debil
        self.speed = 1
        self.load_imgs(size)
        self._changeimg = False
        self._selectimg = False
        self.image = self._activo[0] #inicia con la imgane normal del fantasma

        self.rect = self.image.get_rect()
        self.rect.x = startx
        self.rect.y = starty
        #self.x = 0
        #self.y = 0
        #self.posx = startx
        #self.posy = starty
        self.posicion = [self.rect.x, self.rect.y]
        self.home = [self._d[0] + (8 * self._t), self._d[1] + (9 * self._t)]   #posicion central de la caja del mapa donde nacen los fantasmas

        self.counter = 0
        self.time = pygame.time.get_ticks()
        self.last_move = 'u'
    def getState(self):
        return self.state
    def load_imgs(self, size):
        ''' Cargamos imágenes comunes a todos los fantasmas'''

        # Imágenes estado 'debil'
        afraid1 = cargar_imagen('ghost/afraid1.png', size)
        afraid2 = cargar_imagen('ghost/afraid2.png', size)

        # Imágenes estado 'debil' parpadeando
        blinker = cargar_imagen('ghost/blinker2.png', size)

        self._debil.append(afraid1)
        self._debil.append(afraid2)
        self._debil.append(blinker)

        # Imágenes estado 'comido' (eyes)
        eyes_down = cargar_imagen('ghost/eyes-down.png', size, True)
        eyes_up = cargar_imagen('ghost/eyes-up.png', size, True)
        eyes_left = cargar_imagen('ghost/eyes-left.png', size, True)
        eyes_right = cargar_imagen('ghost/eyes-right.png', size, True)

        self._comido.append(eyes_down)
        self._comido.append(eyes_up)
        self._comido.append(eyes_left)
        self._comido.append(eyes_right)


    def estado_start(self):
        '''
        estado en el que inicia el fantasma
        tambien cuando algun fantasma mata a pacman
        '''
        self.rect.x = self.posicion[0]
        self.rect.y = self.posicion[1]
        self.state = 'start'

    def estado_activo(self):
        '''
        estado en el que inicia el fantasma
        se llama cuando finaliza el estado debil donde el fantasma es vulnerable
        stambien cuando el fantasma es comido y llega al origen (caja del mapa)
        '''
        self.parpadeo = False
        self.state = 'activo'
    def estado_debil(self):
        '''
        estado vulnerable del fantasma, dura 8 segundos
        la variable self.time toma el tiempo para empezar el conteo
        se llama cuando pacman se come los puntos grandes
        '''
        self.state ='debil'
        self.time = pygame.time.get_ticks()
    def estado_comido(self):
        '''
        estado cuando el fantasma es comido por pacman, solo se ven los ojos
        '''
        self.rect.x = self.posicion[0]
        self.rect.y = self.posicion[1]
        self.state = 'comido'
        self.time = pygame.time.get_ticks()
    def estado_parpadear(self):
        '''
        se activa 2 segundos antes que finalice el estado debil
        '''
        self.parpadeo = True

    def ubicarObjeto(self, objeto = None, pointx = -1, pointy = -1):
        '''
        funcion que me permite determinar en que direccion se encuentra un objeto como pacman, o punto del mapa
        por player puedo recibir un sprite que tenga posx y posy para determinar su direccion respecto al fantasma
        si pointx y pointy son diferentes de -1 determino la dirreccion respecto al fantasma de ese punto en el mapa
        '''
        if objeto != None and pointx == -1 and pointy == -1:
            p = objeto
            objetox = p.posx
            objetoy = p.posy
        elif pointx != -1 and pointy != -1:
            objetox = pointx
            objetoy = pointy

        ghostx = self.posicion[0]
        ghosty = self.posicion[1]
        distx = ghostx - objetox
        disty = ghosty - objetoy
        #manh_dist = abs(distx) + abs(disty)
        if distx > 0 and disty > 0:
            if distx >= disty:
                return ['l','u','d','r']
            if distx < disty:
                return ['u','l','r','d']
        if distx < 0 and disty < 0:
            if abs(distx) >= abs(disty):
                return ['r','d','u','l']
            if abs(distx) < abs(disty):
                return ['d','r','l','u']
        if distx > 0 and disty < 0:
            if distx >= abs(disty):
                return ['l','d','u','r']
            if distx < abs(disty):
                return ['d','l','r','u']
        if distx < 0 and disty > 0:
            if abs(distx) >= disty:
                return ['r','u','d','l']
            if abs(distx) < disty:
                return ['u','r','l','d']
        if distx == 0 and disty > 0:
            return ['u','r','l','d']
        if distx == 0 and disty < 0:
            return ['d','l','r','u']
        if distx > 0 and disty == 0:
            return ['l','u','d','r']
        if distx < 0 and disty == 0:
            return ['r','d','u','l']
        if distx == 0 and disty == 0:
            return ['same']

    def changeimages(self, player):
        p = player
        if self.state == 'activo' or self.state == 'start':
            ubicar = self.ubicarObjeto(p)
            if ubicar[0] == 'd':
                if self.counter == 15:
                    self._changeimg = True
                    self._selectimg = not self._selectimg
                    self.counter = 0
                else:
                    self.counter += 1
                if self._selectimg:
                    self.image = self._activo[0]
                else:
                    self.image = self._activo[1]
            if ubicar[0] == 'u':
                if self.counter == 15:
                    self._changeimg = True
                    self._selectimg = not self._selectimg
                    self.counter = 0
                else:
                    self.counter += 1
                if self._selectimg:
                    self.image = self._activo[2]
                else:
                    self.image = self._activo[3]
            if ubicar[0] == 'l':
                if self.counter == 15:
                    self._changeimg = True
                    self._selectimg = not self._selectimg
                    self.counter = 0
                else:
                    self.counter += 1
                if self._selectimg:
                    self.image = self._activo[4]
                else:
                    self.image = self._activo[5]
            if ubicar[0] == 'r':
                if self.counter == 15:
                    self._changeimg = True
                    self._selectimg = not self._selectimg
                    self.counter = 0
                else:
                    self.counter += 1
                if self._selectimg:
                    self.image = self._activo[6]
                else:
                    self.image = self._activo[7]

        if self.state == 'debil':
            if not self.parpadeo:
                if self.counter == 15:
                    self._changeimg = True
                    self._selectimg = not self._selectimg
                    self.counter = 0
                else:
                    self.counter += 1
                if self._selectimg:
                    self.image = self._debil[0]
                else:
                    self.image = self._debil[1]
            if self.parpadeo:
                if self.counter == 15:
                    self._changeimg = True
                    self._selectimg = not self._selectimg
                    self.counter = 0
                else:
                    self.counter += 1
                if self._selectimg:
                    self.image = self._debil[0]
                else:
                    self.image = self._debil[2]

        if self.state == 'comido':
            ubicar = self.ubicarObjeto(p, self.home[0], self.home[1])
            if ubicar[0] == 'd':
                self.image = self._comido[0]
            if ubicar[0] == 'u':
                self.image = self._comido[1]
            if ubicar[0] == 'l':
                self.image = self._comido[2]
            if ubicar[0] == 'r':
                self.image = self._comido[3]
            '''
            if ubicar[0] == 'same':
                #self.image = self._comido[]
                pass
            '''

    def update(self, player, width, turn):
        p = player

        if self.rect.x < (self._d[0] - self._t + 5):
                self.rect.x = self._d[0] + self._t * (width -1)
        if self.rect.x + self._t > self._d[0] + self._t * (width)  :
                self.rect.x = self._d[0]
        if self.stop == False:
            if turn:
                self.moves(p)

        if self.state is 'activo' or self.state is 'start':
            self.changeimages(p)

        elif self.state is 'debil':
            get_time = pygame.time.get_ticks()
            debil_time = self.time + 8*1000         #tiempo que dura el estado debil del fantasma 8 segundos
            parpadear_time = self.time + 6*1000     #a los 6 segundos se activa el parpadeo durante 2 segundos

            if get_time >= parpadear_time and get_time < debil_time:
                self.estado_parpadear()
            elif get_time >= debil_time:
                self.estado_activo()
            self.changeimages(p)

        elif self.state is 'comido':
            get_time = pygame.time.get_ticks()
            comido_time = self.time + 4*1000         #tiempo que dura el estado comido del fantasma hasta recuperarse 3 segundos

            if get_time >= comido_time:
                self.estado_start()
            self.changeimages(p)

    def valid_move(self, direction, door_open=False):
        #solo realiza el movimiento si es valido
        aux = 0
        if direction == 'd':
            if onBox(self, self._d, self._t):
                self.valid_move(self, 'r')
            self.rect.y += self.speed
            aux = self.speed
            while aux > 0:
                ls = pygame.sprite.spritecollideany(self,self._m)

                if ls != None:
                    self.rect.y -= 1
                    aux -= 1
                else:
                    return aux
        if direction == 'u':
            self.rect.y -= self.speed
            aux = self.speed
            while aux > 0:
                ls = pygame.sprite.spritecollideany(self,self._m)

                if ls != None:
                    self.rect.y += 1
                    aux -= 1
                else:
                    return aux
        if direction == 'l':
            self.rect.x -= self.speed
            aux = self.speed
            while aux > 0:
                ls = pygame.sprite.spritecollideany(self,self._m)

                if ls != None:
                    self.rect.x += 1
                    aux -= 1
                else:
                    return aux
        if direction == 'r':
            self.rect.x += self.speed
            aux = self.speed
            while aux > 0:
                ls = pygame.sprite.spritecollideany(self,self._m)

                if ls != None:
                    self.rect.x -= 1
                    aux -= 1
                else:
                    return aux
        if aux == 0:
            return -1

    def moves(self, player):
        #funcion para definir los movimientos del fantasma
        p = player
        if self.state == 'start':
            #movimiento cuando el fantasma aparece en la caja
            nextm = self.valid_move('u')
            if nextm == -1 and onBox(self, self._d, self._t):
                if player.rect.x < self.rect.x:
                    nextm = self.valid_move('l')
                else:
                    nextm = self.valid_move('r')
                self.estado_activo()
            if nextm == -1:
                self.estado_activo()

        if self.state == 'activo':
            #movimiento cuando el fantasma esta en estado activo
            ubicar = self.ubicarObjeto(p)
            for x in range(4):
                nextm = self.valid_move(ubicar[x])
                if nextm != -1:
                    self.last_move = ubicar[x]
                    return
            if ubicar[0] == 'same':
                nextm = self.valid_move(self.last_move)


        if self.state == 'debil':
            ubicar = self.ubicarObjeto(p)
            away = ubicar[::-1]
            for x in range(4):
                nextm = self.valid_move(away[x])
                if nextm != -1:
                    self.last_move = away[x]
                    return
            if away[0] == 'same':
                nextm = self.valid_move(self.last_move)

        if self.state == 'comido':
            #moviento cuando el fantasma es comido
            pass


class Blinky(Ghost):
    __instance = None
    def __new__(cls, size, dock, tile, startx, starty, mazesprites):
        if Blinky.__instance is None:
            Blinky.__instance = object.__new__(cls)
        return Blinky.__instance
    def __init__(self, size, dock, tile, startx, starty, mazesprites):
        Ghost.__init__(self, size, dock, tile, startx, starty, mazesprites)

    def load_imgs(self, size):
        super().load_imgs(size)
        '''
        Cargamos imágenes para Blinky estado 'activo'
        '''
        img_red_d1 = cargar_imagen('ghost/red-down1.png', size)
        img_red_d2 = cargar_imagen('ghost/red-down2.png', size)
        img_red_u1 = cargar_imagen('ghost/red-up1.png', size)
        img_red_u2 = cargar_imagen('ghost/red-up2.png', size)
        img_red_l1 = cargar_imagen('ghost/red-left1.png', size)
        img_red_l2 = cargar_imagen('ghost/red-left2.png', size)
        img_red_r1 = cargar_imagen('ghost/red-right1.png', size)
        img_red_r2 = cargar_imagen('ghost/red-right2.png', size)

        self._activo.append(img_red_d1)
        self._activo.append(img_red_d2)
        self._activo.append(img_red_u1)
        self._activo.append(img_red_u2)
        self._activo.append(img_red_l1)
        self._activo.append(img_red_l2)
        self._activo.append(img_red_r1)
        self._activo.append(img_red_r2)




class Clyde(Ghost):
    __instance = None
    def __new__(cls,  size, dock, tile, startx, starty, mazesprites):
        if Clyde.__instance is None:
            Clyde.__instance = object.__new__(cls)
        return Clyde.__instance
    def __init__(self, size, dock, tile, startx, starty, mazesprites):
        Ghost.__init__(self, size, dock, tile, startx, starty, mazesprites)

    def load_imgs(self, size):
        super().load_imgs(size)
        '''
        Cargamos imágenes para Clyde estado 'activo'
        '''
        img_orange_d1 = cargar_imagen('ghost/orange-down1.png', size)
        img_orange_d2 = cargar_imagen('ghost/orange-down2.png', size)
        img_orange_u1 = cargar_imagen('ghost/orange-up1.png', size)
        img_orange_u2 = cargar_imagen('ghost/orange-up2.png', size)
        img_orange_l1 = cargar_imagen('ghost/orange-left1.png', size)
        img_orange_l2 = cargar_imagen('ghost/orange-left2.png', size)
        img_orange_r1 = cargar_imagen('ghost/orange-right1.png', size)
        img_orange_r2 = cargar_imagen('ghost/orange-right2.png', size)

        self._activo.append(img_orange_d1)
        self._activo.append(img_orange_d2)
        self._activo.append(img_orange_u1)
        self._activo.append(img_orange_u2)
        self._activo.append(img_orange_l1)
        self._activo.append(img_orange_l2)
        self._activo.append(img_orange_r1)
        self._activo.append(img_orange_r2)


class Inky(Ghost):
    __instance = None
    def __new__(cls,  size, dock, tile, startx, starty, mazesprites):
        if Inky.__instance is None:
            Inky.__instance = object.__new__(cls)
        return Inky.__instance
    def __init__(self, size, dock, tile, startx, starty, mazesprites):
        Ghost.__init__(self, size, dock, tile, startx, starty, mazesprites)

    def load_imgs(self, size):
        super().load_imgs(size)
        '''
        Cargamos imágenes para Inky estado 'activo'
        '''
        img_cian_d1 = cargar_imagen('ghost/cian-down1.png', size)
        img_cian_d2 = cargar_imagen('ghost/cian-down2.png', size)
        img_cian_u1 = cargar_imagen('ghost/cian-up1.png', size)
        img_cian_u2 = cargar_imagen('ghost/cian-up2.png', size)
        img_cian_l1 = cargar_imagen('ghost/cian-left1.png', size)
        img_cian_l2 = cargar_imagen('ghost/cian-left2.png', size)
        img_cian_r1 = cargar_imagen('ghost/cian-right1.png', size)
        img_cian_r2 = cargar_imagen('ghost/cian-right2.png', size)

        self._activo.append(img_cian_d1)
        self._activo.append(img_cian_d2)
        self._activo.append(img_cian_u1)
        self._activo.append(img_cian_u2)
        self._activo.append(img_cian_l1)
        self._activo.append(img_cian_l2)
        self._activo.append(img_cian_r1)
        self._activo.append(img_cian_r2)

class Pinky(Ghost):
    __instance = None
    def __new__(cls,  size, dock, tile, startx, starty, mazesprites):
        if Pinky.__instance is None:
            Pinky.__instance = object.__new__(cls)
        return Pinky.__instance
    def __init__(self, size, dock, tile, startx, starty, mazesprites):
        Ghost.__init__(self, size, dock, tile, startx, starty, mazesprites)

    def load_imgs(self, size):
        super().load_imgs(size)
        '''
        Cargamos imágenes para Pinky estado 'activo'
        '''
        img_pink_d1 = cargar_imagen('ghost/pink-down1.png', size)
        img_pink_d2 = cargar_imagen('ghost/pink-down2.png', size)
        img_pink_u1 = cargar_imagen('ghost/pink-up1.png', size)
        img_pink_u2 = cargar_imagen('ghost/pink-up2.png', size)
        img_pink_l1 = cargar_imagen('ghost/pink-left1.png', size)
        img_pink_l2 = cargar_imagen('ghost/pink-left2.png', size)
        img_pink_r1 = cargar_imagen('ghost/pink-right1.png', size)
        img_pink_r2 = cargar_imagen('ghost/pink-right2.png', size)

        self._activo.append(img_pink_d1)
        self._activo.append(img_pink_d2)
        self._activo.append(img_pink_u1)
        self._activo.append(img_pink_u2)
        self._activo.append(img_pink_l1)
        self._activo.append(img_pink_l2)
        self._activo.append(img_pink_r1)
        self._activo.append(img_pink_r2)



class GhostFactory(object):
    def get_ghost(self, id, dock, tilesize, size, mazesprites):
        '''
        id asignaciones - Blinky = 0, Clyde = 1, Inky = 2, Pinky = 3
        '''
        if id == 0:
            blinky_startx = dock[0] + (8 * tilesize)
            blinky_starty = dock[1] + (9 * tilesize)
            return Blinky(size, dock, tilesize, blinky_startx, blinky_starty, mazesprites)
        if id == 1:
            clyde_startx =  dock[0] + (8 * tilesize)
            clyde_starty = dock[1] + (9 * tilesize)
            return Clyde(size, dock, tilesize, clyde_startx, clyde_starty, mazesprites)
        if id == 2:
            inky_startx =  dock[0] + (8 * tilesize)
            inky_starty = dock[1] + (9 * tilesize)
            return Inky(size, dock, tilesize, inky_startx, inky_starty, mazesprites)
        if id == 3:
            pinky_startx = dock[0] + (8 * tilesize)
            pinky_starty = dock[1] + (9 * tilesize)
            return Pinky(size, dock, tilesize, pinky_startx, pinky_starty, mazesprites)
        # if id != 0 and id != 1 and id != 2 and id != 3:
        #         print('The input was not a valid integer. The ghost was not created..."'
