---
layout: default
title: Supported Formats
nav_order: 5
---

# Supported Formats
{: .no_toc }

SimplyConvertFile supports over 80 different file formats across 9 categories. Conversions can occur within the same category or between different categories using [special conversion rules]({% link configuration/special-rules.md %}).

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Images (14 formats)

`AVIF` `BMP` `CR2` `GIF` `HEIC` `HEIF` `ICO` `JPEG` `JPG` `PNG` `RAW` `SVG` `TIF` `TIFF` `WEBP`

**Common conversions:**
- RAW/HEIC → JPEG (with quality preservation)
- PNG → WEBP (for web optimization)
- Any format → ICO (for icons)
- GIF → MP4/WEBM (animated GIFs to video)

## Audio (13 formats)

`AAC` `AC3` `AIFF` `ALAC` `CAF` `FLAC` `M4A` `MKA` `MP3` `OGG` `OPUS` `WAV` `WMA`

**Common conversions:**
- Lossy ↔ Lossless (MP3 ↔ FLAC)
- Video extraction (MP4/AVI/MKV → MP3/WAV/FLAC)
- Quality optimization (various bitrate settings for MP3, AAC)

## Video (10 formats)

`AVI` `M4V` `MKV` `MOV` `MP4` `MPEG` `MTS` `TS` `WEBM` `WMV`

**Common conversions:**
- MP4 ↔ MKV (container changes with quality presets)
- Any format → MP4 (with H.264/AAC encoding)
- Any format → WEBM (for web embedding)
- GIF → MP4 (animated GIFs to efficient video)

## Documents

`DOC` `DOCX` `EPUB` `MOBI` `ODT` `PDF` `RTF`

**Common conversions:**
- Office formats → PDF (DOC/DOCX/ODT → PDF)
- PDF → JPEG (first page extraction)
- Images → PDF (single or multi-page)
- RTF ↔ DOCX (document format interchange)

## Spreadsheets

`CSV` `ODS` `XLS` `XLSX`

## Presentations

`ODP` `PPT` `PPTX`

## Markup

`HTML` `MD` `XML`

**Common conversions:**
- Markdown → HTML/PDF (with styling)

## Data

`JSON` `TXT` `YAML`

## Archives (13 formats)

`7Z` `BZ2` `DEB` `DMG` `GZ` `ISO` `LZMA` `LZO` `RAR` `RPM` `TAR` `XZ` `ZIP`

**Common conversions:**
- RAR/7Z/TAR → ZIP (extract and recompress)
- ZIP → 7Z (better compression)
- Various → TAR/TGZ (Linux-friendly archives)

{: .note }
> Some formats are **output-restricted** (can be converted from but not to): DMG, DEB, RPM, RAW, CR2, NEF. See [Special Rules]({% link configuration/special-rules.md %}#output-restricted-formats) for details.
