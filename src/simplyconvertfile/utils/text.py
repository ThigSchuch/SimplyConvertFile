#!/usr/bin/python3
"""
Internationalization and text utilities for the file converter.

This module handles all text localization and provides a centralized
location for all user-facing strings in the application.
"""

import gettext
import locale
import subprocess
from pathlib import Path

from simplyconvertfile import APP_ID

# Locale directory resolution (first match wins):
# 1. Package-relative po/ directory (development / pip install)
# 2. System locale directory (/usr/share/locale)
# 3. User locale directory (~/.local/share/locale) - legacy
_PACKAGE_DIR = Path(__file__).parent.parent
_HOME = Path.home()

_locale_dirs = [
    str(_PACKAGE_DIR / "po"),
    "/usr/share/locale",
    str(_HOME / ".local" / "share" / "locale"),
]

# Ensure system locale is applied for gettext
try:
    locale.setlocale(locale.LC_ALL, "")
except locale.Error:
    pass


def _compile_po_files(po_dir: Path) -> None:
    """Compile .po files to .mo if missing or outdated (dev/fallback).

    This ensures translations work when running from source without
    a prior build step. Silently skips if msgfmt is not available.
    """
    for po_file in po_dir.glob("*.po"):
        lang = po_file.stem
        out_dir = po_dir / lang / "LC_MESSAGES"
        mo_file = out_dir / f"{APP_ID}.mo"

        if mo_file.exists() and mo_file.stat().st_mtime >= po_file.stat().st_mtime:
            continue

        try:
            out_dir.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                ["msgfmt", "-o", str(mo_file), str(po_file)],
                check=True,
                capture_output=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, OSError):
            pass


# Bind to the first locale directory that contains translation files.
# bindtextdomain overwrites previous calls for the same domain,
# so only the last call takes effect — we must pick the right one.
_bound = False
for _locale_dir in _locale_dirs:
    _dir = Path(_locale_dir)
    if _dir.is_dir():
        # Auto-compile .po → .mo if needed (dev environment / first run)
        _compile_po_files(_dir)
        gettext.bindtextdomain(APP_ID, _locale_dir)
        _bound = True
        break

if not _bound:
    gettext.bindtextdomain(APP_ID, _locale_dirs[0])

gettext.textdomain(APP_ID)


def _(message) -> str:
    """Translate a message using gettext.

    Args:
        message: The message to translate.

    Returns:
        str: The translated message, or the original if no translation available.
    """
    return gettext.gettext(message)


