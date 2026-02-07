#!/usr/bin/python3
"""
Multi-file conversion handler for organizing output files into separate folders.

This module manages conversions that produce multiple output files (e.g., animated
GIF to static images, PDF to images) by organizing them into dedicated folders
to keep the source directory clean and organized.

Classes:
    MultiFileHandler: Handles detection and management of multi-file conversions.
"""

from pathlib import Path
from typing import Optional, Tuple

from simplyconvertfile.config.settings import settings_manager
from simplyconvertfile.utils.logging import logger


class MultiFileHandler:
    """Handles multi-file conversion scenarios by organizing outputs into folders.

    When converting animated GIFs or PDFs to static image formats, ImageMagick
    creates multiple files (frames or pages). This handler detects such scenarios,
    creates unique output folders, and organizes the output into a dedicated folder
    to maintain directory cleanliness.

    Attributes:
        source_file: Path to the source file.
        source_format: Format of the source file (uppercase).
        target_format: Target format for conversion (uppercase).

    Examples:
        >>> handler = MultiFileHandler(Path("animation.gif"), "GIF", "PNG")
        >>> is_multi, output_dir = handler.should_use_multi_file_output()
        >>> if is_multi:
        ...     print(f"Use multi-file mode, output to: {output_dir}")
    """

    def __init__(
        self, source_file: Path, source_format: str, target_format: str
    ) -> None:
        """Initialize the multi-file handler.

        Args:
            source_file: Path to the source file being converted.
            source_format: Format of the source file (will be uppercased).
            target_format: Target format for conversion (will be uppercased).
        """
        self.source_file = source_file
        self.source_format = source_format.upper()
        self.target_format = target_format.upper()

    def should_use_multi_file_output(self) -> Tuple[bool, Optional[Path]]:
        """Determine if this conversion should use multi-file output organization.

        Checks the multi_file_conversions configuration to see if the combination
        of source and target formats matches any pattern that produces multiple files.
        Creates a unique output folder to avoid conflicts with previous conversions.

        Returns:
            Tuple[bool, Optional[Path]]: A tuple containing:
                - bool: True if multi-file output should be used
                - Optional[Path]: The folder path where files should be organized,
                                or None if multi-file output is not applicable

        Examples:
            >>> handler = MultiFileHandler(Path("anim.gif"), "GIF", "PNG")
            >>> is_multi, output_dir = handler.should_use_multi_file_output()
            >>> if is_multi:
            ...     print(f"Frames will be saved to: {output_dir}")
        """
        try:
            config = settings_manager.get("multi_file_conversions", {})
            if not config.get("enabled", False):
                logger.debug("Multi-file conversions disabled in settings")
                return False, None

            patterns = config.get("patterns", [])

            for pattern in patterns:
                if (
                    pattern.get("from") == self.source_format
                    and self.target_format in pattern.get("to", [])
                ):
                    logger.debug(
                        "Found multi-file pattern: {} -> {}",
                        self.source_format,
                        self.target_format,
                    )

                    output_folder = self._create_unique_output_folder(pattern)
                    return True, output_folder

            logger.debug(
                "No multi-file pattern found for {} -> {}",
                self.source_format,
                self.target_format,
            )
            return False, None

        except Exception as e:
            logger.error("Error checking multi-file conversion: {}", str(e))
            return False, None

    def _create_unique_output_folder(self, pattern: dict) -> Path:
        """Create a unique output folder for multi-file conversions.

        Generates a folder name based on the source file, suffix, and target format.
        If the folder already exists, appends a counter (1), (2), etc. to ensure
        uniqueness without overwriting previous conversions.

        Args:
            pattern: The multi-file pattern dictionary containing folder configuration.

        Returns:
            Path: The path to the output folder.

        Examples:
            >>> source = Path("/home/user/animation.gif")
            >>> pattern = {"folder_suffix": "_frames"}
            >>> handler = MultiFileHandler(source, "GIF", "PNG")
            >>> folder = handler._create_unique_output_folder(pattern)
            >>> print(folder)
            /home/user/animation_frames_PNG
        """
        suffix = pattern.get("folder_suffix", "_output")
        base_name = self.source_file.stem

        # Create base folder name: basename_suffix_format
        base_folder_name = f"{base_name}{suffix}_{self.target_format}"

        output_folder = self.source_file.parent / base_folder_name
        counter = 1

        # Ensure uniqueness by appending counter if folder exists
        while output_folder.exists():
            folder_name = f"{base_folder_name} ({counter})"
            output_folder = self.source_file.parent / folder_name
            counter += 1

        try:
            output_folder.mkdir(parents=True, exist_ok=True)
            logger.debug("Created unique multi-file output folder: {}", output_folder)
        except Exception as e:
            logger.error("Failed to create output folder {}: {}", output_folder, str(e))
            raise

        return output_folder

    def get_multi_file_output_pattern(self, pattern: dict, target_extension: str) -> str:
        """Get the output filename pattern for multi-file conversion.

        Generates the filename pattern that ImageMagick will use to create
        individual files, replacing Python placeholders with values that
        ImageMagick understands (like %05d for sequence numbers).

        Args:
            pattern: The multi-file pattern dictionary.
            target_extension: Target file extension (lowercase, without dot).

        Returns:
            str: The filename pattern ready for ImageMagick (e.g., 'video_frame_%05d.png')

        Examples:
            >>> pattern = {"output_filename_pattern": "{input_stem}_frame_%05d.{ext}"}
            >>> handler = MultiFileHandler(Path("anim.gif"), "GIF", "PNG")
            >>> template = handler.get_multi_file_output_pattern(pattern, "png")
            >>> print(template)
            'anim_frame_%05d.png'
        """
        filename_pattern = pattern.get(
            "output_filename_pattern", "{input_stem}_%05d.{ext}"
        )

        # Replace placeholders with actual values
        result = filename_pattern.format(
            input_stem=self.source_file.stem, ext=target_extension.lower()
        )

        logger.debug("Generated output filename pattern: {}", result)
        return result

    @staticmethod
    def is_multi_file_conversion(source_format: str, target_format: str) -> bool:
        """Static method to check if a conversion is multi-file without creating handler.

        Useful for quick checks before handler instantiation.

        Args:
            source_format: Format of the source file (uppercase).
            target_format: Target format for conversion (uppercase).

        Returns:
            bool: True if this conversion produces multiple files.

        Examples:
            >>> is_multi = MultiFileHandler.is_multi_file_conversion("GIF", "PNG")
            >>> print(is_multi)
            True
        """
        try:
            config = settings_manager.get("multi_file_conversions", {})
            if not config.get("enabled", False):
                return False

            patterns = config.get("patterns", [])

            for pattern in patterns:
                if (
                    pattern.get("from") == source_format.upper()
                    and target_format.upper() in pattern.get("to", [])
                ):
                    return True

            return False

        except Exception as e:
            logger.error("Error checking if conversion is multi-file: {}", str(e))
            return False
