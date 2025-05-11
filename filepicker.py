#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Made by papi
# Created on: Sun 11 May 2025 12:32:06 PM IST
# filepicker.py
# Description:

import os, time
import pygame

ITEM_HEIGHT = 40
VISIBLE_ITEMS = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT = (100, 100, 255)

class FilePicker():
    def __init__(self, screen, joystick):
        self.current_path = os.getcwd()
        self.entries = self.list_dir(self.current_path)
        self.scroll_offset = 0
        self.selected_index = 0
        self.FONT = pygame.font.SysFont(None, 32)
        self.screen = screen
        self.joystick = joystick
        self.width, self.height = screen.get_size()

    def list_dir(self, path):
        try:
            self.entries = os.listdir(path)
            self.entries = sorted(self.entries)
            return ['..'] + self.entries
        except Exception as e:
            print("Error:", e)
            return []

    def event(self):
        hat = self.joystick.get_hat(0)
        if hat[1] == 1:  # Up
            self.selected_index = max(0, self.selected_index - 1)
            if self.selected_index < self.scroll_offset:
                self.scroll_offset = self.selected_index
            time.sleep(0.2)
        elif hat[1] == -1:  # Down
            self.selected_index = min(len(self.entries) - 1, self.selected_index + 1)
            if self.selected_index >= self.scroll_offset + VISIBLE_ITEMS:
                self.scroll_offset = self.selected_index - VISIBLE_ITEMS + 1
            time.sleep(0.2)
        if self.joystick.get_button(7):
            return os.path.join(self.current_path)
        if self.joystick.get_button(0):  # A or Start to enter
            selected = self.entries[self.selected_index]
            selected_path = os.path.join(self.current_path, selected)
            if selected == '..':
                current_path = os.path.dirname(self.current_path)
                self.entries = self.list_dir(self.current_path)
                self.selected_index = 0
                self.scroll_offset = 0
            elif os.path.isdir(selected_path):
                self.current_path = selected_path
                self.entries = self.list_dir(self.current_path)
                self.selected_index = 0
                scroll_offset = 0
            time.sleep(0.2)

        elif self.joystick.get_button(1) or self.joystick.get_button(6):  # B or Back to go up
            self.current_path = os.path.dirname(self.current_path)
            self.entries = self.list_dir(self.current_path)
            self.selected_index = 0
            self.scroll_offset = 0
            time.sleep(0.2)
        return ""

    def draw(self):
        rect = pygame.Rect(0, 0, self.width // 2, self.height // 2)
        rect.center = (self.width // 2, self.height // 2)

        pygame.draw.rect(self.screen, WHITE, rect)
        content_surface = pygame.Surface((rect.width, rect.height))
        content_surface.fill(WHITE)
        for i, entry in enumerate(self.entries[self.scroll_offset:self.scroll_offset + VISIBLE_ITEMS]):
            y = i * ITEM_HEIGHT
            full_path = os.path.join(self.current_path, entry)
            is_dir = os.path.isdir(full_path)
            bg_color = HIGHLIGHT if i + self.scroll_offset == self.selected_index else WHITE
            pygame.draw.rect(content_surface, bg_color, (0, y, rect.width, ITEM_HEIGHT))
            label = f"[DIR] {entry}" if is_dir else entry
            text = self.FONT.render(label, True, BLACK)
            content_surface.blit(text, (10, y + 8))
        text_surf = self.FONT.render("Press Start to select folder!", True, (255, 255, 255))  # white text
        text_rect = text_surf.get_rect()
        box_rect = pygame.Rect(0, 0, text_rect.width + 2 * 10, text_rect.height + 2 * 10)
        box_rect.bottomright = (content_surface.get_width() - 10, content_surface.get_height() - 10)
        pygame.draw.rect(content_surface, (0, 200, 0), box_rect, border_radius=8)  # green box
        content_surface.blit(text_surf, (box_rect.x + 10, box_rect.y + 10))
        self.screen.blit(content_surface, rect.topleft)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("Controller Folder Picker")
    pygame.joystick.init()
    if pygame.joystick.get_count() < 1:
        print("No controller connected.")
        pygame.quit()
        sys.exit()

    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    fp = FilePicker(screen,joystick)
    clock = pygame.time.Clock()
    while True:
        screen.fill((0,0,0))
        fp.draw()
        pygame.display.flip()
        clock.tick(30)
        text = fp.event()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
        if len(text) > 0:
            print(text)
            break
    pygame.quit()
