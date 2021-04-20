import random

class Solution:
    # Class Initialization
    def __init__(self, list_size):
        if list_size <= 0:
            print('Size must be greater than 0.')
            return
        self.fitness = 0
        self.size = list_size
        self.list = [0]*list_size
    # Mutate Function
    def mutate(self, type=0, prob=0.5):
        if type == 0:
            for z in range(0, self.size):
                if random.random() < prob:
                    self.list[z] = random.randrange(0, 18)
        elif type == 1:
            for z in range(0, self.size):
                if random.random() < prob:
                    idx = self.list[random.randrange(0, self.size)]
                    temp = self.list[idx]
                    self.list[idx] = self.list[z]
                    self.list[z] = temp
