import tcod as libtcod

class BasicEnemy:
    def __init__(self, owner = None):
        self.owner = owner
    def take_turn(self, target, fov_map, game_map, entities):
        enemy = self.owner
        if libtcod.map_is_in_fov(fov_map, enemy.x, enemy.y):
            if enemy.get_distance(target) >= 2:
                enemy.move_towards(target.x, target.y, game_map, entities)
            elif target.fighter.hp > 0:
                print('The {0} insults you!'.format(enemy.name))
            
        print('The '+self.owner.name + 'wonders when it will move')

    