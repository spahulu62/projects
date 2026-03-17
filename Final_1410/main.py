"""
Final Project: 1410
Create a simple game that will record points from destroying aliens.
Create different screens and functioning UI

Author: Spencer Pahulu
Date: November 2025 - December 2025
"""

#Imports
import sys
import pygame
import random
from pygame import mixer
from button import Button
from menus import main_menu, get_font, save_score


"""--------------------------------------------------Setup-----------------------------------------------------------"""
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
screen_rect = screen.get_rect()

#fps
clock = pygame.time.Clock()
fps = 60
dt = 0
last_count = pygame.time.get_ticks()

#Mixer set up
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

#Colors
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

#Load Sounds
explosion_fx = pygame.mixer.Sound('assets/explosions/explosion_fx.mp3')
explosion_fx.set_volume(0.25)

explosion2_fx = pygame.mixer.Sound('assets/explosions/explosion2_fx.mp3')
explosion2_fx.set_volume(0.25)

laser_fx = pygame.mixer.Sound('assets/laser_fx.mp3')
laser_fx.set_volume(0.25)

#font
main_font = pygame.font.Font('assets/aquire.otf', 30)

"""-------------------------------------------------Images-----------------------------------------------------------"""
#Background Images
bg = pygame.image.load('assets/City.png')
bg = pygame.transform.scale(bg, (1280, 720))

#Player Ship Images
ship = pygame.image.load('assets/player/player_ship.png')
ship = pygame.transform.scale(ship,(100,65))
ship = pygame.transform.rotate(ship,270)

#Heart Images
heart_image = pygame.image.load('assets/player/heart.png')
heart_image = pygame.transform.scale(heart_image,(50,50))

#Bullet Images
beam = pygame.image.load('assets/player/beam.PNG')
beam = pygame.transform.rotate(beam,270)

#Alien Bullets
alien_beam = pygame.image.load('assets/alien/red_beam.png')
alien_beam = pygame.transform.rotate(alien_beam,270)

"""--------------------------------------------Functions-------------------------------------------------------------"""
#draws background
def draw_bg():
    screen.blit(bg, (0,0))

"""-------------------------------------------Player Code------------------------------------------------------------"""
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health = 3):
        pygame.sprite.Sprite.__init__(self)
        self.image = ship
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()
        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        #movement speed
        speed = 8
        #cooldown for shot
        cooldown = 500 #millisecons
        game_over = False

        #key presses
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.rect.x -= speed
        if key[pygame.K_d]:
            self.rect.x += speed
        if key[pygame.K_s]:
            self.rect.y += speed
        if key[pygame.K_w]:
            self.rect.y -= speed

        #current time
        time_now = pygame.time.get_ticks()
        #shooting
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            laser_fx.play()
            bullet = Bullets(self.rect.right, self.rect.centery)
            bullet_group.add(bullet)
            self.last_shot = time_now



        if pygame.sprite.spritecollide(player_ship, alien_group, True, pygame.sprite.collide_mask):
            self.health_remaining -= 1
            explosion2_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)


        if self.health_remaining <= 0:
            self.kill()
            explosion2_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            game_over = True
        return game_over

class Bullets(pygame.sprite.Sprite):
    def __init__(self, x = 0, y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = beam
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        global score
        self.rect.x += 5
        if self.rect.x > 1280:
            self.kill()

        if pygame.sprite.spritecollide(self, alien_group, True, pygame.sprite.collide_mask):
            self.kill()
            explosion_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)
            score += 10
            if len(alien_group) == 0:
                score += 100

def draw_health_bar(current_health, max_health, x_start, y_start, heart_spacing):
    for i in range(current_health):
        screen.blit(heart_image, (x_start + i * (heart_image.get_width() + heart_spacing), y_start))

"""---------------------------------------------Alien Code-----------------------------------------------------------"""
#Global variables
rows = 6
cols = 5
alien_cooldown = 800 #millisecons
last_alien_shot = pygame.time.get_ticks()

