import json
from typing import Any, Dict, List, Optional

class Node:
    __slots__ = ("value", "left", "right")

    def __init__(self, value: int) -> None:
        self.value = value
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None


def insert_bst(root: Optional[Node], key: int) -> Node:
    if root is None:
        return Node(key)
    if key < root.value:
        root.left = insert_bst(root.left, key)
    else:
        root.right = insert_bst(root.right, key)
    return root


def height(node: Optional[Node]) -> int:
    if not node:
        return 0
    return 1 + max(height(node.left), height(node.right))


def balance_factor(node: Optional[Node]) -> int:
    return height(node.left) - height(node.right) if node else 0


def rotate_left(z: Node) -> Node:
    y = z.right
    assert y is not None
    t2 = y.left
    y.left = z
    z.right = t2
    return y


def rotate_right(z: Node) -> Node:
    y = z.left
    assert y is not None
    t3 = y.right
    y.right = z
    z.left = t3
    return y


def insert_avl(root: Optional[Node], key: int) -> Node:
    if root is None:
        return Node(key)
    if key < root.value:
        root.left = insert_avl(root.left, key)
    else:
        root.right = insert_avl(root.right, key)

    bf = balance_factor(root)
    if bf > 1 and key < root.left.value:
        return rotate_right(root)
    if bf < -1 and key > root.right.value:
        return rotate_left(root)
    if bf > 1 and key > root.left.value:
        root.left = rotate_left(root.left)
        return rotate_right(root)
    if bf < -1 and key < root.right.value:
        root.right = rotate_right(root.right)
        return rotate_left(root)
    return root


def level_order(root: Optional[Node]) -> List[int]:
    if not root:
        return []
    queue: List[Optional[Node]] = [root]
    order: List[int] = []
    while queue:
        node = queue.pop(0)
        if node:
            order.append(node.value)
            queue.append(node.left)
            queue.append(node.right)
    return order


questions: List[Dict[str, Any]] = []


def add_vocab(qid: str, term: str, definition: str, synonyms: List[str], hints: List[str], explanation: str) -> None:
    questions.append(
        {
            "id": qid,
            "level": 1,
            "question_type": "vocab",
            "topic": "vocabulary",
            "subtopic": "core",
            "term": term,
            "definition": definition,
            "acceptable_synonyms": synonyms,
            "hints": hints,
            "explanation": explanation,
        }
    )


