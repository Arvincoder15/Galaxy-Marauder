#####################################################################################
## File Name: arvinaskari.py
## Program: ICS3U Final Project - Galaxy Marauder
## Author: Arvin Askari
## Date: Monday, January 23rd, 2023
## Description: This is a spaceship laser blasting alien game that allows the user
##  to try and attempt to eliminate all the aliens using their lasers before they
##  touch the spaceship which then results in the game to be over and for that user
##  to lose the game. In order to win the game, the user would need to eliminate
##  the aliens before it touches the spaceship. Then if either of these outcomes
##  were to happen, the user will either have the option to restart the game, return
##  to the main lobby and try a harder level, or quit the game.
## Input: User inputs which level of difficulty they would like to play and they
##  keep on click on keys like the left arrow and right to arrow to move and even
##  the space bar to shoot lasers out of the spaceship.
#####################################################################################

# Imports pygame, imports random, and imports time, while also intilalizes pygame.
import pygame
import random
import time
pygame.init()

# Initializes the the variables and values for each colour.
BLACK = (0,0, 0)

WHITE = (255,255,255)
RED   = (255,0, 0)
GREEN = (0,255,0)
BLUE  = (0,0,255)
LIGHT_BLUE = (102,255,255)

# Initializes the variables such as fonts, sounds, clock, and text.
titleFont = pygame.font.SysFont("calibri", 60)
restartGameFont = pygame.font.SysFont("calibri", 20)
buttonFont = pygame.font.SysFont("calibri", 20)
scoreFont = pygame.font.SysFont("calibri", 20)
gameOverFont = pygame.font.SysFont("monospace", 60)
clock = pygame.time.Clock()
title = titleFont.render('GALAXY MARAUDER', True, WHITE)
difficultyTitle = titleFont.render('Choose a Difficulty', True, WHITE)
laserShot = pygame.mixer.Sound('laser.ogg')
alienExplode = pygame.mixer.Sound('alienexplode.ogg')

# Intializes images in order for pygame to be able to load it in png's and also fixes the size of the images.
spaceImage = pygame.image.load('space.png')
gameTitleImage = pygame.image.load('spaceshipalien.png')
spaceshipVSalien = pygame.image.load('spaceshipvsalien.png')
spaceshipImage = pygame.image.load('spaceship.png')
spaceshipImage = pygame.transform.scale(spaceshipImage, (200, 50))
laserImage = pygame.image.load('laser.png')
laserImage = pygame.transform.scale(laserImage, (80, 60))

# Intializes texts that need to be renderd with their specific given font and colour.
wonSurface = gameOverFont.render("YOU WIN!",True,BLUE)
lostSurface = gameOverFont.render("YOU LOST!",True,RED)
playAgain = restartGameFont.render('Click "p" to Play Again!', True, WHITE)
quitGame = restartGameFont.render('Click "ESC" to Quit!', True, WHITE)
goBack = restartGameFont.render('Click "b" to Go Back!', True, WHITE)

# Intializes catagory buttons for the main menu and for when the user wants to select levels.
catButtons = [[(170,130,200,100),'Play Game'],
              [(430,130,200,100),'Quit Game']]

catButtons2 = [[(80,130,200,100),'Easy'],
               [(300,130,200,100),'Hard'],
               [(520,130,200,100),'Impossible']]

# Intializes the variable for the game window (win) by setting its size (800,600) and
#   gives a caption to the title of the program.
win = pygame.display.set_mode((800,600))
pygame.display.set_caption('Galaxy Marauder by Arvin Askari')

# Intializes the variables that are needed for the game to function.
speed = 4                # Sets the starting speed of the aliens.

score = 0                # Sets the starting score of the program.
scoreX = 5               # Sets the x-coordinate of the score text.
scoreY = 5               # Sets the y=coordinate of the score text.

currentScreen = 1        # Initalizes currentScreen to 1 (main menu).

spaceship_x = 370        # Sets the starting x-coordinate of the spaceship.
spaceship_y = 523        # Sets the starting y-coordinate of the spaceship.
spaceship_Xchange = 60   # Sets the amount of distance/pixels the spaceship will move from left to right.

alienImages = []         # Creates an empty list for the alien images.
alien_x = []             # Creates an empty list for x-coordinates of the aliens.
alien_y = []             # Creates an empty list for y-coordinates of the aliens.
alien_Xchange = []       # Creates an empty list for the change in x-coordinates of the aliens.
alien_Ychange = []       # Creates an empty list for the change in y-coordinates of the aliens.
alienNumber = 25         # Intializes the alienNumber to be set to 25 (amount of aliens on the game screen).

