import pygame
import random
import math
import shelve

# Player speed variable
player_speed = 0.5

# Creating variables for difficulty
# Enemy speed variables
diff_speed_list = [0.3, 0.5, 0.8]

# Enemy number variables
num_enemy_list = [4, 6, 10]

# Colour variables
white = (255, 255, 255)
black = (0, 0, 0)

# End game variables
end_game = 0
active = False
# Game start is false by default
game_start = False

new_high_score=0

# Enemy image variables
enemyImage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = []

# Bullet variables
# Start coordinates of bullet
bulletX = 0
bulletY = 480
bulletY_change = 3

bullet_state = "Ready"  # Ready - bullet is waiting to be fired

# Scoring variables
score_num = 0  # Start score of 0

# Text coordinates
score_textX = 10
score_textY = 10


# Defining functions so in future everytime function name is called designted code will run
def game_start_text(x, y):
   start_game_tab = font.render("Press tab to start the game", True, white)
   screen.blit(start_game_tab, (x, y))  # .blit function constantly redraws image at new coordinates


def score_show(x, y):
   score = font.render("Score: {}".format(score_num), True, white)
   screen.blit(score, (x, y))


def game_over_text():
   game_over = game_over_font.render("GAME OVER", True, white)
   screen.blit(game_over, (180, 100))


def player(x, y):
   screen.blit(playerImage, (x, y))


def enemy(x, y, i):
   screen.blit(enemyImage[i], (x, y))


def bullet_fire(x, y):
   global bullet_state  # global means that the variable can be used outside of the function
   bullet_state = "fire"  # Fire - bullet has been fired
   screen.blit(bulletImage, (x + 16, y + 10))  # Slight changes to X and Y to make positioning of bullet centered


def isCollision(enemyX, enemyY, bulletX, bulletY):
   distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (
       math.pow(enemyY - bulletY, 2)))  # formula for distance between two coordinates
   # if the distance between the two coordinates is less than 27, execute collision code
   if distance < 27:
       return True
   else:
       return False


# set game difficulty
def set_difficulty():
   # Creating array for level
   level = ['1', '2', '3']

   diff = input("How hard would you like the game to be? 1, 2 or 3?")
   while diff not in level:  # While loop to reject all invalid inputs, displays message to user
       diff = input("Sorry, please pick 1, 2, or 3 ")
   return int(diff) -1 # int to convert string input to integer
                       # minus one as list index's start with 0



# adjusts value of main enemy speed variable so it can efficiently be used in later code
def set_enemy_speed(diff):
   for i in range(num_enemy_list[diff]):
       enemyX_change.append(diff_speed_list[diff])  # changes speed of enemy based on user input

# Pressing tab to start game
def setup_game():
   #Global variables can be used outside of the function
   global game_start
   global active
   global end_game
   while not game_start: #displays startup text before tab is pressed
       game_start_text(200, 200)
       # Being able to quit the game before tab is pressed, rather than having to press tab first and then be able to quit
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               active = False
               game_start = True
               end_game = 1

           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_TAB:
                   game_start = True
           pygame.display.update()  # updates display to make game start text appear


