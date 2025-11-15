import json
from typing import Any, Dict, List, Optional

class TreeNode:
    __slots__ = ("value", "left", "right")

    def __init__(self, value: int) -> None:
        self.value = value
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None


def insert_bst(root: Optional[TreeNode], key: int) -> TreeNode:
    if root is None:
        return TreeNode(key)
    if key < root.value:
        root.left = insert_bst(root.left, key)
    else:
        root.right = insert_bst(root.right, key)
    return root


def build_bst_from_list(values: List[int]) -> Optional[TreeNode]:
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
        left = 2 * i + 1
        right = 2 * i + 2
        if left < len(nodes):
            node.left = nodes[left]
        if right < len(nodes):
            node.right = nodes[right]
    return nodes[0]


TREE_BUILDERS = {
    "build_bst_from_list": build_bst_from_list,
    "build_balanced_tree": build_balanced_tree,
    "build_small_tree": build_small_tree,
    "build_unbalanced_right": build_unbalanced_right,
    "build_complete_tree": build_complete_tree,
}


def make_task(task: Dict[str, Any]) -> Dict[str, Any]:
    namespace: Dict[str, Any] = {"TreeNode": TreeNode}
    exec(task["reference_impl"], namespace)
    func = namespace[task["function_name"]]
    for case in task["test_cases"]:
        builder = TREE_BUILDERS[case["tree_builder"]]
        root = builder(*case.get("builder_args", []))
        args = [root if arg == "__root__" else arg for arg in case.get("call_args", [])]
        case["expected"] = func(*args)
    return task


tasks: List[Dict[str, Any]] = []

# Task 1: count leaves
tasks.append(make_task({
    "id": "code-count-leaves",
    "level": 5,
    "topic": "trees",
    "prompt": "Write count_leaves(root) that returns how many nodes in the tree have no children.",
    "function_name": "count_leaves",
    "function_signature": "def count_leaves(root: TreeNode) -> int:",
    "helper_description": "Treat None as contributing 0 leaves. A leaf has both children equal to None.",
    "hints": ["Check for the leaf condition before recursing.", "Sum leaves from left and right subtrees."],
    "explanation": "Use recursion: if a node has no children return 1, otherwise recurse on children and sum their counts.",
    "reference_impl": """
from typing import Optional

def count_leaves(root: Optional[TreeNode]) -> int:
    if not root:
        return 0
    if not root.left and not root.right:
        return 1
    return count_leaves(root.left) + count_leaves(root.right)
""",
    "test_cases": [
        {"description": "Complete balanced tree", "tree_builder": "build_balanced_tree", "call_args": ["__root__"]},
        {"description": "Small mixed tree", "tree_builder": "build_small_tree", "call_args": ["__root__"]},
        {"description": "Right-skewed chain", "tree_builder": "build_unbalanced_right", "call_args": ["__root__"]},
    ],
}))

# Task 2: count_less_than

tasks.append(make_task({
    "id": "code-count-less-than",
    "level": 5,
    "topic": "trees",
    "prompt": "Implement count_less_than(root, limit) that returns how many nodes store a value strictly less than limit.",
    "function_name": "count_less_than",
    "function_signature": "def count_less_than(root: TreeNode, limit: int) -> int:",
    "helper_description": "You may assume integer keys. Traverse the whole tree; no BST assumption is required.",
    "hints": ["Check the current node then recurse on children.", "Add the recursive counts together."],
    "explanation": "Perform a recursive traversal counting the node if its value is below the limit, then recurse left/right.",
    "reference_impl": """
from typing import Optional

def count_less_than(root: Optional[TreeNode], limit: int) -> int:
    if not root:
        return 0
    count = 1 if root.value < limit else 0
    return count + count_less_than(root.left, limit) + count_less_than(root.right, limit)
""",
    "test_cases": [
        {"description": "Values below threshold", "tree_builder": "build_balanced_tree", "call_args": ["__root__", 11]},
        {"description": "High threshold", "tree_builder": "build_small_tree", "call_args": ["__root__", 20]},
        {"description": "Tight threshold", "tree_builder": "build_unbalanced_right", "call_args": ["__root__", 4]},
    ],
}))

# Task 3: range sum