lasers = []              # Creates an empty list for the lasers.
laser_x = spaceship_x    # Ensures that the x-coordinate of the laser is the same as the x-coordinate of the spaceship.
laser_y = spaceship_y    # Ensures that the y-coordinate of the laser is the same as the y-coordinate of the spaceship.
laser_Xchange = 0        # Ensures that the lasers do not move 
laser_Ychange = 12       # Sets a starting speed of the laser to 12 where it the higher the number, the faster it can move in the y direction. 

# Intializes and sets the aliens to be appended on the game screen given the number of aliens (25) by giving them
#   a random starting position and x and y direction change.
for num in range(alienNumber):
    alienImages.append(pygame.image.load('aliens.png'))
    alienImages[num]=pygame.transform.scale(alienImages[num], (100, 50))
    alien_x.append(random.randint(64, 737))
    alien_y.append(random.randint(30, 180))
    alien_Xchange.append(speed)
    alien_Ychange.append(random.randint(30, 100))

# Ensures it receives an input for the highscore and if it does not it stays at zero.       
try:
    highScore = int(getHighScore())
except:
    highScore = 0

# Creates the function of showScore that blits the score on the top left hand of the game window
#   and gradually increases as aliens get hit by a laser.
def showScore(x, y):
    points = scoreFont.render('Points: ' + str(score), True, WHITE)
    win.blit(points, (x , y ))

# Creates a function that shows the high score at the top of the screen by blitting and rendering it.
def showHighScore(highScore):
    highScores = scoreFont.render('High Score: ' + str(highScore), True, WHITE)
    win.blit(highScores, (125, 5))

# Creates a function that uses a text file that stores the number that is associated with thr highscore and returns
#   as it constantly updates and reads it.
def getHighScore():
    with open('highscoregame.text', 'r') as f:
        return f.read()

# Creates a gameOver function that will blit and render the words "GAME OVER" once the user loses the game.
def gameOver():
    gameOverTxt = gameOverFont.render('GAME OVER', True, WHITE)
    win.blit(gameOverTxt, (280, 280))

# A function that blits the image of the spaceship at its desired coordinates by decreasing its x value by 16 and increasing its y value by 10.
def spaceship(x, y):
    win.blit(spaceshipImage, (x - 16, y + 10))

# A function that blits the images of the aliens on the game window with its desired coordinates and the amount of aliens.
def alien(x, y, i):
    win.blit(alienImages[i], (x, y))

# Creates a function that blits the image of a laser with its disired coordinates and changes its x value by 16 and y value by 10.
def laser(x, y):
    win.blit(laserImage, (x + 16, y + 10))

# A function that allows for the aliens to move by calling the x, y, change in x, change in y, alienNumber, and speed of the aliens.
#   Puts in range the amount of the alien number and ensures that if the x-coordinate of the alien is less than 736, the speed
#   in which the alien has will multiply negative one. however if it is less than 64 then it matches that speed.
#   This function also adds and matches the alien_x[i] and alien_y[i] with the alien_Xchange[i] and alien_Ychange[i] by also
#   blitting the alien images doing these actions to the game window.
def moveAliens(alien_x, alien_y, alien_Xchange, alien_Ychange, alienNumber, speed):
    for i in range(alienNumber):
        if alien_x[i] > 736:
            alien_Xchange[i] = speed * -1
            alien_y[i] += alien_Ychange[i]
        elif alien_x[i] < 64:
            alien_Xchange[i] = speed
            alien_y[i] += alien_Ychange[i]
        alien_x[i] += alien_Xchange[i]
        win.blit(alienImages[i], (alien_x[i], alien_y[i]))

