---
layout: default
title: Home
nav_order: 1
permalink: /
---

# SimplyConvertFile
{: .fs-9 }

A powerful and comprehensive file conversion tool for Linux with a GTK 3 graphical interface.
{: .fs-6 .fw-300 }

[Get Started]({% link getting-started/installation.md %}){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View on GitHub](https://github.com/ThigSchuch/SimplyConvertFile){: .btn .fs-5 .mb-4 .mb-md-0 }

---

## Overview

SimplyConvertFile supports **80+ formats** across images, videos, audio, documents, spreadsheets, presentations, markup, data formats, and archives.

Originally developed as a [Nemo file manager action](https://github.com/linuxmint/cinnamon-spices-actions) (`convert-file@thigschuch`), now available as a **standalone Linux application**.

Whether you need to convert a single image to a different format or batch-process hundreds of media files, SimplyConvertFile handles it efficiently with real-time progress tracking and detailed error reporting.

## Key Features

- **Single & Batch Conversion** — Convert one file or process multiple files simultaneously with intelligent grouping and sequential processing
- **Smart Format Detection** — Automatically detects file types and suggests contextually appropriate target formats
- **File Picker** — Launch without arguments to select files via a native GTK file chooser
- **Real-time Progress Tracking** — Visual progress bars with detailed status information and cancellation support
- **Comprehensive Error Handling** — Detailed error reporting with expandable details, copy-to-clipboard, and GitHub issue reporting
- **Custom Conversion Rules** — Define your own conversion templates with specific quality settings
- **Desktop Notifications** — Configurable notification system with granular control over events
- **Cross-Format Conversion** — Special rules for converting between format groups (e.g., video to audio, GIF to video)
- **Internationalization** — Full gettext support with translations for 18 languages
- **Usage-Based Suggestions** — Remembers your most-used conversions and pre-selects preferred formats

## Quick Install

```bash
# Via APT repository (recommended — auto-updates)
curl -fsSL https://thigschuch.github.io/SimplyConvertFile/gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/simplyconvertfile.gpg
echo "deb [signed-by=/usr/share/keyrings/simplyconvertfile.gpg] https://thigschuch.github.io/SimplyConvertFile/ stable main" | sudo tee /etc/apt/sources.list.d/simplyconvertfile.list
sudo apt update && sudo apt install simplyconvertfile
```

See [Installation]({% link getting-started/installation.md %}) for all install methods.

## Quick Start

```bash
# Open file picker
simplyconvertfile

# Convert a file
simplyconvertfile document.pdf

# Batch convert
simplyconvertfile *.heic
```

See [Usage]({% link usage/single-conversion.md %}) for detailed guides.
