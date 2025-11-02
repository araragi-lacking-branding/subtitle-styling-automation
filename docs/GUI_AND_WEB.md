# GUI and Web Interface (Future Roadmap)

This document outlines the planned GUI and web interface implementations for the subtitle styling automation tool.

## Desktop GUI (Planned)

### Technology Options

1. **tkinter** - Built-in Python GUI library (no extra dependencies)
2. **PyQt5/PyQt6** - More feature-rich but requires additional dependencies
3. **Kivy** - Cross-platform and modern

### Planned Features

- Drag-and-drop file/folder selection
- Live preview of subtitle changes
- Side-by-side comparison (original vs. styled)
- Batch processing with progress bar
- Save/load preset configurations
- Export to multiple formats

### Mockup (Planned Interface)

```
+---------------------------------------------------+
|  Subtitle Styling Automation                      |
+---------------------------------------------------+
| Input: [Browse...] /path/to/subtitles             |
| Output: [Browse...] /path/to/output               |
|                                                   |
| Style: [Clean ▼]  [x] Remove HI annotations      |
|                                                   |
| Files to process: 15 files                        |
| [Process] [Cancel]                                |
|                                                   |
| Progress: [████████░░] 80% (12/15 files)          |
|                                                   |
| Preview:                                          |
| +---------------------+  +---------------------+  |
| | Original            |  | Styled              |  |
| | <i>Hello</i> world  |  | Hello world         |  |
| +---------------------+  +---------------------+  |
+---------------------------------------------------+
```

## Web Application (Planned)

### Technology Options

1. **Flask** - Lightweight web framework
2. **FastAPI** - Modern, fast, with automatic API documentation
3. **Streamlit** - Rapid prototyping for data apps

### Planned Features

- Web-based interface accessible from any browser
- Upload subtitle files or paste text directly
- Real-time processing and preview
- Download processed files
- RESTful API for integration with other tools
- User authentication (optional, for hosted versions)

### API Endpoints (Planned)

```
POST /api/process
    - Upload and process subtitle file
    - Body: multipart file upload + style parameters
    - Returns: Processed subtitle file

POST /api/process/text
    - Process subtitle text directly
    - Body: JSON with text and style parameters
    - Returns: JSON with processed text

GET /api/styles
    - List available style guides
    - Returns: JSON array of style options

POST /api/batch
    - Process multiple files at once
    - Body: multipart file uploads
    - Returns: ZIP file with all processed subtitles
```

### Web Interface Mockup

```html
+---------------------------------------------------+
|  🎬 Subtitle Styling Automation                   |
+---------------------------------------------------+
|                                                   |
|  [Upload Files] [Paste Text]                      |
|                                                   |
|  Style: [Clean ▼]                                 |
|  Options: ☑ Remove HI  ☐ Uppercase  ☐ Title Case |
|                                                   |
|  +---------------------------------------------+  |
|  | Original Subtitle                           |  |
|  | ------------------------------------------- |  |
|  | <i>Hello world</i> [MUSIC PLAYING]          |  |
|  +---------------------------------------------+  |
|                                                   |
|  [Process ↓]                                      |
|                                                   |
|  +---------------------------------------------+  |
|  | Processed Subtitle                          |  |
|  | ------------------------------------------- |  |
|  | Hello world                                 |  |
|  +---------------------------------------------+  |
|                                                   |
|  [Download .srt] [Copy Text]                      |
|                                                   |
+---------------------------------------------------+
```

## Implementation Timeline

1. **Phase 1** (Current): CLI tool with core functionality ✅
2. **Phase 2** (Next): Video extraction support
3. **Phase 3**: Basic GUI using tkinter
4. **Phase 4**: Web application with Flask/FastAPI
5. **Phase 5**: Advanced features (presets, plugins, etc.)

## Status

Both GUI and web interfaces are planned but not yet implemented. The current focus is on:
- Completing the CLI functionality
- Adding video extraction support
- Expanding subtitle format support

Contributions for GUI/Web development are welcome!
