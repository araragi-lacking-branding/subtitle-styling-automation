# Anime Fansub Style Guide

This document explains the anime fansub styling implemented in the `subtitle-styling-automation` tool, based on standards from professional fansubbing groups like Good Job! Media, MTBB, Commie, and SubsPlus.

## Overview

The `fansub` style is designed specifically for anime subtitles and applies industry-standard formatting conventions used by professional fansubbing groups.

## Features

### 1. Proper Ellipsis

**Before:** `Wait... what?`  
**After:** `Wait… what?`

Replaces three periods (`...`) with the proper ellipsis character (`…`, U+2026). This is the standard in professional subtitling and provides better typography.

### 2. Em Dashes

**Before:** `I was going to--`  
**After:** `I was going to—`

Replaces double or triple hyphens (`--` or `---`) with the em dash (`—`). Em dashes are used for interruptions or abrupt stops in dialogue, which is common in anime.

### 3. Smart Quotes

**Before:** `"Hello there"`  
**After:** `"Hello there"`

Converts straight ASCII quotes to typographically correct "smart quotes" or "curly quotes":
- Opening double quotes: `"`
- Closing double quotes: `"`
- Opening single quotes: `'`
- Closing single quotes: `'`

### 4. Japanese Honorifics Preserved

**Examples:**
- `Naruto-kun` → Preserved as-is
- `Sakura-chan` → Preserved as-is
- `Kakashi-sensei` → Preserved as-is
- `hokage-sama` → Preserved as-is

The fansub style does NOT remove or translate Japanese honorifics, as these convey important cultural and relationship information that anime fans expect to see.

### 5. Sentence Case Capitalization

**Before:** `kakashi-sensei always says... "never give up."`  
**After:** `Kakashi-sensei always says… "Never give up."`

Capitalizes the first letter of sentences while preserving:
- Proper nouns (names, places)
- Existing capitalization in names and honorifics
- Japanese terms and honorifics

### 6. Proper Spacing

Ensures correct spacing around punctuation:
- No spaces around em dashes: `word—word`
- Space after ellipsis when followed by new sentence: `word… Word`
- Proper spacing preserved around quotes

## Usage

### Basic Usage

```bash
# Process a single anime subtitle file
subtitle-style anime.srt --style fansub

# Specify output file
subtitle-style anime.srt --style fansub --output anime-styled.srt

# Process entire directory of anime subtitles
subtitle-style --directory ./anime-subs --style fansub --output ./styled-subs
```

### With Additional Options

```bash
# Remove hearing impaired annotations (sound effects, etc.)
subtitle-style anime.srt --style fansub --remove-hi

# Verbose output to see what's being processed
subtitle-style anime.srt --style fansub --verbose
```

### Python API

```python
from subtitle_styling.parser import SubtitleFile
from subtitle_styling.styler import apply_style_guide

# Load anime subtitle file
sub = SubtitleFile('anime.srt')

# Apply fansub style
apply_style_guide(sub.subtitles, style='fansub')

# Save the styled file
sub.save('anime-fansub.srt')
```

## Example Transformations

### Example 1: Dialogue with Ellipsis

**Input:**
```
"Wait... what are you saying?"
```

**Output:**
```
"Wait… What are you saying?"
```

### Example 2: Interrupted Dialogue

**Input:**
```
Naruto-kun, I was going to--
```

**Output:**
```
Naruto-kun, I was going to—
```

### Example 3: Multiple Sentences

**Input:**
```
"Sensei said we should..." he trailed off.
```

**Output:**
```
"Sensei said we should…" he trailed off.
```

### Example 4: Honorifics Preserved

**Input:**
```
The hokage-sama will-- wait, stop!
```

**Output:**
```
The hokage-sama will—wait, stop!
```

## Technical Details

The fansub style applies the following transformations in order:

1. **Remove formatting tags** - Strips HTML and SubStation Alpha formatting tags
2. **Fix punctuation spacing** - Adds missing spaces after punctuation
3. **Replace ellipsis** - Three periods → single ellipsis character
4. **Replace em dashes** - Double/triple hyphens → em dash
5. **Convert to smart quotes** - Straight quotes → curly quotes
6. **Normalize spacing** - Around em dashes, ellipsis, multiple spaces
7. **Apply sentence case** - Capitalize first letter while preserving names/honorifics

## Differences from Other Styles

| Feature | `clean` | `fansub` | `sentence` |
|---------|---------|----------|------------|
| Ellipsis character | ❌ | ✅ | ❌ |
| Em dashes | ❌ | ✅ | ❌ |
| Smart quotes | ❌ | ✅ | ❌ |
| Preserve honorifics | ✅ | ✅ | ❌ (lowercases) |
| Sentence case | ❌ | ✅ | ✅ |
| Quote spacing | Removes | Preserves | Removes |

## Standards and References

This implementation is based on:
- **Good Job! Media** fansubbing standards
- **MTBB** (More Than Blue Blobs) style guidelines
- **Commie** subtitle formatting practices
- **SubsPlus** professional standards
- Netflix and professional subtitle formatting guides for ellipsis and em dash usage

For more information on fansubbing standards, see:
- [Kaleido Subtitling Handbook](https://kaleido-subs.github.io/handbook/)
- Professional subtitle formatting guides
- Anime fansubbing community resources

## Tips

1. **Use with `--remove-hi`** to remove sound effect annotations like `[MUSIC PLAYING]` while keeping dialogue clean
2. **Preserve the original** by using `--output` to save to a different file
3. **Test on a sample** file first to ensure the style matches your expectations
4. **Batch process** entire seasons by pointing to a directory with all episode subtitle files

## Contributing

If you notice any anime-specific formatting that should be handled differently, please open an issue or submit a pull request with examples!
