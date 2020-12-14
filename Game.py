import random
import numpy as np


class Game:
    ACTION_UP = 0
    ACTION_LEFT = 1
    ACTION_DOWN = 2
    ACTION_RIGHT = 3
    
    ACTIONS = [ACTION_UP, ACTION_LEFT, ACTION_DOWN, ACTION_RIGHT]
    ACTIONS_NAMES = ['UP', 'LEFT', 'DOWN', 'RIGHT']
    WIND_DIRECTION = ['TOP', 'LEFT', 'BOTTOM', 'RIGHT']
    
    MOVEMENTS = {
        ACTION_UP: (1, 0),
        ACTION_RIGHT: (0, 1),
        ACTION_LEFT: (0, -1),
        ACTION_DOWN: (-1, 0)
    }
    
    num_actions = len(ACTIONS)
    
    def __init__(self, n, m, wrong_action_p=0.1, alea=False, wind=False):
        self.n = n
        self.m = m
        self.wrong_action_p = wrong_action_p
        self.alea = alea
        self.generate_game()

        self.side_wind = None
        if wind:
            self.side_wind = np.random.choice([0, 1, 2, 3])
            print(f'Wind from {self.WIND_DIRECTION[self.side_wind]}')
            self.wind_vector = self._generate_wind(self.side_wind)
            print(f'Vector: {self.wind_vector}')

    def _generate_wind(self, side):
        if side in [0, 2]:
            wind_vector = np.random.randint(3, size=self.m)
        else:
            wind_vector = np.random.randint(3, size=self.n)

        return wind_vector
        
    def _position_to_id(self, x, y):
        """Gives the position id (from 0 to n)"""
        return x + y * self.n
    
    def _id_to_position(self, id):
        """Réciproque de la fonction précédente"""
        return (id % self.n, id // self.n)
    
    def generate_game(self):
        cases = [(x, y) for x in range(self.n) for y in range(self.m)]
        hole = random.choice(cases)
        cases.remove(hole)
        start = random.choice(cases)
        cases.remove(start)
        end = random.choice(cases)
        cases.remove(end)
        block = random.choice(cases)
        cases.remove(block)
        
        self.position = start
        self.end = end
        self.hole = hole
        self.block = block
        self.counter = 0
        
        if not self.alea:
            self.start = start
        return self._get_state()
    
    def reset(self):
        if not self.alea:
            self.position = self.start
            self.counter = 0
            return self._get_state()
        else:
            return self.generate_game() 
    
    def _get_grille(self, x, y):
        grille = [
            [0] * self.n for i in range(self.m)
        ]
        grille[x][y] = 1
        return grille
    
    def _get_state(self):
        if self.alea:
            return [self._get_grille(x, y) for (x, y) in
                    [self.position, self.end, self.hole, self.block]]
        return self._position_to_id(*self.position)

    def move(self, action):
        """
        takes an action parameter
        :param action : the id of an action
        :return ((state_id, end, hole, block), reward, is_final, actions)
        """
        self.counter += 1
        if action not in self.ACTIONS:
            raise Exception('Invalid action')

        choice = random.random()
        if choice < self.wrong_action_p:
            action = (action + 1) % 4
        elif choice < 2 * self.wrong_action_p:
            action = (action - 1) % 4

        d_x, d_y = self.MOVEMENTS[action]
        x, y = self.position
        new_x, new_y = x + d_x, y + d_y

        if self.side_wind is not None:
            if self.side_wind == 0:
                v = (-1, 0)
            elif self.side_wind == 1:
                v = (0, 1)
            elif self.side_wind == 2:
                v = (1, 0)
            else:
                v = (0, -1)

            if np.random.choice([True, False], p=[0.2, 0.8]):
                new_x += v[0]
                new_y += v[1]
                #print(f'Ffffff')

        if self.block == (new_x, new_y):
            return self._get_state(), -1, False, self.ACTIONS
        elif self.hole == (new_x, new_y):
            self.position = new_x, new_y
            return self._get_state(), -10, True, None
        elif self.end == (new_x, new_y):
            self.position = new_x, new_y
            return self._get_state(), 10, True, self.ACTIONS
        elif new_x >= self.n or new_y >= self.m or new_x < 0 or new_y < 0:
            return self._get_state(), -1, False, self.ACTIONS
        elif self.counter > 190:
            self.position = new_x, new_y
            return self._get_state(), -10, True, self.ACTIONS
        else:
            self.position = new_x, new_y
            return self._get_state(), -1, False, self.ACTIONS

    def print(self):
        str = ""
        for i in range(self.n - 1, -1, -1):
            for j in range(self.m):
                if (i, j) == self.position:
                    str += "x"
                elif (i, j) == self.block:
                    str += "¤"
                elif (i, j) == self.hole:
                    str += "o"
                elif (i, j) == self.end:
                    str += "@"
                else:
                    str += "."
            str += "\n"
        print(str)
