# ASS Format Support and Fansub Styling

This document explains the Advanced SubStation Alpha (ASS) format support in the subtitle styling automation tool, including professional fansub group style templates.

## Overview

The tool now supports generating `.ass` subtitle files with professional styling templates based on prominent anime fansubbing groups. ASS format provides advanced typography control including fonts, colors, outlines, shadows, and positioning.

## Quick Start

```bash
# Generate ASS file with GJM styling
subtitle-style anime.srt --format ass --ass-style gjm

# Generate both SRT and ASS files
subtitle-style anime.srt --format both --ass-style mtbb

# Apply fansub text styling + ASS visual styling
subtitle-style anime.srt --style fansub --format ass --ass-style commie
```

## Available ASS Styles

### GJM (Good Job! Media)
- **Font**: Gandhi Sans, 75pt
- **Colors**: White text with dark gray outline
- **Outline**: 3.5px outline, 1.5px shadow
- **Characteristics**: Clean, modern sans-serif; excellent readability
- **Best for**: Contemporary anime, action, sci-fi

### MTBB (More Than Blue Blobs)
- **Font**: Fontin Sans, 68pt
- **Colors**: White text with black outline
- **Outline**: 3.0px outline, 2.0px shadow
- **Characteristics**: Minimal, professional styling
- **Best for**: Drama, slice-of-life, clean presentation

### Commie
- **Font**: Cronos Pro, 70pt (Bold)
- **Colors**: White text with black outline
- **Outline**: 4.0px strong outline, 1.5px shadow
- **Characteristics**: Bold, high-contrast for readability
- **Best for**: High-energy shows, comedy, clear visibility

### SubsPlus
- **Font**: Arial, 72pt
- **Colors**: White text with black outline
- **Outline**: 3.0px outline, 2.0px shadow
- **Characteristics**: Standard, professional, widely compatible
- **Best for**: General use, maximum compatibility

### Default
- **Font**: Arial, 70pt
- **Colors**: White text with black outline
- **Outline**: 3.0px outline, 2.0px shadow
- **Characteristics**: Basic ASS styling
- **Best for**: Quick conversions, testing

## Format Options

### SRT Only (Default)
```bash
subtitle-style input.srt
# or explicitly
subtitle-style input.srt --format srt
```

Generates clean SRT subtitle files with text styling applied.

### ASS Only
```bash
subtitle-style input.srt --format ass --ass-style gjm
```

Generates ASS subtitle files with professional styling. Text styling is applied first, then converted to ASS with visual formatting.

### Both Formats
```bash
subtitle-style input.srt --format both --ass-style mtbb
```

Generates both:
- `output.srt` - Clean SRT file
- `output.ass` - Styled ASS file

Perfect for providing multiple format options to users.

## Combining Text and Visual Styling

You can combine text styling (fansub, uppercase, etc.) with ASS visual styling:

```bash
# Fansub text style + GJM visual style
subtitle-style anime.srt --style fansub --format ass --ass-style gjm

# Uppercase text + Commie visual style
subtitle-style movie.srt --style uppercase --format ass --ass-style commie
```

**Recommended combination for anime:**
```bash
subtitle-style anime.srt --style fansub --format both --ass-style gjm
```

This applies:
1. Proper ellipsis (… instead of ...)
2. Em dashes (— instead of --)
3. Smart quotes (" ")
4. Preserved honorifics (-kun, -chan, etc.)
5. Professional GJM visual styling

## Directory Processing

Process entire directories with ASS output:

```bash
# Convert all subtitles to ASS with MTBB style
subtitle-style --directory ./subs --format ass --ass-style mtbb --output ./ass-output

# Generate both formats for all files
subtitle-style --directory ./subs --format both --ass-style gjm --output ./processed
```

## ASS File Structure

Generated ASS files include:

```
[Script Info]
- Resolution: 1920x1080 (full HD)
- Scaled borders and shadows: yes

[V4+ Styles]
- Default style with fansub group specifications
- Font, size, colors, outline, shadow
- Margins and alignment

[Events]
- Dialogue lines with timing
- All styled with Default style
```

