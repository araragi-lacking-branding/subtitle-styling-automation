# Usage Examples

This document provides detailed examples of using the subtitle styling automation tool.

## Basic Examples

### 1. Clean a Single File

```bash
# Basic cleaning (removes tags, normalizes whitespace)
subtitle-style input.srt

# Output will be: input.styled.srt
```

### 2. Specify Output Location

```bash
subtitle-style input.srt --output cleaned.srt
```

### 3. Remove Hearing Impaired Annotations

```bash
# Remove [SOUND EFFECTS] and (descriptions)
subtitle-style input.srt --remove-hi --output clean.srt
```

## Style Guide Examples

### 4. Apply Different Styles

```bash
# Uppercase
subtitle-style input.srt --style uppercase --output UPPERCASE.srt

# Lowercase
subtitle-style input.srt --style lowercase --output lowercase.srt

# Title Case
subtitle-style input.srt --style title --output Title_Case.srt

# Sentence case
subtitle-style input.srt --style sentence --output Sentence_case.srt
```

## Directory Processing

### 5. Process All Subtitles in a Directory

```bash
# Process all .srt and .txt files
subtitle-style --directory ./subtitles --verbose
```

### 6. Process with Output to Different Directory

```bash
# Keep original structure in output directory
subtitle-style --directory ./input --output ./output --style clean
```

### 7. Process Specific File Types

```bash
# Only process .srt files
subtitle-style --directory ./subs --extensions .srt

# Process multiple extensions
subtitle-style --directory ./subs --extensions .srt .txt .sub
```

## Advanced Examples

### 8. Complete Workflow

```bash
# Extract subtitles from videos (future feature, manual for now)
# ffmpeg -i movie.mkv -map 0:2 movie.srt

# Clean and style the subtitle
subtitle-style movie.srt \
    --output movie.clean.srt \
    --style sentence \
    --remove-hi \
    --verbose
```

### 9. Batch Processing with Different Styles

```bash
# Clean version
subtitle-style --directory ./subs --output ./clean --style clean

# Uppercase version for emphasis
subtitle-style --directory ./subs --output ./upper --style uppercase

# Sentence case for readability
subtitle-style --directory ./subs --output ./sentence --style sentence
```

## Python API Examples

### 10. Basic Python Usage

```python
from subtitle_styling.parser import SubtitleFile
from subtitle_styling.styler import apply_style_guide

# Load a subtitle file
sub = SubtitleFile('input.srt')

# Apply cleaning
apply_style_guide(sub.subtitles, style='clean')

# Save
sub.save('output.srt')
```

### 11. Custom Processing

```python
from subtitle_styling.parser import SubtitleFile
from subtitle_styling.styler import SubtitleCleaner

# Load file
sub = SubtitleFile('input.srt')

# Custom processing
for item in sub.subtitles:
    # Remove tags
    item.text = SubtitleCleaner.remove_formatting_tags(item.text)
    
    # Custom replacement
    item.text = item.text.replace('colour', 'color')
    
    # Normalize
    item.text = SubtitleCleaner.normalize_whitespace(item.text)

# Save
sub.save('output.srt')
```

### 12. Batch Processing in Python

```python
from subtitle_styling.parser import scan_subtitle_files, SubtitleFile
from subtitle_styling.styler import apply_style_guide
from pathlib import Path

# Scan directory
files = scan_subtitle_files('./subtitles')

# Process each file
for filepath in files:
    sub = SubtitleFile(filepath)
    apply_style_guide(sub.subtitles, style='clean', remove_hi=True)
    
    # Save with .clean.srt extension
    path = Path(filepath)
    output = path.parent / f"{path.stem}.clean{path.suffix}"
    sub.save(str(output))
```

### 13. Working with Subtitle Text

```python
from subtitle_styling.parser import SubtitleFile

# Load file
sub = SubtitleFile('input.srt')

# Get all text lines
all_text = sub.get_text_lines()
print(f"Total lines: {len(all_text)}")

# Search for specific content
for i, text in enumerate(all_text):
    if 'important phrase' in text.lower():
        print(f"Found at subtitle {i+1}: {text}")

# Iterate over subtitles with timing
for item in sub.subtitles:
    print(f"{item.start} --> {item.end}")
    print(f"  {item.text}")
```

## Real-World Scenarios

### 14. Preparing Subtitles for Different Platforms

```bash
# YouTube-style (uppercase, no HI)
subtitle-style movie.srt \
    --output movie.youtube.srt \
    --style uppercase \
    --remove-hi

# Professional streaming (clean, sentence case)
subtitle-style movie.srt \
    --output movie.streaming.srt \
    --style sentence \
    --remove-hi

# Archive version (clean only, keep HI)
subtitle-style movie.srt \
    --output movie.archive.srt \
    --style clean
```

### 15. Educational Content

```bash
# Create teacher version (clean, easy to read)
subtitle-style lecture.srt \
    --output lecture.teacher.srt \
    --style sentence \
    --remove-hi

# Create student version (includes descriptions)
subtitle-style lecture.srt \
    --output lecture.student.srt \
    --style sentence
```

## Tips and Tricks

### Always Use Verbose Mode for Debugging

```bash
subtitle-style input.srt --verbose
```

### Preview Before Batch Processing

```bash
# Test on one file first
subtitle-style test.srt --style uppercase --verbose

# If satisfied, process directory
subtitle-style --directory ./all_subs --style uppercase
```

### Combining with Other Tools

```bash
# Extract, clean, and convert
ffmpeg -i video.mkv subtitle.srt
subtitle-style subtitle.srt --output clean.srt --style clean
# Further processing...
```
