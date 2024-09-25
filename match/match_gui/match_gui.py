import pygame
import pygame_gui  # Import pygame_gui
from pygame_gui.core import ObjectID
import json
import random
from const import *

THEME =  {}
with open("match/match_gui/theme.json", 'r', encoding='utf-8') as file:
    theme = json.load(file)



class CommentBox:
    def __init__(self, ui_manager, center_position):
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
        if self.clean_comments:  # Check if there are comments to display
            current_comment = self.clean_comments[self.current_comment_index]["comment"]
            self.comment_label.set_text(current_comment)  # Update to the current comment

            # Calculate the size of the text using the font defined earlier (separate from theme)
            text_size = self.font.size(current_comment)

            # Update the size of the label based on the text, adding padding
            new_width = text_size[0] + 20  # Add padding (10px on each side)
            new_height = text_size[1] + 20  # Add padding (10px top and bottom)
            self.comment_label.set_dimensions((new_width, new_height))

            # Recenter the label based on its new dimensions
            new_position = (
                self.center_position[0] - new_width // 2,  # Center x - half width
                self.center_position[1] - new_height // 2  # Center y - half height
            )
            self.comment_label.set_relative_position(new_position)  # Set new position of the label
            self.comment_label.rebuild()  # Refresh the label display

import pygame
import pygame_gui
from pygame_gui.core import ObjectID

class ScoreElement:
    def __init__(self, ui_manager, match_engine, position):
        self.ui_manager = ui_manager
        self.match_engine = match_engine

        # Load the font that matches the theme (if you want to match the theme's font size)
        self.font = pygame.font.Font("assets/fonts/coolvetica.ttf", theme["#score_element"]["font"]['size'])  # Example font

        # Create a score label
        self.score_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(position, (300, 50)),  # Default size, will be updated
            text=self.get_score_text(),  # Set initial score text
            manager=self.ui_manager,
            object_id=ObjectID(object_id='#comment_box')  # Adjust if you have a specific object_id
        )

        self.old_score = self.match_engine.return_score()  # Initial score

        # Set the initial size based on the current score text
        self.update_label_size()

    def update(self):
        current_score = self.match_engine.return_score()
        if current_score != self.old_score:
            self.update_score_display(current_score)  # Update the score display
            self.old_score = current_score  # Update the old score

    def update_score_display(self, score):
        self.score_label.set_text(self.get_score_text(score))  # Update the score label text
        self.update_label_size()  # Adjust size based on new score text

    def get_score_text(self, score=None):
        if score is None:
            score = self.match_engine.return_score()  # Retrieve current score if not provided

        home_score = score["home_team"]
        away_score = score["away_team"]
        home_short_name = self.match_engine.home_team["short_name"]
        away_short_name = self.match_engine.away_team["short_name"]
        return f"{home_short_name} {home_score} - {away_score} {away_short_name}"

    def update_label_size(self):
        # Get the current score text
        score_text = self.score_label.text

        # Calculate the size of the text using the font
        text_size = self.font.size(score_text)  # Returns (width, height)

        # Update the label dimensions based on text size, add some padding
        new_width = text_size[0] + 20  # Add padding
        new_height = text_size[1] + 20  # Add padding
        self.score_label.set_dimensions((new_width, new_height))

        # Optionally, reposition the label based on new dimensions
        current_position = self.score_label.relative_rect.topleft
        self.score_label.set_relative_position((current_position[0], current_position[1]))

        # Rebuild the label to apply changes
        self.score_label.rebuild()


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
