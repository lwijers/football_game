
class Scene_base:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.next = self
        self.events = None

    def set_events(self, events):
        self.events = events

    def switch_to_scene(self, next_scene):
        self.next = next_scene(self.game_data)

    def process_events(self):
        print("uh-oh, you didn't override this in the child class")

    def update(self):
        print("uh-oh, you didn't override this in the child class")

    def draw(self, screen):
        print("uh-oh, you didn't override this in the child class")


