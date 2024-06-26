import pytest
from pathlib import Path
from main import process_scenario, MarkdownOutputStrategy

def test_process_scenario(example_json_path, tmp_path):
    output_path = tmp_path / "output.txt"
    process_scenario(example_json_path, MarkdownOutputStrategy())
    output_path = example_json_path.parent / (example_json_path.stem + "_output.txt")
    assert output_path.exists()
    content = output_path.read_text(encoding="utf-8")
    assert "Example Scenario" in content
