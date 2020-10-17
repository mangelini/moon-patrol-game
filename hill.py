from actor import Actor
from settings import *

class Hill(Actor):
    def __init__(self, arena, pos, level):
        self._x, self._y = pos
        self._w, self._h = 1280, 360
        self._speed = 1
        self._arena = arena
        arena.add(self)
        self.bgCanvas = False
        self._state = ''
        self._level = level

    def symbol(self):
        if self._level == 'level_1':
            return 0, 257, 512, 126
        else:
            return 0, 385, 512, 126
    
    def collide(self, other):
        pass
    
    def move(self):
        self._x -= self._speed

        if self._x + self._w < 0:
            self._x = 0

    def position(self):
        return self._x, self._y, self._w, self._h
    
    def second_position(self):
        return self._x + self._w, self._y, self._w, self._h
    
    def set_bigger_than_canvas(self, value: bool):
        self.bgCanvas = value
    
    def get_bigger_than_canvas(self):
        return self.bgCanvas
    
    def get_state(self):
        return self._state