import unittest

class TestTrie(unittest.TestCase):
    def setUp(self):
        self.trie = Trie()
        self.words = ["apple", "app", "banana", "band", "bandana"]
        for word in self.words:
            self.trie.insert(word)

    def test_insert_and_search(self):
        """Test insertion and search of words in the Trie."""
        self.assertTrue(self.trie.search("apple"))
        self.assertTrue(self.trie.search("app"))
        self.assertTrue(self.trie.search("band"))
        self.assertFalse(self.trie.search("apples"))
        self.assertFalse(self.trie.search("bandanas"))

    def test_starts_with(self):
        """Test finding words with a given prefix."""
        self.assertEqual(sorted(self.trie.starts_with("ban")), ["banana", "band", "bandana"])
        self.assertEqual(sorted(self.trie.starts_with("app")), ["app", "apple"])
        self.assertEqual(self.trie.starts_with("xyz"), [])

    def test_empty_trie(self):
        """Test behavior of an empty Trie."""
        empty_trie = Trie()
        self.assertFalse(empty_trie.search("anything"))
        self.assertEqual(empty_trie.starts_with("any"), [])

    def test_insert_duplicate(self):
        """Test inserting duplicate words."""
        self.trie.insert("apple")
        self.assertTrue(self.trie.search("apple"))
        self.assertEqual(sorted(self.trie.starts_with("app")), ["app", "apple"])


class TestSuffixTree(unittest.TestCase):
    def setUp(self):
        self.suffix_tree = SuffixTree()
        self.text = "banana"
        self.suffix_tree.insert(self.text)

    def test_insert_and_search(self):
        """Test insertion and search of substrings in the Suffix Tree."""
        self.assertEqual(sorted(self.suffix_tree.search("ana")), [1, 3])
        self.assertEqual(self.suffix_tree.search("ban"), [0])
        self.assertEqual(self.suffix_tree.search("xyz"), [])

    def test_search_full_string(self):
        """Test searching for the full string."""
        self.assertEqual(self.suffix_tree.search("banana"), [0])

    def test_search_empty_string(self):
        """Test searching for an empty string."""
        self.assertEqual(self.suffix_tree.search(""), [])

    def test_insert_empty_string(self):
        """Test inserting an empty string."""
        empty_suffix_tree = SuffixTree()
        empty_suffix_tree.insert("")
        self.assertEqual(empty_suffix_tree.search(""), [])

    def test_insert_and_search_single_character(self):
        """Test inserting and searching a single character."""
        single_char_tree = SuffixTree()
        single_char_tree.insert("a")
        self.assertEqual(single_char_tree.search("a"), [0])
        self.assertEqual(single_char_tree.search("b"), [])

    def test_collect_positions(self):
        """Test the helper function _collect_positions."""
        node = self.suffix_tree.tree
        for char in "ana":
            node = node[char]
        positions = self.suffix_tree._collect_positions(node)
        self.assertEqual(sorted(positions), [1, 3])

    def test_insert_and_search_with_special_characters(self):
        """Test inserting and searching strings with special characters."""
        special_tree = SuffixTree()
        special_tree.insert("a!b@c#")
        self.assertEqual(special_tree.search("!b"), [1])
        self.assertEqual(special_tree.search("xyz"), [])

    def test_insert_and_search_unicode(self):
        """Test inserting and searching strings with Unicode characters."""
        unicode_tree = SuffixTree()
        unicode_tree.insert("café")
        self.assertEqual(unicode_tree.search("afé"), [1])
        self.assertEqual(unicode_tree.search("é"), [3])
        self.assertEqual(unicode_tree.search("xyz"), [])


if __name__ == "__main__":
    unittest.main()
