import pygame
import random
import math
import enemigo
random.seed(pygame.time.get_ticks())

ALTO=1000
ANCHO=1000
pygame.mixer.init(44100, -16, 2, 2048)
channel5 = pygame.mixer.Channel(4)
disparo=pygame.mixer.Sound('disparo.ogg')
blast=pygame.mixer.Sound('blast.ogg')
disparo.set_volume(0.3)

#screensize = pygame.display.Info()
#RESOLUTION = [screensize.current_w, screensize.current_h]
#bglimit = 10
#Funciones

def recortarTorr(archivo):
    fondo=pygame.image.load(archivo)
    infoFondo=fondo.get_rect()
    matriz=[]
    spawn=[[0, 34, 87, 79], [89, 34, 87, 79], [178, 34, 87, 79], [267, 34, 87, 79], [356, 34, 87, 79],
            [445, 34, 87, 79], [534, 34, 87, 79], [624, 34, 87, 79], [713, 34, 87, 79]]
    shoot=[17, 195, 87, 79]
    explode=[[89, 280, 97, 97], [193, 280, 97, 97], [300, 280, 97, 97], [400, 280, 97, 97], [600, 280, 97, 97]]
    spawnS=[]
    shootS=[]
    explodeS=[]


    #Spawn L
    for x in range(9):
        cuadro=fondo.subsurface(spawn[x])
        spawnS.append(cuadro)

    #Unspawn L
    for x in range(9):
        cuadro=fondo.subsurface(spawn[8-x])
        spawnS.append(cuadro)

    #Explode L
    for x in range(5):
        cuadro=fondo.subsurface(explode[x])
        explodeS.append(cuadro)


    cuadro=fondo.subsurface(shoot)
    shootS.append(cuadro)

    return spawnS, shootS, explodeS


def recortarBalaT(archivo):
    fondo=pygame.image.load(archivo)
    infoFondo=fondo.get_rect()
    matriz=[]

    cuadro=fondo.subsurface(108, 201, 35, 11)
    matriz.append(cuadro)

    return matriz

matrizBalaT=recortarBalaT('torreta.png')

#Clases
class Turret(pygame.sprite.Sprite):
    def __init__(self, matriz):
        pygame.sprite.Sprite.__init__(self)
        self.f=matriz
        self.image=self.f[0][0]
        self.rect=self.image.get_rect()
        self.indice=0
        self.rect.x=50
        self.rect.y=500
        self.accion=0
        self.dir = 'L'
        self._health = 100
        self.shoottimer = 25
        self.shoot = False
        self.incremento=1
        self.spawned=False
        self.hide=True

    def getHealth(self):
        return self._health

    def die(self):
        #ouch.play()

        channel5.play(blast)


    def shooting(self, posPlayer):
        if posPlayer[0]-self.rect.x<=400:
            self.hide=False
        if not self.hide:
            self.shoottimer -= 1
            if self.shoottimer < 0:
                self.shoot = True
                self.shoottimer = random.randrange(20,50)
            if self.spawned:
                if self.shoot:
                    channel5.play(disparo)
                    self.accion=1
                    #self.rect.x-=17
                else:
                    #self.rect.x+=17
                    self.accion=0
                    self.indice=8
    def update(self):
        #Idle L

        if self.accion==0:
            if self.hide:
                self.image = self.f[self.accion][0]
            else:
                self.image = self.f[self.accion][self.indice]
                self.indice += self.incremento

                if self.indice >=8:
                    self.incremento=0
                    self.indice+=self.incremento
                    self.spawned=True


        #1
        #Attack L
        if self.accion==1:
            self.indice=0
            self.image = self.f[self.accion][self.indice]
            shoot=BalaT(matrizBalaT)
            self.shoot=False
            self.shoottimer=25




class BalaT(pygame.sprite.Sprite):
    def __init__(self, matriz):
        pygame.sprite.Sprite.__init__(self)
        self.f=matriz
        self.image=self.f[0]
        self.rect=self.image.get_rect()
        self.rect.x=50
        self.rect.y=450
        self.vel_x=50
        self.dir = 'L'
        self.lucky = random.randrange(0,2)
    def AIbullet(self, player, noplayers = 1, player2 = None):
        movedir = random.randrange(0,2)
        if noplayers == 1:
            selectplayer = player
        else:
            distanceplayer1 = math.fabs(player.rect.x-self.rect.x)+math.fabs(player.rect.y-self.rect.y)
            distanceplayer2 = math.fabs(player2.rect.x-self.rect.x)+math.fabs(player2.rect.y-self.rect.y)
            if distanceplayer1 > distanceplayer2:
                selectplayer = player2
            else:
                selectplayer = player
        if movedir:
            if self.rect.y - selectplayer.rect.y > 10:
                self.rect.y -= 4
            elif self.rect.y - selectplayer.rect.y < - 5:
                self.rect.y += 4

    def update(self):
        self.rect.x-=self.vel_x
            #Mov diagonal

#PRUEBAS
'''
if __name__ == '__main__':
    pygame.init()
    pantalla=pygame.display.set_mode([ANCHO, ALTO])  #Crea la ventana
    todos=pygame.sprite.Group()
    matrizTurret=recortarTorr('torreta.png')
    tor=Turret(matrizTurret)
    todos.add(tor)


    print 'Funciona'
    fin=False
    reloj=pygame.time.Clock()



    while not fin:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                fin=True

        todos.update()
        pantalla.fill([0,0,0])
        todos.draw(pantalla)


        pygame.display.flip()
        reloj.tick(20)
'''
