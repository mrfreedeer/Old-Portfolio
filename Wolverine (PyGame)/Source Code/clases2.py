import pygame
import random
import math

bite=pygame.mixer.Sound('bite.ogg')
cry=pygame.mixer.Sound('cry.ogg')

channel6 = pygame.mixer.Channel(5)
def recortarReptV2(archivo):
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




    idle=[[5, 51, 228, 174], [280, 51, 228, 174], [552, 51, 228, 174], [825, 51, 228, 174], [1091, 51, 228, 174]]

    walkRight=[[0, 321, 228, 174] , [294, 321, 228, 174] , [554, 321, 228, 174] , [816, 321, 228, 174] , [1092, 321, 228, 174] ,[1362, 321, 228, 174] ]

    attack1=[[0,605,228,180], [282,554,228,227], [535,554,228,227], [820,554,228,227], [1108,605,192,180]]

    die=[[262, 111, 55, 57], [328, 111, 67, 57], [404, 11 ,74, 57]]


    #Idle R-L
    for x in range(5):
        cuadro=fondo.subsurface(idle[x])
        #cuadro=pygame.transform.scale(cuadro, (100, 125))
        cuadro2=pygame.transform.flip(cuadro, True, False)
        #cuadro2=pygame.transform.scale(cuadro2, (100, 125))
        idleR.append(cuadro)
        idleL.append(cuadro2)

    #Walk R-L
    for x in range(6):
        cuadro=fondo.subsurface(walkRight[x])
        #cuadro=pygame.transform.scale(cuadro, (100, 125))
        cuadro2=pygame.transform.flip(cuadro, True, False)
        #cuadro2=pygame.transform.scale(cuadro2, (100, 125))
        walkR.append(cuadro)
        walkL.append(cuadro2)

    #Attack 1 R-L
    for x in range(5):
        cuadro=fondo.subsurface(attack1[x])
        #cuadro=pygame.transform.scale(cuadro, (100, 125))
        cuadro2=pygame.transform.flip(cuadro, True, False)
        #cuadro2=pygame.transform.scale(cuadro2, (100, 125))
        attack1R.append(cuadro)
        attack1L.append(cuadro2)

    #Die 1 R-L
    for x in range(3):
        cuadro=fondo.subsurface(die[x])
        #cuadro=pygame.transform.scale(cuadro, (100, 125))
        cuadro2=pygame.transform.flip(cuadro, True, False)
        #cuadro2=pygame.transform.scale(cuadro2, (100, 125))
        dieR.append(cuadro)
        dieL.append(cuadro2)


    return idleR, idleL, walkR, walkL, attack1R, attack1L, dieR, dieL


def recortarRept(max_x, max_y, archivo, vector):
    imagen=pygame.image.load(archivo)
    info=imagen.get_rect()
    an_imagen=info[2]
    al_imagen=info[3]
    an_image_corte= an_imagen/max_x
    al_image_corte= al_imagen/max_y
    mapa=[]
    for i in range(max_y):
        mapis=[]
        for j in range(vector[i]):
            cuadro=imagen.subsurface(j*an_image_corte, i*al_image_corte, an_image_corte, al_image_corte)
            mapis.append(cuadro)
        mapa.append(mapis)
    return mapa


class fondo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("stage11.png")
        self.rect=self.image.get_rect()
        self.rect.x=0
        self.rect.y=-50
        self.varx=0
        self.vary=0
        self.mov=True

    def update(self):
        self.rect.x=self.rect.x-self.varx
        self.rect.y=self.rect.y+self.vary

    def movefondo(self):
        self.rect.x=self.rect.x-self.varx