# This function allows for the lasers to move along the y axis and make their way up in order to try and collide with the aliens
#   by also calling the variables lasers and laser_Ychange. This function in order to work globalizes the variables score and
#   alien number and creates a varible index of zero. It also makes a variable of aliens prenset on screen in which looks at
#   their x and y coordinates and iterates multiple aliens at the same time by using the zip parameter. This function also
#   uses a colliderect in which uses the width and height of the laser and aliens to determine if they were to collide. If so,
#   then the score would increase by one and the alien and laser would both disappear. However, if this were to not happen,
#   it would then continue blitting the image of the laser and increases the index by one. If an alien were to be hit, the pop
#   parameter is used to remove the alien at the desired index that is taken from the list, which then decreases the alien Number by one each time.
def moveLaser(lasers, laser_Ychange):
    global score
    global alienNumber
    index = 0
    aliens_on_screen = [(x, y) for x, y in zip(alien_x, alien_y) if x >= 0]
    while index < len(lasers):
        x, y = lasers[index]
        hit_alien = False
        for laser in range(len(aliens_on_screen)):
            alien_rect = alienImages[laser].get_rect(x=aliens_on_screen[laser][0], y=aliens_on_screen[laser][1])
            if alien_rect.colliderect(pygame.Rect(x, y, laserImage.get_width(), laserImage.get_height())):
                score += 1
                aliens_on_screen[laser] = (-100, -100)
                hit_alien = True
                break
        if hit_alien:
            lasers.pop(index)
        else:
            win.blit(laserImage, (x, y))
            y -= laser_Ychange
            lasers[index] = (x, y)
            index += 1
        hit_aliens = [laser for k, (x, y) in enumerate(aliens_on_screen) if x == -100 and y == -100]
        for hit in hit_aliens:
            aliens_on_screen.pop(hit)
            alien_x.pop(hit)
            alien_y.pop(hit)
            alien_Xchange.pop(hit)
            alien_Ychange.pop(hit)
            alienNumber -= 1
            alienExplode.play()

# This function checks for any collisions between the spaceship and the aliens by calling the x and y coordinates of both the
#   spaceship and the aliens. By using the absolute value of the x coordinates of the spaceship and aliens, it is able to determine
#   any collison between them depending on where they are on the screen. Should they collide, the game will blit game over and the
#   the game will be lost by the user as it breaks the game.
def checkCollision(spaceship_x, alien_x, spaceship_y, alien_y):
    for i in range(alienNumber):
        if alien_y[i] >= 450:
            if abs(spaceship_x - alien_x[i]) < 80:
                for laser in range(alienNumber):
                    alien_y[laser] = 2000
                gameOver()
                win.blit(lostSurface, (280, 200))
                win.blit(playAgain, (150, 100))
                win.blit(quitGame, (450, 100))
                win.blit(goBack, (300, 400))
                break

# This function moves the spaceshipa and checks its positon with its x coordinate ensuring it does not leave the screen and by
#   allowing it to be able to move left to right.
def moveSpaceship(spaceship_x, spaceship_y):
    if spaceship_x <= 16:
        spaceship_x = 16;
    elif spaceship_x >= 750:
        spaceship_x = 750
    spaceship(spaceship_x, spaceship_y)
    showScore(scoreX, scoreY)

# This function draws catagory buttons for the main menu and changes colour to blue if it is hovered over.
def drawCatagoryButtons(catButtons):
    catMousePos = pygame.mouse.get_pos()
    for b in catButtons:
        if pygame.Rect(b[0]).collidepoint(catMousePos):
            catBtncolour = BLUE
        else:
            catBtncolour = BLACK
        pygame.draw.rect(win,catBtncolour,b[0],0)
        pygame.draw.rect(win,WHITE,b[0],3)
        txtSurface = buttonFont.render(b[1],True,WHITE)
        x = b[0][0] + (b[0][2] - txtSurface.get_width()) // 2
        y = b[0][1] + (b[0][3] - txtSurface.get_height()) // 2
        win.blit(txtSurface,(x,y))

# This function draws catagory buttons for the levels screen and changes colours to red if it is hovered over.
def drawCatagoryButtons2(catButtons2):
    catMousePos = pygame.mouse.get_pos()
    for b in catButtons2:
        if pygame.Rect(b[0]).collidepoint(catMousePos):
            catBtncolour2 = RED
        else:
            catBtncolour2 = BLACK
        pygame.draw.rect(win,catBtncolour2,b[0],0)
        pygame.draw.rect(win,WHITE,b[0],3)
        txtSurface = buttonFont.render(b[1],True,WHITE)
        x = b[0][0] + (b[0][2] - txtSurface.get_width()) // 2
        y = b[0][1] + (b[0][3] - txtSurface.get_height()) // 2
        win.blit(txtSurface,(x,y))

# This functions checks to see if any of the catagory buttons have been clicked by the user.
def catClickBtn(mp,buttons):
    for i,b in enumerate(buttons):
        if pygame.Rect(b[0]).collidepoint(mp):
            return i
    return -1

