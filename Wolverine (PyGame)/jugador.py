import pygame
import math

pygame.init()
ALTO=1000
ANCHO=1000
limites=[10, 8, 11, 10, 8, 6, 9, 4, 12, 8, 8, 10, 9, 4, 7, 5, 2, 8, 9, 9, 9]
pygame.mixer.init(44100, -16, 2, 2048)
step=pygame.mixer.Sound('pasosJugador3.ogg')
step.set_volume(0.05)
step2=pygame.mixer.Sound('pasosJugador2.ogg')
step2.set_volume(0.05)
attack1=pygame.mixer.Sound('ataque1.ogg')
attack2=pygame.mixer.Sound('ataque2.ogg')
jump = pygame.mixer.Sound('jump.ogg')
screensize = pygame.display.Info()
RESOLUTION = [screensize.current_w, screensize.current_h]
bglimit = 10
#Funciones
'''
def recortarCara(archivo):
    fondo=pygame.image.load(archivo)
    infoFondo=fondo.get_rect()
    lista=[]
    cuadro=fondo.subsurface(5, 1628, 105, 105)
    #cuadro=pygame.transform.scale(cuadro, (95, 95))
    lista.append(cuadro)
    return lista
'''
def recortar(archivo):
    fondo=pygame.image.load(archivo)
    infoFondo=fondo.get_rect()
    matriz=[]
    idleR=[]
    idleL=[]
    walkR=[]
    walkL=[]
    jumpR=[]
    jumpL=[]
    attack1R=[]
    attack1L=[]
    attack2R=[]
    attack2L=[]

    idle=[[18,25,54,59], [93,25,54,59], [172,25,54,59]]

    #walkRight=[[11, 193, 59, 59], [174, 193, 49, 59], [89, 192, 59, 59], [249, 193, 59, 59], [323, 200, 56, 53], [402, 197, 56, 55]]
    #walkRight=[[11, 193, 59, 59], [89, 192, 59, 59], [249, 193, 59, 59], [323, 200, 56, 53], [402, 197, 56, 55]]
    walkRight=[[11, 193, 59, 59] , [172, 196, 51, 55], [249, 193, 59, 59], [323, 200, 56, 53], [402, 197, 56, 55],[16, 281, 51, 55], [91, 281, 51, 55]]

    '''          Se ancha                               Se ancha                             '''
    jump=[[178, 252, 40, 85], [244, 253, 56, 85], [331, 253, 40, 85], [391, 262, 66, 76]]


    attack1=[[245, 11, 60, 72], [323, 12, 60, 72], [385, 12, 77, 72]]

    attack2=[[242, 108, 63, 59], [313, 95, 73, 73], [397, 98, 54, 74]]

    #Idle R-L
    for x in range(3):
        cuadro=fondo.subsurface(idle[x])
        cuadro=pygame.transform.scale(cuadro, (125, 125))
        cuadro2=pygame.transform.flip(cuadro, True, False)
        cuadro2=pygame.transform.scale(cuadro2, (125, 125))
        idleR.append(cuadro)
        idleL.append(cuadro2)


    #Walk R-L
    for x in range(6):
        cuadro=fondo.subsurface(walkRight[x])
        cuadro=pygame.transform.scale(cuadro, (125, 125))
        cuadro2=pygame.transform.flip(cuadro, True, False)
        cuadro2=pygame.transform.scale(cuadro2, (125, 125))
        walkR.append(cuadro)
        walkL.append(cuadro2)

    #Jump R-L
    '''
    for x in range(4):
        cuadro=fondo.subsurface(jump[x])
        cuadro=pygame.transform.scale(cuadro, (100, 179))
        cuadro2=pygame.transform.flip(cuadro, True, False)
        cuadro2=pygame.transform.scale(cuadro2, (100, 179))
        jumpR.append(cuadro)
        jumpL.append(cuadro2)
    '''
    cuadro=fondo.subsurface(jump[0])
    cuadro=pygame.transform.scale(cuadro, (92, 179))
    cuadro2=pygame.transform.flip(cuadro, True, False)
    cuadro2=pygame.transform.scale(cuadro2, (92, 179))
    jumpR.append(cuadro)
    jumpL.append(cuadro2)

    cuadro=fondo.subsurface(jump[1])
    cuadro=pygame.transform.scale(cuadro, (120, 179))
    cuadro2=pygame.transform.flip(cuadro, True, False)
    cuadro2=pygame.transform.scale(cuadro2, (120, 179))
    jumpR.append(cuadro)
    jumpL.append(cuadro2)

    cuadro=fondo.subsurface(jump[2])
    cuadro=pygame.transform.scale(cuadro, (92, 179))
    cuadro2=pygame.transform.flip(cuadro, True, False)
    cuadro2=pygame.transform.scale(cuadro2, (92, 179))
    jumpR.append(cuadro)
    jumpL.append(cuadro2)

    cuadro=fondo.subsurface(jump[3])
    cuadro=pygame.transform.scale(cuadro, (152, 160))
    cuadro2=pygame.transform.flip(cuadro, True, False)
    cuadro2=pygame.transform.scale(cuadro2, (152, 160))
    jumpR.append(cuadro)
    jumpL.append(cuadro2)

    #Attack 1 R-L
    for x in range(3):
        cuadro=fondo.subsurface(attack1[x])
        cuadro=pygame.transform.scale(cuadro, (125, 125))
        cuadro2=pygame.transform.flip(cuadro, True, False)
        cuadro2=pygame.transform.scale(cuadro2, (125, 125))
        attack1R.append(cuadro)
        attack1L.append(cuadro2)

    #Attack 2 R-L
    for x in range(3):
        cuadro=fondo.subsurface(attack2[x])
        cuadro=pygame.transform.scale(cuadro, (125, 125))
        cuadro2=pygame.transform.flip(cuadro, True, False)
        cuadro2=pygame.transform.scale(cuadro2, (125, 125))
        attack2R.append(cuadro)
        attack2L.append(cuadro2)

    return idleR, idleL, walkR, walkL, jumpR, jumpL, attack1R, attack1L, attack2R, attack2L

