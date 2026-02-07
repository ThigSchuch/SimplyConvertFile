#!/usr/bin/python3
"""
Data format converter implementation.

This module provides conversion functionality for data formats using
Pandoc and Python scripts. Supports JSON, YAML, YML, and TXT formats.
"""

from simplyconvertfile.converters.base import TemplateBasedConverter
from simplyconvertfile.utils.logging import logger


class DataConverter(TemplateBasedConverter):
    """
    A converter for data formats.

    This converter handles conversions between data formats (JSON, YAML, TXT)
    using Pandoc for text conversions and Python scripts for data format conversions.

    Configuration (from settings.json):
        - data_rules.format_commands: Specific commands for each format
        - data_rules.command_template: Default fallback command (Pandoc)

    Attributes:
        Inherits all attributes from the base TemplateBasedConverter class:
            file (Path): The input data file to be converted.
            format (str): The format to convert the file to.
            target_file (Path): The output file after conversion.
            batch_mode (bool): Whether running in batch mode.
            output_dir (Optional[Path]): Output directory for batch conversions.

    Methods:
        build_command(self) -> None: Builds the appropriate command for conversion.
        _build_default_command(self) -> None: Builds the default fallback command.

    Dependencies:
        - Pandoc (for text-based conversions)
        - Python 3 with yaml module (for JSON/YAML conversions)
    """

    DATA_FORMATS = {
        "JSON",
        "YAML",
        "YML",
        "TXT",
    }

    def build_command(self) -> None:
        """
        Build command for data format conversion.

        Uses the template system from settings.json:
        1. Checks data_rules.format_commands for target format
        2. Falls back to data_rules.command_template if no specific command
        3. Uses _build_default_command as last resort
        """
        logger.debug(
            "Building data conversion command for: {} -> {}",
            self.file,
            self.target_file,
        )
        self.build_command_from_template(self._build_default_command)
        logger.debug("Data conversion command built: {}", self.command)

    def _build_default_command(self) -> None:
        """
        Build the default fallback command for data format conversion.

        This is only used if no template is found in settings.json.
        Default behavior: use Pandoc for text conversions.
        """
        logger.debug(
            "Building default data conversion command for format: {}", self.format
        )

        # For TXT conversions, use Pandoc
        if self.format == "TXT":
            self.command = [
                "pandoc",
                str(self.file),
                "-o",
                str(self.target_file),
                "-t",
                "plain",
            ]
            logger.debug("Using Pandoc for data conversion: {}", self.command)
        else:
            # For other data formats, use Pandoc with appropriate output format
            format_map = {
                "JSON": "json",
                "YAML": "markdown",
                "YML": "markdown",
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
            logger.debug("Using Pandoc for data conversion: {}", self.command)
