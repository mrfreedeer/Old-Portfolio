import pygame

red = (255,0,0)         #rgb(255,0,0)
green = (0,255,0)       #rgb(0,255,0)
blue = (0,0,255)        #rgb(0,0,255)
darkBlue = (0,0,128)    #rgb(0,0,128)
yellow =(255,255,51)    #rgb(255,255,51)
white = (255,255,255)   #rgb(255,255,255)
black = (0,0,0)         #rgb(0,0,0)
pink = (255,200,200) #rgb(255,200,200)c

class Modifier(pygame.sprite.Sprite):
    def __init__(self, image,type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.type = type
        self.blink = True

class Platform(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
class Whatever(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
class Facade(object):
    def __init__(self, screen, menurenders, Wolverine, initialposition, bckg, bckgpos, wolvface, enemyface, enemyface1, enemyface2, enemyface3, bossface):
        self._normalrenders = menurenders[:]
        self._menurenders = menurenders
        self._Wolverine = Wolverine
        self._screen = screen
        self._initialposition = initialposition
        self._display_info = []
        self._turnedoptions = []
        self._bckg = bckg
        self._bckgpos = bckgpos
        self._modifiers = []
        self.pause = False
        self._screensize = pygame.display.Info()
        self._lifepos = [100, 30]
        self._enemylifepos = [self._screensize.current_w - 50,30]
        self._enemy1lifepos = [self._screensize.current_w - 50,80]
        self._bosslifepos = [self._screensize.current_w - 50,30]
        self._healthheight = 20
        self._pauserenders = []
        self._storyrenders = []
        self._storypostions = [[25, self._screensize.current_h-75],[25, self._screensize.current_h-125]]
        self._normalpauserenders = []
        self.pausepositions = []
        self.wolvface = wolvface
        self.enemyface = enemyface
        self.enemy1face = enemyface1
        self.enemy2face = enemyface2
        self.enemy3face = enemyface3
        self.bossface = bossface
    def setposbglevel1(self):
        posbg = [0, -840]
        posbg[1] += self._screensize[1]-200
        self.posbg = posbg[:]
        self.prevposbg = posbg[:]
        self.defaultposbg = posbg[:]
        self.posbgfixedy = 840
    def setposbglevel2(self):
        posbg = [0, -530]
        posbg[1] += self._screensize[1]-200
        self.posbg = posbg[:]
        self.prevposbg = posbg[:]
        self.defaultposbg = posbg[:]
        self.posbgfixedy = 530
    def setposbglevel3(self):
        posbg = [0, -850]
        posbg[1] += self._screensize[1]-200
        self.posbg = posbg[:]
        self.prevposbg = posbg[:]
        self.defaultposbg = posbg[:]
        self.posbgfixedy = 950
    def drawLife(self, health, noplayers = 1, health2=0):
        self._screen.blit(self.wolvface, (self._lifepos[0] - 75, self._lifepos[1]/2 - 5))
        rect = [self._lifepos[0], self._lifepos[1], 302 , self._healthheight]
        rect2 = [self._lifepos[0] + 1, self._lifepos[1] + 1, health*3, self._healthheight-2]
        pygame.draw.rect(self._screen, red,rect, 1)
        pygame.draw.rect(self._screen, yellow,rect2)
        if noplayers >= 2:
            wolvierect = self.wolvface.get_rect()
            wolvierect.y = self._lifepos[1]/2 - 5
            wolvierect2 = self.wolvface2.get_rect()
            wolvieheight = wolvierect.height
            wolvierect2.y = self._lifepos[1]/2 +5 + wolvieheight
            wolviebottom = wolvierect2.bottom
            self._screen.blit(self.wolvface2, (self._lifepos[0] - 75, self._lifepos[1]/2 +5 + wolvieheight))
            rectW2 = [self._lifepos[0], wolviebottom - self._healthheight, 302 , self._healthheight]
            rectW22 = [self._lifepos[0] + 1, wolviebottom - self._healthheight + 1, health2*3, self._healthheight-2]
            pygame.draw.rect(self._screen, green,rectW2, 1)
            pygame.draw.rect(self._screen, blue,rectW22)

    def drawEnemyLife(self, enemy, noplayers = 1, enemy2=None):
            health = enemy._health
            self._screen.blit(self.enemyface, [self._enemylifepos[0] - 352, self._enemylifepos[1]-15])
            rect = [self._enemylifepos[0] - 302, self._enemylifepos[1], 302 , self._healthheight]
            rect2 = [self._enemylifepos[0] -301, self._enemylifepos[1] + 1, health*3, self._healthheight-2]
            pygame.draw.rect(self._screen, red,rect, 1)
            pygame.draw.rect(self._screen, yellow,rect2)
            if noplayers >= 2:
                health2 = enemy2._health
                wolvierect = self.wolvface.get_rect()
                wolvierect.y = self._lifepos[1]/2 - 5
                wolvierect2 = self.wolvface2.get_rect()
                wolvieheight = wolvierect.height
                wolvierect2.y = self._lifepos[1]/2 +5 + wolvieheight
                wolviebottom = wolvierect2.bottom
                self._screen.blit(self.enemyface, [self._enemylifepos[0]-352, wolviebottom - self._healthheight-15])
                rectW2 = [self._enemylifepos[0]-302, wolviebottom - self._healthheight, 302 , self._healthheight]
                rectW22 = [self._enemylifepos[0] -301, wolviebottom - self._healthheight + 1, health2*3, self._healthheight-2]
                pygame.draw.rect(self._screen, green,rectW2, 1)
                pygame.draw.rect(self._screen, blue,rectW22)

    def drawEnemy1Life(self, enemy, noplayers = 1, enemy2=None):
            health = enemy._health
            self._screen.blit(self.enemy1face, [self._enemy1lifepos[0] - 352, self._enemy1lifepos[1]-15])
            rect = [self._enemy1lifepos[0] - 302, self._enemy1lifepos[1], 302 , self._healthheight]
            rect2 = [self._enemy1lifepos[0] -301, self._enemy1lifepos[1] + 1, health*3, self._healthheight-2]
            pygame.draw.rect(self._screen, red,rect, 1)
            pygame.draw.rect(self._screen, yellow,rect2)
            if noplayers >= 2:
                health2 = enemy2._health
                wolvierect = self.wolvface.get_rect()
                wolvierect.y = self._lifepos[1]/2 - 5
                wolvierect2 = self.wolvface2.get_rect()
                wolvieheight = wolvierect.height
                wolvierect2.y = self._lifepos[1]/2 +5 + wolvieheight
                wolviebottom = wolvierect2.bottom
                self._screen.blit(self.enemyface, [self._enemy1lifepos[0]-352, wolviebottom - self._healthheight-15])
                rectW2 = [self._enemy1lifepos[0]-302, wolviebottom - self._healthheight, 302 , self._healthheight]
                rectW22 = [self._enemy1lifepos[0] -301, wolviebottom - self._healthheight + 1, health2*3, self._healthheight-2]
                pygame.draw.rect(self._screen, green,rectW2, 1)
                pygame.draw.rect(self._screen, blue,rectW22)

    def drawEnemy2Life(self, enemy, noplayers = 1, enemy2=None):
            health = enemy._health
            self._screen.blit(self.enemy2face, [self._enemylifepos[0] - 352, self._enemylifepos[1]-15])
            rect = [self._enemylifepos[0] - 302, self._enemylifepos[1], 302 , self._healthheight]
            rect2 = [self._enemylifepos[0] -301, self._enemylifepos[1] + 1, health*3, self._healthheight-2]
            pygame.draw.rect(self._screen, red,rect, 1)
            pygame.draw.rect(self._screen, yellow,rect2)
            if noplayers >= 2:
                health2 = enemy2._health
                wolvierect = self.wolvface.get_rect()
                wolvierect.y = self._lifepos[1]/2 - 5
                wolvierect2 = self.wolvface2.get_rect()
                wolvieheight = wolvierect.height
                wolvierect2.y = self._lifepos[1]/2 +5 + wolvieheight
                wolviebottom = wolvierect2.bottom
                self._screen.blit(self.enemyface, [self._enemylifepos[0]-352, wolviebottom - self._healthheight-15])
                rectW2 = [self._enemylifepos[0]-302, wolviebottom - self._healthheight, 302 , self._healthheight]
                rectW22 = [self._enemylifepos[0] -301, wolviebottom - self._healthheight + 1, health2*3, self._healthheight-2]
                pygame.draw.rect(self._screen, green,rectW2, 1)
                pygame.draw.rect(self._screen, blue,rectW22)
    def drawEnemy3Life(self, enemy, noplayers = 1, enemy2=None):
            health = enemy._health
            self._screen.blit(self.enemy3face, [self._enemy1lifepos[0] - 352, self._enemy1lifepos[1]-15])
            rect = [self._enemy1lifepos[0] - 302, self._enemy1lifepos[1], 302 , self._healthheight]
            rect2 = [self._enemy1lifepos[0] -301, self._enemy1lifepos[1] + 1, health*3, self._healthheight-2]
            pygame.draw.rect(self._screen, red,rect, 1)
            pygame.draw.rect(self._screen, yellow,rect2)
            if noplayers >= 2:
                health2 = enemy2._health
                wolvierect = self.wolvface.get_rect()
                wolvierect.y = self._lifepos[1]/2 - 5
                wolvierect2 = self.wolvface2.get_rect()
                wolvieheight = wolvierect.height
                wolvierect2.y = self._lifepos[1]/2 +5 + wolvieheight
                wolviebottom = wolvierect2.bottom
                self._screen.blit(self.enemyface, [self._enemy1lifepos[0]-352, wolviebottom - self._healthheight-15])
                rectW2 = [self._enemy1lifepos[0]-302, wolviebottom - self._healthheight, 302 , self._healthheight]
                rectW22 = [self._enemy1lifepos[0] -301, wolviebottom - self._healthheight + 1, health2*3, self._healthheight-2]
                pygame.draw.rect(self._screen, green,rectW2, 1)
                pygame.draw.rect(self._screen, blue,rectW22)
    def drawBossLife(self, enemy):
            health = enemy._health
            self._screen.blit(self.bossface, [self._bosslifepos[0] - 452, self._bosslifepos[1]-15])
            rect = [self._bosslifepos[0] - 402, self._bosslifepos[1], 402 , self._healthheight]
            rect2 = [self._bosslifepos[0] -401, self._bosslifepos[1] + 1, health/30, self._healthheight-2]
            pygame.draw.rect(self._screen, red,rect, 1)
            pygame.draw.rect(self._screen, yellow,rect2)

    def drawScore(self, score1, scorerender, noplayers = 1 , score2 = 0, ):
        score1pos = [self._lifepos[0] + 352, self._lifepos[1]]
        self._screen.blit(score1, score1pos)
        self._screen.blit(scorerender,[score1pos[0] - 10, score1pos[1] - 25] )
        if noplayers >= 2:
            wolvierect = self.wolvface.get_rect()
            wolvierect.y = self._lifepos[1]/2 - 5
            wolvierect2 = self.wolvface2.get_rect()
            wolvieheight = wolvierect.height
            wolvierect2.y = self._lifepos[1]/2 +5 + wolvieheight
            wolviebottom = wolvierect2.bottom
            score2pos = [self._lifepos[0] + 352, wolviebottom - self._healthheight]
            self._screen.blit(score2, score2pos)
    def loadmodifiers(self, path, quantity = 4):
        image = pygame.image.load(path).convert_alpha()
        imageinfo = image.get_rect()
        xwidth = imageinfo[2]/quantity
        self._modifiers = []
        for x in range(quantity):
            subsquare = image.subsurface(x * xwidth, 0, xwidth, imageinfo[3])
            subsquare = pygame.transform.scale(subsquare,[75,75])
            self._modifiers.append(subsquare)
    def setPauserenders(self, pauserenders):
        self._pauserenders = pauserenders
        self._normalpauserenders = pauserenders[:]
    def setStoryrenders(self,storyrenders):
        self._storyrenders = storyrenders
        self._normalstoryrenders = storyrenders[:]
    def getModifier(self, i):
        if i < len(self._modifiers):
            m = Modifier(self._modifiers[i], i)
            return m
        else:
            return -1
    def getModifiers(self):
        return self._modifiers
    def getTurned(self):
        return self._turnedoptions
    def appendTurned(self,objt):
        self._turnedoptions.append(objt)
    def popmenurenders(self, popindex):
        self._menurenders.pop(popindex)
    def insertmenurenders(self,insertindex, element):
        self._menurenders.insert(insertindex, element)
    def emptyTurned(self):
        self._turnedoptions = []
    def resetmenurenders(self):
        self._menurenders = self._normalrenders[:]
    def display_menu(self):
        self.display_Wolverine()
        i = 0
        info = self._menurenders[0].get_rect()
        space = info.height + 10
        for x in self._menurenders:
            self._screen.blit(x,[self._initialposition[0], self._initialposition[1] + i * space])
            info = x.get_rect()
            xinfo = [self._initialposition[0], self._initialposition[1] + i * space, x.get_width(), x.get_height()]
            i += 1
            if xinfo not in self._display_info:
                self._display_info.append(xinfo)

    def display_Wolverine(self):
        self._screen.blit(self._Wolverine, [self._initialposition[0], self._initialposition[1] - 100])
    def checkmouse(self, mousepos):
        for x in self._display_info:
            if mousepos[0] >= x[0] and mousepos[0]<= x[0]+x[2] and mousepos[1] >= x[1] and mousepos[1] <= x[1]+x[3]:
                return self._display_info.index(x)
        return -1
    def checkmousepause(self,mousepos, overwrite = None):
        i = 0
        for x in self._pauserenders:
            rect = x.get_rect()
            if overwrite == None:
                rect.x, rect.y = self.pausepositions[i][0], self.pausepositions[i][1]
            else:
                rect.x, rect.y = overwrite[0], overwrite[1]
            i += 1
            if rect.collidepoint(mousepos):
                return self._pauserenders.index(x)
        return -1
    def checkmousestory(self,mousepos, overwrite = None):
        i = 0
        for x in self._storyrenders:
            rect = x.get_rect()
            if overwrite == None:
                rect.x, rect.y = self._storypostions[i][0], self._storypostions[i][1]
            else:
                rect.x, rect.y = overwrite[0], overwrite[1]
            i += 1
            if rect.collidepoint(mousepos):
                return self._storyrenders.index(x)
        return -1

    def display_bkg(self):
        self._screen.blit(self._bckg, self._bckgpos)
    def isLimitrigger(self, key, player, bginfo):
        bglimit = 150
        limit = 15
        if player.rect.x > self._screensize[0] - bglimit and key == pygame.K_RIGHT:
            return True

        if player.rect.x < limit and key == pygame.K_LEFT:
            return True
        if player.rect.y > self._screensize[1] - bglimit and key == pygame.K_DOWN:
            return True
        if player.rect.y + player.rect.height < self.posbgfixedy + self.posbg[1] + limit and key == pygame.K_UP:
            return True
    def checklevel2abyss(self, jugador):
        if jugador.accion not in [4,5]:
            if jugador.rect.x >= (self.posbg[0] + 180) and jugador.rect.x + jugador.rect.width <= (self.posbg[0] + 570):
                if jugador.rect.bottom >= (self.posbg[1] + 508) and jugador.rect.bottom <= (self.posbg[1] + 616):
                    return True
        return False
    def checklimits(self, key, player, bginfo):
        bglimit = 150
        if player.vel_multiplier > 1:
            limit = 30
        else:
            limit = 15

        if player.rect.x > self._screensize[0] - bglimit and key == pygame.K_RIGHT:
                if bginfo[0] + self.posbg[0] - self._screensize[0]  - limit >0:
                    self.posbg[0] -= limit
        if player.rect.x < limit and key == pygame.K_LEFT:
            if self.posbg[0]  + limit <0:
                    self.posbg[0] += limit
        if player.rect.y > self._screensize[1] - bglimit and key == pygame.K_DOWN:
                if bginfo[1] + self.posbg[1] - self._screensize[1]  - limit >0:
                    self.posbg[1] -= limit
        if player.rect.y + player.rect.height < self.posbgfixedy + self.posbg[1] + limit and key == pygame.K_UP:
            if self.posbg[1] + self.posbgfixedy + limit < self._screensize[1] - 200:
                    self.posbg[1] += limit
        if player.rect.y  < 0 + limit and key == pygame.K_UP:
            if self.posbg[1] + limit < 0:
                    self.posbg[1] += limit

    def resetposbg(self):
        self.posbg = self.defaultposbg[:]

class Builder(object):
    def __init__(self, normalfont, titlefont, scorefont):
        self._normalfont = normalfont
        self._titlefont = titlefont
        self._scorefont = scorefont
    def buildscreen(self):
        self._screensize = pygame.display.Info()
        screen = pygame.display.set_mode([self._screensize.current_w,self._screensize.current_h-70])
        return screen
    def buildresolution(self):
        return (self._screensize.current_w, self._screensize.current_h-70)
    def buildtxtrenders(self, txtlist, fonttype = 0, colour = black):
        renders = []
        if fonttype == 0:
            for x in txtlist:
                renders.append(self._normalfont.render(x, True, colour))
        else:
            for x in txtlist:
                renders.append(self._titlefont.render(x, True, colour))
        return renders
    def buildtxtrender(self,txt, fonttype = 0, colour = black):
        if fonttype == 0:
            return self._normalfont.render(txt, True, colour)
        else:
            return self._titlefont.render(txt, True, colour)
    def buildscorerender(self,txt,colour = white):
        return self._scorefont.render(txt, True, colour)