#Clases
class Jugador(pygame.sprite.Sprite):
    def __init__(self, matriz, validmoves):
        pygame.sprite.Sprite.__init__(self)
        self.f=matriz
        self.image=self.f[0][0]
        self.rect=self.image.get_rect()
        self.indice=0
        self.rect.x=50
        self.rect.y=450
        self.vel_x=0
        self.vel_y=0
        self.vel_x_value = 36
        self.vel_y_value = 15
        self.damage1 = 10
        self.damage2 = 15
        self.vel_multiplier = 1
        self.damagedealtmultiplier = 1
        self.damageinflictedmultiplier = 1
        self.accion=0
        self.salto=False
        self.dir = 'R'
        self._health = 100
        self.finished = False
        self.updatemove = False
        self.still = True
        self.prevkey = None
        self.interrupt = False
        self.score = 0
        self.validmoves = validmoves
        self.currentkey = None
        self.startjump = -1
        self.onplatform = False
        self.interruptjump = False
    def printstats(self):
        print "--------------Stats-------------"
        print "Vel: ", self.vel_multiplier
        print "Dmgdealt: ", self.damagedealtmultiplier
        print "Dmginflic: ", self.damageinflictedmultiplier
    def getHealth(self):
        if self._health < 0:
            self._health = 0
        return self._health
    def dealDamage(self,damage):
        self._health -= damage * self.damagedealtmultiplier
    def inflictDamage(self, enemy):
        if math.fabs(enemy.rect.y - self.rect.y) <= self.rect.height/2:
            if self.prevkey == self.validmoves[4]:
                return self.damage1 * self.damageinflictedmultiplier
            elif self.prevkey == self.validmoves[5]:
                return self.damage2 * self.damageinflictedmultiplier
            else:
                return 0
        else:
            return 0
    def gravedad(self, v):
        if self.vel_y==0:
            self.vel_y=1
        else:
            self.vel_y+=v
    def stopjump(self):
        self.interruptjump = True
        self.soltartecla()

    def move(self, key):

        checklist = self.validmoves[0:4]
        if self.still and self.finished:
            self.finished = False
            self.updatemove = False
            self.still = False
            if key == self.validmoves[0]:
                self.derecha()
            elif key == self.validmoves[1]:
                self.izquierda()
            elif key == self.validmoves[2]:
                self.arriba()
            elif key == self.validmoves[3]:
                self.abajo()
            elif key == self.validmoves[4]:
                self.ataquefuerte()
            elif key == self.validmoves[5]:
                self.ataquedebil()
            elif key == self.validmoves[6]:
                self.saltar()
        else:
            if self.accion in [4,5]:
                if key == self.validmoves[0]:
                    self.vel_x= self.vel_x_value * self.vel_multiplier
                    self.dir = 'R'
                    self.indice = 0
                    self.accion = 4
                elif key == self.validmoves[1]:
                    self.dir = 'L'
                    self.indice = 0
                    self.accion = 5
                    self.vel_x= -self.vel_x_value * self.vel_multiplier
                self.currentkey = key
            elif key != self.prevkey:
                self.interrupt = True
                self.soltartecla()
                self.prevkey = key
                self.move(key)


        self.prevkey = key

    def saltar(self):
        self.indice = 0
        if self.dir == 'R':
            self.accion = 4
        else:
            self.accion = 5
        self.vel_y = -40
    def update(self):
        '''
        if self.salto:
            self.vel_y=-15
            self.salto=False
        '''
        #Idle R
        if self.accion==0:
            self.image = self.f[self.accion][self.indice]
            self.indice += 1

            if self.indice > 2:
                self.indice=0
                self.finished = True
        #Idle L
        if self.accion==1:
            self.image = self.f[self.accion][self.indice]
            self.indice += 1

            if self.indice > 2:
                self.indice=0
                self.finished = True
        #Walk R
        if self.accion==2:
            self.image = self.f[self.accion][self.indice]
            if self.indice==0:
                step.play()
            if self.indice==3:
                step.play()
            self.indice += 1

            if self.indice > 5:
                self.indice=0
                self.finished = True

        #Walk L
        if self.accion==3:
            self.image = self.f[self.accion][self.indice]
            if self.indice==0:
                step.play()
            if self.indice==3:
                step.play()
            self.indice += 1

            if self.indice > 5:
                self.indice=0
                self.finished = True

        #Jump R
        if self.accion==4:
            if self.indice <4:
                self.image = self.f[self.accion][self.indice]
                if self.indice in [0,1]:
                    jump.play()
                self.indice += 1

                if self.startjump == -1:
                    self.startjump = self.rect.bottom
            #Es 7 normalmente
            if self.indice == 3:
                self.image = self.f[self.accion][self.indice]

        #Jump L
        if self.accion==5:
            if self.indice <4:
                self.image = self.f[self.accion][self.indice]
                if self.indice in [0,1]:
                    jump.play()
                self.indice += 1
                if self.startjump == -1:
                    self.startjump = self.rect.bottom
            #Es 7 normalmente
            if self.indice == 3:
                self.image = self.f[self.accion][self.indice]

        #1
        #Attack R
        if self.accion==6:
            if self.indice <3:
                self.image = self.f[self.accion][self.indice]
                if self.indice==2:
                    attack1.play()
                self.indice += 1
            #Es 7 normalmente
            if self.indice > 2:
                self.indice=0
                self.finished = True

        #Attack L
        if self.accion==7:
            if self.indice <3:
                self.image = self.f[self.accion][self.indice]
                if self.indice==2:
                    attack1.play()
                self.indice += 1
            #Es 7 normalmente
            if self.indice > 2:
                self.indice=0
                self.finished = True
        #2
        #Attack R
        if self.accion==8:
            if self.indice <3:
                self.image = self.f[self.accion][self.indice]
                if self.indice==1:
                    attack2.play()
                self.indice += 1
            #Es 7 normalmente
            if self.indice > 2:
                self.indice=0
                self.finished = True

        #Attack L
        if self.accion==9:
            if self.indice <3:
                self.image = self.f[self.accion][self.indice]
                if self.indice==1:
                    attack2.play()
                self.indice += 1
            #Es 7 normalmente
            if self.indice > 2:
                self.indice=0
                self.finished = True
        self.rect.y += self.vel_y
        self.rect.x += self.vel_x

        if self.startjump != -1:
            if self.rect.bottom > self.startjump:
                self.vel_x = 0
                self.rect.bottom = self.startjump
                self.startjump = -1
                self.vel_y = 0
                self.finished = True
                if self.currentkey not in [pygame.K_LEFT, pygame.K_RIGHT]:
                    if self.dir=='L':
                        self.accion = 1
                    else:
                        self.accion = 0
                    self.indice = 0
                else:
                    self.currentkey = None
                    if self.dir=='L':
                        self.accion = 3
                        self.vel_x = -self.vel_x_value
                    else:
                        self.accion = 2
                        self.vel_x = self.vel_x_value
                    self.indice = 0
            else:
                self.gravedad(5)

        if self.rect.x + self.rect.width > RESOLUTION[0] - bglimit:
            self.rect.x = RESOLUTION[0] - bglimit - self.rect.width
        elif self.rect.x < bglimit:
            self.rect.x = bglimit
        if self.rect.y  + self.rect.height > RESOLUTION[1] - bglimit:
            self.rect.y = RESOLUTION[1] - bglimit- self.rect.height


        if self.updatemove:
            self.soltartecla()


    def derecha(self):
        if self.accion==4:
            pass
        else:
            self.indice=0
            self.vel_y=0
            self.salto=False
            self.dir='R'
            self.accion=2
            self.vel_x= self.vel_x_value * self.vel_multiplier
        '''
        if self.rect.x>=1050:
            self.rect.x=1050
            self.vel_x=0
        '''
    def izquierda(self):
        if self.accion==5:
            pass
        else:
            self.indice=0
            self.vel_y=0
            self.salto=False
            self.dir='L'
            self.accion=3
            self.vel_x=-self.vel_x_value * self.vel_multiplier

    def arriba(self):
        self.vel_y=- self.vel_y_value * self.vel_multiplier
        if self.dir=='R':
            self.indice=0
            self.accion=2
            self.vel_x=0
        else:
            self.indice=0
            self.accion=3
            self.vel_x=0

    def abajo(self):
        self.vel_y = self.vel_y_value * self.vel_multiplier
        if self.dir=='R':
            self.indice=0
            self.accion=2
            self.vel_x=0
        else:
            self.indice=0
            self.accion=3
            self.vel_x=0

    '''
    def saltar(self):
        self.salto=True
        self.indice=0
        self.rect.y+=-20
        if self.dir=='R':
            self.accion=4
        if self.dir=='L':
            self.accion=5
        self.salto=True
    '''
    def ataquedebil(self):
        self.indice=0
        if self.dir=='R':
            self.accion=6
        if self.dir=='L':
            self.accion=7

    def ataquefuerte(self):
        self.indice=0
        if self.dir=='R':
            self.accion=8
        if self.dir=='L':
            self.accion=9

    def soltartecla(self):
        if self.accion in [4,5]:
            self.currentkey = None
            if self.prevkey in self.validmoves[0:3]:
                self.vel_x = 0
        if self.prevkey in self.validmoves[0:4] and self.accion not in [4,5]:
            self.interrupt = True
        if ((self.finished and self.updatemove) or (self.interrupt and not self.onplatform)and self.accion not in [4,5]):
            self.indice=0
            if self.accion==2 or self.accion==3:
                if self.dir=='R':
                    self.accion=0
                if self.dir=='L':
                    self.accion=1
                self.vel_x=0
                self.vel_y=0

            if self.accion in [4,5,6,7,8,9]:
                if self.dir=='R':
                    self.accion=0
                if self.dir=='L':
                    self.accion=1
                self.vel_x=0
            self.updatemove = False
            self.prevkey = None
            self.interrupt = False
            self.finished = True
            self.still = True

        else:
            if self.accion not in [4,5]:
                self.updatemove = True
        if self.interruptjump:
            self.indice=0
            self.interruptjump = False
            if self.prevkey == None:
                if self.dir=='R':
                    self.accion=0
                if self.dir=='L':
                    self.accion=1
            else:
                if self.dir=='R':
                    self.accion=2
                if self.dir=='L':
                    self.accion=3

            self.vel_x=0
            self.updatemove = False
            self.prevkey = None
            self.interrupt = False
            self.finished = True
            self.still = True

    def resetValue(self,modid):
        if modid == 0:
            self.damagedealtmultiplier = 1
        elif modid == 1:
            self.damageinflictedmultiplier = 1
        elif modid == 2:
            self.damagedealtmultiplier = 1
        elif modid == 3:
            self.vel_multiplier = 1
    def dealtwithModifiers(self,modid):
        if modid == 0:
            self.damageinflictedmultiplier = 0.5
        elif modid == 1:
            if self.damageinflictedmultiplier == 0.5:
                self.damageinflictedmultiplier = 1
            else:
                self.damageinflictedmultiplier = 2
        elif modid == 2:
            self.damagedealtmultiplier =  2
        elif modid == 3:
            self.vel_multiplier = 2
        elif modid == 5:
            self._health += 20
        elif modid == 4:
            self._health += 50
        if self._health > 100:
            self._health = 100
