from ast import While
from collections import namedtuple
from enum import Enum
import pygame
import random
pygame.init()

BLOCK_WIDTH = 20
FRAME_RATE = 20

#COLORS
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0, 0, 255)
RED = (200,0,0)

font  = pygame.font.SysFont("Aria", 23)

#coordiantes
Point = namedtuple("Point",["x","y"])

#Directions available
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    

#class implementing the game environemt
class SnakeGame:
    
    def __init__(self,width=600,height=400):
        self.w = width #width of window
        self.h = height # height of window
        self.window = pygame.display.set_mode((self.w, self.h)) #create main window
        pygame.display.set_caption("Navid's Snake Game") #give title
        self.clock = pygame.time.Clock() # for keeping time
        self.direction = Direction.RIGHT # Defualt initila direction
        self.snake_head = Point(((self.w) //(2 * BLOCK_WIDTH)) * BLOCK_WIDTH, ((self.h) //(2 * BLOCK_WIDTH)) * BLOCK_WIDTH) # initial coordinates of head of snake
        # whole body of snake (top left corner of each block)/ initially contians only 3 blocks
        self.snake_body = [self.snake_head, #head
                           Point(self.snake_head.x - BLOCK_WIDTH,self.snake_head.y), # first left square
                           Point(self.snake_head.x - 2*BLOCK_WIDTH,self.snake_head.y)] # second left square
        self.score = 0
        self.isOver = False
        self.food = self.__random_food()
        
    #randomly place food, excludes edges
    def __random_food(self):
        
        food = Point(random.randint(0, ((self.w - BLOCK_WIDTH) //BLOCK_WIDTH ))* BLOCK_WIDTH, #x
                     random.randint(0, ((self.h - BLOCK_WIDTH) //BLOCK_WIDTH ))* BLOCK_WIDTH) #y
        if food in self.snake_body:
            return self.__random_food()
        
        else:
            return food
        
    #main play function causing snake to move
    def play(self):
        
        self.__update_screen()
        self.clock.tick(FRAME_RATE)
        
        #get user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if red x is clicked for closing
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
                    
        # move snake based on direction given
        self.__move_head()
        
        # if collision happened
        if self.isOver:
            return self.score, self.isOver
            
        self.__update_screen()
        self.clock.tick(FRAME_RATE)
        return self.score, self.isOver
            
            
    # move to new position based on input
    def __move_head(self):
        x = self.snake_head.x
        y = self.snake_head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_WIDTH
        elif self.direction == Direction.LEFT:
            x -= BLOCK_WIDTH
        elif self.direction == Direction.UP:
            y -= BLOCK_WIDTH
        elif self.direction == Direction.DOWN:
            y += BLOCK_WIDTH
            
        p = Point(x,y) # new head
            
        #termination case borders or collide with self
        if x<0 or x> self.w - BLOCK_WIDTH or y<0 or y> self.h - BLOCK_WIDTH or p in self.snake_body:
            self.isOver = True
            return
            
        self.snake_body.insert(0,p) #insert at front
        
        self.snake_head = p # update head
                   
        #Food is eaten
        if self.food == self.snake_head:
            self.score += 1
            self.food = self.__random_food() # renew food
            self.__update_screen()
            
        else:
            self.snake_body.pop() # remove last one, indicating movement
            
        
        
    #draws snake, food, and score
    def __update_screen(self):
        self.window.fill(BLACK)
        for item in self.snake_body:
            pygame.draw.rect(self.window, WHITE, pygame.Rect(item.x, item.y, BLOCK_WIDTH, BLOCK_WIDTH)) # draw each block
            pygame.draw.rect(self.window, BLACK, pygame.Rect(item.x, item.y, 1, BLOCK_WIDTH)) # draw lines separating squares
            pygame.draw.rect(self.window, BLACK, pygame.Rect(item.x, item.y, BLOCK_WIDTH, 1)) # draw lines separating squares
        pygame.draw.rect(self.window, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_WIDTH, BLOCK_WIDTH)) # draw food
        text = font.render(f"Score: {self.score}",True,WHITE) #show text score
        self.window.blit(text,(self.w //2 -18, 0))
        pygame.display.flip()       
        
        
        
#Main function for the game
def main():
    width = 600
    height = 400
    game = SnakeGame(width,height)
    
    while(True):
        game.play()
        if game.isOver:
            break
        
    print(f"Your Score is {game.score}.")
    pygame.quit()
    

#run as main 
if __name__ == "__main__":
    main()