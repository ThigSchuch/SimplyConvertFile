#!/usr/bin/python3
"""
Video converter implementation.

This module provides video conversion functionality using FFmpeg.
Supports conversion between various video formats including MP4, AVI, MKV, WebM, etc.
"""

from simplyconvertfile.converters.base import TemplateBasedConverter
from simplyconvertfile.utils.logging import logger


class VideoConverter(TemplateBasedConverter):
    """
    A class for converting video files using FFmpeg.

    This class inherits from the base abstract class 'TemplateBasedConverter' and implements
    the '_build_default_command' method specific to video file conversion using FFmpeg.
    It provides good quality defaults and handles most common video conversions.

    Attributes:
        Inherits attributes from the 'TemplateBasedConverter' class:
            file (Path): The input video file to be converted.
            format (str): The format to convert the video file to.
            target_file (Path): The output video file after conversion.
            batch_mode (bool): Whether running in batch mode.
            output_dir (Optional[Path]): Output directory for batch conversions.

    Methods:
        _build_default_command(self) -> None: Method to build the default FFmpeg command for video conversion.

    Dependencies:
        - FFmpeg
    """

    def _build_default_command(self) -> None:
        """Build the default FFmpeg command for video conversion."""
        logger.debug(
            "Building default FFmpeg command for video conversion: {} -> {}",
            self.file,
            self.target_file,
        )
        self.command = [
            "ffmpeg",
            "-i",
            str(self.file),
            "-y",  # Overwrite output file without asking
            str(self.target_file),
        ]
        logger.debug("Video conversion command built: {}", self.command)
