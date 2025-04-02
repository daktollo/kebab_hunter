import numpy as np
import random
import pygame

class KebabHunterEnvironment:
    def __init__(self, grid_size=5, cell_size=100):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.window_size = grid_size * cell_size
        self.num_bombs = random.randint(1, 3)  # Random number of bombs (1 to 3)
        self.reset()

        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption("Kebab Hunter")

        # Load images
        self.robot_image = pygame.image.load("images/robot.png")
        self.robot_image = pygame.transform.scale(self.robot_image, (cell_size, cell_size))
        self.kebab_image = pygame.image.load("images/kebab.png")
        self.kebab_image = pygame.transform.scale(self.kebab_image, (cell_size, cell_size))
        self.bomb_image = pygame.image.load("images/bomb.png")
        self.bomb_image = pygame.transform.scale(self.bomb_image, (cell_size, cell_size))

    def reset(self):
        """Resets the environment to the initial state."""
        self.robot_position = [random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)]
        self.kebab_position = [random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)]
        while self.kebab_position == self.robot_position:
            self.kebab_position = [random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)]
        self.bomb_positions = []
        for _ in range(self.num_bombs):
            bomb_position = [random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)]
            while bomb_position == self.robot_position or bomb_position == self.kebab_position or bomb_position in self.bomb_positions:
                bomb_position = [random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)]
            self.bomb_positions.append(bomb_position)
        self.done = False
        return self.get_state()

    def get_state(self):
        """Returns the current state as a tuple of robot, kebab, and bomb positions."""
        state = tuple(self.robot_position + self.kebab_position)
        for bomb_position in self.bomb_positions:
            state += tuple(bomb_position)
        return state

    def step(self, action):
        """
        Takes an action and updates the environment.
        Actions: 0 = up, 1 = down, 2 = left, 3 = right
        Returns: next_state, reward, done
        """
        if self.done:
            raise ValueError("Episode has ended. Please reset the environment.")

        # Move the robot
        if action == 0 and self.robot_position[0] > 0:  # Up
            self.robot_position[0] -= 1
        elif action == 1 and self.robot_position[0] < self.grid_size - 1:  # Down
            self.robot_position[0] += 1
        elif action == 2 and self.robot_position[1] > 0:  # Left
            self.robot_position[1] -= 1
        elif action == 3 and self.robot_position[1] < self.grid_size - 1:  # Right
            self.robot_position[1] += 1

        # Calculate reward
        if self.robot_position == self.kebab_position:
            reward = 10
            self.done = True
        elif self.robot_position in self.bomb_positions:
            reward = -1
            self.done = True
        else:
            reward = -1

        return self.get_state(), reward, self.done

    def render(self):
        """Renders the grid with the robot, kebab, and bomb positions using pygame."""
        self.screen.fill((255, 255, 255))  # White background

        # Draw grid
        for x in range(0, self.window_size, self.cell_size):
            pygame.draw.line(self.screen, (200, 200, 200), (x, 0), (x, self.window_size))
            pygame.draw.line(self.screen, (200, 200, 200), (0, x), (self.window_size, x))

        # Draw robot
        robot_x, robot_y = self.robot_position[1] * self.cell_size, self.robot_position[0] * self.cell_size
        self.screen.blit(self.robot_image, (robot_x, robot_y))

        # Draw kebab
        kebab_x, kebab_y = self.kebab_position[1] * self.cell_size, self.kebab_position[0] * self.cell_size
        self.screen.blit(self.kebab_image, (kebab_x, kebab_y))

        # Draw bombs
        for bomb_position in self.bomb_positions:
            bomb_x, bomb_y = bomb_position[1] * self.cell_size, bomb_position[0] * self.cell_size
            self.screen.blit(self.bomb_image, (bomb_x, bomb_y))

        # Update display
        pygame.display.flip()

    def close(self):
        """Closes the pygame window."""
        pygame.quit()
