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


    def test_create_chunks_basic(self):
        self.pipeline = IngestionPipeline(chunk_size=10, chunk_overlap=2)
        self.metadata = {"test": "metadata"}
        # chunk_size=10, chunk_overlap=2 -> step = 8
        # "0123456789012345" (16 chars)
        # chunk 1: text[0:10] -> "0123456789"
        # chunk 2: text[8:18] -> "89012345"
        text = "0123456789012345"
        chunks = self.pipeline.create_chunks(text, self.metadata)

        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[0]["content"], "0123456789")
        self.assertEqual(chunks[1]["content"], "89012345")
        self.assertEqual(chunks[0]["length"], 10)
        self.assertEqual(chunks[1]["length"], 8)

    def test_create_chunks_overlap(self):
        self.pipeline = IngestionPipeline(chunk_size=10, chunk_overlap=2)
        self.metadata = {"test": "metadata"}
        # step = 8
        # "ABCDEFGHIJK" (11 chars)
        # chunk 1: text[0:10] -> "ABCDEFGHIJ"
        # chunk 2: text[8:18] -> "IJ K" -> "IJK"
        text = "ABCDEFGHIJK"
        chunks = self.pipeline.create_chunks(text, self.metadata)

        self.assertEqual(len(chunks), 2)
        # The overlap is "IJ" which is at indices 8 and 9
        self.assertTrue(chunks[1]["content"].startswith(chunks[0]["content"][-2:]))
        self.assertEqual(chunks[0]["content"][-2:], "IJ")
        self.assertEqual(chunks[1]["content"][:2], "IJ")

    def test_create_chunks_short_text(self):
        text = "short"
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


    def test_get_metadata_valid_path(self):
        # Setup a known DEV_HOME for testing
        original_dev_home = self.pipeline.dev_home
        self.pipeline.dev_home = os.path.abspath(".")

        # Test a valid file inside DEV_HOME
        test_file = os.path.join(self.pipeline.dev_home, "core/rag/ingestion_pipeline.py")
        metadata = self.pipeline.get_metadata(test_file)

        self.assertEqual(metadata["source"], "core/rag/ingestion_pipeline.py")
        self.assertEqual(metadata["ecosystem"], "win11-ai-orchestrator")

        # Restore DEV_HOME
        self.pipeline.dev_home = original_dev_home

    def test_get_metadata_path_traversal(self):
        # Setup a known DEV_HOME for testing
        original_dev_home = self.pipeline.dev_home
        self.pipeline.dev_home = os.path.abspath(".")

        # Test an invalid file outside DEV_HOME using path traversal
        traversal_file = "../../etc/passwd"

        with self.assertRaises(ValueError) as context:
            self.pipeline.get_metadata(traversal_file)

        self.assertTrue("Path traversal detected" in str(context.exception))

        # Test an absolute path outside DEV_HOME
        absolute_file = "/etc/passwd"

        with self.assertRaises(ValueError) as context:
            self.pipeline.get_metadata(absolute_file)

        self.assertTrue("Path traversal detected" in str(context.exception))

        # Restore DEV_HOME
        self.pipeline.dev_home = original_dev_home

