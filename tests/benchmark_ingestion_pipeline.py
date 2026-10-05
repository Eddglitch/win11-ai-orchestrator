import timeit
import re
import sys
import os

# Add the root directory to sys.path to import core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.rag.ingestion_pipeline import IngestionPipeline

def benchmark_clean_content():
    pipeline = IngestionPipeline()
    test_text = "line1\n\n   \nline2\n\n\nline3\n" * 100
    extension = ".py"

    # Warm up
    pipeline.clean_content(test_text, extension)

    number = 10000
    timer = timeit.Timer(lambda: pipeline.clean_content(test_text, extension))
    result = timer.timeit(number=number)

    print(f"Mean execution time over {number} iterations: {result/number:.10f} seconds")

if __name__ == "__main__":
    benchmark_clean_content()
