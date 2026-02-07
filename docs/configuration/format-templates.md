---
layout: default
title: Format Templates
parent: Configuration
nav_order: 2
---

# Format Templates
{: .no_toc }

Customize conversion commands and quality settings for each format group.

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## How Format Rules Work

Each format group has a rules section with two parts:

- **`by_target`** — Specific commands for a particular target format (takes precedence)
- **`default`** — Fallback command used when no specific command exists

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

## Image Rules

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

**Adjustable parameters:**
- `-quality 90` — JPEG quality (1–100, higher = better)
- `-depth 8` — PNG bit depth
- `webp:lossless=false` — WEBP compression mode

## Audio Rules

```json
"audio_rules": {
    "by_target": {
        "MP3": "ffmpeg -i '{input}' -codec:a libmp3lame -b:a 192k -y '{output}'",
        "FLAC": "ffmpeg -i '{input}' -codec:a flac -compression_level 5 -y '{output}'",
        "AAC": "ffmpeg -i '{input}' -codec:a aac -b:a 128k -y '{output}'"
    }
}
```

**Adjustable parameters:**
- `-b:a 192k` — Bitrate (128k, 192k, 256k, 320k)
- `-q:a 2` — Quality level (0–9, lower = better)
- `-compression_level 5` — FLAC compression (0–8)

## Video Rules

```json
"video_rules": {
    "by_target": {
        "MP4": "ffmpeg -i '{input}' -codec:v libx264 -crf 23 -codec:a aac -y '{output}'",
        "MKV": "ffmpeg -i '{input}' -codec:v libx265 -crf 28 -codec:a flac -y '{output}'"
    }
}
```

**Quality parameters:**
- `-crf 23` — Constant Rate Factor (18–28, lower = better quality, larger file)
- `-codec:v libx264` — Video codec (h264, h265/hevc, vp9)
- `-codec:a aac` — Audio codec

## Example Customizations

**High-Quality JPEG Conversion:**
```json
"JPEG": "convert '{input}' -quality 95 -sampling-factor 4:2:0 -strip '{output}'"
```

**Web-Optimized PNG:**
```json
"PNG": "convert '{input}' -depth 8 -colors 256 -strip '{output}'"
```

**High-Quality MP3:**
```json
"MP3": "ffmpeg -i '{input}' -codec:a libmp3lame -b:a 320k -y '{output}'"
```

**Fast Video Encoding (lower quality):**
```json
"MP4": "ffmpeg -i '{input}' -codec:v libx264 -preset ultrafast -crf 28 '{output}'"
```
