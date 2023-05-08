'''
Emerson Smith 
CS 1410 X03
April 13th, 2023
Final Project

Here are the references I used for this project:
https://www.geeksforgeeks.org/snake-game-in-python-using-pygame-module/# 
https://www.youtube.com/watch?v=QFvqStqPCRU&t=4542s
https://www.youtube.com/watch?v=PHdZdrMCKuY
https://www.youtube.com/watch?v=AY9MnQ4x3zk&t=5104s
https://www.pygame.org/docs/ref/pygame.html
github.com/clear-code-projects/Snake - This was for the apple graphic
'''
import pygame
import sys
import random
from pygame.math import Vector2 as v

pygame.init()
snake_cell_size = 40
snake_cell_number = 20
width = 800
height = 800
snake_screen = pygame.display.set_mode((width, height))
snake_clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 80)
pygame.display.set_caption("Snake Game")

#Snake class, this includes the body, location, and how the snake moves.
class Snake:
    def __init__(self):
        self.body = []
        self.body.append(v(5,10))
        self.body.append(v(4,10))
        self.body.append(v(3,10))
        self.direction = v()
        self.direction.x , self.direction.y = 1, 0
        self.new_snake_block = False
        self.score = 0


    def draw_snake(self):
        for i in range(len(self.body)):
            snake_block = self.body[i]
            snake_x_pos = int(snake_block.x * 40)
            snake_y_pos = int(snake_block.y * 40)
            snake_rectangle = pygame.Rect(snake_x_pos, snake_y_pos, snake_cell_size, snake_cell_size)
            pygame.draw.rect(snake_screen, ("Blue"), snake_rectangle)
        
    def move_snake(self):
        if self.new_snake_block == True:
            snake_body_copy = []
            for i in range(len(self.body)):
                snake_body_copy.append(self.body[i])
            snake_body_copy.insert(0, v(self.body[0].x + self.direction.x, 
            self.body[0].y + self.direction.y))
            self.body = []
            for i in range(len(snake_body_copy)):
                self.body.append(snake_body_copy[i])
            self.new_snake_block = False
            self.add_score()
            print(f"Your score is: {self.score}")
        else:
            snake_body_copy = self.body[:-1]
            snake_body_copy.insert(0, snake_body_copy[0] + self.direction)
            self.body = snake_body_copy[:]
        return snake_body_copy

    def add_body(self):
        self.new_snake_block = True

    def add_score(self):
        self.score += 1



#This class controls the random placement of the apple
class Apple:
    def __init__(self):
        self.randomize()

    def draw_apple(self):
        x_pos_apple = self.position.x * 40
        y_pos_apple = self.position.y * 40
        apple_rect = pygame.Rect(x_pos_apple, y_pos_apple, snake_cell_size, snake_cell_size)
        for i in range(snake_cell_size):
            for j in range(snake_cell_size):
                snake_screen.blit(apple, apple_rect)

    #Randomize the position of the apple
    def randomize(self):
        fruit_placement = 20 - 1
        self.x , self.y = random.randint(0, fruit_placement), random.randint(0, fruit_placement)
        self.position = v(self.x, self.y)

#Main class is where we update the snake position and the collision,
class Main:
    def __init__(self):
        self.snake = Snake()
        self.apple = Apple()
    
    def events(self):
        while True:
            for event in pygame.event.get():
                snake_screen.fill((175, 215, 70))
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == SCREEN_UPDATE:
                    snake_game.update()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if snake_game.snake.direction.y != 1:
                            snake_game.snake.direction = v(0,-1)
                    if event.key == pygame.K_DOWN:
                        if snake_game.snake.direction.y != -1:
                            snake_game.snake.direction = v(0,1)
                    if event.key == pygame.K_LEFT:
                        if snake_game.snake.direction.x != 1:
                            snake_game.snake.direction = v(-1,0)
                    if event.key == pygame.K_RIGHT:
                        if snake_game.snake.direction.x != -1:
                            snake_game.snake.direction = v(1,0)
                
                snake_game.draw_stuff()
                pygame.display.update()

    #Calls the methods to draw the apple and the snake
    def draw_stuff(self):
        self.apple.draw_apple()
        self.snake.draw_snake()
    
    #Updates the next position of the snake or if there's a game over
    def update(self):
        self.snake.move_snake()
        self.crash()
        self.lose()

    def lose(self):
        x, y = self.snake.body[0].x, self.snake.body[0].y
        if x < 0:
            self.game_over()
        else:
            if x >= snake_cell_number:
                self.game_over()
            else:
                if y < 0:
                    self.game_over()
                else:
                    if y >= snake_cell_number:
                        self.game_over()
        for i in range(1, len(self.snake.body)):
            if self.snake.body[i] == self.snake.body[0]:
                self.game_over()
            
    #Checks if the player has hit a wall or the snakes body
    def crash(self):
        if self.apple.position == self.snake.body[0]:
            self.apple.randomize()
            self.snake.add_body()

    def game_over(self):
        s = Snake()
    # Set up the font and text to display on the game over screen
        font = pygame.font.SysFont("arialblack", 64)
        text = font.render("GAME OVER", True, ("Black"))
        text_rect = text.get_rect(center=(400,150))
        snake_screen.fill("White")
        snake_screen.blit(text, text_rect)
        image = pygame.image.load("Graphics/snake.png").convert_alpha()
        image_resize = pygame.transform.scale(image, (500, 500))
        snake_screen.blit(image_resize, (150, 310))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

snake_game = Main()
snake_game.events()