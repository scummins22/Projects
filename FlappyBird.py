import random

import pygame
from pygame.locals import *

pygame.init()

#clock
clock = pygame.time.Clock()

#frames per second
FPS = 60

#screen size variables
screen_width = 864
screen_height = 936

#screen variable
screen = pygame.display.set_mode((screen_width, screen_height))

#game title
pygame.display.set_caption('Flappy Bird')

#load images
bg = pygame.image.load('images/bg.png')
ground = pygame.image.load('images/ground.png')
bird1 = pygame.image.load('images/bird1.png')
bird2 = pygame.image.load('images/bird2.png')
bird3 = pygame.image.load('images/bird3.png')
pipe = pygame.image.load('images/pipe.png')
restart = pygame.image.load('images/restart.png')

#game variables
ground_x_pos = 0
moving_speed = 2.5
fly = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False
high_score = 0
def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height/2)
    score = 0
    return score
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.index = 0
        self.counter = 0
        pygame.sprite.Sprite.__init__(self)
        self.images = [bird1, bird2, bird3]
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        if game_over == False:

            if fly == True:
                #if the mouse is clicked and released, the bird will go up
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    self.vel = -8

                #if the mouse is not clicked, the bird will go down
                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False
                self.vel += 0.5
                if self.vel > 8:
                    self.vel = 8

                if self.rect.bottom <= 768:
                    self.rect.y += self.vel

                if self.rect.bottom >= 768:
                    self.rect.bottom = 768
            self.counter += 1
            cooldown = 5

            #animate the bird
            if self.counter > cooldown:
                self.counter = 0
                self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

            #rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -1.5)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        #create pipe image and make it skinnier
        self.image = pipe
        self.image = pygame.transform.scale(pipe, (int(screen_width/10), int(screen_height/2)))
        self.rect = self.image.get_rect()

        #position 1 is top, position -1 is bottom
        if position == 1:
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect.bottomleft = [x, y - int(pipe_gap/2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap/2)]

    def update(self):
        if game_over == False:
            self.rect.x -= moving_speed
            if self.rect.right < 0:
                self.kill()

        self.rect.x -= moving_speed

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw(self):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        #draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height/2))
bird_group.add(flappy)

button = Button(int(screen_width/2) - 190, int(screen_height/2) - 100, restart)

run = True
while run:


    clock.tick(FPS)


    #draw background
    screen.blit(bg, (0,0))

    #draw bird
    bird_group.draw(screen)
    bird_group.update()

    pipe_group.draw(screen)

    screen.blit(ground, (ground_x_pos, 768))

    # display score and high score side by side at the top
    score_font = pygame.font.Font('flappy-font.ttf', 40)
    score_surface = score_font.render("Score: "f'{int(score)}', True, (255,255,255))
    high_score_surface = score_font.render("High Score: "f'{int(high_score)}', True, (255,255,255))

    # Make a rectangle for the score to display on the top left of the screen
    score_rect = score_surface.get_rect(topleft=(10, 10))

    # Make a rectangle for the high score to display on the top right of the screen
    high_score_rect = high_score_surface.get_rect(topright=(screen_width - 10, 10))

    screen.blit(score_surface, score_rect)
    screen.blit(high_score_surface, high_score_rect)





    #check score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
    if score > high_score:
        high_score = score






    #check if bird collides with pipe
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    #check if bird collides with ground
    if flappy.rect.bottom >= 768:
        game_over = True
        fly = False

    if game_over == False and fly == True:

        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            bottom_pipe = Pipe(screen_width, int(screen_height / 2)+pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2)+pipe_height, 1)
            pipe_group.add(bottom_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        ground_x_pos -= moving_speed
        if(ground_x_pos <= -35):
            ground_x_pos = 0

        pipe_group.update()

    #check if mouse is clicked
    if pygame.mouse.get_pressed()[0] == 1:
        fly = True

    if game_over == True:
        #draw button & check if mouse is clicked
        if button.draw() == True:
            #reset game variables
            game_over = False
            score = reset_game()



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and fly == False and game_over == False:
            fly = True
    pygame.display.update()
    
pygame.quit()