import numpy as np
import random
import pickle

class QLearningAgent:
    def __init__(self, state_size, action_size, learning_rate=0.2, discount_factor=0.95, exploration_rate=1.0, exploration_decay=0.99, min_exploration_rate=0.01):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.min_exploration_rate = min_exploration_rate
        self.q_table = {}

    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0.0)

    def update_q_value(self, state, action, reward, next_state):
        max_next_q = max([self.get_q_value(next_state, a) for a in range(self.action_size)])
        current_q = self.get_q_value(state, action)
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[(state, action)] = new_q

    def choose_action(self, state):
        if random.uniform(0, 1) < self.exploration_rate:
            return random.randint(0, self.action_size - 1)
        q_values = [self.get_q_value(state, a) for a in range(self.action_size)]
        return np.argmax(q_values)

    def decay_exploration(self):
        self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)

    def save(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load(self, filepath):
        with open(filepath, 'rb') as f:
            self.q_table = pickle.load(f)
