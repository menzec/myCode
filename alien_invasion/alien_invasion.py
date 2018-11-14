#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-30 19:30:04
# @Author  : ${menzec} (${menzc@outlook.com})
# @Link    : http://example.org
# @Version : $Id$

import sys
import pygame
from settings import Settings


def run_game():
    # create a screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_heigth))
    pygame.display.set_caption('Alien Invasion')
    # main process
    while True:
        # keyborad and mouse event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(ai_settings.bg_color)
        # display the screen just drawed
        pygame.display.flip()


# run_game()
print('hello world')
