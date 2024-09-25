import pygame
import pygame_gui  # Import pygame_gui
from pygame_gui.core import ObjectID
import json
import random
from const import *

THEME =  {}
with open("match/match_gui/theme.json", 'r', encoding='utf-8') as file:
    theme = json.load(file)

class ResizableLabel:
    def __init__(self, ui_manager, position, object_id, initial_text="", font_path=None, font_size=30):
        self.ui_manager = ui_manager
        self.font = pygame.font.Font(font_path, font_size)  # Load font
        self.label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(position, (300, 50)),  # Default size
            text=initial_text,
            manager=ui_manager,
            object_id=ObjectID(object_id=object_id)
        )
        self.update_label_size()

    def update_label_size(self):
        # Get current label text and calculate size
        text = self.label.text
        text_size = self.font.size(text)
        new_width = text_size[0] + 20
        new_height = text_size[1] + 20
        self.label.set_dimensions((new_width, new_height))
        self.label.rebuild()

    def set_text(self, text):
        self.label.set_text(text)
        self.update_label_size()

class CommentBox(ResizableLabel):
    def __init__(self, ui_manager, center_position):
        super().__init__(ui_manager, (0, 0), '#comment_box', "", "assets/fonts/coolvetica.ttf",
                         theme["#comment_box"]["font"]['size'])
        self.ui_manager = ui_manager
        self.publication_threshold = 0.5  # Probability threshold
        self.dirty_comments = []  # Comments that need to be filtered
        self.clean_comments = []  # Comments that pass the filter
        self.current_comment_index = 0
        self.comment_display_time = 1500  # Time to display each comment in milliseconds
        self.comment_timer = 0  # Timer to track comment display time
        self.clock = pygame.time.Clock()  # Create a clock for timing

        # Initialize label with empty text
        self.comment_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (400, 100)),  # Default size, will be updated
            text="",  # Initialize with an empty string
            manager=self.ui_manager,
            object_id=ObjectID(object_id='#comment_box')
        )

        self.center_position = center_position  # Store the center position

        # Initialize the font separately for sizing purposes
        self.font = pygame.font.Font("assets/fonts//coolvetica.ttf", theme["#comment_box"]["font"]['size'])  # Match the theme font

    def update(self):
        if self.clean_comments:  # Only update if there are valid comments to display
            time_passed = self.clock.tick()  # Get time since last frame (in milliseconds)
            self.comment_timer += time_passed  # Increment timer with the time passed

            if self.comment_timer >= self.comment_display_time:
                self.comment_timer = 0  # Reset the timer
                self.current_comment_index += 1  # Move to the next comment
                if self.current_comment_index >= len(self.clean_comments):
                    self.current_comment_index = 0  # Loop back to the first comment
                self.update_comment_label()  # Update the comment label with the new comment

    def show_report(self, report):
        self.dirty_comments = report.get_all_entries()  # Get comments from the report
        self.filter_comments()  # Filter comments before displaying
        self.update_comment_label()  # Show the first comment initially

    def filter_comments(self):
        self.clean_comments = []  # Reset clean comments

        for comment in self.dirty_comments:
            # If the comment is already marked as must_display, append it directly
            if comment.get("must_display", False):
                self.clean_comments.append(comment)
            # If it’s not marked, check against the threshold
            elif random.random() < self.publication_threshold:
                comment['must_display'] = True
                self.clean_comments.append(comment)  # Append if the threshold is met

    def update_comment_label(self):
        current_comment = self.clean_comments[self.current_comment_index]["comment"]
        self.set_text(current_comment)  # Use set_text from the base class

        # Center the label based on the new size
        new_position = (
            self.center_position[0] - self.label.relative_rect.width // 2,
            self.center_position[1] - self.label.relative_rect.height // 2
        )
        self.label.set_relative_position(new_position)

class ScoreElement(ResizableLabel):
    def __init__(self, ui_manager, match_engine, position):
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


class MatchGui:
    def __init__(self, ui_manager, match_engine):
        self.m_engine = match_engine
        self.ui_manager = ui_manager

        # Create an instance of the ScoreElement
        self.score_element = ScoreElement(ui_manager, match_engine, (SW / 2 - 100, 50))

        # Create an instance of the CommentBox
        self.comment_box = CommentBox(ui_manager, (SW / 2, 200))

    def update(self):
        self.score_element.update()  # Update the score display
        self.comment_box.update()  # Update the comment box

    def draw(self, screen):
        self.ui_manager.draw_ui(screen)

    def show_report(self, report):
        self.comment_box.show_report(report)  # Use the CommentBox to show comments

    def end_match(self):
        self.match_ongoing = False  # Set to False when the match ends
