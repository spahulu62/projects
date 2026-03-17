"""
This file hold the button class that is used a bunch to create different type of buttons and all buttons for every
screen. Very important file.

Author: Spencer Pahulu
Date: November 2025 - December 2025
"""

import pygame


pygame.init()

screen = pygame.display.set_mode((1280, 720))

class Button:
    def __init__(self, image, x_pos, y_pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center = (self.x_pos, self.y_pos))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            offset_x = mouse_pos[0] - self.rect.x
            offset_y = mouse_pos[1] - self.rect.y
            if self.mask.get_at((offset_x, offset_y)):
                return True
        return False

    def change_color(self, position):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            offset_x = mouse_pos[0] - self.rect.x
            offset_y = mouse_pos[1] - self.rect.y
            if self.mask.get_at((offset_x, offset_y)): # Check if the pixel under the mouse is part of the mask
                self.text = self.font.render(self.text_input, True, self.hovering_color)
            else:
                self.text = self.font.render(self.text_input, True, self.base_color)

