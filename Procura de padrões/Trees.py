class Trie:
    """
    Trie implementation for storing and searching strings.
    """
    def __init__(self):
        self.trie = {}

    def insert(self, word):
        """
        Insert a word into the Trie.
        """
        current = self.trie
        for char in word + "$":  # Add end marker to indicate the end of a word
            if char not in current:
                current[char] = {}
            current = current[char]

    def search(self, word):
        """
        Check if a word exists in the Trie.
        """
        current = self.trie
        for char in word:
            if char not in current:
                return False
            current = current[char]
        return "$" in current  # Word exists if end marker is present

    def starts_with(self, prefix):
        """
        Find all words in the Trie that start with a given prefix.
        """
        current = self.trie
        for char in prefix:
            if char not in current:
                return []  # Return empty list if prefix not found
            current = current[char]
        return self._collect_words(prefix, current)

    def _collect_words(self, prefix, node):
        """
        Helper function to collect all words starting from a given node.
        """
        words = []
        for char, child in node.items():
            if char == "$":
                words.append(prefix)
            else:
                words.extend(self._collect_words(prefix + char, child))
        return words


class SuffixTree:
    """
    Suffix Tree implementation for storing and searching substrings.
    """
    def __init__(self):
        self.tree = {}

    def insert(self, text):
        """
        Insert all suffixes of a string into the Suffix Tree.
        """
        if text == "":
            # Handle empty string case explicitly
            current = self.tree
            if "$" not in current:
                current["$"] = {}
            if "index" not in current["$"]:
                current["$"]["index"] = []
            current["$"]["index"].append(0)
            return

        for i in range(len(text)):
            self._insert_suffix(text[i:], i)

    def _insert_suffix(self, suffix, index):
        """
        Helper function to insert a suffix into the tree.
        """
        current = self.tree
        for char in suffix + "$":  # Add end marker to indicate the end of a suffix
            if char not in current:
                current[char] = {}
            current = current[char]
            if char == "$":
                if "index" not in current:
                    current["index"] = []
                if index not in current["index"]:  # Avoid duplicate indices
                    current["index"].append(index)

    def search(self, substring):
        """
        Find all positions of a substring in the Suffix Tree.
        """
        if substring == "":
            return []  # Return empty list for empty query

        current = self.tree
        for char in substring:
            if char not in current:
                return []  # Return empty list if substring not found
            current = current[char]
        return self._collect_positions(current)

    def _collect_positions(self, node):
        """
        Helper function to collect all positions from a given node.
        """
        positions = []
        for key, child in node.items():
            if key == "index":
                positions.extend(child)
            elif isinstance(child, dict):
                positions.extend(self._collect_positions(child))
        return sorted(positions)  # Sort positions for consistent test results


# Example Usage
if __name__ == "__main__":
    # Trie Example
    print("=== Trie Example ===")
    trie = Trie()
    words = ["apple", "app", "banana", "band", "bandana"]
    for word in words:
        trie.insert(word)

    print("Search 'app':", trie.search("app"))  # True
    print("Search 'apple':", trie.search("apple"))  # True
    print("Search 'apples':", trie.search("apples"))  # False
    print("Words starting with 'ban':", trie.starts_with("ban"))  # ['banana', 'band', 'bandana']

    # Suffix Tree Example
    print("\n=== Suffix Tree Example ===")
    suffix_tree = SuffixTree()
    text = "banana"
    suffix_tree.insert(text)

    print("Search 'ana':", suffix_tree.search("ana"))  # [1, 3]
    print("Search 'ban':", suffix_tree.search("ban"))  # [0]
    print("Search 'xyz':", suffix_tree.search("xyz"))  # []
