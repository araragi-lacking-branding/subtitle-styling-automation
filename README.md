# Subtitle Styling Automation

A Python tool to automatically scan directories for subtitle files, extract them, and modify their styling with basic text cleanup. This tool focuses on text-based subtitle formats (starting with SRT) and is designed to be OS-agnostic.

## Features

- 📁 **Directory Scanning**: Recursively scan directories for subtitle files
- 🧹 **Text Cleaning**: Remove formatting tags, normalize whitespace, fix common errors
- 🎨 **Style Guides**: Apply various text styles (uppercase, lowercase, title case, sentence case)
- ♿ **Accessibility**: Remove hearing impaired annotations (optional)
- 🌍 **Encoding Support**: Automatic encoding detection for input files
- 💻 **CLI Interface**: Easy-to-use command-line interface
- 🔧 **OS Agnostic**: Works on Windows, macOS, and Linux

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/araragi-lacking-branding/subtitle-styling-automation.git
cd subtitle-styling-automation

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Requirements

- Python 3.7 or higher
- pysrt >= 1.1.2
- chardet >= 5.0.0

## Usage

### Command Line Interface

#### Process a Single File

```bash
# Clean up a subtitle file (default behavior)
subtitle-style input.srt

# Apply uppercase styling
subtitle-style input.srt --style uppercase

# Remove hearing impaired annotations
subtitle-style input.srt --remove-hi

# Specify output location
subtitle-style input.srt --output output.srt
```

#### Process a Directory

```bash
# Process all subtitle files in a directory
subtitle-style --directory ./subtitles

# Process with specific style
subtitle-style --directory ./subtitles --style sentence

# Save to different directory
subtitle-style --directory ./input --output ./output
```

#### Available Styles

- `clean` - Remove formatting tags, normalize whitespace, fix common errors (default)
- `fansub` - Anime fansub style (ellipsis, em dash, smart quotes, preserves honorifics)
- `uppercase` - Convert all text to UPPERCASE
- `lowercase` - Convert all text to lowercase
- `title` - Convert All Text To Title Case
- `sentence` - Convert text to Sentence case

##### Fansub Style Details

The `fansub` style implements anime fansubbing standards based on groups like Good Job! Media, MTBB, Commie, and SubsPlus:
- Replaces `...` with proper ellipsis `…`
- Replaces `--` with em dash `—`
- Uses smart quotes `" "` and `' '`
- Preserves Japanese honorifics (-san, -kun, -chan, -sama, -sensei)
- Applies sentence case while preserving proper nouns and names
- Maintains proper spacing around punctuation

```bash
# Apply fansub style to anime subtitles
subtitle-style anime.srt --style fansub --output anime-styled.srt
```

#### Additional Options

```bash
# Verbose output
subtitle-style input.srt -v

# Custom file extensions
subtitle-style --directory ./subs --extensions .srt .txt .sub

# Complete example
subtitle-style --directory ./input \
               --output ./output \
               --style sentence \
               --remove-hi \
               --verbose
```

### Python API

```python
from subtitle_styling.parser import SubtitleFile, scan_subtitle_files
from subtitle_styling.styler import apply_style_guide

# Load a subtitle file
subtitle = SubtitleFile('input.srt')

# Apply style guide
apply_style_guide(subtitle.subtitles, style='clean', remove_hi=True)

# Save the modified file
subtitle.save('output.srt')

# Scan directory for subtitle files
files = scan_subtitle_files('./subtitles', extensions=['.srt'])
```

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run tests with coverage
pytest --cov=subtitle_styling --cov-report=html
```

### Project Structure

```
subtitle-styling-automation/
├── src/
│   └── subtitle_styling/
│       ├── __init__.py      # Package initialization
│       ├── parser.py        # Subtitle file parsing and scanning
│       ├── styler.py        # Text cleaning and styling
│       └── cli.py           # Command-line interface
├── tests/
│   ├── test_parser.py       # Parser tests
│   └── test_styler.py       # Styler tests
├── examples/
│   └── sample.srt           # Example subtitle file
├── requirements.txt         # Python dependencies
├── setup.py                 # Package setup
└── README.md               # This file
```

## Examples

See the `examples/` directory for sample subtitle files that demonstrate the tool's capabilities.

```bash
# Process the example file
subtitle-style examples/sample.srt --verbose
```

## Roadmap

- [x] Basic SRT subtitle parsing
- [x] Text cleaning and normalization
- [x] Multiple style guides
- [x] Command-line interface
- [x] Directory scanning
- [ ] Additional subtitle formats (ASS, SSA, VTT)
- [ ] Extract subtitles from video files (using ffmpeg)
- [ ] GUI interface (using tkinter or PyQt)
- [ ] Web application interface (using Flask/FastAPI)
- [ ] Image-based subtitle rendering
- [ ] Batch processing with progress tracking

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
