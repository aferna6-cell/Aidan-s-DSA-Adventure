#!/usr/bin/env python3
"""DSA Study Game – interactive practice for classic CS coursework."""
from __future__ import annotations

import json
import os
import random
import re
import sys
import textwrap
import uuid
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

# =============================
# Global configuration
# =============================
LEVEL_UNLOCK_REQUIREMENTS = {
    2: 8,  # need 8 fully correct answers in lower level
    3: 8,
    4: 8,
    5: 8,
}

XP_REWARDS = {
    "full": 10,
    "partial": 5,
    "none": 0,
}

HINT_COMMAND = "hint"
QUIT_COMMAND = "q"
END_CODE_SENTINEL = "END"


# =============================
# Tree helpers for level 3 and level 5
# =============================
@dataclass
class TreeNode:
    value: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None

    def __repr__(self) -> str:
        return f"TreeNode({self.value})"


def insert_bst(root: Optional[TreeNode], key: int) -> TreeNode:
    if root is None:
        return TreeNode(key)
    if key < root.value:
        root.left = insert_bst(root.left, key)
    else:
        root.right = insert_bst(root.right, key)
    return root


def tree_height(node: Optional[TreeNode]) -> int:
    if not node:
        return 0
    return 1 + max(tree_height(node.left), tree_height(node.right))


def tree_to_level_order_list(root: Optional[TreeNode]) -> List[int]:
    if not root:
        return []
    queue: List[Optional[TreeNode]] = [root]
    output: List[int] = []
    while queue:
        node = queue.pop(0)
        if node:
            output.append(node.value)
            queue.append(node.left)
            queue.append(node.right)
    return output


def balance_factor(node: Optional[TreeNode]) -> int:
    return tree_height(node.left) - tree_height(node.right) if node else 0


def rotate_right(y: TreeNode) -> TreeNode:
    x = y.left
    assert x is not None
    t2 = x.right
    x.right = y
    y.left = t2
    return x


def rotate_left(x: TreeNode) -> TreeNode:
    y = x.right
    assert y is not None
    t2 = y.left
    y.left = x
    x.right = t2
    return y


def insert_avl(root: Optional[TreeNode], key: int, steps: List[str]) -> TreeNode:
    if root is None:
        steps.append(f"Inserted {key} as a new node.")
        return TreeNode(key)
    if key < root.value:
        root.left = insert_avl(root.left, key, steps)
    else:
        root.right = insert_avl(root.right, key, steps)

    bf = balance_factor(root)
    if bf > 1 and key < root.left.value:
        steps.append(f"Left-left case at {root.value}, perform right rotation.")
        return rotate_right(root)
    if bf < -1 and key > root.right.value:
        steps.append(f"Right-right case at {root.value}, perform left rotation.")
        return rotate_left(root)
    if bf > 1 and key > root.left.value:
        steps.append(f"Left-right case at {root.value}, rotate left at {root.left.value} then right at {root.value}.")
        root.left = rotate_left(root.left)
        return rotate_right(root)
    if bf < -1 and key < root.right.value:
        steps.append(f"Right-left case at {root.value}, rotate right at {root.right.value} then left at {root.value}.")
        root.right = rotate_right(root.right)
        return rotate_left(root)
    return root


# Heap helpers

def heapify_list(values: List[int]) -> List[int]:
    import heapq

    heap: List[int] = []
    for val in values:
        heapq.heappush(heap, val)
    return list(heap)


# =============================
# Level 3 generators
# =============================
def generate_random_bst_insertion_task() -> Dict[str, Any]:
    start_values = random.sample(range(10, 60), random.randint(5, 7))
    root: Optional[TreeNode] = None
    for val in start_values:
        root = insert_bst(root, val)
    inserts = random.sample([v for v in range(10, 60) if v not in start_values], random.randint(2, 3))
    explanation_lines = [
        f"Start with BST level-order: {', '.join(map(str, tree_to_level_order_list(root)))}"
    ]
    for val in inserts:
        root = insert_bst(root, val)
        explanation_lines.append(f"Insert {val} following BST rules.")
    expected = tree_to_level_order_list(root)
    explanation_lines.append(f"Final level-order traversal: {', '.join(map(str, expected))}.")
    return {
        "id": f"generated-bst-{uuid.uuid4().hex[:8]}",
        "level": 3,
        "question_type": "tree_heap",
        "structure_kind": "BST",
        "representation": "Level-order traversal",
        "initial_values": start_values,
        "inserts": inserts,
        "expected_representation": expected,
        "grading_representation_hint": "Provide the final level-order traversal as comma-separated integers.",
        "hints": [
            "Recall that BST inserts go left for smaller keys and right for larger keys.",
            "Perform a breadth-first traversal after all inserts to describe the final tree."
        ],
        "explanation": "\n".join(explanation_lines),
    }


