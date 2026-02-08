---
layout: default
title: Architecture
nav_order: 7
---

# Architecture
{: .no_toc }

The project follows clean code principles with a well-organized, modular architecture.

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Project Structure

```
src/simplyconvertfile/
├── __init__.py
├── __main__.py          # Module entry point (python -m simplyconvertfile)
├── actions/             # Workflow orchestration
│   ├── base.py          # Abstract base class for actions
│   ├── batch.py         # Batch conversion workflow
│   ├── batch_helpers/   # Batch processing utilities
│   │   ├── error_handler.py     # Error collection and reporting
│   │   ├── file_processor.py    # Individual file conversion logic
│   │   ├── format_validator.py  # Format validation and compatibility
│   │   ├── output_manager.py    # Output directory management
│   │   ├── progress_tracker.py  # Progress tracking for batch ops
│   │   └── state_manager.py     # Batch state tracking and UI
│   └── single.py        # Single file conversion workflow
├── config/              # Configuration and format definitions
│   ├── formats.py       # Format groups and conversion rules
│   ├── settings.json    # Default system settings (read-only)
│   ├── settings.py      # Settings file parser and manager
│   ├── types.py         # Type definitions and enums
│   └── user_settings.json # User customizations template
├── converters/          # Format-specific conversion logic
│   ├── archive.py       # Archive format converter
│   ├── audio.py         # Audio format converter
│   ├── base.py          # Base converter with template-based commands
│   ├── data.py          # Data format converter
│   ├── document.py      # Document format converter
│   ├── helpers/         # Conversion execution utilities
│   │   ├── commands.py           # Command template processing
│   │   ├── constants.py          # Converter constants and defaults
│   │   ├── conversion_manager.py # Conversion coordination
│   │   ├── error_manager.py      # Error handling and reporting
│   │   ├── errors.py             # Error type definitions
│   │   ├── execution.py          # Command execution engine
│   │   ├── file_manager.py       # File operations and temp files
│   │   ├── multi_file_handler.py # Multi-file conversion support
│   │   ├── progress_tracker.py   # Progress monitoring
│   │   ├── sanitizer.py          # Dangerous command detection
│   │   ├── subprocess.py         # Subprocess management
│   │   ├── temp_file.py          # Temporary file management
│   │   ├── template_processor.py # Template processing utilities
│   │   └── validation.py         # Conversion validation
│   ├── image.py         # Image format converter
│   ├── markup.py        # Markup format converter
│   ├── office.py        # Office format converter
│   ├── presentation.py  # Presentation format converter
│   ├── special.py       # Special cross-format converter
│   ├── spreadsheet.py   # Spreadsheet format converter
│   ├── task_converter.py # Task-based converter orchestration
│   └── video.py         # Video format converter
├── core/                # Core business logic
│   └── factory.py       # Factory pattern for converter instantiation
├── main.py              # Application entry point
├── po/                  # Translation files (18 languages)
├── resources/           # Application resources (icons)
├── ui/                  # User interface components
│   ├── aui.py           # Advanced UI components
│   ├── dialogs.py       # GTK dialog windows
│   ├── gi.py            # GTK initialization
│   ├── icons.py         # Icon theme management
│   └── notifications.py # Desktop notification service
└── utils/               # Utility functions
    ├── dependencies.py  # Dependency detection and installation
    ├── logging.py       # Logging configuration
    ├── text.py          # Internationalization and text constants
    ├── usage_tracker.py # Usage tracking and smart preselection
    └── validation.py    # File validation utilities
```

## Design Patterns

### Factory Pattern

The `ConverterFactory` dynamically creates the appropriate converter instance based on format types and conversion rules:

```python
converter = ConverterFactory.create_converter(
    from_format="JPEG",
    to_format="PNG",
    file=Path("image.jpg")
)
```

### Strategy Pattern

Different converter classes implement the same interface but use different conversion strategies (ImageMagick, FFmpeg, LibreOffice, etc.).

### Template Method Pattern

`BaseAction` defines the workflow skeleton, while `Action` and `BatchAction` implement specific steps.

## Key Components

### Actions Layer (`actions/`)

Orchestrates the conversion workflow: file validation, format detection, user interaction (dialogs), error handling, notifications, and progress tracking.

### Converters Layer (`converters/`)

Implements actual conversion logic with format-specific converters. Features template-based command building with placeholder substitution, subprocess management with cancellation support, progress monitoring, multi-step command execution, and tool-agnostic design.

**Converter Helpers** provide:

| Component | Purpose |
|:----------|:--------|
| `ConversionManager` | Orchestrates the conversion workflow |
| `CommandSanitizer` | Detects dangerous commands before execution |
| `ErrorManager` | Collects and formats error information |
| `ExecutionEngine` | Manages subprocess execution with cancellation |
| `FileManager` | Handles file operations and temporary files |
| `FileValidator` | Validates intermediate files in multi-step conversions |
| `ProgressTracker` | Monitors and reports conversion progress |
| `TemplateProcessor` | Processes command templates with dynamic substitution |

### Configuration Layer (`config/`)

Maps formats to groups and converters, reads and validates settings, manages type definitions and enums.

### Core Layer (`core/`)

Business logic: `ConverterFactory` determines and instantiates the right converter.

### UI Layer (`ui/`)

GTK-based user interface: selection dialogs, progress bars with cancellation, error and information dialogs, icon theme integration, and desktop notifications.

### Utils Layer (`utils/`)

Cross-cutting concerns: text and internationalization, usage tracking for smart format preselection, dependency management with cross-distribution package detection, file validation, and color-coded debug logging.
