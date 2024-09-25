import os
import sys
import pygame
# import game_data
from match import match_scene
from const import *
import event_bus
import pygame_gui

class Game:
    def __init__(self):
        self.init()
        self.screen = None
        self.event_bus = event_bus.EventBus()
        self.clock = pygame.time.Clock()
        self.active_scene = match_scene.Match_scene(self.event_bus)
        # self.active_scene.set_clock(self.clock)




    def init(self):
        pygame.init()
        pygame.mixer.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1700, 50)
        self.screen = pygame.display.set_mode((SW, SH))

    def check_exit(self, events):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LALT] or pressed[pygame.K_RALT]:
            if pressed[pygame.K_F4]:
                return True

        if pressed[pygame.K_ESCAPE]:
            return True

        for event in events:
            if event.type == pygame.QUIT:
                return True
        else:
            return False


    def run(self):
        running = True

        while running:

            events = pygame.event.get()

            self.active_scene.set_events(events)

            self.active_scene.process_events()

            self.active_scene.update()

            self.active_scene.draw(self.screen)

            self.active_scene = self.active_scene.next

            pygame.display.flip()

            self.clock.tick(FPS)

            if self.check_exit(events):
                pygame.quit()
                sys.exit()
