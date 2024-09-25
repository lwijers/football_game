import random

class EventChecker:
    def __init__(self, event_bus, event_handler, match_engine):
        self.event_handler = event_handler
        self.match_engine = match_engine
        self.event_bus = event_bus

    def check_events(self, minute, report):
        """
        Check for base events and trigger if they occur.
        """
        if minute == 'pre_match':
            self.event_bus.publish("pre_match", minute=minute, report=report, game_stats=self.match_engine.game_stats)

        elif minute == '40':
            self.event_bus.publish("announce_extra_time_first_half", minute=minute, report=report, game_stats=self.match_engine.game_stats)

        elif minute == 'end_first_half':
            self.event_bus.publish("end_first_half", minute=minute, report=report, game_stats=self.match_engine.game_stats)

        elif minute == 'half_time':
            self.event_bus.publish("half_time", minute=minute, report=report, game_stats=self.match_engine.game_stats)

        elif minute == 'start_second_half':
            self.event_bus.publish("start_second_half", minute=minute, report=report, game_stats=self.match_engine.game_stats)

        elif minute == '85':
            self.event_bus.publish("announce_extra_time_second_half", minute=minute, report=report, game_stats=self.match_engine.game_stats)

        elif minute == 'post_match':
            self.event_bus.publish("post_match", minute=minute, report=report, game_stats=self.match_engine.game_stats)

        else:
            self.check_dynamic_events(minute, report, self.match_engine.game_stats)

    def check_possession_switch(self, minute, report, game_stats):
        midfield_stats = game_stats["home_team"]["midfield"] + game_stats["away_team"]["midfield"]
        possession_chance = random.random()


        # Check if home team should win possession
        if possession_chance <= game_stats["home_team"]["midfield"] / midfield_stats:
            if game_stats['has_possession'] == "home_team":
                # print(f"Minute {minute}: Home team keeps possession.")
                self.event_bus.publish('keeps_possession', minute=minute, report=report, game_stats=game_stats,
                                       team_in_possession="home_team")
            else:
                # print(f"Minute {minute}: Switching possession to home team.")
                self.event_bus.publish('switch_possession', minute=minute, report=report, game_stats=game_stats,
                                       team_in_possession="home_team")
                game_stats['has_possession'] = "home_team"  # Update possession status
        else:
            if game_stats['has_possession'] == "away_team":
                # print(f"Minute {minute}: Away team keeps possession.")
                self.event_bus.publish('keeps_possession', minute=minute, report=report, game_stats=game_stats,
                                       team_in_possession="away_team")
            else:
                # print(f"Minute {minute}: Switching possession to away team.")
                self.event_bus.publish('switch_possession', minute=minute, report=report, game_stats=game_stats,
                                       team_in_possession="away_team")
                game_stats['has_possession'] = "away_team"  # Update possession status

    def check_dynamic_events(self, minute, report, game_stats):
        self.check_possession_switch(minute, report, self.match_engine.game_stats)

