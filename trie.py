
def char_to_idx(char: str):
    return ord(char) - 97


class TrieNode:

    def __init__(self, key=""):
        self.key = key
        self.last_char = None if len(key) == 0 else key[-1]
        self.children = [None] * 26
        self.fail = self
        self.parent = None
        self.terminal = False

    def __getitem__(self, char: str) -> 'TrieNode':
        return self.children[char_to_idx(char)]

    def __setitem__(self, char: str, value: int):
        self.children[char_to_idx(char)] = value

    def __repr__(self) -> str:
        return self.key if len(self.key) > 0 else "ε"


class Trie:

    def __init__(self):
        self.root = TrieNode()
        self.nodes: list[TrieNode] = [self.root]

    def insert_key(self, key):
        current = self.root
        current_idx = 0
        l = 0

        while l < len(key):
            next_idx = current[key[l]]
            if next_idx is not None:
                current_idx = next_idx
                current = self.nodes[current_idx]
                l += 1
            else:
                next_idx = len(self.nodes)
                next = TrieNode(key=key[:l+1])
                self.nodes.append(next)

                current[key[l]] = next_idx
                next.parent = current

                current = next
                current_idx = next_idx
                l += 1

        current.terminal = True
        return current_idx
    
    def link_suffixes(self):
        queue = [self.root]

        while len(queue) > 0:
            current = queue.pop(0)

            # add not None children to the end of the queue
            for child in current.children:
                if child is not None:
                    queue.append(self.nodes[child])

            # skip root from linking fail
            if current is self.root: 
                continue

            # link direct children of root back to root
            if current.parent is self.root:
                current.fail = self.root
                continue

            # link rest of nodes
            last_char = current.last_char
            suffix = current.parent.fail
            while True:
                if suffix[last_char] is not None:
                    break
                if suffix is self.root:
                    break
                suffix = suffix.fail

            if suffix[last_char] is None:
                current.fail = suffix # suffix here is actually root
            else:
                current.fail = self.nodes[suffix[last_char]]

    def fail(self, node: TrieNode) -> TrieNode:
        return node.fail
    
    def go(self, node: TrieNode, char: str) -> TrieNode:
        next = node[char]
        if next is None:
            if node is self.root:
                return self.root
            else:
                return None
        else:
            return self.nodes[next]