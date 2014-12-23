import pygame, sys, time, random
from pygame.locals import *

#Initializer
pygame.init()
mainClock = pygame.time.Clock()

#set up names list
names = []
file = open('names.txt', 'r')
for line in file:
    names.append(line.strip())
numNames = len(names)

#Background/Screen/Constants
WINDOWWIDTH = 1200
WINDOWHEIGHT = 800
defaultBackground = (255,255,255)
caption = 'FEAR THE GEAR'

screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption(caption)
background = pygame.Surface(screen.get_size())
background = background.convert()

#Defining Colors
bg1=(255,0,0)
bg2=(255,128,0)
bg3=(255,255,0)
bg4=(0,255,0)
bg5=(0,128,255)
bg6=(255,0,255)


#Name/Font Display
font = pygame.font.SysFont("impact", 120)
name_display = font.render("THE GEAR", 1, (0, 0, 0))

#Music Effects
spinSound = pygame.mixer.Sound('spinningnoise.mp3')
winSound = pygame.mixer.Sound('winningnoise.mp3')

#Gear and Logos
gearImage = pygame.image.load('gear.png')
gearImage = pygame.transform.scale(gearImage, (500, 500))
original_gearImage = gearImage
gear = gearImage.get_rect()

#Variables that are used as "timers"
angle = 0
global bg
bg = 0
whichName = 0
global phase
phase = 0
global epilepsy
epilepsy = 0
global fakeout
fakeout = 0

#Functions
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotozoom(image, angle, 1)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def center_name(name_display):
    width = name_display.get_width()
    width = width/2
    starting_point = (WINDOWWIDTH/2)-width
    return starting_point

def main_screen():
    screen.blit(background, (0,0))
    screen.blit(gearImage, (350, 250))
    screen.blit(name_display, (center_name(name_display), 50))
    
def epileptic():
    global bg
    bg = bg + .5
    if bg == 0:
        background.fill(defaultBackground)
    if bg == 1:
        background.fill(bg1)
    if bg == 2:
        background.fill(bg2)
    if bg == 3:
        background.fill(bg3)
    if bg == 4:
        background.fill(bg4)
    if bg == 5:
        background.fill(bg5)
    if bg == 6:
        background.fill(bg6)
        bg = 0

def reset():
    global bg
    global phase
    global epilepsy
    global fakeout
    bg = 0
    phase = 0
    epilepsy = 0
    fakeout = 0
    
###############################################################
#Game Area

while True:

    #No spinning goin' on
    while phase == 0:
        main_screen()
        background.fill(defaultBackground)
        pygame.display.update()

        #Event handler for default phase
        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        phase = 1
                        pygame.mixer.music.load('spinningnoise.mp3')
                        pygame.mixer.music.set_endevent(pygame.USEREVENT)
                        pygame.mixer.music.play()
                    if event.key == K_e:
                        phase = 1
                        epilepsy = 1
                        pygame.mixer.music.load('spinningnoise.mp3')
                        pygame.mixer.music.set_endevent(pygame.USEREVENT)
                        pygame.mixer.music.play()
                    if event.key == K_f:
                        phase = 1
                        fakeout = 1
                        pygame.mixer.music.load('spinningnoise.mp3')
                        pygame.mixer.music.set_endevent(pygame.USEREVENT)
                        pygame.mixer.music.play()

    #Spin da wheel phase
    while phase == 1:
        main_screen()

        #Rotating
        angle = angle + 5
        if (angle < 180):
            gearImage = rot_center(gearImage, -7.5)
        else:
            gearImage = original_gearImage
            gearImage = rot_center(gearImage, -7.5)
            angle = 0

        #Bg colors
        if epilepsy == 1:
            epileptic()

        #Choose next name to spin through
        whichName = whichName + 1
        if whichName >= numNames:
            whichName = 0
            name_display = font.render(names[0], 1, (0, 0, 0))
        else:
            name_display = font.render(names[whichName], 1, (0, 0, 0))

        #Event handler for during the spin
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == USEREVENT:
                name_display.fill(defaultBackground)
                screen.blit(name_display, (center_name(name_display), 50))
                pygame.display.update()
                luckyNumber = random.randint(0, numNames-1)
                #fakeout game mode
                if fakeout == 1:
                    main_screen()
                    pygame.display.update
                    name_display = font.render (names[luckyNumber], 1, (0,0,0))
                    screen.blit(name_display, (center_name(name_display), 50))
                    pygame.display.update()
                    time.sleep(1)
                    luckyNumber = random.randint(0, numNames-1)
                phase = 2
                pygame.mixer.music.load('winningnoise.mp3')
                pygame.mixer.music.play()
        
        pygame.display.update()

    #You are da winna phase
    while phase == 2:
        background.fill(defaultBackground)
        screen.blit(background, (0,0))
        screen.blit(gearImage, (350, 250))
        blinkCounter = 0
        while blinkCounter < 4:
            name_display.fill(defaultBackground)
            screen.blit(name_display, (center_name(name_display), 50))
            pygame.display.update()
            time.sleep(.5)
            name_display = font.render(names[luckyNumber], 1, (0,0,0))
            screen.blit(name_display, (center_name(name_display), 50))
            pygame.display.update()
            time.sleep(.5)
            blinkCounter = blinkCounter + 1
        reset()
