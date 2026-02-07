---
layout: default
title: Changelog
parent: About
nav_order: 1
---

# Changelog

---

## Version 2.0.0 (Latest)

- **Standalone Application** — Converted from Nemo action to standalone Linux application with pip installation support
- **Expanded Format Support** — 80+ formats across 9 categories
- **GUI File Picker** — Launch without arguments to select files via native GTK file chooser
- **Per-Format Converters** — Dedicated converter classes for each format category
- **Complete Architecture Rewrite** — Modular design with clear separation of concerns
- **Advanced Batch Processing** — Sequential processing with real-time progress tracking, automatic output directory creation, mixed-format support, and detailed error collection
- **Automatic File Validation** — Multi-step conversion protection that detects temporary files, injects validation checks, and prevents cascading failures
- **Smart Format Preselection** — Usage-based learning system that tracks conversion history and pre-selects your most frequently used target formats
- **Intelligent Tool Optimization** — Automatic selection of best conversion tools
- **Advanced Error Handling** — Expandable error dialogs with command output, copy-to-clipboard, and GitHub issue reporting
- **Flexible Configuration System** — Custom conversion rules with quality presets, special cross-format rules, conversion exclusions, and output-restricted formats
- **Enhanced User Experience** — Desktop notifications with granular event control, keyboard navigation, cancellation support, and progress dialogs
- **Robust Dependency Management** — Cross-distribution package detection, automatic package manager identification, and installation command generation
- **Internationalization** — Full gettext support with translations for 18 languages
- **Debug Mode** — Color-coded logging to stdout via DEBUG trigger file
- **Desktop Integration** — Makefile, .deb packaging, and .desktop file support

## Version 1.1 (Nemo action)

- Added support for JPG files
- Fixed image rotation handling

## Version 1.0 (Nemo action)

- Initial release as Cinnamon Nemo action
- Basic single file conversion
- Support for common image, audio, and video formats
