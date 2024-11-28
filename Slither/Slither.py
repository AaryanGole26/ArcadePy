import pygame
import random
import os

pygame.mixer.init()
pygame.init()

# Colors
red = (255, 0, 0)
yellow = (255, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)

# Creating window
screen_width = 1000
screen_height = 700
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Set the background to black (fill with black for gameplay)
bg_color = black

# Home Screen background (used in the welcome and game over screens)
bgimg2 = pygame.image.load("./home.jpg")
bgimg2 = pygame.transform.scale(bgimg2, (screen_width, screen_height))  # Scale to fit the screen

# Game Title
pygame.display.set_caption("Slither")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont('Harrington', 45)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def main():
    exit_game = False
    while not exit_game:
        # Display home screen background during welcome screen
        gameWindow.blit(bgimg2, (0, 0))  # Home screen background (scaled to fit the screen)
        text_screen("Welcome to the land of snakes where they...", black, 65, 150)
        text_screen("Press SPACEBAR To Continue...", red, 75, 500)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('back.mp3')
                    pygame.mixer.music.play()
                    gameloop()
        pygame.display.update()    
        clock.tick(60)

# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    # Bug Fixing relating HI-SCORE maintenance
    if(not os.path.exists("hiscore.txt")):
        with open("hiscore.txt", "w") as f:
            f.write("0")

    with open("hiscore.txt", "r") as f:
        hiscore = f.read()

    food_x = random.randint(20, int(screen_width / 2))  # Corrected here: cast to int
    food_y = random.randint(20, int(screen_height / 2))  # Corrected here: cast to int
    score = 0
    init_velocity = 5
    snake_size = 25
    fps = 60
    while not exit_game:
        if game_over:
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))
            gameWindow.fill(white)
            gameIcon = pygame.image.load('Slither.png')
            pygame.display.set_icon(gameIcon)

            # Display home screen background during game over screen
            gameWindow.blit(bgimg2, (0, 0))  # Home screen background (scaled to fit the screen)
            text_screen("Game Over! Press Enter To Continue", white, 125, 175)
            text_screen("Score: " + str(score), white, 400, 475)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        main()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 20 and abs(snake_y - food_y) < 20:
                score += 10
                food_x = random.randint(20, int(screen_width / 2))  # Corrected here: cast to int
                food_y = random.randint(20, int(screen_height / 2))  # Corrected here: cast to int
                snk_length += 5
                if score > int(hiscore):
                    hiscore = score 

            # Set the background to black (not bg.jpg) during gameplay
            gameWindow.fill(bg_color)  # Fill the screen with black
            text_screen("Score: " + str(score), green, 125, 645)
            text_screen("High Score: " + str(hiscore), green, 500, 645)

            # Snake food
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load('end.mp3')
                pygame.mixer.music.play()

            plot_snake(gameWindow, yellow, snk_list, snake_size)
        pygame.display.update()
        
        clock.tick(fps)

    pygame.quit()
    quit()

# Start the game
if __name__ == "__main__":
    main()
