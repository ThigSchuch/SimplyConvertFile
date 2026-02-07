#!/usr/bin/python3
"""
Audio converter implementation.

This module provides audio conversion functionality using FFmpeg.
Supports conversion between various audio formats including MP3, WAV, FLAC, OGG, etc.
"""

from simplyconvertfile.converters.base import TemplateBasedConverter
from simplyconvertfile.utils.logging import logger


class AudioConverter(TemplateBasedConverter):
    """
    A subclass of TemplateBasedConverter that implements audio file conversion using FFmpeg.

    This class provides the necessary implementation for audio file conversion
    using FFmpeg by defining the '_build_default_command' method with appropriate
    quality settings for audio files.

    Attributes:
        Inherits all attributes from the base TemplateBasedConverter class:
            file (Path): The input audio file to be converted.
            format (str): The audio format to convert the file to.
            target_file (Path): The output audio file after conversion.
            batch_mode (bool): Whether running in batch mode.
            output_dir (Optional[Path]): Output directory for batch conversions.

    Methods:
        _build_default_command(self) -> None: Builds the default FFmpeg command for audio file conversion.

    Dependencies:
        - FFmpeg
    """

    def _build_default_command(self) -> None:
        """Build the default FFmpeg command for audio conversion."""
        logger.debug(
            "Building default FFmpeg command for audio conversion: {} -> {}",
            self.file,
            self.target_file,
        )
        self.command = [
            "ffmpeg",
            "-i",
            str(self.file),
            "-q:a",
            "2",  # High quality audio
            "-y",  # Overwrite output file without asking
            str(self.target_file),
        ]
        logger.debug("Audio conversion command built: {}", self.command)
