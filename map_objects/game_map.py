import tcod as libtcod
from random import randint
from Entity import Entity
from map_objects.rectangle import Rect
from map_objects.tile import Tile
from components.fighter import Fighter
from components.ai import BasicEnemy


    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        '''
        地图的房间从全部为墙开始删减
        '''
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False       

    def create_enemy(self, room, entities, max_num_per_room):
        enemy_num = randint(0, max_num_per_room)

        for r in range(enemy_num):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if (randint(0, 100) <= 50):
                    fighter_component = Fighter(hp = 10, defense = 0, power = 2)
                    ai_component = BasicEnemy()
                    enemy = Entity(x, y, 'o', libtcod.desaturated_green, 'Goblin', blocks = True, fighter = fighter_component, ai = ai_component)


                else:
                    fighter_component = Fighter(hp = 30, defense = 1, power = 3)
                    ai_component = BasicEnemy()
                    enemy = Entity(x, y, 'T', libtcod.darker_green, 'Troll', blocks = True, fighter = fighter_component, ai = ai_component)

                
                entities.append(enemy)

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_num_per_room):
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)

            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1) 

            new_room = Rect(x, y, w, h)
            '''
            break会跳出这种写法的else
            即当该随机room与其他room均不交叉时才进入else
            '''
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                self.create_room(new_room)

                (new_x, new_y) = new_room.center()
                '''将玩家置于第一个房间，只有一个出口'''
                if num_rooms == 0:
                    player.x = new_x 
                    player.y = new_y
                else:
                    (prev_x, prev_y) = rooms[num_rooms-1].center()

                    if randint(0, 1) == 1:
                        self.create_h_tunnel(prev_x, new_x ,prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)
                self.create_enemy(new_room, entities, max_num_per_room)
                rooms.append(new_room)
                num_rooms += 1
    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False