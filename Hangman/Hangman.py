import pygame
import math
import random
import os
import sys

# Initialize Pygame
pygame.mixer.init()
pygame.init()

# setup display
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HangMan!")

# Load the game icon with error handling
try:
    gameIcon = pygame.image.load('./HangMan.jpg')
    pygame.display.set_icon(gameIcon)
except pygame.error as e:
    print(f"Error loading game icon: {e}")

# Button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

# Load images with error handling
images = []
for i in range(7):
    try:
        image = pygame.image.load(f"./hangman{str(i)}.png")
        images.append(image)
    except pygame.error as e:
        print(f"Error loading image ./hangman{str(i)}.png:", e)

# Game variables
hangman_status = 0
words = ["INSTAGRAM", "COMPUTER", "PYTHON", "PYGAME", "LAPTOP", "DJANGO", "SERVER", "FILE"]
word = random.choice(words)
guessed = []

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

def draw():
    win.fill(WHITE)

    # draw title
    text = TITLE_FONT.render("HANGMAN", 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, RED, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    if len(images) > hangman_status:
        win.blit(images[hangman_status], (150, 100))
    pygame.display.update()

def display_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    global hangman_status

    FPS = 60
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Exit the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1

        draw()

        # Check if player won
        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break

        if won:
            display_message("You WON and saved your life!")
            try:
                pygame.mixer.music.load('./applause.mp3')
                pygame.mixer.music.play()
            except pygame.error as e:
                print("Error loading applause music:", e)
            return False  # Exit the game

        # Check if player lost
        if hangman_status == 6:
            display_message("You LOST and are HUNG till DEATH!")
            try:
                pygame.mixer.music.load('./end.mp3')
                pygame.mixer.music.play()
            except pygame.error as e:
                print("Error loading end music:", e)
            return False  # Exit the game

    return True  # Continue if no quit condition

# Start the game and allow quitting
if __name__ == "__main__":
    try:
        main()
    except pygame.error as e:
        print(f"Pygame error: {e}")
    pygame.quit()
    quit()
