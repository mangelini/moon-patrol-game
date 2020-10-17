from actor import Actor
from settings import *


class Rover(Actor):
    def __init__(self, arena, pos, r_type):
        self._x, self._y = pos
        self._w, self._h = 50, 30
        self._dx, self._dy = 0, 0
        self._arena = arena
        self._g = 0.4
        self._speed = 3
        arena.add(self)
        self._arena_w, self._arena_h = self._arena.size()
        self._state = "ground"
        self._boost = 0
        self.r_lives = 3
        self._type = r_type

    def move(self):
        self._y += self._dy

        if self._y < self._arena_h - self._h - 120:
            if self._dy < 0:
                self._state = "jumping_up"
            else:
                self._state = "jumping_down"
        elif self._y > self._arena_h - self._h - 120:
            self._state = "ground"
            self._y = self._arena_h - self._h - 120

        self._x += self._dx
        if self._x < 0:
            self._x = 0
        elif self._type == 1 and self._x == ROVER_X_TARGET:
            self._dx = 0
        elif self._type == 2 and self._x == ROVER_2_X_TARGET:
            self._dx = 0
        elif self._x > self._arena_w - self._w:
            self._x = self._arena_w - self._w

    def go_right(self):
        self._dx, self._dy = +self._speed, 0

    def set_offset(self, offset):
        self._dy = offset

    def go_left(self):
        self._dx, self._dy = -self._speed, 0

    def jump(self):
        self._dy += self._g

    def stay(self):
        self._dx, self._dy = 0, 0

        if (self._x > ROVER_X_TARGET and self._type == 1) or (self._x > ROVER_2_X_TARGET and self._type == 2):
            self._dx = -self._speed
        elif (self._x < ROVER_X_TARGET and self._type == 1) or (self._x < ROVER_2_X_TARGET and self._type == 2):
            self._dx += 1

    def collide(self, other):
        from hole import Hole
        from rock import Rock
        from bullet import Bullet
        if type(other) is Hole:
            self._state = 'fall'
            self._y += 21
        elif isinstance(other, Rock) or isinstance(other, Bullet):
            self._state = 'explode'

    def position(self):
        return self._x, self._y, self._w, self._h

    """
        If the rover has not collided with an obstacle
        return one of the three states. Otherwise return
        symbols for the explosion
    """

    def symbol(self):
        if self._state != 'fall' and self._state != 'explode' and self._type == 1:
            return 248, 157, 33, 27
        elif self._state != 'fall' and self._state != 'explode' and self._type == 2:
            return 212, 157, 33, 27
        else:
            self._state = 'delete'
            return 174, 286, 29, 32

    def set_state(self, state):
        self._state = state

    def get_state(self):
        return self._state

    def get_x(self):
        return self._x
    
    def lives(self):
        return self.r_lives
