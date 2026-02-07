#!/usr/bin/python3
"""
Office and e-book converter implementation.

This module provides conversion functionality for office documents and e-books using
LibreOffice, Pandoc, and Calibre's ebook-convert tool. Supports various formats including
DOCX, ODT, RTF, PDF, EPUB, and MOBI.
"""

from simplyconvertfile.converters.base import TemplateBasedConverter
from simplyconvertfile.utils.logging import logger


class OfficeConverter(TemplateBasedConverter):
    """
    A converter for office documents and e-books.

    This converter handles conversions between office formats (DOCX, ODT, RTF),
    e-book formats (EPUB, MOBI), and PDF using LibreOffice, Pandoc, and
    ebook-convert based on the target format.

    Configuration (from settings.json):
        - office_rules.format_commands: Specific commands for each format
        - office_rules.command_template: Default fallback command (usually LibreOffice)

    Attributes:
        Inherits all attributes from the base TemplateBasedConverter class:
            file (Path): The input file to be converted.
            format (str): The format to convert the file to.
            target_file (Path): The output file after conversion.
            batch_mode (bool): Whether running in batch mode.
            output_dir (Optional[Path]): Output directory for batch conversions.

    Methods:
        build_command(self) -> None: Builds the appropriate command for conversion.
        _build_default_command(self) -> None: Builds the default fallback command.

    Dependencies:
        - LibreOffice (for DOCX, ODT, RTF, PDF conversions)
        - Pandoc (for additional document conversions)
        - Calibre's ebook-convert (for EPUB/MOBI conversions)
    """

    LIBREOFFICE_FORMATS = {
        "PDF",
        "DOCX",
        "ODT",
        "RTF",
    }

    EBOOK_FORMATS = {
        "EPUB",
        "MOBI",
    }

    def build_command(self) -> None:
        """
        Build command for office/e-book conversion.

        Uses the template system from settings.json:
        1. Checks office_rules.format_commands for target format
        2. Falls back to office_rules.command_template if no specific command
        3. Uses _build_default_command as last resort
        """
        logger.debug(
            "Building office conversion command for: {} -> {}",
            self.file,
            self.target_file,
        )
        self.build_command_from_template(self._build_default_command)
        logger.debug("Office conversion command built: {}", self.command)

    def _build_default_command(self) -> None:
        """
        Build the default fallback command for office/e-book conversion.

        This is only used if no template is found in settings.json.
        Default behavior:
        - Use LibreOffice for office formats and PDF
        - Use ebook-convert for e-book formats
        - Use Pandoc as general fallback
        """
        logger.debug(
            "Building default office conversion command for format: {}", self.format
        )

        if self.format in self.LIBREOFFICE_FORMATS:
            self.command = [
                "libreoffice",
                "--headless",
                "--convert-to",
                self.format.lower(),
                "--outdir",
                str(self.target_file.parent),
                str(self.file),
            ]
            logger.debug("Using LibreOffice for office conversion: {}", self.command)
        elif self.format in self.EBOOK_FORMATS:
            self.command = [
                "ebook-convert",
                str(self.file),
                str(self.target_file),
                "--enable-heuristics",
            ]
            logger.debug("Using ebook-convert for e-book conversion: {}", self.command)
        else:
            # Fallback to Pandoc for other formats
            self.command = [
                "pandoc",
                str(self.file),
                "-o",
                str(self.target_file),
            ]
            logger.debug("Using Pandoc for office conversion: {}", self.command)