vocab_entries = [
    ("vocab-stack", "Stack", "A linear collection that supports push and pop at one end only, implementing last-in first-out behavior.", ["stack", "lifo"], ["Think about undo operations.", "Newest element leaves first."], "Stacks are LIFO structures with O(1) push/pop at the top."),
    ("vocab-queue", "Queue", "A linear collection where enqueues add to the rear and dequeues remove from the front, yielding first-in first-out order.", ["queue", "fifo"], ["Imagine people waiting in line.", "Departure order matches arrival order."], "Queues model FIFO behavior and power BFS frontiers."),
    ("vocab-deque", "Deque", "A double-ended queue supporting insertion and removal at both the front and back in constant time.", ["deque", "double ended queue"], ["Generalizes both stacks and queues.", "Push or pop on either end."], "Deques allow O(1) operations at both ends."),
    ("vocab-singly", "Singly linked list", "A list composed of nodes where each node stores data plus a pointer to the next node only.", ["singly linked list", "sll"], ["Traversal is forward only.", "Each node knows only its successor."], "Singly linked lists chain nodes with a data field and one next pointer."),
    ("vocab-doubly", "Doubly linked list", "A linked list whose nodes store pointers to both the previous and next nodes.", ["dll", "doubly linked list"], ["Bidirectional traversal is possible.", "Each node has two links."], "Doubly linked lists maintain next and prev references for flexible inserts."),
    ("vocab-sentinel-node", "Sentinel node", "A dummy node placed at an endpoint of a list to simplify insertion and deletion edge cases.", ["sentinel", "dummy node"], ["Often seen in linked lists.", "Stores no user data."], "Sentinel nodes act as guards so code avoids repeated null checks."),
    ("vocab-binary-tree", "Binary tree", "A hierarchical structure in which each node has at most two children called left and right.", ["binary tree"], ["Foundation for BSTs and heaps.", "Each node has ≤ 2 children."], "Binary trees limit branching to two children per node."),
    ("vocab-full", "Full binary tree", "A binary tree where every internal node has exactly two children.", ["proper binary tree", "strict binary tree"], ["No node has only one child.", "Leaves may appear at different depths."], "Full binary trees require internal nodes to have two children."),
    ("vocab-complete", "Complete binary tree", "A binary tree whose levels are completely filled except possibly the last, which is filled from left to right.", ["complete tree"], ["Supports array representation.", "Used by heaps."], "Complete binary trees have no gaps when laid out level by level."),
    ("vocab-extended", "Extended binary tree", "A binary tree where null children are replaced by special external nodes, aiding traversal proofs.", ["extended tree", "full binary tree with externals"], ["Sometimes called a 2-tree.", "External nodes represent null pointers."], "Extended binary trees insert external nodes to reason about structure."),
    ("vocab-bst", "Binary search tree", "A binary tree organized so left descendants are less than the node and right descendants are greater.", ["bst", "binary search tree"], ["In-order traversal lists keys in sorted order.", "Supports logarithmic search when balanced."], "BSTs maintain key order and power sorted operations."),
    ("vocab-avl", "AVL tree", "A self-balancing BST keeping subtree heights within one by using rotations.", ["avl", "avl tree"], ["Named for Adelson-Velsky and Landis.", "Balance factor triggers rotations."], "AVL trees guarantee logarithmic height by rebalancing after inserts/deletes."),
    ("vocab-red-black", "Red-black tree", "A balanced BST that colors nodes red or black and enforces color properties to bound height.", ["red black tree", "rbt"], ["All root-to-leaf paths have the same number of black nodes.", "Rebalancing uses color flips and rotations."], "Red-black trees keep height O(log n) via coloring rules."),
    ("vocab-heap", "Heap", "A tree-based structure satisfying the heap order property so parents dominate their children.", ["heap"], ["Often stored in arrays.", "Supports fast access to priority element."], "Heaps keep the extreme (min or max) key at the root."),
    ("vocab-min-heap", "Min-heap", "A heap in which every parent key is ≤ its children, so the minimum key sits at the root.", ["min heap"], ["Used by priority queues selecting smallest element.", "Delete-min is efficient."], "Min-heaps provide O(1) access to the minimum key."),
    ("vocab-max-heap", "Max-heap", "A heap where each parent key is ≥ its children, keeping the maximum at the root.", ["max heap"], ["Used for priority queues needing the largest element.", "Heapsort uses a max-heap."], "Max-heaps expose the largest key at the root with O(log n) updates."),
    ("vocab-priority-queue", "Priority queue", "An abstract data type supporting insert and removal of the highest-priority item rather than FIFO order.", ["priority queue", "pq"], ["Often backed by heaps.", "Removes based on key priority."], "Priority queues return elements by priority instead of arrival time."),
    ("vocab-height", "Height", "The number of edges on the longest path from a node down to a leaf.", ["tree height"], ["Leaves have height 0.", "Height measures downward."], "Height measures how tall a subtree is and bounds recursion depth."),
    ("vocab-depth", "Depth", "The number of edges from the root to a node.", ["node depth"], ["Root has depth 0.", "Each level increases depth by one."], "Depth counts distance from the root toward leaves."),
    ("vocab-leaf", "Leaf", "A node in a tree that has no children.", ["leaf node"], ["Also called an external node.", "Terminates a path."], "Leaves represent endpoints in a tree with degree zero."),
    ("vocab-internal", "Internal node", "Any node in a tree that has at least one child.", ["internal node"], ["Opposite of a leaf.", "Participates in branching."], "Internal nodes own children and create branching structure."),
    ("vocab-subtree", "Subtree", "A tree formed by a node together with all its descendants.", ["sub tree", "sub-tree"], ["Every child defines one.", "Supports recursive definitions."], "Subtrees form natural subproblems for recursive algorithms."),
    ("vocab-root", "Root", "The unique top node in a tree that has no parent.", ["tree root"], ["Depth zero.", "All nodes descend from it."], "The root anchors the tree and defines traversal starting points."),
    ("vocab-level", "Level", "All nodes at the same depth in a tree.", ["tree level"], ["Level numbers start at zero at the root.", "Level-order traversal visits by level."], "A level groups nodes of equal depth, helpful for BFS reasoning."),
    ("vocab-level-order", "Level-order traversal", "A breadth-first traversal visiting nodes level by level from the root downward.", ["bfs", "breadth first"], ["Implemented with a queue.", "Processes siblings before children."], "Level-order traversal explores a tree breadth-first."),
    ("vocab-preorder", "Pre-order traversal", "A traversal order visiting the node, then the left subtree, then the right subtree.", ["preorder"], ["Node is processed before its children.", "Captures prefix expressions."], "Pre-order yields node-left-right order useful for copying trees."),
    ("vocab-inorder", "In-order traversal", "A traversal visiting the left subtree, then the node, then the right subtree.", ["inorder"], ["Applied to BSTs produces sorted keys.", "Node is processed between its children."], "In-order traversal prints BST keys in sorted order."),
    ("vocab-postorder", "Post-order traversal", "A traversal order visiting the left subtree, then the right subtree, then the node.", ["postorder"], ["Children processed before parent.", "Useful for freeing trees."], "Post-order handles descendants before their parent node."),
    ("vocab-call-stack", "Call stack", "The runtime stack of activation records for active function calls.", ["callstack", "activation stack"], ["Grows with recursion depth.", "Stores locals and return addresses."], "The call stack pushes a new frame for each function call and pops on return."),
    ("vocab-base-case", "Base case", "The simplest input of a recursive algorithm that can be solved directly without further recursion.", ["basecase", "base condition"], ["Prevents infinite recursion.", "Often checks for empty input."], "Base cases stop recursion when a minimal instance is reached."),
    ("vocab-recursive-step", "Recursive step", "The part of a recursive algorithm that breaks the problem into smaller instances and recurses.", ["recursive case", "inductive step"], ["Must move toward base case.", "Combines results."], "Recursive steps reduce the problem and call the function again."),
    ("vocab-amortized", "Amortized analysis", "A technique that averages costs over a sequence of operations to show a low average per operation despite occasional expensive ones.", ["amortized", "amortized cost"], ["Used for dynamic arrays.", "Spreads expensive operations across many cheap ones."], "Amortized analysis charges costly operations to many cheap ones to get an average bound."),
    ("vocab-big-o", "Big-O", "Asymptotic notation describing an upper bound on growth rate up to constant factors.", ["big o"], ["Represents worst-case upper limit.", "Ignores constant multipliers."], "Big-O provides an asymptotic upper bound on runtime or space."),
    ("vocab-big-theta", "Big-Theta", "Asymptotic notation giving a tight bound, both upper and lower, on a function's growth.", ["big theta", "theta"], ["Means same order both ways.", "Sandwiches the growth between two multiples."], "Θ(f(n)) means the function grows on the same order as f(n)."),
    ("vocab-big-omega", "Big-Omega", "Asymptotic notation describing a lower bound on growth rate.", ["big omega", "omega"], ["Guarantees at least this fast.", "Opposite of Big-O."], "Ω(f(n)) says the runtime cannot be asymptotically faster than f(n)."),
    ("vocab-worst-case", "Worst-case complexity", "The running time of an algorithm on the most expensive input of size n.", ["worst case"], ["Provides safety guarantee.", "Often expressed with Big-O."], "Worst-case analysis ensures performance never exceeds a stated bound."),
    ("vocab-average-case", "Average-case complexity", "The expected running time over all inputs of size n under a specified distribution.", ["average case"], ["Depends on probability assumptions.", "Often matches everyday performance."], "Average-case complexity studies expected cost using input probabilities."),
    ("vocab-best-case", "Best-case complexity", "The minimal running time achieved on the easiest inputs of size n.", ["best case"], ["Rarely used for guarantees.", "Sometimes constant time."], "Best-case complexity reflects the most favorable inputs."),
    ("vocab-fragmentation", "Fragmentation", "Wasted memory caused when free space is split into small pieces that cannot satisfy large requests.", ["memory fragmentation"], ["External fragmentation scatters free space.", "Compaction fights it."], "Fragmentation prevents allocating large contiguous blocks even if total free space is large."),
    ("vocab-free-list", "Free list", "A data structure that tracks available memory blocks for allocation.", ["freelist", "free list"], ["Updated on every free.", "May be organized by block size."], "Free lists store addresses of unallocated blocks to reuse them."),
    ("vocab-garbage-collection", "Garbage collection", "Automatic memory management that reclaims objects no longer reachable by the program.", ["garbage collection", "gc"], ["Seen in Java/Python.", "Runs periodically or on demand."], "Garbage collectors find unreachable objects and free their memory."),
    ("vocab-coalescing", "Coalescing", "The allocator action of merging adjacent free blocks into a larger block.", ["coalescence", "coalesce"], ["Happens after freeing.", "Reduces fragmentation."], "Coalescing combines neighboring free blocks to create larger chunks."),
    ("vocab-compaction", "Memory compaction", "Relocating allocated blocks to eliminate gaps and form large contiguous free regions.", ["compaction", "compact"], ["Requires updating pointers.", "Often part of garbage collectors."], "Compaction moves live objects so free space becomes contiguous."),
    ("vocab-roving-pointer", "Roving pointer", "An allocator technique that remembers the last position searched in the free list to distribute scanning cost.", ["roving pointer", "next fit"], ["Avoids starting from the head each time.", "Walks the free list in a loop."], "Roving pointers continue searching from where the last allocation stopped to balance effort."),
    ("vocab-trie", "Trie", "A prefix tree storing keys character by character where each edge represents a symbol.", ["trie", "prefix tree"], ["Great for autocomplete.", "Each node may mark the end of a word."], "Tries support fast prefix queries by branching per character."),
    ("vocab-stack-overflow", "Stack overflow", "An error that occurs when the call stack exceeds its capacity, often due to runaway recursion.", ["stack overflow"], ["Happens when recursion lacks a base case.", "Process aborts when stack memory is exhausted."], "Stack overflow occurs when recursion depth or local allocations exceed stack limits."),
    ("vocab-branch-factor", "Branching factor", "The number of children an internal node has on average, influencing tree height.", ["fanout", "branch factor"], ["Binary trees have factor 2.", "Higher branching shrinks height."], "Branching factor affects how quickly trees expand and impacts height analysis."),
    ("vocab-subtree-size", "Subtree size", "The number of nodes contained in a node's subtree, including the node itself.", ["size", "subtree count"], ["Used in order-statistic trees.", "Helps answer rank queries."], "Subtree size counts nodes below a node and enables augmented tree operations."),
    ("vocab-order-statistic", "Order statistic tree", "A BST augmented with subtree sizes so it can select the k-th smallest element in O(log n).", ["order statistic tree", "os tree"], ["Stores subtree counts.", "Supports select and rank queries."], "Order statistic trees keep subtree sizes to answer rank and select queries."),
    ("vocab-heapify", "Heapify", "The bottom-up process of converting an arbitrary array into a heap by sifting down non-leaf nodes.", ["heapify", "build heap"], ["Runs in linear time.", "Start from the last parent."], "Heapify rearranges an array in Θ(n) to satisfy the heap order property."),
    ("vocab-splay", "Splay tree", "A self-adjusting BST that moves accessed nodes to the root using rotations, giving amortized O(log n) operations.", ["splay", "splay tree"], ["Uses zig/zig-zig/zig-zag steps.", "Recently accessed items stay near the top."], "Splay trees adapt to access patterns by splaying accessed nodes to the root."),
    ("vocab-treap", "Treap", "A randomized BST that stores both a key and a random priority, maintaining BST order by key and heap order by priority.", ["treap", "tree heap"], ["Random priorities keep tree balanced.", "Insert rotates to restore heap order."], "Treaps combine BST and heap properties using random priorities."),
    ("vocab-internal-path-length", "Internal path length", "The sum of the depths of all internal nodes in a tree.", ["internal path length", "ipl"], ["Measures total search cost in BSTs.", "Related to average depth."], "Internal path length approximates the total work of visiting every internal node."),
]

