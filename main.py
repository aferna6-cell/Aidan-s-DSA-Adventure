#!/usr/bin/env python3
"""
DSA Study Game - Level-Based Learning Tool
A terminal-based game with adaptive difficulty, level gating, and partial credit.
"""

import json
import os
import random
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# ==================== Configuration ====================

# Level unlock thresholds
REQUIRED_CORRECT_FOR_LEVEL_2 = 10
REQUIRED_CORRECT_FOR_LEVEL_3 = 10

# Scoring
FULL_CREDIT_XP = 10
PARTIAL_CREDIT_XP = 5
NO_CREDIT_XP = 0

# Partial credit strategy: Only full-credit answers count toward level unlocks
# (Two partial-credit answers do NOT equal one full correct)
PARTIAL_COUNTS_FOR_UNLOCK = False


# ==================== Question Class ====================

class Question:
    """Represents a DSA question."""

    def __init__(self, data: Dict):
        self.id = data["id"]
        self.topic = data["topic"]
        self.subtopic = data.get("subtopic", "")
        self.difficulty = data["difficulty"]  # 1, 2, or 3
        self.type = data["type"]  # "mcq" or "short_answer"
        self.prompt = data["prompt"]

        # MCQ fields
        self.choices = data.get("choices", [])
        self.correctChoiceIndex = data.get("correctChoiceIndex", None)

        # Short answer fields
        self.expectedAnswer = data.get("expectedAnswer", "")
        self.expectedAnswerKeywords = data.get("expectedAnswerKeywords", [])

        self.explanation = data["explanation"]
        self.hints = data.get("hints", [])


# ==================== Game Class ====================

