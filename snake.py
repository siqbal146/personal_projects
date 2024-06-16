# Sadaf Iqbal
# 6/14/2024
# Snake base code from Coder Space on YT: https://www.youtube.com/watch?v=_-KjEgCLQFw
# Goal: understand base code, and be able to make modifications to the final game independently

# my modifications: 
# adjusted screen display to include a border and a score board, and added score counter
# increase game speed as score increases 
# added start text and game over text
# added a key/movement queue so user can't turn around too fast and run into themselves
# added eyes to the snake :)

# issues: 
# to add: bombs (explode after 5sec, if tail is in radius it breaks tail, break wall? (big task), bomb visuals), instructions?

import pygame as pg #pygame library
from random import randrange #specifically import randrange function from random module
from collections import deque
pg.font.init()

TILE_SIZE = 30 #tile size for the grid
GAME_WINDOW = 690
BORDER_SIZE = 5
SCORE_BOARD = 50
SCREEN_WIDTH = GAME_WINDOW + BORDER_SIZE*2
SCREEN_HEIGHT = GAME_WINDOW + BORDER_SIZE*2 + SCORE_BOARD
#tuples that define the range for the random coordinates of tile centers on the grid
RANGE_H = (BORDER_SIZE + TILE_SIZE//2, SCREEN_WIDTH - BORDER_SIZE - TILE_SIZE//2, TILE_SIZE) #horizontal range
RANGE_V = (SCORE_BOARD + BORDER_SIZE + TILE_SIZE//2, SCREEN_HEIGHT - BORDER_SIZE - TILE_SIZE//2, TILE_SIZE) #vertical range
get_random_position = lambda: [randrange(*RANGE_H), randrange(*RANGE_V)] #create a random position function using the RANGE tuple

#define the parameters of the snake
snake = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2]) #define the head of the snake. the -2 shrinks the size so you get the border around the pixel
snake.center = get_random_position() #define snake head random position on grid
length = 1 #length of snake
segments = [snake.copy()] #list where snake segments will be stored. first segment is placed as a copy
#rect(x,y,width,height)
eye_size = 5
eye1 = pg.Rect(segments[0][0]+5,segments[0][1]+5,eye_size,eye_size)
eye2 = pg.Rect(segments[0][0]+TILE_SIZE-12,segments[0][1]+5,eye_size,eye_size)
#movement parameters/objects
snake_dir = (0,0) #define a direction for the snake to make it move
move_queue = deque() #create queue to store upcoming moves
opp_keys = {pg.K_w: pg.K_s, pg.K_a: pg.K_d, pg.K_s: pg.K_w, pg.K_d: pg.K_a} #match opposite keys for the key tracker (can't hit s if moving in w direction)
available_dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1} #use this direction to prevent the snake from moving back on itself (if going in d direction, don't do anything when user hits a)
move_dirs = {pg.K_w: (0, -TILE_SIZE), pg.K_s: (0, TILE_SIZE), pg.K_a: (-TILE_SIZE, 0), pg.K_d: (TILE_SIZE, 0)} #directions associated with each keystroke 

#control speed of snake
time, time_step = 0, 110 #time step is delay in ms

#define variables to determine the food for the snake
food = snake.copy() #use copy of the snakes head to make the food variable (since it looks the same anyway)
food.center = get_random_position() #assign food a random position

screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]) #create a screen with given resolution
clock = pg.time.Clock() #create instance of clock class to set frame rate
font = pg.font.SysFont('ocraextended', 36) #set up font object

score = 0 #initialize score to 0