for entry in vocab_entries:
    add_vocab(*entry)

assert sum(1 for q in questions if q["level"] == 1) >= 45


def add_short_answer(qid: str, topic: str, prompt: str, required: List[str], partial: List[str], explanation: str, hints: List[str]) -> None:
    questions.append(
        {
            "id": qid,
            "level": 2,
            "question_type": "short_answer",
            "topic": topic,
            "prompt": prompt,
            "expectedAnswer": "See explanation.",
            "expectedKeywordsRequired": required,
            "expectedKeywordsPartial": partial,
            "hints": hints,
            "explanation": explanation,
        }
    )


level2_data = [
    ("sa-nested-loop-n2", "complexity", "Consider two nested loops: the outer loop runs n times and the inner loop runs n times. What is the time complexity?", ["o(n^2)", "n^2"], ["quadratic", "nested"], "Each of the n iterations of the outer loop triggers n inner iterations, so the total work is Θ(n^2).", ["Count how many times the body executes.", "Multiplying outer and inner counts gives total work."]),
    ("sa-log-loop", "complexity", "A loop repeatedly halves n until it becomes 0. What is the time complexity?", ["o(log n)", "log n"], ["logarithmic", "halving"], "Halving each step yields ⌊log₂ n⌋ iterations, giving Θ(log n).", ["How many times can you divide n by 2?", "Logarithms count repeated halving."]),
    ("sa-triple-loop", "complexity", "Two nested loops each run n times, and an innermost loop runs 5 times regardless of n. What is the complexity?", ["o(n^2)", "n^2"], ["constant inner", "constant factor"], "The constant-time inner loop does not change growth, so the runtime stays Θ(n^2).", ["Ignore constant 5.", "Outer loops dominate."]),
    ("sa-n-log-n", "complexity", "An algorithm splits the problem in half then spends linear time merging results. What is the time complexity?", ["o(n log n)", "n log n"], ["divide and conquer", "mergesort"], "The recurrence T(n) = 2T(n/2) + Θ(n) solves to Θ(n log n).", ["Write the recurrence.", "Use the Master Theorem."]),
    ("sa-queue-use", "linear structures", "Name a realistic use case for a queue and explain why FIFO order is required.", ["fifo", "order"], ["scheduling", "breadth", "buffer"], "Queues model resources such as print jobs or BFS frontiers where the earliest arrivals must be processed first.", ["Think about fairness.", "What data structure powers BFS?"]),
    ("sa-stack-use", "linear structures", "Why are stacks a good fit for evaluating arithmetic expressions using postfix notation?", ["lifo", "operands"], ["push", "pop", "operators"], "Stacks keep the most recent operands handy so each operator pops its operands and pushes the result.", ["Consider reverse Polish notation.", "Think of the order operands are processed."]),
    ("sa-array-insert-front", "arrays", "What is the time complexity of inserting an element at the front of a dynamic array of length n?", ["o(n)", "n"], ["shift", "move"], "All n elements shift one position, so insertion at the front costs Θ(n).", ["Do you have to move other elements?", "Compare with append."]),
    ("sa-array-insert-back", "arrays", "Assuming unused capacity, what is the time complexity of appending to the end of a dynamic array?", ["o(1)", "constant"], ["amortized", "append"], "Appending is Θ(1) amortized because it only copies when resizing.", ["Consider amortized analysis.", "Most appends do no copying."]),
    ("sa-linkedlist-middle", "linked lists", "Why is inserting at the middle of a singly linked list Θ(n) even if insertion itself is O(1)?", ["traverse", "find"], ["need predecessor", "no random access"], "Finding the node before the insertion point requires linear traversal, dominating the cost.", ["How do you reach the middle node?", "What extra info do you need to insert?"]),
    ("sa-binary-search", "searching", "Binary search on a sorted array repeatedly halves the search range. State its complexity and requirement on the data.", ["o(log n)", "sorted"], ["halving", "order"], "Binary search runs in Θ(log n) but only works on data with random access arranged in sorted order.", ["What structure enables midpoints?", "Why can't it handle unsorted arrays?"]),
    ("sa-linear-vs-binary", "searching", "When would linear search be preferable to binary search even on sorted data?", ["unsorted", "small", "linked"], ["stream", "no random"], "Linear search may win on tiny arrays, streaming inputs, or linked lists where random access is expensive.", ["Consider access cost.", "What about streaming data?"]),
    ("sa-tree-height-depth", "trees", "Explain the relationship between the depth of a node and the height of the tree.", ["depth", "root", "longest"], ["levels", "distance"], "Depth counts edges from the root to a node, while height is the maximum depth among nodes (or maximum root-to-leaf path).", ["One measures downward, the other upward.", "Which one is global?"]),
    ("sa-bst-search", "trees", "Describe how BST search locates a key and why its average cost is logarithmic.", ["compare", "left", "right"], ["balanced", "height"], "BST search compares the key to the node value and recurses left or right, halving the search space when the tree is balanced so cost is Θ(log n).", ["How many children do you examine?", "What happens with balanced vs skewed trees?"]),
    ("sa-bst-skew", "trees", "What causes a BST to devolve to linear time, and how can you prevent it?", ["skew", "sorted"], ["balancing", "avl", "red-black"], "Inserting keys in sorted order creates a skewed tree of height n; self-balancing trees like AVL or red-black maintain logarithmic height.", ["Think of inserting sorted data.", "What rotations keep height small?"]),
    ("sa-heap-insert", "heaps", "Outline the steps of inserting a key into a binary heap and state the complexity.", ["bubble", "up", "o(log n)"], ["swap", "parent", "heap property"], "Insert at the end, then bubble up swapping with parents until the heap property holds, taking Θ(log n).", ["Where is the new key placed initially?", "How do you restore order?"]),
    ("sa-heapify-vs-insert", "heaps", "Compare building a heap by repeated insertions versus the heapify algorithm.", ["n log n", "linear"], ["heapify", "bottom-up"], "Individual inserts cost Θ(n log n) total, whereas heapify runs in Θ(n) by sifting down from the middle.", ["How many inserts occur?", "Why does heapify start from the middle?"]),
    ("sa-heap-sort", "heaps", "Explain why heapsort has Θ(n log n) complexity even though heapify is linear.", ["extract", "log n", "n times"], ["delete max", "heap property"], "After heapify builds the heap, heapsort performs n delete-max operations, each Θ(log n), dominating the runtime.", ["What operation repeats n times?", "What is the cost of delete-max?"]),
    ("sa-tree-traversal", "trees", "What traversal order prints BST keys in sorted order, and why?", ["in-order", "left", "right"], ["sorted", "visit"], "In-order traversal visits left subtree, node, then right, matching the BST ordering relation, so output is sorted.", ["Which traversal visits a node between its subtrees?", "How does BST order map to traversal order?"]),
    ("sa-recursion-base", "recursion", "Why must every recursive function have a base case, and what happens if it does not?", ["terminate", "stop"], ["infinite", "stack", "overflow"], "The base case halts the recursion; without it the function calls itself indefinitely until stack overflow.", ["What prevents infinite recursion?", "What error occurs if recursion never stops?"]),
    ("sa-recursion-trees", "recursion", "Explain why recursion is a natural fit for tree traversals.", ["subtree", "self-similar"], ["divide", "left", "right"], "Trees are defined recursively: each node roots smaller subtrees, so recursive functions naturally process the node then recurse on children.", ["How does a tree's definition relate to recursion?", "What does each recursive call handle?"]),
    ("sa-queue-implementation", "linear structures", "Why might a linked list implementation of a queue be preferable to an array implementation?", ["o(1)", "front", "rear"], ["no shifting", "dynamic"], "Linked queues add/remove nodes in Θ(1) without shifting or resizing, and they can grow until memory runs out.", ["What happens when array front moves?", "How does linked storage grow?"]),
    ("sa-stack-callstack", "recursion", "How does the call stack emulate a stack data structure during recursion?", ["push", "pop", "frames"], ["activation", "return"], "Each call pushes a frame storing parameters/local variables; returning pops it, mirroring stack push/pop behavior.", ["What happens when a function calls another?", "Where are return addresses stored?"]),
    ("sa-amortized-dynamic-array", "analysis", "Explain why dynamic array append has amortized O(1) cost even though occasional resizes copy many elements.", ["amortized", "spread"], ["doubling", "rare"], "Expensive resizes happen after capacity doubles, so the total cost over many appends is linear, giving O(1) amortized per append.", ["How often do resizes happen?", "What happens to unused capacity after doubling?"]),
    ("sa-graph-bfs-queue", "graphs", "Why does BFS require a queue while DFS is typically implemented with a stack or recursion?", ["fifo", "level"], ["order", "frontier"], "BFS explores level by level, needing a queue to process vertices in order of discovery, whereas DFS dives deep using stack/LIFO behavior.", ["How do BFS and DFS differ in exploration order?", "Which frontier ordering matches each?"]),
    ("sa-graph-dfs-recursion", "graphs", "What risks arise from using recursion for DFS on very deep graphs?", ["stack", "overflow"], ["depth", "recursion"], "Deep recursion may exhaust the call stack, causing stack overflow or high memory usage.", ["How much stack space does each call consume?", "What if the graph is like a linked list?"]),
    ("sa-hash-table-load", "hashing", "How does the load factor of a hash table influence performance?", ["collisions", "alpha"], ["resize", "expected"], "Higher load factors increase collisions, slowing lookups; resizing keeps the load factor below a threshold to maintain O(1) expected operations.", ["Define load factor.", "What happens when many keys share buckets?"]),
    ("sa-hash-open-addressing", "hashing", "Why does open addressing require low load factors compared to chaining?", ["clusters", "probe"], ["performance", "empty"], "Open addressing searches sequential slots during collisions; without many empty slots, probe sequences grow long, hurting performance.", ["What happens as the table fills?", "How are collisions resolved without lists?"]),
    ("sa-memory-fragmentation", "memory", "Explain how coalescing free blocks reduces external fragmentation.", ["merge", "adjacent"], ["bigger", "contiguous"], "Coalescing merges neighbors so larger contiguous blocks exist, letting future allocations succeed.", ["What stops big allocations when free space is scattered?", "What happens after combining blocks?"]),
    ("sa-call-stack-cost", "recursion", "What additional overhead does recursion impose compared to an iterative loop?", ["stack frame", "push"], ["return", "call"], "Each call pushes a new frame with parameters and locals, so recursion pays overhead in stack space and call setup/teardown time.", ["Consider activation records.", "How many frames exist simultaneously?"]),
    ("sa-tree-breadth-vs-depth", "trees", "Contrast BFS and DFS for tree traversal in terms of data structures used and memory usage.", ["queue", "stack"], ["level", "depth"], "BFS uses a queue and may store an entire level, while DFS uses a stack/recursion and stores only a path from root to leaf.", ["Which traversal stores siblings?", "Which stores only ancestors?"]),
    ("sa-avl-rotations", "trees", "Why do AVL trees perform rotations, and what triggers a rotation?", ["balance", "factor"], ["difference", "rebalance"], "When the height difference between left and right subtrees exceeds one, rotations restore balance, keeping height logarithmic.", ["Track subtree heights.", "What limit do AVL trees enforce?"]),
    ("sa-complete-tree-vs-full", "trees", "Differentiate between complete and full binary trees.", ["levels", "two children"], ["last level", "left"], "Full trees require every internal node to have two children; complete trees require nodes to be as far left as possible with all levels filled except maybe the last.", ["One property focuses on children counts.", "The other focuses on filling order."]),
    ("sa-recursion-stack-depth", "recursion", "How is the maximum recursion depth related to tree height when recursively traversing a tree?", ["height", "depth"], ["path", "call stack"], "The deepest recursive call chain equals the tree's height plus one since each level adds one frame on the stack.", ["What is the longest path you can follow?", "Each call handles one level."]),
    ("sa-priority-queue-use", "heaps", "Give an example where a priority queue beats a regular queue and explain why.", ["priority", "key"], ["scheduler", "dijkstra"], "Priority queues let you remove the highest-priority element, crucial in Dijkstra's algorithm or OS schedulers where urgency matters more than arrival time.", ["What algorithm picks the smallest tentative distance next?", "When does urgency beat arrival order?"]),
    ("sa-big-o-bounds", "analysis", "Why does stating an algorithm is O(n^2) not guarantee it ever actually takes n^2 steps?", ["upper", "bound"], ["worst", "maybe faster"], "Big-O is an upper bound; the algorithm could be faster on average but never exceed c·n^2 beyond some n.", ["Big-O ignores what part of behavior?", "Is it a tight or loose bound?"]),
    ("sa-big-theta-meaning", "analysis", "What does it mean if T(n) is Θ(n log n)?", ["upper", "lower"], ["same order", "tight"], "Θ(n log n) means T(n) grows proportionally to n log n, bounded above and below by constant multiples of n log n for large n.", ["How many bounds are given?", "Is it tight?"]),
    ("sa-omega", "analysis", "If an algorithm is Ω(n), what guarantee does that provide?", ["lower", "at least"], ["cannot be faster", "growth"], "Ω(n) ensures the runtime is at least linear beyond some n; it cannot run asymptotically faster than a constant multiple of n.", ["Think of best-case vs guaranteed minimum.", "Does Ω give an upper bound?"]),
    ("sa-fragmentation-prevention", "memory", "How do compaction or paging help mitigate external fragmentation?", ["move", "contiguous"], ["relocate", "defragment"], "Compaction relocates allocations to pack them tightly, creating large contiguous free ranges; paging uses fixed-size frames to avoid needing contiguous space.", ["What if you could move allocated blocks?", "How do fixed-size frames change the problem?"]),
    ("sa-recursion-vs-iteration", "recursion", "Give one reason to choose recursion over iteration even if both are possible.", ["clarity", "natural"], ["divide", "simplify"], "Recursion often mirrors the problem's structure (trees, divide-and-conquer), yielding clearer code even if an iterative solution exists.", ["Think of tree problems.", "Which style matches self-similar definitions?"]),
]

