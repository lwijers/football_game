import pygame
import pygame_gui  # Import pygame_gui
import os
from const import *
import scene_base
import match.match_engine as match_engine
from match.match_gui import match_gui

PATH =  os.getcwd()

ajax = {
    'name': 'Ajax',
    'short_name': 'AJX',
    'color': "red",
    "attack": 15,  # Max is 20
    "midfield": 12,
    "defense": 10,
    "goalkeeper": 8  # New stat
}
feyenoord = {
    "name": 'Feyenoord',
    "short_name": 'FEY',
    'color': "black",
    "attack": 10,
    "midfield": 14,
    "defense": 1,
    "goalkeeper": 12  # New stat
}

home_team = ajax
away_team = feyenoord

class Match_scene(scene_base.Scene_base):
    def __init__(self, event_bus):
        scene_base.Scene_base.__init__(self, event_bus)
        self.m_engine = match_engine.MatchEngine(event_bus, home_team, away_team)
        self.ui_manager = pygame_gui.UIManager((SW, SH), f"{PATH}/match/match_gui/theme.json")
        self.m_gui = match_gui.MatchGui(self.ui_manager,self.m_engine)
        self.match_report = self.m_engine.run_match()
        print(self.match_report.generate_report())
        print(self.match_report.entries)
        print(self.m_engine.game_stats)
        self.m_gui.show_report(self.match_report)

    def process_events(self):
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                pass

            # Handle pygame_gui events
            self.ui_manager.process_events(event)

    def update(self):
        self.m_gui.update()
        self.ui_manager.update(1 / FPS)  # Update the UI Manager with a time step


    def draw(self, screen):
        screen.fill(BG_COLOR)

        self.m_gui.draw(screen)
        self.ui_manager.draw_ui(screen)
