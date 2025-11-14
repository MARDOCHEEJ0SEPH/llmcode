"""Tests for tool system"""

import pytest
import tempfile
from pathlib import Path
from llmcode.tools.file_tools import ReadTool, WriteTool, EditTool
from llmcode.tools.bash_tool import BashTool
from llmcode.tools.base import ToolStatus


class TestReadTool:
    """Tests for ReadTool"""

    def test_read_existing_file(self):
        """Test reading an existing file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Line 1\nLine 2\nLine 3\n")
            temp_file = f.name

        try:
            tool = ReadTool()
            result = tool.execute(temp_file)

            assert result.status == ToolStatus.SUCCESS
            assert "Line 1" in result.output
            assert "Line 2" in result.output
            assert "Line 3" in result.output
        finally:
            Path(temp_file).unlink()

    def test_read_nonexistent_file(self):
        """Test reading a file that doesn't exist"""
        tool = ReadTool()
        result = tool.execute("/nonexistent/file.txt")

        assert result.status == ToolStatus.ERROR
        assert "not found" in result.error.lower()


class TestWriteTool:
    """Tests for WriteTool"""

    def test_write_file(self):
        """Test writing a file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.txt"

            tool = WriteTool()
            result = tool.execute(str(file_path), "Hello, World!")

            assert result.status == ToolStatus.SUCCESS
            assert file_path.exists()
            assert file_path.read_text() == "Hello, World!"


class TestEditTool:
    """Tests for EditTool"""

    def test_edit_file(self):
        """Test editing a file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Hello, World!")
            temp_file = f.name

        try:
            tool = EditTool()
            result = tool.execute(temp_file, "World", "Python")

            assert result.status == ToolStatus.SUCCESS
            assert Path(temp_file).read_text() == "Hello, Python!"
        finally:
            Path(temp_file).unlink()

    def test_edit_string_not_found(self):
        """Test editing when string doesn't exist"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Hello, World!")
            temp_file = f.name

        try:
            tool = EditTool()
            result = tool.execute(temp_file, "Python", "Java")

            assert result.status == ToolStatus.ERROR
            assert "not found" in result.error.lower()
        finally:
            Path(temp_file).unlink()


class TestBashTool:
    """Tests for BashTool"""

    def test_simple_command(self):
        """Test running a simple command"""
        tool = BashTool()
        result = tool.execute("echo 'Hello, World!'")

        assert result.status == ToolStatus.SUCCESS
        assert "Hello, World!" in result.output

    def test_failed_command(self):
        """Test running a command that fails"""
        tool = BashTool()
        result = tool.execute("exit 1")

        assert result.status == ToolStatus.WARNING
        assert result.metadata["return_code"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
