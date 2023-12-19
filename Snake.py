import copy
import random


class snake:
    def __init__(self, init_pos, init_dir, init_stamina, init_life, init_step, turning_penalty, id):
        self.id = id
        self.snake_pos = copy.deepcopy(init_pos)
        self.snake_body = [copy.deepcopy(init_pos)]
        self.grow_period = 0
        self.direction = copy.deepcopy(init_dir)
        self.change_to = self.direction
        self.score = 0
        self.stamina = init_stamina
        self.old_stamina = init_stamina
        self.old_snake_pos = copy.deepcopy(init_pos)
        self.life = init_life
        self.step = init_step
        self.turning_penalty = turning_penalty
        self.flag = True
        self.finish = False
        self.is_growing = False
        self.actions = ["", "UP", "DOWN", "LEFT", "RIGHT"]

    def AI(self, food_map, snakes):
        act = random.choice(self.actions)
        return act
