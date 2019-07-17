class Fighter:
    def __init__(self, hp, defense, power, owner = None):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.owner = owner
    