class Game:
    """Main game class with level gating and partial credit."""

    def __init__(self):
        """Initialize game."""
        self.questions: List[Question] = []
        self.progress: Dict = {
            "topics": {},  # topic -> {level, correct_at_level}
            "questions": {}  # question_id -> {total_attempts, correct_attempts, last_seen}
        }
        self.load_questions()
        self.load_progress()

    # ==================== Loading/Saving ====================

    def load_questions(self, filename: str = "questions.json"):
        """Load questions from JSON file."""
        if not os.path.exists(filename):
            print(f"ERROR: {filename} not found!")
            print("Please ensure questions.json exists.")
            sys.exit(1)

        try:
            with open(filename, "r") as f:
                questions_data = json.load(f)

            self.questions = []
            for q_data in questions_data:
                try:
                    # Validate required fields
                    required = ["id", "topic", "difficulty", "type", "prompt", "explanation"]
                    if not all(field in q_data for field in required):
                        continue

                    if "hints" not in q_data:
                        q_data["hints"] = []

                    self.questions.append(Question(q_data))
                except Exception as e:
                    print(f"Warning: Skipping invalid question: {e}")
                    continue

            print(f"✓ Loaded {len(self.questions)} questions")

            # Verify we have questions for all topics
            topics = self.get_topics()
            if not topics:
                print("ERROR: No valid questions found!")
                sys.exit(1)

        except Exception as e:
            print(f"ERROR loading questions: {e}")
            sys.exit(1)

    def load_progress(self):
        """Load progress from progress.json."""
        if not os.path.exists("progress.json"):
            self.initialize_progress()
            return

        try:
            with open("progress.json", "r") as f:
                self.progress = json.load(f)

            # Ensure all topics are initialized
            for topic in self.get_topics():
                if topic not in self.progress["topics"]:
                    self.progress["topics"][topic] = {
                        "level": 1,
                        "correct_at_level": {"1": 0, "2": 0, "3": 0}
                    }
                else:
                    # Ensure correct_at_level exists
                    if "correct_at_level" not in self.progress["topics"][topic]:
                        self.progress["topics"][topic]["correct_at_level"] = {"1": 0, "2": 0, "3": 0}

            if "questions" not in self.progress:
                self.progress["questions"] = {}

        except Exception as e:
            print(f"Warning: Error loading progress, starting fresh: {e}")
            self.initialize_progress()

    def initialize_progress(self):
        """Initialize progress for all topics."""
        self.progress = {"topics": {}, "questions": {}}
        for topic in self.get_topics():
            self.progress["topics"][topic] = {
                "level": 1,
                "correct_at_level": {"1": 0, "2": 0, "3": 0}
            }
        self.save_progress()

    def save_progress(self):
        """Save progress to progress.json."""
        try:
            with open("progress.json", "w") as f:
                json.dump(self.progress, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save progress: {e}")

    # ==================== Helper Methods ====================

    def get_topics(self) -> List[str]:
        """Get sorted list of unique topics."""
        return sorted(set(q.topic for q in self.questions))

    def get_questions_by_topic_and_difficulty(self, topic: str, difficulty: int) -> List[Question]:
        """Get questions for specific topic and difficulty."""
        return [q for q in self.questions if q.topic == topic and q.difficulty == difficulty]

    def get_topic_level(self, topic: str) -> int:
        """Get current level for a topic (1-3)."""
        return self.progress["topics"].get(topic, {}).get("level", 1)

    def get_correct_count(self, topic: str, level: int) -> int:
        """Get number of correct answers at a specific level for a topic."""
        level_str = str(level)
        return self.progress["topics"].get(topic, {}).get("correct_at_level", {}).get(level_str, 0)

    def check_and_unlock_level(self, topic: str):
        """Check if conditions are met to unlock next level for a topic."""
        current_level = self.get_topic_level(topic)

        if current_level == 1:
            correct_at_1 = self.get_correct_count(topic, 1)
            if correct_at_1 >= REQUIRED_CORRECT_FOR_LEVEL_2:
                self.progress["topics"][topic]["level"] = 2
                self.save_progress()
                self.clear_screen()
                print("\n" + "="*60)
                print(f"🎉 LEVEL UP! 🎉")
                print(f"\n{topic.replace('_', ' ').title()} - LEVEL 2 UNLOCKED!")
                print(f"\nYou can now access medium difficulty questions.")
                print("="*60 + "\n")
                input("Press Enter to continue...")
                return True

        elif current_level == 2:
            correct_at_2 = self.get_correct_count(topic, 2)
            if correct_at_2 >= REQUIRED_CORRECT_FOR_LEVEL_3:
                self.progress["topics"][topic]["level"] = 3
                self.save_progress()
                self.clear_screen()
                print("\n" + "="*60)
                print(f"🏆 MASTERY ACHIEVED! 🏆")
                print(f"\n{topic.replace('_', ' ').title()} - LEVEL 3 UNLOCKED!")
                print(f"\nYou can now access hard difficulty questions.")
                print("="*60 + "\n")
                input("Press Enter to continue...")
                return True

        return False

    # ==================== Question Asking ====================

    def normalize_answer(self, answer: str) -> str:
        """Normalize answer for comparison."""
        return answer.strip().lower()

    def check_answer_correctness(self, question: Question, user_answer: str) -> Tuple[str, int]:
        """
        Check answer correctness.
        Returns: (status, xp) where status is "full", "partial", or "incorrect"
        """
        if question.type == "mcq":
            # For MCQ, only full credit or no credit
            user_answer = user_answer.strip().upper()

            # Convert letter to index or use number directly
            if len(user_answer) == 1 and user_answer.isalpha():
                user_idx = ord(user_answer) - ord('A')
            elif user_answer.isdigit():
                user_idx = int(user_answer)
            else:
                return ("incorrect", NO_CREDIT_XP)

            if user_idx == question.correctChoiceIndex:
                return ("full", FULL_CREDIT_XP)
            else:
                return ("incorrect", NO_CREDIT_XP)

        else:  # short_answer or similar
            user_normalized = self.normalize_answer(user_answer)
            expected_normalized = self.normalize_answer(question.expectedAnswer)

            # Check for exact match
            if user_normalized == expected_normalized:
                return ("full", FULL_CREDIT_XP)

            # Check keyword matching
            if question.expectedAnswerKeywords:
                keywords_found = sum(
                    1 for keyword in question.expectedAnswerKeywords
                    if keyword.lower() in user_normalized
                )
                total_keywords = len(question.expectedAnswerKeywords)

                # Full credit: all keywords present
                if keywords_found == total_keywords:
                    return ("full", FULL_CREDIT_XP)

                # Partial credit: at least half keywords present
                if keywords_found >= (total_keywords + 1) // 2:  # ceiling division
                    return ("partial", PARTIAL_CREDIT_XP)

            return ("incorrect", NO_CREDIT_XP)

    def ask_question(self, question: Question):
        """Ask a question and handle response."""
        self.clear_screen()
        self.print_header(
            f"Topic: {question.topic.replace('_', ' ').title()} | "
            f"Difficulty: {'⭐' * question.difficulty} (Level {question.difficulty})"
        )

        if question.subtopic:
            print(f"Subtopic: {question.subtopic}")
        print(f"\n{question.prompt}\n")

        # Display choices for MCQ
        if question.type == "mcq":
            for i, choice in enumerate(question.choices):
                letter = chr(ord('A') + i)
                print(f"  {letter}) {choice}")
            print()

        # Handle hints
        hints_used = []

        while True:
            user_input = input("Your answer (or type 'hint' for a hint): ").strip()

            if user_input.lower() == "hint":
                if len(hints_used) < len(question.hints):
                    hint_idx = len(hints_used)
                    print(f"\n💡 Hint {hint_idx + 1}: {question.hints[hint_idx]}\n")
                    hints_used.append(hint_idx)
                else:
                    if len(question.hints) == 0:
                        print("\n⚠️  No hints available for this question!\n")
                    else:
                        print("\n⚠️  No more hints available!\n")
                continue

            if user_input:
                break

            print("Please enter an answer.\n")

        # Check correctness
        status, xp = self.check_answer_correctness(question, user_input)

        # Display feedback
        if status == "full":
            print("\n" + "="*60)
            print("✅ CORRECT! Full credit.")
            print(f"   +{xp} XP")
            print("="*60)
        elif status == "partial":
            print("\n" + "="*60)
            print("⚡ PARTIALLY CORRECT!")
            print("   You have the right idea, but check the details.")
            print(f"   +{xp} XP")
            print("="*60)
        else:
            print("\n" + "="*60)
            print("❌ INCORRECT")
            print(f"   +{xp} XP")
            print("="*60)

        # Show explanation
        print(f"\n📚 Explanation: {question.explanation}\n")

        # Update progress
        self.update_progress(question, status)

        input("Press Enter to continue...")

    def update_progress(self, question: Question, status: str):
        """Update progress after answering a question."""
        q_id = question.id
        topic = question.topic
        level = question.difficulty

        # Update question stats
        if q_id not in self.progress["questions"]:
            self.progress["questions"][q_id] = {
                "total_attempts": 0,
                "correct_attempts": 0,
                "partial_attempts": 0,
                "last_seen": None
            }

        self.progress["questions"][q_id]["total_attempts"] += 1
        self.progress["questions"][q_id]["last_seen"] = datetime.now().isoformat()

        if status == "full":
            self.progress["questions"][q_id]["correct_attempts"] += 1
        elif status == "partial":
            self.progress["questions"][q_id]["partial_attempts"] = \
                self.progress["questions"][q_id].get("partial_attempts", 0) + 1

        # Update topic progress
        if status == "full":
            # Only full credit counts toward level unlock
            level_str = str(level)
            self.progress["topics"][topic]["correct_at_level"][level_str] += 1
            self.save_progress()

            # Check for level unlock
            self.check_and_unlock_level(topic)
        else:
            self.save_progress()

    # ==================== Game Modes ====================

    def study_by_topic(self):
        """Study questions by topic with level selection."""
        self.clear_screen()
        self.print_header("Study by Topic")

        topics = self.get_topics()

        print("\nAvailable topics:\n")
        for i, topic in enumerate(topics, 1):
            level = self.get_topic_level(topic)
            print(f"  {i}. {topic.replace('_', ' ').title()}")
            print(f"      Current Level: {level} / 3")

            # Show progress bars for each level
            for lvl in range(1, 4):
                correct = self.get_correct_count(topic, lvl)
                if lvl == 1:
                    req = REQUIRED_CORRECT_FOR_LEVEL_2
                elif lvl == 2:
                    req = REQUIRED_CORRECT_FOR_LEVEL_3
                else:
                    req = 0  # Level 3 is max

                if lvl <= level:
                    if lvl < 3:
                        progress = min(correct / req, 1.0) if req > 0 else 1.0
                        bar_len = 15
                        filled = int(bar_len * progress)
                        bar = "█" * filled + "░" * (bar_len - filled)
                        print(f"      Level {lvl}: {bar} {correct}/{req}")
                    else:
                        print(f"      Level {lvl}: {correct} correct (Mastery!)")
                else:
                    print(f"      Level {lvl}: 🔒 Locked")

        print(f"\n  {len(topics) + 1}. Back to main menu")

        # Get topic selection
        while True:
            try:
                choice = input("\nSelect a topic: ").strip()
                choice_num = int(choice)

                if choice_num == len(topics) + 1:
                    return

                if 1 <= choice_num <= len(topics):
                    selected_topic = topics[choice_num - 1]
                    self.select_level_and_study(selected_topic)
                    return
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            except KeyboardInterrupt:
                return

    def select_level_and_study(self, topic: str):
        """Select level and study questions."""
        self.clear_screen()
        self.print_header(f"Study: {topic.replace('_', ' ').title()}")

        current_level = self.get_topic_level(topic)

        print("\nSelect difficulty level:\n")
        for level in range(1, 4):
            if level <= current_level:
                level_name = ["", "Easy", "Medium", "Hard"][level]
                count = len(self.get_questions_by_topic_and_difficulty(topic, level))
                correct = self.get_correct_count(topic, level)
                print(f"  {level}. Level {level} ({level_name}) - {count} questions - {correct} correct")
            else:
                if level == 2:
                    needed = REQUIRED_CORRECT_FOR_LEVEL_2 - self.get_correct_count(topic, 1)
                    print(f"  {level}. 🔒 Level 2 (Medium) - Locked")
                    print(f"      (Answer {needed} more Level 1 questions correctly to unlock)")
                elif level == 3:
                    needed = REQUIRED_CORRECT_FOR_LEVEL_3 - self.get_correct_count(topic, 2)
                    print(f"  {level}. 🔒 Level 3 (Hard) - Locked")
                    print(f"      (Answer {needed} more Level 2 questions correctly to unlock)")

        print(f"\n  4. Back")

        # Get level selection
        while True:
            try:
                choice = input("\nSelect level: ").strip()
                choice_num = int(choice)

                if choice_num == 4:
                    return

                if 1 <= choice_num <= 3:
                    if choice_num <= current_level:
                        self.study_level(topic, choice_num)
                        return
                    else:
                        print(f"Level {choice_num} is locked. Complete previous levels first.")
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input.")
            except KeyboardInterrupt:
                return

    def study_level(self, topic: str, level: int):
        """Study questions from a specific topic and level."""
        questions = self.get_questions_by_topic_and_difficulty(topic, level)

        if not questions:
            self.clear_screen()
            print(f"\n⚠️  No questions available for {topic} Level {level}!")
            input("Press Enter to continue...")
            return

        # Randomize question order
        random.shuffle(questions)

        # Ask up to 5 questions
        num_to_ask = min(5, len(questions))

        for i, question in enumerate(questions[:num_to_ask], 1):
            self.ask_question(question)

        self.clear_screen()
        print("\n" + "="*60)
        print("✅ Study session complete!")
        print("="*60 + "\n")

        # Show updated progress
        correct = self.get_correct_count(topic, level)
        print(f"{topic.replace('_', ' ').title()} - Level {level}: {correct} correct answers\n")

        input("Press Enter to return to menu...")

    def view_progress(self):
        """Display progress summary."""
        self.clear_screen()
        self.print_header("Progress Summary")

        topics = self.get_topics()

        for topic in topics:
            level = self.get_topic_level(topic)
            print(f"\n{topic.replace('_', ' ').title()}:")
            print(f"  Current Level: {level} / 3")

            for lvl in range(1, 4):
                correct = self.get_correct_count(topic, lvl)

                if lvl <= level:
                    if lvl == 1:
                        needed = max(0, REQUIRED_CORRECT_FOR_LEVEL_2 - correct)
                        if needed > 0:
                            print(f"  Level {lvl}: {correct} correct ({needed} more needed for Level 2)")
                        else:
                            print(f"  Level {lvl}: {correct} correct (✓ Completed)")
                    elif lvl == 2:
                        needed = max(0, REQUIRED_CORRECT_FOR_LEVEL_3 - correct)
                        if needed > 0:
                            print(f"  Level {lvl}: {correct} correct ({needed} more needed for Level 3)")
                        else:
                            print(f"  Level {lvl}: {correct} correct (✓ Completed)")
                    else:
                        print(f"  Level {lvl}: {correct} correct (✓ Mastery!)")
                else:
                    print(f"  Level {lvl}: 🔒 Locked")

        print()
        input("Press Enter to return to menu...")

    def display_main_menu(self) -> str:
        """Display main menu and return choice."""
        self.clear_screen()
        self.print_header("📚 DSA Study Game - Level-Based Learning 📚")

        # Calculate total progress
        total_correct = 0
        for topic in self.get_topics():
            for lvl in range(1, 4):
                total_correct += self.get_correct_count(topic, lvl)

        print(f"\n   Total Correct Answers: {total_correct}")
        print(f"   Total Questions: {len(self.questions)}\n")

        print("─" * 60)
        print("\n1. Study by topic (with level selection)")
        print("2. View progress summary")
        print("3. Quit")
        print()

        choice = input("Select an option (1-3): ").strip()
        return choice

    def run(self):
        """Main game loop."""
        try:
            while True:
                choice = self.display_main_menu()

                if choice == "1":
                    self.study_by_topic()
                elif choice == "2":
                    self.view_progress()
                elif choice == "3":
                    self.clear_screen()
                    print("\n" + "="*60)
                    print("Thanks for studying!")
                    print("Keep mastering those DSA concepts! 🚀")
                    print("="*60 + "\n")
                    self.save_progress()
                    break
                else:
                    print("\n⚠️  Invalid choice. Please select 1-3.")
                    input("Press Enter to continue...")
        except KeyboardInterrupt:
            print("\n\nSaving progress and exiting...")
            self.save_progress()
            print("Goodbye!\n")

    # ==================== UI Helpers ====================

    @staticmethod
    def clear_screen():
        """Clear terminal screen."""
        os.system('clear' if os.name == 'posix' else 'cls')

    @staticmethod
    def print_separator(char="=", length=60):
        """Print separator line."""
        print(char * length)

    @staticmethod
    def print_header(text: str):
        """Print formatted header."""
        Game.print_separator()
        print(f"  {text}")
        Game.print_separator()


# ==================== Main Entry Point ====================

def main():
    """Entry point."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
