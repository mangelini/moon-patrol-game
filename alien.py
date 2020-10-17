from actor import Actor
from random import choice


class Alien(Actor):
    def __init__(self, arena, pos, level):
        self._x, self._y = pos
        self._w, self._h = 20, 20
        self._arena = arena
        arena.add(self)
        self._arena_w, self._arena_h = self._arena.size()
        self._state = ''
        self._level = level

    def move(self):
        if self._y < 0:
            self._state = 'delete'
        else:
            dx = choice([-20, -15, -10, -5, 0, 5, 10, 15, 20])
            dy = choice([-5, 0, 5])

            self._x = (self._x + dx) % self._arena_w
            self._y = (self._y + dy) % self._arena_h

    def collide(self, other):
        from bullet import Bullet

        if type(other) is Bullet:
            self._arena.add_to_score(20)
            self._state = 'delete'

    def position(self):
        return self._x, self._y, 16, 10

    def symbol(self):
        if self._level == 'level_1':
            return 140, 230, 16, 7
        else:
            return 67, 229, 16, 10
    
    def get_x(self):
        return self._x
    
    def get_y(self):
        return self._y
    
    def get_state(self):
        return self._state
