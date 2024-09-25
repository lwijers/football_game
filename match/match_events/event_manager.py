import random
from match.match_events import event_checker, event_handler

class EventManager:
    def __init__(self, match_engine, game_stats):
        self.match_engine = match_engine
        self.event_bus = self.match_engine.event_bus
        self.game_stats = game_stats
        self.event_handler =event_handler.EventHandler(self, self.event_bus, self.match_engine)
        self.event_checker = event_checker.EventChecker(self.event_bus, self.event_handler, self.match_engine)

    def process_events(self, minute, report):
        """
        Check for specific events that might occur at this minute.
        """
        self.event_checker.check_events(minute, report)


