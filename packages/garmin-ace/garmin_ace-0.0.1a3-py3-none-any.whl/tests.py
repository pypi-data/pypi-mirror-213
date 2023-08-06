import unittest
import os
import filecmp

from decoder import ACEFileDecoder
from encoder import ACEFileEncoder

class TestACEFileDecoderEncoder(unittest.TestCase):
    def test_decoding_encoding(self):
        original_file_path = 'data/checklist.ace'
        tmp_file_path = '/tmp/temp.ace'

        checklist = ACEFileDecoder.read_from_file(original_file_path)

        encoder = ACEFileEncoder(checklist)
        encoder.write_to_file(tmp_file_path)

        # Check that the original file and the re-encoded file are identical
        self.assertTrue(filecmp.cmp(original_file_path, tmp_file_path, shallow=False))

        os.remove(tmp_file_path)


if __name__ == '__main__':
    unittest.main()

