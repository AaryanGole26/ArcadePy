import random
import sys
import pygame
from pygame.locals import *

# Variables of game
FPS = 32
SCREENWIDTH = 800
SCREENHEIGHT = 625
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = './gallery/sprites/UFO.png'
BACKGROUND = './gallery/sprites/background.png'
PILLAR = './gallery/sprites/pillar.png'


def main():
    """
    Shows welcome images on the screen
    """
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.15)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))    
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))    
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))    
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))    
                gameIcon = pygame.image.load('./gallery/sprites/FU.png')
                pygame.display.set_icon(gameIcon)
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    # Create 2 pillars for blitting on the screen
    newPillar1 = getRandomPillar()
    newPillar2 = getRandomPillar()

    # my List of upper pillars
    upperPillars = [
        {'x': int(SCREENWIDTH+200), 'y': newPillar1[0]['y']},
        {'x': int(SCREENWIDTH+200) + int(SCREENWIDTH/2), 'y': newPillar2[0]['y']},
    ]
    # my List of lower pillars
    lowerPillars = [
        {'x': int(SCREENWIDTH+200), 'y': newPillar1[1]['y']},
        {'x': int(SCREENWIDTH+200) + int(SCREENWIDTH/2), 'y': newPillar2[1]['y']},
    ]

    pillarVelX = -9
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8  # velocity while flapping
    playerFlapped = False  # It is true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['hover'].play()

        crashTest = isCollide(playerx, playery, upperPillars, lowerPillars)
        if crashTest:
            return

        # check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pillar in upperPillars:
            pillarMidPos = pillar['x'] + GAME_SPRITES['pillar'][0].get_width()/2
            if pillarMidPos <= playerMidPos < pillarMidPos + 9:
                score += 1
                print(f"Your score is {score}") 
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pillars to the left
        for upperPillar, lowerPillar in zip(upperPillars, lowerPillars):
            upperPillar['x'] += pillarVelX
            lowerPillar['x'] += pillarVelX

        # Add a new pillar when the first is about to cross the leftmost part of the screen
        if 0 < upperPillars[0]['x'] < 10:
            newpillar = getRandomPillar()
            upperPillars.append(newpillar[0])
            lowerPillars.append(newpillar[1])

        # if the pillar is out of the screen, remove it
        if upperPillars[0]['x'] < -GAME_SPRITES['pillar'][0].get_width():
            upperPillars.pop(0)
            lowerPillars.pop(0)

        # Blitting our Sprites
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPillar, lowerPillar in zip(upperPillars, lowerPillars):
            SCREEN.blit(GAME_SPRITES['pillar'][0], (upperPillar['x'], upperPillar['y']))
            SCREEN.blit(GAME_SPRITES['pillar'][1], (lowerPillar['x'], lowerPillar['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.40))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPillars, lowerPillars):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True

    for pillar in upperPillars:
        pillarHeight = GAME_SPRITES['pillar'][0].get_height()
        if (playery < pillarHeight + pillar['y'] and
            abs(playerx - pillar['x']) < GAME_SPRITES['pillar'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pillar in lowerPillars:
        if (playery + GAME_SPRITES['player'].get_height() > pillar['y']) and \
           abs(playerx - pillar['x']) < GAME_SPRITES['pillar'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False


def getRandomPillar():
    """
    Generate positions of two pillars(one bottom straight and one top rotated ) for blitting on the screen
    """
    pillarHeight = GAME_SPRITES['pillar'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 * offset))
    pillarX = SCREENWIDTH + 10
    y1 = pillarHeight - y2 + offset
    pillar = [
        {'x': pillarX, 'y': -y1},  # upper Pillar
        {'x': pillarX, 'y': y2}    # lower Pillar
    ]
    return pillar


if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init()  # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy UFO')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('./gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('./gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('./gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('./gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('./gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('./gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('./gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('./gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('./gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('./gallery/sprites/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] = pygame.image.load('./gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('./gallery/sprites/base.jpg').convert_alpha()
    GAME_SPRITES['pillar'] = (
        pygame.transform.rotate(pygame.image.load(PILLAR).convert_alpha(), 180),
        pygame.image.load(PILLAR).convert_alpha()
    )

    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('./gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('./gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('./gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('./gallery/audio/swoosh.wav')
    GAME_SOUNDS['hover'] = pygame.mixer.Sound('./gallery/audio/hover.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        main()  # Shows welcome screen to the user until he presses a button
        mainGame()  # This is the main game function