from actor import Actor

class Bomber(Actor):
    def __init__(self, arena, pos):
        self._x, self._y = pos
        self._arena = arena
        arena.add(self)
        self._state = ''
        self._speed = 15
    
    def symbol(self):
        if self._state == 'explode':
            self._state = 'delete'
            return 252, 137, 14, 16
        else:
            return 163, 248, 23, 12
    
    def move(self):
        arena_w, arena_y = self._arena.size()
        if self._x < arena_w:
            self._x += self._speed
        else:
            self._state = 'delete'
    
    def position(self):
        return self._x, self._y, 23, 12
    
    def get_state(self):
        return self._state
    
    def collide(self, other):
        from bullet import Bullet

        if isinstance(other, Bullet):
            self._state = 'explode'
            self._arena.add_to_score(20)
    
    def get_x(self):
        return self._x
    
