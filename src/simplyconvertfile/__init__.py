"""
SimplyConvertFile - Universal File Format Converter for Linux.

A standalone application for converting files between 80+ formats including
images, videos, audio, documents, spreadsheets, presentations, markup,
data formats, and archives.

Originally developed as a Nemo file manager action (convert-file@thigschuch),
now available as a standalone Linux application with GTK 3 UI.
"""

try:
    from importlib.metadata import version as _get_version

    __version__ = _get_version("simplyconvertfile")
except Exception:
    __version__ = "2.0.0"  # Fallback for editable/dev installs

APP_NAME = "SimplyConvertFile"
APP_ID = "simplyconvertfile"
APP_DISPLAY_NAME = "Simply Convert File"
APP_DESCRIPTION = "Converts a file to a different format"
APP_AUTHOR = "thigschuch"
APP_URL = "https://github.com/ThigSchuch/SimplyConvertFile"

# Legacy config directory name (for migration)
LEGACY_CONFIG_DIR_NAME = "convert-file@thigschuch"
# Legacy gettext domain
LEGACY_GETTEXT_DOMAIN = "convert-file@thigschuch"
