import filecmp
import os
import tempfile
import unittest
from unittest.mock import patch

import garmin_ace
from garmin_ace.convert import OrgFileHandler, AceFileHandler, HtmlFileHandler, \
                               get_handler_for_file, get_supported_formats

class TestFileHandler(unittest.TestCase):
    handlers = [OrgFileHandler, AceFileHandler, HtmlFileHandler]

    def test_get_handler_for_file(self):

        handler = get_handler_for_file("test.org", self.handlers)
        self.assertIsInstance(handler, OrgFileHandler)

        handler = get_handler_for_file("test.ace", self.handlers)
        self.assertIsInstance(handler, AceFileHandler)

        handler = get_handler_for_file("test.html", self.handlers)
        self.assertIsInstance(handler, HtmlFileHandler)

        with self.assertRaises(ValueError):
            get_handler_for_file("test.unknown", self.handlers)

    def test_get_supported_formats(self):
        import_formats, export_formats = get_supported_formats(self.handlers)
        
        self.assertIn(".org", import_formats)
        self.assertIn(".ace", import_formats)
        self.assertIn(".ace", export_formats)
        self.assertIn(".html", export_formats)

    @patch.object(OrgFileHandler, 'import_file')
    @patch.object(AceFileHandler, 'export_file')
    def test_main(self, mock_export_file, mock_import_file):
        test_args = ["ace-convert", "test.org", "test.ace"]
        with patch.object(garmin_ace.convert.sys, 'argv', test_args):
            garmin_ace.convert.main()
        
        mock_import_file.assert_called_once_with("test.org")
        mock_export_file.assert_called_once_with(mock_import_file.return_value, "test.ace")

class TestConvertion(unittest.TestCase):

    def test_convert_org_ace(self):
        tmp_file = tempfile.NamedTemporaryFile(suffix='.ace', delete=False)

        test_args = ["ace-convert", 'data/pa18.org', tmp_file.name]
        with patch.object(garmin_ace.convert.sys, 'argv', test_args):
            garmin_ace.convert.main()

        self.assertTrue(filecmp.cmp('data/pa18.ace', tmp_file.name, shallow=False))
        os.unlink(tmp_file.name)
class TestConvertion(unittest.TestCase):

    def test_convert_org_ace(self):
        tmp_file = tempfile.NamedTemporaryFile(suffix='.ace', delete=False)

        test_args = ["ace-convert", 'data/pa18.org', tmp_file.name]
        with patch.object(garmin_ace.convert.sys, 'argv', test_args):
            garmin_ace.convert.main()

        self.assertTrue(filecmp.cmp('data/pa18.ace', tmp_file.name, shallow=False))
        os.unlink(tmp_file.name)

    def test_convert_org_html(self):
        tmp_file = tempfile.NamedTemporaryFile(suffix='.html', delete=False)

        test_args = ["ace-convert", 'data/pa18.org', tmp_file.name]
        with patch.object(garmin_ace.convert.sys, 'argv', test_args):
            garmin_ace.convert.main()

        self.assertTrue(filecmp.cmp('data/pa18.html', tmp_file.name, shallow=False))
        os.unlink(tmp_file.name)

    def test_convert_ace_ace(self):
        tmp_file = tempfile.NamedTemporaryFile(suffix='.ace', delete=False)

        test_args = ["ace-convert", 'data/pa18.ace', tmp_file.name]
        with patch.object(garmin_ace.convert.sys, 'argv', test_args):
            garmin_ace.convert.main()

        self.assertTrue(filecmp.cmp('data/pa18.ace', tmp_file.name, shallow=False))
        os.unlink(tmp_file.name)

    def test_convert_ace_html(self):
        tmp_file = tempfile.NamedTemporaryFile(suffix='.html', delete=False)

        test_args = ["ace-convert", 'data/pa18.ace', tmp_file.name]
        with patch.object(garmin_ace.convert.sys, 'argv', test_args):
            garmin_ace.convert.main()

        self.assertTrue(filecmp.cmp('data/pa18.html', tmp_file.name, shallow=False))
        os.unlink(tmp_file.name)


if __name__ == "__main__":
    unittest.main()

