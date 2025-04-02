# Kebab Hunter: A 5x5 Q-Learning Environment

## Overview

Kebab Hunter is a reinforcement learning environment where a robot navigates a 5x5 grid to collect kebabs and earn rewards. The goal is to train the robot using Q-learning to maximize its rewards by efficiently collecting kebabs while avoiding penalties.

## Features

- **Grid Size**: The environment is a 5x5 grid.
- **Robot**: The agent (robot) starts at a random position in the grid.
- **Kebabs**: Kebabs are placed randomly in the grid, and the robot earns rewards by collecting them.
- **Rewards**: Positive rewards are given for collecting kebabs, and penalties may be applied for invalid moves or other conditions.
- **Q-Learning**: The robot learns an optimal policy to navigate the grid and maximize its cumulative reward.

## Folder Structure

```
kebab_hunter/
├── README.md          # Project documentation
├── environment.py     # Code for the 5x5 grid environment
├── q_learning.py      # Implementation of the Q-learning algorithm
├── image/             # Folder containing images for visualization
│   ├── robot.png      # Image of the robot
│   ├── kebab.png      # Image of the kebab
│   └── grid.png       # Background grid image
└── results/           # Folder for storing training results and logs
```

## How It Works

1. **Environment**: The 5x5 grid is initialized with the robot and kebabs placed randomly.
2. **Actions**: The robot can move up, down, left, or right within the grid boundaries.
3. **Rewards**: 
   - Collecting a kebab: +10 points
   - Invalid move (e.g., moving out of bounds): -1 point
4. **Q-Learning**: The robot uses Q-learning to learn the best actions to take in each state to maximize its rewards.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Required libraries: `numpy`, `matplotlib`

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd kebab_hunter
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Environment

1. Train the robot using Q-learning:
   ```bash
   python q_learning.py
   ```

2. Visualize the robot's performance:
   ```bash
   python visualize.py
   ```

## Customization

- Modify the grid size or reward structure in `environment.py`.
- Add more complex obstacles or goals to the environment.

## Future Enhancements

- Add obstacles to the grid for more challenging navigation.
- Implement Deep Q-Learning for better performance.
- Create a GUI for interactive visualization.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- Inspired by classic reinforcement learning problems.
- Special thanks to the creators of Q-learning algorithms.