tasks.append(make_task({
    "id": "code-range-sum",
    "level": 5,
    "topic": "trees",
    "prompt": "Implement range_sum(root, low, high) that sums node values in the inclusive range [low, high].",
    "function_name": "range_sum",
    "function_signature": "def range_sum(root: TreeNode, low: int, high: int) -> int:",
    "helper_description": "If the tree is a BST you can prune branches, but a full traversal also earns credit.",
    "hints": ["Only add the node if low <= value <= high.", "You may skip left/right subtrees when the node value is outside the range."],
    "explanation": "Use recursion; for a BST you can skip left when the node value is below low or skip right when above high.",
    "reference_impl": """
from typing import Optional

def range_sum(root: Optional[TreeNode], low: int, high: int) -> int:
    if not root:
        return 0
    total = 0
    if low <= root.value <= high:
        total += root.value
    if root.value > low:
        total += range_sum(root.left, low, high)
    if root.value < high:
        total += range_sum(root.right, low, high)
    return total
""",
    "test_cases": [
        {"description": "Middle range", "tree_builder": "build_balanced_tree", "call_args": ["__root__", 6, 15]},
        {"description": "Low range only", "tree_builder": "build_small_tree", "call_args": ["__root__", 0, 3]},
        {"description": "Full range", "tree_builder": "build_unbalanced_right", "call_args": ["__root__", 1, 10]},
    ],
}))

# Task 4: tree height

tasks.append(make_task({
    "id": "code-tree-height",
    "level": 5,
    "topic": "trees",
    "prompt": "Write tree_height(root) that returns the height in edges (empty tree = -1, single node = 0).",
    "function_name": "tree_height",
    "function_signature": "def tree_height(root: TreeNode) -> int:",
    "helper_description": "Height is the number of edges on the longest path from this node to a leaf.",
    "hints": ["Height of an empty tree is -1.", "Height is 1 + max(left_height, right_height)."],
    "explanation": "Use recursion returning -1 for None, otherwise 1 + max(left height, right height).",
    "reference_impl": """
from typing import Optional

def tree_height(root: Optional[TreeNode]) -> int:
    if not root:
        return -1
    return 1 + max(tree_height(root.left), tree_height(root.right))
""",
    "test_cases": [
        {"description": "Complete tree", "tree_builder": "build_complete_tree", "call_args": ["__root__"]},
        {"description": "Right skewed", "tree_builder": "build_unbalanced_right", "call_args": ["__root__"]},
        {"description": "Single node", "tree_builder": "build_bst_from_list", "builder_args": [[42]], "call_args": ["__root__"]},
    ],
}))

# Task 5: nodes at depth

tasks.append(make_task({
    "id": "code-nodes-at-depth",
    "level": 5,
    "topic": "trees",
    "prompt": "Implement count_nodes_at_depth(root, depth) that counts how many nodes appear exactly at the given depth (root depth = 0).",
    "function_name": "count_nodes_at_depth",
    "function_signature": "def count_nodes_at_depth(root: TreeNode, depth: int) -> int:",
    "helper_description": "Depth decreases as you recurse; stop counting when depth becomes negative.",
    "hints": ["When depth == 0 you found a node to count.", "Recurse on children with depth-1."],
    "explanation": "Decrease depth as you traverse; when depth hits zero return 1 if the node exists, else recurse and sum results.",
    "reference_impl": """
from typing import Optional

def count_nodes_at_depth(root: Optional[TreeNode], depth: int) -> int:
    if not root or depth < 0:
        return 0
    if depth == 0:
        return 1
    return count_nodes_at_depth(root.left, depth - 1) + count_nodes_at_depth(root.right, depth - 1)
""",
    "test_cases": [
        {"description": "Depth two in complete tree", "tree_builder": "build_complete_tree", "call_args": ["__root__", 2]},
        {"description": "Depth one in small tree", "tree_builder": "build_small_tree", "call_args": ["__root__", 1]},
        {"description": "Depth four in skewed tree", "tree_builder": "build_unbalanced_right", "call_args": ["__root__", 4]},
    ],
}))

# Task 6: sum left leaves

tasks.append(make_task({
    "id": "code-sum-left-leaves",
    "level": 5,
    "topic": "trees",
    "prompt": "Write sum_left_leaves(root) that adds the values of all leaves that are left children of their parent.",
    "function_name": "sum_left_leaves",
    "function_signature": "def sum_left_leaves(root: TreeNode) -> int:",
    "helper_description": "Pass along whether a node is reached from a left edge.",
    "hints": ["Use a helper that tracks if the current node is a left child.", "Add the node value only when it is a leaf reached via the left edge."],
    "explanation": "Recurse while tracking whether the current node is a left child; when it is a leaf reached from the left, add its value.",
    "reference_impl": """
from typing import Optional

def sum_left_leaves(root: Optional[TreeNode]) -> int:
    def helper(node: Optional[TreeNode], is_left: bool) -> int:
        if not node:
            return 0
        if not node.left and not node.right and is_left:
            return node.value
        return helper(node.left, True) + helper(node.right, False)
    return helper(root, False)
""",
    "test_cases": [
        {"description": "Balanced tree", "tree_builder": "build_balanced_tree", "call_args": ["__root__"]},
        {"description": "Complete tree", "tree_builder": "build_complete_tree", "call_args": ["__root__"]},
        {"description": "Skewed tree", "tree_builder": "build_unbalanced_right", "call_args": ["__root__"]},
    ],
}))

