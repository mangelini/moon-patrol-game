#!/usr/bin/env python3
"""
    MOON PATROL v7.3
    Game inspired by: http://ascii-patrol.com/

    The game starts with a CLI for setting up the match.

    OBSERVATION: Don't know why but in vscode the current directory points at the previous folder (not Moon Patrol),
                    so I needed to specify the relative path 'Moon Patrol/score.txt'. Maybe it's just the compiler.
                    If you have problems with it try to detect the current directory with 'cwd = os.getcwd()' as shown
                    here: https://stackoverflow.com/questions/22282760/filenotfounderror-errno-2-no-such-file-or-directory
    
    BUGS: 
        - Sometimes aliens goes in the ground
        - Sometimes when the rover hit a rock it doesn't explode
        - Hitting the Spcebar when the rover is jumping destoys it
        - in co-op when a rover is destoyed the user can still create
            bullets because of design fault (when the object is deleted
            there still is an instance in the list)
"""

import g2d
from moon_patrol_game import MoonPatrolGame
from settings import *
from sys import exit
from os import system, name
import datetime

hero_lives = 2


class MoonPatrolGui:
    def __init__(self):
        self._settings = {}
        self.cli()
        self._game = MoonPatrolGame(self._settings)
        self.reset()
    
    def reset(self):
        self.sprites = g2d.load_image("https://tomamic.github.io/images/sprites/moon-patrol.png")
        self.background = g2d.load_image("https://tomamic.github.io/images/sprites/moon-patrol-bg.png")
        #self.game_over = g2d.load_image("moon-patrol-game-over.png") Not Working
        self._arena = self._game.arena()
        self._hero = self._game.hero()
        self._is_game_starting = True
        g2d.init_canvas(self._arena.size())

        if self._settings['level'] == 'level_1':
            g2d.main_loop(self.level_1_tick)
        else:
            g2d.main_loop(self.level_2_tick)

    def handle_keyboard(self):
        # Hero 1
        if g2d.key_pressed("ArrowUp") or self._hero[0].get_state() != "ground":
            if self._hero[0].get_state() == "ground":
                self._hero[0].set_offset(-6)
                self._hero[0].set_state("jumping_up")
            else:
                self._hero[0].jump()
        elif g2d.key_released("ArrowUp"):
            self._hero[0].stay()
        if g2d.key_pressed("ArrowRight"):
            self._game.ground_boost()
        elif g2d.key_released("ArrowRight"):
            self._game.ground_release_boost()
        elif g2d.key_pressed("ArrowLeft"):
            self._hero[0].go_left()
        elif g2d.key_released("ArrowLeft"):
            self._hero[0].stay()
        elif g2d.key_pressed("Spacebar"):
            self._game.hero_shoot_straight(0)
            self._game.hero_shoot_up(0)
        elif g2d.key_released('Spacebar'):
            self._hero[0].stay()
        
        # Hero 2
        if self._settings['mode'] == 'co-op':
            if g2d.key_pressed("w") or self._hero[1].get_state() != "ground":
                if self._hero[1].get_state() == "ground":
                    self._hero[1].set_offset(-6)
                    self._hero[1].set_state("jumping_up")
                else:
                    self._hero[1].jump()
            elif g2d.key_released("w"):
                self._hero[1].stay()
            if g2d.key_pressed("d"):
                self._game.ground_boost()
            elif g2d.key_released("d"):
                self._game.ground_release_boost()
            elif g2d.key_pressed("a"):
                self._hero[1].go_left()
            elif g2d.key_released("a"):
                self._hero[1].stay()
            elif g2d.key_pressed("s"):
                self._game.hero_shoot_straight(1)
                self._game.hero_shoot_up(1)
            elif g2d.key_released('s'):
                self._hero[1].stay()
    
    def level_1_tick(self):
        global hero_lives
        
        if self._game.game_won():
            self._game.reset(2, self._settings)
            g2d.alert("Level won")
            self._settings['level'] = 'level_2'
            self.reset()
        elif self._game.in_game():
            self._game.update_obstacles()
            self._game.generate_random_obstacles()

            if self._hero[0].get_x() < ROVER_X_TARGET and self._is_game_starting:
                for hero in self._hero:
                    hero.go_right()
                    hero.move()
            else:
                self._game.add_second_to_score()
                self._is_game_starting = False
                self._game.generate_alien()
                self._game.generate_random_bullet_from_aliens()
                self.handle_keyboard()
                self._arena.move_all()  # Game logic

            self.draw()
        else:
            hero_lives -= 1
            if self._game.game_over():
                g2d.alert("Game over")
                self.write_score()
                g2d.close_canvas()
            else:
                self._arena.add_to_score(-20)
                self._game.reset(hero_lives, self._settings, self._arena.get_score())
                self.reset()
    
    def level_2_tick(self):
        global hero_lives

        if self._game.game_won():
            g2d.alert("Game won")
            g2d.close_canvas()
        elif self._game.in_game():
            self._game.update_obstacles()

            if self._hero[0].get_x() < ROVER_X_TARGET and self._is_game_starting:
                for hero in self._hero:
                    hero.go_right()
                    hero.move()
            else:
                self._game.add_second_to_score()
                self._is_game_starting = False
                self._game.generate_bomber()
                self._game.bomber_shoot()
                self._game.generate_cannon()
                self._game.cannon_shoot()
                self._game.generate_alien()
                self._game.generate_random_bullet_from_aliens()
                self.handle_keyboard()
                self._arena.move_all() 
            
            self.draw()
        else:
            hero_lives -= 1
            if self._game.game_over():
                self.write_score()
                g2d.alert("Game over")
                #g2d.draw_image_clip(self.game_over, 0, 0, 3069, 1470, 0, 0, 1280, 720)
                g2d.close_canvas()
            else:
                self._arena.add_to_score(-20)
                self._game.reset(hero_lives, self._settings, self._arena.get_score())
                self.reset()

    def cli(self):
        choice = 0
        while choice != 1:
            print(
                            " _____________________\n"
                            "|    ______________  |\n"
                            "|                    |\n"
                            "|     MOON PATROL    |\n"
                            "|    ______________  |\n"
                            "|     __.______      |\n"
                            "|    / _____ \\_\\_    |\n"
                            "|    \\__  __   __\\   |\n"
                            "|    /__\\/\\ \\_/ /\\   |\n"
                            "|    \\__/\\_\\/ \\/_/   |\n"
                            "|____________________|\n")
        
            choice = int(input(
                'Insert:\n'
                '1 -> to setup the game\n'
                '2 -> to view the manual\n'
                '3 -> to view your highest score\n'
                '4 -> Exit\n'))
            
            if choice == 1:
                level = input('Level:\n'
                                ' 1 or 2? ')
                if level == '1':
                    self._settings['level'] = 'level_1'
                else:
                    self._settings['level'] = 'level_2'

                def_mode = input('Do you want to play in default mode? (y/n) ')

                if def_mode == 'y':
                    self._settings['mode'] = 'singleplayer'
                    self._settings['difficulty'] = 'Normal'
                else:
                    mode = input('Do you want to play in singleplayer or co-op? ')

                    if mode == 'singleplayer':
                        self._settings['mode'] = 'singleplayer'
                    else:
                        self._settings['mode'] = 'co-op'

                    difficulty = input('What level of difficulty do you want? (Easy, Normal, Hard) ')

                    self._settings['difficulty'] = difficulty
            elif choice == 2:
                man = self.read_manual()
                print(man)

                input('\nPress Enter to return to the menu\n')

            elif choice == 3:
                try:
                    score = self.read_score()
                    
                    if score != None:
                        print('\nYour highest score is: {}\nMade in: {}\n' .format(score[0], score[1]))
                except:
                    print('Play to make a score')
                    
                input('Press Enter to return to the menu\n')
            elif choice == 4:
                exit()
            
            # Clear screen for windows and linux/mac
            if name == 'nt': 
                _ = system('cls')
            else: 
                _ = system('clear')

        
    
    def draw(self):
        g2d.clear_canvas()
        for a in self._arena.actors():
            if type(a) in self._game.bg_list:
                g2d.draw_image_clip(self.background, a.symbol(), a.position())
                g2d.draw_image_clip(self.background, a.symbol(), a.second_position())
            else:
                g2d.draw_image_clip(self.sprites, a.symbol(), a.position())
            if a.get_state() == 'delete':
                self._arena.remove(a)
        
        g2d.set_color((255, 255, 255))
        g2d.draw_text('Remaining time: ' + str(self._game.remaining_time()), (10, 10), 20)
        g2d.draw_text('Score: ' + str(self._arena.get_score()), (ARENA_W/2, 10), 20)
        g2d.draw_text('Lives: ' + str(hero_lives + 1), (ARENA_W-80, 10), 20)
    
    def read_score(self):
        with open('score.txt', 'r') as f1:
            for line in f1:
                result = line.split()

        return result
    
    def write_score(self):
        result = self.read_score()
            
        if int(result[0]) < self._arena.get_score():
            with open('score.txt', 'w') as f2:
                d = datetime.datetime.now()
                f2.write(str(self._arena.get_score()) + ' ' + d.strftime('%Y:%H:%M') + ' ' + d.strftime('%X'))
    
    def read_manual(self):
        with open('manual.txt', 'r') as f:
            result = f.read()
        
        return result


gui = MoonPatrolGui()