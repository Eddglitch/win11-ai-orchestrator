import unittest
import sys
import os

# Add the root directory to sys.path to import core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.rag.ingestion_pipeline import IngestionPipeline

class TestIngestionPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = IngestionPipeline()

    def test_clean_content_python(self):
        input_text = "line1\n\n   \nline2\n\n\nline3\n"
        expected_output = "line1\n\nline2\n\nline3"
        self.assertEqual(self.pipeline.clean_content(input_text, ".py"), expected_output)

    def test_clean_content_js(self):
        input_text = "const x = 1;\n\n\nconst y = 2;"
        expected_output = "const x = 1;\n\nconst y = 2;"
        self.assertEqual(self.pipeline.clean_content(input_text, ".js"), expected_output)

    def test_clean_content_other_extension(self):
        input_text = "  hello world  \n\n\n  "
        expected_output = "hello world"
        # For non-code extensions, it should just strip
        self.assertEqual(self.pipeline.clean_content(input_text, ".txt"), expected_output)

    def test_clean_content_empty(self):
        self.assertEqual(self.pipeline.clean_content("", ".py"), "")
        self.assertEqual(self.pipeline.clean_content("   ", ".py"), "")

if __name__ == "__main__":
    unittest.main()
