import pygame, random
from pygame.locals import *
from pygame.font import *


# some colors
BLACK = (   0,   0,   0)
WHITE = ( 255, 255, 255)
DARKGRAY = ( 47, 79, 79)

RED   = ( 255,   0,   0)
GREEN = (   0, 255,   0)
DARKGREEN = ( 0, 155, 0)
BLUE  = ( 0,   0,   255)

# -----------------------------------------------------------------------------

class Mole(pygame.sprite.Sprite):

    def __init__(self, fmn, delayTime):
        
        super().__init__()
        self.image = pygame.image.load(fmn).convert_alpha()
        self.rect = self.image.get_rect()
        self.fleeDelay = delayTime
        self.fleeTime = 3

# time limitation of the character moving
    def delayFlee(self):
        if(time - self.fleeTime) > self.fleeDelay:
            self.flee()
            self.fleeTime = time
        

    # move mole to a new random location
    # after it is hit
    def flee(self):
        x = random.randint(0, scrWidth-1-self.rect.width)
        y = random.randint(0, scrHeight-1-self.rect.height)
        self.rect.topleft = (x,y)

    


    def draw(self, screen):
        screen.blit(self.image, self.rect)

# ----------------------------------------------------------------------------

class Shovel(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("shovel.gif").convert_alpha()
        self.rect = self.image.get_rect()


    # did the shovel hit the mole?
    def hit(self, target):
        hitSnd.play()
        return self.rect.colliderect(target)


    # follows the mouse cursor
    def update(self, pt):
        self.rect.center = pt


    def draw(self, screen):
        screen.blit(self.image, self.rect)


def centerImage(screen, im):
    x = (scrWidth - im.get_width())/2
    y = (scrHeight - im.get_height())/2
    screen.blit(im, (x,y))
    
# -------------main--------------------------------------------------------
#to init the music that is contained in the game        
def initMusic():
    global hitSnd
    
    #background music
    # (3) Add musich which plays until the program end
    pygame.mixer.music.load('FindYou.ogg')
    pygame.mixer.music.set_volume(0.09)
    pygame.mixer.music.play(-1) #to make music plays till the end of program

    #to add  clashes sound effects
    hitSnd = pygame.mixer.Sound('clashes.wav')
    hitSnd.set_volume(8)
        
# ---------------------------------------------------------------------------
def isGameOver():
    global finalMsg
     
    if hits >= winningScore and time < timeLimit:
        finalMsg = 'Awesome!'
        return True
    elif hits < winningScore and time == timeLimit:
        finalMsg = 'Loser!'
        return True
    else:
        return False

def delayFlee(self):
    time = pygame.time.get_ticks()
    if(time - self.fleeTime) > self.fleeDelay:
        self.flee()
        self.fleeTime = time
    

#-----------------------------------------------------------------------------

pygame.init()
# (1) Increase the size of the game area
screen = pygame.display.set_mode([896,512])

# (2) Replace the green backrgound by a picture
#to load background image:
scrWidth, scrHeight = screen.get_size()
bg = pygame.image.load('1.jpg').convert()
pygame.display.set_caption("Whack-a- japanese mole")


#to init the music game
initMusic()

#to create game font
pygame.font.init()
gameFont = pygame.font.Font('Onana.ttf', 90)

#create sprites for normal character
#(7) Add another mole than can be whacked
mole = Mole('mole.gif', 120)
mole2 = Mole('mole.gif', 4)

#create sprite for unnormal character
#(7)
Supermole = Mole('mouse.gif', 0.7)
shovel = Shovel()

#game vars
hits = 0
mousePos = (scrWidth/2, scrHeight/2)
isPressed = False
gameOver = False
#(5)Add a time limit for winning and losing the game
timeLimit = 20

#to create the winning score
#(4)Add winning score
winningScore = 70


clock = pygame.time.Clock()

running = True
while running:
    clock.tick(30)

    # handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        if event.type == MOUSEMOTION:
            mousePos = pygame.mouse.get_pos()

        if event.type == MOUSEBUTTONDOWN:
            isPressed = True

    #to create a timing move in a second        
    time = int(pygame.time.get_ticks()/1000)
   
    #draw background image (2)
    screen.blit (bg, [0,0])
    
    
    #update game
    if isPressed:
        isPressed = False
        if shovel.hit(Supermole):
            Supermole.flee()
            hits += 5
        elif shovel.hit(mole):
            mole.flee()
            hits += 1
        elif shovel.hit(mole2):
            mole2.flee()
            hits += 1


    if not gameOver:
        timeIm = gameFont.render(str(time), True, WHITE)
        screen.blit(timeIm, (10,10))
        shovel.update(mousePos)
        gameOver = isGameOver()
        
        #to redraw game (7)
        mole.draw(screen)
        mole2.draw(screen)
        Supermole.draw(screen)
        shovel.draw(screen)
        
        #to wait before moving into a new location
        #(8) & (9)
        mole2.delayFlee()
        Supermole.delayFlee()

        #to show how many characters that has been hitten
        hitIm = gameFont.render("Hits = " + str(hits), True, WHITE)
        centerImage(screen, hitIm)

     #to create a final message after playing the game
     #(6) Add a message for reporting to the player win or lose
    elif gameOver:
        screen.blit(gameFont.render(finalMsg, 1, GREEN),(200,200))
    

    pygame.display.update()

pygame.quit()