class jugador(pygame.sprite.Sprite):
    def __init__(self, matriz):
        pygame.sprite.Sprite.__init__(self)
        self.m=matriz
        self.image=self.m[0][0]
        self.rect=self.image.get_rect()
        self.varx=0
        self.vary=0
        self.j=0
        self.rect.x=300
        self.rect.y=250
        self.salud=100
        self.accion=0
        self.puntaje=0
        self.dir=True
        self.mov=False
        self.c=0
        self.cambiodir=0
        self.flag=True
        self.Tmuerte=5
        self.Tesperar=10
        self.sonido=pygame.mixer.Sound('golpes2.mp3')
        self.Tiempo=120


    def update(self):
        if self.dir:
            self.accion=self.accion
        else:
            if self.flag:
                self.accion=self.accion+self.cambiodir
                self.flag=False
        self.rect.x=self.rect.x+self.varx
        self.rect.y=self.rect.y+self.vary
        self.image=self.m[self.accion][self.j]
        self.j+=1
        if self.j>=len(self.m[self.accion]):
            self.j=0
            if self.dir:
                if not (self.accion==0) and self.mov:
                    self.accion=0
                    self.varx=0
            else:
                if not (self.accion==8) and self.mov:
                    self.accion=8
                    self.varx=0
        if self.salud<=0:
            self.Tmuerte-=1
        if self.Tesperar>0:
            self.Tesperar-=1

        if self.Tesperar==0:
            self.Tiempo-=1
            self.Tesperar=10


class barravida_enemigo(pygame.sprite.Sprite):
    def __init__ (self, vector, pos):
        pygame.sprite.Sprite.__init__(self)
        self.v=vector
        self.image=self.v[0][0]
        self.rect=self.image.get_rect()
        self.i=0
        self.varx=0
        self.rect.midbottom=pos
    def update(self, pos):
        self.rect.midbottom=pos

    def comoloquierollamar(self):
        self.i+=1
        if self.i>=4:
            self.i=4
        self.image=self.v[0][self.i]



class Reptil2(pygame.sprite.Sprite):
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
        self._health = 100
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

            if self.indice >= 4:
                self.indice=0
            self.vel_x = 0
            self.vel_y = 0
        #Idle L
        if self.accion==1:
            self.image = self.f[self.accion][self.indice]
            self.indice += 1

            if self.indice >= 4:
                self.finished = True
                self.indice=0
            self.vel_x = 0
            self.vel_y = 0

        #Walk R
        if self.accion==2:
            if self.indice <=5:
                self.image = self.f[self.accion][self.indice]
                '''
                if self.indice==0:
                    stepE.play()
                if self.indice==3:
                    stepE.play()
                '''
                self.indice += 1
            #Es 7 normalmente
            if self.indice > 5:
                self.finished = True
                self.indice=0

        #Walk L
        if self.accion==3:
            if self.indice <=5:
                self.image = self.f[self.accion][self.indice]
                '''
                if self.indice==0:
                    stepE.play()
                if self.indice==3:
                    stepE.play()
                '''
                self.indice += 1
            #Es 7 normalmente
            if self.indice > 5:
                self.finished = True
                self.indice=0

        #1
        #Attack R
        if self.accion==4:
            #if self.indice <=1:
            self.image = self.f[self.accion][self.indice]
            if self.indice==1:
                bite.play()
            self.indice += 1

            if self.indice >=4:
                self.finished = True
                self.indice=0
            self.vel_x = 0
            self.vel_y = 0

        #Attack L
        if self.accion==5:
            #if self.indice <=1:
            self.image = self.f[self.accion][self.indice]
            if self.indice==1:
                bite.play()
            self.indice += 1

            if self.indice >=4:
                self.finished = True
                self.indice=0

            self.vel_x = 0
            self.vel_y = 0

        #Die R
        if self.accion==6:
            if self.indice <2:
                if self.indice==0:
                    channel6.play(cry)
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
                    channel6.play(cry)
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



