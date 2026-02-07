#!/usr/bin/env python3
"""
SimplyConvertFile - Universal File Format Converter for Linux.

This module serves as the main entry point for the SimplyConvertFile application,
providing a unified interface for both single file and batch file conversions.

The application supports conversion between various file formats including:
- Images (JPEG, PNG, GIF, BMP, TIFF, WebP, etc.)
- Videos (MP4, AVI, MKV, MOV, WebM, etc.)
- Audio files (MP3, WAV, FLAC, OGG, AAC, etc.)
- Documents (PDF, DOCX, HTML, TXT, etc.)
- Archives (ZIP, TAR, 7Z, RAR, etc.)

Features:
- Single file conversion with format selection dialog
- Batch conversion for multiple files of the same type
- Progress tracking and cancellation support
- Comprehensive error handling and user notifications
- Configurable conversion templates and settings
- File picker dialog when launched without arguments
- Cross-platform compatibility (Linux-focused)

Usage:
    simplyconvertfile [file_path ...]

    When called without arguments, opens a GTK file chooser dialog.
    When called with file paths, proceeds directly to conversion.

Examples:
    # Launch file picker
    simplyconvertfile

    # Convert single image
    simplyconvertfile image.jpg

    # Convert multiple images to PNG
    simplyconvertfile image1.jpg image2.bmp image3.tiff

    # Convert video file
    simplyconvertfile video.mp4

Note:
    For batch conversions, all files must belong to the same format group
    (e.g., all images, all videos, etc.).
"""

import sys
import traceback
from pathlib import Path
from typing import List, Optional

from simplyconvertfile.actions import Action, BatchAction
from simplyconvertfile.ui import InfoDialogWindow
from simplyconvertfile.utils import text
from simplyconvertfile.utils.logging import logger


def _get_supported_extensions() -> List[str]:
    """Get all supported file extensions from the format configuration.

    Returns:
        List[str]: Sorted list of supported extensions (lowercase, without dots).
    """
    try:
        from simplyconvertfile.config import format_config

        extensions = set()
        for group in format_config._format_groups.values():
            for fmt in group.formats:
                extensions.add(fmt.lower())
        return sorted(extensions)
    except Exception:
        # Fallback list of common extensions
        return [
            "7z",
            "aac",
            "ac3",
            "aiff",
            "alac",
            "avi",
            "avif",
            "bmp",
            "caf",
            "cr2",
            "csv",
            "deb",
            "dmg",
            "doc",
            "docx",
            "epub",
            "flac",
            "gif",
            "heic",
            "heif",
            "htm",
            "html",
            "ico",
            "iso",
            "jpeg",
            "jpg",
            "json",
            "m4a",
            "m4v",
            "md",
            "mka",
            "mkv",
            "mobi",
            "mov",
            "mp3",
            "mp4",
            "mpeg",
            "mpg",
            "mts",
            "odp",
            "ods",
            "odt",
            "ogg",
            "opus",
            "pdf",
            "png",
            "ppt",
            "pptx",
            "rar",
            "raw",
            "rpm",
            "rtf",
            "svg",
            "tar",
            "tar.bz2",
            "tar.gz",
            "tar.lzma",
            "tar.lzo",
            "tar.xz",
            "tgz",
            "tif",
            "tiff",
            "ts",
            "txt",
            "wav",
            "webm",
            "webp",
            "wma",
            "wmv",
            "xls",
            "xlsx",
            "xml",
            "yaml",
            "yml",
            "zip",
        ]


def _open_file_chooser() -> Optional[List[str]]:
    """Open a GTK file chooser dialog for selecting files to convert.

    Returns:
        Optional[List[str]]: List of selected file paths, or None if cancelled.
    """
    import gi

    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk

    # Ensure app is initialized (icon, name)
    from simplyconvertfile.ui.icons import _ensure_app_initialized

    _ensure_app_initialized()

    dialog = Gtk.FileChooserDialog(
        title=text.UI.APPLICATION_TITLE,
        action=Gtk.FileChooserAction.OPEN,
    )
    dialog.add_buttons(
        text.UI.CANCEL_BUTTON_LABEL,
        Gtk.ResponseType.CANCEL,
        text.UI.OK_BUTTON_LABEL,
        Gtk.ResponseType.OK,
    )
    dialog.set_select_multiple(True)
    dialog.set_default_response(Gtk.ResponseType.OK)

    # Add filter for supported formats
    supported_filter = Gtk.FileFilter()
    supported_filter.set_name(_get_supported_formats_label())
    for ext in _get_supported_extensions():
        supported_filter.add_pattern(f"*.{ext}")
        supported_filter.add_pattern(f"*.{ext.upper()}")
    dialog.add_filter(supported_filter)

    # Add "All files" filter
    all_filter = Gtk.FileFilter()
    all_filter.set_name("All Files")
    all_filter.add_pattern("*")
    dialog.add_filter(all_filter)

    response = dialog.run()
    file_paths = None

    if response == Gtk.ResponseType.OK:
        file_paths = dialog.get_filenames()
        logger.debug("Files selected via file chooser: {}", file_paths)

    dialog.destroy()

    # Process pending GTK events to ensure dialog is fully closed
    while Gtk.events_pending():
        Gtk.main_iteration()

    return file_paths


def _get_supported_formats_label() -> str:
    """Get a label string for the supported formats file filter."""
    return "Supported Formats"


def main() -> None:
    """Main entry point for the SimplyConvertFile application.

    Parses command-line arguments and executes the appropriate conversion workflow
    based on the number of files provided. When no files are given, opens a
    GTK file chooser dialog to select files interactively.

    Command-line Usage:
        simplyconvertfile [file_path ...]

    Args:
        None (reads from sys.argv)

    Returns:
        None

    Raises:
        SystemExit: With code 1 if invalid usage or conversion fails
    """
    logger.info("SimplyConvertFile application started")
    logger.debug("Command line arguments: {}", sys.argv)

    file_paths: List[str] = sys.argv[1:]

    # If no files provided, open a file chooser dialog
    if not file_paths:
        logger.info("No files provided, opening file chooser dialog")
        selected = _open_file_chooser()
        if selected:
            file_paths = selected
        else:
            logger.info("File chooser cancelled by user")
            sys.exit(0)

    logger.debug("Processing {} file(s): {}", len(file_paths), file_paths)

    try:
        if len(file_paths) == 1:
            logger.info("Starting single file conversion")
            action = Action(Path(file_paths[0]))

        else:
            logger.info("Starting batch conversion with {} files", len(file_paths))
            action = BatchAction(file_paths)

        action.run()
        logger.info("Conversion action completed successfully")

    except Exception as e:
        logger.error("Conversion failed with error: {}", str(e))
        logger.error("Traceback:\n{}", traceback.format_exc())
        raise


if __name__ == "__main__":
    main()