def generate_random_avl_insertion_task() -> Dict[str, Any]:
    base_values = random.sample(range(5, 40), 5)
    root: Optional[TreeNode] = None
    steps: List[str] = []
    for val in base_values:
        root = insert_avl(root, val, steps)
    inserts = random.sample([v for v in range(5, 40) if v not in base_values], 2)
    for val in inserts:
        steps.append(f"-- Now inserting {val} --")
        root = insert_avl(root, val, steps)
    expected = tree_to_level_order_list(root)
    steps.append(f"Level-order after rebalancing: {', '.join(map(str, expected))}.")
    return {
        "id": f"generated-avl-{uuid.uuid4().hex[:8]}",
        "level": 3,
        "question_type": "tree_heap",
        "structure_kind": "AVL",
        "representation": "Level-order traversal",
        "initial_values": base_values,
        "inserts": inserts,
        "expected_representation": expected,
        "grading_representation_hint": "List the final AVL tree in level-order (breadth-first).",
        "hints": [
            "Track balance factor at each node; rotate when |BF| exceeds 1.",
            "Perform level-order traversal on the balanced tree."
        ],
        "explanation": "\n".join(steps),
    }


def generate_random_heap_insertion_task() -> Dict[str, Any]:
    initial = heapify_list(random.sample(range(10, 99), random.randint(5, 7)))
    inserts = random.sample(range(10, 99), 2)
    explanation_lines = [f"Starting min-heap array: {initial}"]
    import heapq

    heap = initial[:]
    heapq.heapify(heap)
    for val in inserts:
        heapq.heappush(heap, val)
        explanation_lines.append(f"Insert {val} and bubble up to maintain heap order: {list(heap)}")
    expected = list(heap)
    explanation_lines.append(f"Final heap array: {expected}")
    return {
        "id": f"generated-heap-{uuid.uuid4().hex[:8]}",
        "level": 3,
        "question_type": "tree_heap",
        "structure_kind": "Min-heap",
        "representation": "Array representation",
        "initial_values": initial,
        "inserts": inserts,
        "expected_representation": expected,
        "grading_representation_hint": "Give the final heap as a comma-separated array (index 0 is the root).",
        "hints": [
            "When inserting into a min-heap, place the value at the end then bubble up.",
            "Compare the final structure against the heap order property."
        ],
        "explanation": "\n".join(explanation_lines),
    }


LEVEL3_GENERATORS: List[Callable[[], Dict[str, Any]]] = [
    generate_random_bst_insertion_task,
    generate_random_avl_insertion_task,
    generate_random_heap_insertion_task,
]


# =============================
# Level 5 tree builders
# =============================
def build_bst_from_list(values: Sequence[int]) -> Optional[TreeNode]:
    root: Optional[TreeNode] = None
    for val in values:
        root = insert_bst(root, val)
    return root


def build_balanced_tree() -> Optional[TreeNode]:
    return build_bst_from_list([10, 5, 15, 3, 7, 12, 18])


def build_small_tree() -> Optional[TreeNode]:
    root = TreeNode(5)
    root.left = TreeNode(2)
    root.right = TreeNode(8)
    root.left.left = TreeNode(1)
    root.left.right = TreeNode(3)
    root.right.right = TreeNode(10)
    return root


def build_unbalanced_right() -> Optional[TreeNode]:
    root = TreeNode(1)
    node = root
    for val in range(2, 7):
        node.right = TreeNode(val)
        node = node.right
    return root


def build_complete_tree() -> Optional[TreeNode]:
    values = [8, 4, 12, 2, 6, 10, 14]
    nodes = [TreeNode(v) for v in values]
    for i, node in enumerate(nodes):
        left_i = 2 * i + 1
        right_i = 2 * i + 2
        if left_i < len(nodes):
            node.left = nodes[left_i]
        if right_i < len(nodes):
            node.right = nodes[right_i]
    return nodes[0]


