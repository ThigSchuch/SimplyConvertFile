---
layout: default
title: Single File Conversion
parent: Usage
nav_order: 1
---

# Single File Conversion
{: .no_toc }

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Launching

### GUI Mode (file picker)

```bash
simplyconvertfile
```

Opens a native GTK file chooser dialog to select files.

### Command Line

```bash
# Convert a single file
simplyconvertfile document.pdf

# Can also run as a Python module
python -m simplyconvertfile video.mp4
```

## Conversion Workflow

1. **Launch** SimplyConvertFile with a file argument, or use the file picker
2. **Choose** your desired output format from the dropdown list
   - Formats are displayed in alphabetical order
   - The dropdown comes pre-selected with default formats for each file group (configurable)
3. **Click** "Convert" and wait for the progress dialog
4. The converted file will appear in the **same directory** with the new extension

### Example

Converting `photo.heic` to JPEG:

```bash
simplyconvertfile photo.heic
```

Select "JPEG" → Convert → Result: `photo.jpeg` created in the same folder.

## Cross-Format Conversions

SimplyConvertFile supports conversions between different format groups:

- **Extract audio from video**: Select MP4/AVI → Convert to MP3/FLAC
- **Animated GIF to video**: Select GIF → Convert to MP4/WEBM
- **Document to PDF**: Select DOC/DOCX/ODT → Convert to PDF
- **Images to PDF**: Convert images into PDF documents

## Error Recovery

If a conversion fails:

1. Check the error dialog for specific missing dependencies
2. Install the required tool (see [Dependencies]({% link getting-started/dependencies.md %}))
3. Retry the conversion

## Cancel Anytime

Click the "Cancel" button during conversion to safely stop the process. Files are properly cleaned up with no corruption.
