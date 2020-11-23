import pygame
import math
import time
from maze import *
from ghost import *
from pygame.locals import *


red = (255,0,0)         #rgb(255,0,0)
green = (0,255,0)       #rgb(0,255,0)
blue = (0,0,255)        #rgb(0,0,255)
darkBlue = (0,0,128)    #rgb(0,0,128)
yellow =(255,255,51)    #rgb(255,255,51)
white = (255,255,255)   #rgb(255,255,255)
black = (0,0,0)         #rgb(0,0,0)
pink = (255,200,200)    #rgb(255,200,200)

def blink(pellet, pantalla,t):
        pantalla.blit(pygame.Surface((2*t/3, 2*t/3)), (pellet.rect.x, pellet.rect.y))
def check(before, jp):
    if jp.rect.x != before[0] or jp.rect.y != before[1]:
        return True
    else:
        return False



if __name__ == '__main__':
    pygame.init()   #Inicializa a Pygame
    pygame.font.init()
    pygame.mixer.init()

    turn = counter = time = slowturn = d = 0
    mazelocation = "/home/juan/Escritorio/Project/maze.txt"
    FREE = 200
    quit = collision = pendingturn = mouthchange = closed = move = False
    pause = pauseStart = habil =  redraweverything  = timefinish = blinker = hadpause = False
    start = True
    speed  = 1
    turnspeed = speed * 2
    timestart = True
    mantain = key = pygame.K_LEFT


    bob = Builder(mazelocation, FREE)
    pantalla = bob.buildscreen()      #Construye la pantalla
    clock = pygame.time.Clock()       #Reloj para acelerar el refresco de los gráficos
    pantalla.fill(black)              #Rellena la pantalla de negro
    m = bob.buildmaze()               #Construye el laberinto dejando un espacio
                                      #libre en la pantalla (FREE)
    m.draw()                          #Dibuja el laberinto
    mazesprites = m.getSprites()      #Obtiene los Sprites del laberinto:
                                      #Paredes, y lineas para interactuar
                                      #Con ellas (colisiones)
    playersize = bob.playersize()
    TILESIZE = bob.tilesize()
    DOCK = bob.dock()


    image = pygame.image.load('Powerpellet.png').convert_alpha()
    image = pygame.transform.scale(image,(int(2*TILESIZE/3),int(2*TILESIZE/3)))
    powerpellets = bob.buildpellets(image, m)


    font = pygame.font.Font('emulogic.ttf',int(bob.tilesize()/2) )
    pausefont = pygame.font.Font('emulogic.ttf', int(bob.tilesize()))

    scoreposy = DOCK[1] + (m._height * TILESIZE) + 10

    #Manejo de las imagenes de Pacman
    image = pygame.image.load('Pacmanc.png').convert_alpha()
    pacimages = []
    pacimages.append(pygame.transform.scale(image, (playersize,playersize)))
    image = pygame.image.load('Pacmanright.png').convert_alpha()
    while d < 4:
        pacimages.append(pygame.transform.scale(image, (playersize,playersize)))
        image =pygame.transform.rotate(image, 90)
        d += 1

    currentpac = pacimages[3]
    string = 'pdying'
    png = '.png'
    deathimages = []
    for h in range(1,8):
        image = pygame.image.load(string+str(h)+png).convert_alpha()
        deathimages.append(pygame.transform.scale(image,(playersize,playersize)))


    jp = bob.buildplayer(currentpac)
    playershadow = bob.buildplayer(currentpac)

    #Para dibujar un Sprite, se añade a un grupo de Sprites primer
    #El grupo puede tener un solo elemento (GroupSingle) o muchos
    #(Group)
    g = pygame.sprite.GroupSingle()
    g.add(jp)
    jp.updatemain(mantain)

    magic = bob.buildmagic()
    pacdotmagic = bob.builcpacdotmagic()
    pacdotmagic.fill(black)
    magic.fill(black)


    pacdots = bob.buildpacdots(m)
    score = bob.buildscore()
    pacdots.draw(pantalla)
    scbase = font.render("Score", True, (255,255,255))
    pantalla.blit(scbase, (DOCK[0],scoreposy))
    scorepts = font.render("0", True, (255,255,255))
    currentscore = prevscore = score.getScore()
    scoreposx = scbase.get_width() + DOCK[0] + 10
    pantalla.blit(scorepts, (scoreposx, scoreposy))

    pausepac = pygame.sprite.Group()
    pausetxt = pausefont.render("Pause", True, white)
    pausepos = (DOCK[0] + 6 * TILESIZE, DOCK[1] + 9 * TILESIZE)
    readytxt = font.render("READY!", True,yellow)
    gameovertxt = font.render("GAME OVER", True, red)
    powerpellets.draw(pantalla)

    fghost = GhostFactory()
    blinky = fghost.get_ghost(0, DOCK, TILESIZE, playersize, mazesprites)
    clyde = fghost.get_ghost(1, DOCK, TILESIZE, playersize, mazesprites)
    inky = fghost.get_ghost(2, DOCK, TILESIZE, playersize, mazesprites)
    pinky = fghost.get_ghost(3, DOCK, TILESIZE, playersize, mazesprites)

    g_ghost = pygame.sprite.Group()
    g_ghost.add(blinky)
    g_ghost.add(clyde)
    g_ghost.add(inky)
    g_ghost.add(pinky)
    d = 0
    before = [jp.rect.x, jp.rect.y]
    channel = pygame.mixer.Channel(0)
    dying = pygame.mixer.Sound('pacman_death.wav')
    chomp = pygame.mixer.Sound('pacman_chomp.wav')
    ready = pygame.mixer.Sound('pacman_beginning.wav')

    lives = pygame.sprite.Group()
    livesc = []
    image = pacimages[jp.Right()]
    image = pygame.transform.scale(image, (int(bob.tilesize()/2), int(bob.tilesize()/2)))
    for x in range(3):
        y = Life(image, scoreposx + (5 + x) * TILESIZE, scoreposy)
        lives.add(y)
        livesc.append(y)
    while True:
        if jp._lives == 0:
            pantalla.blit(pygame.Surface((bob.tilesize()*4, bob.tilesize())), (scoreposx + 5 * bob.tilesize(), scoreposy))
            pantalla.blit(pygame.Surface((TILESIZE * 5, TILESIZE)),(pausepos[0] , pausepos[1] + 2 * TILESIZE))
            pantalla.blit(gameovertxt, (pausepos[0] , pausepos[1] + 2 * TILESIZE))
            start = move = False
            lives.draw(pantalla)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
        else:
            if start:
                pantalla.blit(pygame.Surface((TILESIZE * 4, TILESIZE)),(pausepos[0] + TILESIZE , pausepos[1] + 2 * TILESIZE))
                pantalla.blit(readytxt, (pausepos[0] + TILESIZE , pausepos[1] + 2 * TILESIZE))
                channel.play(ready, 0)
                last_time = pygame.time.get_ticks()
                currentpac = pacimages[jp.Left()]
                keep = True
                jp.image = currentpac
                g.draw(pantalla)
                pantalla.blit(pygame.Surface((bob.tilesize()*4, bob.tilesize())), (scoreposx + 5 * bob.tilesize(), scoreposy))
                lives.draw(pantalla)
                pygame.display.flip()
                while keep:
                    diff_time_ms = pygame.time.get_ticks()
                    if diff_time_ms - last_time >= 5000:
                        keep = False

                redraweverything = True
                channel.play(chomp, -1)
                move = True

            if pause:
                if pauseStart:

                    pygame.mixer.pause()
                    pygame.draw.rect(pantalla, black, (jp.posx, jp.posy, playersize, playersize) )
                    pausepacplayer = bob.buildplayer(pacimages[0], jp.rect.x, jp.rect.y)
                    pausepac = pygame.sprite.Group()
                    pausepac.add(pausepacplayer)
                    pauseStart = False
                    pausepac.draw(pantalla)
                    pantalla.blit(pausetxt, pausepos)
                    redraweverything = True
                    pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                        quit = True

                    #Maneja cuando opriman un botón
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            pause = False
                            pygame.mixer.unpause()
                            channel.play(chomp,-1)

            else:
                if redraweverything:
                    pantalla.fill(black)
                    m.draw()
                    pacdots.draw(pantalla)
                    g.draw(pantalla)
                    pantalla.blit(scbase, (DOCK[0],scoreposy))
                    pantalla.blit(scorepts, (scoreposx, scoreposy))
                    DOCK[0] + 8 * TILESIZE, DOCK[1] + 8 * TILESIZE
                    pantalla.blit(pygame.Surface((5, m._height * TILESIZE)),(DOCK[0] - TILESIZE - 5, DOCK[1]))
                    pantalla.blit(pygame.Surface((5, m._height * TILESIZE)),(DOCK[0] + TILESIZE * (m._width + 1) + 5, DOCK[1]))
                    pantalla.blit(pygame.Surface((TILESIZE, 1)),(DOCK[0] + 8 * TILESIZE, DOCK[1] + 8 * TILESIZE))
                    redraweverything = False
                    powerpellets.draw(pantalla)
                    lives.draw(pantalla)




                #Dibuja un Rectangulo Negro encima del jugador para luego
                #Redibujarlo en otra posición
                pygame.draw.rect(pantalla, black, (jp.posx, jp.posy, playersize, playersize) )

                #Maneja los eventos de teclado y ventana
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                        quit = True

                    #Maneja cuando opriman un botón
                    if event.type == pygame.KEYDOWN:
                        if event.key != pygame.K_p:
                            key = event.key
                        playershadow.changedir(key,jp)
                        collision = False
                        if event.key == pygame.K_p:
                            pause = pauseStart = True

                        #Esta función (spritecollideany) retorna None cuando no hay
                        #colisiones, y un Sprite cuando Sí

                        ls = pygame.sprite.spritecollideany(playershadow, mazesprites, False)
                        if ls != None:
                            collision = True
                            if mantain != key:
                                pendingturn = True

                        #Los movimientos son sostenidos
                        #Es decir, se mantienen hasta que se cambie de movimiento
                        #En tal caso, cambia de movimiento en cuanto sea posible
                        if not collision:
                            mantain = key
                            pendingturn = False
                            jp.updatemain(mantain)
                            if key == pygame.K_RIGHT:
                                currentpac = pacimages[jp.Right()]
                            elif key == pygame.K_LEFT:
                                currentpac = pacimages[jp.Left()]
                            elif key == pygame.K_UP:
                                currentpac = pacimages[jp.Up()]
                            elif key == pygame.K_DOWN:
                                currentpac = pacimages[jp.Down()]


                #Manejo de movimiento de Pacman
                #Se mueve después de un número de turnos, para que
                #el movimiento no sea demasiado rápido

                if move and turn >= turnspeed or start:
                    if not check(before,jp):
                        pygame.mixer.pause()
                        hadpause = True
                    else:
                        if hadpause:
                            channel.play(chomp, -1)
                            hadpause = False
                    before[0] = jp.rect.x
                    before[1] = jp.rect.y
                    start = False
                    if (jp.posx < DOCK[0] + 2 * TILESIZE or jp.posx > DOCK[0] + (m.getWidth() - 4) * TILESIZE) and (jp.posy >= TILESIZE * 10 and jp.posy <= TILESIZE * 11):
                        realspeed = speed * 1.5
                    elif slowturn != 0:
                        pass
                    else:
                        realspeed = speed
                    jp.movement(mantain, realspeed)
                    if counter == 15:
                        mouthchange = True
                        closed = not closed
                        counter = 0
                    else:
                        counter += 1
                    turn = 0

                if not quit:
                    if mouthchange:
                        if closed:
                            jp.image = pacimages[0]
                        else:
                            jp.image = currentpac


                    #Se actualizan los grupos de Sprite y los Sprite
                    #para actualizar la posicion de los Sprites en la
                    #pantalla y redibujarlos
                    g.update(mazesprites, m.getWidth())
                    g_ghost.update(jp, mazesprites, m.getWidth())
                    jp.update(mazesprites, m.getWidth())
                    playershadow.changedir(key, jp)

                    #Se dibuja a Pacman
                    g.draw(pantalla)
                    g_ghost.draw(pantalla)

                    '''
                    for x in g_ghost:
                        #_______________________________# jp.crashed para colision con Jugador
                        if jp.crashed(x):
                            print("Fantasma Colisionó con Jugador")
                        #_______________________________# m.crashed para colision con laberinto
                        if m.crashed(x):
                            print("Fantasma Colisionó con laberinto")
                    '''
                    #Se encarga de cambiar de dirección en caso de
                    #que exista un movimiento pendiente
                    #que no se había podido realizar
                    #debido a colisiones con el laberinto
                    ls = pygame.sprite.spritecollideany(playershadow, mazesprites, False)
                    for x in g_ghost:
                        if jp.crashed(x):
                            channel.play(dying)
                            jp.die(deathimages, pantalla)
                            key = mantain = pygame.K_LEFT
                            move = False
                            start = keep = True
                            last_time = pygame.time.get_ticks()
                            currentpac = pacimages[jp.Left()]
                            l = livesc[len(livesc) - 1]
                            l.kill()
                            livesc.remove(l)
                            while keep:
                                diff_time_ms = pygame.time.get_ticks()
                                if diff_time_ms - last_time >= 1200:
                                    keep = False

                    if ls == None and pendingturn:
                        mantain = key
                        pendingturn = False
                        jp.updatemain(mantain)
                        if key == pygame.K_RIGHT:
                            currentpac = pacimages[jp.Right()]
                        elif key == pygame.K_LEFT:
                            currentpac = pacimages[jp.Left()]
                        elif key == pygame.K_UP:
                            currentpac = pacimages[jp.Up()]
                        elif key == pygame.K_DOWN:
                            currentpac = pacimages[jp.Down()]

                #Colisiones con los pacdots
                #En caso de colisionar con éstos,
                #Pacman se mueve más lento
                paccolide = pygame.sprite.spritecollide(playershadow, pacdots, False)
                powercollide = pygame.sprite.spritecollide(playershadow, powerpellets, False)


                if len(powercollide) != 0:
                    for o in powercollide:
                        pantalla.blit(pacdotmagic, (o.rect.x, o.rect.y))
                        o.kill()
                        score.bigconsume()
                    habil = True
                else:
                    if slowturn > turnspeed * 5:
                        slowturn = 0
                        habil = False

                if len(paccolide) != 0:
                    for o in paccolide:
                        pantalla.blit(pacdotmagic, (o.rect.x, o.rect.y))
                        o.kill()
                        score.consume()
                    habil = True
                else:
                    if slowturn > turnspeed * 5:
                        slowturn = 0
                        habil = False
                if slowturn != 0:
                    realspeed = speed * .3
                else:
                    realspeed = speed

                pantalla.blit(magic, (DOCK[0] + TILESIZE * (m.getWidth()) , DOCK[1] + 8 * TILESIZE))
                pantalla.blit(magic, (DOCK[0] - TILESIZE , DOCK[1] + 8 * TILESIZE))

                if d > (turnspeed * 30):
                    blinker = not blinker
                    d = 0
                    if blinker:
                        for x in powerpellets:
                            blink(x, pantalla, TILESIZE)
                    else:
                        powerpellets.draw(pantalla)


                pygame.display.flip()
                clock.tick(450)
                currentscore = score.getScore()
                if prevscore != currentscore:
                    scorepts = font.render(str(currentscore), True, white)
                    prevscore = currentscore
                    scoremagic = pygame.Surface((TILESIZE * 5, TILESIZE))
                    pantalla.blit(scoremagic, (scoreposx,scoreposy))
                    pantalla.blit(scorepts, (scoreposx, scoreposy))
                turn += 1
                d += 1
                if habil:
                    slowturn += 1


        #pos = pygame.mouse.get_pos()
        #print(pos)
