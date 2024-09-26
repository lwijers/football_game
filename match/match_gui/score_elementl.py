import pygame
import pygame_gui
from pygame_gui.core import ObjectID
import random
from match.match_gui import resizable_label



class ScoreElement(resizable_label.ResizableLabel):
    def __init__(self, ui_manager, match_engine, position, theme):
        # Call the parent constructor with the correct object_id
        super().__init__(ui_manager, position, '#score_element', "", "assets/fonts/coolvetica.ttf",
                         theme["#score_element"]["font"]['size'])

        self.match_engine = match_engine
        self.old_score = self.match_engine.return_score()  # Initial score

        # Set the initial score text
        self.set_text(self.get_score_text())

    def update(self):
        current_score = self.match_engine.return_score()
        if current_score != self.old_score:
            self.set_text(self.get_score_text(current_score))  # Update the score display
            self.old_score = current_score  # Update the old score

    def get_score_text(self, score=None):
        if score is None:
            score = self.match_engine.return_score()  # Retrieve current score if not provided

        home_score = score["home_team"]
        away_score = score["away_team"]
        home_short_name = self.match_engine.home_team["short_name"]
        away_short_name = self.match_engine.away_team["short_name"]
        return f"{home_short_name} {home_score} - {away_score} {away_short_name}"
