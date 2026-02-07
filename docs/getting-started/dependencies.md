---
layout: default
title: Dependencies
parent: Getting Started
nav_order: 2
---

# Dependencies
{: .no_toc }

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Core Requirements

- **[Python 3](https://www.python.org/)** — Core runtime (3.8 or higher)
- **[GTK 3](https://www.gtk.org/)** — User interface library
- **[GObject Introspection](https://gi.readthedocs.io/)** — Python bindings for GTK (`python3-gi` package)

## Format-Specific Tools

Install only the tools you need for your desired conversion types.

### Image Conversions

- **[ImageMagick](https://imagemagick.org/)** (`convert` command)
  - Handles most image format conversions
  - Required for: JPEG, PNG, WEBP, AVIF, HEIC, BMP, TIFF, ICO, GIF
  - Installation: `sudo apt install imagemagick`

### Audio & Video Conversions

- **[FFmpeg](https://ffmpeg.org/)**
  - Comprehensive multimedia framework
  - Required for: All audio and video conversions, GIF to video, video to audio extraction
  - Installation: `sudo apt install ffmpeg`
  - Supports hardware acceleration for faster conversions

### Document Conversions

- **[LibreOffice](https://www.libreoffice.org/)** (headless mode)
  - Converts office documents: DOC, DOCX, ODT, XLS, XLSX, PPT, PPTX → PDF
  - Installation: `sudo apt install libreoffice`

- **[Pandoc](https://pandoc.org/)** (optional)
  - Extended document format support: Markdown, HTML, RTF, EPUB
  - Installation: `sudo apt install pandoc`
  - For PDF output: Also install `texlive-xetex` for PDF engine

- **[Calibre](https://calibre-ebook.com/)** (optional)
  - Advanced ebook format support: EPUB, MOBI conversions
  - Required for: `ebook-convert` command used in special conversion rules
  - Installation: `sudo apt install calibre`

- **[Poppler Utils](https://poppler.freedesktop.org/)** (optional)
  - PDF processing tools: `pdftotext`, `pdftohtml`
  - Required for: PDF to text and PDF to HTML conversions
  - Installation: `sudo apt install poppler-utils`

### Archive Operations

- **[7-Zip](https://www.7-zip.org/)** (`p7zip` package)
  - Handles most archive formats
  - Required for: 7Z, RAR extraction, cross-format archive conversions
  - Installation: `sudo apt install p7zip-full`

- **[RAR](http://www.rarlab.com/)** (optional)
  - RAR archive extraction and creation
  - Installation: `sudo apt install rar`

- **[Genisoimage](https://wiki.debian.org/genisoimage)** (optional)
  - ISO image creation from files and directories
  - Installation: `sudo apt install genisoimage`

- **RPM tools** (optional)
  - RPM package extraction: `rpm2cpio`, `cpio`
  - Installation: `sudo apt install rpm2cpio cpio`

- **Advanced compression tools** (optional)
  - LZOP: `sudo apt install lzop`
  - XZ Utils: `sudo apt install xz-utils`

- **Standard archive tools** (usually pre-installed)
  - `zip`/`unzip` for ZIP files
  - `tar` for TAR archives
  - `gzip`, `bzip2`, `xz` for compression

## Quick Install Commands

### Debian / Ubuntu / Linux Mint

```bash
# Install all dependencies
sudo apt install imagemagick ffmpeg libreoffice pandoc calibre poppler-utils p7zip-full rar genisoimage rpm2cpio cpio lzop xz-utils

# Minimal install (images and basic conversions only)
sudo apt install imagemagick ffmpeg

# For Python/GTK dependencies (if not present)
sudo apt install python3 python3-gi gir1.2-gtk-3.0 gir1.2-notify-0.7
```

### Fedora / RHEL

```bash
sudo dnf install ImageMagick ffmpeg libreoffice pandoc calibre poppler-tools p7zip rpm cpio lzop xz
```

### Arch Linux

```bash
sudo pacman -S imagemagick ffmpeg libreoffice-fresh pandoc calibre poppler p7zip rpm-tools cpio lzop xz
```

## Dependency Management

The application includes intelligent dependency detection and installation guidance:

**Automatic Package Manager Detection**
: Supports `apt`, `dnf`, `yum`, `pacman`, `zypper`, `emerge`, `apk`, `flatpak`, `snap`. Automatically detects your system's package manager and falls back to manual installation instructions.

**Cross-Distribution Package Mapping**
: Package names vary by distribution (e.g., `p7zip-full` on Ubuntu vs `p7zip` on Fedora). Automatic package name resolution for your specific distribution. Flatpak/Snap support for sandboxed environments.

**Dependency Verification**
: Pre-conversion tool availability checks with detailed error messages and installation commands. Clipboard integration for easy command copying.
