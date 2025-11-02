# Subtitle Styling Automation - Quick Reference

## Installation

```bash
pip install -r requirements.txt
pip install -e .
```

## Basic Commands

| Command | Description |
|---------|-------------|
| `subtitle-style file.srt` | Clean a single file (default: clean style) |
| `subtitle-style file.srt -o output.srt` | Specify output file |
| `subtitle-style -d ./subs` | Process all files in directory |
| `subtitle-style file.srt -v` | Verbose output |

## Style Options

| Style | Effect | Example |
|-------|--------|---------|
| `clean` | Remove tags, fix spacing (default) | Hello world |
| `fansub` | Anime fansub (… — " " honorifics) | "Wait… Naruto-kun said that." |
| `uppercase` | ALL CAPS | HELLO WORLD |
| `lowercase` | all lowercase | hello world |
| `title` | Title Case | Hello World |
| `sentence` | Sentence case | Hello world |

```bash
subtitle-style file.srt --style uppercase

# Anime fansub style for preserving honorifics
subtitle-style anime.srt --style fansub
```

## Common Options

| Option | Description |
|--------|-------------|
| `--remove-hi` | Remove [SOUND] and (descriptions) |
| `--extensions .srt .txt` | File types to process |
| `-v, --verbose` | Show detailed progress |

## Common Workflows

### Clean and prepare for YouTube
```bash
subtitle-style movie.srt --style uppercase --remove-hi -v
```

### Batch process a directory
```bash
subtitle-style -d ./input -o ./output --style sentence --remove-hi
```

### Process specific file types
```bash
subtitle-style -d ./subs --extensions .srt --style clean
```

## Python API

```python
from subtitle_styling.parser import SubtitleFile
from subtitle_styling.styler import apply_style_guide

# Load and process
sub = SubtitleFile('input.srt')
apply_style_guide(sub.subtitles, style='clean', remove_hi=True)
sub.save('output.srt')
```

## Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=subtitle_styling
```

## File Formats Supported

Currently supported:
- ✅ SRT (SubRip)
- ✅ Plain text subtitles

Planned:
- 🔄 ASS/SSA (Advanced SubStation Alpha)
- 🔄 VTT (WebVTT)
- 🔄 SUB (MicroDVD)

## Troubleshooting

**Problem**: File encoding errors  
**Solution**: The tool auto-detects encoding. If issues persist, ensure input is UTF-8.

**Problem**: Missing command  
**Solution**: Run `pip install -e .` to install the CLI command.

**Problem**: Tests failing  
**Solution**: Install test dependencies: `pip install -r requirements-dev.txt`

## Project Structure

```
subtitle-styling-automation/
├── src/subtitle_styling/    # Main package
│   ├── parser.py           # File parsing & scanning
│   ├── styler.py           # Text cleaning & styling
│   └── cli.py              # Command-line interface
├── tests/                   # Test suite
├── examples/               # Example files
└── docs/                   # Documentation
```

## Getting Help

- Run `subtitle-style --help` for CLI help
- Check `docs/EXAMPLES.md` for detailed examples
- See `README.md` for full documentation
