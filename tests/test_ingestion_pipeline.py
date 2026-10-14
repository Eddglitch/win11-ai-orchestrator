import unittest
from core.rag.ingestion_pipeline import IngestionPipeline

class TestIngestionPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = IngestionPipeline()

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
        self.pipeline = IngestionPipeline(chunk_size=10, chunk_overlap=2)
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
