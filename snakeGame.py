import pygame
import time
import random

pygame.init()

#RGB
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)

display_x = 800
display_y = 600

#screen resolution as tuple
gameDisplay = pygame.display.set_mode((display_x,display_y))

#title
pygame.display.set_caption('TestSnake')

clock = pygame.time.Clock()

smallfont = pygame.font.SysFont(None,25)
medfont = pygame.font.SysFont(None,50)
largefont = pygame.font.SysFont(None,80)

def main():
    game_intro()
    gameLoop()
    

def pause():
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False;

                if event.key == pygame.K_q:
                    main()

        gameDisplay.fill(black)
        msgScreen("Paused", white, -100, size= "large")
        msgScreen("Press ESC to continue or Q to quit", white, 25, size= "medium")

        pygame.display.update()
        clock.tick(15)

def game_intro():
    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        
        gameDisplay.fill(black)
        
        msgScreen("Welcome to Snake",red,-100,"large")
        msgScreen("The objective of the game is to control the snake with arrow keys and pick up apples",white, -30)
        msgScreen("Press P to play or ESC to pause or Q to quit",white, 20, "medium")

        pygame.display.update()
        clock.tick(15)


def randAppleGen(snake_size):
    randAppleX = round(random.randrange(0,(display_x-snake_size)/10.0)*10.0)
    randAppleY = round(random.randrange(0,(display_y-snake_size)/10.0)*10.0)
    return randAppleX,randAppleY

    
def score(score):
    text = smallfont.render("Score: " + str(score),True, white)
    gameDisplay.blit(text, [0,0])

def snake(snake_size, snakeList):
    for XandY in snakeList:
        pygame.draw.rect(gameDisplay, white, [XandY[0],XandY[1],snake_size ,snake_size])

def text_objects(text, color,size):
    #render the font with the color
    if size == "small":
        textSurface = smallfont.render(text,True,color)
    if size == "medium":
        textSurface = medfont.render(text,True,color)
    if size == "large":
        textSurface = largefont.render(text,True,color)
    return textSurface, textSurface.get_rect()

#displace to skip lines 
def msgScreen(msg,color,y_displace=0,size = "small"):
    
    textSurface, textRect = text_objects(msg, color, size)
    #centers text
    textRect.center = (display_x/2),(display_y/2)+y_displace
    #write text in the middle of temp_rect^
    gameDisplay.blit(textSurface, textRect)

def gameLoop():

    snakeList = []
    snakeLength = 1;
    snake_size = 10
    FPS = 30
    gameExit = False;
    gameOver = False;
    
    lead_x = display_x/2
    lead_y = display_y/2

    lead_x_change = 0;
    lead_y_change = 0;

    randAppleX, randAppleY = randAppleGen(snake_size)

    #randomize spawn of pickup/apple //rounding it making it possible for snake to
    #hit it everytime since snake always go multiples of 10 //math just for rounding
    
    while not gameExit:

        while gameOver == True:
            gameDisplay.fill(white)
            msgScreen("Game Over",red,y_displace = -50, size = "large")
            msgScreen("Press P to play again or Q to quit", black, size = "medium")
            msgScreen("Final Score: " + str(snakeLength-1) ,black,y_displace = 50, size = "medium")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True;
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                        main()
                        
                    if event.key == pygame.K_p:
                        gameLoop()
                        
        #gets every event mouse movement/keyboard possible
        for event in pygame.event.get():
            #QUIT is a pygame type look online
            if event.type == pygame.QUIT:
                gameExit = True;
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -snake_size ;
                    lead_y_change = 0;
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = snake_size ;
                    lead_y_change = 0;
                elif event.key == pygame.K_UP:
                    lead_y_change = -snake_size ;
                    lead_x_change = 0;
                    
                elif event.key == pygame.K_DOWN:
                    lead_y_change = snake_size ;
                    lead_x_change = 0;

                elif event.key == pygame.K_ESCAPE:
                    pause()

        if lead_x >= display_x or lead_x < 0 or lead_y >= display_y or lead_y < 0:
            gameOver = True
                

        lead_x += lead_x_change
        lead_y += lead_y_change

        #background black
        gameDisplay.fill(black)

        score(snakeLength-1)

        #creating snake head, then the body
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            #deletes the list so snake wont grow infinite without getting apple
            del snakeList[0]

        #go through everything up to last element/snake head
        for eachSnakePart in snakeList[:-1]:
            if eachSnakePart == snakeHead:
                gameOver = True;
        snake(snake_size, snakeList)
        
        pygame.draw.rect(gameDisplay, red, [randAppleX,randAppleY,snake_size,snake_size])
        pygame.display.update()

        #if snake touches apple respawn apple and update everything else
        if(lead_x == randAppleX and lead_y == randAppleY):
            randAppleX,randAppleY = randAppleGen(snake_size)
            snakeLength +=1
            

        #framesPerSec
        clock.tick(FPS)
                  
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
