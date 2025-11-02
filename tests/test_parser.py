"""Tests for subtitle parser module."""

import os
import tempfile
import pytest
from pathlib import Path

from subtitle_styling.parser import SubtitleFile, scan_subtitle_files


def test_subtitle_file_creation():
    """Test creating an empty SubtitleFile."""
    subtitle = SubtitleFile()
    assert len(subtitle) == 0
    assert subtitle.filepath is None


def test_subtitle_file_load(tmp_path):
    """Test loading a subtitle file."""
    # Create a test SRT file
    srt_content = """1
00:00:01,000 --> 00:00:03,000
Hello world

2
00:00:04,000 --> 00:00:06,000
Second subtitle
"""
    srt_file = tmp_path / "test.srt"
    srt_file.write_text(srt_content, encoding='utf-8')
    
    # Load the file
    subtitle = SubtitleFile(str(srt_file))
    
    assert len(subtitle) == 2
    assert subtitle.filepath == str(srt_file)
    assert subtitle.encoding == 'utf-8' or subtitle.encoding == 'ascii'


def test_subtitle_file_save(tmp_path):
    """Test saving a subtitle file."""
    # Create a test SRT file
    srt_content = """1
00:00:01,000 --> 00:00:03,000
Hello world
"""
    input_file = tmp_path / "input.srt"
    input_file.write_text(srt_content, encoding='utf-8')
    
    # Load and save
    subtitle = SubtitleFile(str(input_file))
    output_file = tmp_path / "output.srt"
    subtitle.save(str(output_file))
    
    assert output_file.exists()
    assert len(subtitle) == 1


def test_get_text_lines(tmp_path):
    """Test getting text lines from subtitles."""
    srt_content = """1
00:00:01,000 --> 00:00:03,000
First line

2
00:00:04,000 --> 00:00:06,000
Second line
"""
    srt_file = tmp_path / "test.srt"
    srt_file.write_text(srt_content, encoding='utf-8')
    
    subtitle = SubtitleFile(str(srt_file))
    lines = subtitle.get_text_lines()
    
    assert len(lines) == 2
    assert "First line" in lines[0]
    assert "Second line" in lines[1]


def test_scan_subtitle_files(tmp_path):
    """Test scanning directory for subtitle files."""
    # Create test files
    (tmp_path / "sub1.srt").write_text("test", encoding='utf-8')
    (tmp_path / "sub2.srt").write_text("test", encoding='utf-8')
    (tmp_path / "video.mp4").write_text("test", encoding='utf-8')
    
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (subdir / "sub3.srt").write_text("test", encoding='utf-8')
    
    # Scan
    files = scan_subtitle_files(str(tmp_path))
    
    assert len(files) == 3
    assert all(f.endswith('.srt') for f in files)


def test_scan_subtitle_files_with_extensions(tmp_path):
    """Test scanning with custom extensions."""
    (tmp_path / "sub1.srt").write_text("test", encoding='utf-8')
    (tmp_path / "sub2.txt").write_text("test", encoding='utf-8')
    (tmp_path / "sub3.ass").write_text("test", encoding='utf-8')
    
    # Scan for .srt only
    files = scan_subtitle_files(str(tmp_path), extensions=['.srt'])
    assert len(files) == 1
    
    # Scan for .txt only
    files = scan_subtitle_files(str(tmp_path), extensions=['.txt'])
    assert len(files) == 1


def test_scan_nonexistent_directory():
    """Test scanning a nonexistent directory."""
    with pytest.raises(ValueError, match="Directory does not exist"):
        scan_subtitle_files("/nonexistent/path")
