from setting import *
from environment import KebabHunterEnvironment
from q_learning import QLearningAgent
from torch.utils.tensorboard import SummaryWriter
import os

def get_unique_run_dir(base_dir):
    """Generate a unique run directory name."""
    for i in range(1, 1000):  # Supports up to 999 runs
        run_dir = os.path.join(base_dir, f"run{i}")
        if not os.path.exists(run_dir):
            return run_dir
    raise RuntimeError("Too many runs, please clean up the base directory.")

def train_agent(episodes=50000, max_steps=100):
    os.makedirs(SAVE_DIR, exist_ok=True)
    unique_run_dir = get_unique_run_dir(SAVE_DIR)
    os.makedirs(unique_run_dir, exist_ok=True)

    log_dir = os.path.join(unique_run_dir, "logs")
    table_dir = os.path.join(unique_run_dir, "table")
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(table_dir, exist_ok=True)

    env = KebabHunterEnvironment(grid_size=5, image_dir=IMAGE_DIR)
    state_size = len(env.get_state())
    action_size = 4  # Up, Down, Left, Right
    agent = QLearningAgent(state_size, action_size)

    # Initialize TensorBoard writer
    writer = SummaryWriter(log_dir=log_dir)

    total_rewards = []

    for episode in range(episodes):
        state = env.reset()
        total_reward = 0

        for step in range(max_steps):
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)
            agent.update_q_value(state, action, reward, next_state)
            state = next_state
            total_reward += reward

            if done:
                break

        agent.decay_exploration()
        total_rewards.append(total_reward)

        # Log metrics to TensorBoard
        writer.add_scalar("Total Reward", total_reward, episode)
        writer.add_scalar("Exploration Rate", agent.exploration_rate, episode)

        # Log average reward every 100 episodes
        if (episode + 1) % 100 == 0:
            avg_reward = sum(total_rewards[-100:]) / 100
            writer.add_scalar("Average Reward (last 100)", avg_reward, episode)
            print(f"Episode {episode + 1}/{episodes}, Total Reward: {total_reward}, Average Reward: {avg_reward:.2f}, Exploration Rate: {agent.exploration_rate:.4f}")

    # Save the Q-table
    q_table_path = os.path.join(table_dir, "q_table.pkl")
    agent.save(q_table_path)
    print(f"Training completed. Q-table saved to '{q_table_path}'.")

    # Close TensorBoard writer
    writer.close()

if __name__ == "__main__":
    train_agent()
