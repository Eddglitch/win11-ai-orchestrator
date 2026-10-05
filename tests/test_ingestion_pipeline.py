import unittest
from core.rag.ingestion_pipeline import IngestionPipeline

class TestIngestionPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = IngestionPipeline()

    def test_clean_content_empty_string(self):
        """Test that empty strings are handled correctly."""
        self.assertEqual(self.pipeline.clean_content("", ".py"), "")
        self.assertEqual(self.pipeline.clean_content("   ", ".py"), "")

    def test_clean_content_unsupported_extension(self):
        """Test that normalization is not applied to unsupported extensions."""
        text = "line1\n\n\nline2"
        # .txt is not in the supported list for normalization
        expected = "line1\n\n\nline2"
        self.assertEqual(self.pipeline.clean_content(text, ".txt"), expected)

    def test_clean_content_supported_extension_normalization(self):
        """Test that multiple blank lines are reduced to double blank lines for supported extensions."""
        extensions = ['.py', '.js', '.ts', '.ps1']
        for ext in extensions:
            text = "line1\n\n\n\nline2"
            expected = "line1\n\nline2"
            self.assertEqual(self.pipeline.clean_content(text, ext), expected, f"Failed for {ext}")

            text_with_spaces = "line1\n \n \nline2"
            expected_with_spaces = "line1\n\nline2"
            self.assertEqual(self.pipeline.clean_content(text_with_spaces, ext), expected_with_spaces, f"Failed for {ext} with spaces")

    def test_clean_content_strip_whitespace(self):
        """Test that leading and trailing whitespace is stripped."""
        self.assertEqual(self.pipeline.clean_content("  hello  ", ".py"), "hello")
        self.assertEqual(self.pipeline.clean_content("\nhello\n", ".js"), "hello")

    def test_clean_content_none_extension(self):
        """Test handling of None as extension (should not crash, just strip)."""
        # Though the type hint says str, it's good to be robust or at least know behavior.
        # In the current code, 'extension in [...]' will work if extension is None if it's not in the list.
        # But if it's None, it might raise TypeError if compared with list of strings?
        # Actually in Python: None in ['.py'] is False.
        self.assertEqual(self.pipeline.clean_content("  text  ", None), "text")

if __name__ == '__main__':
    unittest.main()
