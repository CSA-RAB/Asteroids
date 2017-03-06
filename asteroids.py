#Ryan Blaschke
#Advanced Computer Programming
#2/28/17
#asteroids



import pygame, sys, random
from pygame.locals import *


########################

########################################################################
'''This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.'''
##############################################################################



pygame.init()   #start pygame



BLACK = (  0,   0,   0)   #colors
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
WHITE = (255, 255, 255)

background = BLACK    #setting background color
entity_color = WHITE

listAsteroid=[]   #asteroids list
listLaser=[]
leveltime=50
creationTime=leveltime
all_sprites_list = pygame.sprite.Group()
lives=3      #start with 3 lives
score=0      #default score of 0
asteroid_count = 0


#Collision Detection
def isPointInsideRect(x,y,rect):
    if (x>rect.left) and (x<rect.right) and (y>rect.top) and (y<rect.bottom):
        return True
    else:
        return False

def doRectOverlap(rect1,rect2):    #when rectangles touch
    for a,b in [(rect1,rect2),(rect2,rect1)]:
        if ((isPointInsideRect(a.left,a.top,b)) or
                (isPointInsideRect(a.left,a.bottom,b)) or
                (isPointInsideRect(a.right,a.top,b)) or
                (isPointInsideRect(a.right,a.bottom,b))):
            return True
    return False


class Entity(pygame.sprite.Sprite):
    """Inherited by any object in the game."""

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class Ship(Entity):            #player ship entity class
    """
    Player controlled or AI controlled, main interaction with
    the game
    """

    def __init__(self, x, y, width, height):
        super(Ship, self).__init__(x, y, width, height)
        self.image = pygame.image.load('ship.png')
        ship = pygame.image.load('ship.png')
        self.image.blit(ship, (0, 0))



class Player(Ship):     #the actual ship and its attributes
    """The player controlled Ship"""

    def __init__(self, x, y, width, height):
        super(Player, self).__init__(x, y, width, height)
        self.y_change = 0.
        self.y_dist = 5
        self.killed=False     #Check if the player is still alive

    def MoveKeyDown(self, key):
        """Responds to a key-down event and moves accordingly"""
        if (key == pygame.K_SPACE) and self.killed==False:
            x = Laser(player.rect.x + 20, player.rect.y + 18, 46, 15)
            all_sprites_list.add(x)
            lse = pygame.mixer.Sound('fire_bow_sound-mike-koenig.wav')    #firing sound effect
            lse.play()   #play sound effect when laser appears
            listLaser.append(x)
        elif (key == pygame.K_UP):
            self.y_change += -self.y_dist
        elif (key == pygame.K_DOWN):
            self.y_change += self.y_dist

    def MoveKeyUp(self, key):  #when the up arrow key is pressed
        """Responds to a key-up event and stops movement accordingly"""
        if (key == pygame.K_UP):
            self.y_change += self.y_dist
        elif (key == pygame.K_DOWN):
            self.y_change += -self.y_dist

    def update(self):    #makes sure the ship stays in bounds
        # moves relative to its current location.
        self.rect.move_ip(0, self.y_change)
        #if ship moves off screen put it back
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > window_height - self.height:
            self.rect.y = window_height - self.height


class Asteroid(Entity):    #asteriod entity class
    def __init__(self, x, y, width, height):
        super(Asteroid, self).__init__(x, y, width, height)
        self.image = pygame.image.load("asteroid_img.jpg")
        self.x_direction = 5
        self.speed = 5  #speed

    def update(self):
        #move the asteroid
        self.rect.x-=5
        #keep asteroid in bounds and make it bounce off sides

class Laser(Entity):         #laser entity class
    def __init__(self,x, y, width, height):
        super(Laser, self).__init__(x, y, width, height)
        self.image = pygame.image.load("Laser_Bullet.png")  #laser image
        self.x_direction = 5
        self.speed = 5  #laser speed

    def update(self):
        #move laser
        self.rect.x+=5


def checkScreen(asteroids,lasers):    #checks for lasers and asteroids
    global score
    for i in asteroids:
        if i.rect.x<=0:                #when asteroid moves off screen then...
            i.remove(all_sprites_list)
            asteroids.remove(i)        #...remove it,
            if player.killed==False:   #negate points if the player wasn't killed
                score-=100
    for i in lasers:
        if i.rect.x>=window_width:
            i.remove(all_sprites_list)
            lasers.remove(i)

