from object import Object

class Player(Object):
    def __init__(self, x, y, char, name, color, fighter_component, race):
        self.inventory = []
        self.level = 1

        Object.__init__(self, x, y, char, name, color, blocks=True, fighter=fighter_component, race=race)

    def get_range(self):
        equipment = self.fighter.get_all_equipped()
        range = self.fighter.range
        for item in equipment:
            range += item.range
        return range
