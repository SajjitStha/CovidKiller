import math
import random

import pygame
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('back.png')

# Caption and Icon
pygame.display.set_caption("Covid Killer")
icon = pygame.image.load('bacteria.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('takla.png')
playerX = 370
playerY = 480
playerX_change = 0
player_health = 100

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_health = []
num_of_enemies = 4  # Set number of enemies to 3
enemy_speed = 1.5  # Slower speed

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('virus.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(enemy_speed)
    enemyY_change.append(40)  # Adjusted value for movement down
    enemy_health.append(50)

# Player Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('weather.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"
player_last_fire_time = 0
player_fire_rate = 200  # Reduced fire rate to make it faster

# Enemy Bullet
enemy_bulletImg = pygame.image.load('weather.png')
enemy_bulletX = []
enemy_bulletY = []
enemy_bulletX_change = 0
enemy_bulletY_change = 5
enemy_bullet_state = []
enemy_last_fire_time = []
enemy_fire_rate = 2000  # Fire rate in milliseconds (2 seconds)

for i in range(num_of_enemies):
    enemy_bulletX.append(0)
    enemy_bulletY.append(0)
    enemy_bullet_state.append("ready")
    enemy_last_fire_time.append(0)

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)
small_font = pygame.font.Font('freesansbold.ttf', 32)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_screen():
    screen.fill((0, 0, 0))  # Fill the screen with black
    game_over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (200, 250))
    restart_text = small_font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
    screen.blit(restart_text, (150, 350))
    show_score(300, 450)
    pygame.display.update()

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def fire_enemy_bullet(x, y, i):
    global enemy_bullet_state
    enemy_bullet_state[i] = "fire"
    screen.blit(enemy_bulletImg, (x + 16, y + 10))

def isCollision(objX, objY, bulletX, bulletY):
    distance = math.sqrt(math.pow(objX - bulletX, 2) + (math.pow(objY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

def show_health_bar(x, y, health, is_player=True):
    if is_player:
        # Player's health bar (white background, green foreground)
        pygame.draw.rect(screen, (255, 255, 255), (x, y, 100, 5))  # White background
        pygame.draw.rect(screen, (0, 255, 0), (x, y, health, 5))  # Green foreground
    else:
        # Enemy's health bar (white background, red foreground)
        pygame.draw.rect(screen, (255, 255, 255), (x, y, 50, 5))  # White background
        pygame.draw.rect(screen, (255, 0, 0), (x, y, health, 5))  # Red foreground

# Game Loop
running = True
game_over = False

while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    if game_over:
        game_over_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Restart the game
                    game_over = False
                    score_value = 0
                    player_health = 100
                    playerX = 370
                    playerY = 480
                    enemyX = [random.randint(0, 736) for _ in range(num_of_enemies)]
                    enemyY = [random.randint(50, 150) for _ in range(num_of_enemies)]
                    enemy_health = [50 for _ in range(num_of_enemies)]
                    bullet_state = "ready"
                    bulletY = 480
                    enemy_bullet_state = ["ready" for _ in range(num_of_enemies)]
                    enemy_last_fire_time = [0 for _ in range(num_of_enemies)]
                if event.key == pygame.K_q:
                    running = False
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is pressed check whether it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    current_time = pygame.time.get_ticks()
                    if current_time - player_last_fire_time > player_fire_rate:
                        # Get the current x coordinate of the spaceship
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)
                        player_last_fire_time = current_time

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement and Firing
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            game_over = True
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = enemy_speed
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -enemy_speed
            enemyY[i] += enemyY_change[i]

        # Enemy Bullet Movement
        if enemy_bullet_state[i] == "fire":
            fire_enemy_bullet(enemy_bulletX[i], enemy_bulletY[i], i)
            enemy_bulletY[i] += enemy_bulletY_change
        if enemy_bulletY[i] > 600:
            enemy_bullet_state[i] = "ready"
            enemy_bulletY[i] = enemyY[i]

        # Enemy Firing Logic
        current_time = pygame.time.get_ticks()
        if enemy_bullet_state[i] == "ready" and current_time - enemy_last_fire_time[i] > enemy_fire_rate:
            enemy_bulletX[i] = enemyX[i]
            fire_enemy_bullet(enemy_bulletX[i], enemy_bulletY[i], i)
            enemy_last_fire_time[i] = current_time

        # Collision with Player
        if isCollision(playerX, playerY, enemy_bulletX[i], enemy_bulletY[i]):
            enemy_bullet_state[i] = "ready"
            enemy_bulletY[i] = enemyY[i]
            player_health -= 10
            if player_health <= 0:
                game_over = True

        # Collision with Bullet
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            enemy_health[i] -= 20
            if enemy_health[i] <= 0:
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)
                enemy_health[i] = 50

        enemy(enemyX[i], enemyY[i], i)
        show_health_bar(enemyX[i], enemyY[i] - 10, enemy_health[i], is_player=False)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_health_bar(playerX, playerY + 70, player_health)
    show_score(textX, testY)
    pygame.display.update()
