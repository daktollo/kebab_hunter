import numpy as np
import random
import pygame

class KebabHunterEnvironment:
    def __init__(self, grid_size=5, cell_size=100, image_dir="images"):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.window_size = grid_size * cell_size
        self.num_bombs = random.randint(1, 3)  # Random number of bombs (1 to 3)
        self.last_moves = [None, None]  # Track the last two moves
        self.image_dir = image_dir
        self.reset()

        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption("Kebab Hunter")

        # Load images
        self.robot_image = pygame.image.load(f"{self.image_dir}/robot.png")
        self.robot_image = pygame.transform.scale(self.robot_image, (cell_size, cell_size))
        self.kebab_image = pygame.image.load(f"{self.image_dir}/kebab.png")
        self.kebab_image = pygame.transform.scale(self.kebab_image, (cell_size, cell_size))
        self.bomb_image = pygame.image.load(f"{self.image_dir}/bomb.png")
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
        self.last_moves = [None, None]  # Reset last moves
        return self.get_state()

    def get_state(self):
        """Returns the current state as a tuple of kebab direction, danger positions, and last two moves."""
        # Direction of the kebab relative to the robot
        kebab_direction = [
            int(self.kebab_position[0] < self.robot_position[0]),  # Kebab is above
            int(self.kebab_position[0] > self.robot_position[0]),  # Kebab is below
            int(self.kebab_position[1] > self.robot_position[1]),  # Kebab is to the right
            int(self.kebab_position[1] < self.robot_position[1])   # Kebab is to the left
        ]

        # Danger positions (bombs) relative to the robot
        danger_positions = [0, 0, 0, 0]  # [Above, Below, Right, Left]
        for bomb_position in self.bomb_positions:
            if bomb_position[0] == self.robot_position[0] - 1 and bomb_position[1] == self.robot_position[1]:
                danger_positions[0] = 1  # Danger above
            if bomb_position[0] == self.robot_position[0] + 1 and bomb_position[1] == self.robot_position[1]:
                danger_positions[1] = 1  # Danger below
            if bomb_position[1] == self.robot_position[1] + 1 and bomb_position[0] == self.robot_position[0]:
                danger_positions[2] = 1  # Danger to the right
            if bomb_position[1] == self.robot_position[1] - 1 and bomb_position[0] == self.robot_position[0]:
                danger_positions[3] = 1  # Danger to the left

        # Combine state components
        state = tuple(kebab_direction + danger_positions + self.last_moves)
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

        # Update last moves
        self.last_moves.pop(0)
        self.last_moves.append(action)

        # Calculate reward
        if self.robot_position == self.kebab_position:
            reward = 20  # Increased reward for collecting a kebab
            self.done = True
        elif self.robot_position in self.bomb_positions:
            reward = -10  # Increased penalty for hitting a bomb
            self.done = True
        else:
            reward = -0.1  # Small penalty for each step to encourage faster completion

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
