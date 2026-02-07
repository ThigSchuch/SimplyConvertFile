# SimplyConvertFile

A powerful and comprehensive file conversion tool for Linux with a GTK 3 graphical interface. Supports **80+ formats** across images, videos, audio, documents, spreadsheets, presentations, markup, data formats, and archives.

Originally developed as a [Nemo file manager action](https://github.com/linuxmint/cinnamon-spices-actions) (`convert-file@thigschuch`), now available as a **standalone Linux application**.

Whether you need to convert a single image to a different format or batch-process hundreds of media files, SimplyConvertFile handles it efficiently with real-time progress tracking and detailed error reporting.

### Key Features

- **Single & Batch Conversion**: Convert one file or process multiple files simultaneously with intelligent grouping and sequential processing
- **Smart Format Detection**: Automatically detects file types and suggests contextually appropriate target formats
- **File Picker**: Launch without arguments to select files via a native GTK file chooser
- **Real-time Progress Tracking**: Visual progress bars with detailed status information, cancellation support, and timeout-based updates
- **Comprehensive Error Handling**: Detailed error reporting with expandable details, copy-to-clipboard functionality, and GitHub issue reporting
- **Custom Conversion Rules**: Define your own conversion templates with specific quality settings and parameters
- **Advanced Batch Processing**: 
  - Sequential processing with progress tracking for multiple files
  - Automatic output directory creation based on configurable thresholds
  - Mixed-format batch support with cross-format conversions
  - Detailed error collection and reporting for failed conversions
- **Flexible Output Options**: 
  - Single file: Save in the same directory as the source
  - Batch mode: Automatic output directory creation when processing 5+ files (configurable threshold)
- **Desktop Notifications**: Configurable notification system with granular control over different event types (start, success, failure, batch events)
- **Cross-Format Conversion**: Special rules for converting between different format groups (e.g., video to audio, GIF to video)
- **Quality Presets**: Optimized conversion templates for common formats with adjustable quality settings
- **Dependency Detection**: Automatically checks for required tools and provides platform-specific installation guidance
- **Cancellation Support**: Stop ongoing conversions at any time without corrupting files, with proper cleanup
- **Unique Filename Generation**: Automatically prevents overwriting existing files
- **Internationalization**: Full gettext support with translations for 18 languages
- **Usage-Based Suggestions**: Remembers your most-used conversions and pre-selects preferred formats
- **Advanced Execution Engine**: Command execution with cancellation support, chained operations, and progress tracking

## Table of Contents

- [Supported Formats](#supported-formats)
  - [Images](#images-14-formats)
  - [Audio](#audio-13-formats)
  - [Video](#video-10-formats)
  - [Documents](#documents)
  - [Spreadsheets](#spreadsheets)
  - [Presentations](#presentations)
  - [Markup](#markup)
  - [Data](#data)
  - [Archives](#archives-13-formats)
- [Dependencies](#dependencies)
  - [Core Requirements](#core-requirements)
  - [Format-Specific Tools](#format-specific-tools)
  - [Quick Install Commands](#quick-install-commands)
- [Installation](#installation)
- [Usage](#usage)
  - [GUI Mode](#gui-no-arguments--opens-file-picker)
  - [Command Line](#command-line)
  - [Single File Conversion](#single-file-conversion)
  - [Batch Conversion](#batch-conversion)
  - [Keyboard Navigation](#keyboard-navigation)
  - [Advanced Features](#advanced-features)
  - [Advanced Usage Tips](#advanced-usage-tips)
- [Configuration](#configuration)
  - [Settings File](#settings-file)
  - [Configuration Options](#configuration-options)
  - [Example Customizations](#example-customizations)
- [Architecture](#architecture)
- [Troubleshooting](#troubleshooting)
- [Internationalization](#internationalization)
- [Performance Tips](#performance-tips)
- [Contributing](#contributing)
- [FAQ](#faq)
- [License](#license)
- [Author](#author)
- [Changelog](#changelog)
- [Acknowledgments](#acknowledgments)

## Supported Formats

SimplyConvertFile supports over 80 different file formats across 9 categories. Conversions can occur within the same category or between different categories using special conversion rules.

### Images (14 formats)
`AVIF`, `BMP`, `CR2`, `GIF`, `HEIC`, `HEIF`, `ICO`, `JPEG`, `JPG`, `PNG`, `RAW`, `SVG`, `TIF`, `TIFF`, `WEBP`

**Common conversions**: 
- RAW/HEIC → JPEG (with quality preservation)
- PNG → WEBP (for web optimization)
- Any format → ICO (for icons)
- GIF → MP4/WEBM (animated GIFs to video)

### Audio (13 formats)
`AAC`, `AC3`, `AIFF`, `ALAC`, `CAF`, `FLAC`, `M4A`, `MKA`, `MP3`, `OGG`, `OPUS`, `WAV`, `WMA`

**Common conversions**:
- Lossy ↔ Lossless (MP3 ↔ FLAC)
- Video extraction (MP4/AVI/MKV → MP3/WAV/FLAC)
- Quality optimization (various bitrate settings for MP3, AAC)

### Video (10 formats)
`AVI`, `M4V`, `MKV`, `MOV`, `MP4`, `MPEG`, `MTS`, `TS`, `WEBM`, `WMV`

**Common conversions**:
- MP4 ↔ MKV (container changes with quality presets)
- Any format → MP4 (with H.264/AAC encoding)
- Any format → WEBM (for web embedding)
- GIF → MP4 (animated GIFs to efficient video)

### Documents
`DOC`, `DOCX`, `EPUB`, `MOBI`, `ODT`, `PDF`, `RTF`

**Common conversions**:
- Office formats → PDF (DOC/DOCX/ODT → PDF)
- PDF → JPEG (first page extraction)
- Images → PDF (single or multi-page)
- RTF ↔ DOCX (document format interchange)

### Spreadsheets
`CSV`, `ODS`, `XLS`, `XLSX`

### Presentations
`ODP`, `PPT`, `PPTX`

### Markup
`HTML`, `MD`, `XML`

**Common conversions**:
- Markdown → HTML/PDF (with styling)

### Data
`JSON`, `TXT`, `YAML`

### Archives (13 formats)
`7Z`, `BZ2`, `DEB`, `DMG`, `GZ`, `ISO`, `LZMA`, `LZO`, `RAR`, `RPM`, `TAR`, `XZ`, `ZIP`

**Common conversions**:
- RAR/7Z/TAR → ZIP (extract and recompress)
- ZIP → 7Z (better compression)
- Various → TAR/TGZ (Linux-friendly archives)

## Dependencies

### Core Requirements
- **[Python 3](https://www.python.org/)** - Core runtime (3.8 or higher)
- **[GTK 3](https://www.gtk.org/)** - User interface library
- **[GObject Introspection](https://gi.readthedocs.io/)** - Python bindings for GTK (python3-gi package)

### Format-Specific Tools

Install only the tools you need for your desired conversion types:

#### For Image Conversions
- **[ImageMagick](https://imagemagick.org/)** (`convert` command)
  - Handles most image format conversions
  - Required for: JPEG, PNG, WEBP, AVIF, HEIC, BMP, TIFF, ICO, GIF
  - Installation: `sudo apt install imagemagick` (Debian/Ubuntu)

#### For Audio & Video Conversions
- **[FFmpeg](https://ffmpeg.org/)**
  - Comprehensive multimedia framework
  - Required for: All audio and video conversions, GIF to video, video to audio extraction
  - Installation: `sudo apt install ffmpeg` (Debian/Ubuntu)
  - Supports hardware acceleration for faster conversions

#### For Document Conversions
- **[LibreOffice](https://www.libreoffice.org/)** (headless mode)
  - Converts office documents: `DOC`, `DOCX`, `ODT`, `XLS`, `XLSX`, `PPT`, `PPTX` → `PDF`
  - Installation: `sudo apt install libreoffice` (Debian/Ubuntu)
  
- **[Pandoc](https://pandoc.org/)** (optional)
  - Extended document format support: `Markdown`, `HTML`, `RTF`, `EPUB`
  - Installation: `sudo apt install pandoc` (Debian/Ubuntu)
  - For PDF output: Also install `texlive-xetex` for `PDF` engine

- **[Calibre](https://calibre-ebook.com/)** (optional)
  - Advanced ebook format support: `EPUB`, `MOBI` conversions
  - Required for: `ebook-convert` command used in special conversion rules
  - Installation: `sudo apt install calibre` (Debian/Ubuntu)

- **[Poppler Utils](https://poppler.freedesktop.org/)** (optional)
  - PDF processing tools: `pdftotext`, `pdftohtml`
  - Required for: `PDF` to text and `PDF` to `HTML` conversions
  - Installation: `sudo apt install poppler-utils` (Debian/Ubuntu)

#### For Archive Operations
- **[7-Zip](https://www.7-zip.org/)** (`p7zip` package)
  - Handles most archive formats
  - Required for: `7Z`, `RAR` extraction, cross-format archive conversions
  - Installation: `sudo apt install p7zip-full` (Debian/Ubuntu)

- **[RAR](http://www.rarlab.com/)** (optional)
  - `RAR` archive extraction and creation
  - Required for: `RAR` file processing
  - Installation: `sudo apt install rar` (Debian/Ubuntu)

- **[Genisoimage](https://wiki.debian.org/genisoimage)** (optional)
  - `ISO` image creation from files and directories
  - Required for: `ISO` format creation
  - Installation: `sudo apt install genisoimage` (Debian/Ubuntu)

- **RPM tools** (optional)
  - `RPM` package extraction: `rpm2cpio`, `cpio`
  - Required for: `RPM` package handling
  - Installation: `sudo apt install rpm2cpio cpio` (Debian/Ubuntu)

- **Advanced compression tools** (optional)
  - `LZOP`: `sudo apt install lzop` (Debian/Ubuntu)
  - `XZ` Utils: `sudo apt install xz-utils` (Debian/Ubuntu)

- **Standard archive tools** (usually pre-installed)
  - `zip`/`unzip` for `ZIP` files
  - `tar` for `TAR` archives
  - `gzip`, `bzip2`, `xz` for compression

### Quick Install Commands

**Debian/Ubuntu/Linux Mint:**
```bash
# Install all dependencies
sudo apt install imagemagick ffmpeg libreoffice pandoc calibre poppler-utils p7zip-full rar genisoimage rpm2cpio cpio lzop xz-utils

# Minimal install (images and basic conversions only)
sudo apt install imagemagick ffmpeg

# For Python/GTK dependencies (if not present)
sudo apt install python3 python3-gi gir1.2-gtk-3.0 gir1.2-notify-0.7
```

**Fedora/RHEL:**
```bash
sudo dnf install ImageMagick ffmpeg libreoffice pandoc calibre poppler-tools p7zip rpm cpio lzop xz
```

**Arch Linux:**
```bash
sudo pacman -S imagemagick ffmpeg libreoffice-fresh pandoc calibre poppler p7zip rpm-tools cpio lzop xz
```

### Dependency Management

The application includes intelligent dependency detection and installation guidance:

**Automatic Package Manager Detection**:
- Supports `apt`, `dnf`, `yum`, `pacman`, `zypper`, `emerge`, `apk`, `flatpak`, `snap`
- Automatically detects your system's package manager
- Falls back to manual installation instructions

**Cross-Distribution Package Mapping**:
- Package names vary by distribution (e.g., `p7zip-full` on Ubuntu vs `p7zip` on Fedora)
- Automatic package name resolution for your specific distribution
- `Flatpak`/`Snap` support for sandboxed environments

**Dependency Verification**:
- Pre-conversion tool availability checks
- Detailed error messages with installation commands
- Clipboard integration for easy command copying

## Installation

### Via APT repository (recommended — auto-updates)

Add the SimplyConvertFile APT repository to get automatic updates via `apt upgrade`:

```bash
# Import the signing key
curl -fsSL https://thigschuch.github.io/SimplyConvertFile/gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/simplyconvertfile.gpg

# Add the repository
echo "deb [signed-by=/usr/share/keyrings/simplyconvertfile.gpg] https://thigschuch.github.io/SimplyConvertFile/ stable main" | sudo tee /etc/apt/sources.list.d/simplyconvertfile.list

# Install
sudo apt update && sudo apt install simplyconvertfile
```

To update later:

```bash
sudo apt update && sudo apt upgrade
```

### Via .deb package (manual install)

Download the latest `.deb` from the [Releases page](https://github.com/thigschuch/SimplyConvertFile/releases) and install:

```bash
sudo dpkg -i simplyconvertfile_*.deb
sudo apt-get install -f  # install dependencies if needed
```

### Via pip (recommended for users)

```bash
pip install .
```

Then optionally add desktop integration:

```bash
cp packaging/simplyconvertfile.desktop ~/.local/share/applications/
cp src/simplyconvertfile/resources/icon.png ~/.local/share/icons/hicolor/48x48/apps/simplyconvertfile.png
gtk-update-icon-cache -f -t ~/.local/share/icons/hicolor/
update-desktop-database ~/.local/share/applications/
```

### System-wide install

```bash
sudo make install
```

### Build .deb package

```bash
make deb
```

### Uninstall

```bash
sudo make uninstall
# or
pip uninstall simplyconvertfile
```

### From Nemo file manager

If you also use the Cinnamon desktop, you can integrate SimplyConvertFile into Nemo's context menu. Copy the provided action file:

```bash
cp packaging/convert-file.nemo_action ~/.local/share/nemo/actions/
```

Or update an existing `.nemo_action` file:

```ini
[Nemo Action]
Name=Convert File
Exec=simplyconvertfile %F
Extensions=7z;aac;...;zip;
Selection=notnone
Dependencies=simplyconvertfile;
```

### Verification

After installation, run `simplyconvertfile` from the terminal or find it in your application menu.

## Usage

### GUI (no arguments — opens file picker)

```bash
simplyconvertfile
```

### Command line

```bash
# Convert a single file
simplyconvertfile document.pdf

# Batch convert multiple files
simplyconvertfile image1.jpg image2.bmp image3.tiff

# Can also run as a Python module
python -m simplyconvertfile video.mp4
```

### Single File Conversion

Perfect for quick, one-off conversions:

1. **Launch** SimplyConvertFile with a file argument, or use the file picker
2. **Choose** your desired output format from the dropdown list
   - Formats are displayed in alphabetical order
   - The dropdown comes pre-selected with default formats for each file group (configurable)
3. **Click** "Convert" and wait for the progress dialog
4. The converted file will appear in the **same directory** with the new extension

**Example**: Converting `photo.heic` to JPEG
- `simplyconvertfile photo.heic` → Select "JPEG" → Convert
- Result: `photo.jpeg` created in the same folder

### Batch Conversion

Efficiently process multiple files at once with advanced batch processing capabilities:

1. **Pass multiple files** as arguments (or select them via the file picker)
   - Files can be from different format groups (images, videos, audio, documents, archives)
   - The target format dropdown will show only formats that are valid for all selected file groups
2. **Choose** the target format
   - Formats are displayed in alphabetical order
   - The dropdown comes pre-selected with default formats for each file group (configurable)
3. **Select output location**:
   - **Same directory**: Files are converted in place (for batches ≤5 files by default, configurable)
   - **Auto-create directory**: For 5+ files (configurable threshold), a "converted_files" folder (configurable name) is automatically created in the source directory
4. **Monitor progress** through the batch conversion dialog
   - Shows current file being processed
   - Overall progress (e.g., "3 of 10 files")
   - Real-time progress updates with sequential processing
5. **Review results**: Summary shows successful conversions and any errors

**Advanced Batch Features**:
- **Sequential Processing**: Files are processed one at a time with real-time progress updates
- **Cancellation Support**: Cancel at any time with proper cleanup and progress updates
- **Error Collection**: Detailed error reporting for each failed conversion
- **Mixed Format Support**: Cross-format conversions within batch operations with intelligent target format filtering
- **Progress Tracking**: Real-time updates with timeout callbacks and UI responsiveness

**Example**: Converting 50 HEIC photos to JPEG
- `simplyconvertfile *.heic` → Choose "JPEG" format
- Files are automatically organized in a "converted_files" directory (configurable)

### Keyboard Navigation

All dialogs support keyboard shortcuts for faster workflow:

#### Format Selection Dialog
- **Enter/Return**: Confirms the selection and starts the conversion (equivalent to clicking "Start" button)
- **Space**: Opens the format dropdown menu for browsing available formats
- **Arrow Keys (Up/Down)**: Navigate through format options directly without opening the dropdown
- **Escape**: Cancels the dialog

#### Progress Dialog (During Conversion)
- **Enter/Return**: Cancels the ongoing conversion
- **Escape**: Cancels the ongoing conversion

#### Error Dialog
- **Enter/Return**: Dismisses the error dialog (equivalent to clicking "OK" button)
- **Escape**: Closes the dialog

### Advanced Features

#### Automatic File Validation

**Multi-Step Conversion Protection**:
The system automatically validates intermediate files in multi-step conversions (such as LibreOffice document conversions) to prevent cascading failures:

- **Automatic Detection**: Identifies multi-step commands with temporary files
- **Validation Injection**: Inserts `test -f '{file}'` checks between conversion steps
- **Enhanced Error Messages**: Shows the actual conversion error instead of generic file-not-found errors
- **Universal Coverage**: Works automatically for all converter types (image, video, audio, document, archive, etc.)

#### Intelligent Tool Selection

**Optimized Tool Usage**:
The conversion engine automatically selects the best tool for each conversion:

- **Pandoc**: Universal document converter for EPUB, HTML, Markdown, RTF
- **Calibre (ebook-convert)**: Specialized ebook formats (MOBI conversions)
- **LibreOffice**: Office document conversions (DOC/DOCX/ODT → PDF)

### Advanced Usage Tips

**Quality Control**: Edit `user_settings.json` to adjust conversion quality parameters (see the Configuration section below):
```bash
nano ~/.config/simplyconvertfile/user_settings.json
```

**Cancel Anytime**: Click the "Cancel" button during conversion to safely stop the process

**Error Recovery**: If a conversion fails:
- Check the error dialog for specific missing dependencies
- Install the required tool
- Retry the conversion

**Cross-Format Conversions**:
- Extract audio from video: Select MP4/AVI → Convert to MP3/FLAC
- Animated GIF to video: Select GIF → Convert to MP4/WEBM
- Document to PDF: Select DOC/DOCX/ODT → Convert to PDF

## Configuration

### ⚠️ IMPORTANT: Never Edit settings.json Directly!

**The main `settings.json` file gets overwritten during application updates.** Any changes you make to it will be lost.

**For customizations, always edit `user_settings.json` instead:**
```bash
nano ~/.config/simplyconvertfile/user_settings.json
```

The examples below show the structure of `settings.json` for reference, but you should only copy the settings you want to customize into your `user_settings.json` file.

### Settings File

Settings are stored in `~/.config/simplyconvertfile/`:

- `settings.json` — Conversion command templates (auto-updated from defaults, read-only)
- `user_settings.json` — Your customizations (override defaults, persists across updates)
- `usage_stats.json` — Conversion history for smart format suggestions
- `DEBUG` — Create this file to enable debug logging to stdout

#### Migration from Nemo Action

If you previously used the `convert-file@thigschuch` Nemo action, your settings at `~/.config/convert-file@thigschuch/` will be automatically migrated on first run.

### Configuration Options

#### 1. Format-Specific Templates

Customize conversion commands and quality settings for each format:

```json
"image_rules": {
    "by_target": {
        "JPEG": "convert '{input}' -quality 90 -strip '{output}'",
        "PNG": "convert '{input}' -depth 8 '{output}'",
        "WEBP": "convert '{input}' -quality 85 -define webp:lossless=false '{output}'"
    },
    "default": "convert '{input}' '{output}'"
}
```

**How format rules work**:
- **`by_target`**: Contains specific commands used when the target format is exactly that key (e.g., "JPEG", "PNG"). These take precedence over the fallback template.
- **`default`**: Fallback command used for all formats in this group when no specific command exists in `by_target`.

**Command priority hierarchy** (highest to lowest):
1. Special rules (for cross-format conversions)
2. User settings overrides
3. `by_target` specific entries
4. `default` fallback

**Available placeholders**:
- `{input}` - Source file path
- `{output}` - Destination file path
- `{output_dir}` - Output directory path
- `{temp_file}` - Temporary file path (for multi-step conversions)
- `{temp_dir}` - Temporary directory path (for document conversions)
- `{input_name}` - Input filename with extension
- `{input_stem}` - Input filename without extension

#### 2. Audio Conversion Settings

```json
"audio_rules": {
    "by_target": {
        "MP3": "ffmpeg -i '{input}' -codec:a libmp3lame -b:a 192k -y '{output}'",
        "FLAC": "ffmpeg -i '{input}' -codec:a flac -compression_level 5 -y '{output}'",
        "AAC": "ffmpeg -i '{input}' -codec:a aac -b:a 128k -y '{output}'"
    }
}
```

**Adjustable parameters**:
- `-b:a 192k` - Bitrate (128k, 192k, 256k, 320k)
- `-q:a 2` - Quality level (0-9, lower = better)
- `-compression_level 5` - FLAC compression (0-8)

#### 3. Video Conversion Settings

```json
"video_rules": {
    "by_target": {
        "MP4": "ffmpeg -i '{input}' -codec:v libx264 -crf 23 -codec:a aac -y '{output}'",
        "MKV": "ffmpeg -i '{input}' -codec:v libx265 -crf 28 -codec:a flac -y '{output}'"
    }
}
```

**Quality parameters**:
- `-crf 23` - Constant Rate Factor (18-28, lower = better quality, larger file)
- `-codec:v libx264` - Video codec (h264, h265/hevc, vp9)
- `-codec:a aac` - Audio codec

#### 4. Special Conversion Rules

Define custom multi-step conversions or unusual format pairs:

```json
"special_rules": [
    {
        "from": "GIF",
        "to": "MP4",
        "command": [
            "ffmpeg -i '{input}' -movflags faststart -pix_fmt yuv420p -vf 'scale=trunc(iw/2)*2:trunc(ih/2)*2' '{output}'"
        ]
    },
    {
        "from": "MP4",
        "to": "GIF",
        "command": [
            "ffmpeg -i '{input}' -vf 'fps=10,scale=320:-1:flags=lanczos,palettegen=stats_mode=diff' -y '{temp_file}'",
            "ffmpeg -i '{input}' -i '{temp_file}' -filter_complex 'fps=10,scale=320:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=5' -y '{output}'"
        ],
        "temp_file_extension": ".png"
    }
]
```

**⚠️ Important Note on Special Rules**: Since special rules can contain any command templates defined by the user, virtually any conversion is possible. You can create custom rules for proprietary tools, specialized converters, or even chain multiple commands together.

#### 5. Notification Settings

Configure desktop notifications for different conversion events:

```json
"notifications": {
    "enabled": true,
    "on_start": false,
    "on_success": true,
    "on_failure": true,
    "on_cancel": true,
    "on_batch_start": false,
    "on_batch_finish": true,
    "on_batch_cancel": true,
    "on_batch_step_start": false,
    "on_batch_step_success": false,
    "on_batch_step_failure": true,
    "on_missing_dependency": true,
    "on_settings_corrupted": true
}
```

**Notification Types**:
- `enabled`: Master switch to enable/disable all notifications
- `on_start`/`on_batch_start`: When conversion begins
- `on_batch_step_start`: When each file in a batch conversion begins processing
- `on_success`/`on_batch_step_success`: Individual file completion
- `on_failure`/`on_batch_step_failure`: Individual file failures
- `on_batch_finish`: Batch completion with success/failure summary
- `on_cancel`/`on_batch_cancel`: User cancellation events
- `on_missing_dependency`: Missing tool detection
- `on_settings_corrupted`: Configuration file issues

#### 6. Default Format Preferences

Customize the default target formats suggested for each format group:

```json
"default_formats": {
    "IMAGE": ["PNG", "JPEG"],
    "VIDEO": ["MP4", "MKV"],
    "AUDIO": ["MP3", "AAC"],
    "DOCUMENT": ["PDF", "DOCX"],
    "ARCHIVE": ["ZIP", "ISO"]
}
```

**Example customization** - Prefer WEBP for images and WEBM for videos:
```json
{
  "default_formats": {
    "IMAGE": ["WEBP", "PNG"],
    "VIDEO": ["WEBM", "MP4"]
  }
}
```

#### 7. Advanced Configuration Options

**Format Display Settings**:
```json
"use_canonical_formats": true
```
Controls whether to show format aliases (JPG/JPEG) or only canonical names. When true, only shows "JPEG" instead of both "JPG" and "JPEG".

**Usage-Based Format Preselection**:
```json
"preselect_format_by_usage": false
```
When enabled, the format selection dialog will pre-select the target format you use most frequently for each source format, based on your conversion history. 

**How it works**:
- Tracks every conversion you perform (e.g., JPEG → PNG, JPEG → WEBP)
- Stores usage statistics in `~/.config/simplyconvertfile/usage_stats.json`
- Pre-selects the most frequently used target format when converting
- Falls back to default formats if no usage history exists

**Privacy**: All tracking data stays local in your home directory and is never transmitted anywhere.

#### 8. Format Aliases

```json
"format_aliases": {
    "DOC": "DOCX",
    "HTM": "HTML",
    "JPG": "JPEG",
    "MK3D": "MKV",
    "MPG": "MPEG",
    "M4V": "MP4",
    "PPT": "PPTX",
    "TIF": "TIFF",
    "XLS": "XLSX",
    "YML": "YAML"
}
```
Maps file extension aliases to their canonical format names. This ensures that files with non-standard extensions are properly recognized and converted.

**Temporary File Settings**:
```json
"temporary": {
    "directory": "/tmp",
    "directory_prefix": "convert_file_",
    "file_suffix": ".tmp",
    "file_prefix": "convert_file_"
}
```

**Batch Processing Settings**:
```json
"directory_creation_threshold": 5,
"output_directory_name": "converted_files"
```
- `directory_creation_threshold`: Minimum number of files before automatically creating a separate output directory
- `output_directory_name`: Default name for auto-created output directories

**User Settings Override**:
User settings in `~/.config/simplyconvertfile/user_settings.json` override system defaults:
```json
{
    "directory_creation_threshold": 3,
    "use_canonical_formats": false,
    "notifications": {
        "enabled": true,
        "on_batch_step_success": false
    },
    "default_formats": {
        "IMAGE": ["WEBP", "PNG"]
    },
    "special_rules": []
}
```

#### 9. Output-Restricted Formats

Some formats cannot be used as conversion targets (output formats):

```json
"output_restricted_formats": [
    "DMG",
    "DEB",
    "RPM",
    "RAW",
    "CR2",
    "NEF"
]
```

These formats:
- ✅ **Can be converted FROM** (used as source files)
- ❌ **Cannot be converted TO** (won't appear in format selection)

**User Override**: You can enable creation by defining a custom `special_rule` in your `user_settings.json`.

#### 10. Conversion Exclusions

Exclude specific conversion pairs that are unreliable or unsupported:

```json
"conversion_exclusions": [
    {
        "from": "EPUB",
        "to": "PDF"
    }
]
```

Users can override excluded conversions by adding a special rule in `user_settings.json`.

### Example Customizations

**High-Quality JPEG Conversion**:
```json
"JPEG": "convert '{input}' -quality 95 -sampling-factor 4:2:0 -strip '{output}'"
```

**Web-Optimized PNG**:
```json
"PNG": "convert '{input}' -depth 8 -colors 256 -strip '{output}'"
```

**High-Quality MP3**:
```json
"MP3": "ffmpeg -i '{input}' -codec:a libmp3lame -b:a 320k -y '{output}'"
```

**Fast Video Encoding (lower quality)**:
```json
"MP4": "ffmpeg -i '{input}' -codec:v libx264 -preset ultrafast -crf 28 '{output}'"
```

### Reloading Configuration

Changes to `user_settings.json` take effect immediately on the next conversion. No restart needed.

## Architecture

The project follows clean code principles with a well-organized, modular architecture that promotes maintainability and extensibility.

### Project Structure

```
src/simplyconvertfile/
├── __init__.py
├── __main__.py        # Module entry point (python -m simplyconvertfile)
├── main.py            # Application entry point
├── actions/           # Workflow orchestration
│   ├── __init__.py
│   ├── base.py       # Abstract base class for actions
│   ├── single.py     # Single file conversion workflow
│   ├── batch.py      # Batch conversion workflow
│   └── batch_helpers/  # Batch processing utilities
│       ├── __init__.py
│       ├── error_handler.py    # Error collection and reporting
│       ├── file_processor.py   # Individual file conversion logic
│       ├── format_validator.py # Format validation and compatibility
│       ├── output_manager.py   # Output directory management
│       ├── progress_tracker.py # Progress tracking for batch operations
│       └── state_manager.py    # Batch state tracking and UI
├── converters/        # Format-specific conversion logic
│   ├── __init__.py
│   ├── base.py       # Base converter with template-based command building
│   ├── archive.py    # Archive format converter
│   ├── audio.py      # Audio format converter
│   ├── data.py       # Data format converter
│   ├── document.py   # Document format converter
│   ├── image.py      # Image format converter
│   ├── markup.py     # Markup format converter
│   ├── office.py     # Office format converter
│   ├── presentation.py # Presentation format converter
│   ├── special.py    # Special cross-format converter
│   ├── spreadsheet.py # Spreadsheet format converter
│   ├── task_converter.py # Task-based converter orchestration
│   ├── video.py      # Video format converter
│   └── helpers/      # Conversion execution utilities
│       ├── __init__.py
│       ├── commands.py          # Command template processing
│       ├── constants.py         # Converter constants and defaults
│       ├── conversion_manager.py # Conversion coordination
│       ├── error_manager.py     # Error handling and reporting
│       ├── errors.py            # Error type definitions
│       ├── execution.py         # Command execution engine
│       ├── file_manager.py      # File operations and temp files
│       ├── multi_file_handler.py # Multi-file conversion support
│       ├── progress_tracker.py  # Progress monitoring
│       ├── subprocess.py        # Subprocess management
│       ├── temp_file.py         # Temporary file management
│       ├── template_processor.py # Template processing utilities
│       └── validation.py        # Conversion validation
├── config/            # Configuration and format definitions
│   ├── __init__.py
│   ├── formats.py    # Format groups and conversion rules
│   ├── settings.json # Default system settings (read-only)
│   ├── settings.py   # Settings file parser and manager
│   ├── types.py      # Type definitions and enums
│   └── user_settings.json # User customizations template
├── core/              # Core business logic
│   ├── __init__.py
│   └── factory.py    # Factory pattern for converter instantiation
├── ui/                # User interface components
│   ├── __init__.py
│   ├── aui.py        # Advanced UI components
│   ├── dialogs.py    # GTK dialog windows
│   ├── gi.py         # GTK initialization
│   ├── icons.py      # Icon theme management
│   └── notifications.py # Desktop notification service
├── utils/             # Utility functions
│   ├── __init__.py
│   ├── dependencies.py  # Dependency detection and installation
│   ├── logging.py       # Logging configuration
│   ├── text.py          # Internationalization and text constants
│   ├── usage_tracker.py # Conversion usage tracking and smart preselection
│   └── validation.py    # File validation utilities
├── resources/         # Application resources
│   ├── icon.png       # Application icon
│   ├── icon_dark.png  # Dark theme icon
│   └── icon_light.png # Light theme icon
└── po/                # Translation files (i18n)
    ├── convert-file@thigschuch.pot # Translation template
    ├── ca.po         # Catalan
    ├── cs.po         # Czech
    ├── da.po         # Danish
    ├── es.po         # Spanish
    ├── eu.po         # Basque
    ├── fi.po         # Finnish
    ├── fr.po         # French
    ├── hu.po         # Hungarian
    ├── is.po         # Icelandic
    ├── it.po         # Italian
    ├── ja.po         # Japanese
    ├── nl.po         # Dutch
    ├── pt.po         # Portuguese
    ├── pt_BR.po      # Brazilian Portuguese
    ├── tr.po         # Turkish
    ├── uk.po         # Ukrainian
    └── vi.po         # Vietnamese
```

### Design Patterns

#### Factory Pattern
The `ConverterFactory` dynamically creates the appropriate converter instance based on format types and conversion rules:

```python
converter = ConverterFactory.create_converter(
    from_format="JPEG",
    to_format="PNG",
    file=Path("image.jpg")
)
```

#### Strategy Pattern
Different converter classes implement the same interface but use different conversion strategies (ImageMagick, FFmpeg, LibreOffice, etc.).

#### Template Method Pattern
`BaseAction` defines the workflow skeleton, while `Action` and `BatchAction` implement specific steps.

### Key Components

#### 1. **Actions Layer** (`actions/`)
Orchestrates the conversion workflow:
- File validation and format detection
- User interaction (dialogs)
- Error handling and notifications
- Progress tracking

#### 2. **Converters Layer** (`converters/`)
Implements actual conversion logic with format-specific converters:
- Per-format converter classes (image, audio, video, document, archive, markup, data, etc.)
- Template-based command building with placeholder substitution
- Subprocess management and cancellation support
- Progress monitoring and error capture
- Multi-step command execution with chained operations
- Tool-agnostic design that works with any conversion tool (ImageMagick, FFmpeg, LibreOffice, Pandoc, 7z, etc.)

**Converter Helpers** provide specialized functionality:
- **ConversionManager**: Orchestrates the conversion workflow
- **FileManager**: Handles file operations and temporary file management
- **ExecutionEngine**: Manages subprocess execution with cancellation support
- **ProgressTracker**: Monitors and reports conversion progress
- **ErrorManager**: Collects and formats error information
- **TemplateProcessor**: Processes command templates with dynamic substitution
- **FileValidator**: Validates intermediate files in multi-step conversions

#### 3. **Configuration Layer** (`config/`)
Manages format definitions and user settings:
- **FormatConfiguration**: Maps formats to groups and converters
- **SettingsManager**: Reads and validates settings.json
- **Type Definitions**: Enums for ConverterType, FormatGroup, etc.

#### 4. **Core Layer** (`core/`)
Business logic and object creation:
- **ConverterFactory**: Determines and instantiates the right converter

#### 5. **UI Layer** (`ui/`)
GTK-based user interface:
- Selection dialogs (format picker)
- Progress bars with cancellation support
- Error and information dialogs
- Icon theme integration
- Desktop notification service

#### 6. **Utils Layer** (`utils/`)
Cross-cutting concerns:
- Text and internationalization
- **Usage tracking** for smart format preselection based on conversion history
- **Dependency management** with cross-distribution package detection
- **File validation** system with format recognition and compatibility checking
- **Logging** with color-coded debug output

## Debug Mode

Enable verbose logging by creating the DEBUG trigger file:

```bash
mkdir -p ~/.config/simplyconvertfile
touch ~/.config/simplyconvertfile/DEBUG
```

Logs are printed to stdout with color-coded levels.

## Troubleshooting

### Common Issues

#### "Command not found" or "Missing dependency" errors

**Problem**: The required conversion tool is not installed.

**Solution**: Install the missing tool using your package manager:
```bash
# For image conversions
sudo apt install imagemagick

# For audio/video conversions
sudo apt install ffmpeg

# For document conversions
sudo apt install libreoffice pandoc calibre poppler-utils

# For archive conversions
sudo apt install p7zip-full rar genisoimage rpm2cpio cpio lzop xz-utils
```

#### Conversion fails with "Invalid format" error

**Problem**: The source or target format is not recognized.

**Solutions**:
1. Ensure the file has the correct extension
2. Check that the format is listed in supported formats
3. Try a different target format from the same group
4. Check `conversion_exclusions` in settings — the conversion pair may be explicitly excluded

#### LibreOffice conversions fail silently

**Problem**: LibreOffice returns success even when conversion fails, causing misleading errors.

**Solution**: This is automatically handled by the file validation system. If you see errors like "File validation failed: /tmp/file.odt", check the previous command's output shown in the error dialog for the actual LibreOffice error.

#### Batch conversion stops after one file

**Problem**: An error occurred and wasn't handled properly.

**Solutions**:
1. Check the error dialog for specific information
2. Try converting files individually to identify the problematic one
3. Ensure all selected files are valid and not corrupted

#### Low quality output

**Problem**: Default quality settings may not meet your needs.

**Solutions**:
1. Edit `user_settings.json` to increase quality parameters (see Configuration section)
2. For JPEG: Increase `-quality` value (85-100)
3. For MP3: Increase bitrate `-b:a` (256k or 320k)
4. For video: Decrease `-crf` value (18-23 for high quality)

#### Slow conversion speed

**Problem**: Complex conversions or large files take time.

**Solutions**:
1. For video: Use faster presets (`-preset fast` or `-preset ultrafast`)
2. Enable hardware acceleration in FFmpeg (if supported)
3. Process fewer files at once
4. Close other resource-intensive applications

### Getting Help

If you encounter issues not covered here:

1. **Check the error message**: It often contains specific information about what went wrong
2. **Enable debug mode**: Create `~/.config/simplyconvertfile/DEBUG` for detailed logs
3. **Verify dependencies**: Run the conversion command manually in terminal to test
4. **Report bugs**: Open an issue on GitHub with:
   - Operating system and version
   - Installed tool versions (`convert --version`, `ffmpeg -version`, etc.)
   - Error message and steps to reproduce

## Internationalization

SimplyConvertFile supports multiple languages through gettext translations:

**Currently supported languages**:
- Basque (eu)
- Catalan (ca)
- Czech (cs)
- Danish (da)
- Dutch (nl)
- English (default)
- Finnish (fi)
- French (fr)
- Hungarian (hu)
- Icelandic (is)
- Italian (it)
- Japanese (ja)
- Portuguese (pt, pt_BR)
- Spanish (es)
- Turkish (tr)
- Ukrainian (uk)
- Vietnamese (vi)

**Contributing translations**: Translation files are located in the `po/` directory. To add a new language:
1. Copy `convert-file@thigschuch.pot` to `your_language.po`
2. Translate the strings
3. Submit a pull request

## Performance Tips

### Optimizing Conversion Speed

1. **Video conversions**: Use hardware acceleration if available
   ```json
   "MP4": "ffmpeg -hwaccel auto -i '{input}' -c:v h264_nvenc '{output}'"
   ```

2. **Batch conversions**: Process in smaller groups if memory is limited

3. **Image conversions**: For large batches, reduce quality slightly for faster processing

### Quality vs. Size Trade-offs

- **Images**: WEBP offers best compression (smaller files) with good quality
- **Audio**: AAC 128k or Opus provides good quality at lower bitrates than MP3
- **Video**: H.265 (HEVC) provides better compression than H.264 but slower encoding
- **Documents**: PDF/A format for archival, regular PDF for sharing

## Contributing

Contributions are welcome! Areas for improvement:

- **New format support**: Add more conversion rules
- **Performance**: Optimize conversion commands
- **UI improvements**: Better progress indication, layout enhancements
- **Testing**: Unit tests for converters and workflows
- **Translations**: Improve existing translations, add more languages

### Development Setup

1. Clone the repository
2. Install development dependencies
3. Make your changes
4. Test with various file types
5. Submit a pull request

## FAQ

**Q: Can I convert multiple different file types at once?**  
A: Yes, batch conversion supports files from different format groups, but the target format dropdown will only show formats that work for all selected files.

**Q: Does it preserve metadata (EXIF, ID3 tags)?**  
A: Depends on the format and conversion. Some converters preserve metadata, others strip it. You can customize this in user_settings.json.

**Q: Can I convert entire folders?**  
A: Select all files within a folder for batch conversion. Recursive folder conversion is not currently supported.

**Q: Is there a size limit for conversions?**  
A: No built-in limit, but very large files (>1GB) may take significant time. Monitor system resources during conversion.

**Q: Can I use this on other desktop environments?**  
A: Yes! Unlike the original Nemo action, SimplyConvertFile is a standalone application that works on any Linux desktop environment with GTK 3 support.

**Q: Does it support drag-and-drop?**  
A: Not currently. Use the file picker or pass files as command line arguments.

**Q: How is this related to the convert-file Nemo action?**  
A: SimplyConvertFile was originally developed as a Cinnamon Nemo action (`convert-file@thigschuch`). It has been refactored into a standalone application that works independently of any file manager, while retaining all the original functionality and adding new features like the GUI file picker and expanded format support.

## License

GPL-3.0-or-later

## Author

**thigschuch**

## Changelog

**Version 2.0.0** (Latest):
- **Standalone Application**: Converted from Nemo action to standalone Linux application with pip installation support
- **Expanded Format Support**: 80+ formats across 9 categories (images, audio, video, documents, spreadsheets, presentations, markup, data, archives)
- **GUI File Picker**: Launch without arguments to select files via native GTK file chooser
- **Per-Format Converters**: Dedicated converter classes for each format category
- **Complete Architecture Rewrite**: Modular design with clear separation of concerns across actions, converters, config, core, UI, and utils layers
- **Advanced Batch Processing**: Sequential processing with real-time progress tracking, automatic output directory creation, mixed-format support, and detailed error collection
- **Automatic File Validation**: Multi-step conversion protection that detects temporary files, injects validation checks, and prevents cascading failures
- **Smart Format Preselection**: Usage-based learning system that tracks conversion history and automatically pre-selects your most frequently used target formats
- **Intelligent Tool Optimization**: Automatic selection of best conversion tools (Pandoc for documents, Calibre for MOBI, LibreOffice for office formats)
- **Advanced Error Handling**: Expandable error dialogs with command output, copy-to-clipboard functionality, and direct GitHub issue reporting
- **Flexible Configuration System**: Custom conversion rules with quality presets, special cross-format rules, conversion exclusions, and output-restricted formats
- **Enhanced User Experience**: Desktop notifications with granular event control, keyboard navigation, cancellation support, and progress dialogs
- **Robust Dependency Management**: Cross-distribution package detection, automatic package manager identification, and installation command generation
- **Internationalization**: Full gettext support with translations for 18 languages
- **Debug Mode**: Color-coded logging to stdout via DEBUG trigger file
- **Desktop Integration**: Makefile, .deb packaging, and .desktop file support

**Version 1.1** (Nemo action):
- Added support for JPG files
- Fixed image rotation handling
  
**Version 1.0** (Nemo action):
- Initial release as Cinnamon Nemo action
- Basic single file conversion
- Support for common image, audio, and video formats

## Acknowledgments

- Originally built for the [`Cinnamon Desktop`](https://github.com/linuxmint/cinnamon) environment as a Nemo action
- [`Python`](https://www.python.org/) 3.8+ for implementation
- [`GTK`](https://www.gtk.org/) for the user interface
- [`FFmpeg`](https://ffmpeg.org/) for multimedia processing
- [`ImageMagick`](https://imagemagick.org/) for image manipulation
- [`LibreOffice`](https://www.libreoffice.org/) for document conversions
- [`Pandoc`](https://pandoc.org/) for advanced document format conversions
- [`7-Zip`](https://www.7-zip.org/) for archive handling
- [`Calibre`](https://calibre-ebook.com/) for eBook format conversions
- [`Poppler-utils`](https://poppler.freedesktop.org/) for PDF processing
- [`RAR`](https://www.rarlab.com/) for RAR archive support
- [`Genisoimage`](https://wiki.debian.org/genisoimage) for ISO image creation
- and many more open-source projects and libraries
- Inspired by the need for quick, accessible file conversions in Linux