# Main Game Loop
def run_game(diff):
   # Player Image variables
   playerX = 370
   playerY = 480
   playerX_change = 0

   # Bullet variables

   # Start coordinates of bullet
   global bulletX
   global bulletY
   global bulletY_change
   global bullet_state
   #Variable for game running status
   global active
   #Scoring variable
   global score_num



   if end_game == 0:
       active = True
   while active:

       # Colour of the Screen
       screen.fill((black))

       # line on screen
       line = pygame.draw.rect(screen, white, [0, 286, 820, 3])

       # To be able to exit the game when game screen is closed
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               active = False

           # Checking whether right or left key is pressed and moving accordingly
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_LEFT:
                   playerX_change = -player_speed
               if event.key == pygame.K_RIGHT:
                   playerX_change = player_speed
               # When space bar pressed, bullet fires
               if event.key == pygame.K_SPACE:
                   bulletX = playerX
                   bullet_fire(bulletX, bulletY)

           # When left or right button is released, player stops moving
           if event.type == pygame.KEYUP:
               if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                   playerX_change = 0
       # updates X coordinate of player to be at the position when the left or right key was released
       playerX += playerX_change

       # creating boundaries so that player cannot move past parameters
       if playerX <= 0:
           playerX = 0
       elif playerX >= 736:
           playerX = 736
       # Enemy movement
       for i in range(num_enemy_list[diff]):  # all following code is applied all the enemies on the screen, the number of which depends on user input/difficulty

           # Game Over
           if enemyY[i] > 250:
               for i in range(num_enemy_list[diff]):
                   enemyY[i] = 2000
                   bullet_state = "Fire"  # bullet cannot be fired once game over
                   playerX = 2000


                   game_over_text()  # Displays game over text
                   check_high_score() # Display high score


           enemyX[i] += enemyX_change[i]  # new X coordinate is original plus X_change value, so constantly changing position
           # Boundaries so that enemy cannot move past parameters
           if enemyX[i] <= 0:
               enemyX_change[i] = diff_speed_list[diff]  # This is done to be able to account for the different enemy speed based on user input
               # Makes the enemy move downwards after hitting boundary
               enemyY[i] += enemyY_change[i]
           elif enemyX[i] >= 736:
               enemyX_change[i] = -diff_speed_list[diff]
               enemyY[i] += enemyY_change[i]

           # Collision
           collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
           if collision:
               bulletY = 480
               bullet_state = "ready"
               score_num += 1
               enemyX[i] = random.randint(0, 736)
               enemyY[i] = random.randint(0, 150)

           enemy(enemyX[i], enemyY[i], i)

       # Bullet movement
       if bulletY <= 0:
           bulletY = 480
           bullet_state = "ready"

       if bullet_state == "fire":
           bullet_fire(bulletX, bulletY)
           bulletY -= bulletY_change  # minus as top of the screen is 0 and bottom is 600 - therefore to go upwards Y coordinate needs to be reduced

       # calling the functions in the while loop as I want the player and score to constantly appear
       player(playerX, playerY)
       score_show(score_textX, score_textY)
       # Make the screen constantly refresh to account for changes
       pygame.display.update()

# Loads in number of enemies based on difficulty, and makes them appear at random locations within specified range
def load_enemy(diff):
   global enemyY
   global enemyX
   for i in range(num_enemy_list[diff]):
       enemyImage.append(pygame.image.load('enemy.png'))
       # Randomises enemy position each time
       enemyX.append(random.randint(0, 736))
       enemyY.append(random.randint(0, 150))
       enemyY_change.append(40)


def check_high_score():

   global new_high_score

   file1 = shelve.open('score.txt')  #opening file to save highest score on disk
   try: #try statement to catch exception when reading file for first time
       score = file1['score'] # Reading the highest score from the file
   except: # First time use, so highest score assumed 0
       score = 0
       file1['score'] = score_num #Writing the new highest score in the file (first time)
       new_high_score =1 #Set variable to indicate new high score
   if(new_high_score):
       high_score_text = high_score_font.render("**NEW HIGH SCORE**", True, white) #Display high score text
       screen.blit(high_score_text, (170, 160))
       # Make the screen constantly refresh to account for changes

   if (score_num > score):
       file1['score'] = score_num  # #Writing the new highest score in the file
       new_high_score = 1

   file1.close() #close the file

# Initialize pygame
pygame.init()

# Creating the screen
screen = pygame.display.set_mode((800, 600))  # Size of the screen
# Creating Title
pygame.display.set_caption("Space Invaders by Tavish Puri")

playerImage = pygame.image.load('player.png')
bulletImage = pygame.image.load('bullet.png')
font = pygame.font.Font('freesansbold.ttf', 30)  # Score Text

# Game over text
game_over_font = pygame.font.Font('freesansbold.ttf', 70)

#High Score text
high_score_font = pygame.font.Font('freesansbold.ttf', 70)

# Game start text
game_start_font = pygame.font.Font('freesansbold.ttf', 60)
# Calling functions
diff = set_difficulty()
set_enemy_speed(diff)
load_enemy(diff)
setup_game()
run_game(diff)

game_over_text()  # Displays game over text
check_high_score() # Display high score




