from actor import Actor
from random import randint

class Bullet(Actor):
    def __init__(self, arena, pos, direction, b_type, difficulty):
        self._x, self._y = pos
        self._w, self._h = 1280, 105
        self._speed = 8
        self._arena = arena
        arena.add(self)
        self._cnt = 0
        self._state = ""
        self._x_max_distance = self._x + 150
        self._dir = direction
        self._y_max_distance = 600
        self._rand_hole = 0
        self._type = b_type
        self._difficulty = difficulty

    def symbol(self):
        if self._state != 'explode':
            if self._type == 'bomb':
                return 156, 266, 19, 18
            elif self._type == 'cannon':
                return 94, 248, 4, 1
            else:
                return 269, 141, 9, 10
        elif self._state == 'explode':
            self._state = 'delete'
            return 252, 137, 14, 16
    
    def collide(self, other):
        # This code is ambiguous because of 'circular dependencies'
        #or type(other) is Ground or type(other) is type(Bullet)
        from rock import Rock
        from ground import Ground
        from hole import Hole
        from rover import Rover

        if isinstance(other, Ground):
            if 20 <= randint(0, 100) <= 80:
                rand_dim_bullet_h = randint(1, 2)
                Hole(self._arena, (self._x, 600), rand_dim_bullet_h, self._difficulty) 

        if isinstance(other, Rock) or isinstance(other, Hole) or isinstance(other, Rover):
            self._state = 'explode'
    
    def move(self):
        if self._state != 'explode':
            if self._y < 0:
                self._state = 'delete'
            if self._dir == 'straight' and self._x < self._x_max_distance:
                self._x += self._speed
            elif self._dir == 'up':
                self._y -= self._speed
            elif self._dir == 'down' and self._y < self._y_max_distance:
                self._y += self._speed
            elif self._dir == 'down' and self._y >= self._y_max_distance:
                self._rand_hole = randint(1, 100)
                self._state = 'explode'
            elif self._dir == 'straight' and self._x >= self._x_max_distance:
                self._state = 'explode'
            elif self._dir == 'backward' and self._x > -self._x_max_distance:
                self._x -= self._speed + 8
            elif self._dir == 'backward' and self._x <= -self._x_max_distance:
                self._state = 'explode'

    def position(self):
        if self._type == 'bomb':
            return self._x, self._y, 19, 18
        elif self._type == 'cannon':
            return self._x, self._y, 4, 1
        elif self._state == 'explode':
            return self._x, self._y, 14, 16
        else:
            return self._x, self._y, 12, 12
    
    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_state(self):
        return self._state
    
    def set_state(self, state: str):
        self._state = state
    
    def create_random_hole(self) -> int:
        return self._rand_hole