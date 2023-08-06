class StringScanner:
    def __init__(self, string):
        self.string = string
        self.pointer = 0

    def scan(self, length):
        start = self.pointer
        self.pointer += length
        return self.string[start:self.pointer]

    def match(self, pattern):
        #print("match()", pattern, self.string[self.pointer:])
        return self.string[self.pointer:self.pointer + len(pattern)] == pattern

    def skip(self, length):
        self.pointer += length

    def scan_up_to(self, pattern):
        end = self.string.find(pattern, self.pointer)
        if end == -1:
            return None
        result = self.string[self.pointer:end]
        self.pointer = end + len(pattern)
        return result

def from_char(char_splitter, text):
    """
    Return the part of `text` from the position of the first `char_splitter` character
    """
    before, after = text.split(Constants.GROUP_START, 1)
    return char_splitter + after