def checkKill(all):  #check to see if the player dies
    global lives
    for i in all:
        if doRectOverlap(i.rect,player.rect):   #when the rectangles overlap...
            all.remove(i)
            i.remove(all_sprites_list)
            lives-=1
    if lives<=0: #only label them "killed" if they have no more lives
        player.killed=True

def laserHit(asteroids,lasers):   #checks to see if lasers hit any asteroids
    global score, asteroid_count, lives
    for i in asteroids:
        for x in listLaser:
            if doRectOverlap(i.rect,x.rect):  #when their rectangles touch...
                i.remove(all_sprites_list)    #...remove the asteroid,
                x.remove(all_sprites_list)    #remove the laser bullet,
                asteroids.remove(i)
                ese = pygame.mixer.Sound('Bomb_Exploding-Sound_Explorer-68256487.wav')  #play sound effect,
                ese.play()
                lasers.remove(x)  #remove laser
                score+=100   #give points
                asteroid_count += 1
                if asteroid_count == 10:
                    lives += 1





pygame.init() #start pygame

window_width = 700   #dimensions
window_height = 400
screen = pygame.display.set_mode((window_width, window_height))
screen.fill(BLACK)  #fill screen
pygame.display.set_caption("Asteroids")   #title caption

clock = pygame.time.Clock()

First = Asteroid(window_width, random.randint(10,window_height-10), 54, 50)
listAsteroid.append(First)
player = Player(20, window_height / 2, 40, 37)

all_sprites_list.add(First)
all_sprites_list.add(player)

font=pygame.font.SysFont("freesansbold.ttf",50) #font for score at end
end = False

while (end==False):        #Start screen/main menu
    screen.fill(BLACK)     #fill screen with black
    fonttxt=pygame.font.SysFont("Britannic Bold", 40)          #font
    welcomelbl=fonttxt.render("Asteroids", 1, WHITE)           #game label
    startlbl=fonttxt.render("Start(left click)", 1, WHITE)     #start label and instructions to start
    highlbl=fonttxt.render("High Score: 10000", 1, WHITE)      #high score
    for event in pygame.event.get():       #when an event happens,
        if event.type==MOUSEBUTTONDOWN:    #specifically left mouse click,
            end=True                       #make while loop end by setting end to True
    screen.blit(welcomelbl, (200, 100))    #Blit title label
    screen.blit(startlbl, (200, 200))      #Blit start label
    screen.blit(highlbl, (200, 300))       #Blit high score label
    pygame.display.flip()



while True:
    pygame.mixer.init()
    pygame.mixer.music.load('Soft-background-music.wav')  # background music
    pygame.mixer.music.play(-1, 0.0)
    laserHit(listAsteroid, listLaser)  # Check if laser hits asteroid
    checkKill(listAsteroid)  # Check if player hit by asteroid
    checkScreen(listAsteroid, listLaser)  # Check if anything off screen
    if creationTime <= 0:  # This creates asteroids after set amount of time
        x = Asteroid(window_width - 1, random.randint(0, window_height - 20), 54, 50)
        listAsteroid.append(x)
        all_sprites_list.add(x)
        leveltime -= .25  # each time an asteroid is formed we make it shorter until next is made
        creationTime = leveltime
    # Event processing here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            player.MoveKeyDown(event.key)
        elif event.type == pygame.KEYUP:
            player.MoveKeyUp(event.key)

    for ent in all_sprites_list:
        ent.update()

    screen.fill(BLACK)

    if player.killed == False:  # Only display score and lives if the player is still alive
        pTxt = font.render("Score: {0}".format(score), 1, WHITE)
        livesTxt = font.render("Lives: {0}".format(lives), 1, WHITE)
        screen.blit(pTxt, (100, 10))
        screen.blit(livesTxt, (450, 10))
    else:  # if not then the player is removed from the game and given a game over screen
        pygame.mixer.init()
        pygame.mixer.music.load('Sad-piano.wav')
        pygame.mixer.music.play(-1, 0.0)
        all_sprites_list.remove(player)
        overTxt = font.render("You lose.", 1, WHITE)
        pTxt = font.render("Top:10000 Score: {0}".format(score), 1, WHITE)
        screen.blit(overTxt, (window_width / 2, window_height / 2))
        screen.blit(pTxt, (window_width / 2, (window_height / 2) + 30))

    all_sprites_list.draw(screen)
    creationTime -= 1
    pygame.display.flip()

    clock.tick(60)



