class Tile:
    '''
    blocked ： 是否有体积碰撞
    explored ： 是否探索过
    
    '''
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked
        self.explored = False
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight
        