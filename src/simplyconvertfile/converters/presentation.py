#!/usr/bin/python3
"""
Presentation converter implementation.

This module provides conversion functionality for presentation formats using
LibreOffice. Supports PPTX and ODP formats.
"""

from simplyconvertfile.converters.base import TemplateBasedConverter
from simplyconvertfile.utils.logging import logger


class PresentationConverter(TemplateBasedConverter):
    """
    A converter for presentation formats.

    This converter handles conversions between presentation formats (PPTX, ODP)
    using LibreOffice's headless mode.

    Configuration (from settings.json):
        - presentation_rules.format_commands: Specific commands for each format
        - presentation_rules.command_template: Default fallback command (LibreOffice)

    Attributes:
        Inherits all attributes from the base TemplateBasedConverter class:
            file (Path): The input presentation file to be converted.
            format (str): The format to convert the file to.
            target_file (Path): The output file after conversion.
            batch_mode (bool): Whether running in batch mode.
            output_dir (Optional[Path]): Output directory for batch conversions.

    Methods:
        build_command(self) -> None: Builds the appropriate command for conversion.
        _build_default_command(self) -> None: Builds the default fallback command.

    Dependencies:
        - LibreOffice (for all presentation conversions)
    """

    PRESENTATION_FORMATS = {
        "PPTX",
        "ODP",
    }

    def build_command(self) -> None:
        """
        Build command for presentation conversion.

        Uses the template system from settings.json:
        1. Checks presentation_rules.format_commands for target format
        2. Falls back to presentation_rules.command_template if no specific command
        3. Uses _build_default_command as last resort
        """
        logger.debug(
            "Building presentation conversion command for: {} -> {}",
            self.file,
            self.target_file,
        )
        self.build_command_from_template(self._build_default_command)
        logger.debug("Presentation conversion command built: {}", self.command)

    def _build_default_command(self) -> None:
        """
        Build the default fallback command for presentation conversion.

        This is only used if no template is found in settings.json.
        Default behavior: use LibreOffice for all presentation conversions.
        """
        logger.debug(
            "Building default presentation conversion command for format: {}",
            self.format,
        )

        self.command = [
            "libreoffice",
            "--headless",
            "--convert-to",
            self.format.lower(),
            "--outdir",
            str(self.target_file.parent),
            str(self.file),
        ]
        logger.debug("Using LibreOffice for presentation conversion: {}", self.command)
