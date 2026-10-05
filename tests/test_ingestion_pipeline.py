import unittest
from core.rag.ingestion_pipeline import IngestionPipeline

class TestIngestionPipeline(unittest.TestCase):
    def setUp(self):
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
