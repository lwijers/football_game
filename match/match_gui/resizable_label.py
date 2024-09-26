import pygame
import pygame_gui
from pygame_gui.core import ObjectID

class ResizableLabel:
    def __init__(self, ui_manager, position, object_id, initial_text="", font_path=None, font_size=30):
        self.ui_manager = ui_manager
        self.font = pygame.font.Font(font_path, font_size)  # Load font
        self.resizeable_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(position, (300, 50)),  # Default size
            text=initial_text,
            manager=ui_manager,
            object_id=ObjectID(object_id=object_id)
        )
        self.update_label_size()

    def update_label_size(self):
        # Get current label text and calculate size
        text = self.resizeable_label.text
        text_size = self.font.size(text)
        new_width = text_size[0] + 20
        new_height = text_size[1] + 20
        self.resizeable_label.set_dimensions((new_width, new_height))
        self.resizeable_label.rebuild()

    def set_text(self, text):
        self.resizeable_label.set_text(text)
        self.update_label_size()
