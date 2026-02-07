#!/usr/bin/python3
"""
Markup and web document converter implementation.

This module provides conversion functionality for markup and web formats using
Pandoc. Supports HTML, HTM, MD (Markdown), and XML formats.
"""

from simplyconvertfile.converters.base import TemplateBasedConverter
from simplyconvertfile.utils.logging import logger


class MarkupConverter(TemplateBasedConverter):
    """
    A converter for markup and web document formats.

    This converter handles conversions between markup formats (HTML, MD, XML)
    using Pandoc for intelligent document structure preservation.

    Configuration (from settings.json):
        - markup_rules.format_commands: Specific commands for each format
        - markup_rules.command_template: Default fallback command (Pandoc)

    Attributes:
        Inherits all attributes from the base TemplateBasedConverter class:
            file (Path): The input markup file to be converted.
            format (str): The format to convert the file to.
            target_file (Path): The output file after conversion.
            batch_mode (bool): Whether running in batch mode.
            output_dir (Optional[Path]): Output directory for batch conversions.

    Methods:
        build_command(self) -> None: Builds the appropriate command for conversion.
        _build_default_command(self) -> None: Builds the default fallback command.

    Dependencies:
        - Pandoc (for all markup conversions)
    """

    MARKUP_FORMATS = {
        "HTML",
        "HTM",
        "MD",
        "XML",
    }

    def build_command(self) -> None:
        """
        Build command for markup conversion.

        Uses the template system from settings.json:
        1. Checks markup_rules.format_commands for target format
        2. Falls back to markup_rules.command_template if no specific command
        3. Uses _build_default_command as last resort
        """
        logger.debug(
            "Building markup conversion command for: {} -> {}",
            self.file,
            self.target_file,
        )
        self.build_command_from_template(self._build_default_command)
        logger.debug("Markup conversion command built: {}", self.command)

    def _build_default_command(self) -> None:
        """
        Build the default fallback command for markup conversion.

        This is only used if no template is found in settings.json.
        Default behavior: use Pandoc for all markup conversions.
        """
        logger.debug(
            "Building default markup conversion command for format: {}", self.format
        )

        # Pandoc target format mapping
        format_map = {
            "HTML": "html",
            "HTM": "html",
            "MD": "markdown",
            "XML": "docbook",
        }

        pandoc_format = format_map.get(self.format, self.format.lower())

        self.command = [
            "pandoc",
            str(self.file),
            "-o",
            str(self.target_file),
            "-t",
            pandoc_format,
        ]
        logger.debug("Using Pandoc for markup conversion: {}", self.command)
