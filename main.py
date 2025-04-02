import pygame
from environment import KebabHunterEnvironment

def main():
    # Initialize the environment
    env = KebabHunterEnvironment(grid_size=5, cell_size=100)
    clock = pygame.time.Clock()
    running = True

    # Reset the environment
    state = env.reset()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get user input for actions
        keys = pygame.key.get_pressed()
        action = None
        if keys[pygame.K_UP]:
            action = 0  # Up
        elif keys[pygame.K_DOWN]:
            action = 1  # Down
        elif keys[pygame.K_LEFT]:
            action = 2  # Left
        elif keys[pygame.K_RIGHT]:
            action = 3  # Right

        # Perform action if valid
        if action is not None:
            state, reward, done = env.step(action)
            print(f"State: {state}, Reward: {reward}, Done: {done}")
            if done:
                print("Episode finished! Resetting environment...")
                state = env.reset()

        # Render the environment
        env.render()

        # Cap the frame rate
        clock.tick(10)

    # Close the environment
    env.close()

if __name__ == "__main__":
    main()
