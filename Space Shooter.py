import pygame
import random
import time
import threading
import math

# Initialize Pygame
pygame.init()

# Set up the display
screenWidth = 800
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Space Shooter")

# Load and scale images
playerImg = pygame.transform.scale(pygame.image.load(r'C:\Users\Yuvan shankar\Downloads\kisspng-portable-network-graphics-spacecraft-clip-art-imag-5bfa68895ed9e4.3539657115431374173885.png').convert_alpha(), (64, 88))
enemyImg = pygame.transform.scale(pygame.image.load(r'C:\Users\Yuvan shankar\Downloads\kisspng-airplane-fighter-aircraft-heavy-bomber-jet-aircraf-fighter-jet-5ac3b48edda9d1.0160411415227751829079.png').convert_alpha(), (64, 64))
bulletImg = pygame.transform.scale(pygame.image.load(r'C:\Users\Yuvan shankar\Downloads\—Pngtree—red bullet effect light effect_7150008.png').convert_alpha(), (15, 89))
backgroundImg = pygame.transform.scale(pygame.image.load(r'C:\Users\Yuvan shankar\Downloads\Breaking Bad\960bd916fdadac434ac17510b2516495454e16b8.jpg'), (800, 600))
blastImg = pygame.transform.scale(pygame.image.load(r'C:\Users\Yuvan shankar\Downloads\pngegg.png').convert_alpha(),(200,200))

# Define colors
white = (255, 255, 255)

# Set up the game variables
playerWidth = 64
playerHeight = 64
playerX = screenWidth // 2 - playerWidth // 2
playerY = screenHeight - playerHeight - 25
playerSpeed = 1

bulletWidth = 8
bulletHeight = 8
bulletX = 0
bulletY = 0
bulletSpeed = 5
bulletState = "ready"  # "ready" means ready to fire, "fire" means bullet is moving

enemyWidth = 64
enemyHeight = 64
enemySpeed = 0.25
enemies = []

score = 0
font = pygame.font.Font(None, 36)

# Function to draw player
def drawPlayer(x, y):
    screen.blit(playerImg, (x, y))

# Function to draw enemy
def drawEnemy(x, y):
    screen.blit(enemyImg, (x, y))

# Function to draw bullet
def drawBullet(x, y):
    screen.blit(bulletImg, (x, y))

# Function to check collision between two objects
def isCollision(obj1_x, obj1_y, obj2_x, obj2_y):
    distance = math.sqrt((math.pow(obj1_x - obj2_x, 2)) + (math.pow(obj1_y - obj2_y, 2)))
    if distance < 27:
        return True
    else:
        return False

# Function to draw blast
def drawBlast(x, y):
    screen.blit(blastImg, (x, y))

# Function to generate enemies
def spawnEnemies():
    enemy_x = random.randint(0, screenWidth - enemyWidth)
    enemy_y = random.randint(-200, -64)
    enemies.append([enemy_x, enemy_y])

# Function to display game over
def gameOver():
    game_over_font = pygame.font.Font(None, 72)
    game_over_text = game_over_font.render("Game Over!", True, white)
    screen.blit(game_over_text, (screenWidth // 2 - game_over_text.get_width() // 2, screenHeight // 2 - game_over_text.get_height() // 2))
    pygame.display.update()

# Function to play music
def startMusic():
    pygame.mixer.music.load(r"C:\Users\Yuvan shankar\Downloads\space-120280.mp3")
    pygame.mixer.music.play(-1)
    pygame.time.wait(15000)
    pygame.mixer.music.fadeout(1000)
    pygame.mixer.music.unload()
    pygame.mixer.music.load(r"C:\Users\Yuvan shankar\Downloads\dead-space-style-ambient-music-184793.mp3")
    pygame.mixer.music.play(-1,1)

# Game loop
running = True
spawnTimer = 0
spawnInterval = 120  # 120 frames = 1 seconds
enemyBoom = pygame.mixer.Sound(r"C:\Users\Yuvan shankar\Downloads\musket-explosion-6383.mp3")
bulletSound = pygame.mixer.Sound(r"C:\Users\Yuvan shankar\Downloads\laser-gun-shot-sound-future-sci-fi-lazer-wobble-chakongaudio-174883.mp3")
thread = threading.Thread(target=startMusic)
thread.start()
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Fire bullet when spacebar is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bulletState == "ready":
                    bulletX = playerX + playerWidth / 2 - bulletWidth / 2 - 4
                    bulletY = playerY - 30
                    bulletState = "fire"
                    pygame.mixer.Sound.play(bulletSound)

    # Move player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and playerX > 0:
        playerX -= playerSpeed
    if keys[pygame.K_RIGHT] and playerX < screenWidth - playerWidth:
        playerX += playerSpeed
    if keys[pygame.K_UP] and playerY > 0:
        playerY += playerSpeed-2
    if keys[pygame.K_DOWN] and playerY < screenHeight - playerHeight:
        playerY -= playerSpeed-2 

    # Draw background
    screen.blit(backgroundImg, (0, 0))

    # Draw player
    drawPlayer(playerX, playerY)

    # Draw and move enemies
    for enemy in enemies:
        enemy[1] += enemySpeed
        drawEnemy(enemy[0], enemy[1])

        # Check collision between player and enemy
        collision = isCollision(playerX, playerY, enemy[0], enemy[1])
        if collision:
            # Game over
            pygame.mixer.Sound.play(enemyBoom)
            drawBlast(playerX-70,playerY-60)
            gameOver()
            time.sleep(0.25)
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            running = False


        # Remove enemies that go out of screen
        if enemy[1] > screenHeight:
            enemies.remove(enemy)

    # Draw and move bullet
    if bulletState == "fire":
        drawBullet(bulletX, bulletY)
        bulletY -= bulletSpeed
        # Reset bullet when it goes out of screen
        if bulletY < 0:
            bulletState = "ready"

    # Check collision between bullet and enemy
    for enemy in enemies:
        collision = isCollision(bulletX, bulletY, enemy[0], enemy[1])
        if collision:
            # Increase score
            score += 1
            # Reset bullet and respawn enemy
            bulletState = "ready"
            enemies.remove(enemy)

    # Draw score
    score_display = font.render("Score: " + str(score), True, white)
    screen.blit(score_display, (10, 10))

    # Spawn enemies at regular intervals
    spawnTimer += 0.75
    if spawnTimer >= spawnInterval:
        spawnEnemies()
        spawnTimer = 0

    # Update display
    pygame.display.update()
