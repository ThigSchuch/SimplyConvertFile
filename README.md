# SimplyConvertFile

A powerful and comprehensive file conversion tool for Linux with a GTK 3 graphical interface. Supports **80+ formats** across images, videos, audio, documents, spreadsheets, presentations, markup, data formats, and archives.

Originally developed as a [Nemo file manager action](https://github.com/linuxmint/cinnamon-spices-actions) (`convert-file@thigschuch`), now available as a **standalone Linux application**.

> **📖 Full documentation: [thigschuch.github.io/SimplyConvertFile](https://thigschuch.github.io/SimplyConvertFile/)**

## Key Features

- **Single & Batch Conversion** — Convert one file or hundreds at once with intelligent grouping
- **Smart Format Detection** — Automatically detects file types and suggests appropriate targets
- **File Picker** — Launch without arguments to select files via a native GTK file chooser
- **Real-time Progress Tracking** — Visual progress bars with cancellation support
- **Custom Conversion Rules** — Define your own templates with specific quality settings
- **Desktop Notifications** — Configurable notification system with granular control
- **Cross-Format Conversion** — Special rules for converting between format groups
- **Internationalization** — Translations for 18 languages
- **Usage-Based Suggestions** — Remembers your most-used conversions

## Quick Install

### Via APT repository (recommended — auto-updates)

```bash
curl -fsSL https://thigschuch.github.io/SimplyConvertFile/gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/simplyconvertfile.gpg
echo "deb [signed-by=/usr/share/keyrings/simplyconvertfile.gpg] https://thigschuch.github.io/SimplyConvertFile/ stable main" | sudo tee /etc/apt/sources.list.d/simplyconvertfile.list
sudo apt update && sudo apt install simplyconvertfile
```

### Via .deb package

Download the latest `.deb` from the [Releases page](https://github.com/ThigSchuch/SimplyConvertFile/releases) and install:

```bash
sudo dpkg -i simplyconvertfile_*.deb
sudo apt-get install -f
```

### Via pip

```bash
pip install .
```

See the [full installation guide](https://thigschuch.github.io/SimplyConvertFile/getting-started/installation/) for all methods.

## Usage

```bash
# Open file picker
simplyconvertfile

# Convert a single file
simplyconvertfile document.pdf

# Batch convert
simplyconvertfile *.heic
```

See the [usage guide](https://thigschuch.github.io/SimplyConvertFile/usage/single-conversion/) for details.

## Supported Formats

**Images:** AVIF, BMP, CR2, GIF, HEIC, HEIF, ICO, JPEG, JPG, PNG, RAW, SVG, TIF, TIFF, WEBP  
**Audio:** AAC, AC3, AIFF, ALAC, CAF, FLAC, M4A, MKA, MP3, OGG, OPUS, WAV, WMA  
**Video:** AVI, M4V, MKV, MOV, MP4, MPEG, MTS, TS, WEBM, WMV  
**Documents:** DOC, DOCX, EPUB, MOBI, ODT, PDF, RTF  
**Spreadsheets:** CSV, ODS, XLS, XLSX  
**Presentations:** ODP, PPT, PPTX  
**Markup:** HTML, MD, XML  
**Data:** JSON, TXT, YAML  
**Archives:** 7Z, BZ2, DEB, DMG, GZ, ISO, LZMA, LZO, RAR, RPM, TAR, XZ, ZIP

See the [full format list](https://thigschuch.github.io/SimplyConvertFile/formats/) with common conversions.

## Documentation

| Topic | Link |
|-------|------|
| Installation | [Getting Started](https://thigschuch.github.io/SimplyConvertFile/getting-started/installation/) |
| Dependencies | [Required Tools](https://thigschuch.github.io/SimplyConvertFile/getting-started/dependencies/) |
| Usage Guide | [Single](https://thigschuch.github.io/SimplyConvertFile/usage/single-conversion/) · [Batch](https://thigschuch.github.io/SimplyConvertFile/usage/batch-conversion/) · [Shortcuts](https://thigschuch.github.io/SimplyConvertFile/usage/keyboard-shortcuts/) |
| Configuration | [Overview](https://thigschuch.github.io/SimplyConvertFile/configuration/overview/) · [Templates](https://thigschuch.github.io/SimplyConvertFile/configuration/format-templates/) · [Notifications](https://thigschuch.github.io/SimplyConvertFile/configuration/notifications/) |
| Reference | [Troubleshooting](https://thigschuch.github.io/SimplyConvertFile/reference/troubleshooting/) · [FAQ](https://thigschuch.github.io/SimplyConvertFile/reference/faq/) · [Performance](https://thigschuch.github.io/SimplyConvertFile/reference/performance/) |
| Contributing | [Development](https://thigschuch.github.io/SimplyConvertFile/contributing/development/) · [Translations](https://thigschuch.github.io/SimplyConvertFile/contributing/translations/) |
| Architecture | [Project Structure](https://thigschuch.github.io/SimplyConvertFile/architecture/) |

## License

GPL-3.0-or-later

## Author

**thigschuch**
