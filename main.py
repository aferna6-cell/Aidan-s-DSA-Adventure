#!/usr/bin/env python3
"""
Data Structures & Algorithms Study Game
A terminal-based interactive learning tool for practicing DSA concepts.
"""

import json
import os
import random
from typing import Dict, List, Optional


class Question:
    """Represents a single DSA question."""

    def __init__(self, data: Dict):
        self.id = data["id"]
        self.topic = data["topic"]
        self.difficulty = data["difficulty"]
        self.type = data["type"]  # "mcq" or "short"
        self.prompt = data["prompt"]
        self.options = data.get("options", [])
        self.answer = data["answer"]
        self.hints = data.get("hints", [])
        self.explanation = data["explanation"]

    def to_dict(self) -> Dict:
        """Convert question back to dictionary format."""
        return {
            "id": self.id,
            "topic": self.topic,
            "difficulty": self.difficulty,
            "type": self.type,
            "prompt": self.prompt,
            "options": self.options,
            "answer": self.answer,
            "hints": self.hints,
            "explanation": self.explanation
        }


class GameState:
    """Manages game state, questions, and progress tracking."""

    def __init__(self):
        self.questions: List[Question] = []
        self.progress: Dict = {
            "questions": {},  # question_id -> {total_attempts, correct_attempts}
            "topics": {}      # topic -> {xp}
        }
        self.load_questions()
        self.load_progress()

    def load_questions(self):
        """Load questions from questions.json, create default if doesn't exist."""
        if not os.path.exists("questions.json"):
            self.create_default_questions()

        with open("questions.json", "r") as f:
            questions_data = json.load(f)
            self.questions = [Question(q) for q in questions_data]

    def create_default_questions(self):
        """Create a default questions.json file with sample questions."""
        default_questions = [
            {
                "id": "complexity_1",
                "topic": "complexity",
                "difficulty": 1,
                "type": "mcq",
                "prompt": "What is the time complexity of accessing an element in an array by index?",
                "options": ["A) O(1)", "B) O(n)", "C) O(log n)", "D) O(n²)"],
                "answer": "A",
                "hints": [
                    "Think about how direct array access works.",
                    "No loops or searching needed for index access."
                ],
                "explanation": "Accessing an array element by index is O(1) because it's a direct memory access using pointer arithmetic."
            },
            {
                "id": "stacks_queues_1",
                "topic": "stacks_queues",
                "difficulty": 2,
                "type": "mcq",
                "prompt": "Which data structure follows the LIFO (Last In First Out) principle?",
                "options": ["A) Queue", "B) Stack", "C) Linked List", "D) Hash Table"],
                "answer": "B",
                "hints": [
                    "Think about a stack of plates.",
                    "The last item added is the first one removed."
                ],
                "explanation": "A Stack follows LIFO - the last element pushed is the first one popped, like a stack of plates."
            },
            {
                "id": "memory_1",
                "topic": "memory",
                "difficulty": 2,
                "type": "mcq",
                "prompt": "Where are local variables typically stored in memory?",
                "options": ["A) Heap", "B) Stack", "C) Static/Global area", "D) Code segment"],
                "answer": "B",
                "hints": [
                    "Think about automatic memory management.",
                    "This memory is automatically freed when a function returns."
                ],
                "explanation": "Local variables are stored on the stack, which provides automatic memory management for function calls."
            },
            {
                "id": "trees_1",
                "topic": "trees",
                "difficulty": 3,
                "type": "short",
                "prompt": "In a binary search tree (BST), what property must be maintained for all nodes?",
                "options": [],
                "answer": "left children smaller right children larger",
                "hints": [
                    "Think about how BSTs organize data for efficient searching.",
                    "Consider the relationship between a node and its left/right children."
                ],
                "explanation": "In a BST, all nodes in the left subtree must be smaller than the node, and all nodes in the right subtree must be larger. This property enables O(log n) search in balanced trees."
            }
        ]

        with open("questions.json", "w") as f:
            json.dump(default_questions, f, indent=2)

        print("✓ Created default questions.json file")

    def load_progress(self):
        """Load progress from progress.json, create default if doesn't exist."""
        if not os.path.exists("progress.json"):
            self.save_progress()
            return

        with open("progress.json", "r") as f:
            self.progress = json.load(f)

            # Ensure all topics are initialized
            topics = set(q.topic for q in self.questions)
            if "topics" not in self.progress:
                self.progress["topics"] = {}
            for topic in topics:
                if topic not in self.progress["topics"]:
                    self.progress["topics"][topic] = {"xp": 0}

            if "questions" not in self.progress:
                self.progress["questions"] = {}

    def save_progress(self):
        """Save current progress to progress.json."""
        with open("progress.json", "w") as f:
            json.dump(self.progress, f, indent=2)

    def update_progress(self, question_id: str, topic: str, correct: bool, used_hint: bool):
        """Update progress after answering a question."""
        # Update question stats
        if question_id not in self.progress["questions"]:
            self.progress["questions"][question_id] = {
                "total_attempts": 0,
                "correct_attempts": 0
            }

        self.progress["questions"][question_id]["total_attempts"] += 1
        if correct:
            self.progress["questions"][question_id]["correct_attempts"] += 1

        # Update topic XP
        if topic not in self.progress["topics"]:
            self.progress["topics"][topic] = {"xp": 0}

        if correct:
            xp_gain = 5 if used_hint else 10
            self.progress["topics"][topic]["xp"] += xp_gain
            print(f"\n🎉 Correct! +{xp_gain} XP")
        else:
            print("\n❌ Incorrect!")

        self.save_progress()

    def get_questions_by_topic(self, topic: str) -> List[Question]:
        """Get all questions for a specific topic."""
        return [q for q in self.questions if q.topic == topic]

    def get_mistake_questions(self) -> List[Question]:
        """Get questions where user has made mistakes."""
        mistake_ids = []
        for qid, stats in self.progress["questions"].items():
            if stats["correct_attempts"] < stats["total_attempts"]:
                mistake_ids.append(qid)

        return [q for q in self.questions if q.id in mistake_ids]

    def get_topics(self) -> List[str]:
        """Get list of unique topics."""
        return sorted(set(q.topic for q in self.questions))

    def get_topic_xp(self, topic: str) -> int:
        """Get XP for a specific topic."""
        return self.progress["topics"].get(topic, {}).get("xp", 0)


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')


