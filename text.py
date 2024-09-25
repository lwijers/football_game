import pygame
import os
import re

# Define font configurations
ui_fonts = {
    'std': {'type': 'Coolvetica', 'size': 30, 'color': (255, 255, 255)},
    'match_score' : {'type': 'Coolvetica', 'size': 80, 'color': (255, 255, 255)},
    'comment_box' : {'type': 'Coolvetica', 'size': 30, 'color': (255, 255, 255)}
}

class FontManager:
    def __init__(self):
        pygame.font.init()
        self.fonts = {}
        self.load_fonts()

    def load_fonts(self):
        """Load fonts into memory from specified paths or use default."""
        for font_name, font_data in ui_fonts.items():
            font_location = f'assets/fonts/{font_data["type"]}.ttf'
            try:
                self.fonts[font_name] = pygame.font.Font(font_location, font_data['size'])
            except FileNotFoundError:
                print(f"Error: Font file {font_location} not found. Using default font.")
                self.fonts[font_name] = pygame.font.SysFont('Arial', font_data['size'])  # Fallback to default font

    def get_font(self, font_cat):
        """Return the font corresponding to the given category."""
        return self.fonts.get(font_cat, self.fonts['std'])

font_manager = FontManager()

# Color dictionary for supported tags
color_dict = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "white": (255, 255, 255),
    "black": (0, 0, 0)
}

def parse_text(text):
    """Parse the text for color tags, e.g., <red>hello</red>."""
    tag_pattern = r'<(?P<color>\w+)>(?P<text>.*?)</\w+>'
    matches = list(re.finditer(tag_pattern, text))

    parsed_parts = []
    last_end = 0

    for match in matches:
        color_name = match.group('color')
        word = match.group('text')

        # Append uncolored text between the last match and current match
        if match.start() > last_end:
            parsed_parts.append((text[last_end:match.start()], color_dict["white"]))  # default color

        # Append the colored word
        parsed_parts.append((word, color_dict.get(color_name, color_dict["white"])))  # use color from tag

        last_end = match.end()

    # Append the remaining part of the string without any tags
    if last_end < len(text):
        parsed_parts.append((text[last_end:], color_dict["white"]))  # default color

    return parsed_parts

def write_surface(text, font_cat='std'):
    """
    Create a surface with the parsed colored text.
    Returns a pygame.Surface object with the rendered text.
    """
    font = font_manager.get_font(font_cat)
    parsed_text = parse_text(text)  # Parse the text with color tags

    # Estimate surface size by summing up widths of each word
    total_width = sum([font.size(word)[0] for word, _ in parsed_text]) + (len(parsed_text) - 1) * 5
    max_height = max([font.size(word)[1] for word, _ in parsed_text])

    # Create a transparent surface to draw the text
    text_surface = pygame.Surface((total_width, max_height), pygame.SRCALPHA)

    # Render each word onto the surface
    current_x = 0
    for word, color in parsed_text:
        my_label = font.render(word, True, color)
        text_surface.blit(my_label, (current_x, 0))
        current_x += my_label.get_width() + 5  # Add space between words

    return text_surface

def write_sprite(text, pos, font_cat='std'):
    """
    Create a sprite that contains the rendered text.
    Returns a pygame.sprite.Sprite object.
    """
    surface = write_surface(text, font_cat)
    sprite = pygame.sprite.Sprite()
    sprite.image = surface
    sprite.rect = surface.get_rect(topleft=pos)
    return sprite

def write(surface, text, pos, font_cat='std', centered=False, right=False):
    """
    Render text directly onto the surface with color parsing.
    """
    font = font_manager.get_font(font_cat)
    parsed_text = parse_text(text)  # Parse the text with color tags

    current_x = pos[0]
    current_y = pos[1]

    for word, color in parsed_text:
        my_label = font.render(word, True, color)

        if centered:
            surface.blit(my_label, (current_x - my_label.get_width() / 2,
                                    current_y - my_label.get_height() / 2))
        elif right:
            surface.blit(my_label, (current_x - my_label.get_width(), current_y))
            current_x -= my_label.get_width() + 5  # Add space between words
        else:
            surface.blit(my_label, (current_x, current_y))
            current_x += my_label.get_width() + 5  # Add space between words
