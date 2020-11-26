import pygame
import time
import random
import ConfigParser
from wolvbasics import *
from jugador import *
from enemigo import *
from operator import attrgetter
from torreta import *
from oniwa import *
#from clases2 import *

red = (255,0,0)         #rgb(255,0,0)
green = (0,255,0)       #rgb(0,255,0)
blue = (0,0,255)        #rgb(0,0,255)
darkBlue = (0,0,128)    #rgb(0,0,128)
yellow =(255,255,51)    #rgb(255,255,51)
white = (255,255,255)   #rgb(255,255,255)
black = (0,0,0)         #rgb(0,0,0)
pink = (255,200,200) #rgb(255,200,200)
posbg = [0, -840]

def distancia(p1,p2):
    return math.sqrt((p1.rect.x -p2.rect.x)**2 +(p1.rect.y-p2.rect.y)**2)

def acercar(dist, enemigo, jugador):
    #print jugador.rect.x, enemigo.rect.x
    if dist > 230 and not((enemigo.accion==3) or (enemigo.accion==8)):
        if jugador.rect.x < enemigo.rect.x and enemigo.rect.x > 50:
            enemigo.left()
        elif jugador.rect.x > enemigo.rect.x and enemigo.rect.x < ANCHO -50:
            enemigo.right()
    else:
        enemigo.golpear()

ohno=pygame.mixer.Sound('ohno.ogg')
ohnoFlag=False
beep=pygame.mixer.Sound('beep.ogg')
channel2=pygame.mixer.Channel(1)
powerup=pygame.mixer.Sound('powerup.ogg')
powerdown=pygame.mixer.Sound('powerdown.ogg')
pygame.mixer.music.load('titlescreen.ogg')
pygame.mixer.music.set_volume(0.5)
level1=pygame.mixer.Sound('level1.ogg')
shoot=pygame.mixer.Sound('shoot.ogg')
shoot.set_volume(0.6)
channel5 = pygame.mixer.Channel(4)
pygame.mixer.music.play()
channel1 = pygame.mixer.Channel(0)
channel1.set_volume(0)
channel1.play(level1, -1)
mouseonoption = -1

def printkey(key):
    if key == pygame.K_LEFT:
        print "Left"
    elif key == pygame.K_RIGHT:
        print "Right"
def readmapplatforms(level):
    interpreter = ConfigParser.ConfigParser()
    interpreter.read('map.map')
    map = interpreter.get(level,'map')
    map = map.split('\n')
    posx = 0
    posy = 0
    platforms = []
    for x in range(len(map)):
        posx = 0
        for y in map[x]:
            if y == 'p':
                platforms.append([posx,posy])
            posx += 75
        posy += 20
    return platforms

def readmapholes(level):
    interpreter = ConfigParser.ConfigParser()
    interpreter.read('map.map')
    map = interpreter.get(level,'map')
    map = map.split('\n')
    posx = 0
    posy = 0
    holes = []
    for x in range(len(map)):
        posx = 0
        for y in map[x]:
            if y == 'h':
                holes.append([posx,posy])
            posx += 75
        posy += 20
    return holes


def readmapspikes(level):
    interpreter = ConfigParser.ConfigParser()
    interpreter.read('map.map')
    map = interpreter.get(level,'map')
    map = map.split('\n')
    posx = 0
    posy = 0
    spikes = []
    for x in range(len(map)):
        posx = 0
        for y in map[x]:
            if y == 's':
                spikes.append([posx,posy])
            posx += 75
        posy += 20
    return spikes