class reptiles(pygame.sprite.Sprite):
    def __init__(self, matriz, pos):
        pygame.sprite.Sprite.__init__(self)
        self.m=matriz
        self.image=self.m[0][0]
        self.rect=self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]
        self.varx=0
        self.vary=0
        self.distancia=0
        self.i=0
        self.golpe=False
        self.accion=0
        self.mov=True
        #self.barra=barravida_enemigo(vector, self.rect.midtop)
        #groupbarras.add(self.barra)
        self.derecha=True
        self.izquierda=False
        self.Tespera=random.randrange(100,200)
        self.donacion=random.randrange(-5,10)
        self._health = 100
        self.Tmuerte=5
        '''
        self.f=matriz
        self.image=self.f[0][0]
        self.rect=self.image.get_rect()
        self.indice=0
        self.rect.x=900
        self.rect.y=500
        self.accion=0
        self.dir = 'R'
        self._health = 100
        self.finished = False
        self.canDie = False
        self.prevkey = None
        self.vel_y = 0
        self.vel_x = 0
        self.vel_x_value = 10
        self.vel_y_value = 6
        self.moverange = 50
        self.movetime = random.randrange(0,100)
        '''

    def update(self):
        self.rect.x=self.rect.x+self.varx
        self.rect.y=self.rect.y+self.vary
        #self.barra.update(self.rect.midtop)
        self.image=self.m[self.accion][self.i]
        self.i+=1
        if(self.Tespera>0):
            self.Tespera-=1
        if self.i>=len(self.m[self.accion]):
            self.i=0
            if self.derecha:
                self.i=0
                self.accion=0
                self.varx=0
            if self.izquierda:
                self.i=0
                self.accion=5
                self.varx=0
        if self._health<=0:
            self.Tmuerte-=1


    def left(self):
        self.izquierda=True
        self.derecha=False
        self.accion=6
        self.varx=-10


    def right(self):
        self.derecha=True
        self.izquierda=False
        self.accion=1
        self.varx=10

    def golpear(self):
        if self.derecha:
                if(self.Tespera<=0):
                    self.accion=2
                    self.golpe=True
                    self.Tespera=random.randrange(100,200)
                    self.varx=0
                    self.i=0

        if self.izquierda:
                if(self.Tespera<=0):
                    self.accion=7
                    self.golpe=True
                    self.Tespera=random.randrange(100,200)
                    self.varx=0
                    self.i=0



channel6 = pygame.mixer.Channel(5)


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




    idle=[[5, 51, 228, 174], [280, 51, 228, 174], [552, 51, 228, 174], [825, 51, 228, 174], [1091, 51, 228, 174]]

    walkRight=[[0, 321, 228, 174] , [294, 321, 228, 174] , [554, 321, 228, 174] , [816, 321, 228, 174] , [1092, 321, 228, 174] ,[1362, 321, 228, 174] ]

    attack1=[[0,605,228,180], [282,554,228,227], [535,554,228,227], [820,554,228,227], [1108,605,192,180]]

    die=[[262, 111, 55, 57], [328, 111, 67, 57], [404, 11 ,74, 57]]  #el tamaño del boss es de 90x90 


    #Idle R-L
    for x in range(5):
        cuadro=fondo.subsurface(idle[x])
        #cuadro=pygame.transform.scale(cuadro, (100, 125))
        cuadro2=pygame.transform.flip(cuadro, True, False)
        #cuadro2=pygame.transform.scale(cuadro2, (100, 125))
        idleR.append(cuadro)
        idleL.append(cuadro2)

    #Walk R-L
    for x in range(6):
        cuadro=fondo.subsurface(walkRight[x])
        #cuadro=pygame.transform.scale(cuadro, (100, 125))
        cuadro2=pygame.transform.flip(cuadro, True, False)
        #cuadro2=pygame.transform.scale(cuadro2, (100, 125))
        walkR.append(cuadro)
        walkL.append(cuadro2)

    #Attack 1 R-L
    for x in range(5):
        cuadro=fondo.subsurface(attack1[x])
        #cuadro=pygame.transform.scale(cuadro, (100, 125))
        cuadro2=pygame.transform.flip(cuadro, True, False)
        #cuadro2=pygame.transform.scale(cuadro2, (100, 125))
        attack1R.append(cuadro)
        attack1L.append(cuadro2)

    #Die 1 R-L
    for x in range(3):
        cuadro=fondo.subsurface(die[x])
        #cuadro=pygame.transform.scale(cuadro, (100, 125))
        cuadro2=pygame.transform.flip(cuadro, True, False)
        #cuadro2=pygame.transform.scale(cuadro2, (100, 125))
        dieR.append(cuadro)
        dieL.append(cuadro2)


    return idleR, idleL, walkR, walkL, attack1R, attack1L, dieR, dieL