#main loop of the program
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT: #first check for closing the app
            exit()
        if event.type == pg.KEYDOWN: #control the direction of the snake with WASD
            if event.key == pg.K_w and available_dirs[pg.K_w]: #check the event for key press. no dir change if dictionary val is 0
                available_dirs = {x:1 for x in available_dirs} #reset all directions to "available"
                available_dirs[opp_keys[pg.K_w]] = 0 #make opposite direction unavailable
                move_queue.append(pg.K_w) #movements are added to a queue, this way user can't change too fast (if going in d direction, then hit w and a quickly, don't want snake to run into itself)
            if event.key == pg.K_s and available_dirs[pg.K_s]:
                available_dirs = {x:1 for x in available_dirs}
                available_dirs[opp_keys[pg.K_s]] = 0
                move_queue.append(pg.K_s)
            if event.key == pg.K_a and available_dirs[pg.K_a]:
                available_dirs = {x:1 for x in available_dirs}
                available_dirs[opp_keys[pg.K_a]] = 0
                move_queue.append(pg.K_a)               
            if event.key == pg.K_d and available_dirs[pg.K_d]:
                available_dirs = {x:1 for x in available_dirs}
                available_dirs[opp_keys[pg.K_d]] = 0
                move_queue.append(pg.K_d)

    #set up the window
    screen.fill((0,0,0)) #paint surface black with 'black'. can choose specific color with RGB (max val is 255)
    #draw borders
    pg.draw.line(screen,(255,255,255),[BORDER_SIZE//2,0],[BORDER_SIZE//2,SCREEN_HEIGHT],BORDER_SIZE) #left border
    pg.draw.line(screen,(255,255,255),[SCREEN_WIDTH-BORDER_SIZE//2,0],[SCREEN_WIDTH-BORDER_SIZE//2,SCREEN_HEIGHT],BORDER_SIZE) #right border
    pg.draw.line(screen,(255,255,255),[0,BORDER_SIZE//2],[SCREEN_WIDTH,BORDER_SIZE//2],BORDER_SIZE) #top border
    pg.draw.line(screen,(255,255,255),[0,SCREEN_HEIGHT-BORDER_SIZE//2],[SCREEN_WIDTH,SCREEN_HEIGHT-BORDER_SIZE//2],BORDER_SIZE) #bottom border
    pg.draw.line(screen,(255,255,255),[0,SCORE_BOARD+BORDER_SIZE//2],[SCREEN_WIDTH,SCORE_BOARD+BORDER_SIZE//2],BORDER_SIZE) #score board border

    #Game over: check borders and snake tail position
    self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1 #function to check if snakes head collides with rest of it's body. it will be true when a collision is detected
    if snake.left < BORDER_SIZE or snake.right > (SCREEN_WIDTH-BORDER_SIZE) or snake.top < (SCORE_BOARD+BORDER_SIZE) or snake.bottom > (SCREEN_HEIGHT-BORDER_SIZE) or self_eating:
        game_over = font.render('GAME OVER :(',True,('red'))
        end_score = font.render(f'SCORE: {score}', True,('yellow'))
        continue_text = font.render('Press any key to try again',True,('yellow'))
        end_score_rect = end_score.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2)) #center score on screen
        game_over_rect = game_over.get_rect(midbottom=(SCREEN_WIDTH//2,end_score_rect.top)) #display game over above score
        continue_text_rect = continue_text.get_rect(midtop=(SCREEN_WIDTH//2,end_score_rect.bottom)) #display continue text below score
        screen.blit(end_score,end_score_rect), screen.blit(game_over,game_over_rect), screen.blit(continue_text,continue_text_rect)
        pg.display.flip() #update the screen
        while event.type != pg.KEYDOWN: #wait for user to press key before restarting the game
            event = pg.event.wait()
            if event.type == pg.QUIT:
                exit()
        snake.center, food.center = get_random_position(), get_random_position() #reset snake and food in random position
        length, snake_dir = 1, (0,0) #reduce snake length to 1, pause snake movement
        segments = [snake.copy()] #reset snake segments
        eye1 = pg.Rect(segments[0][0]+5,segments[0][1]+5,eye_size,eye_size) #reset eye position
        eye2 = pg.Rect(segments[0][0]+TILE_SIZE-12,segments[0][1]+5,eye_size,eye_size)
        available_dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1} #reset direction dict so you can start in any direction
        score = 0 #reset scored
        time_step = 110 #reset game speed
        

    #check positions of snake and food
    if snake.center == food.center:
        food.center = get_random_position()
        length +=1
        score +=1 #increment score
        if score%5 == 0 and score > 0 and time_step > 0: #increase game speed every 5 points
            time_step -= 10
    food_in_tail = pg.Rect.collidelist(food, segments[:-1]) != -1 #check if food is in snake body. true when food is in tail
    if food_in_tail:
        food.center = get_random_position()
    #draw food
    [pg.draw.rect(screen,(255,0,0), food)]
    #draw snake
    [pg.draw.rect(screen, (0,255,0), segment) for segment in segments] #list comprehension, go through segments and draw each 1 using the draw.rect function
    pg.draw.rect(screen,'black',eye1)
    pg.draw.rect(screen,'black',eye2)
    #start text, only show when snake isn't moving
    if snake_dir == (0,0):
        start_text = font.render('START GAME WITH WASD',True,(255,255,0))
        start_text_rect = start_text.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2))
        screen.blit(start_text,start_text_rect)

    #draw the score
    score_text = font.render(f'SCORE: {score}',True,(255,255,255))
    score_text_rect = score_text.get_rect(center=(SCREEN_WIDTH//2,SCORE_BOARD//2))
    screen.blit(score_text,score_text_rect)

    #move snake's head using move and place function
    #track time interval to define when snake takes next step
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        if move_queue:
            #snake direction, available_dirs
            key = move_queue.popleft()
            snake_dir = move_dirs[key] #adjust snake direction based on next keystroke
            
        time = time_now
        snake.move_ip(snake_dir)
        eye1.move_ip(snake_dir)
        eye2.move_ip(snake_dir)
        segments.append(snake.copy())
        segments = segments[-length:] #record path of snake and leave last steps by length of the snake

    pg.display.flip() #update the screen
    clock.tick(60) #set a delay to determine 60 fps


'''
Notes:

for display screen, top left is (0,0). this is why right is positive, but up is negative

what is a lambda function? https://www.youtube.com/watch?v=KR22jigJLok
lambda is a keyword in python: defining the anonymous function. EX:
standard function:
def add(x,y):
    return x+y

lambda function:
lambda x,y: x+y

lambda can only have single line expressions, whatever is computed in that line gets returned
anonymous function means you don't call it, they're not bound to an identifier
so you can assign it to a variable
add = lambda x,y: x+y 
add(4,5)
we could also just put the function and inputs in parentheses: (lambda x,y: x+y)(4,5)
what's the point of lambda functions? they're made to be passed into a higher order function
what's a higher order function? in basic terms, a function that can take in a function as an input, or return a function as an output
higher order function use is what lambda functions were made for
'''