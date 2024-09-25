from match.match_comments import comment_generator


class Match_report:
    def __init__(self, match_engine):
        self.match_engine = match_engine

        self.entries = []
        self.comment_generator = comment_generator.CommentGenerator("match/match_comments/comments.json")

    def add_entry(self, comment, minute, must_display=False, **kwargs):
        comment = self.comment_generator.generate_comment(comment, **kwargs)


        report_entry = {
            "minute": minute,
            "comment": comment,
            "must_display" : must_display
        }
        self.entries.append(report_entry)

    def get_all_entries(self):
        return self.entries  # Return all entries in structured format

    def generate_report(self):
        """Generates a formatted match report."""
        report_lines = []
        for entry in self.entries:
            line = (f"Minute {entry['minute']}: {entry['comment']}  "
                    # f"Score: {entry['score']} | "
                    # f"Team in possession: {entry['possession']} | "
                    # f"Total possession: {entry['total_possession']} | "
                    # f"Shots: {entry['shots']} | "
                    # f"Shots on Goal: {entry['shots_on_goal']}")
                    )
            report_lines.append(line)
        return "\n".join(report_lines)