## Technical Details

### Color Format
ASS colors use BGR format with alpha: `&HAABBGGRR`
- `&H00FFFFFF` = White (opaque)
- `&H000000FF` = Red
- `&H00FF0000` = Blue
- `&H0000FF00` = Green

### Alignment
- Value `2` = Bottom center (standard for subtitles)
- Margins control distance from screen edges

### Outline and Shadow
- **Outline**: Border around text (in pixels)
- **Shadow**: Drop shadow for depth (in pixels)
- Both scaled appropriately for 1080p resolution

## Font Availability

**Note**: The fansub styles use specific fonts:
- Gandhi Sans (GJM)
- Fontin Sans (MTBB)
- Cronos Pro (Commie)
- Arial (SubsPlus, Default)

If these fonts aren't installed on the viewer's system, the video player will fall back to Arial or a similar sans-serif font. For distribution:
1. Use font embedding if your release format supports it
2. Include font files with instructions
3. Use `Default` or `SubsPlus` style for maximum compatibility

## Python API

```python
from subtitle_styling.parser import SubtitleFile
from subtitle_styling.styler import apply_style_guide
from subtitle_styling.ass_converter import convert_srt_to_ass

# Load and style subtitle
sub = SubtitleFile('input.srt')
apply_style_guide(sub.subtitles, style='fansub')

# Save as SRT
sub.save('output.srt')

# Convert to ASS with GJM styling
convert_srt_to_ass('output.srt', 'output.ass', style_name='gjm')
```

### Available Styles List
```python
from subtitle_styling.ass_converter import get_available_styles

styles = get_available_styles()
print(styles)
# ['gjm', 'mtbb', 'commie', 'subsplus', 'default']
```

## Resolution Scaling

All styles are optimized for 1920x1080 (Full HD) resolution. The ASS format supports resolution-independent scaling, so subtitles will adjust automatically for:
- 720p (1280x720)
- 1080p (1920x1080) ✓ Optimized
- 1440p (2560x1440)
- 4K (3840x2160)

Video players will scale fonts, outlines, and shadows proportionally.

## Best Practices

1. **Choose appropriate style for content**
   - Modern anime → GJM
   - Drama/SoL → MTBB
   - Action/Comedy → Commie
   - General/Compatible → SubsPlus

2. **Use fansub text styling with ASS**
   ```bash
   --style fansub --format ass --ass-style gjm
   ```

3. **Generate both formats for flexibility**
   ```bash
   --format both --ass-style mtbb
   ```

4. **Test with your video player**
   - VLC, MPV, MPC-HC all support ASS
   - Test subtitle visibility on different scenes

5. **Consider font availability**
   - Use `subsplus` for widest compatibility
   - Provide font files for specialized fonts

## Comparison: SRT vs ASS

| Feature | SRT | ASS |
|---------|-----|-----|
| Font control | ❌ | ✅ |
| Color/styling | ❌ | ✅ |
| Outlines/shadows | ❌ | ✅ |
| Positioning | Limited | ✅ Full control |
| File size | Smaller | Larger |
| Compatibility | Universal | Most players |
| Styling options | Basic | Professional |

## Troubleshooting

### Fonts not displaying correctly
- The specified font isn't installed on the system
- Solution: Use `--ass-style subsplus` for Arial (universal)

### Subtitles too large/small
- Resolution mismatch
- Solution: ASS auto-scales; if issues persist, edit fontsize in .ass file

### Colors appear wrong
- This shouldn't happen with the tool
- If it does, report as a bug with your command and output file

## Future Enhancements

Planned features:
- Custom resolution support (--resolution 1280x720)
- Additional fansub group styles
- Sign/typesetting style templates
- Karaoke timing support
- Custom style creation tool

## References

- [Aegisub Manual](https://aegisub.org/docs/latest/) - Industry standard ASS editor
- [ASS Format Specification](https://wiki.x266.mov/docs/subtitles/SSA)
- [Fansub Style Guides](https://kaleido-subs.github.io/handbook/)
