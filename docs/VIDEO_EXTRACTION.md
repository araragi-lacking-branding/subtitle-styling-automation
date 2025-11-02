# Subtitle Video Extraction (Future Enhancement)

This document outlines how to extract subtitles from video files. This functionality is planned for a future release.

## Overview

To extract subtitles from video files, we'll need to use ffmpeg. The implementation will support:

- Extracting embedded subtitle tracks
- Multiple subtitle formats (SRT, ASS, VTT, etc.)
- Selecting specific subtitle tracks by language
- Batch extraction from multiple video files

## Requirements

Users will need to install ffmpeg separately:

### Windows
```bash
# Download from https://ffmpeg.org/download.html
# Or use chocolatey:
choco install ffmpeg
```

### macOS
```bash
brew install ffmpeg
```

### Linux
```bash
sudo apt-get install ffmpeg  # Debian/Ubuntu
sudo yum install ffmpeg      # RHEL/CentOS
```

## Planned Implementation

```python
# Future API example
from subtitle_styling.extractor import extract_subtitles

# Extract all subtitle tracks from a video
extract_subtitles('video.mkv', output_dir='subtitles/')

# Extract specific language track
extract_subtitles('video.mkv', language='eng', output='english.srt')

# Batch extraction from directory
extract_all_subtitles(directory='videos/', output_dir='subtitles/')
```

## Status

This feature is planned but not yet implemented. Currently, the tool focuses on processing existing subtitle files.

For now, users can manually extract subtitles using ffmpeg:

```bash
# List subtitle tracks
ffmpeg -i video.mkv

# Extract specific subtitle track (e.g., track 0:2)
ffmpeg -i video.mkv -map 0:2 output.srt
```