for entry in level2_data:
    add_short_answer(*entry)

assert sum(1 for q in questions if q["level"] == 2) >= 35

# Level 3 static examples
level3_static_inputs = [
    {
        "id": "tree-static-bst-1",
        "topic": "trees",
        "structure_kind": "BST",
        "initial_values": [30, 15, 45, 10, 20],
        "inserts": [25, 50],
        "representation": "Level-order traversal",
        "hints": ["Insert left for smaller keys, right for larger.", "Perform a breadth-first traversal after all inserts."],
        "explanation": "Start from the given BST and insert 25 under 20 then 50 to the right of 45, then list nodes level-order.",
    },
    {
        "id": "tree-static-avl-1",
        "topic": "trees",
        "structure_kind": "AVL",
        "initial_values": [20, 10, 30, 5, 14, 25],
        "inserts": [27],
        "representation": "Level-order traversal",
        "hints": ["Track balance factors after each insert.", "Use rotations when the balance exceeds one."],
        "explanation": "Inserting 27 causes a right-left imbalance at 30; rotate right at 30 then left at 20 to rebalance before listing nodes level-order.",
    },
    {
        "id": "tree-static-heap-1",
        "topic": "heaps",
        "structure_kind": "Min-heap",
        "initial_values": [8, 12, 14, 20, 30, 18],
        "inserts": [6, 11],
        "representation": "Array representation",
        "hints": ["Insert at the end then bubble up.", "Compare new elements with parents until order holds."],
        "explanation": "Insert 6 then 11, bubbling each up to maintain the min-heap; report the final array.",
    },
    {
        "id": "tree-static-heap-2",
        "topic": "heaps",
        "structure_kind": "Max-heap",
        "initial_values": [90, 70, 80, 40, 60, 30],
        "inserts": [85],
        "representation": "Array representation",
        "hints": ["Insert at end and bubble up by swapping with parent if larger.", "Remember heaps are complete trees."],
        "explanation": "After inserting 85 at the end, swap upward until the max-heap property is restored, then list the array.",
    },
]