def print_separator(char="=", length=60):
    """Print a visual separator."""
    print(char * length)


def print_header(text: str):
    """Print a formatted header."""
    print_separator()
    print(f"  {text}")
    print_separator()


def ask_question(game: GameState, question: Question) -> None:
    """
    Present a question to the user and handle their response.

    Args:
        game: The game state
        question: The question to ask
    """
    print_header(f"Topic: {question.topic.replace('_', ' ').title()} | Difficulty: {'⭐' * question.difficulty}")
    print(f"\n{question.prompt}\n")

    if question.type == "mcq":
        for option in question.options:
            print(f"  {option}")
        print()

    hints_used = 0
    hint_used_flag = False

    while True:
        user_input = input("Your answer (or type 'hint' for a hint): ").strip()

        if user_input.lower() == "hint":
            if hints_used < len(question.hints):
                print(f"\n💡 Hint {hints_used + 1}: {question.hints[hints_used]}\n")
                hints_used += 1
                hint_used_flag = True
            else:
                print("\n⚠️  No more hints available!\n")
            continue

        # Check answer
        correct = False
        if question.type == "mcq":
            # For MCQ, compare the letter only (case-insensitive)
            correct = user_input.upper() == question.answer.upper()
        else:
            # For short answer, check if key terms are present (case-insensitive)
            user_lower = user_input.lower()
            answer_lower = question.answer.lower()
            # Simple check: see if answer keywords are in user input
            answer_words = answer_lower.split()
            matches = sum(1 for word in answer_words if word in user_lower)
            correct = matches >= len(answer_words) * 0.6  # 60% of keywords must match

        # Update progress
        game.update_progress(question.id, question.topic, correct, hint_used_flag)

        # Show explanation
        print(f"\n📚 Explanation: {question.explanation}\n")

        input("Press Enter to continue...")
        break