TREE_BUILDERS: Dict[str, Callable[..., Optional[TreeNode]]] = {
    "build_bst_from_list": build_bst_from_list,
    "build_balanced_tree": build_balanced_tree,
    "build_small_tree": build_small_tree,
    "build_unbalanced_right": build_unbalanced_right,
    "build_complete_tree": build_complete_tree,
}


# =============================
# Utility functions
# =============================
def normalize_sequence_answer(answer: str) -> List[str]:
    tokens = [token for token in re.split(r"[\s,]+", answer.strip()) if token]
    return tokens


def keyword_score(answer: str, required: List[str], partial: List[str]) -> Tuple[bool, bool]:
    normalized = answer.lower()
    required_hits = sum(1 for kw in required if kw.lower() in normalized)
    partial_hits = sum(1 for kw in partial if kw.lower() in normalized)
    full_credit = required_hits == len(required) and len(required) > 0
    partial_credit = False
    if not full_credit:
        half_required = (len(required) + 1) // 2
        if required_hits >= half_required and len(required) > 0:
            partial_credit = True
        elif partial_hits >= max(1, len(partial) // 2):
            partial_credit = True
    return full_credit, partial_credit


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# =============================
# Main game class
# =============================
class DSAStudyGame:
    def __init__(self) -> None:
        self.questions: List[Dict[str, Any]] = self.load_json("questions.json")
        self.code_tasks: List[Dict[str, Any]] = self.load_json("code_tasks.json")
        self.questions_by_level: Dict[int, List[Dict[str, Any]]] = {}
        for question in self.questions:
            self.questions_by_level.setdefault(question["level"], []).append(question)
        self.level_stats: Dict[int, Dict[str, int]] = {
            level: {"attempts": 0, "full_correct": 0, "partial": 0, "xp": 0}
            for level in range(1, 6)
        }
        self.unlocked_levels: Dict[int, bool] = {1: True, 2: False, 3: False, 4: False, 5: False}

    @staticmethod
    def load_json(filename: str) -> List[Dict[str, Any]]:
        if not os.path.exists(filename):
            print(f"Required file {filename} is missing.")
            sys.exit(1)
        try:
            with open(filename, "r", encoding="utf-8") as handle:
                return json.load(handle)
        except json.JSONDecodeError as exc:
            print(f"Failed to parse {filename}: {exc}")
            sys.exit(1)

    # ----------------------------
    # Core loop
    # ----------------------------
    def start(self) -> None:
        try:
            while True:
                self.show_summary()
                self.show_menu()
                choice = input("Select a level (1-5) or Q to quit: ").strip().lower()
                if choice == "q":
                    print("Thanks for studying! Keep practicing.")
                    break
                if not choice.isdigit():
                    print("Please enter a number between 1 and 5, or Q to quit.")
                    continue
                level = int(choice)
                if level not in range(1, 6):
                    print("Invalid level.")
                    continue
                if not self.unlocked_levels.get(level, False):
                    print("⚠️  That level is locked. Master the previous level first!")
                    continue
                if level == 1:
                    self.run_level_1_vocab()
                elif level == 2:
                    self.run_level_2_short_answer()
                elif level == 3:
                    self.run_level_3_trees_heaps()
                elif level == 4:
                    self.run_level_4_design()
                else:
                    self.run_level_5_code_tasks()
        except KeyboardInterrupt:
            print("\nInterrupted. Progress for this session is summarized below:")
            self.show_summary()

    def show_menu(self) -> None:
        print("\n=== DSA Study Game ===")
        for level in range(1, 6):
            status = "Unlocked" if self.unlocked_levels.get(level) else "Locked"
            description = {
                1: "Vocabulary",
                2: "Conceptual short answer",
                3: "Trees & heaps",
                4: "Algorithm design",
                5: "Recursive coding",
            }[level]
            print(f"{level}) Level {level} – {description} [{status}]")
        print("Q) Quit")

    def show_summary(self) -> None:
        print("\nSession progress:")
        for level in range(1, 6):
            stats = self.level_stats[level]
            print(
                f"  Level {level}: attempts={stats['attempts']}, full correct={stats['full_correct']}, "
                f"partial={stats['partial']}, XP={stats['xp']}"
            )

    def award_xp(self, level: int, credit: str) -> None:
        xp = XP_REWARDS[credit]
        self.level_stats[level]["xp"] += xp
        if credit == "full":
            self.level_stats[level]["full_correct"] += 1
        elif credit == "partial":
            self.level_stats[level]["partial"] += 1
        self.check_unlocks()

    def check_unlocks(self) -> None:
        for level in range(2, 6):
            if not self.unlocked_levels[level]:
                requirement = LEVEL_UNLOCK_REQUIREMENTS[level]
                if self.level_stats[level - 1]["full_correct"] >= requirement:
                    self.unlocked_levels[level] = True
                    print(
                        f"\n🎉 Level {level} unlocked! Keep the streak going for more XP."
                    )

    # ----------------------------
    # Level 1
    # ----------------------------
    def run_level_1_vocab(self) -> None:
        questions = self.questions_by_level.get(1, [])
        if not questions:
            print("No vocabulary questions loaded.")
            return
        while True:
            question = random.choice(questions)
            hints = question.get("hints", [])
            hint_index = 0
            print("\nDefinition:")
            print(textwrap.fill(question["definition"], width=80))
            prompt = (
                f"Type the corresponding term (or '{HINT_COMMAND}' for a hint, '{QUIT_COMMAND}' to return): "
            )
            answer = input(prompt).strip()
            if answer.lower() == QUIT_COMMAND:
                return
            if answer.lower() == HINT_COMMAND:
                if hint_index < len(hints):
                    print(f"Hint: {hints[hint_index]}")
                    hint_index += 1
                else:
                    print("No more hints available.")
                continue
            self.level_stats[1]["attempts"] += 1
            normalized = answer.lower().strip()
            valid_terms = [question["term"].lower()] + [syn.lower() for syn in question.get("acceptable_synonyms", [])]
            if normalized in valid_terms:
                print("✅ Correct!" )
                print(question["explanation"])
                self.award_xp(1, "full")
            else:
                print(f"❌ Incorrect. The correct term was: {question['term']}")
                print(question["explanation"])
                self.award_xp(1, "none")

    # ----------------------------
    # Level 2
    # ----------------------------
    def run_level_2_short_answer(self) -> None:
        questions = self.questions_by_level.get(2, [])
        if not questions:
            print("No short-answer questions loaded.")
            return
        while True:
            question = random.choice(questions)
            print("\nQuestion:")
            print(textwrap.fill(question["prompt"], width=80))
            print(f"(Type '{QUIT_COMMAND}' to return to the menu)")
            response = input("Your answer: ").strip()
            if response.lower() == QUIT_COMMAND:
                return
            self.level_stats[2]["attempts"] += 1
            full, partial = keyword_score(
                response,
                question.get("expectedKeywordsRequired", []),
                question.get("expectedKeywordsPartial", []),
            )
            if full:
                print("✅ Correct!")
                self.award_xp(2, "full")
            elif partial:
                print("➗ Partially correct – you have the main idea, but check details.")
                self.award_xp(2, "partial")
            else:
                print("❌ Incorrect – review the explanation carefully.")
                self.award_xp(2, "none")
            self.display_hints_and_explanation(question)

    # ----------------------------
    # Level 3
    # ----------------------------
    def run_level_3_trees_heaps(self) -> None:
        static_questions = self.questions_by_level.get(3, [])
        if not static_questions and not LEVEL3_GENERATORS:
            print("No tree/heap tasks available.")
            return
        while True:
            use_generator = random.choice([True, False]) if LEVEL3_GENERATORS else False
            if use_generator:
                question = random.choice(LEVEL3_GENERATORS)()
            else:
                question = random.choice(static_questions)
            print("\nStructure type:", question.get("structure_kind", "Tree/Heap"))
            print("Representation:", question.get("representation"))
            print("Initial values:", question.get("initial_values"))
            print("Insert in this order:", question.get("inserts"))
            print(f"Provide answer as described ({question.get('grading_representation_hint')})")
            print(f"(Type '{HINT_COMMAND}' for a hint, '{QUIT_COMMAND}' to return to the menu)")
            hints = question.get("hints", [])
            hint_index = 0
            while True:
                user_answer = input("Your final structure: ").strip()
                if user_answer.lower() == QUIT_COMMAND:
                    return
                if user_answer.lower() == HINT_COMMAND:
                    if hint_index < len(hints):
                        print(f"Hint: {hints[hint_index]}")
                        hint_index += 1
                    else:
                        print("No additional hints available.")
                    continue
                break
            self.level_stats[3]["attempts"] += 1
            expected_tokens = [str(val) for val in question["expected_representation"]]
            user_tokens = normalize_sequence_answer(user_answer)
            if user_tokens == expected_tokens:
                print("✅ Correct structure!")
                self.award_xp(3, "full")
            else:
                print("❌ Not quite. Compare against the expected state shown below.")
                print("Expected:", ", ".join(expected_tokens))
                self.award_xp(3, "none")
            print(question.get("explanation", ""))

    # ----------------------------
    # Level 4
    # ----------------------------
    def run_level_4_design(self) -> None:
        questions = self.questions_by_level.get(4, [])
        if not questions:
            print("No design questions available.")
            return
        while True:
            question = random.choice(questions)
            print("\nDesign prompt:")
            print(textwrap.fill(question["prompt"], width=80))
            print(f"(Type '{QUIT_COMMAND}' to return)")
            answer = input("Describe your approach: ").strip()
            if answer.lower() == QUIT_COMMAND:
                return
            self.level_stats[4]["attempts"] += 1
            full, partial = keyword_score(
                answer,
                question.get("expectedKeywordsRequired", []),
                question.get("expectedKeywordsPartial", []),
            )
            if full:
                print("✅ Strong design!")
                self.award_xp(4, "full")
            elif partial:
                print("➗ Partially correct – refine the algorithm.")
                self.award_xp(4, "partial")
            else:
                print("❌ Missing key ideas – review the explanation.")
                self.award_xp(4, "none")
            self.display_hints_and_explanation(question)

    # ----------------------------
    # Level 5
    # ----------------------------
    def run_level_5_code_tasks(self) -> None:
        if not self.code_tasks:
            print("No coding tasks loaded.")
            return
        task = random.choice(self.code_tasks)
        print("\nRecursive coding challenge:")
        print(textwrap.fill(task["prompt"], width=80))
        print(f"Function signature: {task['function_signature']}")
        if task.get("helper_description"):
            print(textwrap.fill(f"Helper info: {task['helper_description']}", width=80))
        print(
            f"Enter your function implementation below. End with a line containing only '{END_CODE_SENTINEL}'."
        )
        user_lines: List[str] = []
        while True:
            line = input()
            if line.strip() == END_CODE_SENTINEL:
                break
            user_lines.append(line)
        user_code = "\n".join(user_lines)
        user_namespace = {"TreeNode": TreeNode}
        try:
            exec(user_code, user_namespace)
        except Exception as exc:
            print(f"Your code did not compile: {exc}")
            return
        user_func = user_namespace.get(task["function_name"])
        if user_func is None:
            print(f"Could not find a function named {task['function_name']} in your code.")
            return
        ref_namespace = {"TreeNode": TreeNode}
        exec(task["reference_impl"], ref_namespace)
        reference_func = ref_namespace[task["function_name"]]
        passed = 0
        total = len(task.get("test_cases", []))
        for case in task.get("test_cases", []):
            builder_name = case["tree_builder"]
            builder = TREE_BUILDERS[builder_name]
            builder_args = case.get("builder_args", [])
            root_for_user = builder(*builder_args)
            root_for_ref = builder(*builder_args)
            call_args = [root_for_user if arg == "__root__" else arg for arg in case.get("call_args", [])]
            ref_args = [root_for_ref if arg == "__root__" else arg for arg in case.get("call_args", [])]
            try:
                user_result = user_func(*call_args)
            except Exception as exc:  # pragma: no cover - runtime feedback
                print(f"Test '{case['description']}' raised an error: {exc}")
                continue
            ref_result = reference_func(*ref_args)
            if user_result == ref_result:
                passed += 1
                print(f"✅ {case['description']}")
            else:
                print(f"❌ {case['description']} – expected {ref_result}, got {user_result}")
        self.level_stats[5]["attempts"] += 1
        if passed == total and total > 0:
            print("All tests passed! Excellent recursion skills.")
            self.award_xp(5, "full")
        elif passed > 0:
            print(f"Partial success: {passed}/{total} tests passed.")
            self.award_xp(5, "partial")
        else:
            print("No tests passed – review the explanation and try again.")
            self.award_xp(5, "none")
        self.display_hints_and_explanation(task)

    # ----------------------------
    def display_hints_and_explanation(self, item: Dict[str, Any]) -> None:
        hints = item.get("hints", [])
        if hints:
            print("Hints:")
            for hint in hints:
                print(f"  - {hint}")
        explanation = item.get("explanation")
        if explanation:
            print("Explanation:")
            print(textwrap.fill(explanation, width=80))


# =============================
# Entrypoint
# =============================
def main() -> None:
    game = DSAStudyGame()
    game.start()


if __name__ == "__main__":
    main()
