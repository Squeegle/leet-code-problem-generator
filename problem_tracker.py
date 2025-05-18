import json
import os
from datetime import datetime
from typing import Dict, List, Set

class ProblemTracker:
    def __init__(self, tracker_file: str = "problem_tracker.json"):
        self.tracker_file = tracker_file
        self.tracked_problems = self._load_tracker()

    def _load_tracker(self) -> Dict:
        """Load the problem tracker from file."""
        if os.path.exists(self.tracker_file):
            with open(self.tracker_file, 'r') as f:
                return json.load(f)
        return {
            "problems": {},
            "last_generated": None
        }

    def _save_tracker(self):
        """Save the problem tracker to file."""
        with open(self.tracker_file, 'w') as f:
            json.dump(self.tracked_problems, f, indent=2)

    def add_problems(self, problems: List[Dict]):
        """Add new problems to the tracker."""
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # If we already generated problems today, don't add new ones
        if self.tracked_problems["last_generated"] == current_date:
            return

        for problem in problems:
            problem_id = problem['questionId']
            if problem_id not in self.tracked_problems["problems"]:
                self.tracked_problems["problems"][problem_id] = {
                    "title": problem['title'],
                    "difficulty": problem['difficulty'],
                    "category": problem['categoryTitle'],
                    "content": problem['content'],
                    "example_testcases": problem['exampleTestcases'],
                    "added_date": current_date,
                    "solved": False,
                    "solution": None
                }

        self.tracked_problems["last_generated"] = current_date
        self._save_tracker()

    def mark_as_solved(self, problem_id: str, solution: str):
        """Mark a problem as solved and store the solution."""
        if problem_id in self.tracked_problems["problems"]:
            self.tracked_problems["problems"][problem_id]["solved"] = True
            self.tracked_problems["problems"][problem_id]["solution"] = solution
            self._save_tracker()

    def get_unsolved_problems(self) -> List[Dict]:
        """Get all unsolved problems."""
        return [
            problem for problem in self.tracked_problems["problems"].values()
            if not problem["solved"]
        ]

    def get_solved_problems(self) -> List[Dict]:
        """Get all solved problems."""
        return [
            problem for problem in self.tracked_problems["problems"].values()
            if problem["solved"]
        ]

    def should_generate_new_problems(self) -> bool:
        """Check if we should generate new problems today."""
        current_date = datetime.now().strftime("%Y-%m-%d")
        return self.tracked_problems["last_generated"] != current_date 