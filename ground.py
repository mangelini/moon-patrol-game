from actor import Actor
import random

class Ground(Actor):
    def __init__(self, arena, pos, difficulty):
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
        self._state = ''
        self._x_bullet = 0
        self._boost = 0

    def get_ground(self):
        return self._h

    def symbol(self):
        return 0, 513, 512, 120
    
    def collide(self, other):
        pass
    
    def move(self):
        self._x -= self._speed + self._boost

        if self._x + self._w < 0:
            self._x = 0

    def position(self):
        return self._x, self._y, self._w, self._h     
    
    def second_position(self):
        return self._x + self._w, self._y, self._w, self._h
    
    def get_background(self):
        return self.grounds[self._cnt]
    
    def is_not_in_canvas(self, x_obs):
        if x_obs >= self._x + self._w + abs(self._x):
            return True
        else: 
            return False
    
    def get_state(self):
        return self._state
    
    def get_x(self):
        return self._x
    
    def boost(self):
        self._boost = 3
    
    def release_boost(self):
        self._boost = 0

