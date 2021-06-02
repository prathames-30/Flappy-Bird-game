import pygame
from pygame.locals import *
import random

pygame.init() #initialise pygame
# To not quickly just finish the running
clock = pygame.time.Clock()
fps = 60


screen_width = 864
screen_height = 900

screen = pygame.display.set_mode((screen_width,screen_height)) #initialize the gaming window

pygame.display.set_caption('Flappy Bird') # set the caption

# define font
font = pygame.font.SysFont('Bauhaus 93',60)

#define colour
white = (255,255,255)


#Define the game variables here
ground_scroll = 0 #we need the ground to move hence it starts from 0
scroll_speed = 4 # with a speed of 4 pixels/sec
flying = False # game starts only on mouse click.
game_over = False # when bird hits then game is done
pipe_gap = 150 #defines gap between the two pipes
pipe_frequency = 1500 #frequency in milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency #keeps a check when was the last pipe encountered initialized to when game had started
score = 0 #shows how many pipes we passed
pass_pipe = False # A trigger to check if we have passed a pipe

# load the background images
bg = pygame.image.load('C:/Users/lenovo/OneDrive - Indian Institute of Technology Guwahati/Desktop/Flappy Bird/Images/bg.png')
ground_img = pygame.image.load('C:/Users/lenovo/OneDrive - Indian Institute of Technology Guwahati/Desktop/Flappy Bird/Images/ground.png')
button_img = pygame.image.load('C:/Users/lenovo/OneDrive - Indian Institute of Technology Guwahati/Desktop/Flappy Bird/Images/restart.png')

def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = screen_height//2
    score = 0
    return score

class Bird(pygame.sprite.Sprite): #We use the pygames sprite class
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        #we animate here
        self.images = []
        self.index = 0 #which index we would be showing at a particular time, we start of with 0.
        self.counter = 0 # controls the speed at which the animation runs
        for num in range(1,4):
            img = pygame.image.load(f'C:/Users/lenovo/OneDrive - Indian Institute of Technology Guwahati/Desktop/Flappy Bird/Images/bird{num}.png')
            self.images.append(img)

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False
    def update(self):
        #handle the animation
        if flying == True:
            # Gravity taking the bird down
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)
            """ if self.rect.bottom >= 768 and self.vel < 0:
                self.rect.y += int(self.vel) """
        if game_over == False:
            # jump when mouse is clicked 
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.vel = -10
                self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            
            self.counter+=1
            flap_cooldown = 5
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index+=1
                if self.index >= len(self.images):
                    self.index = 0

            self.image = self.images[self.index]

            # Rotating the bird with respect to its velocity
            self.image = pygame.transform.rotate(self.images[self.index], -2*self.vel)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('C:/Users/lenovo/OneDrive - Indian Institute of Technology Guwahati/Desktop/Flappy Bird/Images/pipe.png')
        self.rect = self.image.get_rect()
        #we keep position = 1 if pipe is from top and position = -1 if it is from bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image,False,True) #first false is for x axis and second true for y axis since we have to flip acc to y axis
            self.rect.bottomleft = [x,y - int(pipe_gap/2)]
        if position == -1:
            self.rect.topleft = [x,y + int(pipe_gap/2)]
        
    def update(self):
        self.rect.x-=scroll_speed  # to make the pipes also move
        if self.rect.x < -5:
            self.kill()

#The restart button
class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos() #gives x,y coordinates of the mouse
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x,self.rect.y))
        return action
        

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, screen_height//2)
bird_group.add(flappy)

button = Button(screen_width//2 - 50,screen_height//2 - 100,button_img)

run = True
while run:
    clock.tick(fps) #fix speed to 60 frames per second
    screen.blit(bg, (0,0)) # start the image from 0,0
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    screen.blit(ground_img, (ground_scroll,768)) #start the ground from ground_scroll,768

    # Check and update the score
    if len(pipe_group) > 0: # we start checking only when pipes are created i.e game has started
        #first check is if the bird is between the pipe i.e in between two ends of the pipe
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        #second check if the bird has completely crossed the pipe
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    #display the score
    draw_text(str(score),font,white,screen_width//2,20)

    # check if bird hits the pipe
    if pygame.sprite.groupcollide(bird_group,pipe_group,False,False) or flappy.rect.top < 0: #if the first false were true bird would have been deleted and if second false were true the pipes would have been deleted
        game_over = True


    # check whether bird has hit the ground
    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False


    if game_over == False and flying == True:
        time_now = pygame.time.get_ticks() #finds current time
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100,100)
            btm_pipe = Pipe(screen_width,(screen_height//2)+pipe_height,-1)
            top_pipe = Pipe(screen_width,(screen_height//2)+pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
        
        ground_scroll-=scroll_speed #decrease the ground scroll by the scroll speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0 #reset the ground_scroll once it crosses the limit.
        pipe_group.update()

    if game_over == True:
        if button.draw() == True:
            game_over = False
            score = reset_game()


    for event in pygame.event.get(): # for all the events happeneing in the game
        if event.type == pygame.QUIT: #if we have to quit i.e. we cross the screen
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
    pygame.display.update()  # updates everything that has happened above

pygame.quit()