# Updates the game window depending on the current screen by blitting images and titles and also calls functions
#   like moveAliens, moveLaser, moveSpaceship, and checkCollision, in order for the game to properly function by constantly
#   updating the screen so no error happens. It also shows the scores, the amount of aliens, and blits a you won text, should
#   all the aliens to be eliminated from the screen. Also for screens 3, 4, and 5, it is given a specific alien and laser speed
#   to make the game more interesting and make it more difficult.
def game_window():
    
    if currentScreen == 1:
        win.blit(spaceImage, (800,600))
        win.blit(title, (100,30))
        win.blit(gameTitleImage, (100, 255))
        drawCatagoryButtons(catButtons)

    elif currentScreen == 2:
        win.blit(spaceImage, (800,600))
        win.blit(difficultyTitle, (155,30))
        win.blit(spaceshipVSalien, (100, 255))
        win.blit(goBack, (300, 560))
        drawCatagoryButtons2(catButtons2)
        
    elif currentScreen == 3:
        win.blit(spaceImage, (800, 600))
        speed = 4
        laser_Ychange = 12
        
        for i in range(alienNumber):
            alien(alien_x[i], alien_y[i], i)
            showScore(scoreX, scoreY)
            showHighScore(highScore)
        moveAliens(alien_x, alien_y, alien_Xchange, alien_Ychange, alienNumber, speed)
        moveLaser(lasers, laser_Ychange)
        moveSpaceship(spaceship_x, spaceship_y)
        checkCollision(spaceship_x, alien_x, spaceship_y, alien_y)

        if alienNumber == 0:
            showHighScore(highScore)
            win.blit(goBack, (300, 300))
            win.blit(wonSurface, (280, 200))
            win.blit(playAgain, (150, 100))
            win.blit(quitGame, (450, 100))

    elif currentScreen == 4:
        win.blit(spaceImage, (800, 600))
        speed = 25
        laser_Ychange = 8

        for i in range(alienNumber):
            alien(alien_x[i], alien_y[i], i)
            showScore(scoreX, scoreY)
            showHighScore(highScore)
        moveAliens(alien_x, alien_y, alien_Xchange, alien_Ychange, alienNumber, speed)
        moveLaser(lasers, laser_Ychange)
        moveSpaceship(spaceship_x, spaceship_y)
        checkCollision(spaceship_x, alien_x, spaceship_y, alien_y)

        if alienNumber == 0:
            showHighScore(highScore)
            win.blit(goBack, (300, 300))
            win.blit(wonSurface, (280, 200))
            win.blit(playAgain, (150, 100))
            win.blit(quitGame, (450, 100))

    elif currentScreen == 5:
        win.blit(spaceImage, (800, 600))
        speed = 45
        laser_Ychange = 5

        for i in range(alienNumber):
            alien(alien_x[i], alien_y[i], i)
            showScore(scoreX, scoreY)
            showHighScore(highScore)
        moveAliens(alien_x, alien_y, alien_Xchange, alien_Ychange, alienNumber, speed)
        moveLaser(lasers, laser_Ychange)
        moveSpaceship(spaceship_x, spaceship_y)
        checkCollision(spaceship_x, alien_x, spaceship_y, alien_y)

        if alienNumber == 0:
            showHighScore(highScore)
            win.blit(goBack, (300, 300))
            win.blit(wonSurface, (280, 200))
            win.blit(playAgain, (150, 100))
            win.blit(quitGame, (450, 100))
            
    pygame.display.update()

#-------------------------------#
# The main program begins here. #
#-------------------------------#

