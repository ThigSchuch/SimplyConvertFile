---
layout: default
title: Overview
parent: Configuration
nav_order: 1
---

# Configuration Overview
{: .no_toc }

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Settings Files

Settings are stored in `~/.config/simplyconvertfile/`:

| File | Purpose |
|:-----|:--------|
| `settings.json` | Conversion command templates (auto-updated from defaults, **read-only**) |
| `user_settings.json` | Your customizations (override defaults, persists across updates) |
| `usage_stats.json` | Conversion history for smart format suggestions |
| `DEBUG` | Create this file to enable debug logging to stdout |

{: .warning }
> The main `settings.json` file gets overwritten during application updates. Any changes you make to it will be lost. For customizations, always edit `user_settings.json`.

## Editing Your Settings

```bash
nano ~/.config/simplyconvertfile/user_settings.json
```

Changes take effect immediately on the next conversion. No restart needed.

## How Overrides Work

User settings in `user_settings.json` are merged with the defaults from `settings.json`. You only need to include the settings you want to change:

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
    }
}
```

## Command Priority

When determining which command to use for a conversion, the system follows this priority (highest to lowest):

1. Special rules (for cross-format conversions)
2. User settings overrides
3. `by_target` specific entries
4. `default` fallback

## Available Placeholders

Use these placeholders in custom conversion commands:

| Placeholder | Description |
|:------------|:------------|
| `{input}` | Source file path |
| `{output}` | Destination file path |
| `{output_dir}` | Output directory path |
| `{temp_file}` | Temporary file path (for multi-step conversions) |
| `{temp_dir}` | Temporary directory path (for document conversions) |
| `{input_name}` | Input filename with extension |
| `{input_stem}` | Input filename without extension |

## General Options

### Format Display

```json
"use_canonical_formats": true
```

Controls whether to show format aliases (JPG/JPEG) or only canonical names. When `true`, only shows "JPEG" instead of both "JPG" and "JPEG".

### Usage-Based Format Preselection

```json
"preselect_format_by_usage": false
```

When enabled, the format selection dialog will pre-select the target format you use most frequently for each source format, based on your conversion history.

How it works:
- Tracks every conversion you perform (e.g., JPEG → PNG, JPEG → WEBP)
- Stores usage statistics in `~/.config/simplyconvertfile/usage_stats.json`
- Pre-selects the most frequently used target format
- Falls back to default formats if no history exists

{: .note }
> All tracking data stays local in your home directory and is never transmitted anywhere.

### Batch Processing

```json
"directory_creation_threshold": 5,
"output_directory_name": "converted_files"
```

| Option | Description |
|:-------|:------------|
| `directory_creation_threshold` | Minimum number of files before automatically creating a separate output directory |
| `output_directory_name` | Default name for auto-created output directories |

### Temporary Files

```json
"temporary": {
    "directory": "/tmp",
    "directory_prefix": "convert_file_",
    "file_suffix": ".tmp",
    "file_prefix": "convert_file_"
}
```
