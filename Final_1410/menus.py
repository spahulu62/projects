"""
This file has the main menu, control screen, and scores screen. Also has simple functions for saving scores and sorting
them, printing all the scores that are saved to the consol (was only used for helping create score screen), and get font
to size font.

The save scores function will create a file if there is none yet to score files. If there is no file the score screen
will say there is no highscores.

Author: Spencer Pahulu
Date: November 2025 - December 2025
"""

import os
import pickle
import pygame
import sys
from button import Button
"""----------------------------------------------Setup---------------------------------------------------------------"""
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
screen_rect = screen.get_rect()


#fps
clock = pygame.time.Clock()
fps = 60

"""---------------------------------------------Images / Font--------------------------------------------------------"""
#Background Images
bg = pygame.image.load('assets/City.png')
bg = pygame.transform.scale(bg, (1280, 720))

#Button Image
button_img = pygame.image.load('assets/button.png').convert_alpha()
button_img_rect = button_img.get_rect()
button_img_mask = pygame.mask.from_surface(button_img)

#Controls Images
wasd_img = pygame.image.load('assets/wasd.png').convert_alpha()
space_bar = pygame.image.load('assets/space_bar.png').convert_alpha()
space_bar = pygame.transform.scale(space_bar, (250, 135))

#Load custom font
main_font = pygame.font.Font('assets/aquire.otf', 30)
#Ajustable font size for titles and other screens
def get_font(size):
    return pygame.font.Font('assets/aquire.otf' , size)

"""---------------------------------------------score functions------------------------------------------------------"""

def save_score(score_data, filename = 'score_data.txt'):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            data = pickle.load(f)
            data = [score_data] + data
            with open(filename, 'wb') as f:
                sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
                pickle.dump(sorted_data[:5], f)


    else:
        with open(filename, 'wb') as f:
            scores = [score_data]
            pickle.dump(scores, f)
            print('new file created')

def print_data(filename = 'score_data.txt'):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            while True:
                try:
                    data = pickle.load(f)
                    print(data)
                except EOFError:
                    break
    else:
        pass

"""-----------------------------------------------Menus--------------------------------------------------------------"""
def controls_screen():
    pygame.display.set_caption('Controls')
    running = True
    clock.tick(fps)

    while running:
        #load background
        screen.fill((0,0,0))
        screen.blit(bg, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        #Title Text for Control Screen
        control_text = get_font(100).render('CONTROLS', True, 'grey')
        screen.blit(control_text, (350,100))

        #Text and Space bar image to show controls
        shoot_text = main_font.render('SHOOT', True, 'green')
        screen.blit(shoot_text, (677,445))

        screen.blit(space_bar, (600, 445))


        #Text and WASD image to show controls
        up_text = main_font.render( 'UP', True, 'green')
        screen.blit(up_text, (260, 375))

        down_text = main_font.render( 'DOWN', True, 'green')
        screen.blit(down_text, (235, 560))

        left_text = main_font.render( 'LEFT', True, 'green')
        screen.blit(left_text, (90, 500))

        right_text = main_font.render( 'RIGHT', True, 'green')
        screen.blit(right_text, (395, 500))

        screen.blit(wasd_img, (150, 350))

        #Text to tell controls as sentences
        list_up_text = get_font(25).render(f"Press 'W' to move UP", True, 'grey')
        list_down_text = get_font(25).render(f"Press 'S' to move DOWN", True, 'grey')
        list_left_text = get_font(25).render(f"Press 'A' to move LEFT", True, 'grey')
        list_right_text = get_font(25).render(f"Press 'D' to move RIGHT", True, 'grey')
        list_shoot_text = get_font(25).render(f"Press 'SPACE BAR' to SHOOT", True, 'grey')
        list_pause_text = get_font(25).render(f"Press 'ESC' to PAUSE", True, 'grey')

        screen.blit(list_up_text, (850, 225))
        screen.blit(list_down_text, (850, 245))
        screen.blit(list_left_text, (850, 265))
        screen.blit(list_right_text, (850, 285))
        screen.blit(list_shoot_text, (850, 305))
        screen.blit(list_pause_text, (850, 325))

        #Back button to return to main menu
        back_button = Button(None,
                             1100,
                             650,
                             "BACK >",
                             get_font(75),
                             'green',
                             'red')

        for button in [back_button]:
            button.change_color(mouse_pos)
            button.update()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_for_input(mouse_pos):
                    running = False

        back_button.update()

        pygame.display.update()

def scores_screen():
    pygame.display.set_caption('Scores')
    running = True
    clock.tick(fps)
    while running:
        screen.fill((0,0,0))
        screen.blit(bg, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        x = 0
        y_offset = 250

        if os.path.exists('score_data.txt'):
            score_title_text = get_font(100).render('HIGHSCORES', True, 'grey')
            screen.blit(score_title_text, (350, 100))
            try:
                with open('score_data.txt', 'rb') as file:
                    data = pickle.load(file)

                for item in data:
                    name, score = item
                    name_text = get_font(30).render(f'{x + 1}.  {name}  ||  Score {score}', True, 'grey')
                    screen.blit(name_text, (475, y_offset))
                    y_offset += 50
                    x += 1

            except ValueError:
                print('value error')
                break

            # Back button to return to main menu
            back_button = Button(None,
                                 1100,
                                 650,
                                 "BACK >",
                                 get_font(75),
                                 'green',
                                 'red')

            for button in [back_button]:
                button.change_color(mouse_pos)
                button.update()

            pygame.display.update()


        else:
            no_scores_text = get_font(100).render('No Scores Yet', True, 'grey')
            screen.blit(no_scores_text, (215, 200))

            # Back button to return to main menu
            back_button = Button(None,
                                 1100,
                                 650,
                                 "BACK >",
                                 get_font(75),
                                 'green',
                                 'red')

            for button in [back_button]:
                button.change_color(mouse_pos)
                button.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_for_input(mouse_pos):
                    running = False

        back_button.update()
        pygame.display.update()

def main_menu():
    running = True
    clock.tick(fps)
    pygame.display.set_caption('Main Menu')



    while running:


        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()
        menu_text = get_font(150).render('Invasion', True, 'green')
        screen.blit(menu_text, (290, 100))

        play_button = Button(button_img,
                             605,
                             300 ,
                             'PLAY',
                             main_font,
                             'white',
                             'green')

        controls_button = Button(button_img,
                                 605,
                                 400,
                                 'CONTROLS',
                                 main_font,
                                 'white',
                                 'green')

        scores_button = Button(button_img,
                               605,
                               500,
                               'SCORES',
                               main_font,
                               'white',
                               'green')

        quit_button = Button(button_img,
                             605,
                             600 ,
                             'QUIT',
                             main_font,
                             'white',
                             'green')

        for button in (play_button, controls_button, scores_button, quit_button):
            button.change_color(menu_mouse_pos)
            button.update()



        play_button.update()
        controls_button.update()
        scores_button.update()
        quit_button.update()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(menu_mouse_pos):
                    running = False
                if controls_button.check_for_input(menu_mouse_pos):
                    controls_screen()
                if scores_button.check_for_input(menu_mouse_pos):
                    scores_screen()
                if quit_button.check_for_input(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