class Aliens(pygame.sprite.Sprite):
    def __init__(self, x = 0, y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/alien/alien' + str(random.randint(1,5)) + '.png')
        self.image = pygame.transform.scale(self.image,(60,50))
        self.image = pygame.transform.rotate(self.image,270)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.y += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction

        self.mask = pygame.mask.from_surface(self.image)

class AlienBullets(pygame.sprite.Sprite):
    def __init__(self, x = 0, y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = alien_beam
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.x -= 5
        if self.rect.x < 0:
            self.kill()

        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            explosion2_fx.play()
            player_ship.health_remaining -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)

def create_alien():
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(725 + item * 100, 105 + row * 100)
            alien_group.add(alien)

"""-------------------------------------------Explosion Code---------------------------------------------------------"""
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x = 0, y = 0, size = 1):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            image = pygame.image.load(f'assets/explosions/exp{num}.png')
            if size == 1:
                image = pygame.transform.scale(image,(20,20))
            if size == 2:
                image = pygame.transform.scale(image,(40,40))
            if size == 3:
                image = pygame.transform.scale(image,(160,160))
            self.images.append(image)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        explosion_speed = 3
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

"""------------------------------------------Sprite Groups-----------------------------------------------------------"""
#create sprite group
spaceship_group = pygame.sprite.Group()  # type: ignore
bullet_group = pygame.sprite.Group()  #type: ignore
alien_group = pygame.sprite.Group()   # type: ignore
alien_bullet_group = pygame.sprite.Group()  # type: ignore
explosion_group = pygame.sprite.Group()    # type: ignore

#Creates Mob of Aliens
create_alien()

#player
player_ship = Spaceship(125, 360, 3)
spaceship_group.add(player_ship)

"""--------------------------------------------Game States-----------------------------------------------------------"""
game_paused = False
game_over = False
countdown = 3
next_wave_count = 3
start = False
score = 0
getting_name = True

def reset():
    global score
    screen.fill((0, 0, 0))
    draw_bg()

    spaceship_group.empty()
    bullet_group.empty()
    alien_bullet_group.empty()
    alien_group.empty()

    spaceship_group.update()
    bullet_group.update()
    alien_group.update()
    alien_bullet_group.update()

    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    alien_bullet_group.draw(screen)

    player_ship.rect.center = (125, 360)
    spaceship_group.add(player_ship)
    create_alien()
    score = 0

def pause_screen():
    pygame.display.set_caption('Paused')
    pause_text = get_font(75).render('PAUSED', True, 'grey')
    screen.blit(pause_text, (275, 50))

