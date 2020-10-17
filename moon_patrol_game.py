#!/usr/bin/env python3

from time import time
from actor import Actor, Arena
from rover import Rover
from ground import Ground
from mountain import Mountain
from hill import Hill
from hole import Hole
from rock import Rock
from bullet import Bullet
from alien import Alien
from settings import *
from cannon import Cannon
from random import randint, choice
from bomber import Bomber


class MoonPatrolGame:
    def __init__(self, settings):
        self.reset(3, settings, 0)

    def arena(self) -> Arena:
        return self._arena

    def reset(self, lives: int, settings: dict, score: int):
        self._settings = settings
        self._arena = Arena((ARENA_W, ARENA_H))
        self._arena.add_to_score(score)
        Mountain(self._arena, (MOUNTAIN_X, MOUNTAIN_Y))
        Hill(self._arena, (HILL_X, HILL_Y), self._settings['level'])
        self._ground = Ground(self._arena, (GROUND_X, GROUND_Y), self._settings['difficulty'])
        self._start_time = time()
        self.bg_list = [Mountain, Hill, Ground]
        self._time_to_generate_alien = time()
        self._hero = []
        self._hero.append(Rover(self._arena, (ROVER_X, ROVER_Y), 1))
        if self._settings['mode'] == 'co-op':
            self._hero.append(Rover(self._arena, (ROVER_2_X, ROVER_2_Y), 2))

        self._start = time()
        self._playtime = 80
        self.hero_lives = lives
        self._aliens = []
        self._obstacles = []
        self._type_obstacles = [Rock, Hole]
        self._rand_x_bomb = 0
        self._time_to_generate_bomber = time()
        self._bomb_ready = False
        self._second = time()

        if self._settings['difficulty'] == 'Easy':
            self.OBS_RANGE = 400
        elif self._settings['difficulty'] == 'Normal':
            self.OBS_RANGE = 300
        else:
            self.OBS_RANGE = 200

    def hero(self) -> Rover:
        return self._hero

    def hero_shoot_straight(self, i: int):
        Bullet(self._arena, (self._hero[i].get_x() + 50, 580), 'straight', 'normal', self._settings['difficulty'])

    def hero_shoot_up(self, i: int):
        Bullet(self._arena, (self._hero[i].get_x() + 8, 540), 'up', 'normal', self._settings['difficulty'])

    def game_over(self) -> bool:
        if self.hero_lives == 0:
            return True
        else:
            return False

    def in_game(self) -> bool:
        if any(isinstance(a, Rover) for a in self._arena.actors()):
            return True
        else:
            return False

    def game_won(self) -> bool:
        return time() - self._start > self._playtime

    def remaining_time(self) -> int:
        return int(self._start + self._playtime - time())

    def generate_random_obstacles(self):
        obstacleInRange = True
        rand_obs = randint(0, ARENA_W * 2)
        rand_dim_o = randint(1, 2)

        for o in self._obstacles:
            if o.get_x() == rand_obs:
                obstacleInRange = False

        if obstacleInRange:
            if self._ground.is_not_in_canvas(rand_obs) == True:
                for obs in self._obstacles:
                    if not(rand_obs <= obs.get_x() - self.OBS_RANGE or rand_obs >= obs.get_x() + self.OBS_RANGE):
                        obstacleInRange = False
                if obstacleInRange:
                    obstacle = choice(self._type_obstacles)
                    self._obstacles.append(obstacle(self._arena, (rand_obs, OBS_Y), rand_dim_o, self._settings['difficulty']))

    def generate_alien(self):
        self._aliens.clear()
        actors = self._arena.actors()

        for a in actors:
            if type(a) is Alien:
                self._aliens.append(a)

        if len(self._aliens) < 2 and time() - self._time_to_generate_alien > 20:
            rand_x_alien = randint(100, 740)
            rand_y_alien = randint(150, 250)

            self._aliens.append(Alien(self._arena, (rand_x_alien, rand_y_alien), self._settings['level']))
            self._time_to_generate_alien = time()

    def generate_random_bullet_from_aliens(self):
        if time() - self._start_time > 8:
            for alien in self._aliens:
                Bullet(self._arena, (alien.get_x() + 5, alien.get_y() + 10), 'down', 'normal', self._settings['difficulty'])
            self._start_time = time()
    
    def generate_cannon(self):
        if self._ground.get_x() < ARENA_W:
            actors = self._arena.actors()
            cannon_available = True
            rand_cannon_x = randint(ARENA_W, ARENA_W*2)

            for a in self._obstacles:
                if isinstance(a, Cannon) or rand_cannon_x == a.get_x():
                    cannon_available = False
                
            if cannon_available:
                self._obstacles.append(Cannon(self._arena, (rand_cannon_x, 570)))
    
    def cannon_shoot(self):
        for o in self._obstacles:
            if isinstance(o, Cannon):
                if not(self._ground.is_not_in_canvas(o.get_x())):
                    if time() - o.get_start_time() > 3:
                        Bullet(self._arena, (o.get_x() - 10, 580), 'backward', 'cannon', self._settings['difficulty'])
                        o.set_start_time(time())
    
    def update_obstacles(self):
        self._obstacles.clear()

        for a in self._arena.actors():
            if isinstance(a, Rock) or isinstance(a, Hole) or isinstance(a, Cannon):
                self._obstacles.append(a)
    
    def ground_boost(self):
        for o in self._obstacles:
            o.boost()
    
    def ground_release_boost(self):
        for o in self._obstacles:
            o.release_boost()
    
    def generate_bomber(self):
        if time() - self._time_to_generate_bomber > 8:
            Bomber(self._arena, (0, 80))
            self._rand_x_bomb = randint(0, ARENA_W)
            self._bomb_ready = True
            self._time_to_generate_bomber = time()

    def bomber_shoot(self):
        for a in self._arena.actors():
            if isinstance(a, Bomber):
                if a.get_x() >= self._rand_x_bomb and self._bomb_ready:
                    self._bomb_ready = False
                    Bullet(self._arena, (a.get_x(), 88), 'down', 'bomb', self._settings['difficulty'])

    def add_second_to_score(self):
        if time() - self._second > 1:
            if self._settings['difficulty'] == 'Hard':
                self._arena.add_to_score(3)
            elif self._settings['difficulty'] == 'Normal':
                self._arena.add_to_score(2)
            else:
                self._arena.add_to_score(1)
            self._second = time()
