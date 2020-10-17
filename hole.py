from actor import Actor, Arena

class Hole(Actor):
    def __init__(self, arena, pos, dim, difficulty):
        self._x, self._y = pos
        self._w, self._h = 1280, 120
        if difficulty == 'Easy':
            self._speed = 4
        elif difficulty == 'Normal':
            self._speed = 5
        else:
            self._speed = 6
        self._arena = arena
        arena.add(self)
        self._arena_w, self._arena_h = self._arena.size()
        self._dim = dim
        self._state = ''
        self._boost = 0

    def symbol(self):
        if self._dim == 1:
            return 154, 140, 25, 21
        else:
            return 159, 167, 23, 28
    
    def collide(self, other):
        pass
    
    def move(self):
        if self._x >= 0:
            self._x -= self._speed + self._boost
        else: 
            self._state = 'delete'

    def position(self):
        if self._dim == 1:
            return self._x, self._y - 1, 40, 35
        else:
            return self._x, self._y - 1, 70, 45
    
    def get_x(self):
        return self._x
    
    def get_state(self):
        return self._state
    
    def boost(self):
        self._boost = 3
    
    def release_boost(self):
        self._boost = 0
