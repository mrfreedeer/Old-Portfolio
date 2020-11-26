import pygame
import random
import math
random.seed(pygame.time.get_ticks())

sword=pygame.mixer.Sound('sword.ogg')
scream=pygame.mixer.Sound('scream.ogg')
channel7 = pygame.mixer.Channel(6)

def recortarBoss(archivo):
    fondo=pygame.image.load(archivo)
    infoFondo=fondo.get_rect()
    matriz=[]
    idleR=[]
    idleL=[]
    walkR=[]
    walkL=[]
    attack1R=[]
    attack1L=[]
    dieR=[]
    dieL=[]




    idle=[[19, 9, 55, 77], [108, 9, 55, 77], [202, 9, 55, 77]]

    walkRight=[[14, 183, 73, 79] , [98, 183, 73, 79] , [193, 183, 73, 79] , [286, 183, 73, 79] , [374, 183, 73, 79] ,[461, 183, 73, 79] ]

    attack1=[[10,629,82,79], [95,629,82,79], [187,629,82,79], [265,629,82,79], [366,629,82,79], [454,629,82,79]]

    die=[[274, 361, 84, 75], [364, 361, 84, 75], [454, 361, 84, 75]]


    #Idle R-L
    for x in range(3):
        cuadro=fondo.subsurface(idle[x])
        cuadro=pygame.transform.scale(cuadro, (100, 125))
        cuadro2=pygame.transform.flip(cuadro, True, False)
        cuadro2=pygame.transform.scale(cuadro2, (100, 125))
        idleR.append(cuadro)
        idleL.append(cuadro2)

    #Walk R-L
    for x in range(6):
        cuadro=fondo.subsurface(walkRight[x])
        cuadro=pygame.transform.scale(cuadro, (100, 125))
        cuadro2=pygame.transform.flip(cuadro, True, False)
        cuadro2=pygame.transform.scale(cuadro2, (100, 125))
        walkR.append(cuadro)
        walkL.append(cuadro2)

    #Attack 1 R-L
    for x in range(6):
        cuadro=fondo.subsurface(attack1[x])
        cuadro=pygame.transform.scale(cuadro, (100, 125))
        cuadro2=pygame.transform.flip(cuadro, True, False)
        cuadro2=pygame.transform.scale(cuadro2, (100, 125))
        attack1R.append(cuadro)
        attack1L.append(cuadro2)

    #Die 1 R-L
    for x in range(3):
        cuadro=fondo.subsurface(die[x])
        cuadro=pygame.transform.scale(cuadro, (100, 125))
        cuadro2=pygame.transform.flip(cuadro, True, False)
        cuadro2=pygame.transform.scale(cuadro2, (100, 125))
        dieR.append(cuadro)
        dieL.append(cuadro2)


    return idleR, idleL, walkR, walkL, attack1R, attack1L, dieR, dieL

