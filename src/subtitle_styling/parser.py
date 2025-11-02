"""Subtitle parser and writer for various subtitle formats."""

import os
import pysrt
import chardet
from typing import List, Optional
from pathlib import Path


class SubtitleFile:
    """Represents a subtitle file with parsing and writing capabilities."""
    
    def __init__(self, filepath: Optional[str] = None):
        """Initialize SubtitleFile.
        
        Args:
            filepath: Path to subtitle file to load
        """
        self.filepath = filepath
        self.subtitles = pysrt.SubRipFile()
        self.encoding = 'utf-8'
        
        if filepath and os.path.exists(filepath):
            self.load(filepath)
    
    def load(self, filepath: str) -> None:
        """Load subtitle file with automatic encoding detection.
        
        Args:
            filepath: Path to subtitle file
        """
        self.filepath = filepath
        
        # Detect encoding
        with open(filepath, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            self.encoding = result['encoding'] or 'utf-8'
        
        # Load subtitles
        self.subtitles = pysrt.open(filepath, encoding=self.encoding)
    
    def save(self, filepath: Optional[str] = None, encoding: str = 'utf-8') -> None:
        """Save subtitle file.
        
        Args:
            filepath: Output path (uses original if not specified)
            encoding: Output encoding (default: utf-8)
        """
        output_path = filepath or self.filepath
        if not output_path:
            raise ValueError("No filepath specified for saving")
        
        self.subtitles.save(output_path, encoding=encoding)
    
    def get_text_lines(self) -> List[str]:
        """Get all subtitle text lines.
        
        Returns:
            List of subtitle text lines
        """
        return [sub.text for sub in self.subtitles]
    
    def __len__(self) -> int:
        """Return number of subtitle entries."""
        return len(self.subtitles)
    
    def __iter__(self):
        """Iterate over subtitle entries."""
        return iter(self.subtitles)


def scan_subtitle_files(directory: str, extensions: Optional[List[str]] = None) -> List[str]:
    """Scan directory for subtitle files.
    
    Args:
        directory: Directory path to scan
        extensions: List of file extensions to look for (default: ['.srt', '.txt'])
    
    Returns:
        List of subtitle file paths
    """
    if extensions is None:
        extensions = ['.srt', '.txt']
    
    subtitle_files = []
    directory_path = Path(directory)
    
    if not directory_path.exists():
        raise ValueError(f"Directory does not exist: {directory}")
    
    for ext in extensions:
        subtitle_files.extend(str(p) for p in directory_path.rglob(f"*{ext}"))
    
    return sorted(subtitle_files)
