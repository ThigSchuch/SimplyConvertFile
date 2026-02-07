#!/usr/bin/python3
"""
Document converter implementation.

This module provides document conversion functionality using LibreOffice, Pandoc,
and other specialized tools. Tool selection is configured via settings.json.
"""

from simplyconvertfile.converters.base import TemplateBasedConverter
from simplyconvertfile.utils.logging import logger


class DocumentConverter(TemplateBasedConverter):
    """
    A converter for document formats using LibreOffice, Pandoc, or specialized tools.

    This converter relies entirely on the template system in settings.json for
    tool selection and command building. The format_commands in document_rule
    determine which tool to use for each format.

    Configuration (from settings.json):
        - format_commands: Specific commands for each format
        - command_template: Default fallback command (usually pandoc)

    Attributes:
        Inherits all attributes from the base TemplateBasedConverter class:
            file (Path): The input document file to be converted.
            format (str): The format to convert the document file to.
            target_file (Path): The output document file after conversion.
            batch_mode (bool): Whether running in batch mode.
            output_dir (Optional[Path]): Output directory for batch conversions.

    Methods:
        build_command(self) -> None: Builds the appropriate command for document conversion.
        _build_default_command(self) -> None: Builds the default fallback command.

    Dependencies:
        - LibreOffice (for office documents and PDF conversion)
        - Pandoc (for markup and text conversions)
        - Calibre's ebook-convert (for MOBI/EPUB conversions)
    """

    DOCUMENT_FORMATS = {
        "PDF",
        "DOCX",
        "ODT",
        "RTF",
        "XLSX",
        "ODS",
        "CSV",
        "PPTX",
        "ODP",
    }

    def build_command(self) -> None:
        """
        Build command for document conversion.

        Uses the template system from settings.json:
        1. Checks format_commands for target format
        2. Falls back to command_template if no specific command
        3. Uses _build_default_command as last resort
        """
        logger.debug(
            "Building document conversion command for: {} -> {}",
            self.file,
            self.target_file,
        )
        self.build_command_from_template(self._build_default_command)
        logger.debug("Document conversion command built: {}", self.command)

    def _build_default_command(self) -> None:
        """
        Build the default fallback command for document conversion.

        This is only used if no template is found in settings.json.
        Default behavior: use pandoc for general document conversions.
        """
        logger.debug(
            "Building default document conversion command for format: {}", self.format
        )
        if self.format in self.DOCUMENT_FORMATS:
            self.command = [
                "libreoffice",
                "--headless",
                "--convert-to",
                self.format.lower(),
                "--outdir",
                str(self.target_file.parent),
                str(self.file),
            ]
            logger.debug("Using LibreOffice for document conversion: {}", self.command)
        else:
            self.command = [
                "pandoc",
                str(self.file),
                "-o",
                str(self.target_file),
            ]
            logger.debug("Using Pandoc for document conversion: {}", self.command)