inGame = True                                                              # sets inGame to True so game functions.
while inGame:                                                              # While loop commences.
 
    game_window()                                                          # Game window is called in order to be constantly updated and drawn.
    clock.tick(60)                                                         # Sets the fps to 60 to ensure little to no lag in the program.
    pygame.time.delay(10)                                                  # Pauses the game for 10 miliseconds.

    win.blit(spaceImage, (0, 0))                                           # Blits the the background of the game.

    try: 
        highScore = int(getHighScore())                                    # Sets the high score to receive input.
    except:
        highScore = 0                                                      # If not, leaves it at zero.

    for event in pygame.event.get():                                       # Checks for any pygame events.
        if event.type == pygame.QUIT:                                      # Checks to see if user clicks on the window's 'X' button
                inGame = False                                             # Exits from the program.
        
        if event.type == pygame.KEYDOWN:                                   # If the user presses any key on their keyboard.
            if event.key == pygame.K_ESCAPE:                               # If user clicks on the 'ESC' button.
                inGame = False                                             # Exits from the program.

            if event.key == pygame.K_b:                                    # If user clicks on 'b' button.
                currentScreen = 1                                          # Sets currenScreen to one.

                alienNumber = 25                                           # Ensures all 25 aliens are present.
                alien_x = []                                               # Resets the alien_x list.
                alien_y = []                                               # Resets the alien_y list.
                alien_Xchange = []                                         # Resets the alien_Xchange list.
                alien_Ychange = []                                         # Resets the alien_Ychange list.
                for num in range(alienNumber):      
                    alien_x.append(random.randint(64, 737))                # Appends random x-coordinates to the aliens.
                    alien_y.append(random.randint(30, 180))                # Appends random y-coordinates to the aliens.
                    alien_Xchange.append(speed)                            # Sets the speed of the alien.
                    alien_Ychange.append(random.randint(30, 100))          # Sets a random Y-coordinate change for the aliens.
                spaceship_x = 370                                          # Resets the spaceship to its original x-coordinate.
                spaceship_y = 523                                          # Resets the spaceship to its original y-coordinate.
                score = 0                                                  # Resets the gaem score to zero.
                
            if event.key == pygame.K_p:
                alienNumber = 25                                           # Ensures all 25 aliens are present.
                alien_x = []                                               # Resets the alien_x list.
                alien_y = []                                               # Resets the alien_y list.
                alien_Xchange = []                                         # Resets the alien_Xchange list.
                alien_Ychange = []                                         # Resets the alien_Ychange list.
                for num in range(alienNumber):      
                    alien_x.append(random.randint(64, 737))                # Appends random x-coordinates to the aliens.
                    alien_y.append(random.randint(30, 180))                # Appends random y-coordinates to the aliens.
                    alien_Xchange.append(speed)                            # Sets the speed of the alien.
                    alien_Ychange.append(random.randint(30, 100))          # Sets a random Y-coordinate change for the aliens.

                spaceship_x += spaceship_Xchange                           # Ensures the x-coordinates of the spaceship changes.
                moveAliens(alien_x, alien_y, alien_Xchange, alien_Ychange, alienNumber, speed) # Calls the function of moveAliens.
                moveLaser(lasers, laser_Ychange)                           # Calls the function of moveLaser.
                checkCollision(spaceship_x, alien_x, spaceship_y, alien_y) # Calls the function of checkCollision.
                moveSpaceship(spaceship_x, spaceship_y)                    # Calls the function of moveSpaceship.
                score = 0                                                  # Resets the game score to zero.
                
            if event.key == pygame.K_LEFT and currentScreen in [3, 4, 5]:  # If the user presses the arrow left key and if it is in the current Screen of 3, 4, or 5.
                spaceship_x -= spaceship_Xchange                           # Decreases the X-coordinate of the spaceship to make it move left.
                
            if event.key == pygame.K_RIGHT and currentScreen in [3, 4, 5]: # If the user presses the arrow right key and if it is in the current Screen of 3, 4, or 5.
                spaceship_x += spaceship_Xchange                           # Increases the X-coordinate of the spaceship to make it move right.
                
                if spaceship_x <= 0:      
                    spaceship_x = 0                                        # Ensures the spaceship does not leave the screen to the left by setting its x-coordinate to zero if it becomes less then zero.
                if spaceship_x >= 736:
                    spaceship_x = 736                                      # Ensures the spaceship does not leave the screen to the right by setting its x-coordinate to 736 if it becomes more than 736.
                            
                spaceship(spaceship_x, spaceship_y)                        # Calls the soaceship function.

            if event.key == pygame.K_a and currentScreen in [3, 4, 5]:     # If the user presses the 'a' key and if it is in the current Screen of 3, 4, or 5.
                spaceship_x -= spaceship_Xchange                           # Decreases the X-coordinate of the spaceship to make it move left.

            if event.key == pygame.K_d and currentScreen in [3, 4, 5]:     # If the user presses the 'd' key and if it is in the current Screen of 3, 4, or 5.
                spaceship_x += spaceship_Xchange                           # Increases the X-coordinate of the spaceship to make it move right.
                
                if spaceship_x <= 0:
                    spaceship_x = 0                                        # Ensures the spaceship does not leave the screen to the left by setting its x-coordinate to zero if it becomes less then zero.
                if spaceship_x >= 736:
                    spaceship_x = 736                                      # Ensures the spaceship does not leave the screen to the right by setting its x-coordinate to 736 if it becomes more than 736.
                            
                spaceship(spaceship_x, spaceship_y)                        # Calls the soaceship function.
    
            if event.key == pygame.K_SPACE and currentScreen in [3, 4, 5]: # If the user presses the space bar 'key' and the game is in current screen 3, 4, or 5.
                laser_x = spaceship_x                                      # The x-coordinate of the laser equals the x-coordinate of the spaceship.
                laser_y = spaceship_y                                      # The y-coordinate of the laser equals the y-coordinate of the spaceship.
                lasers.append([laser_x, laser_y])                          # Appends the x and y coordinates of the laser to the screen using its image.
                laserShot.play()                                           # Plays a sound that sounds like a laser being blasted.
                
        if event.type == pygame.KEYUP:                                     # If the user is not pressing any keys.
            spaceship_Xchange = 30                                         # The spaceship_Xchange becomes 30.

        if event.type == pygame.MOUSEBUTTONDOWN:                           # If the suer clicks anywhere on the game window (win).
            clickPos = pygame.mouse.get_pos()                              # Recognizes the mouse position on the screen in which it clicked.

            if highScore < alienNumber:                                    # If the high score is less than the alien number.
                highScore = alienNumber                                    # High score becomes the same to the alien number.
            with open('highscoregame.text','w') as f:                      # Opens the title file and sets the variable f.
                f.write(str(highScore))                                    # The variable f write the high score using a string in the text file.
            showHighScore(highScore)                                       # Shows the high score by calling the high score function in its parameters.
 
            if currentScreen == 1:                                         # If the user is on the first game screen.
                cat = catClickBtn(clickPos,catButtons)                     # Ensures and determines which main menu category the user clicked.
                if cat != 1:                                               # If the user did not click the background.
                 currentScreen = 2                                         # User clicks on play game and the screen changes to the level choice page (currentScreen 2).

                elif cat == 1:                                             # If the user clicks on quit game button.
                    inGame = False                                         # It exits from the program.

            elif currentScreen == 2:                                       # If the user clicks on the second game screen.
                cat = catClickBtn(clickPos,catButtons2)                    # Ensures and determines which level difficulty category the user clicked.
               
                if cat == 0:                                               # If user clicked on easy mode.
                    currentScreen = 3                                      # Takes user to the easy mode screen (currentScreen 3).

                elif cat == 1:                                             # If user clicked on hard mode.
                    currentScreen = 4                                      # Takes user to the hard mode screen (currentScreen 4).

                elif cat == 2:                                             # If the user clicked on impossible mode.
                    currentScreen = 5                                      # Takes user to impossiblee mode screen (currentScreen 5).

            elif currentScreen == 3:                                       # If the user clicks on the third game screen.
                moveAliens(alien_x, alien_y, alien_Xchange, alien_Ychange, alienNumber, speed) # Calls the moveAliens function so aliens can move.
                moveLaser(lasers, laser_Ychange)                                               # Calls the moveLaser function so lasers can move.                       
                checkCollision(spaceship_x, alien_x, spaceship_y, alien_y)                     # Calls the checkCollision functions to see if the spaceship and aliens collide.
                moveSpaceship(spaceship_x, spaceship_y)                                        # Calls the moveSpaceship function so the spaceship can move.
 
            elif currentScreen == 4:                                       # If the user clicks on the fourth game screen.
                moveAliens(alien_x, alien_y, alien_Xchange, alien_Ychange, alienNumber, speed) # Calls the moveAliens function so aliens can move.
                moveLaser(lasers, laser_Ychange)                                               # Calls the moveLaser function so lasers can move.                       
                checkCollision(spaceship_x, alien_x, spaceship_y, alien_y)                     # Calls the checkCollision functions to see if the spaceship and aliens collide.
                moveSpaceship(spaceship_x, spaceship_y)                                        # Calls the moveSpaceship function so the spaceship can move.

            elif currentScreen == 5:                                       # If the user clicks on the fifth game screen.
                moveAliens(alien_x, alien_y, alien_Xchange, alien_Ychange, alienNumber, speed) # Calls the moveAliens function so aliens can move.
                moveLaser(lasers, laser_Ychange)                                               # Calls the moveLaser function so lasers can move.                       
                checkCollision(spaceship_x, alien_x, spaceship_y, alien_y)                     # Calls the checkCollision functions to see if the spaceship and aliens collide.
                moveSpaceship(spaceship_x, spaceship_y)                                        # Calls the moveSpaceship function so the spaceship can move.

            pygame.display.update()                                         # Constantly updates pygame display.

pygame.quit()                                                               # Quits pygame.