class Text:
    """Centralized text constants for the application.

    All user-facing strings are defined here to facilitate internationalization
    and maintain consistency across the application. Strings are wrapped with
    gettext _() function for translation support.

    This class contains constants organized into categories for:
    - UI elements and labels
    - File validation messages
    - Conversion process messages
    - Error handling and notifications
    - Application constants

    All messages support string formatting with named placeholders.

    Examples:
        >>> text.UI.APPLICATION_TITLE
        'File Converter'
        >>> text.Validation.FILE_NOT_FOUND_MESSAGE.format(path="/tmp/test.jpg")
        "File not found:\n/tmp/test.jpg\n\nCheck if the file exists."
    """

    class UI:
        """UI elements, labels, and button text."""

        APPLICATION_TITLE = _("File Converter")
        FORMAT_SELECTION_LABEL = _("Choose output format:")
        CONVERSION_PROGRESS_LABEL = _("Converting\n{file} to {extension}")
        COPY_ERROR_BUTTON_LABEL = _("Copy Error")
        COPY_COMMAND_BUTTON_LABEL = _("Copy Command")
        REPORT_ERROR_BUTTON_LABEL = _("Report Error")
        OK_BUTTON_LABEL = _("OK")
        CANCEL_BUTTON_LABEL = _("Cancel")
        CANCELLING_BUTTON_LABEL = _("Cancelling...")
        START_BUTTON_LABEL = _("Start")
        ERROR_DETAILS_COPIED_MESSAGE = _("Error details copied to clipboard")
        INSTALL_COMMAND_COPIED_MESSAGE = _("Install command copied to clipboard")
        MANUAL_INSTALLATION_REQUIRED_MESSAGE = _(
            "No installation instructions available. Please install '{dependency}' manually."
        )
        MIXED_FORMATS_PLACEHOLDER = _("multiple files selected")

    class Validation:
        """File and input validation messages."""

        INVALID_USAGE_MESSAGE = _("Select one or more files to convert.")
        FILE_NOT_FOUND_MESSAGE = _(
            "File not found:\n{path}\n\nCheck if the file exists."
        )
        INVALID_FILE_MESSAGE = _(
            "Invalid file:\n{path}\n\nSelect a file, not a folder."
        )
        MISSING_EXTENSION_MESSAGE = _(
            "No file extension:\n{path}\n\n"
            "Add an extension (e.g., .jpg, .mp4, .pdf) to determine the format."
        )
        UNSUPPORTED_FORMAT_ERROR_MESSAGE = _("Unsupported file format: {extension}")
        UNSUPPORTED_FORMAT_DETAILS_MESSAGE = _(
            "The file '{filename}' has an unsupported format ({extension}).\n\n"
            "This format is not recognized by the converter or the required "
            "tools are not installed on your system."
        )
        ERRORS_MESSAGE = _(
            "Found {error_count} validation error(s) in the selected files:\n\n"
            "{errors}\n\n"
            "The process will continue with valid files only."
        )

    class Conversion:
        """Conversion process related messages."""

        ERROR_MESSAGE = _("Conversion failed.")
        NO_SUITABLE_CONVERTER_MESSAGE = _("No converter found for this format")
        NO_CONVERSION_OPTIONS_MESSAGE = _(
            "No converters available for {extension} files.\n\n"
            "File: {filename}\n\n"
            "Possible causes:\n"
            "• Missing rules\n"
            "• Missing required tools\n"
            "• Unsupported format\n"
            "• Installation issue\n\n"
            "Check system dependencies."
        )
        CONVERTER_ERROR_DETAILS_MESSAGE = _(
            "Failed to create converter for {source} → {target}\n\n"
            "File: {file}\n\n"
            "This could indicate:\n"
            "• Missing conversion tools\n"
            "• Incompatible format combination\n"
            "• System configuration issue"
        )
        BATCH_CONVERSION_PROGRESS_MESSAGE = _(
            "Converting {current} of {total} files to {extension}\n{file}"
        )
        OUTPUT_DIRECTORY_ERROR_MESSAGE = _(
            "Failed to create or access output directory.\n\n" "Error: {error}"
        )
        FAILED_MESSAGE = _("Conversion failed: {error}")
        CANCELLED_BY_USER_MESSAGE = _("Conversion cancelled by user")
        FAILED_CHECK_TOOLS_MESSAGE = _(
            "Conversion failed - check if required tools are installed "
            "(e.g., ffmpeg, convert, 7z, rar, etc.) and the file format is supported"
        )
        TEMPLATE_ERROR_MESSAGE = _("Template error: {error}")

    class Errors:
        """General error messages and tool-related errors."""

        MISSING_TOOL_MESSAGE = _("Required tool '{tool}' is not installed.")
        MISSING_TOOL_MAIN_MESSAGE = _(
            "The conversion tool '{tool}' is required but not found on your system."
        )
        MISSING_TOOL_ERROR_DETAILS = _(
            "Missing Tool: {tool}\n\n"
            "Install Command:\n{install_command}\n\n"
            "Instructions:\n"
            "Copy the install command above and run it in your terminal. "
            "If the command does not work, please refer to your distribution's "
            "package manager or the tool's official installation instructions."
        )
        UNEXPECTED_ERROR_MESSAGE = _("An unexpected error occurred during conversion.")
        REQUIRED_TOOL_NOT_FOUND_MESSAGE = _(
            "Required tool not found. Please make sure all required "
            "conversion tools are installed (e.g., ffmpeg, convert, etc.)"
        )
        SHELL_COMMAND_EXECUTION_FAILED_MESSAGE = _(
            "Shell command execution failed.\n\nError: {error}\n\nCommand: {command}"
        )
        CHAINED_COMMAND_EXECUTION_FAILED_MESSAGE = _(
            "Chained command execution failed.\n\nError: {error}\n\nCommand: {command}"
        )
        FAILED_CONVERSIONS_PLACEHOLDER = _("Failed conversions:\n\n{errors}")
        FAILED_TO_CREATE_TEMP_DIR_MESSAGE = _("Failed to create temporary directory")
        TEMP_DIR_NOT_AVAILABLE_MESSAGE = _("Temporary directory not available")
        TEMP_DIR_DOES_NOT_EXIST_MESSAGE = _("Temporary directory does not exist")
        NO_ARCHIVE_TEMPLATE_MESSAGE = _("No archive template available in settings")
        NO_CONTENTS_IN_ARCHIVE_MESSAGE = _("No contents found in extracted archive")

    class Operations:
        """Operation status and batch processing messages."""

        FAILED_MESSAGE = _("Operation failed")
        CANCELLED_BY_USER_MESSAGE = _("Operation cancelled by user")
        CHAINED_COMMAND_STEP_FAILED_MESSAGE = _(
            "Step {step}/{total} failed.\n\nError: {error}\n\nCommand: {command}"
        )
        FILE_VALIDATION_FAILED_MESSAGE = _(
            "File validation failed: {file}\n\n"
            "The previous conversion step likely failed.\n\n"
            "Previous step output:\n{previous_error}"
        )
        BATCH_CONVERSION_CANCELLED_MESSAGE = _("Batch conversion cancelled")
        BATCH_CONVERSION_COMPLETED_WITH_ERRORS_MESSAGE = _(
            "Batch conversion completed with {error_count} error(s)."
        )

    class Notifications:
        """Desktop notification titles and messages."""

        SUCCESS_TITLE = _("Conversion Complete")
        SUCCESS_MESSAGE = _("Successfully converted {filename} to {extension}")
        FAILURE_TITLE = _("Conversion Failed")
        FAILURE_MESSAGE = _("Failed to convert {filename} to {extension}")
        BATCH_SUCCESS_TITLE = _("Batch Conversion Complete")
        BATCH_SUCCESS_MESSAGE = _(
            "Successfully converted {successful} of {total} files to {extension}"
        )
        BATCH_FAILURE_TITLE = _("Batch Conversion Failed")
        BATCH_FAILURE_MESSAGE = _(
            "Failed to convert {failed} of {total} files to {extension}"
        )
        CONVERSION_STARTED_TITLE = _("Conversion Started")
        CONVERSION_STARTED_MESSAGE = _(
            "Conversion started for {filename} to {extension}"
        )
        BATCH_CONVERSION_STARTED_TITLE = _("Batch Conversion Started")
        BATCH_CONVERSION_STARTED_MESSAGE = _(
            "Batch conversion of {total} files to {extension} has started"
        )
        BATCH_STEP_CONVERSION_STARTED_TITLE = _("Batch Step Conversion Started")
        BATCH_STEP_CONVERSION_STARTED_MESSAGE = _(
            "Converting {filename} to {extension}"
        )
        BATCH_CONVERSION_CANCELLED_TITLE = _("Batch Conversion Cancelled")
        BATCH_CONVERSION_CANCELLED_MESSAGE = _(
            "Conversion cancelled after processing {completed} of {total} files to {extension}"
        )
        SINGLE_CONVERSION_CANCELLED_TITLE = _("Conversion Cancelled")
        SINGLE_CONVERSION_CANCELLED_MESSAGE = _(
            "File conversion to {extension} was cancelled"
        )
        USER_SETTINGS_CORRUPTED_TITLE = _("Settings Error")
        USER_SETTINGS_CORRUPTED_MESSAGE = _(
            "User settings file is corrupted\n"
            "(~/.config/simplyconvertfile/user_settings.json)\n"
            "Using default settings instead."
        )
        MISSING_TOOL_TITLE = _("Missing Conversion Tool")
        MISSING_TOOL_MESSAGE = _("Required tool '{tool}' is not installed.")

    class Security:
        """Security-related messages for dangerous command detection."""

        DANGEROUS_COMMAND_BLOCKED_TITLE = _("Dangerous Command Blocked")
        DANGEROUS_COMMAND_BLOCKED_MESSAGE = _(
            "A potentially dangerous command was blocked.\n\n"
            "Reason: {reason}\n\n"
            "Command: {command}\n\n"
            "If you need to allow dangerous commands, enable the "
            "'allow_dangerous_commands' option in your user settings."
        )
        DANGEROUS_COMMAND_CONFIRM_TITLE = _("Potentially Dangerous Command")
        DANGEROUS_COMMAND_CONFIRM_MESSAGE = _(
            "The following command contains a potentially dangerous operation "
            "and requires your confirmation to proceed.\n\n"
            "Reason: {reason}\n\n"
            "Command:\n{command}"
        )
        CONTINUE_ANYWAY_BUTTON_LABEL = _("Continue Anyway")

        # Dangerous command category labels
        CATEGORY_PRIVILEGE_ESCALATION = _("privilege escalation")
        CATEGORY_FILE_DELETION = _("file deletion")
        CATEGORY_DIRECTORY_DELETION = _("directory deletion")
        CATEGORY_FILE_DESTRUCTION = _("file destruction")
        CATEGORY_FILE_TRUNCATION = _("file truncation")
        CATEGORY_RAW_DISK_OPERATION = _("raw disk operation")
        CATEGORY_FILESYSTEM_CREATION = _("filesystem creation")
        CATEGORY_DISK_PARTITIONING = _("disk partitioning")
        CATEGORY_FILESYSTEM_SIGNATURE_REMOVAL = _("filesystem signature removal")
        CATEGORY_BLOCK_DEVICE_DISCARD = _("block device discard")
        CATEGORY_SYSTEM_SHUTDOWN = _("system shutdown")
        CATEGORY_SYSTEM_REBOOT = _("system reboot")
        CATEGORY_SYSTEM_POWER_OFF = _("system power off")
        CATEGORY_SYSTEM_HALT = _("system halt")
        CATEGORY_SYSTEM_INIT_CONTROL = _("system init control")
        CATEGORY_SYSTEM_SERVICE_CONTROL = _("system service control")
        CATEGORY_NETWORK_ACCESS = _("network access")
        CATEGORY_NETWORK_DOWNLOAD = _("network download")
        CATEGORY_NETWORK_CONNECTION = _("network connection")
        CATEGORY_REMOTE_SHELL_ACCESS = _("remote shell access")
        CATEGORY_REMOTE_FILE_COPY = _("remote file copy")
        CATEGORY_REMOTE_FILE_SYNC = _("remote file sync")
        CATEGORY_FILE_TRANSFER = _("file transfer")
        CATEGORY_PERMISSION_CHANGE = _("permission change")
        CATEGORY_OWNERSHIP_CHANGE = _("ownership change")
        CATEGORY_GROUP_OWNERSHIP_CHANGE = _("group ownership change")
        CATEGORY_SHELL_CODE_EXECUTION = _("shell code execution")
        CATEGORY_DANGEROUS_OPERATION = _("dangerous operation")


text = Text()
