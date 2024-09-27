import json
import random


class Player:
    _id_counter = 0

    def __init__(self, first_name, last_name, position, age, current_ability, potential_ability):
        self.id = Player._id_counter  # Assign the current ID
        Player._id_counter += 1

        # Initialize attributes
        self.attributes = {
            'first_name': first_name,
            'last_name': last_name,
            'position': position,
            'age': age,
            'current_ability': current_ability,
            'potential_ability': potential_ability,
            'attack': 0,
            'midfield': 0,
            'defense': 0,
            'goalkeeping': 0
        }

    def __str__(self):
        """Return a formatted string with the player's information."""
        return (f"ID: {self.id}, Name: {self.attributes['first_name']} {self.attributes['last_name']}, "
                f"Position: {self.attributes['position']}, Age: {self.attributes['age']}, "
                f"Current Ability: {self.attributes['current_ability']}, "
                f"Potential Ability: {self.attributes['potential_ability']}, "
                f"Attack: {self.attributes['attack']}, Defense: {self.attributes['defense']}, "
                f"Midfield: {self.attributes['midfield']}, goalkeeping: {self.attributes['goalkeeping']}")


class PlayerGenerator:
    def __init__(self):
        # Load names from the JSON file (names.json)
        with open('names.json', 'r') as file:
            data = json.load(file)

        self.dutch_first_names = data['dutch_first_names']
        self.dutch_surnames = data['dutch_surnames']
        self.other_first_names = data['other_first_names']
        self.other_surnames = data['other_surnames']
        self.positions = ['Forward', 'Midfielder', 'Defender', 'Goalkeeper']

        self.ability_cap = 10
        self.points_per_ability_level = 10

    def random_name(self):
        """Select a random name with 70% Dutch names and 30% other names."""
        if random.random() < 0.7:
            first_name = random.choice(self.dutch_first_names)
            surname = random.choice(self.dutch_surnames)
        else:
            first_name = random.choice(self.other_first_names)
            surname = random.choice(self.other_surnames)
        return first_name, surname

    def random_position(self, role):
        """Select a random position."""
        if role:
            return role
        return random.choice(self.positions)

    def random_age(self):
        """Generate a random age for the player (between 18 and 40)."""
        return random.randint(18, 40)

    def generate_player(self, role=None, ca=None, pa=None):
        """Generate a single player with random attributes."""
        first_name, last_name = self.random_name()
        position = self.random_position(role)
        age = self.random_age()

        if ca == None:
            current_ability = random.randint(1, self.ability_cap)
        else:
            current_ability = ca
        if pa == None:
            potential_ability = random.randint(current_ability, self.ability_cap)  # Potential can't be lower than current
        else:
            potential_ability = pa
        # Generate current and potential abilities based on position
        # current_ability = random.rr.randint(current_ability, 10)  # Potential can't be lower than current

        # Create the player
        player = Player(first_name, last_name, position, age, current_ability, potential_ability)

        # Distribute stats based on position
        self.distribute_stats(player)

        return player

    def distribute_stats(self, player):
        # TODO: Add a weighted price per skill allocation point depending on the player's position
        # TODO: fine tune skill cap and allcation points
        points_to_spend = player.attributes['current_ability'] * self.points_per_ability_level
        distribution_chances = {
            'Forward': {'attack': 0.6, 'midfield': 0.24, 'defense': 0.15, 'goalkeeping': 0.01},
            'Midfielder': {'attack': 0.15, 'midfield': 0.6, 'defense': 0.15, 'goalkeeping': 0.1},
            'Defender': {'attack': 0.1, 'midfield': 0.2, 'defense': 0.6, 'goalkeeping': 0.1},
            'Goalkeeper': {'attack': 0.05, 'midfield': 0.15, 'defense': 0.2, 'goalkeeping': 0.6}
        }

        # Select the distribution based on the player's position
        distribution = distribution_chances[player.attributes['position']]

        # Calculate cumulative probabilities
        cumulative_distribution = []
        cumulative_sum = 0.0
        for stat, chance in distribution.items():
            cumulative_sum += chance
            cumulative_distribution.append((stat, cumulative_sum))

        # Allocate points based on the cumulative distribution
        while points_to_spend > 0:
            roll = random.random()  # Generates a float between 0.0 and 1.0
            allocated = False  # Reset allocated flag for each point

            for stat, cumulative_probability in cumulative_distribution:
                if roll < cumulative_probability:
                    player.attributes[stat] += 1  # Allocate a point to the skill
                    points_to_spend -= 1  # Decrease the points to spend
                    allocated = True  # Mark that a point was allocated
                    break  # Exit the loop after allocating a point

            if not allocated:
                print("Failed to allocate a point. Falling back to the highest chance stat.")

    def generate_players(self, num_players,  role=None, ca=None, pa=None):
        """Generate multiple players."""
        players = []
        for _ in range(num_players):
            player = self.generate_player(ca=ca, pa=ca, role=role)
            players.append(player)
        return players


# Example usage
player_gen = PlayerGenerator()

# Generate a single player
# Generate multiple players
for role in ['Forward', 'Midfielder', 'Defender', 'Goalkeeper']:
    players = player_gen.generate_players(10, role=role,ca=1)
    for player in players:
        print(player)