# Task 7: validate BST

tasks.append(make_task({
    "id": "code-validate-bst",
    "level": 5,
    "topic": "trees",
    "prompt": "Implement is_valid_bst(root, lower=None, upper=None) that returns True if the tree satisfies BST ordering.",
    "function_name": "is_valid_bst",
    "function_signature": "def is_valid_bst(root: TreeNode, lower: Optional[int] = None, upper: Optional[int] = None) -> bool:",
    "helper_description": "Use min/max bounds that shrink as you recurse down the tree.",
    "hints": ["When visiting a node ensure lower < node.value < upper.", "Update the bounds when recursing left or right."],
    "explanation": "Carry allowable bounds down the recursion: left children tighten the upper bound, right children tighten the lower bound.",
    "reference_impl": """
from typing import Optional

def is_valid_bst(root: Optional[TreeNode], lower: Optional[int] = None, upper: Optional[int] = None) -> bool:
    if not root:
        return True
    if lower is not None and root.value <= lower:
        return False
    if upper is not None and root.value >= upper:
        return False
    return is_valid_bst(root.left, lower, root.value) and is_valid_bst(root.right, root.value, upper)
""",
    "test_cases": [
        {"description": "Valid BST", "tree_builder": "build_balanced_tree", "call_args": ["__root__"]},
        {"description": "Single node always valid", "tree_builder": "build_bst_from_list", "builder_args": [[1]], "call_args": ["__root__"]},
        {"description": "Complete tree valid", "tree_builder": "build_complete_tree", "call_args": ["__root__"]},
    ],
}))

# Task 8: path sum

tasks.append(make_task({
    "id": "code-path-sum",
    "level": 5,
    "topic": "trees",
    "prompt": "Implement has_path_sum(root, target) returning True if some root-to-leaf path sums to target.",
    "function_name": "has_path_sum",
    "function_signature": "def has_path_sum(root: TreeNode, target: int) -> bool:",
    "helper_description": "Subtract node values as you go down; check when reaching leaves.",
    "hints": ["When you reach a leaf, compare the remaining target to the node value.", "Recurse on children with target - node.value."],
    "explanation": "At each node subtract its value from the target; when at a leaf check if the remainder equals the leaf value.",
    "reference_impl": """
from typing import Optional

def has_path_sum(root: Optional[TreeNode], target: int) -> bool:
    if not root:
        return False
    if not root.left and not root.right:
        return root.value == target
    remaining = target - root.value
    return has_path_sum(root.left, remaining) or has_path_sum(root.right, remaining)
""",
    "test_cases": [
        {"description": "Path exists in balanced tree", "tree_builder": "build_balanced_tree", "call_args": ["__root__", 43]},
        {"description": "No such path", "tree_builder": "build_small_tree", "call_args": ["__root__", 99]},
        {"description": "Skewed tree path", "tree_builder": "build_unbalanced_right", "call_args": ["__root__", 21]},
    ],
}))

# Task 9: count full nodes

tasks.append(make_task({
    "id": "code-count-full-nodes",
    "level": 5,
    "topic": "trees",
    "prompt": "Write count_full_nodes(root) that counts how many nodes have both a left and right child.",
    "function_name": "count_full_nodes",
    "function_signature": "def count_full_nodes(root: TreeNode) -> int:",
    "helper_description": "A full node has two children; leaves and nodes with one child do not count.",
    "hints": ["Check if both children exist, add one, then recurse.", "Visit every node recursively."],
    "explanation": "Traverse the tree; when a node has both children add one plus recurse on each subtree.",
    "reference_impl": """
from typing import Optional

def count_full_nodes(root: Optional[TreeNode]) -> int:
    if not root:
        return 0
    full = 1 if root.left and root.right else 0
    return full + count_full_nodes(root.left) + count_full_nodes(root.right)
""",
    "test_cases": [
        {"description": "Complete tree", "tree_builder": "build_complete_tree", "call_args": ["__root__"]},
        {"description": "Balanced BST", "tree_builder": "build_balanced_tree", "call_args": ["__root__"]},
        {"description": "Right skewed", "tree_builder": "build_unbalanced_right", "call_args": ["__root__"]},
    ],
}))

with open("code_tasks.json", "w", encoding="utf-8") as handle:
    json.dump(tasks, handle, indent=2)
