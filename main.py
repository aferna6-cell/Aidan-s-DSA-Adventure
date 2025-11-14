#!/usr/bin/env python3
"""
Data Structures & Algorithms Study Game
A terminal-based interactive learning tool for practicing DSA concepts.
"""

import json
import os
import random
from typing import Dict, List, Optional, Tuple


class Question:
    """Represents a single DSA question."""

    def __init__(self, data: Dict):
        self.id = data["id"]
        self.topic = data["topic"]
        self.difficulty = data["difficulty"]
        self.type = data["type"]  # "mcq", "short", "complexity_mcq", "trace", "order"
        self.prompt = data["prompt"]
        self.options = data.get("options", [])
        self.answer = data["answer"]  # Can be string or list (for order questions)
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


class Game:
    """Main game class that encapsulates all game logic."""

    def __init__(self):
        """Initialize the game with questions and progress tracking."""
        self.questions: List[Question] = []
        self.progress: Dict = {
            "questions": {},  # question_id -> {total_attempts, correct_attempts}
            "topics": {}      # topic -> {xp}
        }
        self.load_questions()
        self.load_progress()

    # ==================== Question Loading ====================

    def load_questions(self):
        """Load questions from questions.json, create default if doesn't exist."""
        if not os.path.exists("questions.json"):
            self.create_default_questions()

        with open("questions.json", "r") as f:
            questions_data = json.load(f)
            self.questions = [Question(q) for q in questions_data]

    def create_default_questions(self):
        """Create a default questions.json file with sample questions of all types."""
        default_questions = [
            # Basic MCQ
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
            # Complexity MCQ (new type)
            {
                "id": "complexity_2",
                "topic": "complexity",
                "difficulty": 2,
                "type": "complexity_mcq",
                "prompt": "What is the time complexity of binary search on a sorted array?",
                "options": ["A) O(1)", "B) O(log n)", "C) O(n)", "D) O(n log n)"],
                "answer": "B",
                "hints": [
                    "Think about how the search space is divided in each step.",
                    "Each comparison eliminates half of the remaining elements."
                ],
                "explanation": "Binary search has O(log n) time complexity because it halves the search space with each comparison."
            },
            # Stack/Queue MCQ
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
            # Trace question (new type)
            {
                "id": "stacks_queues_2",
                "topic": "stacks_queues",
                "difficulty": 2,
                "type": "trace",
                "prompt": "Trace the following stack operations:\n  stack = []\n  stack.push(5)\n  stack.push(3)\n  stack.push(7)\n  stack.pop()\n  stack.push(2)\n\nWhat does the stack contain now? (Format: [5, 3, 2])",
                "options": [],
                "answer": "[5, 3, 2]",
                "hints": [
                    "Remember LIFO - Last In First Out.",
                    "After pop(), the 7 is removed. Then 2 is pushed."
                ],
                "explanation": "Starting empty, we push 5, 3, 7 giving [5,3,7]. Pop removes 7, giving [5,3]. Push 2 gives [5,3,2]."
            },
            # Memory MCQ
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
            # Tree short answer
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
            },
            # Order question (new type)
            {
                "id": "complexity_3",
                "topic": "complexity",
                "difficulty": 2,
                "type": "order",
                "prompt": "Order these time complexities from FASTEST to SLOWEST:",
                "options": ["O(n²)", "O(1)", "O(n log n)", "O(n)", "O(log n)"],
                "answer": ["O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n²)"],
                "hints": [
                    "Constant time is fastest, polynomial is slowest.",
                    "Logarithmic beats linear, and linear beats linearithmic."
                ],
                "explanation": "From fastest to slowest: O(1) constant, O(log n) logarithmic, O(n) linear, O(n log n) linearithmic, O(n²) quadratic."
            },
            # Trace question for trees
            {
                "id": "trees_2",
                "topic": "trees",
                "difficulty": 3,
                "type": "trace",
                "prompt": "Given this BST insertion sequence into an empty tree:\n  insert(5), insert(3), insert(7), insert(1)\n\nWhat is the value of the left child of the root?",
                "options": [],
                "answer": "3",
                "hints": [
                    "The first value inserted becomes the root.",
                    "Values less than the root go to the left subtree."
                ],
                "explanation": "5 becomes the root. 3 is less than 5, so it becomes the left child of the root. 7 goes right, 1 goes to the left of 3."
            }
        ]

        with open("questions.json", "w") as f:
            json.dump(default_questions, f, indent=2)

        print("✓ Created default questions.json file with multiple question types")

    # ==================== Progress Tracking ====================

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

    # ==================== Question Handlers ====================

    def handle_hint_system(self, question: Question) -> Tuple[Optional[str], bool]:
        """
        Handle hint system for any question type.
        Returns: (user_answer, hint_was_used)
        """
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

            return user_input, hint_used_flag

    def ask_mcq_question(self, question: Question) -> bool:
        """
        Handle multiple choice questions (both regular and complexity-specific).
        Returns: True if correct, False otherwise
        """
        # Display options
        for option in question.options:
            print(f"  {option}")
        print()

        # Get answer with hint support
        user_answer, hint_used = self.handle_hint_system(question)

        # Check answer (compare letter only, case-insensitive)
        correct = user_answer.upper() == question.answer.upper()

        # Update progress
        self.update_progress(question.id, question.topic, correct, hint_used)

        return correct

    def ask_short_question(self, question: Question) -> bool:
        """
        Handle short answer questions.
        Returns: True if correct, False otherwise
        """
        # Get answer with hint support
        user_answer, hint_used = self.handle_hint_system(question)

        # Check if key terms are present (case-insensitive, fuzzy matching)
        user_lower = user_answer.lower()
        answer_lower = question.answer.lower()
        answer_words = answer_lower.split()
        matches = sum(1 for word in answer_words if word in user_lower)
        correct = matches >= len(answer_words) * 0.6  # 60% of keywords must match

        # Update progress
        self.update_progress(question.id, question.topic, correct, hint_used)

        return correct

    def ask_trace_question(self, question: Question) -> bool:
        """
        Handle trace questions (code execution trace).
        Returns: True if correct, False otherwise
        """
        # Get answer with hint support
        user_answer, hint_used = self.handle_hint_system(question)

        # Simple string comparison after normalizing whitespace
        user_normalized = user_answer.strip().replace(" ", "").lower()
        answer_normalized = str(question.answer).strip().replace(" ", "").lower()
        correct = user_normalized == answer_normalized

        # Update progress
        self.update_progress(question.id, question.topic, correct, hint_used)

        return correct

    def ask_order_question(self, question: Question) -> bool:
        """
        Handle ordering questions.
        Returns: True if correct, False otherwise
        """
        # Display items to order
        print("  Items to order:")
        for i, item in enumerate(question.options, 1):
            print(f"    {i}. {item}")
        print()
        print("  Enter your answer as:")
        print("    - Numbers (e.g., '2,5,1,4,3')")
        print("    - Or the actual items separated by commas")
        print()

        # Get answer with hint support
        user_answer, hint_used = self.handle_hint_system(question)

        # Parse user input
        user_items = [item.strip() for item in user_answer.split(",")]

        # Convert to canonical form (the actual strings)
        canonical_order = []
        for item in user_items:
            # Check if it's a number (1-indexed position)
            if item.isdigit():
                idx = int(item) - 1
                if 0 <= idx < len(question.options):
                    canonical_order.append(question.options[idx])
                else:
                    canonical_order.append(item)  # Invalid number, will fail comparison
            else:
                # It's a string, use as-is
                canonical_order.append(item)

        # Normalize both for comparison (strip whitespace, case-insensitive)
        canonical_normalized = [s.strip().lower() for s in canonical_order]
        answer_normalized = [s.strip().lower() for s in question.answer]

        correct = canonical_normalized == answer_normalized

        # Update progress
        self.update_progress(question.id, question.topic, correct, hint_used)

        return correct

    def ask_question(self, question: Question) -> None:
        """
        Route question to appropriate handler based on type.

        Args:
            question: The question to ask
        """
        # Print question header
        self.print_header(
            f"Topic: {question.topic.replace('_', ' ').title()} | "
            f"Difficulty: {'⭐' * question.difficulty}"
        )
        print(f"\n{question.prompt}\n")

        # Route to appropriate handler based on type
        if question.type in ["mcq", "complexity_mcq"]:
            self.ask_mcq_question(question)
        elif question.type == "short":
            self.ask_short_question(question)
        elif question.type == "trace":
            self.ask_trace_question(question)
        elif question.type == "order":
            self.ask_order_question(question)
        else:
            # Unknown question type - skip with warning
            print(f"⚠️  Warning: Unknown question type '{question.type}'. Skipping...")
            input("Press Enter to continue...")
            return

        # Show explanation
        print(f"\n📚 Explanation: {question.explanation}\n")
        input("Press Enter to continue...")

    # ==================== Game Modes ====================

    def study_by_topic(self):
        """Let user study questions from a specific topic."""
        self.clear_screen()
        self.print_header("Study by Topic")

        topics = self.get_topics()

        print("\nAvailable topics:\n")
        for i, topic in enumerate(topics, 1):
            xp = self.get_topic_xp(topic)
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
                    questions = self.get_questions_by_topic(selected_topic)

                    if not questions:
                        print("\n⚠️  No questions available for this topic!")
                        input("Press Enter to continue...")
                        return

                    # Shuffle and ask questions
                    random.shuffle(questions)

                    for question in questions:
                        self.clear_screen()
                        self.ask_question(question)

                    self.clear_screen()
                    print("\n✅ Topic complete! Great job!\n")
                    input("Press Enter to return to menu...")
                    return
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def adventure_mode(self):
        """Present questions from all topics in random order."""
        self.clear_screen()
        self.print_header("Adventure Mode")

        if not self.questions:
            print("\n⚠️  No questions available!")
            input("Press Enter to continue...")
            return

        print("\n🎮 Get ready for a mixed challenge across all topics!")
        num_questions = min(5, len(self.questions))  # Ask up to 5 questions
        print(f"   You'll face {num_questions} random questions.\n")

        input("Press Enter to start...")

        # Select random questions
        questions = random.sample(self.questions, num_questions)

        for i, question in enumerate(questions, 1):
            self.clear_screen()
            print(f"\n[Question {i}/{num_questions}]\n")
            self.ask_question(question)

        self.clear_screen()
        print("\n🏆 Adventure complete! You're getting stronger!\n")
        input("Press Enter to return to menu...")

    def review_mistakes(self):
        """Let user review questions they've answered incorrectly."""
        self.clear_screen()
        self.print_header("Review Mistakes")

        mistake_questions = self.get_mistake_questions()

        if not mistake_questions:
            print("\n🎉 Great news! You haven't made any mistakes yet,")
            print("   or you've already corrected all of them!\n")
            input("Press Enter to continue...")
            return

        print(f"\n📝 You have {len(mistake_questions)} question(s) to review.\n")
        input("Press Enter to start reviewing...")

        random.shuffle(mistake_questions)

        for question in mistake_questions:
            self.clear_screen()
            self.ask_question(question)

        self.clear_screen()
        print("\n✅ Review session complete! Keep up the great work!\n")
        input("Press Enter to return to menu...")

    # ==================== Main Menu ====================

    def display_main_menu(self) -> str:
        """Display the main menu and return user's choice."""
        self.clear_screen()
        self.print_header("📚 DSA Study Game 📚")

        # Show total XP
        total_xp = sum(topic_data.get("xp", 0) for topic_data in self.progress["topics"].values())
        print(f"\n   Total XP: {total_xp}\n")

        print("1. Study by topic")
        print("2. Adventure mode (random topics)")
        print("3. Review mistakes")
        print("4. Quit")
        print()

        choice = input("Select an option (1-4): ").strip()
        return choice

    def run(self):
        """Main game loop."""
        while True:
            choice = self.display_main_menu()

            if choice == "1":
                self.study_by_topic()
            elif choice == "2":
                self.adventure_mode()
            elif choice == "3":
                self.review_mistakes()
            elif choice == "4":
                self.clear_screen()
                print("\n👋 Thanks for studying! Keep learning and growing!\n")
                self.print_separator()
                break
            else:
                print("\n⚠️  Invalid choice. Please select 1-4.")
                input("Press Enter to continue...")

    # ==================== Helper Methods ====================

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

    @staticmethod
    def clear_screen():
        """Clear the terminal screen."""
        os.system('clear' if os.name == 'posix' else 'cls')

    @staticmethod
    def print_separator(char="=", length=60):
        """Print a visual separator."""
        print(char * length)

    @staticmethod
    def print_header(text: str):
        """Print a formatted header."""
        Game.print_separator()
        print(f"  {text}")
        Game.print_separator()


def main():
    """Entry point for the DSA Study Game."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
