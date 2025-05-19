# LeetCode Problem Generator

A Python-based tool that automatically generates and tracks LeetCode practice problems. This tool helps you maintain a consistent coding practice routine by providing daily LeetCode problems and tracking your progress.

## Features

- Automatically fetches problems from LeetCode's GraphQL API
- Generates daily practice problems
- Tracks solved and unsolved problems
- Creates Jupyter notebooks with problem descriptions and solution templates
- Maintains a history of problems and solutions
- Runs automatically at system startup and daily at 8 AM
- Preserves your work by only adding new problems when existing ones are completed
- Tracks problem completion through test case execution

## Prerequisites

- Python 3.x
- Jupyter Notebook
- Linux-based system (for automated scheduling)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd leet-code-problem-generator
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Setup

1. Run the setup script to configure automated problem generation:
   ```bash
   ./setup_daily_problems.sh
   ```
   This will:
   - Create a systemd service for startup execution
   - Set up a daily cron job (runs at 8 AM)
   - Create necessary log files
   - Make required scripts executable

## Usage

### Manual Problem Generation

To manually generate new problems:
```bash
python generate_leetcode_problems.py
```

The tool will:
- Check if you have any uncompleted problems
- Only generate new problems if all existing problems are completed
- Append new problems to your existing notebook
- Preserve all your previous work and solutions

### Viewing Problems

Problems are stored in `leetcode_practice.ipynb`. Open this file with Jupyter Notebook:
```bash
jupyter notebook leetcode_practice.ipynb
```

### Completing Problems

1. Open the notebook in Jupyter
2. For each problem:
   - Read the problem description
   - Implement your solution in the solution cell
   - Run the test cases cell to verify your solution
   - The problem is considered complete when all test cases pass

### Checking Status

- View cron jobs: `crontab -l`
- Check service status: `systemctl status leetcode-problems.service`
- View logs: `tail -f leetcode_problems.log`

## Project Structure

- `generate_leetcode_problems.py`: Main script for generating problems
- `problem_tracker.py`: Manages problem tracking and history
- `problem_tracker.json`: Stores problem history and solutions
- `setup_daily_problems.sh`: Setup script for automated execution
- `check_and_generate.sh`: Helper script for automated execution
- `leetcode_practice.ipynb`: Jupyter notebook containing problems
- `leetcode_problems.log`: Log file for automated execution

## How It Works

1. The system fetches problems from LeetCode's GraphQL API
2. Problems are filtered to avoid duplicates
3. Selected problems are added to a Jupyter notebook
4. Problem history is tracked in `problem_tracker.json`
5. Solutions can be marked as solved by running the test cases
6. New problems are only added when all existing problems are completed
7. Your work is preserved between sessions

## Contributing

Feel free to submit issues and enhancement requests! 