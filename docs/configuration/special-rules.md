---
layout: default
title: Special Rules
parent: Configuration
nav_order: 3
---

# Special Conversion Rules
{: .no_toc }

Define custom multi-step conversions or unusual format pairs.

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Overview

Special rules define conversions that require custom handling, typically cross-format conversions (e.g., GIF to video) or multi-step processes.

{: .note }
> Since special rules can contain any command templates, virtually any conversion is possible. You can create custom rules for proprietary tools, specialized converters, or even chain multiple commands together.

## Examples

### GIF to MP4

```json
"special_rules": [
    {
        "from": "GIF",
        "to": "MP4",
        "command": [
            "ffmpeg -i '{input}' -movflags faststart -pix_fmt yuv420p -vf 'scale=trunc(iw/2)*2:trunc(ih/2)*2' '{output}'"
        ]
    }
]
```

### MP4 to GIF (multi-step with palette generation)

```json
{
    "from": "MP4",
    "to": "GIF",
    "command": [
        "ffmpeg -i '{input}' -vf 'fps=10,scale=320:-1:flags=lanczos,palettegen=stats_mode=diff' -y '{temp_file}'",
        "ffmpeg -i '{input}' -i '{temp_file}' -filter_complex 'fps=10,scale=320:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=5' -y '{output}'"
    ],
    "temp_file_extension": ".png"
}
```

## Format Aliases

Map file extension aliases to their canonical format names:

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

This ensures files with non-standard extensions are properly recognized and converted.

## Default Format Preferences

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

Example — prefer WEBP for images and WEBM for videos:
```json
{
    "default_formats": {
        "IMAGE": ["WEBP", "PNG"],
        "VIDEO": ["WEBM", "MP4"]
    }
}
```

## Output-Restricted Formats

Some formats cannot be used as conversion targets:

```json
"output_restricted_formats": [
    "DMG", "DEB", "RPM", "RAW", "CR2", "NEF"
]
```

These formats can be converted **from** (used as source files) but cannot be converted **to** (won't appear in format selection).

To enable creation of a restricted format, define a custom `special_rule` in your `user_settings.json`.

## Conversion Exclusions

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