for entry in level3_static_inputs:
    structure = entry["structure_kind"]
    if structure in {"BST", "AVL"}:
        root: Optional[Node] = None
        inserter = insert_avl if structure == "AVL" else insert_bst
        for value in entry["initial_values"]:
            root = inserter(root, value)
        for value in entry["inserts"]:
            root = inserter(root, value)
        expected = level_order(root)
    else:
        import heapq

        if structure == "Min-heap":
            heap = entry["initial_values"][:]
            heapq.heapify(heap)
            for value in entry["inserts"]:
                heapq.heappush(heap, value)
            expected = list(heap)
        else:  # Max-heap
            heap = [-v for v in entry["initial_values"]]
            heapq.heapify(heap)
            for value in entry["inserts"]:
                heapq.heappush(heap, -value)
            expected = [-v for v in heap]
    questions.append(
        {
            **entry,
            "level": 3,
            "question_type": "tree_heap",
            "representation": entry["representation"],
            "expected_representation": expected,
            "grading_representation_hint": "Provide values comma-separated in level-order.",
        }
    )

# Level 4 design questions
level4_entries = [
    ("design-two-sum", "design", "Describe an O(n) algorithm to determine whether an unsorted array contains two numbers that add to a target T.", ["hash", "set"], ["store", "complement"], "Scan once while storing seen values in a hash set; for each value x check if T-x was seen.", ["Think about complements.", "Which structure stores prior elements with O(1) lookup?"]),
    ("design-majority", "design", "How can you find a majority element (appearing > n/2 times) in linear time and constant space?", ["boyer", "moore"], ["cancel", "counter"], "Use the Boyer-Moore majority vote algorithm: cancel different elements with a counter, then verify the candidate.", ["Consider pairing eliminations.", "Only one element can survive constant-space tallying."]),
    ("design-kth-smallest", "design", "Outline how to find the k-th smallest element in a BST efficiently.", ["inorder", "k", "count"], ["traversal", "subtree"], "Use an in-order traversal counting nodes until you reach the k-th visit, or store subtree sizes to skip entire branches.", ["Which traversal yields sorted order?", "How do subtree sizes help?"]),
    ("design-range-query", "design", "Design a data structure to answer how many BST keys fall within [L, R] in O(log n) time per query.", ["augmented", "subtree", "counts"], ["store", "range", "size"], "Augment each BST node with subtree size and track counts of keys <= value to compute range counts quickly.", ["What info helps skip subtrees?", "How can prefix counts help?"]),
    ("design-min-stack", "design", "How can you support push, pop, and getMin on a stack in O(1) time?", ["aux", "stack", "min"], ["pair", "track"], "Maintain a parallel stack of running minima or store (value, currentMin) pairs so getMin returns the top's stored min.", ["Store extra data per node.", "What must you know after each push?"]),
    ("design-queue-two-stacks", "design", "Describe how to implement a queue using two stacks while keeping amortized O(1) operations.", ["two", "stacks", "transfer"], ["enqueue", "dequeue", "reverse"], "Use an inbox stack for enqueues and an outbox stack for dequeues; transfer only when the outbox is empty to keep amortized O(1).", ["How do you reverse order using stacks?", "When do you move items between stacks?"]),
    ("design-heap-merge", "design", "What data structure lets you merge two priority queues faster than O(n), and how does it work?", ["binomial", "fibonacci"], ["meld", "tree"], "Use a meldable heap such as a binomial or Fibonacci heap that links trees in logarithmic or constant amortized time.", ["Think of forest-based heaps.", "Which heaps support fast meld?"]),
    ("design-median-stream", "design", "How can you maintain the median of a stream of numbers with O(log n) updates?", ["two", "heaps"], ["max heap", "min heap"], "Keep a max-heap of the lower half and a min-heap of the upper half, rebalancing sizes so the median is at the heap tops.", ["What two structures can partition the stream?", "How do you keep their sizes balanced?"]),
    ("design-graph-toposort", "design", "Outline Kahn's algorithm for topological sorting and explain its complexity.", ["indegree", "queue"], ["remove", "zero", "edges"], "Repeatedly enqueue nodes with indegree zero, remove edges, and append nodes to the ordering; runtime is Θ(V + E).", ["Track incoming edges.", "Which nodes enter the queue?"]),
    ("design-disjoint-set", "design", "How do union by rank and path compression improve disjoint-set operations?", ["rank", "path compression"], ["flatten", "near constant"], "Union by rank attaches the smaller tree under the taller one, and path compression flattens trees during find, giving almost-constant inverse Ackermann time.", ["What happens to tree height?", "Which operations are optimized?"]),
    ("design-interval-tree", "design", "Which structure supports stabbing queries (find intervals covering a point) efficiently?", ["interval", "tree"], ["augmented", "bst"], "An interval tree augments a BST with max endpoints to skip irrelevant subtrees and answer queries in O(log n + k).", ["What metadata lets you prune subtrees?", "Which tree stores intervals as nodes?"]),
    ("design-lru-cache", "design", "Describe how to implement an LRU cache with O(1) get and put.", ["hash", "doubly", "list"], ["map", "evict", "tail"], "Combine a hash map for key lookups with a doubly linked list ordering nodes by recency; evict from the tail when capacity is exceeded.", ["Which structure keeps recency order?", "How do you find nodes quickly?"]),
    ("design-graph-dijkstra", "design", "Explain the data structures needed for Dijkstra's algorithm with a binary heap priority queue.", ["min", "heap", "dist"], ["relax", "extract", "adjacency"], "Maintain a min-heap keyed by tentative distances; repeatedly extract the smallest, relax neighbors, and update heap keys.", ["What structure selects the next vertex?", "How are edges stored?"]),
    ("design-merge-k-lists", "design", "How can you merge k sorted linked lists efficiently?", ["min", "heap", "k"], ["priority", "nodes", "log k"], "Insert the head of each list into a min-heap; repeatedly extract the smallest and push the next node from that list, giving O(n log k).", ["Which structure tracks the smallest head?", "How many elements are in the heap?"]),
    ("design-balanced-parentheses", "design", "Design an algorithm to check whether a string of parentheses, braces, and brackets is balanced.", ["stack", "push", "pop"], ["matching", "pairs", "lifo"], "Traverse characters, pushing opening symbols onto a stack and popping when matching closers appear; string is valid if stack empties and every closer matches its opener.", ["Which structure remembers opening symbols?", "How do you detect mismatched pairs?"]),
    ("design-spiral-matrix", "design", "Sketch an algorithm to print all elements of an n x n matrix in spiral order.", ["layers", "bounds"], ["top", "bottom", "left", "right"], "Maintain four boundaries (top, bottom, left, right) and traverse edges while shrinking the boundaries inward.", ["Think of peeling onions.", "Update boundaries each time you finish an edge."]),
    ("design-range-min-query", "design", "Which preprocessing technique answers range minimum queries in O(1) after O(n log n) preprocessing?", ["sparse", "table"], ["precompute", "overlapping"], "Sparse tables precompute minima for intervals of length 2^k, enabling O(1) RMQ by combining two overlapping blocks.", ["What structure stores answers for power-of-two lengths?", "How do you answer arbitrary ranges?"]),
    ("design-order-statistics-heap", "design", "How could you adapt a heap to return the median in O(log n) time without storing all elements in one heap?", ["two", "heaps", "balance"], ["max", "min", "sizes"], "Maintain both a max-heap for lower half and min-heap for upper half, rebalancing so sizes differ by at most one, allowing the median to be read from the heap roots.", ["Similar to streaming median.", "One heap holds lower values, the other higher ones."]),
    ("design-tree-diameter", "design", "Describe a linear-time algorithm to compute the diameter (longest path) of a tree.", ["two", "dfs"], ["farthest", "twice"], "Run DFS/BFS from any node to find the farthest node A, then DFS/BFS from A to find farthest node B; the path length from A to B is the diameter.", ["How can you find the farthest node?", "Why run the search twice?"]),
    ("design-top-k-stream", "design", "How do you maintain the top k largest values from a stream efficiently?", ["min", "heap", "k"], ["size", "drop", "smallest"], "Use a min-heap of size k; push new items and pop the smallest when size exceeds k.", ["Which structure discards the smallest quickly?", "Why store only k elements?"]),
    ("design-balanced-bst-sort", "design", "Explain how to use a BST to sort n distinct numbers and compare it to heapsort.", ["insert", "inorder", "o(n log n)"], ["balance", "height", "extract"], "Insert all numbers into a balanced BST then perform an in-order traversal to output them. Like heapsort, it costs Θ(n log n), but the BST yields sorted order via traversal rather than repeated delete-min.", ["What traversal prints sorted order?", "What keeps insertion cost logarithmic?"]),
    ("design-graph-bipartite", "design", "How can you test if an undirected graph is bipartite?", ["bfs", "color"], ["two", "colors", "queue"], "Perform BFS coloring with two colors; if you encounter an edge whose endpoints already share a color, the graph is not bipartite.", ["Which traversal checks neighbors level by level?", "What happens when two adjacent nodes share a color?"]),
    ("design-interval-partition", "design", "How can you schedule the minimum number of classrooms for a set of time intervals?", ["sort", "start", "end"], ["priority", "min heap", "rooms"], "Sort by start time and use a min-heap of end times to track ongoing classes; reuse rooms when the earliest ending class frees a room.", ["What structure tracks the soonest finishing interval?", "When can a class reuse a room?"]),
]

for entry in level4_entries:
    qid, topic, prompt, required, partial, explanation, hints = entry
    questions.append(
        {
            "id": qid,
            "level": 4,
            "question_type": "design",
            "topic": topic,
            "prompt": prompt,
            "expectedAnswer": "See explanation.",
            "expectedKeywordsRequired": required,
            "expectedKeywordsPartial": partial,
            "hints": hints,
            "explanation": explanation,
        }
    )

assert sum(1 for q in questions if q["level"] == 4) >= 20

with open("questions.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2)