class Boss(pygame.sprite.Sprite):
    def __init__(self, matriz, pos):
        pygame.sprite.Sprite.__init__(self)
        self.m=matriz
        self.image=self.m[0][0]
        self.rect=self.image.get_rect()
        self._health = 100
        self.rect.x=pos[0]
        self.rect.y=pos[1]
	    self.varx=0
        self.vary=0
        self.distancia=0
        self.i=0
        self.golpe=False
        self.golpekatana=False
        self.golpeshuriken=False
        self.accion=0
        self.mov=True
        self.derecha=True
        self.izquierda=False
        self.Tespera=random.randrange(100,200)
        self.Tesperakatana=random.randrange(300,350)
        self.Tesperashuriken=random.randrange(400,450)
        self.salud=100
        self.Tmuerte=5

    def update(self):
		self.rect.x=self.rect.x+self.varx
		self.rect.y=self.rect.y+self.vary
        self.barra.update(self.rect.midtop)
		self.image=self.m[self.accion][self.i]
        self.i+=1
		if(self.Tespera>0):
			self.Tespera-=1
		if self.i>=len(self.m[self.accion]):
			self.i=0
	    if self.derecha:
			self.i=0
		    self.accion=0
			self.varx=0
		if self.izquierda:
		    self.i=0
			self.accion=9
			self.varx=0
		if self.salud<=0:
			self.Tmuerte-=1
            
            
	def left(self):
		self.izquierda=True
		self.derecha=False
		self.accion=6
        self.varx=-10
            
            
	def right(self):
		self.derecha=True
		self.izquierda=False
		self.accion=1
        self.varx=10
            
    def golpear(self):
		if self.derecha:
			if(self.Tespera<=0):
				self.accion=3
				self.golpe=True
				self.Tespera=random.randrange(100,200)
				self.varx=0
				self.i=0
            
        if self.izquierda:
			if(self.Tespera<=0):
				self.accion=12
				self.golpe=True
				self.Tespera=random.randrange(100,200)
				self.varx=0
				self.i=0
            
	def acercar(self):
		if self.derecha:
			if(self.Tespera<=0):
				self.accion=2
				self.varx=10
                self.i=0
            
		if self.izquierda:
			if(self.Tespera<=0):
				self.accion=11
				self.varx=-10
				self.i=0
            
    def correr(self):
		if self.derecha:
			if(self.Tespera<=0):
				self.accion=5
				self.varx=20
				self.i=0
            
		if self.izquierda:
			if(self.Tespera<=0):
				self.accion=14
				self.varx=-20
				self.i=0
            
    """def salto(self):
                    if self.derecha:
                            if(self.Tespera<=0):
                                self.accion=6
                                #self.golpe=True
                                #self.Tespera=random.randrange(100,200)
                                self.varx=0
                                self.i=0

                    if self.izquierda:
                            if(self.Tespera<=0):
                                self.accion=15
                                #self.golpe=True
                                #self.Tespera=random.randrange(100,200)
                                self.varx=0 #las acciones son en base a los sprites del boss y pues asi yo manejaba la derecha e izquierda
                                #si algo lo acomodan a como uds lo hacen... alejo para que acomode el salto tal como el wolverine
                                self.i=0"""


    def ataquekatana(self):
        if self.derecha:
                if(self.Tesperakatana<=0):
                    self.accion=7
                    self.golpekatana=True
                    self.Tesperakatana=random.randrange(100,200)
                    self.varx=0
                    self.i=0

        if self.izquierda:
                if(self.Tesperakatana<=0):
                    self.accion=16
                    self.golpekatana=True
                    self.Tesperakatana=random.randrange(100,200)
                    self.varx=0
                    self.i=0

    def lanzashuriken(self):
        if self.derecha:
                if(self.Tesperashuriken<=0):
                    self.accion=1
                    self.golpeshuriken=True
                    self.Tesperashuriken=random.randrange(100,200)
                    self.varx=0
                    self.i=0

        if self.izquierda:
                if(self.Tesperashuriken<=0):
                    self.accion=10
                    self.golpeshuriken=True
                    self.Tesperashuriken=random.randrange(100,200)
                    self.varx=0
                    self.i=0

