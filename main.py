from setting import *
import pygame
from environment import KebabHunterEnvironment
from q_learning import QLearningAgent

def select_q_table_file():
    """Prompts the user to input the Q-table file path."""
    file_path = "saves/run7/table/q_table.pkl"
    return file_path

def main_menu():
    """Displays the main menu and allows the user to select the mode of play."""
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Kebab Hunter - Main Menu")
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    human_button = pygame.Rect(100, 100, 200, 50)
    ai_button = pygame.Rect(100, 200, 200, 50)

    while True:
        screen.fill((255, 255, 255))  # White background

        # Draw buttons
        pygame.draw.rect(screen, (0, 128, 0), human_button)
        pygame.draw.rect(screen, (0, 0, 128), ai_button)

        # Draw text
        human_text = font.render("Play as Human", True, (255, 255, 255))
        ai_text = font.render("Play with AI", True, (255, 255, 255))
        screen.blit(human_text, (human_button.x + 25, human_button.y + 10))
        screen.blit(ai_text, (ai_button.x + 40, ai_button.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if human_button.collidepoint(event.pos):
                    return "human"
                if ai_button.collidepoint(event.pos):
                    return "ai"

        clock.tick(30)

def main():
    mode = main_menu()
    game_speed = 1  # Oyun hızını kontrol eden değişken
    if mode == "human":
        # Initialize the environment
        env = KebabHunterEnvironment()
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
            clock.tick(game_speed)  # Oyun hızını kontrol eden satır

        # Close the environment
        env.close()
    elif mode == "ai":
        q_table_file = select_q_table_file()
        if not q_table_file:
            print("No Q-table file selected. Exiting AI mode.")
            return

        # Initialize the environment and agent
        env = KebabHunterEnvironment()
        state_size = len(env.get_state())
        action_size = 4  # Up, Down, Left, Right
        agent = QLearningAgent(state_size, action_size)
        agent.load(q_table_file)

        clock = pygame.time.Clock()
        running = True

        # Reset the environment
        state = env.reset()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # AI chooses an action
            action = agent.choose_action(state)
            state, reward, done = env.step(action)
            print(f"State: {state}, Reward: {reward}, Done: {done}")
            if done:
                print("Episode finished! Resetting environment...")
                state = env.reset()

            # Render the environment
            env.render()

            # Cap the frame rate
            clock.tick(game_speed)  # Oyun hızını kontrol eden satır

        # Close the environment
        env.close()

if __name__ == "__main__":
    main()
