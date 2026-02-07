#!/usr/bin/python3
"""
Image converter implementation.

This module provides image conversion functionality using ImageMagick's convert command.
Supports conversion between various image formats including JPEG, PNG, GIF, TIFF, WebP, etc.
"""

from simplyconvertfile.converters.base import TemplateBasedConverter
from simplyconvertfile.utils.logging import logger


class ImageConverter(TemplateBasedConverter):
    """
    A subclass of TemplateBasedConverter that implements image file conversion using ImageMagick.

    This converter uses the 'convert' command from ImageMagick to handle
    conversion between various image formats. It supports most common
    image formats and provides good quality defaults.

    Attributes:
        Inherits all attributes from the base TemplateBasedConverter class:
            - file (Path): The input image file to be converted.
            - format (str): The format to convert the image file to.
            - target_file (Path): The output image file after conversion.
            - batch_mode (bool): Whether running in batch mode.
            - output_dir (Optional[Path]): Output directory for batch conversions.

    Methods:
        _build_default_command(self) -> None: Builds the default ImageMagick convert command.

    Dependencies:
        - ImageMagick (convert command)
    """

    def _build_default_command(self) -> None:
        """Build the default ImageMagick command for image conversion."""
        logger.debug(
            "Building default ImageMagick command for image conversion: {} -> {}",
            self.file,
            self.target_file,
        )
        self.command = [
            "convert",
            str(self.file),
            str(self.target_file),
        ]
        logger.debug("Image conversion command built: {}", self.command)
