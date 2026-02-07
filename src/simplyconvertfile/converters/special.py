#!/usr/bin/python3
"""
Special converter implementation.

This module provides special conversion functionality for complex conversions
that require custom command templates or multi-step processes.
"""


from simplyconvertfile.converters.base import TemplateBasedConverter
from simplyconvertfile.utils.logging import logger


class SpecialConverter(TemplateBasedConverter):
    """
    A converter that handles special conversion rules with custom commands.

    This converter uses the conversion rules defined in the format configuration
    to handle complex conversions that require specific command templates,
    multiple steps, or temporary files.

    Attributes:
        Inherits all attributes from the base Converter class plus:
            rule (ConversionRule): The special conversion rule to follow
    """

    def _build_default_command(self) -> None:
        """Build the default command for special conversion.

        Special converters rely entirely on templates from settings.json
        and do not provide default commands. This method is a no-op.

        Note:
            Special conversions are handled through the template system
            and special_rules configuration. No default fallback is provided.
        """
        logger.debug(
            "Building special conversion command for: {} -> {}",
            self.file,
            self.target_file,
        )
        # Special converters rely entirely on templates - no default command
        logger.debug("Special conversion command built (template-based)")