class ninjas(pygame.sprite.Sprite):
    def __init__(self, matriz, groupbarras, vector, pos):
        pygame.sprite.Sprite.__init__(self)
        self.m=matriz
        self.image=self.m[0][0]
        self.rect=self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]
        self.varx=0
        self.vary=0
        self.distancia=0
        self.i=0
        self.golpe=False
        self.accion=0
        self.mov=True
        self.barra=barravida_enemigo(vector, self.rect.midtop)
        groupbarras.add(self.barra)
        self.derecha=True
        self.izquierda=False
        self.Tespera=random.randrange(300,400)
        self.donacion=random.randrange(-10,10)
        self.salud=100
        self.Tmuerte= 5

    def update(self):
        self.rect.x=self.rect.x+self.varx
        self.rect.y=self.rect.y+self.vary
        print self.accion, self.i, 'ninjas'
        self.image=self.m[self.accion][self.i]
        self.barra.update(self.rect.midtop)
        self.i+=1
        if(self.Tespera>0):
            self.Tespera-=1
        if self.i>=len(self.m[self.accion]):
            self.i=0
            if self.derecha:
                self.i=0
                self.accion=0
                self.varx=0
            if self.izquierda:
                self.i=0
                self.accion=5
                self.varx=0
        if self.salud<=0:
            self.Tmuerte-=1

    def left(self):
        self.izquierda=True
        self.derecha=False
        self.accion=6
        self.varx=-10


    def right(self):
        self.izquierda=False
        self.accion=1
        self.derecha=True
        self.varx=10

    def golpear(self):
        if self.derecha:
                if(self.Tespera<=0):
                    self.i=0
                    self.accion=4
                    self.golpe=True
                    self.Tespera=random.randrange(300,400)
                    self.varx=0
        if self.izquierda:
                if(self.Tespera<=0):
                    self.i=0
                    self.accion=9
                    self.golpe=True
                    self.Tespera=random.randrange(300,400)
                    self.varx=0


class enemigas(pygame.sprite.Sprite):
    def __init__(self, matriz, groupbarras, vector, pos):
        pygame.sprite.Sprite.__init__(self)
        self.m=matriz
        self.image=self.m[0][0]
        self.rect=self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]
        self.varx=0
        self.vary=0
        self.distancia=0
        self.i=0
        self.golpe=False
        self.accion=0
        self.mov=True
        self.barra=barravida_enemigo(vector, self.rect.midtop)
        groupbarras.add(self.barra)
        self.derecha=True
        self.izquierda=False
        self.Tespera=random.randrange(300,400)
        self.donacion=random.randrange(-10,10)
        self.salud=100
        self.Tmuerte=5

    def update(self):
        self.rect.x=self.rect.x+self.varx
        self.rect.y=self.rect.y+self.vary
        self.barra.update(self.rect.midtop)
        print self.accion, self.i
        self.image=self.m[self.accion][self.i]
        self.i+=1
        if(self.Tespera>0):
            self.Tespera-=1
        if self.i>=len(self.m[self.accion]):
            self.i=0
            if self.derecha:
                self.i=0
                self.accion=0
                self.varx=0
            if self.izquierda:
                self.i=0
                self.accion=4
                self.varx=0
        if self.salud<=0:
            self.Tmuerte-=1

    def left(self):
        self.izquierda=True
        self.derecha=False
        self.accion=5
        self.varx=-10


    def right(self):
        self.izquierda=False
        self.accion=1
        self.derecha=True
        self.varx=10

    def golpear(self):
        if self.derecha:
                if(self.Tespera<=0):
                    self.i=0
                    self.accion=2
                    self.golpe=True
                    self.Tespera=random.randrange(300,400)
                    self.varx=0
        if self.izquierda:
                if(self.Tespera<=0):
                    self.i=0
                    self.accion=6
                    self.golpe=True
                    self.Tespera=random.randrange(300,400)
                    self.varx=0


