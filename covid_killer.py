import math
import random
import pygame
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('back1.jpg')

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
num_of_enemies = 4  # Set number of enemies to 4
enemy_speed = 1.5  # Slower speed

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('virus.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(enemy_speed)
    enemyY_change.append(40)  # Adjusted value for movement down
    enemy_health.append(50)

# Player Bullet
bulletImg = pygame.image.load('weather.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"
player_last_fire_time = 0
player_fire_rate = 200  # Reduced fire rate to make it faster

# Enemy Bullet
enemy_bulletImg = pygame.image.load('covidbullet.png')
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
high_score = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)
small_font = pygame.font.Font('freesansbold.ttf', 32)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    score_bg = pygame.Surface((score.get_width() + 10, score.get_height() + 10))
    score_bg.fill((50, 50, 50))
    screen.blit(score_bg, (x - 5, y - 5))
    screen.blit(score, (x, y))

def show_high_score(x, y):
    high_score_text = font.render("High Score : " + str(high_score), True, (255, 255, 255))
    screen.blit(high_score_text, (x, y))

def game_over_screen():
    screen.fill((0, 0, 0))  # Fill the screen with black
    game_over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (200, 250))
    restart_button = create_button("Restart", 150, 350, 200, 50)
    quit_button = create_button("Quit", 450, 350, 200, 50)
    show_score(300, 450)
    show_high_score(300, 500)
    pygame.display.update()
    return restart_button, quit_button

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
    return distance < 27

def show_health_bar(x, y, health, is_player=True):
    if is_player:
        # Player's health bar (white background, green foreground)
        pygame.draw.rect(screen, (255, 255, 255), (x, y, 100, 5))  # White background
        pygame.draw.rect(screen, (0, 255, 0), (x, y, health, 5))  # Green foreground
    else:
        # Enemy's health bar (white background, red foreground)
        pygame.draw.rect(screen, (255, 255, 255), (x, y, 50, 5))  # White background
        pygame.draw.rect(screen, (255, 0, 0), (x, y, health, 5))  # Red foreground

def create_button(text, x, y, width, height):
    button_color = (255, 255, 255)
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, button_color, button_rect)
    button_text = small_font.render(text, True, (0, 0, 0))
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)
    return button_rect

def handle_button_click(button_rect, action):
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
        return action
    return None

# Create a Clock object to manage the frame rate
clock = pygame.time.Clock()

# Game Loop
running = True
game_over = False
game_started = False

# Add this function to show the controls screen
def controls_screen():
    screen.fill((0, 0, 0))  # Fill the screen with black

    

    # Title with a larger font and a different color
    controls_text = over_font.render("Controls", True, (255, 215, 0))  # Gold color for the title
    screen.blit(controls_text, (300, 100))

    control_instructions = [
        "Movement: <- & -> Arrow Keys to Move",
        "Press Space to Fire",
        "Destroy the Enemies to Earn Points",
        "Avoid Enemy Bullets"
    ]
    
    instruction_color = (255, 255, 255)  # White color for instructions
    for i, line in enumerate(control_instructions):
        instruction_text = small_font.render(line, True, instruction_color)
        screen.blit(instruction_text, (100, 200 + i * 40))

    # Create a back button with hover effect
    back_button = create_button("Back", 300, 400, 200, 50)
    
    # Draw a border around the button
    pygame.draw.rect(screen, (0, 255, 0), back_button, 3)  # Green border

    # Check for mouse hover to change button color
    mouse_pos = pygame.mouse.get_pos()
    if back_button.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (0, 200, 0), back_button)  # Darker green when hovered

    pygame.display.update()
    
    return back_button# Main Menu
def main_menu():
    screen.fill((0, 0, 0))  # Fill the screen with black
    menu_text = over_font.render("Covid Killer", True, (255, 255, 255))
    screen.blit(menu_text, (220, 100))
    start_button = create_button("Start", 260, 230, 300, 50)
    controls_button = create_button("Controls",260,300,300,50) 
    quit_button = create_button("Quit", 260, 370, 300, 50)
    pygame.display.update()
    return start_button,controls_button,quit_button 

while running:

    # Limit the frame rate to 60 frames per second
    clock.tick(60)

    # Main Menu
    if not game_started:
        start_button, controls_button, quit_button = main_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if handle_button_click(start_button, "start") == "start":
            game_started = True
        elif handle_button_click(controls_button, "controls") == "controls":
            back_button = controls_screen()
            in_controls_screen = True
            while in_controls_screen:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        in_controls_screen = False
                    
                    # Handle "Back" button click to return to the main menu
                    if handle_button_click(back_button, "back") == "back":
                        in_controls_screen = False
                continue

        if handle_button_click(quit_button, "quit") == "quit":
            running = False
        continue

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    if game_over:
        if score_value > high_score:
            high_score = score_value
        restart_button, quit_button = game_over_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if handle_button_click(restart_button, "restart") == "restart":
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
        if handle_button_click(quit_button, "quit") == "quit":
            running = False
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is pressed check whether it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    current_time = pygame.time.get_ticks()
                    if current_time - player_last_fire_time > player_fire_rate:
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)
                        player_last_fire_time = current_time

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Checking for boundaries of spaceship so it doesn't go out of bounds
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over = True
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = enemy_speed
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -enemy_speed
            enemyY[i] += enemyY_change[i]

        # Fire enemy bullet
        current_time = pygame.time.get_ticks()
        if current_time - enemy_last_fire_time[i] > enemy_fire_rate:
            if enemy_bullet_state[i] == "ready":
                enemy_bulletX[i] = enemyX[i]
                enemy_bulletY[i] = enemyY[i]
                fire_enemy_bullet(enemy_bulletX[i], enemy_bulletY[i], i)
                enemy_last_fire_time[i] = current_time

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemy_health[i] -= 10  # Reduce enemy health by 10 on collision
            if enemy_health[i] <= 0:  # If enemy health is 0 or less
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)
                enemy_health[i] = 50  # Reset enemy health to 50
                enemy_speed += 0.1  # Increase speed slightly

        # Draw enemy and health bar
        enemy(enemyX[i], enemyY[i], i)
        show_health_bar(enemyX[i], enemyY[i] - 10, enemy_health[i], is_player=False)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Enemy Bullet Movement
    for i in range(num_of_enemies):
        if enemy_bulletY[i] >= 600:
            enemy_bulletY[i] = enemyY[i]
            enemy_bullet_state[i] = "ready"

        if enemy_bullet_state[i] == "fire":
            fire_enemy_bullet(enemy_bulletX[i], enemy_bulletY[i], i)
            enemy_bulletY[i] += enemy_bulletY_change

        # Check for collision with player
        player_collision = isCollision(playerX, playerY, enemy_bulletX[i], enemy_bulletY[i])
        if player_collision:
            enemy_bulletY[i] = enemyY[i]
            enemy_bullet_state[i] = "ready"
            player_health -= 10  # Reduce player health by 10 on collision
            if player_health <= 0:  # If player health is 0 or less
                game_over = True
    
    player(playerX, playerY)
    show_health_bar(playerX, playerY - 20, player_health)

    show_score(textX, textY)
    show_high_score(textX, textY + 40)
    pygame.display.update()