from actor import Actor, Arena


class Rock(Actor):
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
        self._dim = dim
        self._i = 0
        self._state = ''
        self._boost = 0

    def symbol(self):
        if self._state != 'explode':
            if self._dim == 1:
                return 80, 203, 14, 12
            else:
                return 112, 199, 13, 16
        else:
            self._state = 'delete'
            return 143, 296, 26, 22
    
    def collide(self, other):
        from bullet import Bullet

        if type(other) is Bullet:
            if self._dim == 2 and self._i == 2:
                self._state = 'explode'
                self._arena.add_to_score(5)
            elif self._dim == 1:
                self._state = 'explode'
                self._arena.add_to_score(5)   
            else:
                self._i += 1
                
    def move(self):
        if self._x >= 0:
            self._x -= self._speed + self._boost
        else: 
            self._state = 'delete'

    def position(self):
        if self._dim == 1:
            return self._x, self._y - 20, 25, 30
        else:
            return self._x, self._y - 30, 35, 50
    
    def get_x(self):
        return self._x

    def get_state(self):
        return self._state
    
    def boost(self):
        self._boost = 3
    
    def release_boost(self):
        self._boost = 0