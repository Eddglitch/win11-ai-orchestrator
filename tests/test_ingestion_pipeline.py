import unittest
from core.rag.ingestion_pipeline import IngestionPipeline

class TestIngestionPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = IngestionPipeline(chunk_size=10, chunk_overlap=2)
        self.metadata = {"test": "metadata"}

    def test_create_chunks_basic(self):
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

if __name__ == "__main__":
    unittest.main()
