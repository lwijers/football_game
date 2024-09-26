import json
import random

class CommentGenerator:
    def __init__(self, json_file):
        with open(json_file, 'r', encoding='utf-8') as file:
            self.templates = json.load(file)

        # Define expected keys for each situation
        self.expected_keys = {
            'pre_match': ['team_a', 'team_b'],
            'announce_extra_time_first_half': ['extra_time'],
            'end_first_half': ['score'],
            'half_time_event': [],
            'start_second_half': ['team_a', 'team_b'],
            'announce_extra_time_second_half': ['extra_time'],
            'post_match': ['team_a', 'team_b', 'score_a', 'score_b'],
            'switch_possession': ['team_ball_gained', 'team_ball_lost'],
            'has_possession': ['team_in_possession', 'score', 'home_team', 'away_team'],
        }

    def validate_arguments(self, trigger, kwargs):
        expected = self.expected_keys.get(trigger, [])
        for key in expected:
            if key not in kwargs:
                raise ValueError(f"Missing argument: {key} for situation '{trigger}'")
            if key == 'team' and not isinstance(kwargs[key], str):
                raise TypeError(f"Expected a string for {key}, got {type(kwargs[key]).__name__}.")

    def generate_comment(self, trigger, **kwargs):
        if trigger not in self.templates:
            return "No comments available for this situation."

        # Validate the arguments before proceeding
        self.validate_arguments(trigger, kwargs)

        template = random.choice(self.templates[trigger])
        return template.format(**kwargs)
