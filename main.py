"""
Sobel Nibbles
Made with PyGame
"""

import numpy as np
import pygame
import random

random.seed(557982)
import math
import sys
import time

from Snake import *


class Simulator:
    def __init__(self, stamina, life, step, pixel_size, scores, Snake_Count, x_length=540, y_length=400,
                 turning_penalty=1):
        self.food_score = None
        # Window size 540 and 400 are default window sizes and if they are changed, the texts may be damaged. Instead
        # of changing the screen dimensions, you can change the pixel size
        self.frame_size_x = x_length
        self.x = self.frame_size_x // pixel_size
        self.frame_size_y = y_length
        self.y = self.frame_size_y // pixel_size

        # score dictionary
        self.scores = scores
        # Colors (R, G, B)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.blue = pygame.Color(0, 0, 255)
        self.snake_colors = [self.white, self.red, self.green, self.blue]
        # Game variables
        self.snake_count = Snake_Count
        self.pixel_size = pixel_size
        self.food_map, self.color_map = self.food_map_init(self.frame_size_x // self.pixel_size,
                                                           self.frame_size_y // self.pixel_size)
        # Snakes Variables
        self.dead_snakes = 0
        self.snakes = []
        first_second = 0
        for x in range(self.snake_count):
            pos, dir = self.player_home(x)
            if first_second == 0:
                self.snakes.append(
                    snake(pos, dir,
                          stamina, life, step, turning_penalty, x))
                first_second += 1
            elif first_second == 1:
                self.snakes.append(snake(pos, dir, stamina, life, step, turning_penalty, x))
                first_second += 1
            else:
                self.snakes.append(snake(pos, dir, stamina, life, step, turning_penalty, x))

        # Checks for errors encountered
        check_errors = pygame.init()
        # pygame.init() example output -> (6, 0)
        # second number in tuple gives number of errors
        if check_errors[1] > 0:
            print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
            sys.exit(-1)
        else:
            print('[+] Game successfully initialised')
        # Initialise game window
        pygame.display.set_caption('Nibbles')
        self.game_window = pygame.display.set_mode((self.frame_size_x, self.frame_size_y + (20 * self.snake_count)))

    def food_map_init(self, x, y):
        map = np.zeros((x, y))
        color_map = np.zeros((x, y))
        for score in self.scores.keys():
            min = self.scores[score][3]
            max = self.scores[score][4]
            food_class = np.random.normal(loc=score, scale=self.scores[score][1],
                                          size=int(((x * y) * self.scores[score][0]) / 2))
            flag = -1
            for food in food_class:
                new_x = 0
                new_y = 0
                flag += 1
                if flag % 2 == 0:
                    new_x = random.randint(math.ceil(x / 2), x - 1)
                    new_y = random.randint(0, math.floor(y / 2) - 1)
                    while map[new_x, new_y] != 0:
                        new_x = random.randint(math.ceil(x / 2), x - 1)
                        new_y = random.randint(0, math.floor(y / 2) - 1)
                elif flag % 2 == 1:
                    new_x = random.randint(0, math.floor(x / 2) - 1)
                    new_y = random.randint(math.ceil(y / 2), y - 1)
                    while map[new_x, new_y] != 0:
                        new_x = random.randint(0, math.floor(x / 2) - 1)
                        new_y = random.randint(math.ceil(y / 2), y - 1)

                abstract_food = int(food)
                if abstract_food < min:
                    abstract_food = min
                elif abstract_food > max:
                    abstract_food = max
                map[new_x, new_y] = abstract_food
                color_map[new_x, new_y] = score
                if flag % 2 == 0:
                    map[(x-1) - new_x, new_y] = abstract_food
                    color_map[(x-1) - new_x, new_y] = score
                elif flag % 2 == 1:
                    map[(x-1) - new_x, new_y] = abstract_food
                    color_map[(x-1) - new_x, new_y] = score
        return map, color_map

    # Game Over
    def game_finish(self):
        my_font = pygame.font.SysFont('times new roman', 90)
        game_finish_surface = my_font.render('Finish', True, self.red)
        game_finish_rect = game_finish_surface.get_rect()
        game_finish_rect.center = (self.frame_size_x / 2, (self.frame_size_y + (20 * self.snake_count)) / 2)
        self.game_window.fill(self.black)
        self.game_window.blit(game_finish_surface, game_finish_rect)
        self.show_score_stamina_life(0, 'times', 20)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()

    # Score
    def show_score_stamina_life(self, choice, font, size):
        func_font = pygame.font.SysFont(font, size, bold=True)
        for i in range(self.snake_count):
            color = self.snake_colors[i]
            score_surface = func_font.render('Score' + str(i) + ': ' + str(self.snakes[i].score), True, color)
            stamina_surface = func_font.render('Stamina' + str(i) + ': ' + str(self.snakes[i].stamina), True, color)
            life_surface = func_font.render('Life' + str(i) + ': ' + str(self.snakes[i].life), True, color)
            score_rect = score_surface.get_rect()
            stamina_rect = stamina_surface.get_rect()
            life_rect = life_surface.get_rect()
            if choice == 1:
                score_rect.bottomleft = (0, self.frame_size_y + ((i + 1) * 20))
                stamina_rect.midbottom = (self.frame_size_x / 2, self.frame_size_y + ((i + 1) * 20))
                life_rect.bottomright = (self.frame_size_x, self.frame_size_y + ((i + 1) * 20))
                self.game_window.blit(score_surface, score_rect)
                self.game_window.blit(stamina_surface, stamina_rect)
                self.game_window.blit(life_surface, life_rect)
            else:
                x_cor = i // 3
                y_cor = i % 3
                if y_cor == 0:
                    print(x_cor)
                    score_rect.bottomleft = (0, ((x_cor + 1) * 20))
                elif y_cor == 1:
                    print(x_cor)
                    score_rect.midbottom = (self.frame_size_x / 2, ((x_cor + 1) * 20))
                elif y_cor == 2:
                    score_rect.bottomright = (self.frame_size_x, ((x_cor + 1) * 20))
                self.game_window.blit(score_surface, score_rect)
            # pygame.display.flip()

    def player_home(self, id):
        if id == 0:
            return [(math.floor(self.x / 2) - 2) * self.pixel_size, ((self.y - 1) * self.pixel_size)], "UP"
        elif id == 1:
            return [(math.floor(self.x / 2) + 2) * self.pixel_size, (self.y - 1) * self.pixel_size], "UP"
        else:
            return [0, self.pixel_size * (3 * id)], "RIGHT"
    def step(self, actions):
        # Main logic
        counter = -1
        for action in actions:
            counter += 1
            color = self.snake_colors[counter]
            player = self.snakes[counter]
            if player.finish:
                continue
            # Whenever a key is pressed down
            if action == 'UP':
                player.change_to = 'UP'
            elif action == 'DOWN':
                player.change_to = 'DOWN'
            elif action == 'LEFT':
                player.change_to = 'LEFT'
            elif action == 'RIGHT':
                player.change_to = 'RIGHT'
            elif action == 'SPACE':
                if not player.flag:
                    player.flag = True
                elif player.flag:
                    player.flag = False

            # Making sure the snake cannot move in the opposite direction instantaneously
            if player.change_to == 'UP' and player.direction != 'DOWN':
                if player.direction != 'UP':
                    player.score -= player.turning_penalty
                player.direction = 'UP'
            if player.change_to == 'DOWN' and player.direction != 'UP':
                if player.direction != 'DOWN':
                    player.score -= player.turning_penalty
                player.direction = 'DOWN'
            if player.change_to == 'LEFT' and player.direction != 'RIGHT':
                if player.direction != 'LEFT':
                    player.score -= player.turning_penalty
                player.direction = 'LEFT'
            if player.change_to == 'RIGHT' and player.direction != 'LEFT':
                if player.direction != 'RIGHT':
                    player.score -= player.turning_penalty
                player.direction = 'RIGHT'

            # Moving the snake
            player.old_snake_pos = [player.snake_pos[0], player.snake_pos[1]]
            if player.direction == 'UP':
                player.snake_pos[1] -= self.pixel_size
            if player.direction == 'DOWN':
                player.snake_pos[1] += self.pixel_size
            if player.direction == 'LEFT':
                player.snake_pos[0] -= self.pixel_size
            if player.direction == 'RIGHT':
                player.snake_pos[0] += self.pixel_size

            # Snake body growing mechanism
            player.snake_body.insert(0, list(player.snake_pos))
            # Snake eating
            if player.grow_period == 0 and len(player.snake_body) == 2 and player.flag:
                self.food_score = self.food_map[
                    player.old_snake_pos[0] // self.pixel_size, player.old_snake_pos[
                        1] // self.pixel_size]
                # Renew ability
                # self.food_map[self.old_snake_pos[0] // self.pixel_size, self.old_snake_pos[1] // self.pixel_size] = 0
                player.grow_period += 2 * self.food_score

                player.score += self.food_score * 15 + 5

            if player.grow_period > 0:
                if not player.is_growing:
                    player.is_growing = True
                player.grow_period -= 1
            else:
                if player.is_growing:
                    player.is_growing = False
                player.snake_body.pop()
                if len(player.snake_body) > 1:
                    player.snake_body.pop()
                else:
                    # Snake stamina and life mechanism
                    player.stamina -= 1
                    if player.stamina == -1:
                        if player.life > 0:
                            player.life -= 1
                            pos, dir = self.player_home(player.id)
                            player.snake_pos = pos
                            player.snake_body = [pos]
                            player.direction = dir
                            player.change_to = dir
                        player.stamina = player.old_stamina - player.step - 1
                        player.old_stamina -= player.step
                        if player.life == 0:
                            player.stamina = 0
                            player.finish = True
                            self.dead_snakes += 1
                            if self.dead_snakes == self.snake_count:
                                self.game_finish()

            # GFX
            self.game_window.fill(self.black)

            # Snake food
            i = 0
            while i < self.frame_size_x // self.pixel_size:
                j = 0
                while j < self.frame_size_y // self.pixel_size:
                    if self.color_map[i, j] == 0:
                        pygame.draw.rect(self.game_window, self.black,
                                         pygame.Rect(i * self.pixel_size, j * self.pixel_size, self.pixel_size,
                                                     self.pixel_size))
                    else:
                        image = self.scores[self.color_map[i, j]][2]
                        DEFAULT_IMAGE_SIZE = (self.pixel_size, self.pixel_size)
                        image = pygame.transform.scale(image, DEFAULT_IMAGE_SIZE)
                        self.game_window.blit(image, (i * self.pixel_size, j * self.pixel_size))

                    j += 1
                i += 1

            # Game Over conditions
            # Getting out of bounds
            if player.snake_pos[0] < 0 or player.snake_pos[
                0] > self.frame_size_x - self.pixel_size:
                player.finish = True
                self.dead_snakes += 1
                if self.dead_snakes == self.snake_count:
                    self.game_finish()
            if player.snake_pos[1] < 0 or player.snake_pos[
                1] > self.frame_size_y - self.pixel_size:
                player.finish = True
                self.dead_snakes += 1
                if self.dead_snakes == self.snake_count:
                    self.game_finish()
            # Touching the snake body
            for block in player.snake_body[1:]:
                if player.snake_pos[0] == block[0] and player.snake_pos[1] == block[1]:
                    player.finish = True
                    self.dead_snakes += 1
                    if self.dead_snakes == self.snake_count:
                        self.game_finish()
            # Touching other snakes body
            for sn in range(self.snake_count):
                if not self.snakes[sn].is_growing and not sn == counter and not self.snakes[sn].finish:
                    for block in self.snakes[sn].snake_body:
                        if player.snake_pos[0] == block[0] and player.snake_pos[1] == block[1]:
                            player.finish = True
                            self.dead_snakes += 1
                            if self.dead_snakes == self.snake_count:
                                self.game_finish()

            # GFX
            for sn in range(self.snake_count):
                color = self.snake_colors[sn]
                if self.snakes[sn].finish:
                    continue
                for pos in self.snakes[sn].snake_body:
                    # Snake body
                    # .draw.rect(play_surface, color, xy-coordinate)
                    # xy-coordinate -> .Rect(x, y, size_x, size_y)
                    if self.snakes[sn].is_growing:
                        pygame.draw.rect(self.game_window, color,
                                         pygame.Rect(pos[0], pos[1], self.pixel_size, self.pixel_size), 2)
                    else:
                        pygame.draw.rect(self.game_window, color,
                                         pygame.Rect(pos[0], pos[1], self.pixel_size, self.pixel_size))

            self.show_score_stamina_life(1, 'consolas', 20)


# Key is mean of food
# in the tuples we have (plenty, variance, image, min range of food score, max range of food score)
# scores = {2.5: (0.3, 0.5, pygame.image.load("onion.png"), 1, 4),
#          6.5: (0.2, 0.75, pygame.image.load("cake.png"), 4, 9),
#          10: (0.05, 0.25, pygame.image.load("sandwich.png"), 9, 12)}
scores = {2.5: (0.15, 0.5, pygame.image.load("onion.png"), 1, 4),
          6.5: (0.1, 0.75, pygame.image.load("cake.png"), 4, 9),
          10: (0.025, 0.25, pygame.image.load("sandwich.png"), 9, 12)}
# scores = {4: (0.5,pygame.Color(0, 0, 0)),
#         16: (0.25, pygame.Color(75, 0, 0)),
#         32: (0.125, pygame.Color(150, 0, 0)),
#         64: (0.001, pygame.Color(250, 0, 0))}

env = Simulator(4, 3, 1, 20, scores, 2)

# FPS (frames per second) controller
fps_controller = pygame.time.Clock()
# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 5

while True:
    Actions = ["", ""]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Whenever a key is pressed down
        if event.type == pygame.KEYDOWN:
            # W -> Up; S -> Down; A -> Left; D -> Right
            if event.key == pygame.K_UP:
                Actions[1] = "UP"
            elif event.key == pygame.K_DOWN:
                Actions[1] = "DOWN"
            elif event.key == pygame.K_LEFT:
                Actions[1] = "LEFT"
            elif event.key == pygame.K_RIGHT:
                Actions[1] = "RIGHT"
            elif event.key == pygame.K_SPACE:
                Actions[1] = "SPACE"

    act = env.snakes[0].AI(copy.deepcopy(env.food_map), copy.deepcopy(env.snakes))
    Actions[0] = act
    print(Actions)
    env.step(Actions)
    # Refresh game screen
    pygame.display.update()
    # Refresh rate
    fps_controller.tick(difficulty)
