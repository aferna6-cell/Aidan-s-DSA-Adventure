#!/usr/bin/env python3
"""
Data Structures & Algorithms Study Game
A terminal-based interactive learning tool for practicing DSA concepts.
Features adaptive difficulty and spaced repetition.
"""

import json
import os
import random
from datetime import datetime, timedelta
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
            "questions": {},  # question_id -> {total_attempts, correct_attempts, last_seen}
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

            # Ensure all question records have last_seen field
            for qid in self.progress["questions"]:
                if "last_seen" not in self.progress["questions"][qid]:
                    self.progress["questions"][qid]["last_seen"] = None

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
                "correct_attempts": 0,
                "last_seen": None
            }

        self.progress["questions"][question_id]["total_attempts"] += 1
        if correct:
            self.progress["questions"][question_id]["correct_attempts"] += 1

        # Update last_seen timestamp
        self.progress["questions"][question_id]["last_seen"] = datetime.now().isoformat()

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

    # ==================== Adaptive Difficulty & Spaced Repetition ====================

    def get_topic_level(self, topic: str) -> int:
        """
        Get the player's level for a topic based on XP.
        Level 1: < 50 XP
        Level 2: 50-149 XP
        Level 3: 150+ XP
        """
        xp = self.get_topic_xp(topic)
        if xp < 50:
            return 1
        elif xp < 150:
            return 2
        else:
            return 3

    def get_preferred_difficulties(self, topic: str) -> List[int]:
        """
        Get the preferred difficulty levels for a topic based on player level.
        Returns a list of difficulty values to prioritize.
        """
        level = self.get_topic_level(topic)
        if level == 1:
            return [1, 2]  # Mainly difficulty 1, some 2
        elif level == 2:
            return [1, 2, 3]  # Mix of all, bias toward 1 and 2
        else:
            return [2, 3, 1]  # Mainly 2 and 3, some 1 for review

    def calculate_question_weight(self, question: Question, topic_filter: Optional[str] = None) -> float:
        """
        Calculate selection weight for a question using spaced repetition algorithm.
        Higher weight = more likely to be selected.

        Factors:
        - Success rate (lower is higher weight)
        - Time since last seen (longer is higher weight)
        - Difficulty match with player level
        """
        qid = question.id
        stats = self.progress["questions"].get(qid, {
            "total_attempts": 0,
            "correct_attempts": 0,
            "last_seen": None
        })

        weight = 1.0

        # Factor 1: Success rate (prefer questions with mistakes)
        total = stats.get("total_attempts", 0)
        correct = stats.get("correct_attempts", 0)

        if total == 0:
            # Never seen - high priority
            weight *= 3.0
        else:
            success_rate = correct / total
            # Lower success rate = higher weight
            # 0% success = 3x weight, 50% = 1.5x, 100% = 1x
            weight *= (2.0 - success_rate) + 1.0

        # Factor 2: Time since last seen (spaced repetition)
        last_seen = stats.get("last_seen")
        if last_seen is None:
            # Never seen - very high priority
            weight *= 2.0
        else:
            try:
                last_seen_dt = datetime.fromisoformat(last_seen)
                time_diff = datetime.now() - last_seen_dt
                hours_ago = time_diff.total_seconds() / 3600

                # More weight for questions not seen recently
                # < 1 hour: 0.5x, 1-24 hours: 1x, 1-7 days: 2x, > 7 days: 3x
                if hours_ago < 1:
                    weight *= 0.5
                elif hours_ago < 24:
                    weight *= 1.0
                elif hours_ago < 168:  # 7 days
                    weight *= 2.0
                else:
                    weight *= 3.0
            except (ValueError, TypeError):
                # Invalid timestamp, treat as never seen
                weight *= 2.0

        # Factor 3: Difficulty match with player level
        if topic_filter:
            preferred_difficulties = self.get_preferred_difficulties(topic_filter)
            if question.difficulty in preferred_difficulties[:2]:
                # Question difficulty matches player level well
                weight *= 1.5
            elif question.difficulty not in preferred_difficulties:
                # Question difficulty doesn't match well
                weight *= 0.3

        return weight

    def select_adaptive_questions(self, questions: List[Question], num_questions: int,
                                 topic: Optional[str] = None) -> List[Question]:
        """
        Select questions using weighted random selection based on spaced repetition.

        Args:
            questions: Pool of questions to select from
            num_questions: Number of questions to select
            topic: Optional topic filter for difficulty matching

        Returns:
            List of selected questions
        """
        if not questions:
            return []

        # Calculate weights for all questions
        weights = [self.calculate_question_weight(q, topic) for q in questions]

        # Handle case where we want more questions than available
        num_to_select = min(num_questions, len(questions))

        # Weighted random selection without replacement
        selected = []
        remaining_questions = list(questions)
        remaining_weights = list(weights)

        for _ in range(num_to_select):
            if not remaining_questions:
                break

            # Normalize weights to probabilities
            total_weight = sum(remaining_weights)
            if total_weight == 0:
                # Fallback to uniform random
                idx = random.randint(0, len(remaining_questions) - 1)
            else:
                probabilities = [w / total_weight for w in remaining_weights]
                idx = random.choices(range(len(remaining_questions)), weights=probabilities)[0]

            selected.append(remaining_questions[idx])
            remaining_questions.pop(idx)
            remaining_weights.pop(idx)

        return selected

    def is_question_new(self, question_id: str) -> bool:
        """Check if a question has never been attempted."""
        stats = self.progress["questions"].get(question_id)
        return stats is None or stats.get("total_attempts", 0) == 0

    def is_question_review(self, question_id: str) -> bool:
        """Check if a question was previously answered incorrectly."""
        stats = self.progress["questions"].get(question_id)
        if stats is None:
            return False
        total = stats.get("total_attempts", 0)
        correct = stats.get("correct_attempts", 0)
        return total > 0 and correct < total

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
        # Show question status (new or review)
        status_indicator = ""
        if self.is_question_new(question.id):
            status_indicator = " [NEW]"
        elif self.is_question_review(question.id):
            status_indicator = " [REVIEW]"

        # Print question header
        self.print_header(
            f"Topic: {question.topic.replace('_', ' ').title()} | "
            f"Difficulty: {'⭐' * question.difficulty}{status_indicator}"
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
        """Let user study questions from a specific topic with adaptive difficulty."""
        self.clear_screen()
        self.print_header("Study by Topic")

        topics = self.get_topics()

        print("\nAvailable topics:\n")
        for i, topic in enumerate(topics, 1):
            xp = self.get_topic_xp(topic)
            level = self.get_topic_level(topic)
            level_name = ["", "Beginner", "Intermediate", "Advanced"][level]
            print(f"  {i}. {topic.replace('_', ' ').title()}")
            print(f"      Level {level} ({level_name}) | XP: {xp}")

        print(f"\n  {len(topics) + 1}. Back to main menu")

        while True:
            try:
                choice = input("\nSelect a topic: ").strip()
                choice_num = int(choice)

                if choice_num == len(topics) + 1:
                    return

                if 1 <= choice_num <= len(topics):
                    selected_topic = topics[choice_num - 1]
                    all_questions = self.get_questions_by_topic(selected_topic)

                    if not all_questions:
                        print("\n⚠️  No questions available for this topic!")
                        input("Press Enter to continue...")
                        return

                    # Use adaptive selection
                    num_questions = min(len(all_questions), 5)
                    questions = self.select_adaptive_questions(
                        all_questions, num_questions, topic=selected_topic
                    )

                    for i, question in enumerate(questions, 1):
                        self.clear_screen()
                        print(f"\n[Question {i}/{len(questions)}]\n")
                        self.ask_question(question)

                    self.clear_screen()
                    print("\n✅ Topic complete! Great job!\n")

                    # Show level progress
                    new_xp = self.get_topic_xp(selected_topic)
                    new_level = self.get_topic_level(selected_topic)
                    print(f"   {selected_topic.replace('_', ' ').title()} - Level {new_level} | XP: {new_xp}\n")

                    input("Press Enter to return to menu...")
                    return
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def adventure_mode(self):
        """Present questions from all topics using adaptive selection."""
        self.clear_screen()
        self.print_header("Adventure Mode")

        if not self.questions:
            print("\n⚠️  No questions available!")
            input("Press Enter to continue...")
            return

        print("\n🎮 Get ready for a mixed challenge across all topics!")
        print("   Questions are selected based on your progress and learning needs.\n")

        num_questions = min(5, len(self.questions))
        print(f"   You'll face {num_questions} adaptive questions.\n")

        input("Press Enter to start...")

        # Use adaptive selection across all questions
        questions = self.select_adaptive_questions(self.questions, num_questions)

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

        # Use adaptive selection for review (prioritize recent mistakes)
        num_to_review = min(len(mistake_questions), 5)
        questions = self.select_adaptive_questions(mistake_questions, num_to_review)

        for question in questions:
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

        # Show total XP and overall stats
        total_xp = sum(topic_data.get("xp", 0) for topic_data in self.progress["topics"].values())
        print(f"\n   Total XP: {total_xp}")

        # Show topic levels
        topics = self.get_topics()
        if topics:
            print("\n   Topic Progress:")
            for topic in topics:
                level = self.get_topic_level(topic)
                xp = self.get_topic_xp(topic)
                level_names = ["", "Beginner", "Intermediate", "Advanced"]
                bar_length = 20

                # Calculate XP progress within current level
                if level == 1:
                    progress = min(xp / 50, 1.0)
                elif level == 2:
                    progress = min((xp - 50) / 100, 1.0)
                else:
                    progress = 1.0

                filled = int(bar_length * progress)
                bar = "█" * filled + "░" * (bar_length - filled)

                print(f"   {topic.replace('_', ' ').title()}: Lvl {level} {bar} {xp} XP")

        print("\n" + "─" * 60)
        print("\n1. Study by topic")
        print("2. Adventure mode (adaptive)")
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