"""class colega(pygame.sprite.Sprite):
    def __init__(self, matriz):
        pygame.sprite.Sprite.__init__(self)
        self.m=matriz
        self.image=self.m[0][0]
        self.rect=self.image.get_rect()
        self.rect.x=50
        self.rect.y=350
        self.varx=0
        self.vary=0
        self.distancia=0
        self.i=0
        self.golpe=False
        self.accion=0
        self.mov=True
        self.derecha=True
        self.izquierda=False
        self.Tespera=random.randrange(0,40)
        self.salud=100
        self.Tmuerte=5

    def update(self):
        self.rect.x=self.rect.x+self.varx
        self.rect.y=self.rect.y+self.vary
        self.image=self.m[self.accion][self.i]
        self.i+=1
        if(self.Tespera>0):
            self.Tespera-=1
        if self.i>=len(self.m[self.accion]):
            self.i=0
            if self.derecha:
                self.i=0
                self.accion=0
                self.varx=0
            if self.izquierda:
                self.i=0
                self.accion=5
                self.varx=0
        if self.salud<=0:
            self.Tmuerte-=1

    def left(self):
        self.izquierda=True
        self.derecha=False
        self.accion=10
        self.varx=-10


    def right(self):
        self.derecha=True
        self.izquierda=False
        self.accion=2
        self.varx=10

    def golpear(self):
        if self.derecha:
                if(self.Tespera<=0):
                    self.golpe=True
                    self.accion=4
                    self.Tespera=random.randrange(0,40)
                    self.varx=0
                    self.i=0

        if self.izquierda:
                if(self.Tespera<=0):
                    self.golpe=True
                    self.accion=12
                    self.Tespera=random.randrange(0,40)
                    self.varx=0
                    self.i=0

    def patada(self):
        if self.golpe:
            if self.derecha:
                if(self.Tespera<=0):
                    self.golpe=True
                    self.accion=5
                    self.Tespera=random.randrange(0,40)
                    self.varx=0
                    self.i=0

            if self.izquierda:
                if(self.Tespera<=0):
                    self.golpe=True
                    self.accion=13
                    self.Tespera=random.randrange(0,40)
                    self.varx=0
                    self.i=0
        self.golpe=False
"""

class helado(pygame.sprite.Sprite):
    def __init__ (self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("helado2.png")
        self.rect=self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]
        self.Ttime=100
        self.id=1
        self.sonido=pygame.mixer.Sound('obtencion.ogg')
        self.varx=0
    def update(self):
        if self.Ttime>0:
            self.Ttime-=1
        self.rect.x=self.rect.x+self.varx

    def desplazar(self):
        self.varx=-10

class pastel(pygame.sprite.Sprite):
    def __init__ (self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("pastel.png")
        self.rect=self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]
        self.Ttime=100
        self.id=0
        self.sonido=pygame.mixer.Sound('obtencion.ogg')
        self.varx=0
    def update(self):
        if self.Ttime>0:
            self.Ttime-=1
        self.rect.x=self.rect.x+self.varx

    def desplazar(self):
        self.varx=-10


class golosina(pygame.sprite.Sprite):
    def __init__ (self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("golosina.png")
        self.rect=self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]
        self.Ttime=100
        self.id=0
        self.varx=0
        self.sonido=pygame.mixer.Sound('obtencion.ogg')
    def update(self):
        if self.Ttime>0:
            self.Ttime-=1
        self.rect.x=self.rect.x+self.varx

    def desplazar(self):
        self.varx=-10



class fuego(pygame.sprite.Sprite):
    def __init__ (self, matriz):
        pygame.sprite.Sprite.__init__(self)
        self.m=matriz
        self.image=self.m[0][0]
        self.rect=self.image.get_rect()
        self.i=0
        self.rect.x=self.rect.x+300
        self.rect.y=self.rect.y-30
        self.retardo=20
    def update(self):
        if self.retardo<=0:
            self.i+=1
            if self.i<9:
                self.image=self.m[0][self.i]
            else:
                self.i=0
                self.image=self.m[0][0]
                self.retardo=20
        else:
            self.retardo-=1

class barravida_jugador(pygame.sprite.Sprite):
    def __init__ (self, vector):
        pygame.sprite.Sprite.__init__(self)
        self.v=vector
        self.image=self.v[0][0]
        self.rect=self.image.get_rect()
        self.i=0
        self.rect.x=100
        self.rect.y=30
    def update(self):
        pass
