import pygame
import pygame_gui
from pygame_gui.core import ObjectID
import random
from match.match_gui import resizable_label

class CommentBox(resizable_label.ResizableLabel):
    def __init__(self, ui_manager, center_position, theme):
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
