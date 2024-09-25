class EventHandler:
    def __init__(self, event_manager, event_bus, match_engine):
        self.match_engine = match_engine
        self.event_manager = event_manager
        self.subscriptions = {
            "pre_match": self.on_pre_match,
            "announce_extra_time_first_half": self.on_announce_extra_time_first_half,
            "end_first_half": self.on_end_first_half,
            "half_time": self.on_half_time_event,
            "start_second_half": self.on_start_second_half,
            "announce_extra_time_second_half": self.on_announce_extra_time_second_half,
            "post_match": self.on_post_match,
            "switch_possession": self.on_switch_possession,
            "keeps_possession": self.on_keeps_possession,
        }
        self.setup_subscriptions(event_bus)

    def setup_subscriptions(self, event_bus):
        for event, handler in self.subscriptions.items():
            event_bus.subscribe(event, handler)

    # def handle_base_events(self, minute, report):
    #     event, kwargs = self.event_manager.event_checker.event_schedule[minute]
    #     event(report, minute, **kwargs)  # Trigger the event with its respective arguments

    def on_pre_match(self, minute, report, game_stats):
        report.add_entry('pre_match', 0, must_display=True, team_a=game_stats['home_team']['name'], team_b=game_stats['away_team']['name'])

    def on_announce_extra_time_first_half(self, minute, report, game_stats):
        report.add_entry('announce_extra_time_first_half', minute, must_display=True, extra_time=game_stats['extra_time_first_half'])

    def on_end_first_half(self, minute, report, game_stats):
        report.add_entry('end_first_half', 45 + self.match_engine.extra_time_first_half + 1, must_display=True, score=f"{game_stats['home_team']['score']} - {game_stats['away_team']['score']}")


    def on_half_time_event(self, minute, report, game_stats):
        report.add_entry('half_time_event', 45, must_display=True)

    def on_start_second_half(self, minute, report, game_stats):
        report.add_entry('start_second_half', 46, must_display=True, team_a=game_stats['home_team']['name'], team_b=game_stats['away_team']['name'])

    def on_announce_extra_time_second_half(self, minute, report, game_stats):
        report.add_entry('announce_extra_time_second_half', minute, must_display=True, extra_time=game_stats['extra_time_second_half'])

    def on_post_match(self, minute, report, game_stats):
        report.add_entry('post_match', 90 + self.match_engine.extra_time_second_half + 1, must_display=True, team_a=game_stats['home_team']['name'], team_b=game_stats['away_team']['name'],
                         score_a=game_stats['home_team']['score'], score_b=game_stats['away_team']['score'])

    def on_switch_possession(self, minute, report, game_stats, team_in_possession):
        # print(f"Minute {minute}: Handling possession switch event. Team in possession: {team_in_possession}")

        team_lost_possession = 'home_team' if team_in_possession == 'away_team' else 'away_team'
        game_stats['has_possession'] = team_in_possession
        game_stats['no_possession'] = team_lost_possession

        game_stats[team_in_possession]["possession_counter"] += 1
        game_stats[team_lost_possession]["possession_counter"] = 0  # Reset for the team that lost possession


        report.add_entry('switch_possession', minute, team_ball_gained=game_stats[team_in_possession]["name"],
                         team_ball_lost=game_stats[team_lost_possession]["name"])

    def on_keeps_possession(self, minute, report, game_stats, team_in_possession):
        # print(f"Minute {minute}: Handling keeps possession event. Team in possession: {team_in_possession}")
        game_stats['has_possession'] = team_in_possession
        report.add_entry('keeps_possession', minute, team_in_possession=team_in_possession)


        report.add_entry('keeps_possession', minute, team_in_possession=team_in_possession)