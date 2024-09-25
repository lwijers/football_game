import random
from match import match_report
from match.match_events import event_manager


class MatchEngine:
    def __init__(self, event_bus, home_team, away_team):
        # Initialize teams and match details
        self.event_bus = event_bus
        self.home_team = home_team
        self.away_team = away_team
        self.score = {"home_team": 0, "away_team": 0}
        self.match_length = 90  # Regular match length
        self.game_stats = {}

        self.extra_time_first_half = self.calculate_extra_time()
        self.extra_time_second_half = self.calculate_extra_time()

        # Create an instance of the event manager to handle match events
        self.match_report = match_report.Match_report(self)
        self.compile_game_stats()

        self.event_manager = event_manager.EventManager(self, self.game_stats)

        self.match_minutes = self.setup_match_minutes()


    def compile_game_stats(self):
        self.game_stats = {'home_team': self.home_team, 'away_team': self.away_team}
        self.game_stats['home_team']['score'] = self.score['home_team']
        self.game_stats['away_team']['score'] = self.score['away_team']
        self.game_stats['extra_time_first_half'] = self.extra_time_first_half
        self.game_stats['extra_time_second_half'] = self.extra_time_second_half
        self.game_stats['match_length'] = self.match_length + self.extra_time_second_half + self.extra_time_first_half
        self.game_stats['has_possession'] = None
        self.game_stats['no_possession'] = None
        self.game_stats['home_team']['possession_counter'] = 0
        self.game_stats['away_team']['possession_counter'] = 0
        self.game_stats['possession_total'] = 0


    def setup_match_minutes(self):
        """
        Create the match timeline with first half, extra time for both halves, and second half.
        """
        # First half timeline (1 to 45)
        first_half = [str(i) for i in range(1, 46)]

        # Extra time for the first half (e.g., 45 + 1, 45 + 2)
        first_half_extra = [f"45 + {i}" for i in range(1, self.extra_time_first_half + 1)]

        # Second half timeline (46 to 90)
        second_half = [str(i) for i in range(46, 91)]

        # Extra time for the second half (e.g., 90 + 1, 90 + 2)
        second_half_extra = [f"90 + {i}" for i in range(1, self.extra_time_second_half + 1)]

        # Combine the entire match timeline into a tuple
        timeline = ('pre_match',) + tuple(first_half + first_half_extra) + (
            'end_first_half', 'half_time', 'start_second_half') + tuple(second_half + second_half_extra) + ('post_match',)
        return timeline

    def calculate_extra_time(self):
        """
        Calculate extra time dynamically with weighted probabilities, peaking at 3 minutes.
        """
        weights = [5, 10, 30, 25, 14, 10, 4, 2]
        extra_time_values = list(range(1, 9))  # Extra time between 1 and 8 minutes
        return random.choices(extra_time_values, weights=weights)[0]

    def run_match(self):
        """
        Simulate the match by iterating through the match timeline and processing events.
        """

        for minute in self.match_minutes:
            self.event_manager.process_events(minute, self.match_report)  # Pass minute to EventManager
        return self.match_report

    def return_score(self):
        return self.score