"""---------------------------------------------Game Loop------------------------------------------------------------"""
class Game:
    running = True

    while running:

        clock.tick(fps)
        mouse_pos = pygame.mouse.get_pos()

        if not start:
            main_menu()
            start = True

        #draw background
        screen.fill((0,0,0))
        draw_bg()

        score_text = get_font(25).render("Score " + str(score), True, 'green')
        screen.blit(score_text, (50, 695))

        if countdown == 0 and game_over == False and game_paused == False:
            pygame.display.set_caption('Invasion')
            #create random alien bullets
            #current time
            time_now = pygame.time.get_ticks()

            if len(alien_group.sprites()) > 0:
                if time_now - last_alien_shot > alien_cooldown:
                    attacking_alien = random.choice(alien_group.sprites())
                    alien_bullet = AlienBullets(attacking_alien.rect.left, attacking_alien.rect.centery)
                    alien_bullet_group.add(alien_bullet)
                    last_alien_shot = time_now

            #if all the aliens die make more
            if len(alien_group.sprites()) == 0:
                if next_wave_count > 0:
                    next_wave_text = get_font(45).render('Next Wave!', True, 'grey')
                    screen.blit(next_wave_text, (300, screen_rect.centery - 100))
                    count_text = get_font(45).render(str(next_wave_count), True, 'red')
                    screen.blit(count_text, (415, screen_rect.centery - 50))
                    count_timer = pygame.time.get_ticks()

                    # update sprite groups
                    player_ship.rect.clamp_ip(screen_rect)
                    player_ship.update()
                    bullet_group.update()

                    if count_timer - last_count > 1000:
                        next_wave_count -= 1
                        last_count = count_timer
                        if next_wave_count == 0:
                            create_alien()
                            if player_ship.health_remaining < 3:
                                player_ship.health_remaining += 1
                            next_wave_count = 3


            #update spaceship / player pos
            player_ship.rect.clamp_ip(screen_rect)
            game_over = player_ship.update()

            #update sprite groups
            bullet_group.update()
            alien_group.update()
            alien_bullet_group.update()


        if countdown > 0 and game_paused == False:
            get_ready_text = get_font(45).render('Get Ready', True, 'grey')
            screen.blit(get_ready_text, (300, screen_rect.centery - 100))
            count_text = get_font(45).render(str(countdown), True, 'red')
            screen.blit(count_text, (415, screen_rect.centery - 50))
            count_timer = pygame.time.get_ticks()
            if count_timer - last_count > 1000:
                countdown -= 1
                last_count = count_timer


        if game_over and getting_name == True:
              name_input = ''
              while getting_name:
                    score_data = [str(name_input) , int(score)]
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_BACKSPACE:
                                name_input = name_input[:-1]
                            elif event.key == pygame.K_RETURN:
                                save_score(score_data)
                                getting_name = False
                                break
                            else:
                                if len(name_input) < 11:
                                    name_input += event.unicode

                    screen.fill((0, 0, 0))
                    draw_bg()

                    input_rect = pygame.Rect(140, 250, 250, 40)

                    game_over_text = get_font(100).render('GAME OVER', True, 'RED')
                    screen.blit(game_over_text, (300, screen_rect.centery - 300))

                    name_text = get_font(50).render('Enter Name', True, 'grey')
                    screen.blit(name_text, (100, 200))

                    score_text = get_font(50).render(f'SCORE {str(score)}', True, 'grey')
                    screen.blit(score_text, (100, 350))

                    input_surface = get_font(30).render(name_input, True, 'grey')
                    screen.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))
                    pygame.draw.rect(screen, 'grey', input_rect, 3)

                    explosion_group.update()
                    spaceship_group.draw(screen)
                    bullet_group.draw(screen)
                    alien_group.draw(screen)
                    alien_bullet_group.draw(screen)
                    explosion_group.draw(screen)

                    pygame.display.update()

              game_over_text = get_font(100).render('GAME OVER', True, 'RED')
              screen.blit(game_over_text, (300, screen_rect.centery - 300))


        if game_over and getting_name == False:
            pygame.display.set_caption('Game Over')

            game_over_text = get_font(100).render('GAME OVER', True, 'RED')
            screen.blit(game_over_text, (300, screen_rect.centery - 300))

            # Back button to return to main menu
            retry_button = Button(None,
                                 300,
                                 screen_rect.centery,
                                 "< Retry >",
                                 get_font(50),
                                 'grey',
                                 'green')

            menu_button = Button(None,
                                  300,
                                  screen_rect.centery - 100,
                                  "< Main Menu >",
                                  get_font(50),
                                  'grey',
                                  'green')

            quit_button = Button(None,
                                 300,
                                 screen_rect.centery + 100,
                                 "< Quit >",
                                 get_font(50),
                                 'grey',
                                 'red')

            for button in [retry_button, menu_button, quit_button]:
                button.change_color(mouse_pos)
                button.update()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_button.check_for_input(mouse_pos):
                        reset()
                        game_paused = False
                        game_over = False
                        countdown = 3
                        next_wave_count = 3
                        player_ship.health_remaining = 3
                        getting_name = True
                        pygame.display.update()
                        break

                    if menu_button.check_for_input(mouse_pos):
                        reset()
                        game_paused = False
                        game_over = False
                        countdown = 3
                        next_wave_count = 3
                        player_ship.health_remaining = 3
                        getting_name = True
                        pygame.display.update()
                        main_menu()
                        break

                    if quit_button.check_for_input(mouse_pos):
                        pygame.quit()
                        sys.exit()

        if game_paused:
            pause_screen()
            resume_button = Button(None,
                                   275,
                                   175,
                                   "<RESUME>",
                                   get_font(50),
                                   'grey',
                                   'green')

            quit_button = Button(None,
                                   550,
                                   175,
                                   "<QUIT>",
                                   get_font(50),
                                   'grey',
                                   'red')

            for button in [resume_button, quit_button]:
                button.change_color(mouse_pos)
                button.update()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            game_paused = not game_paused
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if resume_button.check_for_input(mouse_pos):
                            game_paused = not game_paused
                        if quit_button.check_for_input(mouse_pos):
                            reset()
                            score = 0
                            game_paused = False
                            game_over = False
                            countdown = 3
                            next_wave_count = 3
                            player_ship.health_remaining = 3
                            pygame.display.update()
                            main_menu()

            quit_button.update()
            resume_button.update()

        #event handlers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = not game_paused

        #update explosion group
        explosion_group.update()

        #update sprite group
        spaceship_group.draw(screen)
        bullet_group.draw(screen)
        alien_group.draw(screen)
        alien_bullet_group.draw(screen)
        explosion_group.draw(screen)
        draw_health_bar(player_ship.health_remaining, 3, 10, 10, 5)

        pygame.display.update()


    pygame.quit()

