from actor import Actor
from time import time


class Cannon(Actor):
    def __init__(self, arena, pos):
        self._x, self._y = pos
        self._speed = 6
        self._arena = arena
        arena.add(self)
        self._state = ''
        self._w, self._h = 40, 30
        self._start_time = time()
        self._boost = 0
        
    def symbol(self):
        if self._state == 'explode':
            self._state = 'delete'
            return 174, 286, 29, 32
        else:
            return 107, 243, 20, 20
    
    def move(self):
        self._x -= self._speed + self._boost
    
    def get_x(self):
        return self._x
    
    def get_state(self):
        return self._state
    
    def collide(self, other):
        from bullet import Bullet

        if isinstance(other, Bullet):
            self._state = 'explode'
            self._arena.add_to_score(20)

    def position(self):
        return self._x, self._y, self._w, self._h 
    
    def get_start_time(self):
        return self._start_time
    
    def set_start_time(self, start_time):
        self._start_time = start_time
    
    def boost(self):
        self._boost = 3
    
    def release_boost(self):
        self._boost = 0
    