import random
from match.match_comments import commentaries
from match import match_report

MATCH_LENGTH = 90
HALF_LENGTH = 45
COMMENT_DURATION = 5
TICKS_PER_MINUTE = 12

class Match_engine:
    PRE_MATCH = "pre_match"
    END_FIRST_HALF = "end_first_half"

    def __init__(self, home_team, away_team):
        self.team_stats = {"home": home_team, "away": away_team}
        self.match_stats = self.initialize_match_stats()
        self.commentaries = commentaries.commentaries
        self.match_report = match_report.Match_report(self)

        self.current_possession = ""
        # self.last_tick_time = time.time()
        # self.current_tick = 0
        self.has_run = False  # Flag to check if the match has been run
        self.match_length = MATCH_LENGTH
    def initialize_match_stats(self):
        return {
            "home": {"possession_counter": 0, "possession_total": 0.0, "score": 0, "shots": 0, "shots_on_goal": 0},
            "away": {"possession_counter": 0, "possession_total": 0.0, "score": 0, "shots": 0, "shots_on_goal": 0}
        }

    def generate_match_report(self):
        extra_time = (self.calculate_extra_time(), self.calculate_extra_time())
        self.match_length = MATCH_LENGTH + sum(extra_time)

        self.match_report.add_entry(self.PRE_MATCH, 0, team_a=self.team_stats["home"]["name"],
                                    team_b=self.team_stats["away"]["name"])

        for minute in range(1, 91 + max(extra_time)):
            if self.process_minute(minute, extra_time):
                break  # Stop if match has ended

    def process_minute(self, minute, extra_time):
        displayed_minute = self.format_minute(minute, 45 if minute <= 45 + extra_time[0] else 90)

        # handle basic match events  (half time, extra time, full time)
        if minute <= 45 + extra_time[0]:  # First half
            if minute == 40: # Extra time called
                self.match_report.add_entry("extra_half_time", minute, extra_time=extra_time[0])
            if minute == 45 + extra_time[0]:  # End of first half
                self.match_report.add_entry(self.END_FIRST_HALF, displayed_minute,
                                            score=f'{self.match_stats["home"]["score"]} - {self.match_stats["away"]["score"]}')
                self.match_report.add_entry("half_time", displayed_minute)
                self.match_report.add_entry("start_second_half", "46", team_a=self.team_stats["away"]["name"],
                                            team_b=self.team_stats["home"]["name"])

        elif 46 <= minute <= 90 + extra_time[1]:  # Second half
            if minute == 85:  # Extra time called
                self.match_report.add_entry("extra_time_second_half", minute, extra_time=extra_time[1])
            if minute == 90 + extra_time[1]:  # End of second half
                self.match_report.add_entry("end_match", displayed_minute, team_a=self.team_stats["home"]["name"],
                                            team_b=self.team_stats["away"]["name"],
                                            score_a=str(self.match_stats["home"]["score"]),
                                            score_b=str(self.match_stats["away"]["score"]))
                return True  # Match ended


        self.calculate_possession()
        print(
            f"Minute: {displayed_minute}, Home Possessions: {self.match_stats['home']['possession_counter']}, Away Possessions: {self.match_stats['away']['possession_counter']}")
        self.match_report.add_entry("match_commentary", displayed_minute)
        return False

    def format_minute(self, minute, regular_time_limit):
        return f"{regular_time_limit} + {minute - regular_time_limit}" if minute > regular_time_limit else str(minute)

    def calculate_extra_time(self):
        weights = [5, 10, 30, 25, 14, 10, 4, 2]
        extra_time_values = list(range(1, 9))
        return random.choices(extra_time_values, weights=weights)[0]

    def update(self):
        if not self.has_run:  # Check if the match has not been run
            self.generate_match_report()
            self.has_run = True  # Set flag to indicate the match has been run
            print(self.match_report.generate_report())
            # print(self.match_stats)

    def calculate_possession(self):
        midfield_stats = self.team_stats["home"]["midfield"] + self.team_stats["away"]["midfield"]
        possession_chance = random.random()

        if possession_chance <= self.team_stats["home"]["midfield"] / midfield_stats:
            self.current_possession = "home"
        else:
            self.current_possession = "away"

        # Always increment the possession counter for the team that currently has possession
        self.match_stats[self.current_possession]["possession_counter"] += 1
        self.match_stats[self.current_possession]["possession_total"] = self.match_stats[self.current_possession][
                                                                            "possession_counter"] / self.match_length

    # def attack(self, possession):
    #     opponent = "away" if possession == "home" else "home"
    #
    #     # Retrieve attack, defense, and goalkeeper stats for both teams
    #     attack_strength = self.team_stats[possession]["attack"]
    #     defense_strength = self.team_stats[opponent]["defense"]
    #     goalkeeper_strength = self.team_stats[opponent]["goalkeeper"]
    #
    #     # Step 1: Chance of taking a shot
    #     shot_chance = attack_strength / (attack_strength + defense_strength + 5)
    #     if random.random() < shot_chance:
    #         self.match_stats[possession]["shots"] += 1
    #         print(random.choice(self.commentaries["uncertain_shot"]))
    #
    #         # Step 2: Chance of the shot being on target
    #         shot_on_target_chance = attack_strength / 40
    #         if random.random() < shot_on_target_chance:
    #             self.match_stats[possession]["shots_on_goal"] += 1
    #
    #             # Step 3: Chance of the shot resulting in a goal
    #             goal_chance = (attack_strength - defense_strength) / (30 + goalkeeper_strength)
    #             if random.random() < max(goal_chance, 0):
    #                 self.match_stats[possession]["score"] += 1
    #                 print(random.choice(self.commentaries["goal"]))
    #                 print(f"!!!!!!GOAL for {possession.upper()}!!!!!!")
    #             else:
    #                 print(random.choice(self.commentaries["shot_on_target_saved"]))
    #         else:
    #             print(random.choice(self.commentaries["missed_target_shot"]))
    #     else:
    #         print(random.choice(self.commentaries["default"]))
    #
    # def end_game(self):
    #     return self.current_tick >= self.match_length  # Check if the match is over
    #
    # def print_minute_stats(self, minute):
    #     print(f"-----------MINUTE {minute + 1}-----------")
    #     print(f"Possession: {self.current_possession}")
    #     print(f"Score: Home {self.match_stats['home']['score']} - Away {self.match_stats['away']['score']}")
    #
    # def print_match_stats(self):
    #     print("-----------FULL TIME-----------")
    #     print(f"Home Team Possession: {round(self.match_stats['home']['possession_total'] * 100)}% - Away Team Possession: {round(self.match_stats['away']['possession_total'] * 100)}%")
    #     print(f"Home Team Score: {self.match_stats['home']['score']}")
    #     print(f"Away Team Score: {self.match_stats['away']['score']}")
    #     print(f"Home Team Shots: {self.match_stats['home']['shots']} (On Target: {self.match_stats['home']['shots_on_goal']})")
    #     print(f"Away Team Shots: {self.match_stats['away']['shots']} (On Target: {self.match_stats['away']['shots_on_goal']})")