def study_by_topic(game: GameState):
    """Let user study questions from a specific topic."""
    clear_screen()
    print_header("Study by Topic")

    topics = game.get_topics()

    print("\nAvailable topics:\n")
    for i, topic in enumerate(topics, 1):
        xp = game.get_topic_xp(topic)
        print(f"  {i}. {topic.replace('_', ' ').title()} (XP: {xp})")

    print(f"  {len(topics) + 1}. Back to main menu")

    while True:
        try:
            choice = input("\nSelect a topic: ").strip()
            choice_num = int(choice)

            if choice_num == len(topics) + 1:
                return

            if 1 <= choice_num <= len(topics):
                selected_topic = topics[choice_num - 1]
                questions = game.get_questions_by_topic(selected_topic)

                if not questions:
                    print("\n⚠️  No questions available for this topic!")
                    input("Press Enter to continue...")
                    return

                # Shuffle and ask questions
                random.shuffle(questions)

                for question in questions:
                    clear_screen()
                    ask_question(game, question)

                clear_screen()
                print("\n✅ Topic complete! Great job!\n")
                input("Press Enter to return to menu...")
                return
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def adventure_mode(game: GameState):
    """Present questions from all topics in random order."""
    clear_screen()
    print_header("Adventure Mode")

    if not game.questions:
        print("\n⚠️  No questions available!")
        input("Press Enter to continue...")
        return

    print("\n🎮 Get ready for a mixed challenge across all topics!")
    num_questions = min(5, len(game.questions))  # Ask up to 5 questions
    print(f"   You'll face {num_questions} random questions.\n")

    input("Press Enter to start...")

    # Select random questions
    questions = random.sample(game.questions, num_questions)

    for i, question in enumerate(questions, 1):
        clear_screen()
        print(f"\n[Question {i}/{num_questions}]\n")
        ask_question(game, question)

    clear_screen()
    print("\n🏆 Adventure complete! You're getting stronger!\n")
    input("Press Enter to return to menu...")


def review_mistakes(game: GameState):
    """Let user review questions they've answered incorrectly."""
    clear_screen()
    print_header("Review Mistakes")

    mistake_questions = game.get_mistake_questions()

    if not mistake_questions:
        print("\n🎉 Great news! You haven't made any mistakes yet,")
        print("   or you've already corrected all of them!\n")
        input("Press Enter to continue...")
        return

    print(f"\n📝 You have {len(mistake_questions)} question(s) to review.\n")
    input("Press Enter to start reviewing...")

    random.shuffle(mistake_questions)

    for question in mistake_questions:
        clear_screen()
        ask_question(game, question)

    clear_screen()
    print("\n✅ Review session complete! Keep up the great work!\n")
    input("Press Enter to return to menu...")


def display_main_menu(game: GameState):
    """Display the main menu and return user's choice."""
    clear_screen()
    print_header("📚 DSA Study Game 📚")

    # Show total XP
    total_xp = sum(topic_data.get("xp", 0) for topic_data in game.progress["topics"].values())
    print(f"\n   Total XP: {total_xp}\n")

    print("1. Study by topic")
    print("2. Adventure mode (random topics)")
    print("3. Review mistakes")
    print("4. Quit")
    print()

    choice = input("Select an option (1-4): ").strip()
    return choice


def main():
    """Main game loop."""
    game = GameState()

    while True:
        choice = display_main_menu(game)

        if choice == "1":
            study_by_topic(game)
        elif choice == "2":
            adventure_mode(game)
        elif choice == "3":
            review_mistakes(game)
        elif choice == "4":
            clear_screen()
            print("\n👋 Thanks for studying! Keep learning and growing!\n")
            print_separator()
            break
        else:
            print("\n⚠️  Invalid choice. Please select 1-4.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
