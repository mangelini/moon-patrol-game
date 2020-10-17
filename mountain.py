from actor import Actor
from settings import *

class Mountain(Actor):
    def __init__(self, arena, pos):
        self._x, self._y = pos
        self._w, self._h = 1280, 720
        self._speed = 1
        self._arena = arena
        arena.add(self)
        self.bgCanvas = False
        self._state = ''

    def symbol(self):
        return 0, 90, 512, 174
    
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