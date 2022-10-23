import pygame   #pip install pygame
import numpy as np #pip install numpy
import time
import random

import speech_recognition as sr  # pip install speechrecognition

# directions variables for the input given
move_left=0
move_right=0
move_up=0
move_down=0

def speech():

    #funtion to take speech input and convert to text
    #returns a string "text"


    global text
    text=""
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak:")
        audio=r.listen(source)

        try:
            #requires internet
            text=r.recognize_google(audio)

            print("You said :",text)
        except sr.UnknownValueError:
            print("Could not understand that")

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
    return text

# funtion to detect wake words
def check():
    text=speech()

    if("l" in text):
        global move_left
        move_left=1
        print("move_left ",move_left)

    elif("h" in text ):
        global move_right
        move_right=1
        print("move_right ",move_right)

    elif("a"in text or "p" in text):
        global move_up
        move_up=1
        print("move_up",move_up)

    elif("n" in text):
        global move_down
        move_down=1
        print("move_down",move_down)


# check whether our snake collides with the apple
# if yes increase the score by 1
# position of apple is random

def collision_with_apple(apple_position, score):
    apple_position = [random.randrange(1,500)*10,random.randrange(1,500)*10]
    score += 1
    return apple_position, score

## if ou snake collides with boundary then return 1
def collision_with_boundaries(snake_head):
    if snake_head[0]>=500 or snake_head[0]<0 or snake_head[1]>=500 or snake_head[1]<0 :
        return 1
    else:
        return 0

## if collides with self then return 1 else return 0
def collision_with_self(snake_position):
    snake_head = snake_position[0]
    if snake_head in snake_position[1:]:
        return 1
    else:
        return 0

def is_direction_blocked(snake_position, current_direction_vector):
    next_step = snake_position[0]+ current_direction_vector
    snake_head = snake_position[0]
    if collision_with_boundaries(snake_head) == 1 or collision_with_self(snake_position) == 1:
        return 1
    else:
        return 0

def generate_snake(snake_head, snake_position, apple_position, button_direction, score):

    if button_direction == 1:
        snake_head[0] += 10
    elif button_direction == 0:
        snake_head[0] -= 10
    elif button_direction == 2:
        snake_head[1] += 10
    elif button_direction == 3:
        snake_head[1] -= 10
    else:
        pass

    if snake_head == apple_position:
        apple_position, score = collision_with_apple(apple_position, score)
        snake_position.insert(0,list(snake_head))

    else:
        snake_position.insert(0,list(snake_head))
        snake_position.pop()

    return snake_position, apple_position, score

def display_snake(snake_position):
    for position in snake_position:
        pygame.draw.rect(display,red,pygame.Rect(position[0],position[1],10,10))

def display_apple(display,apple_position, apple):
    display.blit(apple,(apple_position[0], apple_position[1]))

def play_game(snake_head, snake_position, apple_position, button_direction, apple, score):


    crashed = False

    current_direction_vector = np.array(snake_position[0])-np.array(snake_position[1])
    # prev_button_direction = 0
    # button_direction = 0
    while crashed is not True:

        for i in range (5):
            time.sleep(.25)
            clock.tick(10)

            display.fill(window_color)
            display_apple(display,apple_position,apple)
            display_snake(snake_position)

            snake_position, apple_position, score = generate_snake(snake_head, snake_position, apple_position, button_direction, score)
            pygame.display.set_caption("Snake Game"+"  "+"SCORE: "+str(score))
            pygame.display.update()
        prev_button_direction = 1
        button_direction = 1


        global move_down
        global move_up
        global move_right
        global move_left
        check()
        print(move_left)
        print(move_up)
        print(move_down)
        print(move_right)
        # for event in pygame.event.get():
        #
        #
        #     if event.type == pygame.QUIT:
        #         crashed = True


        if move_left==1:
                # and prev_button_direction != 1:
            move_left=0
            print("Entered")
            button_direction = 0
        elif move_right==1 and prev_button_direction != 0:
            move_right=0
            button_direction = 1
        elif move_up==1 and prev_button_direction != 2:
            move_up=0
            button_direction = 3
        elif move_down==1 and prev_button_direction != 3:
            move_down=0
            button_direction = 2
        print("Button",button_direction)


        # print(button_direction)



        # prev_button_direction = button_direction
        # button_direction=0
        if is_direction_blocked(snake_position, current_direction_vector) == 1:
            crashed = True

        clock.tick(1)
    return score

## display final score
def display_final_score(display_text, final_score):
    largeText = pygame.font.Font('freesansbold.ttf',35)
    TextSurf = largeText.render(display_text, True, black)
    TextRect = TextSurf.get_rect()
    TextRect.center = ((display_width/2),(display_height/2))
    display.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(1)

if __name__ == "__main__":

    ###### initialize required parameters ########
    display_width = 500
    display_height = 500
    green = (0,255,0)
    red = (255,0,0)
    black = (0,0,0)
    window_color = (0,00,00)
    apple_image = pygame.image.load('C:/Users/Aakash/Desktop/Inkedapple_LI.jpg')
    clock=pygame.time.Clock()

    snake_head = [250,250]
    snake_position = [[250,250],[240,250],[230,250]]
    apple_position = [random.randrange(1,50)*10,random.randrange(1,50)*10]
    score = 0

    pygame.init() #initialize pygame modules

    #### display game window #####
    # global text_1
    # text_1=speech()


    display = pygame.display.set_mode((display_width,display_height))
    display.fill(window_color)
    pygame.display.update()

    final_score = play_game(snake_head, snake_position, apple_position, 1, apple_image, score)
    display = pygame.display.set_mode((display_width,display_height))
    display.fill(window_color)
    pygame.display.update()

    display_text = 'Your Score is: ' + str(final_score)
    display_final_score(display_text, final_score)

    pygame.quit()




