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

if __name__ == "__main__":
    unittest.main()