class Oniwa(pygame.sprite.Sprite):
    def __init__(self, matriz):
        pygame.sprite.Sprite.__init__(self)
        self.f=matriz
        self.image=self.f[0][0]
        self.rect=self.image.get_rect()
        self.indice=0
        self.rect.x=900
        self.rect.y=500
        self.accion=0
        self.dir = 'R'
        self._health = 12000
        self.finished = False
        self.canDie = False
        self.prevkey = None
        self.vel_y = 0
        self.vel_x = 0
        self.vel_x_value = 10
        self.vel_y_value = 6
        self.moverange = 50
        self.movetime = random.randrange(0,100)

    def getHealth(self):
        return self._health

    def getSlope(self, posJugador):
        point1 = [self.rect.x, self.rect.y]
        if self.rect.x == posJugador[0]:
            return False
        m = float(posJugador[1] -  point1[1])/(posJugador[0] - point1[0])
        b = posJugador[1] - m*posJugador[0]

        return [m, b]
    def isAttacking(self):
        if self.prevkey in ['AL', 'AR']:
            return True
        else:
            return False
    def AImove(self, jugador1, jugador2 = None, noplayers = 1):
        if self.accion not in[6,7]:
            self.movetime -= 1
            if self.movetime <= -50:
                self.movetime = random.randrange(0,50)
                self.move('I')
            if self.movetime <= 0:
                if noplayers == 1:
                    selectplayer = jugador1
                else:
                    distanceplayer1 = math.fabs(jugador1.rect.x-self.rect.x)+math.fabs(jugador1.rect.y-self.rect.y)
                    distanceplayer2 = math.fabs(jugador2.rect.x-self.rect.x)+math.fabs(jugador2.rect.y-self.rect.y)
                    if distanceplayer1 > distanceplayer2:
                        selectplayer = jugador2
                    else:
                        selectplayer = jugador1
                if math.fabs(selectplayer.rect.x - self.rect.x) <= self.moverange and math.fabs(selectplayer.rect.y- self.rect.y) <= self.moverange/4:
                    if selectplayer.rect.x - self.rect.x > 0:
                        self.move('AR')
                    else:
                        self.move('AL')
                else:
                    movedir = random.randrange(0,2)
                    discardedy = False
                    if movedir:
                        if selectplayer.rect.y - self.rect.y > self.moverange/4:
                            self.vel_y = self.vel_y_value
                            if selectplayer.rect.x - self.rect.x > 0:
                                self.move('R')
                            else:
                                self.move('L')
                        elif selectplayer.rect.y - self.rect.y < -self.moverange/4:
                            self.vel_y = -self.vel_y_value
                            if selectplayer.rect.x - self.rect.x > 0:
                                self.move('R')
                            else:
                                self.move('L')
                        else:
                            discardedy = True
                    elif discardedy or movedir == 0:
                        if selectplayer.rect.x - self.rect.x > self.moverange:
                            self.vel_x = self.vel_x_value
                            if selectplayer.rect.x - self.rect.x > 0:
                                self.move('R')
                            else:
                                self.move('L')
                        elif selectplayer.rect.x - self.rect.x < -self.moverange:
                            self.vel_x = -self.vel_x_value
                            if selectplayer.rect.x - self.rect.x > 0:
                                self.move('R')
                            else:
                                self.move('L')
        random.seed(pygame.time.get_ticks())
    def die(self):
        if not self.accion in [6,7]:
            if self.dir=='R' or self.move=='R' or self.move=='AR' or self.move=='I':
                self.accion=6
                self.finished = False

            elif self.dir=='L' or self.move=='L' or self.move=='AL':
                self.accion=7
                self.finished = False
        else:
            pass

    def move(self, key):
        if (self.finished and self.prevkey in ['AL', 'AR']) or self.prevkey not in ['AL', 'AR'] :
            self.finished = False
            if key == 'R':
                self.accion = 2
            elif key == 'L':
                self.accion = 3
            elif key == 'AR':
                self.accion = 4
            elif key == 'AL':
                self.accion = 5
            elif key == 'I':
                self.accion = 0
            self.prevkey = key
            self.indice = 0
    def update(self):
        #Idle R
        if self.accion==0:
            self.image = self.f[self.accion][self.indice]
            self.indice += 1

            if self.indice > 2:
                self.indice=0
            self.vel_x = 0
            self.vel_y = 0
        #Idle L
        if self.accion==1:
            self.image = self.f[self.accion][self.indice]
            self.indice += 1

            if self.indice > 2:
                self.finished = True
                self.indice=0
            self.vel_x = 0
            self.vel_y = 0

        #Walk R
        if self.accion==2:
            if self.indice <=5:
                self.image = self.f[self.accion][self.indice]

                self.indice += 1
            #Es 7 normalmente
            if self.indice > 5:
                self.finished = True
                self.indice=0

        #Walk L
        if self.accion==3:
            if self.indice <=5:
                self.image = self.f[self.accion][self.indice]

                self.indice += 1
            #Es 7 normalmente
            if self.indice > 5:
                self.finished = True
                self.indice=0

        #1
        #Attack R
        if self.accion==4:
            channel7.play(sword)
            self.image = self.f[self.accion][self.indice]

            self.indice += 1

            if self.indice > 5:
                self.finished = True
                self.indice=0
            self.vel_x = 0
            self.vel_y = 0

        #Attack L
        if self.accion==5:
            channel7.play(sword)
            self.image = self.f[self.accion][self.indice]

            self.indice += 1

            if self.indice > 5:
                self.finished = True
                self.indice=0

            self.vel_x = 0
            self.vel_y = 0

        #Die R
        if self.accion==6:
            if self.indice <2:
                if self.indice==0:
                    channel7.play(scream)
                self.image = self.f[self.accion][self.indice]
                self.indice += 1

            if self.indice >= 2:
                self.indice = 0
                self.finished = True




            self.vel_x = 0
            self.vel_y = 0
        #Die L
        if self.accion==7:
            if self.indice <=2:
                if self.indice==0:
                    channel7.play(scream)
                self.image = self.f[self.accion][self.indice]

                self.indice += 1

            if self.indice >= 2:
                self.indice = 0
                self.finished = True

        if self.accion in [6,7] and self.finished:
            self.canDie = True



            self.vel_x = 0
            self.vel_y = 0
        self.rect.y += self.vel_y
        self.rect.x += self.vel_x



        #if self.rect.x + self.rect.width > RESOLUTION[0] - bglimit:
        #    self.rect.x = RESOLUTION[0] - bglimit - self.rect.width
        #elif self.rect.x < bglimit:
        #    self.rect.x = bglimit
