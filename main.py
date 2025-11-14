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
    """Represents a single DSA question using the new schema."""

    def __init__(self, data: Dict):
        self.id = data["id"]
        self.topic = data["topic"]
        self.subtopic = data.get("subtopic", "")
        self.difficulty = data["difficulty"]
        self.type = data["type"]  # "mcq" or "short_answer"
        self.prompt = data["prompt"]

        # MCQ-specific fields
        self.choices = data.get("choices", [])
        self.correctChoiceIndex = data.get("correctChoiceIndex", None)

        # Short answer-specific fields
        self.expectedAnswer = data.get("expectedAnswer", "")
        self.expectedAnswerKeywords = data.get("expectedAnswerKeywords", [])

        self.explanation = data["explanation"]
        self.hints = data.get("hints", [])

    def to_dict(self) -> Dict:
        """Convert question back to dictionary format."""
        result = {
            "id": self.id,
            "topic": self.topic,
            "subtopic": self.subtopic,
            "difficulty": self.difficulty,
            "type": self.type,
            "prompt": self.prompt,
            "explanation": self.explanation,
            "hints": self.hints
        }

        if self.type == "mcq":
            result["choices"] = self.choices
            result["correctChoiceIndex"] = self.correctChoiceIndex
        elif self.type == "short_answer":
            result["expectedAnswer"] = self.expectedAnswer
            result["expectedAnswerKeywords"] = self.expectedAnswerKeywords

        return result


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

    def load_questions(self, filename: str = "questions.json"):
        """
        Load questions from JSON file.

        Args:
            filename: Path to the questions JSON file
        """
        if not os.path.exists(filename):
            print(f"⚠️  Warning: {filename} not found!")
            print("Please ensure questions.json exists in the same directory as main.py")
            self.questions = []
            return

        try:
            with open(filename, "r") as f:
                questions_data = json.load(f)

            # Validate and load questions
            self.questions = []
            for i, q_data in enumerate(questions_data):
                try:
                    # Validate required fields
                    required = ["id", "topic", "difficulty", "type", "prompt", "explanation"]
                    missing = [field for field in required if field not in q_data]
                    if missing:
                        print(f"⚠️  Question {i}: Missing fields {missing}, skipping...")
                        continue

                    # Set hints to empty list if missing
                    if "hints" not in q_data:
                        q_data["hints"] = []

                    # Validate type-specific fields
                    if q_data["type"] == "mcq":
                        if "choices" not in q_data or "correctChoiceIndex" not in q_data:
                            print(f"⚠️  MCQ question {q_data['id']}: Missing choices or correctChoiceIndex, skipping...")
                            continue
                    elif q_data["type"] == "short_answer":
                        if "expectedAnswerKeywords" not in q_data:
                            q_data["expectedAnswerKeywords"] = []
                        if "expectedAnswer" not in q_data:
                            q_data["expectedAnswer"] = ""

                    self.questions.append(Question(q_data))

                except Exception as e:
                    print(f"⚠️  Error loading question {i}: {e}")
                    continue

            print(f"✓ Loaded {len(self.questions)} questions from {filename}")

        except json.JSONDecodeError as e:
            print(f"⚠️  Error parsing {filename}: {e}")
            self.questions = []
        except Exception as e:
            print(f"⚠️  Unexpected error loading questions: {e}")
            self.questions = []

    def get_questions_by_topic(self, topic: str, min_difficulty: Optional[int] = None,
                               max_difficulty: Optional[int] = None) -> List[Question]:
        """
        Get questions filtered by topic and optionally by difficulty range.

        Args:
            topic: Topic name to filter by
            min_difficulty: Minimum difficulty (inclusive), None to ignore
            max_difficulty: Maximum difficulty (inclusive), None to ignore

        Returns:
            List of matching questions
        """
        filtered = [q for q in self.questions if q.topic == topic]

        if min_difficulty is not None:
            filtered = [q for q in filtered if q.difficulty >= min_difficulty]

        if max_difficulty is not None:
            filtered = [q for q in filtered if q.difficulty <= max_difficulty]

        return filtered

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

    def handle_hint_system(self, question: Question, hints_used: List[int]) -> Optional[str]:
        """
        Handle hint system for any question type.
        Returns: user_answer if they gave an answer, None if they asked for hint
        """
        user_input = input("Your answer (or type 'hint' for a hint): ").strip()

        if user_input.lower() == "hint":
            if len(hints_used) < len(question.hints):
                hint_idx = len(hints_used)
                print(f"\n💡 Hint {hint_idx + 1}: {question.hints[hint_idx]}\n")
                hints_used.append(hint_idx)
                return None
            else:
                if len(question.hints) == 0:
                    print("\n⚠️  No hints available for this question!\n")
                else:
                    print("\n⚠️  No more hints available!\n")
                return None

        return user_input

    def ask_question(self, question: Question) -> bool:
        """
        Ask a question and handle the user's response.

        Args:
            question: The question to ask

        Returns:
            True if answered correctly, False otherwise
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

        if question.subtopic:
            print(f"Subtopic: {question.subtopic}")
        print(f"\n{question.prompt}\n")

        hints_used = []
        correct = False

        if question.type == "mcq":
            # Display choices with letter labels
            for i, choice in enumerate(question.choices):
                letter = chr(ord('A') + i)
                print(f"  {letter}) {choice}")
            print()

            # Get answer with hint support
            while True:
                user_answer = self.handle_hint_system(question, hints_used)
                if user_answer is None:
                    continue  # User asked for hint, re-prompt

                # Parse user answer - accept letters (A, B, C) or numbers (0, 1, 2)
                user_answer = user_answer.strip().upper()

                # Try to convert letter to index
                if len(user_answer) == 1 and user_answer.isalpha():
                    user_idx = ord(user_answer) - ord('A')
                elif user_answer.isdigit():
                    user_idx = int(user_answer)
                else:
                    print("⚠️  Please enter a letter (A, B, C, ...) or number (0, 1, 2, ...)")
                    continue

                # Check if valid index
                if 0 <= user_idx < len(question.choices):
                    correct = (user_idx == question.correctChoiceIndex)
                    break
                else:
                    print(f"⚠️  Please enter a valid choice (A-{chr(ord('A') + len(question.choices) - 1)})")
                    continue

        elif question.type == "short_answer":
            # Get answer with hint support
            while True:
                user_answer = self.handle_hint_system(question, hints_used)
                if user_answer is None:
                    continue  # User asked for hint, re-prompt
                break

            # Normalize answer
            user_normalized = user_answer.strip().lower()
            expected_normalized = question.expectedAnswer.strip().lower()

            # Check if correct - either exact match or all keywords present
            if user_normalized == expected_normalized:
                correct = True
            elif question.expectedAnswerKeywords:
                # Check if all keywords appear in the user's answer
                keywords_found = all(
                    keyword.lower() in user_normalized
                    for keyword in question.expectedAnswerKeywords
                )
                correct = keywords_found
            else:
                # No keywords specified, only accept exact match
                correct = False

        else:
            # Unknown question type
            print(f"⚠️  Warning: Unknown question type '{question.type}'. Skipping...")
            input("Press Enter to continue...")
            return False

        # Update progress
        hint_used_flag = len(hints_used) > 0
        self.update_progress(question.id, question.topic, correct, hint_used_flag)

        # Show explanation
        print(f"\n📚 Explanation: {question.explanation}\n")
        input("Press Enter to continue...")

        return correct

    # ==================== Game Modes ====================

    def study_by_topic(self):
        """Let user study questions from a specific topic with adaptive difficulty."""
        self.clear_screen()
        self.print_header("Study by Topic")

        topics = self.get_topics()

        if not topics:
            print("\n⚠️  No topics available! Please check questions.json")
            input("Press Enter to continue...")
            return

        print("\nAvailable topics:\n")
        for i, topic in enumerate(topics, 1):
            xp = self.get_topic_xp(topic)
            level = self.get_topic_level(topic)
            level_name = ["", "Beginner", "Intermediate", "Advanced"][level]
            num_questions = len(self.get_questions_by_topic(topic))
            print(f"  {i}. {topic.replace('_', ' ').title()}")
            print(f"      Level {level} ({level_name}) | XP: {xp} | {num_questions} questions")

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
                        print(f"\n⚠️  No questions available for topic '{selected_topic}'!")
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
            except KeyboardInterrupt:
                print("\n\nReturning to main menu...")
                return

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

        try:
            # Use adaptive selection across all questions
            questions = self.select_adaptive_questions(self.questions, num_questions)

            for i, question in enumerate(questions, 1):
                self.clear_screen()
                print(f"\n[Question {i}/{num_questions}]\n")
                self.ask_question(question)

            self.clear_screen()
            print("\n🏆 Adventure complete! You're getting stronger!\n")
            input("Press Enter to return to menu...")
        except KeyboardInterrupt:
            print("\n\nReturning to main menu...")
            return

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

        try:
            # Use adaptive selection for review (prioritize recent mistakes)
            num_to_review = min(len(mistake_questions), 5)
            questions = self.select_adaptive_questions(mistake_questions, num_to_review)

            for question in questions:
                self.clear_screen()
                self.ask_question(question)

            self.clear_screen()
            print("\n✅ Review session complete! Keep up the great work!\n")
            input("Press Enter to return to menu...")
        except KeyboardInterrupt:
            print("\n\nReturning to main menu...")
            return

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
        try:
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
        except KeyboardInterrupt:
            self.clear_screen()
            print("\n\n👋 Thanks for studying! Keep learning and growing!\n")
            self.print_separator()

    # ==================== Helper Methods ====================

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

    if not game.questions:
        print("\n⚠️  No questions loaded! Please ensure questions.json exists.")
        print("Exiting...")
        return

    game.run()


if __name__ == "__main__":
    main()
