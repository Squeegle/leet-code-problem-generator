import json
import requests
from typing import List, Dict, Set
import random
from problem_tracker import ProblemTracker

class LeetCodeProblem:
    def __init__(self, title: str, description: str, difficulty: str, 
                 solution_template: str, test_cases: List[Dict]):
        self.title = title
        self.description = description
        self.difficulty = difficulty
        self.solution_template = solution_template
        self.test_cases = test_cases

def fetch_leetcode_problems() -> List[Dict]:
    """Fetch problems from LeetCode's GraphQL API."""
    url = "https://leetcode.com/graphql"
    
    # GraphQL query to fetch problems
    query = """
    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
        problemsetQuestionList: questionList(
            categorySlug: $categorySlug
            limit: $limit
            skip: $skip
            filters: $filters
        ) {
            total: totalNum
            questions: data {
                questionId
                title
                titleSlug
                difficulty
                categoryTitle
                content
                exampleTestcases
            }
        }
    }
    """
    
    variables = {
        "categorySlug": "",
        "limit": 100,  # Fetch 100 problems at a time
        "skip": 0,
        "filters": {}
    }
    
    try:
        response = requests.post(url, json={
            "query": query,
            "variables": variables
        })
        response.raise_for_status()
        data = response.json()
        
        if "data" in data and "problemsetQuestionList" in data["data"]:
            return data["data"]["problemsetQuestionList"]["questions"]
        return []
    except Exception as e:
        print(f"Error fetching problems: {e}")
        return []

def get_unused_problems(problems_data: List[Dict], count: int) -> List[Dict]:
    """Get a list of problems that haven't been used before."""
    tracker = ProblemTracker()
    used_problem_ids = set(tracker.tracked_problems["problems"].keys())
    
    unused_problems = [p for p in problems_data if p['questionId'] not in used_problem_ids]
    
    if len(unused_problems) < count:
        print(f"Warning: Only {len(unused_problems)} unused problems available.")
        return []
    
    selected = random.sample(unused_problems, min(count, len(unused_problems)))
    return selected

def generate_problems() -> List[LeetCodeProblem]:
    tracker = ProblemTracker()
    
    # If we already have unsolved problems and it's the same day, don't generate new ones
    if not tracker.should_generate_new_problems():
        unsolved = tracker.get_unsolved_problems()
        if unsolved:
            print("Using existing unsolved problems.")
            return [
                LeetCodeProblem(
                    title=problem['title'],
                    description=f"""Problem ID: {problem_id}
Difficulty: {problem['difficulty']}
Category: {problem['category']}

{problem['content']}

Example:
{problem['example_testcases']}""",
                    difficulty=problem['difficulty'],
                    solution_template=f"""def {problem['title'].lower().replace(' ', '_')}(*args, **kwargs):
    # Your code here
    pass""",
                    test_cases=[{"input": {"args": [], "kwargs": {}}, "output": None}]
                )
                for problem_id, problem in tracker.tracked_problems["problems"].items()
                if not problem["solved"]
            ]
    
    problems_data = fetch_leetcode_problems()
    if not problems_data:
        print("Failed to fetch problems. Using fallback problems.")
        return get_fallback_problems()
    
    # Select 5 random unused problems
    selected_problems = get_unused_problems(problems_data, 5)
    
    if not selected_problems:
        print("No new problems available. Using existing unsolved problems.")
        return generate_problems()  # Recursively try to get existing problems
    
    # Add new problems to tracker
    tracker.add_problems(selected_problems)
    
    problems = []
    for problem in selected_problems:
        # Create solution template based on problem type
        solution_template = f"""def {problem['titleSlug'].replace('-', '_')}(*args, **kwargs):
    # Your code here
    pass"""
        
        # Create test cases (simplified version)
        test_cases = [
            {"input": {"args": [], "kwargs": {}}, "output": None}
        ]
        
        problems.append(LeetCodeProblem(
            title=problem['title'],
            description=f"""Problem ID: {problem['questionId']}
Difficulty: {problem['difficulty']}
Category: {problem['categoryTitle']}

{problem['content']}

Example:
{problem['exampleTestcases']}""",
            difficulty=problem['difficulty'],
            solution_template=solution_template,
            test_cases=test_cases
        ))
    
    return problems

def get_fallback_problems() -> List[LeetCodeProblem]:
    """Return fallback problems if fetching from LeetCode fails."""
    return [
        LeetCodeProblem(
            title="Two Sum",
            description="""Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
You may assume that each input would have exactly one solution, and you may not use the same element twice.
You can return the answer in any order.

Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:
Input: nums = [3,2,4], target = 6
Output: [1,2]

Example 3:
Input: nums = [3,3], target = 6
Output: [0,1]""",
            difficulty="Easy",
            solution_template="""def two_sum(nums: List[int], target: int) -> List[int]:
    # Your code here
    pass""",
            test_cases=[
                {"input": {"nums": [2,7,11,15], "target": 9}, "output": [0,1]},
                {"input": {"nums": [3,2,4], "target": 6}, "output": [1,2]},
                {"input": {"nums": [3,3], "target": 6}, "output": [0,1]}
            ]
        )
    ]

def create_notebook_content(problems: List[LeetCodeProblem]) -> dict:
    cells = []
    
    # Add title cell
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": ["# LeetCode Practice Problems\n\nThis notebook contains LeetCode problems fetched from the official LeetCode API."]
    })
    
    # Add each problem
    for i, problem in enumerate(problems, 1):
        # Problem description
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [f"## Problem {i}: {problem.title}\n\n**Difficulty**: {problem.difficulty}\n\n{problem.description}"]
        })
        
        # Solution template
        cells.append({
            "cell_type": "code",
            "metadata": {},
            "source": [problem.solution_template],
            "execution_count": None,
            "outputs": []
        })
        
        # Test cases
        test_cases_code = "def test_solution():\n"
        for j, test_case in enumerate(problem.test_cases, 1):
            test_cases_code += f"    # Test case {j}\n"
            test_cases_code += f"    result = {problem.solution_template.split('(')[0]}(**{test_case['input']})\n"
            test_cases_code += f"    assert result == {test_case['output']}, f'Test case {j} failed. Expected {test_case['output']}, got {{result}}'\n"
        test_cases_code += "    print('All test cases passed!')\n\n"
        test_cases_code += "test_solution()"
        
        cells.append({
            "cell_type": "code",
            "metadata": {},
            "source": [test_cases_code],
            "execution_count": None,
            "outputs": []
        })
    
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    return notebook

def main():
    problems = generate_problems()
    notebook = create_notebook_content(problems)
    
    with open('leetcode_practice.ipynb', 'w') as f:
        json.dump(notebook, f, indent=1)

if __name__ == "__main__":
    main() 