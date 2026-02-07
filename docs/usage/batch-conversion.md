---
layout: default
title: Batch Conversion
parent: Usage
nav_order: 2
---

# Batch Conversion
{: .no_toc }

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Overview

Efficiently process multiple files at once with advanced batch processing capabilities.

## Workflow

1. **Pass multiple files** as arguments (or select them via the file picker)
   - Files can be from different format groups (images, videos, audio, documents, archives)
   - The target format dropdown will show only formats that are valid for all selected file groups
2. **Choose** the target format
   - Formats are displayed in alphabetical order
   - The dropdown comes pre-selected with default formats for each file group (configurable)
3. **Select output location**:
   - **Same directory**: Files are converted in place (for batches ≤5 files by default, configurable)
   - **Auto-create directory**: For 5+ files (configurable threshold), a "converted_files" folder is automatically created
4. **Monitor progress** through the batch conversion dialog
   - Shows current file being processed
   - Overall progress (e.g., "3 of 10 files")
   - Real-time progress updates with sequential processing
5. **Review results**: Summary shows successful conversions and any errors

## Example

Converting 50 HEIC photos to JPEG:

```bash
simplyconvertfile *.heic
```

Choose "JPEG" format → Files are automatically organized in a "converted_files" directory (configurable).

## Advanced Batch Features

**Sequential Processing**
: Files are processed one at a time with real-time progress updates.

**Cancellation Support**
: Cancel at any time with proper cleanup and progress updates.

**Error Collection**
: Detailed error reporting for each failed conversion. The batch continues even if individual files fail.

**Mixed Format Support**
: Cross-format conversions within batch operations with intelligent target format filtering.

**Progress Tracking**
: Real-time updates with timeout callbacks and UI responsiveness.

## Output Directory Settings

By default, when converting 5 or more files, SimplyConvertFile creates a `converted_files` directory in the source location. You can customize this in your `user_settings.json`:

```json
{
    "directory_creation_threshold": 3,
    "output_directory_name": "converted_files"
}
```

See [Configuration]({% link configuration/overview.md %}) for more details.
