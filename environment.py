from setting import *
import numpy as np
import random
import pygame

class KebabHunterEnvironment:
    def __init__(self, grid_size=3, cell_size=100, image_dir=IMAGE_DIR):  # Changed grid_size to 4
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.window_size = grid_size * cell_size
        self.num_bombs = 2  # Fixed number of bombs set to 3
        self.image_dir = image_dir
        self.rewards = {
            "step": -0.1,  # Reduced step penalty
            "wall_penalty": -0.5,  # Reduced wall penalty
            "kebab_reward": 1.0,  # Normalized kebab reward
            "bomb_penalty": -1.0,  # Normalized bomb penalty
            "direction_bonus": 0.25,  # Reduced direction bonus
            "wrong_direction_penalty": -0.2  # Reduced wrong direction penalty
        }
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

    def is_kebab_reachable(self):
        """Checks if the kebab is reachable from the robot's position."""
        visited = set()
        stack = [tuple(self.robot_position)]

        while stack:
            current = stack.pop()
            if current == tuple(self.kebab_position):
                return True  # Kebab is reachable
            if current in visited:
                continue
            visited.add(current)

            # Add valid neighbors to the stack
            for action in range(4):  # Actions: 0 = up, 1 = down, 2 = left, 3 = right
                neighbor = self.get_new_position(action)
                if self.is_valid_position(neighbor) and tuple(neighbor) not in visited:
                    stack.append(tuple(neighbor))

        return False  # No path to the kebab

    def reset(self):
        """Resets the environment to the initial state."""
        while True:
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

            # Ensure the robot has at least one valid move and the kebab is reachable
            if not self.is_deadlock() and self.is_kebab_reachable():
                break

        self.done = False
        return self.get_state()

    def get_state(self):
        """Returns the current state as a tuple of kebab direction and danger positions."""
        # Direction of the kebab relative to the robot
        kebab_direction = [
            int(self.kebab_position[0] < self.robot_position[0]),  # Kebab is above
            int(self.kebab_position[0] > self.robot_position[0]),  # Kebab is below
            int(self.kebab_position[1] > self.robot_position[1]),  # Kebab is to the right
            int(self.kebab_position[1] < self.robot_position[1])   # Kebab is to the left
        ]

        # Danger positions (bombs and walls) relative to the robot
        danger_positions = [0, 0, 0, 0]  # [Above, Below, Right, Left]

        # Check for walls
        if self.robot_position[0] == 0:  # Wall above
            danger_positions[0] = -1
        if self.robot_position[0] == self.grid_size - 1:  # Wall below
            danger_positions[1] = -1
        if self.robot_position[1] == self.grid_size - 1:  # Wall to the right
            danger_positions[2] = -1
        if self.robot_position[1] == 0:  # Wall to the left
            danger_positions[3] = -1

        # Check for bombs
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
        state = tuple(kebab_direction + danger_positions)
        return state

    def calculate_step_reward(self):
        """Returns the base reward for taking a step."""
        return self.rewards["step"]

    def calculate_wall_penalty(self):
        """Returns the penalty for hitting a wall."""
        return self.rewards["wall_penalty"]

    def calculate_kebab_reward(self):
        """Returns the reward for collecting a kebab."""
        return self.rewards["kebab_reward"]

    def calculate_bomb_penalty(self):
        """Returns the penalty for hitting a bomb."""
        return self.rewards["bomb_penalty"]

    def calculate_direction_bonus(self):
        """Returns the bonus for moving in the direction of the kebab."""
        return self.rewards["direction_bonus"]

    def calculate_wrong_direction_penalty(self):
        """Returns the penalty for moving in the wrong direction."""
        return self.rewards["wrong_direction_penalty"]

    def calculate_rewards(self, action, initial_distance):
        """Calculate and sum all rewards for the current step."""
        reward = self.calculate_step_reward()  # Base step penalty

        # Wall penalty
        if (action == 0 and self.robot_position[0] == 0) or \
           (action == 1 and self.robot_position[0] == self.grid_size - 1) or \
           (action == 2 and self.robot_position[1] == 0) or \
           (action == 3 and self.robot_position[1] == self.grid_size - 1):
            reward += self.calculate_wall_penalty()

        # Kebab reward
        if self.robot_position == self.kebab_position:
            reward += self.calculate_kebab_reward()

        # Bomb penalty
        if self.robot_position in self.bomb_positions:
            reward += self.calculate_bomb_penalty()

        # Direction bonus or wrong direction penalty
        kebab_direction = [
            int(self.kebab_position[0] < self.robot_position[0]),  # Kebab is above
            int(self.kebab_position[0] > self.robot_position[0]),  # Kebab is below
            int(self.kebab_position[1] > self.robot_position[1]),  # Kebab is to the right
            int(self.kebab_position[1] < self.robot_position[1])   # Kebab is to the left
        ]
        if (action == 0 and kebab_direction[0]) or \
           (action == 1 and kebab_direction[1]) or \
           (action == 2 and kebab_direction[3]) or \
           (action == 3 and kebab_direction[2]):
            reward += self.calculate_direction_bonus()
        else:
            reward += self.calculate_wrong_direction_penalty()

        return reward

    def is_deadlock(self):
        """Checks if the robot is in a deadlock situation."""
        for action in range(4):  # Actions: 0 = up, 1 = down, 2 = left, 3 = right
            new_position = self.get_new_position(action)
            if self.is_valid_position(new_position):
                return False  # At least one valid move exists
        return True  # No valid moves available

    def get_new_position(self, action):
        """Returns the new position based on the action."""
        new_position = self.robot_position[:]
        if action == 0:  # Up
            new_position[0] -= 1
        elif action == 1:  # Down
            new_position[0] += 1
        elif action == 2:  # Left
            new_position[1] -= 1
        elif action == 3:  # Right
            new_position[1] += 1
        return new_position

    def is_valid_position(self, position):
        """Checks if a position is valid (not a wall, bomb, or out of bounds)."""
        if position[0] < 0 or position[0] >= self.grid_size or \
           position[1] < 0 or position[1] >= self.grid_size:
            return False  # Out of bounds
        if position in self.bomb_positions:
            return False  # Bomb position
        return True

    def step(self, action):
        """
        Takes an action and updates the environment.
        Actions: 0 = up, 1 = down, 2 = left, 3 = right
        Returns: next_state, reward, done
        """
        if self.done:
            raise ValueError("Episode has ended. Please reset the environment.")

        # Calculate initial distance to the kebab
        initial_distance = abs(self.robot_position[0] - self.kebab_position[0]) + abs(self.robot_position[1] - self.kebab_position[1])

        # Move the robot
        if action == 0 and self.robot_position[0] > 0:  # Up
            self.robot_position[0] -= 1
        elif action == 1 and self.robot_position[0] < self.grid_size - 1:  # Down
            self.robot_position[0] += 1
        elif action == 2 and self.robot_position[1] > 0:  # Left
            self.robot_position[1] -= 1
        elif action == 3 and self.robot_position[1] < self.grid_size - 1:  # Right
            self.robot_position[1] += 1

        # Check for deadlock
        if self.is_deadlock():
            self.reset()  # Reconfigure the environment
            return self.get_state(), 0, False  # Return neutral reward and not done

        # Calculate rewards
        reward = self.calculate_rewards(action, initial_distance)

        # Check if the episode is done
        if self.robot_position == self.kebab_position or self.robot_position in self.bomb_positions:
            self.done = True

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