def main():

    pygame.init()
    screensize = pygame.display.Info()
    pygame.font.init()
    bob = Builder(pygame.font.Font('WolverineFont.ttf', 40), pygame.font.Font('WolverineFont.ttf', 60), pygame.font.Font('WolverineFont.ttf', 15))
    screen = bob.buildscreen()
    menubckg = pygame.image.load('menu.png').convert_alpha()
    gamebckg = pygame.image.load('bg.png').convert_alpha()
    bginfo = [gamebckg.get_rect()[2],gamebckg.get_rect()[3]]
    fondo = pygame.image.load('fondo.png').convert_alpha()
    fondo2 = pygame.image.load('harbor.png').convert_alpha()
    fondo3 = pygame.image.load('laboratory.png').convert_alpha()
    fondo3 = pygame.transform.scale(fondo3, [2400, 1200])
    bginfo2 =[fondo2.get_rect()[2],fondo2.get_rect()[3]]
    player1 = pygame.image.load('jugador1.png').convert_alpha()
    player1=pygame.transform.scale(player1, (750, 350))
    player2 = pygame.image.load('jugador2.png').convert_alpha()
    player2=pygame.transform.scale(player2, (750, 350))
    im0 = pygame.image.load('instMods.png').convert_alpha()
    im0 = pygame.transform.scale(im0, (700, 125))
    bginfo3 =[fondo3.get_rect()[2],fondo3.get_rect()[3]]
    #EnemyFace
    bossface = pygame.image.load('bossface.png').convert_alpha()
    bossface = pygame.transform.scale(bossface, (40,40))
    enemyface3 = pygame.image.load('enemyFace3.png').convert_alpha()
    enemyface3 = pygame.transform.scale(enemyface3, (40,40))
    enemyface2 = pygame.image.load('enemyFace2.png').convert_alpha()
    enemyface2 = pygame.transform.scale(enemyface2, (40,40))
    enemyface1 = pygame.image.load('enemyFace1.png').convert_alpha()
    enemyface1 = pygame.transform.scale(enemyface1, (40,40))
    enemyface = pygame.image.load('enemyFace.png').convert_alpha()
    enemyface = pygame.transform.scale(enemyface, (40,40))
    wolvieface = pygame.image.load('WolverineFace.png').convert_alpha()
    wolvieface = pygame.transform.scale(wolvieface, (40,40))

    #Platform
    platform = pygame.image.load('platform.png').convert_alpha()
    platform = pygame.transform.scale(platform, (75,20))

    #Hole
    hole = pygame.image.load('vacio.png').convert_alpha()
    hole = pygame.transform.scale(hole, (75,100))

    spike = pygame.image.load('spikes.png').convert_alpha()
    spike = pygame.transform.scale(spike, (100,75))


    reptilsprites='reptilfinal.png'
    #reptilm=recortarRept(6, 10, reptilsprites, [5,6,5,6,6,5,6,5,6,6])
    mreptil=recortarReptV2(reptilsprites)

    #History
    level1History = pygame.image.load('Level1History.png').convert_alpha()
    level1History = pygame.transform.scale(level1History, [screensize.current_w, screensize.current_h-80])
    level2History = pygame.image.load('Level2History.png').convert_alpha()
    level2History = pygame.transform.scale(level2History, [screensize.current_w, screensize.current_h-80])
    bossLevelHistory = pygame.image.load('BossLevelHistory.png').convert_alpha()
    bossLevelHistory = pygame.transform.scale(bossLevelHistory, [screensize.current_w, screensize.current_h-80])
    winningHistory = pygame.image.load('WinningHistory.png').convert_alpha()
    winningHistory = pygame.transform.scale(winningHistory, [screensize.current_w, screensize.current_h-80])
    flagH1 = False
    flagH2 = False
    flagBoss = False
    flagEnd = False
    oniwaDead = False
    boss1='boss.png'
    bossrecorte=recortarRept(9,18, boss1, [4,8,6,6,6,6,8,6,9,4,8,6,6,6,6,8,6,9])
    mBoss=recortarBoss(boss1)

    menuoptions = ["Nivel 1", "Nivel 2", "Nivel Boss","Instrucciones", "Salir"]
    pauseoptions = ["Back to Menu"]
    storyoptions = ["Back to Menu", "Play"]

    pauserender = bob.buildtxtrender("PAUSE", 1, white)
    pauseoptionrenders = bob.buildtxtrenders(pauseoptions, 0, white)
    menurenders = bob.buildtxtrenders(menuoptions)
    WolverineTitle = bob.buildtxtrender("Wolverine", 1)
    end = False
    fac = Facade(screen, menurenders, WolverineTitle, [250,200], menubckg, [-550,0], wolvieface, enemyface, enemyface1, enemyface2, enemyface3, bossface)
    fac._screensize = bob.buildresolution()
    posbg[1] += fac._screensize[1]-200
    fac.posbg = posbg[:]
    fac.prevposbg = posbg[:]
    fac.defaultposbg = posbg[:]
    fac.posbgfixedy = 840
    fac.display_bkg()
    mouseclick = False
    fac.display_menu()
    fac.loadmodifiers('gamemodifiers.png', quantity=6)
    modi = 0
    storyrenders = bob.buildtxtrenders(storyoptions)
    fac.setPauserenders(pauseoptionrenders)
    fac.setStoryrenders(storyrenders)
    modifiers = pygame.sprite.Group()
    everyone = pygame.sprite.Group()
    whatevers = pygame.sprite.Group()
    bossG = pygame.sprite.Group()
    m = fac.getModifier(modi)
    modifiers.add(m)
    everyone.add(m)
    state = 'menu'
    backtomenured = bob.buildtxtrender("Back to Menu", 0, red)



    wolverine=pygame.image.load('wolverine_sprites.png').convert_alpha()
    infoWolverine=wolverine.get_rect()

    todos=pygame.sprite.Group()
    jugadores=pygame.sprite.Group()

    enemigos=pygame.sprite.Group()
    enemigos2=pygame.sprite.Group()

    enemigos2n=pygame.sprite.Group()
    enemigos2n2=pygame.sprite.Group()

    balas=pygame.sprite.Group()
    balasTorreta=pygame.sprite.Group()
    plataformas = pygame.sprite.Group()
    vacios = pygame.sprite.Group()
    pinchos = pygame.sprite.Group()

    matrizJugador=[]
    #matrizJugador2=[]
    matrizJugador=recortar('wolverine_sprites.png')
    matrizJugador2=recortar('wolverine_sprites2.png')
    matrizEnemigos1=recortarEne1('enemy.png')
    matrizEnemigos2=recortarEne2('enemigoMovil.png')
    matrizBala=recortarBala('lasers.png')
    matrizTorreta=recortarTorr('torreta.png')

    reloj=pygame.time.Clock()
    #Nivel 1
    generator1=True
    generator2=True
    numberOfMovingEnemies=4
    numberOfStillEnemies=2
    canGenerate=True
    allDead=False
    numberOfDeaths=0

    #Nivel 2
    generator21=4
    generator22=4
    numberOfMovingEnemies2=4
    numberOfStillEnemies2=2
    canGenerate2=True
    allDead2=False
    numberOfDeaths2=0

    inst=0

    #screen.blit(gamebckg, [0,0])
    pygame.draw.polygon(screen, [255,255,255], [[0,400], [ANCHO, 400]],2)
    pygame.display.flip()

    fin=False
    allowedmoves = [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN, pygame.K_k, pygame.K_j, pygame.K_SPACE]
    moves = []
    blink2 = False
    pausewidth = pauserender.get_width()/2
    pauseheight = pauserender.get_height()/2
    for x in pauseoptionrenders:
        pauseheight += x.get_height()/2 + 10
    pausepositions = []

    pausexpos = fac._screensize[0]/2
    pauseypos = fac._screensize[1]/2 - pauseheight
    xpos = pausexpos
    ypos = pauseypos + pauserender.get_height() + 10
    for x in pauseoptionrenders:
        pausepositions.append((pausexpos-x.get_width()/2, ypos))
        ypos += x.get_height() + 10
    fac.pausepositions = pausepositions
    blink = False
    blinkers = []
    blinkEnemy = False
    time = pygame.time.get_ticks()
    turn = False
    modlist = []
    playermodlist = {}
    turn2 = False
    random.seed(pygame.time.get_ticks())
    time2 = pygame.time.get_ticks()
    score = bob.buildscorerender("score")
    endscore = 18000
    genscore = 0
    winrender = bob.buildtxtrender("Congratulations", 1, white)
    loserender = bob.buildtxtrender("GAME OVER", 1, red)
    gameover = False
    while not end:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    mouseclick = True
            if event.type == pygame.MOUSEBUTTONUP:
                    mouseclick = False
            if state == 'menu':
                pygame.mixer.music.set_volume(0.3)
                channel1.set_volume(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        modi -= 1
                        blink = True
                        time = pygame.time.get_ticks()
                        lasttime = pygame.time.get_ticks()
                    if event.key == pygame.K_RIGHT:
                        modi += 1
                        blink = True
                        time = pygame.time.get_ticks()
                        lasttime = pygame.time.get_ticks()
                    if modi < 0:
                        modi = 5
                    elif modi > 5:
                        modi = 0
                    if modifiers:
                        for x in modifiers:
                            x.kill()
                    m = fac.getModifier(modi)
                    modifiers.add(m)
                    everyone.add(m)
            #Nivel 1
            elif state == menuoptions[0] or state == menuoptions[1] or state == menuoptions[2]:

                pygame.mixer.music.set_volume(0)
                channel1.set_volume(0.3)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        fac.pause = not fac.pause

                    if event.key in allowedmoves:
                        moves.insert(0,event.key)
                    if moves != []:
                        if not jugador.onplatform:
                            jugador.move(moves[0])
                        else:
                            if moves[0] == pygame.K_UP:
                                pass
                            else:
                                jugador.move(moves[0])

                if event.type == pygame.KEYUP:
                    if event.key in allowedmoves:
                        moves.remove(event.key)
                    jugador.soltartecla()
                    if moves != []:
                        jugador.move(moves[0])


        mousepos = pygame.mouse.get_pos()
        mouseonoption = fac.checkmouse(mousepos)
        if state == 'menu':
            if blink:
                if pygame.time.get_ticks()-lasttime >= 200:
                    turn = not turn
                    lasttime = pygame.time.get_ticks()
                    if turn:
                        m.kill()
                    else:
                        modifiers.add(m)
                        everyone.add(m)
                if pygame.time.get_ticks() - time >= 2000:
                    blink = False
                    modifiers.add(m)
                    everyone.add(m)

            if mouseonoption != -1 and mouseclick: #Detecting Option Clicked
                #print "Menu Option Clicked: ", menuoptions[mouseonoption]
                mouseclick = False

                if menuoptions[mouseonoption] == "Nivel 1":
                    state = 'Level1History'
                elif menuoptions[mouseonoption] == "Nivel 2":
                    state  = 'Level2History'
                elif menuoptions[mouseonoption] == "Nivel Boss":
                    state  = 'BossLevelHistory'
                else:
                    state = menuoptions[mouseonoption]
                if state == menuoptions[0]:
                    fac.setposbglevel1()
                elif state == menuoptions[1]:
                    fac.setposbglevel2()

                if mouseonoption == 0:
                    modwait = 15000
                else:
                    modwait = 10000
            if mouseonoption != -1 and mouseonoption not in fac.getTurned():
                #Turns blue the option the mouse is on
                txt = menuoptions[mouseonoption]
                fac.appendTurned(mouseonoption)
                newrender = bob.buildtxtrender(txt, 0, white)
                fac.popmenurenders(mouseonoption)
                fac.insertmenurenders(mouseonoption, newrender)
                beep.play()
            elif fac.getTurned() != [] and mouseonoption == -1:
                #Returns all text to normal colors
                fac.emptyTurned()
                fac.resetmenurenders()
            elif len(fac.getTurned()) > 1:
                fac.emptyTurned()
                fac.resetmenurenders()
                txt = menuoptions[mouseonoption]
                fac.appendTurned(mouseonoption)
                newrender = bob.buildtxtrender(txt, 0, white)
                fac.popmenurenders(mouseonoption)
                fac.insertmenurenders(mouseonoption, newrender)
            screen.fill(black)
            fac.display_bkg()
            fac.display_menu()
            mousepos = pygame.mouse.get_pos()

            everyone.draw(screen)
            #1 Player

            if state == menuoptions[0]:
                platforms = readmapplatforms('level1')
                for p in platforms:
                    x = Platform(platform)
                    plataformas.add(x)
                    x.rect.x = p[0]
                    x.rect.y = p[1]
                    todos.add(x)
                holes = readmapholes('level1')
                for h in holes:
                    x = Whatever(hole)
                    vacios.add(x)
                    whatevers.add(x)
                    x.rect.x = h[0]
                    x.rect.y = h[1]
                    todos.add(x)
                spikes = readmapspikes('level1')
                for s in spikes:
                    x = Whatever(spike)
                    pinchos.add(x)
                    whatevers.add(x)
                    x.rect.x = s[0]
                    x.rect.y = s[1]
                    todos.add(x)
                genscore=0
                jugador=Jugador(matrizJugador,allowedmoves)
                jugadores.add(jugador)
                todos.add(jugador)

            elif state == menuoptions[1]:
                platforms = readmapplatforms('level2')
                for p in platforms:
                    x = Platform(platform)
                    plataformas.add(x)
                    x.rect.x = p[0]
                    x.rect.y = p[1]
                    todos.add(x)
                holes = readmapholes('level2')
                for h in holes:
                    x = Whatever(hole)
                    vacios.add(x)
                    whatevers.add(x)
                    x.rect.x = h[0]
                    x.rect.y = h[1]
                    todos.add(x)
                spikes = readmapspikes('level1')
                for s in spikes:
                    x = Whatever(spike)
                    pinchos.add(x)
                    whatevers.add(x)
                    x.rect.x = s[0]
                    x.rect.y = s[1]
                    todos.add(x)
                genscore=0
                jugador=Jugador(matrizJugador,allowedmoves)
                jugadores.add(jugador)
                todos.add(jugador)

        if state == 'Level1History':
            mousepos = pygame.mouse.get_pos()
            screen.blit(level1History,  [0,0])

            i = 0
            for x in fac._storyrenders:
                screen.blit(x,fac._storypostions[i])
                i += 1
            select = fac.checkmousestory(mousepos)
            if select != -1 and len(fac.getTurned())<1:
                beep.play()

            if select != -1:
                txt = storyoptions[select]
                fac._storyrenders.pop(select)
                selectedrender = bob.buildtxtrender(txt, 0, red)
                fac._storyrenders.insert(select,selectedrender)
                fac._turnedoptions.append(select)

            elif select == -1 and fac.getTurned() != []:
                fac._storyrenders = fac._normalstoryrenders[:]
                fac.emptyTurned()

            elif len(fac.getTurned())> 1:
                txt = storyoptions[select]
                fac._storyrenders = fac._normalstoryrenders[:]
                fac._storyrenders.pop(select)
                selectedrender = bob.buildtxtrender(txt, 0, red)
                fac._storyrenders.insert(select,selectedrender)
                fac._turnedoptions.append(select)
            if storyoptions[select] == "Back to Menu" and mouseclick and select != -1:
                state = 'menu'
                fac.resetposbg()
                mouseclick = False
            elif storyoptions[select] == "Play" and mouseclick and select != -1:
                platforms = readmapplatforms('level1')
                for p in platforms:
                    x = Platform(platform)
                    plataformas.add(x)
                    x.rect.x = p[0]
                    x.rect.y = p[1]
                    todos.add(x)
                holes = readmapholes('level1')
                for h in holes:
                    x = Whatever(hole)
                    vacios.add(x)
                    whatevers.add(x)
                    x.rect.x = h[0]
                    x.rect.y = h[1]
                    todos.add(x)
                spikes = readmapspikes('level1')
                for s in spikes:
                    x = Whatever(spike)
                    pinchos.add(x)
                    whatevers.add(x)
                    x.rect.x = s[0]
                    x.rect.y = s[1]
                    todos.add(x)
                genscore=0
                jugador=Jugador(matrizJugador,allowedmoves)
                jugadores.add(jugador)
                todos.add(jugador)
                fac.setposbglevel1()
                state=menuoptions[0]
        elif state == 'Level2History':
            mousepos = pygame.mouse.get_pos()
            screen.blit(level2History,  [0,0])

            i = 0
            for x in fac._storyrenders:
                screen.blit(x,fac._storypostions[i])
                i += 1
            select = fac.checkmousestory(mousepos)
            if select != -1 and len(fac.getTurned())<1:
                beep.play()

            if select != -1:
                txt = storyoptions[select]
                fac._storyrenders.pop(select)
                selectedrender = bob.buildtxtrender(txt, 0, red)
                fac._storyrenders.insert(select,selectedrender)
                fac._turnedoptions.append(select)

            elif select == -1 and fac.getTurned() != []:
                fac._storyrenders = fac._normalstoryrenders[:]
                fac.emptyTurned()

            elif len(fac.getTurned())> 1:
                txt = storyoptions[select]
                fac._storyrenders = fac._normalstoryrenders[:]
                fac._storyrenders.pop(select)
                selectedrender = bob.buildtxtrender(txt, 0, red)
                fac._storyrenders.insert(select,selectedrender)
                fac._turnedoptions.append(select)
            if storyoptions[select] == "Back to Menu" and mouseclick and select != -1:
                state = 'menu'
                fac.resetposbg()
                mouseclick = False
            elif storyoptions[select] == "Play" and mouseclick and select != -1:
                platforms = readmapplatforms('level2')
                for p in platforms:
                    x = Platform(platform)
                    plataformas.add(x)
                    x.rect.x = p[0]
                    x.rect.y = p[1]
                    todos.add(x)
                holes = readmapholes('level2')
                for h in holes:
                    x = Whatever(hole)
                    vacios.add(x)
                    whatevers.add(x)
                    x.rect.x = h[0]
                    x.rect.y = h[1]
                    todos.add(x)
                spikes = readmapspikes('level2')
                for s in spikes:
                    x = Whatever(spike)
                    pinchos.add(x)
                    whatevers.add(x)
                    x.rect.x = s[0]
                    x.rect.y = s[1]
                    todos.add(x)
                genscore=0
                jugador=Jugador(matrizJugador,allowedmoves)
                jugadores.add(jugador)
                todos.add(jugador)
                fac.setposbglevel2()
                state=menuoptions[1]
        elif state == 'BossLevelHistory':
            mousepos = pygame.mouse.get_pos()
            screen.blit(bossLevelHistory,  [0,0])

            i = 0
            for x in fac._storyrenders:
                screen.blit(x,fac._storypostions[i])
                i += 1
            select = fac.checkmousestory(mousepos)
            if select != -1 and len(fac.getTurned())<1:
                beep.play()

            if select != -1:
                txt = storyoptions[select]
                fac._storyrenders.pop(select)
                selectedrender = bob.buildtxtrender(txt, 0, red)
                fac._storyrenders.insert(select,selectedrender)
                fac._turnedoptions.append(select)

            elif select == -1 and fac.getTurned() != []:
                fac._storyrenders = fac._normalstoryrenders[:]
                fac.emptyTurned()

            elif len(fac.getTurned())> 1:
                txt = storyoptions[select]
                fac._storyrenders = fac._normalstoryrenders[:]
                fac._storyrenders.pop(select)
                selectedrender = bob.buildtxtrender(txt, 0, red)
                fac._storyrenders.insert(select,selectedrender)
                fac._turnedoptions.append(select)
            if storyoptions[select] == "Back to Menu" and mouseclick and select != -1:
                state = 'menu'
                fac.resetposbg()
                mouseclick = False
            elif storyoptions[select] == "Play" and mouseclick and select != -1:
                platforms = readmapplatforms('boss')
                for p in platforms:
                    x = Platform(platform)
                    plataformas.add(x)
                    x.rect.x = p[0]
                    x.rect.y = p[1]
                    todos.add(x)
                holes = readmapholes('boss')
                for h in holes:
                    x = Whatever(hole)
                    vacios.add(x)
                    whatevers.add(x)
                    x.rect.x = h[0]
                    x.rect.y = h[1]
                    todos.add(x)
                spikes = readmapspikes('boss')
                for s in spikes:
                    x = Whatever(spike)
                    pinchos.add(x)
                    whatevers.add(x)
                    x.rect.x = s[0]
                    x.rect.y = s[1]
                    todos.add(x)
                genscore=0
                jugador=Jugador(matrizJugador,allowedmoves)
                jugadores.add(jugador)
                todos.add(jugador)
                fac.setposbglevel3()
                state=menuoptions[2]
        elif state == 'winningHistory':
            mousepos = pygame.mouse.get_pos()
            screen.blit(winningHistory,  [0,0])

            i = 0
            for x in fac._storyrenders:
                if x != fac._storyrenders[1]:
                    screen.blit(x,fac._storypostions[i])
                    i += 1
            select = fac.checkmousestory(mousepos)
            if select != -1 and len(fac.getTurned())<1:
                beep.play()

            if select != -1:
                txt = storyoptions[select]
                fac._storyrenders.pop(select)
                selectedrender = bob.buildtxtrender(txt, 0, red)
                fac._storyrenders.insert(select,selectedrender)
                fac._turnedoptions.append(select)

            elif select == -1 and fac.getTurned() != []:
                fac._storyrenders = fac._normalstoryrenders[:]
                fac.emptyTurned()

            elif len(fac.getTurned())> 1:
                txt = storyoptions[select]
                fac._storyrenders = fac._normalstoryrenders[:]
                fac._storyrenders.pop(select)
                selectedrender = bob.buildtxtrender(txt, 0, red)
                fac._storyrenders.insert(select,selectedrender)
                fac._turnedoptions.append(select)
            if storyoptions[select] == "Back to Menu" and mouseclick and select != -1:
                state = 'menu'
                fac.resetposbg()
                mouseclick = False

        #Primer nivel
        elif state == menuoptions[0]:
            pygame.display.flip()
            #print numberOfStillEnemies, numberOfMovingEnemies, numberOfDeaths, fac.posbg[0]
            if moves != [] and jugador.prevkey == None:
                jugador.move(moves[0])
            if genscore >= endscore and numberOfDeaths>=30 and fac.posbg[0]<=-1010 and numberOfStillEnemies==0 and numberOfMovingEnemies==0:
                #for j in jugadores:
                #    j.kill()
                winrenderrect = winrender.get_rect()
                winrenderpos = [RESOLUTION[0]/2 - winrenderrect.width/2,RESOLUTION[1]/2 - winrenderrect.height]
                newbckpos = [RESOLUTION[0]/2 - fac._pauserenders[0].get_rect().width/2]
                newbckpos.append(RESOLUTION[1]/2 + winrenderrect.height + 50)


                screen.blit(winrender, winrenderpos )
                mousepos = pygame.mouse.get_pos()

                i = 0
                for x in fac._storyrenders:
                    screen.blit(x,fac._storypostions[i])
                    i += 1
                select = fac.checkmousestory(mousepos)
                if select != -1 and len(fac.getTurned())<1:
                    beep.play()

                if select != -1:
                    txt = storyoptions[select]
                    fac._storyrenders.pop(select)
                    selectedrender = bob.buildtxtrender(txt, 0, red)
                    fac._storyrenders.insert(select,selectedrender)
                    fac._turnedoptions.append(select)

                elif select == -1 and fac.getTurned() != []:
                    fac._storyrenders = fac._normalstoryrenders[:]
                    fac.emptyTurned()

                elif len(fac.getTurned())> 1:
                    txt = storyoptions[select]
                    fac._storyrenders = fac._normalstoryrenders[:]
                    fac._storyrenders.pop(select)
                    selectedrender = bob.buildtxtrender(txt, 0, red)
                    fac._storyrenders.insert(select,selectedrender)
                    fac._turnedoptions.append(select)
                if storyoptions[select] == "Back to Menu" and mouseclick and select != -1:
                    state = 'menu'
                    fac.resetposbg()
                    mouseclick = False
                elif storyoptions[select] == "Play" and mouseclick and select != -1:
                    platforms = readmapplatforms('level2')
                    for p in platforms:
                        x = Platform(platform)
                        plataformas.add(x)
                        x.rect.x = p[0]
                        x.rect.y = p[1]
                        todos.add(x)
                    holes = readmapholes('level2')
                    for h in holes:
                        x = Whatever(hole)
                        vacios.add(x)
                        whatevers.add(x)
                        x.rect.x = h[0]
                        x.rect.y = h[1]
                        todos.add(x)
                    genscore=0
                    jugador=Jugador(matrizJugador,allowedmoves)
                    jugadores.add(jugador)
                    todos.add(jugador)
                    fac.setposbglevel2()
                    state= 'Level2History'
            elif gameover:
                '''
                if ohnoFlag:
                    ohno.play()
                '''
                loserenderrect = loserender.get_rect()
                loserenderpos = [RESOLUTION[0]/2 - loserenderrect.width/2,RESOLUTION[1]/2 - loserenderrect.height]
                newbckpos = [RESOLUTION[0]/2 - fac._pauserenders[0].get_rect().width/2]
                newbckpos.append(RESOLUTION[1]/2 + loserenderrect.height + 50)
                genscore=0

                screen.blit(loserender, loserenderpos )
                screen.blit(fac._pauserenders[0], newbckpos)

                select = fac.checkmousepause(mousepos, newbckpos)

                if select != -1:
                    txt = pauseoptions[select]
                    fac._pauserenders.pop(select)
                    fac._pauserenders.insert(select,backtomenured)
                    fac._turnedoptions.append(select)
                if select != -1 and len(fac.getTurned())==1:
                    beep.play()

                elif select == -1 and fac.getTurned() != []:
                    fac._pauserenders = fac._normalpauserenders[:]
                    fac.emptyTurned()
                elif len(fac.getTurned())> 1:
                    txt = pauseoptions[select]
                    fac._pauserenders = fac._normalpauserenders[:]
                    fac._pauserenders.pop(select)
                    fac._pauserenders.insert(select,backtomenured)
                    fac._turnedoptions.append(select)
                if pauseoptions[select] == "Back to Menu" and mouseclick and select!= -1:
                    poofsprite.kill()
                    numberOfStillEnemies=0
                    numberOfMovingEnemies=0
                    numberOfDeaths=0
                    fac.posbg[0]=0
                    for x in vacios:
                        x.kill()
                    for x in plataformas:
                        x.kill()
                    for x in whatevers:
                        x.kill()
                    for j in jugadores:
                        j.kill()
                    for e in enemigos:
                        e.kill()
                    for e in enemigos2:
                        e.kill()
                    for b in balas:
                        b.kill()
                    state = 'menu'
                    fac.resetposbg()
                    gameover = False
            elif not fac.pause:
                if (fac.posbg[0]==0 and numberOfDeaths==0) or (fac.posbg[0]<=-220 and numberOfDeaths==6) or (fac.posbg[0]<=-320 and numberOfDeaths==12) or (fac.posbg[0]<=-520 and numberOfDeaths==18) or (fac.posbg[0]<=-660 and numberOfDeaths==24) or (fac.posbg[0]<=-990 and numberOfDeaths==30):
                    canGenerate=True
                if canGenerate:
                    lasttime2 = pygame.time.get_ticks()
                    time4 = pygame.time.get_ticks()
                    if numberOfMovingEnemies<=0:
                        generator2=True
                        numberOfMovingEnemies=4
                    if numberOfStillEnemies<=0:
                        generator1=True
                        numberOfStillEnemies=2
                    for i in range(numberOfMovingEnemies):
                        if generator2:
                            enemy2=Enemigo2(matrizEnemigos2)
                            enemy2.rect.x=random.randrange(0, fac._screensize[0] - enemy2.rect.width, 50)
                            enemy2.rect.y=random.randrange( fac.posbgfixedy+ fac.posbg[1], fac._screensize[1] - enemy2.rect.height)
                            enemigos2.add(enemy2)
                            todos.add(enemy2)
                    generator2=False

                    for i in range(numberOfStillEnemies):
                        if generator1:
                            enemy=Enemigo1(matrizEnemigos1)
                            enemy.rect.x = random.randrange(0,20)
                            enemy.rect.y=random.randrange( fac.posbgfixedy+ fac.posbg[1], fac._screensize[1] - enemy.rect.height)
                            enemigos.add(enemy)
                            todos.add(enemy)
                    generator1=False
                    canGenerate=False

                for x in jugadores:
                    lsmod = pygame.sprite.spritecollideany(x, modifiers)
                    if lsmod != None:
                        if not lsmod.blink:
                            if lsmod.type in playermodlist:
                                playermodlist.pop(lsmod.type)
                                playermodlist[lsmod.type] = [ pygame.time.get_ticks(), x]
                            else:
                                playermodlist[lsmod.type] = [ pygame.time.get_ticks(), x]
                            x.dealtwithModifiers(lsmod.type)
                            if lsmod.type in [1,5]:
                                channel2.play(powerup)
                                x.score += 100
                                genscore += 100
                            else:
                                channel2.play(powerdown)
                                x.score -= 100
                                genscore -= 100
                            if x.score < 0:
                                x.score = 0
                            if genscore < 0:
                                genscore = 0
                            lsmod.kill()
                            if lsmod in modlist:
                                modlist.remove(lsmod)
                    lscolbullets = pygame.sprite.spritecollide(x, balas, True)
                    for z in lscolbullets:
                        if z.rect.y >= x.rect.y and z.rect.y <= x.rect.bottom -1:
                            x.dealDamage(1)
                gottapop = []
                for x in playermodlist:
                    if pygame.time.get_ticks() - playermodlist[x][0] >= 10000:
                        playermodlist[x][1].resetValue(x)
                        gottapop.append(x)
                for x in gottapop:
                    playermodlist.pop(x)
                if (pygame.time.get_ticks() - time >= random.randrange(modwait,modwait*2) and (len(modlist)<=15)) or len(modlist) <= 3:
                    if len(platforms) > 0:
                        m = fac.getModifier(random.randrange(0,6))
                        platformrandom = random.randrange(0, len(platforms))
                        m.rect.x = platforms[platformrandom][0]
                        m.rect.y = platforms[platformrandom][1] - m .rect.height
                        blink = True
                        blinkers.append(m)
                        lasttime = pygame.time.get_ticks()
                        time = pygame.time.get_ticks()
                        modifiers.add(m)
                        todos.add(m)
                        modlist.append(m)
                elif pygame.time.get_ticks() - time2 >= 20000:
                    time2 = pygame.time.get_ticks()
                    if modlist != []:
                        modlist[0].kill()
                        modlist.pop(0)

                if blink:
                    if pygame.time.get_ticks()-lasttime >= 200:
                        turn = not turn
                        lasttime = pygame.time.get_ticks()
                        if turn:
                            for x in blinkers:
                                x.kill()
                        else:
                            for x in blinkers:
                                modifiers.add(x)
                                todos.add(x)
                    if pygame.time.get_ticks() - time >= 2000:
                        blink = not blink
                        for x in blinkers:
                            x.blink = False
                            modifiers.add(x)
                            todos.add(x)
                        blinkers = []
                enemybar = []
                enemybar1 = []



                for x in enemigos:
                    if (x.rect.y + x.rect.height < fac.posbgfixedy + fac.posbg[1]) :
                        x.rect.y = fac.posbgfixedy + fac.posbg[1] - x.rect.height
                    jugadorlscol=[]
                    jugadorlscol = pygame.sprite.spritecollide(x, jugadores, False)
                    if jugadorlscol != []:
                        if len(enemybar1) >2:
                            enemybar1.pop()
                            enemybar1.append(x)
                        else:
                            enemybar1.append(x)
                    for y in jugadorlscol:
                        damageinf = y.inflictDamage(x)
                        x._health -= damageinf
                        if x._health <0:
                            x._health = 0
                        if damageinf > 0:
                            if x._health == 0:
                                y.score += 200
                                genscore += 200
                                numberOfStillEnemies-=1
                                numberOfDeaths+=1
                                x.die()
                                x.kill()
                            else:
                                y.score += 75
                                genscore += 75

                for x in enemigos:
                    if x.shoot:
                        x.shoot = False
                        channel5.play(shoot)
                        b = Bala(matrizBala)
                        b.rect.x,b.rect.y = x.rect.x + 20,x.rect.y +50
                        balas.add(b)
                        todos.add(b)
                        #x.shoot = False


                for x in enemigos2:
                    if (x.rect.y + x.rect.height < fac.posbgfixedy + fac.posbg[1]) :
                        x.rect.y = fac.posbgfixedy + fac.posbg[1] - x.rect.height
                    if x._health == 0:
                        x.die()
                    if x.canDie and x.finished:
                        x.kill()
                        numberOfDeaths+=1
                        numberOfMovingEnemies-=1
                    if not x.canDie:
                        if state == menuoptions[0]:

                            x.AImove(jugador)

                    jugadorlscol = []
                    jugadorlscol = pygame.sprite.spritecollide(x, jugadores, False)
                    if jugadorlscol != []:
                        if len(enemybar) >2:
                            enemybar.pop()
                            enemybar.append(x)
                        else:
                            enemybar.append(x)
                    for y in jugadorlscol:
                        damageinf = y.inflictDamage(x)
                        x._health -= damageinf
                        if x._health < 0:
                            x._health = 0
                        if damageinf > 0:
                            if x._health == 0:
                                y.score += 200
                                genscore += 200
                                x.die()
                            else:
                                y.score += 50
                                genscore += 50
                for x in jugadores:
                    enemylscol = pygame.sprite.spritecollide(x, enemigos2, False)
                    for y in enemylscol:
                        if y.isAttacking():
                            x.dealDamage(0.5)
                tokillbullets =[]
                for x in balas:
                    if x.lucky:
                        if state == menuoptions[0]:
                            x.AIbullet(jugador)
                    if x.rect.x > fac.posbg[0] + 2400:
                        tokillbullets.append(x)
                for b in tokillbullets:
                    b.kill()

                lsplatcollide = pygame.sprite.spritecollide(jugador, plataformas, False)

                for x in lsplatcollide:
                    if jugador.rect.bottom>=x.rect.top and jugador.accion and jugador.vel_y > 0:
                        jugador.vel_y = 0
                        jugador.stopjump()
                        jugador.rect.bottom = x.rect.top
                        jugador.onplatform = True
                lsspikecollide = pygame.sprite.spritecollide(jugador,pinchos, False)
                for x in lsspikecollide:
                    if jugador.rect.bottom < x.rect.bottom:
                        jugador.dealDamage(0.5)

                lsvaciocollide = pygame.sprite.spritecollide(jugador,vacios,False)
                if len(lsvaciocollide) >= 1:
                    for x in lsvaciocollide:
                        vaciodie = False
                        if jugador.rect.x >= x.rect.x + 5 and jugador.dir == 'R' and jugador.accion != 4 :
                            if jugador.rect.bottom - 50 >= x.rect.top:
                                if x.rect.bottom >= jugador.rect.bottom:
                                    vaciodie = True
                                    #print "die1"
                                    #print jugador.rect.x, jugador.rect.y, jugador.rect.bottom, "\n---", x.rect.x, x.rect.y, x.rect.top

                        if jugador.rect.x - 10 <= x.rect.x  and jugador.dir == 'L' and jugador.accion != 5 :
                            if jugador.rect.bottom - 50 >= x.rect.top:
                                if x.rect.bottom >= jugador.rect.bottom:
                                    vaciodie = True
                                    #print jugador.rect.x, jugador.rect.y, jugador.rect.bottom, "\n---", x.rect.x, x.rect.y, x.rect.top
                                    #print "die2"

                        if vaciodie:
                            jugador.gravedad(100)
                            gameover = True
                            poof = pygame.image.load("poof.png")
                            poof = pygame.transform.scale(poof, [jugador.rect.width, jugador.rect.height])
                            poofsprite = Whatever(poof)
                            whatevers.add(poofsprite)
                            poofsprite.rect.x=jugador.rect.x
                            poofsprite.rect.y= jugador.rect.y
                            todos.add(poofsprite)
                            jugador.kill()

                if jugador.onplatform and len(lsplatcollide)== 0:
                    anytrue = False
                    for x in plataformas:
                        rect = jugador.rect.copy()
                        rect.bottom += 10
                        if x.rect.colliderect(rect):
                            anytrue = True
                    if not anytrue:
                        if jugador.accion not in [4,5]:
                            jugador.gravedad(10)
                todos.update()

                if (jugador.rect.y + jugador.rect.height < fac.posbgfixedy + fac.posbg[1]) and jugador.accion not in [4,5] and not jugador.onplatform:
                    jugador.rect.y = fac.posbgfixedy + fac.posbg[1] - jugador.rect.height
                    #2 jugadores
                if jugador.onplatform:
                    if jugador.rect.y + jugador.rect.height >= fac.posbgfixedy + fac.posbg[1]:
                        jugador.onplatform = False
                if jugador.getHealth() <= 0:
                        gameover = True
                if moves != []:
                    fac.checklimits(moves[0],jugador, bginfo)
                if fac.prevposbg != fac.posbg:
                    fac.prevposbg[0] = fac.prevposbg[0] - fac.posbg[0]
                    fac.prevposbg[1] = fac.prevposbg[1] - fac.posbg[1]
                    for x in enemigos:
                        x.rect.x -= fac.prevposbg[0]
                        x.rect.y -= fac.prevposbg[1]
                    for x in enemigos2:
                        x.rect.x -= fac.prevposbg[0]
                        x.rect.y -= fac.prevposbg[1]
                    for m in modifiers:
                        m.rect.x -= fac.prevposbg[0]
                        m.rect.y -= fac.prevposbg[1]
                    for x in balas:
                        x.rect.x -= fac.prevposbg[0]
                        x.rect.y -= fac.prevposbg[1]
                    for x in plataformas:
                        x.rect.x -= fac.prevposbg[0]
                        x.rect.y -= fac.prevposbg[1]
                    for x in vacios:
                        x.rect.x -= fac.prevposbg[0]
                        x.rect.y -= fac.prevposbg[1]
                    for x in pinchos:
                        x.rect.x -= fac.prevposbg[0]
                        x.rect.y -= fac.prevposbg[1]
                    fac.prevposbg = fac.posbg[:]
                screen.fill([0,0,0])
                screen.blit(fondo,[0,-50])
                screen.blit(gamebckg, fac.posbg)

                drawlist = []
                for x in todos:
                    drawlist.append(x)
                drawlist.sort(key = attrgetter('rect.y'))
                drawgroup = pygame.sprite.Group()
                plataformas.draw(screen)
                vacios.draw(screen)
                for x in drawlist:
                    if x not in plataformas and x not in vacios:
                        drawgroup.add(x)
                        drawgroup.draw(screen)
                        drawgroup.remove(x)

                #todos.draw(screen)

                scorerender1 = bob.buildscorerender(str(jugador.score))
                if state == menuoptions[0]:
                    fac.drawLife(jugador.getHealth())
                    fac.drawScore(scorerender1, scorerender = score)

                    if enemybar1 != []:
                        for x in enemybar1:
                            if jugador.inflictDamage(x) == 0:
                                enemybar1.remove(x)
                    if enemybar1 != []:
                        if jugador.inflictDamage(enemybar1[0]) > 0:
                            fac.drawEnemy1Life(enemybar1[0])


                    if enemybar != []:
                        for x in enemybar:
                            if jugador.inflictDamage(x) == 0:
                                enemybar.remove(x)
                    if enemybar != []:
                        if jugador.inflictDamage(enemybar[0]) > 0:
                            fac.drawEnemyLife(enemybar[0])

                if (jugador.rect.bottom> fac._screensize[1] - 30) and jugador.accion in [0,1,2,3,4,5]:
                    if bginfo[1] + fac.posbg[1] - fac._screensize[1]  - 30 >0 and fac.posbg[1]>-200:
                            fac.posbg[1] -= 30
                pygame.display.flip()
                reloj.tick(10)

            else:
                screen.blit(pauserender, [pausexpos- pausewidth,pauseypos])
                i = 0
                for x in fac._pauserenders:
                    screen.blit(x,fac.pausepositions[i])
                    i += 1
                select = fac.checkmousepause(mousepos)

                if select != -1 and len(fac.getTurned())<1:
                    beep.play()

                if select != -1:
                    txt = pauseoptions[select]
                    fac._pauserenders.pop(select)
                    selectedrender = bob.buildtxtrender(txt, 0, red)
                    fac._pauserenders.insert(select,selectedrender)
                    fac._turnedoptions.append(select)

                elif select == -1 and fac.getTurned() != []:
                    fac._pauserenders = fac._normalpauserenders[:]
                    fac.emptyTurned()

                elif len(fac.getTurned())> 1:
                    txt = pauseoptions[select]
                    fac._pauserenders = fac._normalpauserenders[:]
                    fac._pauserenders.pop(select)
                    selectedrender = bob.buildtxtrender(txt, 0, red)
                    fac._pauserenders.insert(select,selectedrender)
                    fac._turnedoptions.append(select)
                if pauseoptions[select] == "Back to Menu" and mouseclick and select != -1:
                    numberOfStillEnemies=0
                    numberOfMovingEnemies=0
                    numberOfDeaths=0
                    fac.posbg[0]=0
                    for j in jugadores:
                        j.kill()
                    for e in enemigos:
                        e.kill()
                    for e in enemigos2:
                        e.kill()
                    for b in balas:
                        b.kill()
                    for x in whatevers:
                        x.kill()
                    for x in plataformas:
                        x.kill()
                    for x in vacios:
                        x.kill()
                    state = 'menu'
                    fac.resetposbg()


                    mouseclick = False
                    fac.pause = False
        #Segundo nivel------------------------------------------------
        elif state == menuoptions[1]:
            #print 'pos=', fac.posbg
            if moves != [] and jugador.prevkey == None:
                jugador.move(moves[0])                                 #Acomodar esto
            if genscore >= endscore and numberOfDeaths2>=24 and fac.posbg[0]<=-1575 and numberOfStillEnemies2==0 and numberOfMovingEnemies2==0:
                #for j in jugadores:
                #    j.kill()
                winrenderrect = winrender.get_rect()
                winrenderpos = [RESOLUTION[0]/2 - winrenderrect.width/2,RESOLUTION[1]/2 - winrenderrect.height]
                newbckpos = [RESOLUTION[0]/2 - fac._pauserenders[0].get_rect().width/2]
                newbckpos.append(RESOLUTION[1]/2 + winrenderrect.height + 50)


                screen.blit(winrender, winrenderpos )
                mousepos = pygame.mouse.get_pos()

                i = 0
                for x in fac._storyrenders:
                    screen.blit(x,fac._storypostions[i])
                    i += 1
                select = fac.checkmousestory(mousepos)
                if select != -1 and len(fac.getTurned())<1:
                    beep.play()

                if select != -1:
                    txt = storyoptions[select]
                    fac._storyrenders.pop(select)
                    selectedrender = bob.buildtxtrender(txt, 0, red)
                    fac._storyrenders.insert(select,selectedrender)
                    fac._turnedoptions.append(select)

                elif select == -1 and fac.getTurned() != []:
                    fac._storyrenders = fac._normalstoryrenders[:]
                    fac.emptyTurned()

                elif len(fac.getTurned())> 1:
                    txt = storyoptions[select]
                    fac._storyrenders = fac._normalstoryrenders[:]
                    fac._storyrenders.pop(select)
                    selectedrender = bob.buildtxtrender(txt, 0, red)
                    fac._storyrenders.insert(select,selectedrender)
                    fac._turnedoptions.append(select)
                if storyoptions[select] == "Back to Menu" and mouseclick and select != -1:
                    state = 'menu'
                    fac.resetposbg()
                    mouseclick = False
                elif storyoptions[select] == "Play" and mouseclick and select != -1:
                    platforms = readmapplatforms('level2')
                    for p in platforms:
                        x = Platform(platform)
                        plataformas.add(x)
                        x.rect.x = p[0]
                        x.rect.y = p[1]
                        todos.add(x)
                    holes = readmapholes('level2')
                    for h in holes:
                        x = Whatever(hole)
                        vacios.add(x)
                        whatevers.add(x)
                        x.rect.x = h[0]
                        x.rect.y = h[1]
                        todos.add(x)
                    genscore=0
                    jugador=Jugador(matrizJugador,allowedmoves)
                    jugadores.add(jugador)
                    todos.add(jugador)
                    fac.setposbglevel2()
                    state='BossLevelHistory'
            elif gameover:
                '''
                if ohnoFlag:
                    ohno.play()
                '''
                loserenderrect = loserender.get_rect()
                loserenderpos = [RESOLUTION[0]/2 - loserenderrect.width/2,RESOLUTION[1]/2 - loserenderrect.height]
                newbckpos = [RESOLUTION[0]/2 - fac._pauserenders[0].get_rect().width/2]
                newbckpos.append(RESOLUTION[1]/2 + loserenderrect.height + 50)
                genscore=0

                screen.blit(loserender, loserenderpos )
                screen.blit(fac._pauserenders[0], newbckpos)

                select = fac.checkmousepause(mousepos, newbckpos)

                if select != -1:
                    txt = pauseoptions[select]
                    fac._pauserenders.pop(select)
                    fac._pauserenders.insert(select,backtomenured)
                    fac._turnedoptions.append(select)
                if select != -1 and len(fac.getTurned())==1:
                    beep.play()

                elif select == -1 and fac.getTurned() != []:
                    fac._pauserenders = fac._normalpauserenders[:]
                    fac.emptyTurned()
                elif len(fac.getTurned())> 1:
                    txt = pauseoptions[select]
                    fac._pauserenders = fac._normalpauserenders[:]
                    fac._pauserenders.pop(select)
                    fac._pauserenders.insert(select,backtomenured)
                    fac._turnedoptions.append(select)
                if pauseoptions[select] == "Back to Menu" and mouseclick and select!= -1:
                    poofsprite.kill()
                    numberOfStillEnemies2=0
                    numberOfMovingEnemies2=0
                    numberOfDeaths2=0
                    fac.posbg[0]=0

                    for x in vacios:
                        x.kill()
                    for x in plataformas:
                        x.kill()
                    for j in jugadores:
                        j.kill()
                    for e in enemigos2n:
                        e.kill()
                    for e in enemigos2n2:
                        e.kill()
                    for b in balas:
                        b.kill()

                    state = 'menu'
                    screen.fill(black)
                    fac.resetposbg()
                    gameover = False
            elif not fac.pause:
                if (fac.posbg[0]==0 and numberOfDeaths2==0) or (fac.posbg[0]<=-500 and numberOfDeaths2==6) or (fac.posbg[0]<=-870 and numberOfDeaths2==12) or (fac.posbg[0]<=-1095 and numberOfDeaths2==18) or (fac.posbg[0]<=-1335 and numberOfDeaths2==24):
                    canGenerate2=True
                if canGenerate2:
                    lasttime2 = pygame.time.get_ticks()
                    time4 = pygame.time.get_ticks()
                    if numberOfMovingEnemies2<=0:
                        generator22=True
                        numberOfMovingEnemies2=4
                    if numberOfStillEnemies2<=0:
                        generator21=True
                        numberOfStillEnemies2=2
                    for i in range(numberOfMovingEnemies2):
                        if generator22:
                            #Modificar esto, aca va el otro enemigo
                            #enemy2Level2=reptiles(reptilm, [random.randrange(300, 900), 550])
                            #enemy2Level2=reptilesV2(reptilm)
                            enemy2Level2=Reptil2(mreptil)
                            enemy2Level2.rect.x=random.randrange(300, 900)
                            enemy2Level2.rect.y=random.randrange(450, 600)
                            enemigos2n2.add(enemy2Level2)
                            todos.add(enemy2Level2)
                    generator22=False

                    for i in range(numberOfStillEnemies2):
                        if generator21:
                            enemyLevel2=Turret(matrizTorreta)
                            enemyLevel2.rect.x = random.randrange(700,1100)
                            enemyLevel2.rect.y=random.randrange(550,575)
                            #random.randrange( fac.posbgfixedy+ fac.posbg[1], fac._screensize[1] - enemyLevel2.rect.height)
                            enemigos2n.add(enemyLevel2)
                            todos.add(enemyLevel2)
                    generator21=False
                    canGenerate2=False
                for x in jugadores:
                    lsmod = pygame.sprite.spritecollideany(x, modifiers)
                    if lsmod != None:
                        if not lsmod.blink:
                            if lsmod.type in playermodlist:
                                playermodlist.pop(lsmod.type)
                                playermodlist[lsmod.type] = [ pygame.time.get_ticks(), x]
                            else:
                                playermodlist[lsmod.type] = [ pygame.time.get_ticks(), x]
                            x.dealtwithModifiers(lsmod.type)
                            if lsmod.type in [1,5]:
                                channel2.play(powerup)
                                x.score += 100
                                genscore += 100
                            else:
                                channel2.play(powerdown)
                                x.score -= 100
                                genscore -= 100
                            if x.score < 0:
                                x.score = 0
                            if genscore < 0:
                                genscore = 0
                            lsmod.kill()
                            if lsmod in modlist:
                                modlist.remove(lsmod)
                    '''
                    Hay que modificar
                    '''
                    lscolbullets = pygame.sprite.spritecollide(x, balas, True)
                    for z in lscolbullets:
                        if z.rect.y >= x.rect.y and z.rect.y <= x.rect.bottom -1:
                            x.dealDamage(1)
                gottapop = []
                for x in playermodlist:
                    if pygame.time.get_ticks() - playermodlist[x][0] >= 10000:
                        playermodlist[x][1].resetValue(x)
                        gottapop.append(x)
                for x in gottapop:
                    playermodlist.pop(x)
                if (pygame.time.get_ticks() - time >= random.randrange(modwait,modwait*2) and (len(modlist)<=15)) or len(modlist) <= 3:
                    if len(platforms) > 0:
                        m = fac.getModifier(random.randrange(0,6))
                        platformrandom = random.randrange(0, len(platforms))
                        m.rect.x = platforms[platformrandom][0]
                        m.rect.y = platforms[platformrandom][1] - m.rect.height
                        blink = True
                        blinkers.append(m)
                        lasttime = pygame.time.get_ticks()
                        time = pygame.time.get_ticks()
                        modifiers.add(m)
                        todos.add(m)
                        modlist.append(m)
                elif pygame.time.get_ticks() - time2 >= 20000:
                    time2 = pygame.time.get_ticks()
                    if modlist != []:
                        modlist[0].kill()
                        modlist.pop(0)

                if blink:
                    if pygame.time.get_ticks()-lasttime >= 200:
                        turn = not turn
                        lasttime = pygame.time.get_ticks()
                        if turn:
                            for x in blinkers:
                                x.kill()
                        else:
                            for x in blinkers:
                                modifiers.add(x)
                                todos.add(x)
                    if pygame.time.get_ticks() - time >= 2000:
                        blink = not blink
                        for x in blinkers:
                            x.blink = False
                            modifiers.add(x)
                            todos.add(x)
                        blinkers = []
                enemybar = []
                enemybar1 = []

                for x in enemigos2n:
                    if (x.rect.y + x.rect.height < fac.posbgfixedy + fac.posbg[1]) :
                        x.rect.y = fac.posbgfixedy + fac.posbg[1] - x.rect.height
                    jugadorlscol=[]
                    jugadorlscol = pygame.sprite.spritecollide(x, jugadores, False)
                    if jugadorlscol != []:
                        if len(enemybar1) >2:
                            enemybar1.pop()
                            enemybar1.append(x)
                        else:
                            enemybar1.append(x)
                    for y in jugadorlscol:
                        damageinf = y.inflictDamage(x)
                        x._health -= damageinf
                        if x._health <0:
                            x._health = 0
                        if damageinf > 0:
                            if x._health == 0:
                                y.score += 200
                                genscore += 200
                                numberOfStillEnemies2-=1
                                numberOfDeaths2+=1
                                x.die()
                                x.kill()
                            else:
                                y.score += 75
                                genscore += 75

                for x in enemigos2n:
                    x.shooting(jugador.rect)
                    if x.shoot:
                        x.shoot = False
                        #channel5.play(shoot)
                        b = BalaT(matrizBalaT)
                        b.rect.x,b.rect.y = x.rect.x + 20,x.rect.y + 25
                        balas.add(b)
                        todos.add(b)
                        #x.shoot = False


                for x in enemigos2n2:
                    if (x.rect.y + x.rect.height -20< fac.posbgfixedy + fac.posbg[1]) :
                        x.rect.y = fac.posbgfixedy + fac.posbg[1] - x.rect.height + 20
                    if x._health == 0:
                        x.kill()
                        numberOfDeaths2+=1
                        numberOfMovingEnemies2-=1
                    #Acomodar esto
                    if not x.canDie:
                        if state == menuoptions[1]:
                            x.AImove(jugador)
                        else:
                            x.AImove(jugador, jugador2,2)

                    jugadorlscol = []
                    jugadorlscol = pygame.sprite.spritecollide(x, jugadores, False)

                    if jugadorlscol != []:
                        if len(enemybar) >2:
                            enemybar.pop()
                            enemybar.append(x)
                        else:
                            enemybar.append(x)

                    for y in jugadorlscol:
                        damageinf = y.inflictDamage(x)
                        x._health -= damageinf
                        if x._health < 0:
                            x._health = 0
                        if damageinf > 0:
                            if x._health == 0:
                                y.score += 200
                                genscore += 200
                                x.die()
                            else:
                                y.score += 50
                                genscore += 50

                for x in jugadores:
                    enemylscol = pygame.sprite.spritecollide(x, enemigos2n2, False)
                    for y in enemylscol:
                        if y.isAttacking():
                            x.dealDamage(0.5)

                tokillbullets =[]
                for x in balas:
                    if x.lucky:
                        if state == menuoptions[1]:
                            x.AIbullet(jugador)
                    if x.rect.x > fac.posbg[0] + 2400:
                        tokillbullets.append(x)
                for b in tokillbullets:
                    b.kill()
                lsplatcollide = pygame.sprite.spritecollide(jugador, plataformas, False)

                for x in lsplatcollide:
                    if jugador.rect.bottom>=x.rect.top and jugador.vel_y > 0:
                        jugador.vel_y = 0
                        jugador.stopjump()
                        jugador.rect.bottom = x.rect.top
                        jugador.onplatform = True
                lsspikecollide = pygame.sprite.spritecollide(jugador,pinchos, False)
                for x in lsspikecollide:
                    if jugador.rect.bottom < x.rect.bottom:
                        jugador.dealDamage(0.5)

                lsvaciocollide = pygame.sprite.spritecollide(jugador,vacios,False)
                if len(lsvaciocollide) >= 1:
                    for x in lsvaciocollide:
                        vaciodie = False
                        if jugador.rect.x >= x.rect.x + 5 and jugador.dir == 'R' and jugador.accion != 4 :
                            if jugador.rect.bottom - 50 >= x.rect.top:
                                if x.rect.bottom >= jugador.rect.bottom:
                                    vaciodie = True
                                    #print "die1"
                                    #print jugador.rect.x, jugador.rect.y, jugador.rect.bottom, "\n---", x.rect.x, x.rect.y, x.rect.top

                        if jugador.rect.x - 10 <= x.rect.x  and jugador.dir == 'L' and jugador.accion != 5 :
                            if jugador.rect.bottom - 50 >= x.rect.top:
                                if x.rect.bottom >= jugador.rect.bottom:
                                    vaciodie = True
                                    #print jugador.rect.x, jugador.rect.y, jugador.rect.bottom, "\n---", x.rect.x, x.rect.y, x.rect.top
                                    #print "die2"

                        if vaciodie:
                            jugador.gravedad(100)
                            gameover = True
                            poof = pygame.image.load("poof.png")
                            poof = pygame.transform.scale(poof, [jugador.rect.width, jugador.rect.height])
                            poofsprite = Whatever(poof)
                            whatevers.add(poofsprite)
                            poofsprite.rect.x=jugador.rect.x
                            poofsprite.rect.y= jugador.rect.y
                            todos.add(poofsprite)
                            jugador.kill()

                if jugador.onplatform and len(lsplatcollide)== 0:
                    anytrue = False
                    for x in plataformas:
                        rect = jugador.rect.copy()
                        rect.bottom += 10
                        if x.rect.colliderect(rect):
                            anytrue = True
                    if not anytrue:
                        if jugador.accion not in [4,5]:
                            jugador.gravedad(10)
                todos.update()
                if fac.checklevel2abyss(jugador):
                    jugador.gravedad(100)
                    gameover = True
                    poof = pygame.image.load("poof.png")
                    poof = pygame.transform.scale(poof, [jugador.rect.width, jugador.rect.height])
                    poofsprite = Whatever(poof)
                    poofsprite.rect.x=jugador.rect.x
                    poofsprite.rect.y= jugador.rect.y
                    todos.add(poofsprite)
                    jugador.kill()

                if (jugador.rect.y + jugador.rect.height < fac.posbgfixedy + fac.posbg[1]) and jugador.accion not in [4,5] and not jugador.onplatform:
                    jugador.rect.y = fac.posbgfixedy + fac.posbg[1] - jugador.rect.height
                    #2 jugadores
                if jugador.onplatform:
                    if jugador.rect.y + jugador.rect.height >= fac.posbgfixedy + fac.posbg[1]:
                        jugador.onplatform = False
                if jugador.getHealth() <= 0:
                        gameover = True
                if moves != []:
                    fac.checklimits(moves[0],jugador, bginfo2)
                if fac.prevposbg != fac.posbg:
                    fac.prevposbg[0] = fac.prevposbg[0] - fac.posbg[0]
                    fac.prevposbg[1] = fac.prevposbg[1] - fac.posbg[1]
                    for x in enemigos2n:
                        x.rect.x -= fac.prevposbg[0]
                        x.rect.y -= fac.prevposbg[1]
                    for x in enemigos2n2:
                        x.rect.x -= fac.prevposbg[0]
                        x.rect.y -= fac.prevposbg[1]
                    for m in modifiers:
                        m.rect.x -= fac.prevposbg[0]
                        m.rect.y -= fac.prevposbg[1]
                    for x in balas:
                        x.rect.x -= fac.prevposbg[0]
                        x.rect.y -= fac.prevposbg[1]
                    for x in plataformas:
                        x.rect.x -= fac.prevposbg[0]
                        x.rect.y -= fac.prevposbg[1]
                    for x in pinchos:
                        x.rect.x -= fac.prevposbg[0]
                        x.rect.y -= fac.prevposbg[1]
                    fac.prevposbg = fac.posbg[:]
                screen.fill([0,0,0])
                #screen.blit(fondo2,[0,-50])
                screen.blit(fondo2, fac.posbg)

                drawlist = []
                for x in todos:
                    drawlist.append(x)
                drawlist.sort(key = attrgetter('rect.y'))
                drawgroup = pygame.sprite.Group()
                plataformas.draw(screen)
                vacios.draw(screen)
                enemigos2n.draw(screen)
                for x in drawlist:
                    if x not in plataformas and x not in vacios and x not in enemigos2n:
                        drawgroup.add(x)
                        drawgroup.draw(screen)
                        drawgroup.remove(x)
                #todos.draw(screen)

                scorerender1 = bob.buildscorerender(str(jugador.score))
                fac.drawLife(jugador.getHealth())
                fac.drawScore(scorerender1, scorerender = score)
                if enemybar != []:
                    for x in enemybar:
                        if jugador.inflictDamage(x) == 0:
                            enemybar.remove(x)
                if enemybar != []:
                    if jugador.inflictDamage(enemybar[0]) > 0:
                        fac.drawEnemy2Life(enemybar[0])
                if enemybar1 != []:
                    for x in enemybar1:
                        if jugador.inflictDamage(x) == 0:
                            enemybar1.remove(x)
                if enemybar1 != []:
                    if jugador.inflictDamage(enemybar1[0]) > 0:
                        fac.drawEnemy3Life(enemybar1[0])



                if (jugador.rect.bottom> fac._screensize[1] - 30) and jugador.accion in [0,1,2,3,4,5]:
                    if bginfo2[1] + fac.posbg[1] - fac._screensize[1]  - 30 >0 and fac.posbg[1]>-200:
                            fac.posbg[1] -= 30
                pygame.display.flip()
                reloj.tick(10)

            else:
                screen.blit(pauserender, [pausexpos- pausewidth,pauseypos])
                i = 0
                for x in fac._pauserenders:
                    screen.blit(x,fac.pausepositions[i])
                    i += 1
                select = fac.checkmousepause(mousepos)

                if select != -1 and len(fac.getTurned())<1:
                    beep.play()

                if select != -1:
                    txt = pauseoptions[select]
                    fac._pauserenders.pop(select)
                    selectedrender = bob.buildtxtrender(txt, 0, red)
                    fac._pauserenders.insert(select,selectedrender)
                    fac._turnedoptions.append(select)

                elif select == -1 and fac.getTurned() != []:
                    fac._pauserenders = fac._normalpauserenders[:]
                    fac.emptyTurned()

                elif len(fac.getTurned())> 1:
                    txt = pauseoptions[select]
                    fac._pauserenders = fac._normalpauserenders[:]
                    fac._pauserenders.pop(select)
                    selectedrender = bob.buildtxtrender(txt, 0, red)
                    fac._pauserenders.insert(select,selectedrender)
                    fac._turnedoptions.append(select)
                if pauseoptions[select] == "Back to Menu" and mouseclick and select != -1:
                    numberOfStillEnemies2=0
                    numberOfMovingEnemies2=0
                    numberOfDeaths2=0
                    fac.posbg[0]=0
                    for j in jugadores:
                        j.kill()
                    for e in enemigos2n:
                        e.kill()
                    for e in enemigos2n2:
                        e.kill()
                    for b in balas:
                        b.kill()
                    state = 'menu'

                    fac.resetposbg()
                    for x in jugadores:
                        x.kill()
                    mouseclick = False
                    fac.pause = False
            #screen.blit(gamebckg, fac.posbg)
        #Nivel boss
        elif state == menuoptions[2]:
            pygame.display.flip()
            #print numberOfStillEnemies, numberOfMovingEnemies, numberOfDeaths, fac.posbg[0]
            if moves != [] and jugador.prevkey == None:
                jugador.move(moves[0])
            if oniwaDead == True and numberOfDeaths>=5:
                #for j in jugadores:
                #    j.kill()
                winrenderrect = winrender.get_rect()
                winrenderpos = [RESOLUTION[0]/2 - winrenderrect.width/2,RESOLUTION[1]/2 - winrenderrect.height]
                newbckpos = [RESOLUTION[0]/2 - fac._pauserenders[0].get_rect().width/2]
                newbckpos.append(RESOLUTION[1]/2 + winrenderrect.height + 50)


                screen.blit(winrender, winrenderpos )
                screen.blit(fac._pauserenders[0], newbckpos)

                state = 'winningHistory'
            elif gameover:
                '''
                if ohnoFlag:
                    ohno.play()
                '''
                loserenderrect = loserender.get_rect()
                loserenderpos = [RESOLUTION[0]/2 - loserenderrect.width/2,RESOLUTION[1]/2 - loserenderrect.height]
                newbckpos = [RESOLUTION[0]/2 - fac._pauserenders[0].get_rect().width/2]
                newbckpos.append(RESOLUTION[1]/2 + loserenderrect.height + 50)
                genscore=0

                screen.blit(loserender, loserenderpos )
                screen.blit(fac._pauserenders[0], newbckpos)

                select = fac.checkmousepause(mousepos, newbckpos)

                if select != -1:
                    txt = pauseoptions[select]
                    fac._pauserenders.pop(select)
                    fac._pauserenders.insert(select,backtomenured)
                    fac._turnedoptions.append(select)
                if select != -1 and len(fac.getTurned())==1:
                    beep.play()

                elif select == -1 and fac.getTurned() != []:
                    fac._pauserenders = fac._normalpauserenders[:]
                    fac.emptyTurned()
                elif len(fac.getTurned())> 1:
                    txt = pauseoptions[select]
                    fac._pauserenders = fac._normalpauserenders[:]
                    fac._pauserenders.pop(select)
                    fac._pauserenders.insert(select,backtomenured)
                    fac._turnedoptions.append(select)
                if pauseoptions[select] == "Back to Menu" and mouseclick and select!= -1:
                    poofsprite.kill()
                    numberOfStillEnemies=0
                    numberOfMovingEnemies=0
                    numberOfDeaths=0
                    fac.posbg[0]=0
                    for x in vacios:
                        x.kill()
                    for x in plataformas:
                        x.kill()
                    for x in whatevers:
                        x.kill()
                    for j in jugadores:
                        j.kill()
                    for e in enemigos:
                        e.kill()
                    for e in enemigos2:
                        e.kill()
                    for e in enemigos2n:
                        e.kill()
                    for e in enemigos2n2:
                        e.kill()
                    for b in balas:
                        b.kill()
                    state = 'menu'
                    fac.resetposbg()
                    gameover = False
            elif not fac.pause:
                if (fac.posbg[0]==0 and numberOfDeaths==0):
                    canGenerate=True
                if canGenerate:
                    lasttime2 = pygame.time.get_ticks()
                    time4 = pygame.time.get_ticks()
                    if numberOfMovingEnemies<=0:
                        generator2=True
                        numberOfMovingEnemies=7
                    if numberOfStillEnemies<=0:
                        generator1=True
                        numberOfStillEnemies=4
                    ntype = 0

                    for i in range(numberOfMovingEnemies):
                        if generator2:
                            if ntype == 0:
                                enemy2=Enemigo2(matrizEnemigos2)
                                enemy2.rect.x=random.randrange(0, fac._screensize[0] - enemy2.rect.width, 50)
                                enemy2.rect.y=random.randrange( fac.posbgfixedy+ fac.posbg[1]-200, fac._screensize[1] - enemy2.rect.height)
                                enemigos2.add(enemy2)
                                todos.add(enemy2)
                                enemy2Level2=Reptil2(mreptil)
                                enemy2Level2.rect.x=random.randrange(300, 900)
                                enemy2Level2.rect.y=random.randrange(450, 600)
                                enemigos2.add(enemy2Level2)
                                todos.add(enemy2Level2)
                                ntype += 1
                            else:
                                enemytype = random.randrange(0,50)
                                if enemytype < 25:
                                    enemy2=Enemigo2(matrizEnemigos2)
                                    enemy2.rect.x=random.randrange(0, fac._screensize[0] - enemy2.rect.width, 50)
                                    enemy2.rect.y=random.randrange( fac.posbgfixedy+ fac.posbg[1]-200, fac._screensize[1] - enemy2.rect.height)
                                    enemigos2.add(enemy2)
                                    todos.add(enemy2)
                                else:
                                    enemy2Level2=Reptil2(mreptil)
                                    enemy2Level2.rect.x=random.randrange(300, 900)
                                    enemy2Level2.rect.y=random.randrange(450, 600)
                                    enemigos2.add(enemy2Level2)
                                    todos.add(enemy2Level2)
                    generator2=False
                    ntype = 0
                    for i in range(numberOfStillEnemies):
                        if generator1:
                            if ntype == 0:
                                enemy=Enemigo1(matrizEnemigos1)
                                enemy.rect.x = random.randrange(0,20)
                                enemy.rect.y=random.randrange( 100, 800)
                                enemigos.add(enemy)
                                todos.add(enemy)
                                enemyLevel2=Turret(matrizTorreta)
                                enemyLevel2.rect.x = random.randrange(700,1100)
                                enemyLevel2.rect.y=random.randrange(550,575)
                                #random.randrange( fac.posbgfixedy+ fac.posbg[1], fac._screensize[1] - enemyLevel2.rect.height)
                                enemigos.add(enemyLevel2)
                                enemigos2n.add(enemyLevel2)
                                todos.add(enemyLevel2)
                                ntype += 1
                            else:
                                enemytype = random.randrange(0,50)
                                if enemytype < 25:
                                    enemy=Enemigo1(matrizEnemigos1)
                                    enemy.rect.x = random.randrange(0,20)
                                    enemy.rect.y=random.randrange( 100, 800)
                                    enemigos.add(enemy)
                                    todos.add(enemy)
                                else:
                                    enemyLevel2=Turret(matrizTorreta)
                                    enemyLevel2.rect.x = random.randrange(700,1100)
                                    enemyLevel2.rect.y=random.randrange(550,575)
                                    #random.randrange( fac.posbgfixedy+ fac.posbg[1], fac._screensize[1] - enemyLevel2.rect.height)
                                    enemigos.add(enemyLevel2)
                                    enemigos2n.add(enemyLevel2)
                                    todos.add(enemyLevel2)

                    generator1=False
                    canGenerate=False

                if (fac.posbg[0]==-405):
                    #Generate oniwa
                    '''
                    bosi=Boss(bossrecorte, [405,700])
                    bossG.add(bosi)
                    todos.add(bosi)
                    '''
                    bossi=Oniwa(mBoss)
                    bossi.rect.x=405
                    bossi.rect.y=500
                    bossG.add(bossi)
                    enemigos2.add(bossi)
                    todos.add(bossi)


                    #If kill oniwa, oniwaDead=True
                for x in bossG:
                    if x._health<=0:
                        oniwaDead=True

                for x in jugadores:
                    lsmod = pygame.sprite.spritecollideany(x, modifiers)
                    if lsmod != None:
                        if not lsmod.blink:
                            if lsmod.type in playermodlist:
                                playermodlist.pop(lsmod.type)
                                playermodlist[lsmod.type] = [ pygame.time.get_ticks(), x]
                            else:
                                playermodlist[lsmod.type] = [ pygame.time.get_ticks(), x]
                            x.dealtwithModifiers(lsmod.type)
                            if lsmod.type in [1,5]:
                                channel2.play(powerup)
                                x.score += 100
                                genscore += 100
                            else:
                                channel2.play(powerdown)
                                x.score -= 100
                                genscore -= 100
                            if x.score < 0:
                                x.score = 0
                            if genscore < 0:
                                genscore = 0
                            lsmod.kill()
                            if lsmod in modlist:
                                modlist.remove(lsmod)
                    lscolbullets = pygame.sprite.spritecollide(x, balas, True)
                    for z in lscolbullets:
                        if z.rect.y >= x.rect.y and z.rect.y <= x.rect.bottom -1:
                            x.dealDamage(1)
                gottapop = []
                for x in playermodlist:
                    if pygame.time.get_ticks() - playermodlist[x][0] >= 10000:
                        playermodlist[x][1].resetValue(x)
                        gottapop.append(x)
                for x in gottapop:
                    playermodlist.pop(x)
                if (pygame.time.get_ticks() - time >= random.randrange(modwait,modwait*2) and (len(modlist)<=15)) or len(modlist) <= 3:
                    if len(platforms) > 0:
                        m = fac.getModifier(random.randrange(0,6))
                        platformrandom = random.randrange(0, len(platforms))
                        m.rect.x = platforms[platformrandom][0]
                        m.rect.y = platforms[platformrandom][1] - m .rect.height
                        blink = True
                        blinkers.append(m)
                        lasttime = pygame.time.get_ticks()
                        time = pygame.time.get_ticks()
                        modifiers.add(m)
                        todos.add(m)
                        modlist.append(m)
                elif pygame.time.get_ticks() - time2 >= 20000:
                    time2 = pygame.time.get_ticks()
                    if modlist != []:
                        modlist[0].kill()
                        modlist.pop(0)

                if blink:
                    if pygame.time.get_ticks()-lasttime >= 200:
                        turn = not turn
                        lasttime = pygame.time.get_ticks()
                        if turn:
                            for x in blinkers:
                                x.kill()
                        else:
                            for x in blinkers:
                                modifiers.add(x)
                                todos.add(x)
                    if pygame.time.get_ticks() - time >= 2000:
                        blink = not blink
                        for x in blinkers:
                            x.blink = False
                            modifiers.add(x)
                            todos.add(x)
                        blinkers = []
                enemybar = []
                enemybar1 = []



                for x in enemigos:
                    if (x.rect.y + x.rect.height < fac.posbgfixedy + fac.posbg[1]) :
                        x.rect.y = fac.posbgfixedy + fac.posbg[1] - x.rect.height
                    jugadorlscol=[]
                    jugadorlscol = pygame.sprite.spritecollide(x, jugadores, False)
                    if jugadorlscol != []:
                        if len(enemybar1) >2:
                            enemybar1.pop()
                            enemybar1.append(x)
                        else:
                            enemybar1.append(x)
                    for y in jugadorlscol:
                        damageinf = y.inflictDamage(x)
                        x._health -= damageinf
                        if x._health <0:
                            x._health = 0
                        if damageinf > 0:
                            if x._health == 0:
                                y.score += 200
                                genscore += 200
                                numberOfStillEnemies-=1
                                numberOfDeaths+=1
                                x.die()
                                x.kill()
                            else:
                                y.score += 75
                                genscore += 75

                for x in enemigos:
                    if x.shoot:
                        #x.shoot = False
                        channel5.play(shoot)
                        b = Bala(matrizBala)
                        b.rect.x,b.rect.y = x.rect.x + 20,x.rect.y +50
                        balas.add(b)
                        todos.add(b)
                        x.shoot = False

                for x in enemigos2n:
                    x.shooting(jugador.rect)
                    if x.shoot:
                        x.shoot = False
                        #channel5.play(shoot)
                        b = BalaT(matrizBalaT)
                        b.rect.x,b.rect.y = x.rect.x + 20,x.rect.y + 25
                        balas.add(b)
                        todos.add(b)
                        #x.shoot = False

                for x in enemigos2:
                    if (x.rect.y + x.rect.height < fac.posbgfixedy + fac.posbg[1]) :
                        x.rect.y = fac.posbgfixedy + fac.posbg[1] - x.rect.height
                    if x._health == 0:
                        x.die()
                    if x.canDie and x.finished:
                        x.kill()
                        numberOfDeaths+=1
                        numberOfMovingEnemies-=1
                    if not x.canDie:
                        x.AImove(jugador)

                    jugadorlscol = []
                    jugadorlscol = pygame.sprite.spritecollide(x, jugadores, False)
                    if jugadorlscol != []:
                        if len(enemybar) >2:
                            enemybar.pop()
                            enemybar.append(x)
                        else:
                            enemybar.append(x)
                    for y in jugadorlscol:
                        damageinf = y.inflictDamage(x)
                        x._health -= damageinf
                        if x._health < 0:
                            x._health = 0
                        if damageinf > 0:
                            if x._health == 0:
                                y.score += 200
                                genscore += 200
                                x.die()
                            else:
                                y.score += 50
                                genscore += 50
                for x in jugadores:
                    enemylscol = pygame.sprite.spritecollide(x, enemigos2, False)
                    for y in enemylscol:
                        if y.isAttacking():
                            x.dealDamage(0.5)
                tokillbullets =[]
                for x in balas:
                    if x.lucky:
                        if state == menuoptions[0]:
                            x.AIbullet(jugador)
                    if x.rect.x > fac.posbg[0] + 2400:
                        tokillbullets.append(x)
                for b in tokillbullets:
                    b.kill()

                lsplatcollide = pygame.sprite.spritecollide(jugador, plataformas, False)

                for x in lsplatcollide:
                    if jugador.rect.bottom>=x.rect.top and jugador.vel_y > 0:
                        jugador.vel_y = 0
                        jugador.stopjump()
                        jugador.rect.bottom = x.rect.top
                        jugador.onplatform = True

                lsvaciocollide = pygame.sprite.spritecollide(jugador,vacios,False)
                if len(lsvaciocollide) >= 1:
                    for x in lsvaciocollide:
                        vaciodie = False
                        if jugador.rect.x >= x.rect.x + 5 and jugador.dir == 'R' and jugador.accion != 4 :
                            if jugador.rect.bottom - 50 >= x.rect.top:
                                if x.rect.bottom >= jugador.rect.bottom:
                                    vaciodie = True
                                    #print "die1"
                                    #print jugador.rect.x, jugador.rect.y, jugador.rect.bottom, "\n---", x.rect.x, x.rect.y, x.rect.top

                        if jugador.rect.x - 10 <= x.rect.x  and jugador.dir == 'L' and jugador.accion != 5 :
                            if jugador.rect.bottom - 50 >= x.rect.top:
                                if x.rect.bottom >= jugador.rect.bottom:
                                    vaciodie = True
                                    #print jugador.rect.x, jugador.rect.y, jugador.rect.bottom, "\n---", x.rect.x, x.rect.y, x.rect.top
                                    #print "die2"

                        if vaciodie:
                            jugador.gravedad(100)
                            gameover = True
                            poof = pygame.image.load("poof.png")
                            poof = pygame.transform.scale(poof, [jugador.rect.width, jugador.rect.height])
                            poofsprite = Whatever(poof)
                            whatevers.add(poofsprite)
                            poofsprite.rect.x=jugador.rect.x
                            poofsprite.rect.y= jugador.rect.y
                            todos.add(poofsprite)
                            jugador.kill()

                if jugador.onplatform and len(lsplatcollide)== 0:
                    anytrue = False
                    for x in plataformas:
                        rect = jugador.rect.copy()
                        rect.bottom += 10
                        if x.rect.colliderect(rect):
                            anytrue = True
                    if not anytrue:
                        if jugador.accion not in [4,5]:
                            jugador.gravedad(10)
                todos.update()

                if (jugador.rect.y + jugador.rect.height < fac.posbgfixedy + fac.posbg[1]) and jugador.accion not in [4,5] and not jugador.onplatform:
                    jugador.rect.y = fac.posbgfixedy + fac.posbg[1] - jugador.rect.height
                    #2 jugadores
                if jugador.onplatform:
                    if jugador.rect.y + jugador.rect.height >= fac.posbgfixedy + fac.posbg[1]:
                        jugador.onplatform = False
                if jugador.getHealth() <= 0:
                        gameover = True
                if moves != []:
                    fac.checklimits(moves[0],jugador, bginfo3)
                if fac.prevposbg != fac.posbg:
                    fac.prevposbg[0] = fac.prevposbg[0] - fac.posbg[0]
                    fac.prevposbg[1] = fac.prevposbg[1] - fac.posbg[1]
                    for x in enemigos:
                        x.rect.x -= fac.prevposbg[0]
                        x.rect.y -= fac.prevposbg[1]
                    for x in enemigos2:
                        x.rect.x -= fac.prevposbg[0]
                        x.rect.y -= fac.prevposbg[1]
                    for m in modifiers:
                        m.rect.x -= fac.prevposbg[0]
                        m.rect.y -= fac.prevposbg[1]
                    for x in balas:
                        x.rect.x -= fac.prevposbg[0]
                        x.rect.y -= fac.prevposbg[1]
                    for x in plataformas:
                        x.rect.x -= fac.prevposbg[0]
                        x.rect.y -= fac.prevposbg[1]
                    for x in vacios:
                        x.rect.x -= fac.prevposbg[0]
                        x.rect.y -= fac.prevposbg[1]
                    for x in pinchos:
                        x.rect.x -= fac.prevposbg[0]
                        x.rect.y -= fac.prevposbg[1]
                    fac.prevposbg = fac.posbg[:]
                screen.fill([0,0,0])
                #screen.blit(fondo3,[0,-50])
                screen.blit(fondo3, fac.posbg)

                drawlist = []
                for x in todos:
                    drawlist.append(x)
                drawlist.sort(key = attrgetter('rect.y'))
                drawgroup = pygame.sprite.Group()
                plataformas.draw(screen)
                vacios.draw(screen)
                for x in drawlist:
                    if x not in plataformas and x not in vacios:
                        drawgroup.add(x)
                        drawgroup.draw(screen)
                        drawgroup.remove(x)

                #todos.draw(screen)
                scorerender1 = bob.buildscorerender(str(jugador.score))
                fac.drawLife(jugador.getHealth())
                fac.drawScore(scorerender1, scorerender = score)
                if (jugador.rect.bottom> fac._screensize[1] - 30) and jugador.accion in [0,1,2,3,4,5]:
                    if bginfo3[1] + fac.posbg[1] - fac._screensize[1]  - 30 >0 and fac.posbg[1]>-200:
                            fac.posbg[1] -= 30
                if enemybar != []:
                    for x in enemybar:
                        if jugador.inflictDamage(x) == 0:
                            enemybar.remove(x)
                if enemybar != []:
                    if jugador.inflictDamage(enemybar[0]) > 0:
                        if type(enemybar[0]) == Enemigo2:
                            fac.drawEnemyLife(enemybar[0])
                        elif type(enemybar[0])== Oniwa:
                            pass
                        else:
                            fac.drawEnemy2Life(enemybar[0])
                if enemybar1 != []:
                    for x in enemybar1:
                        if jugador.inflictDamage(x) == 0:
                            enemybar1.remove(x)
                if enemybar1 != []:
                    if jugador.inflictDamage(enemybar1[0]) > 0:
                        if type(enemybar1[0]) == Enemigo1:
                            fac.drawEnemy1Life(enemybar1[0])
                        elif type(enemybar1[0])== Oniwa:
                            pass
                        else:
                            fac.drawEnemy3Life(enemybar1[0])
                for x in bossG:
                    fac.drawBossLife(x)
                pygame.display.flip()
                reloj.tick(10)

            else:
                screen.blit(pauserender, [pausexpos- pausewidth,pauseypos])
                i = 0
                for x in fac._pauserenders:
                    screen.blit(x,fac.pausepositions[i])
                    i += 1
                select = fac.checkmousepause(mousepos)

                if select != -1 and len(fac.getTurned())<1:
                    beep.play()

                if select != -1:
                    txt = pauseoptions[select]
                    fac._pauserenders.pop(select)
                    selectedrender = bob.buildtxtrender(txt, 0, red)
                    fac._pauserenders.insert(select,selectedrender)
                    fac._turnedoptions.append(select)

                elif select == -1 and fac.getTurned() != []:
                    fac._pauserenders = fac._normalpauserenders[:]
                    fac.emptyTurned()

                elif len(fac.getTurned())> 1:
                    txt = pauseoptions[select]
                    fac._pauserenders = fac._normalpauserenders[:]
                    fac._pauserenders.pop(select)
                    selectedrender = bob.buildtxtrender(txt, 0, red)
                    fac._pauserenders.insert(select,selectedrender)
                    fac._turnedoptions.append(select)
                if pauseoptions[select] == "Back to Menu" and mouseclick and select != -1:
                    numberOfStillEnemies=0
                    numberOfMovingEnemies=0
                    numberOfDeaths=0
                    fac.posbg[0]=0
                    for j in jugadores:
                        j.kill()
                    for e in enemigos:
                        e.kill()
                    for e in enemigos2:
                        e.kill()
                    for b in balas:
                        b.kill()
                    for x in whatevers:
                        x.kill()
                    for x in plataformas:
                        x.kill()
                    for x in vacios:
                        x.kill()
                    state = 'menu'
                    fac.resetposbg()


                    mouseclick = False
                    fac.pause = False




        #Instrucciones------------------------------------------------
        elif state == menuoptions[3]:
            newbckpos =   [850, 650]
            screen.fill([0,0,0])
            fac.display_bkg()
            #screen.blit(menubckg2, [100, 0])
            screen.blit(im0, [10, 300])
            screen.blit(player1,[10,0])
            screen.blit(player2,[10,400])

            screen.blit(fac._pauserenders[0], newbckpos)


            select = fac.checkmousepause(mousepos, newbckpos)

            if select != -1:
                txt = pauseoptions[select]
                fac._pauserenders.pop(select)
                fac._pauserenders.insert(select,backtomenured)
                fac._turnedoptions.append(select)

            if select != -1 and len(fac.getTurned())==1:
                beep.play()

            elif select == -1 and fac.getTurned() != []:
                fac._pauserenders = fac._normalpauserenders[:]
                fac.emptyTurned()
            elif len(fac.getTurned())> 1:
                txt = pauseoptions[select]
                fac._pauserenders = fac._normalpauserenders[:]
                fac._pauserenders.pop(select)
                fac._pauserenders.insert(select,backtomenured)
                fac._turnedoptions.append(select)
            if pauseoptions[select] == "Back to Menu" and mouseclick and select!= -1:
                state = 'menu'
                fac.resetposbg()

            #screen.blit(x,[750, 350])
            #select = fac.checkmousepause(mousepos)


            """for enemy in enemigos:
            if enemy.golpe:
                if enemy.derecha:
                    punto=[enemy.rect.x+50,enemy.rect.y+50]
                if enemy.izquierda:
                    punto=[enemy.rect.x-50,enemy.rect.y+50]
                golpe_protagonista=jugador1.rect.collidepoint(punto)
                if golpe_protagonista:
                    print("fist")
                    jugador1.salud-=20"""



        elif state == 'Salir':
            end = True
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    main()
