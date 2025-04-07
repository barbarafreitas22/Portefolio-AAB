class BWT:
    """
    Simplified implementation of Burrows-Wheeler Transform algorithm
    """
    def __init__(self, text=""):
        """Initialize with an optional text to encode"""
        if text:
            if "$" not in text:
                text += "$"  # Ensure the text has an end marker
            self.original_text = text
            self.bwt, self.suffix_array = self.encode(text)
        else:
            self.original_text = ""
            self.bwt = ""
            self.suffix_array = []
            
    def encode(self, text):
        """
        Encode a string using Burrows-Wheeler Transform
        Returns the BWT string and the suffix array
        """
        # Create all rotations of the text
        rotations = []
        for i in range(len(text)):
            rotations.append((text[i:] + text[:i], i))
            
        # Sort the rotations
        sorted_rotations = sorted(rotations)
        
        # Extract the last character of each rotation to form BWT
        bwt = "".join(rotation[0][-1] for rotation in sorted_rotations)
        
        # Create suffix array
        suffix_array = [rotation[1] for rotation in sorted_rotations]
        
        return bwt, suffix_array
    
    def decode(self, bwt=None):
        """
        Decode the BWT string back to the original text
        """
        if bwt is None:
            bwt = self.bwt
            
        n = len(bwt)
        if n == 0:
            return ""
            
        # Initialize the table with empty strings
        table = [""] * n
        
        # Build the table iteratively
        for _ in range(n):
            # Prepend BWT characters to the existing table rows
            table = sorted([bwt[i] + table[i] for i in range(n)])
            
        # Find the row ending with '$' which is the original text
        for row in table:
            if row.endswith("$"):
                return row
                
        return ""
    
    def find_occurrences(self, pattern):
        """
        Find all occurrences of a pattern in the original text using BWT
        Returns a list of starting positions
        """
        if not pattern or not self.bwt:
            return []
            
        # Get first column (sorted BWT)
        first_column = sorted(self.bwt)
        
        # Build the Last-to-First mapping
        last_to_first = self._build_last_to_first_mapping(first_column)
        
        # Initialize top and bottom pointers
        top = 0
        bottom = len(self.bwt) - 1
        
        # Process pattern from right to left
        i = len(pattern) - 1
        while top <= bottom and i >= 0:
            char = pattern[i]
            
            # Check if character exists in the current range
            found = False
            for j in range(top, bottom + 1):
                if self.bwt[j] == char:
                    found = True
                    break
                    
            if not found:
                return []  # No match
                
            # Calculate new top and bottom
            new_top = None
            new_bottom = None
            
            for j in range(top, bottom + 1):
                if self.bwt[j] == char:
                    if new_top is None:
                        new_top = last_to_first[j]
                    new_bottom = last_to_first[j]
            
            top = new_top
            bottom = new_bottom + (self.bwt[top:bottom+1].count(char) - 1)
            i -= 1
            
        # Convert to original positions using suffix array
        result = []
        for i in range(top, bottom + 1):
            result.append(self.suffix_array[i])
            
        return sorted(result)
    
    def _build_last_to_first_mapping(self, first_column):
        """Build the Last-to-First column mapping"""
        mapping = []
        
        for i, char in enumerate(self.bwt):
            # Count occurrences of this character before position i
            count = self.bwt[:i].count(char)
            
            # Find the corresponding position in first column
            pos = 0
            found = 0
            while found <= count:
                if first_column[pos] == char:
                    found += 1
                if found > count:
                    break
                pos += 1
                
            mapping.append(pos)
            
        return mapping

if __name__ == "__main__":
    # Test with example string
    test_string = "ACGTACGT$"
    
    # Encode
    bwt = BWT(test_string)
    print(f"Original text: {test_string}")
    print(f"BWT: {bwt.bwt}")
    print(f"Suffix Array: {bwt.suffix_array}")
    
    # Decode
    decoded = bwt.decode()
    print(f"Decoded text: {decoded}")
    print(f"Correctly decoded: {decoded == test_string}")
    
    # Pattern matching
    pattern = "ACG"
    occurrences = bwt.find_occurrences(pattern)
    print(f"Occurrences of '{pattern}': {occurrences}")