if __name__ == '__main__':
    def test_clean_content_python_normalization(self):
        text = "def hello():\n\n\n\n    print('world')"
        expected = "def hello():\n\n    print('world')"
        self.assertEqual(self.pipeline.clean_content(text, ".py"), expected)

    def test_clean_content_js_normalization(self):
        text = "function hello() {\n\n \n\n    console.log('world');\n}"
        expected = "function hello() {\n\n    console.log('world');\n}"
        self.assertEqual(self.pipeline.clean_content(text, ".js"), expected)

    def test_clean_content_ts_normalization(self):
        text = "const x: number = 1;\n\n\n\nconst y: number = 2;"
        expected = "const x: number = 1;\n\nconst y: number = 2;"
        self.assertEqual(self.pipeline.clean_content(text, ".ts"), expected)

    def test_clean_content_ps1_normalization(self):
        text = "Write-Host 'Hello'\n\n\n\nWrite-Host 'World'"
        expected = "Write-Host 'Hello'\n\nWrite-Host 'World'"
        self.assertEqual(self.pipeline.clean_content(text, ".ps1"), expected)

    def test_clean_content_txt_no_normalization(self):
        text = "This is a text file.\n\n\n\nNo normalization here."
        expected = "This is a text file.\n\n\n\nNo normalization here."
        self.assertEqual(self.pipeline.clean_content(text, ".txt"), expected)

    def test_clean_content_stripping(self):
        text = "   \n  Hello World  \n   "
        expected = "Hello World"
        self.assertEqual(self.pipeline.clean_content(text, ".txt"), expected)
        self.assertEqual(self.pipeline.clean_content(text, ".py"), expected)

    def test_clean_content_empty_string(self):
        self.assertEqual(self.pipeline.clean_content("", ".py"), "")

    def test_clean_content_whitespace_only(self):
        self.assertEqual(self.pipeline.clean_content("   \n   ", ".js"), "")
        # Set small chunk_size and chunk_overlap to test the logic easily
        self.metadata = {"source": "test_file.py"}

    def test_create_chunks_exact_size(self):
        text = "0123456789"  # length 10
        chunks = self.pipeline.create_chunks(text, self.metadata)

        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0]["content"], "0123456789")
        self.assertEqual(chunks[0]["metadata"], self.metadata)
        self.assertEqual(chunks[0]["length"], 10)

    def test_create_chunks_with_overlap(self):
        # text length 18, step is 8
        # i=0: "0123456789"
        # i=8: "89abcdefgh"
        text = "0123456789abcdefgh"
        chunks = self.pipeline.create_chunks(text, self.metadata)

        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[0]["content"], "0123456789")
        self.assertEqual(chunks[0]["length"], 10)
        self.assertEqual(chunks[1]["content"], "89abcdefgh")
        self.assertEqual(chunks[1]["length"], 10)

    def test_create_chunks_shorter_than_size(self):
        text = "short"  # length 5
        chunks = self.pipeline.create_chunks(text, self.metadata)

        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0]["content"], "short")
        self.assertEqual(chunks[0]["length"], 5)

    def test_create_chunks_empty_text(self):
        text = ""
        chunks = self.pipeline.create_chunks(text, self.metadata)

        # Current implementation: range(0, 0, 8) is empty
        self.assertEqual(len(chunks), 0)

    def test_create_chunks_metadata(self):
        text = "some text to chunk"
        chunks = self.pipeline.create_chunks(text, self.metadata)

        for chunk in chunks:
            self.assertEqual(chunk["metadata"], self.metadata)
        text = ""  # length 0
        chunks = self.pipeline.create_chunks(text, self.metadata)

        self.assertEqual(len(chunks), 0)

    def test_create_chunks_multiple_overlaps(self):
        # step is 2
        # i=0: "0123"
        # i=2: "2345"
        # i=4: "4567"
        pipeline = IngestionPipeline(chunk_size=4, chunk_overlap=2)
        text = "01234567"  # length 8
        chunks = pipeline.create_chunks(text, self.metadata)

        self.assertEqual(len(chunks), 3)
        self.assertEqual(chunks[0]["content"], "0123")
        self.assertEqual(chunks[1]["content"], "2345")
        self.assertEqual(chunks[2]["content"], "4567")

    def test_clean_content_code_files(self):
        """Test whitespace normalization for code files (.py, .js, .ts, .ps1)"""
        text = "def foo():\n\n\n\n    pass\n \n\ndef bar():\n    pass"
        pipeline = IngestionPipeline()

        for ext in [".py", ".js", ".ts", ".ps1"]:
            cleaned = pipeline.clean_content(text, ext)
            self.assertEqual(cleaned, "def foo():\n\n    pass\n\ndef bar():\n    pass")

    def test_clean_content_general_stripping(self):
        """Test general leading/trailing whitespace stripping logic."""
        text = "   some content \n\n"
        pipeline = IngestionPipeline()
        self.assertEqual(pipeline.clean_content(text, ".txt"), "some content")

if __name__ == "__main__":
    unittest.main()
