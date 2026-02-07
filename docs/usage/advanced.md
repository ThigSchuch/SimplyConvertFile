---
layout: default
title: Advanced Features
parent: Usage
nav_order: 4
---

# Advanced Features
{: .no_toc }

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Automatic File Validation

### Multi-Step Conversion Protection

The system automatically validates intermediate files in multi-step conversions (such as LibreOffice document conversions) to prevent cascading failures:

- **Automatic Detection** — Identifies multi-step commands with temporary files
- **Validation Injection** — Inserts `test -f '{file}'` checks between conversion steps
- **Enhanced Error Messages** — Shows the actual conversion error instead of generic file-not-found errors
- **Universal Coverage** — Works automatically for all converter types (image, video, audio, document, archive, etc.)

## Intelligent Tool Selection

The conversion engine automatically selects the best tool for each conversion:

| Tool | Use Case |
|:-----|:---------|
| **Pandoc** | Universal document converter for EPUB, HTML, Markdown, RTF |
| **Calibre** (`ebook-convert`) | Specialized ebook formats (MOBI conversions) |
| **LibreOffice** | Office document conversions (DOC/DOCX/ODT → PDF) |
| **ImageMagick** | Image format conversions |
| **FFmpeg** | Audio and video conversions |
| **7-Zip** | Archive operations |

## Usage Tips

**Quality Control**
: Edit `user_settings.json` to adjust conversion quality parameters:
```bash
nano ~/.config/simplyconvertfile/user_settings.json
```
See [Configuration]({% link configuration/overview.md %}) for details.

**Cross-Format Conversions**
: - Extract audio from video: Select MP4/AVI → Convert to MP3/FLAC
- Animated GIF to video: Select GIF → Convert to MP4/WEBM
- Document to PDF: Select DOC/DOCX/ODT → Convert to PDF
