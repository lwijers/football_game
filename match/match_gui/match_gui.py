import json
from const import *
from match.match_gui import comment_box
from match.match_gui import score_elementl


THEME =  {}

with open("match/match_gui/theme.json", 'r', encoding='utf-8') as file:
    THEME = json.load(file)





class MatchGui:
    def __init__(self, ui_manager, match_engine):
        self.m_engine = match_engine
        self.ui_manager = ui_manager

        # Create an instance of the ScoreElement
        self.score_element = score_elementl.ScoreElement(ui_manager, match_engine, (SW / 2 - 100, 50), THEME)

        # Create an instance of the CommentBox
        self.comment_box = comment_box.CommentBox(ui_manager, (SW / 2, 200), THEME)

    def update(self):
        self.score_element.update()  # Update the score display
        self.comment_box.update()  # Update the comment box

    def draw(self, screen):
        self.ui_manager.draw_ui(screen)

    def show_report(self, report):
        self.comment_box.show_report(report)  # Use the CommentBox to show comments

    def end_match(self):
        self.match_ongoing = False  # Set to False when the match ends
