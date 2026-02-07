# #!/usr/bin/python3
# """
# Archive converter implementation.

# This module provides archive conversion functionality using various archive tools.
# Supports conversion between archive formats by extracting and recompressing content.
# """

# import traceback
# from pathlib import Path
# from typing import List, Optional

# from simplyconvertfile.config.settings import get_converter_template, settings_manager
# from simplyconvertfile.converters.base import TemplateBasedConverter
# from simplyconvertfile.converters.helpers import (
#     CommandBuilder,
#     CommandParser,
#     CommandExecutor,
#     TempFileManager,
#     ToolValidator,
#     ProgressManager,
#     CommandExecutionResult,
# )
# from simplyconvertfile.utils import dependency_manager, text
# from simplyconvertfile.utils.logging import logger


# class ArchiveExtractor:
#     """Helper class for archive extraction operations."""

#     DEFAULT_EXTRACTION_TEMPLATE = "7z x '{input}' -o'{output_dir}/' -y"

#     def __init__(self, converter: "ArchiveConverter"):
#         self.converter = converter

#     def extract_archive(self) -> bool:
#         """Extract the source archive to temporary directory.

#         Returns:
#             bool: True if extraction succeeded, False otherwise.
#         """
#         if not self.converter.temp_dir:
#             self.converter.error_manager.set_error(
#                 text.Errors.TEMP_DIR_NOT_AVAILABLE_MESSAGE
#             )
#             return False

#         try:
#             template = self._get_extraction_template()
#             cmd_str = CommandBuilder.build_archive_extraction(
#                 template, self.converter.file, self.converter.temp_dir
#             )

#             if not self._validate_and_execute_command(cmd_str):
#                 return False

#             return True

#         except Exception as e:
#             error_msg = str(e)
#             error_msg = f"{error_msg}\n\nTraceback:\n{traceback.format_exc()}"
#             self.converter.error_manager.set_error(error_msg)
#             return False

#     def _get_extraction_template(self) -> str:
#         """Get the extraction template for the source file format."""
#         source_ext = self.converter.file.suffix[1:].upper()
#         archive_config: dict = settings_manager.get("archive_rules", {})
#         template = archive_config.get("extraction_templates", {}).get(
#             source_ext,
#             archive_config.get("extraction_default", self.DEFAULT_EXTRACTION_TEMPLATE),
#         )

#         if isinstance(template, (list, tuple)):
#             template = " ".join(str(t) for t in template)
#         elif not isinstance(template, str):
#             template = str(template)

#         return template

#     def _validate_and_execute_command(self, cmd_str: str) -> bool:
#         """Validate tools and execute the extraction command."""
#         is_shell = CommandParser.is_shell_command(cmd_str)
#         cmd_list = []

#         if is_shell:
#             tool_name = cmd_str.split()[0]
#             if not self.converter.tool_validator.check_tool(tool_name):
#                 return self.converter._handle_missing_tool(tool_name, cmd_str)
#         else:
#             cmd_list, _ = CommandParser.parse_command(cmd_str)
#             tool_name = cmd_list[0]
#             if not self.converter.tool_validator.check_tool(tool_name):
#                 return self.converter._handle_missing_tool(tool_name, cmd_str)

#         result = CommandExecutor.run_cancellable_command(
#             cmd_str if is_shell else cmd_list,
#             shell=is_shell,
#             cwd=self.converter.temp_dir,
#             cancel_check=lambda: self.converter.progress_tracker._cancelled,
#         )

#         if not result.success:
#             # Check if this was due to cancellation
#             if (
#                 "cancelled" in result.error_output.lower()
#                 or "cancel" in result.error_output.lower()
#             ):
#                 self.converter.progress_tracker._cancelled = True
#             else:
#                 self.converter.error_manager.set_error(result.error_output, cmd_str)
#             return False

#         return True

#     def _handle_missing_tool(self, tool_name: str, command_str: str) -> bool:
#         """Handle missing tool dependency."""
#         install_cmd = dependency_manager.get_install_instructions(tool_name)
#         if install_cmd:
#             if self.converter.batch_mode:
#                 self.converter.error_manager.set_error(
#                     text.Errors.MISSING_TOOL_ERROR_DETAILS.format(
#                         tool=tool_name,
#                         install_command=install_cmd,
#                     ),
#                     command_str,
#                 )
#             else:
#                 self.converter.conversion_manager.show_missing_tool_dialog(
#                     tool_name, install_cmd, self.converter.batch_mode, command_str
#                 )
#         return False


# class ArchiveCreator:
#     """Helper class for archive creation operations."""

#     def __init__(self, converter: "ArchiveConverter"):
#         self.converter = converter

#     def create_archive(self) -> bool:
#         """Create the target archive from extracted contents.

#         Returns:
#             bool: True if archive creation succeeded, False otherwise.
#         """
#         contents = self._prepare_archive_contents()
#         if not contents:
#             return False

#         template = self._get_creation_template()
#         if not template:
#             return False

#         try:
#             command_str = CommandBuilder.build_archive_creation(
#                 template, self.converter.target_file, contents, self.converter.temp_dir
#             )

#             if not self._validate_and_execute_command(command_str, template, contents):
#                 return False

#             return True

#         except Exception as e:
#             self.converter.error_manager.set_error(str(e))
#             return False

#     def _prepare_archive_contents(self) -> List[Path]:
#         """Prepare archive contents and validate environment."""
#         if not self.converter.temp_dir or not self.converter.temp_dir.exists():
#             self.converter.error_manager.set_error(
#                 text.Errors.TEMP_DIR_DOES_NOT_EXIST_MESSAGE
#             )
#             return []

#         contents = list(self.converter.temp_dir.iterdir())
#         if not contents:
#             self.converter.error_manager.set_error(
#                 text.Errors.NO_CONTENTS_IN_ARCHIVE_MESSAGE
#             )
#             return []

#         self._update_target_for_compression_format(contents)
#         try:
#             self.converter.valid_target_file()
#         except Exception as e:
#             self.converter.error_manager.set_error(str(e))
#             return []

#         # Create parent directory if it doesn't exist
#         self.converter.target_file.parent.mkdir(parents=True, exist_ok=True)

#         return contents

#     def _get_creation_template(self) -> str:
#         """Get the creation template for the target format."""
#         template, _ = get_converter_template("archive", self.converter.format)
#         if not template:
#             return ""

#         if isinstance(template, (list, tuple)):
#             template = " ".join(str(t) for t in template)
#         elif not isinstance(template, str):
#             template = str(template)

#         return template

#     def _validate_and_execute_command(
#         self, command_str: str, template: str, contents: List[Path]
#     ) -> bool:
#         """Validate tools and execute the creation command."""
#         is_shell = "&&" in command_str
#         cmd = []

#         if is_shell:
#             tool_name = command_str.split()[0]
#             if not self.converter.tool_validator.check_tool(tool_name):
#                 return self.converter._handle_missing_tool(tool_name, command_str)
#         else:
#             cmd, _ = CommandParser.parse_command(command_str)
#             if "{input}" in template:
#                 cmd = CommandBuilder.add_input_files_to_command(cmd, contents)
#             tool_name = cmd[0]
#             if not self.converter.tool_validator.check_tool(tool_name):
#                 return self.converter._handle_missing_tool(tool_name, " ".join(cmd))

#         result = CommandExecutor.run_cancellable_command(
#             command_str if is_shell else cmd,
#             shell=is_shell,
#             cwd=self.converter.temp_dir,
#             cancel_check=lambda: self.converter.progress_tracker._cancelled,
#         )

#         if not result.success:
#             # Check if this was due to cancellation
#             if (
#                 "cancelled" in result.error_output.lower()
#                 or "cancel" in result.error_output.lower()
#             ):
#                 self.converter.progress_tracker._cancelled = True
#             else:
#                 self.converter.error_manager.set_error(result.error_output, command_str)
#             return False

#         return True

#     def _update_target_for_compression_format(self, contents: List[Path]) -> None:
#         """Update target file name for compression-only formats."""
#         compression_only_formats: set[str] = {
#             fmt.upper() for fmt in settings_manager.get("compression_only_formats", [])
#         }

#         if (
#             self.converter.format.upper() in compression_only_formats
#             and len(contents) > 1
#         ):
#             compression_ext = self.converter.format.lower()
#             self.converter.target_file = (
#                 self.converter.target_file.parent
#                 / f"{self.converter.target_file.stem}.tar.{compression_ext}"
#             )


# class ArchiveConverter(TemplateBasedConverter):
#     """
#     Converter for archive formats using various archive tools.

#     This converter extracts source archives and recompresses them into
#     the target format, properly handling the archive contents rather than
#     creating a new archive containing the old archive file.

#     The conversion process is two-phase:
#     1. Extract the source archive to a temporary directory
#     2. Create a new archive from the extracted contents

#     All configuration (compression formats, tool mappings, etc.) is loaded
#     from settings.json and can be customized by users in user_settings.json.

#     Attributes:
#         temp_dir (Optional[Path]): Temporary extraction directory
#         temp_dir_manager (Optional[TempFileManager]): Manager for temp directory lifecycle
#         tool_validator (ToolValidator): Validator for tool availability
#         extractor (ArchiveExtractor): Helper for extraction operations
#         creator (ArchiveCreator): Helper for creation operations
#     """

#     def __init__(self, file: Path, format: str, **kwargs) -> None:
#         """Initialize the archive converter with temporary directory management.

#         Sets up the archive converter with tool validation and temporary directory
#         management for extraction and recompression operations.

#         Args:
#             file: Path to the source archive file.
#             format: Target archive format (e.g., "ZIP", "TAR.GZ").
#             **kwargs: Additional arguments passed to parent Converter class,
#                      including batch_mode for tool validation.

#         Examples:
#             >>> converter = ArchiveConverter(Path("/tmp/archive.zip"), "TAR.GZ")
#             >>> converter.temp_dir_manager is not None
#             True
#         """
#         self.temp_dir: Optional[Path] = None
#         self.temp_dir_manager: Optional[TempFileManager] = None
#         self.tool_validator = ToolValidator(batch_mode=kwargs.get("batch_mode", False))
#         self._missing_tool_info: Optional[tuple] = (
#             None  # Store missing tool info for later
#         )
#         super().__init__(file, format, **kwargs)

#         # Initialize helper classes
#         self.extractor = ArchiveExtractor(self)
#         self.creator = ArchiveCreator(self)

#     def _build_default_command(self) -> None:
#         """Build the default archive conversion command.

#         Archive conversion is a two-phase process that doesn't fit the simple
#         single-command pattern. This method sets up the basic command structure
#         and delegates the actual conversion logic to the convert() method.
#         """
#         logger.debug("Building default archive conversion setup")
#         # Archive conversion requires temp directory setup, handled in convert()
#         self.command = ["7z", "x", str(self.file), f"-o{self.target_file.parent}"]
#         logger.debug("Archive conversion default command built: {}", self.command)

#     def convert(self) -> bool:
#         """
#         Execute archive conversion: extract source, create target archive.

#         Note: Direct conversions (e.g., GZ->BZ2) are handled by special_rules
#         in the factory before this converter is even instantiated.

#         Returns:
#             bool: True if conversion succeeded, False otherwise
#         """
#         logger.info(
#             "Starting archive conversion: {} -> {}", self.file, self.target_file
#         )

#         # Set up temporary directory for extraction
#         try:
#             self.temp_dir_manager = TempFileManager(is_dir=True)
#             self.temp_dir = self.temp_dir_manager.__enter__()
#         except Exception as e:
#             logger.error("Failed to create temp directory: {}", str(e))
#             self.error_manager.set_error(text.Errors.FAILED_TO_CREATE_TEMP_DIR_MESSAGE)
#             return False

#         try:
#             # Create progress manager for UI feedback
#             progress_manager = ProgressManager(
#                 batch_mode=self.batch_mode,
#                 cancel_callback=self.progress_tracker.create_cancel_callback(),
#             )

#             # Execute both phases with progress tracking
#             result = self._execute_archive_conversion_with_progress(progress_manager)

#             # Check if a tool was missing and show dialog after progress dialog closes
#             if self._missing_tool_info and not self.batch_mode:
#                 tool_name, install_cmd, command_str = self._missing_tool_info
#                 self.conversion_manager.show_missing_tool_dialog(
#                     tool_name, install_cmd, self.batch_mode, command_str
#                 )
#                 return False

#             # Handle cancellation cleanup
#             if not result.success and result.cancelled:
#                 logger.info("Archive conversion was cancelled by user")
#                 self._delete_target_file()
#                 return False

#             return result.success

#         finally:
#             self._cleanup_temp_directory()

#     def _execute_archive_conversion_with_progress(
#         self, progress_manager: ProgressManager
#     ) -> CommandExecutionResult:
#         """Execute the complete archive conversion with progress tracking.

#         Shows a single progress dialog that covers both extraction and creation phases.

#         Args:
#             progress_manager: Progress manager for UI feedback.

#         Returns:
#             CommandExecutionResult: Result of the conversion operation.
#         """
#         message = text.UI.CONVERSION_PROGRESS_LABEL.format(
#             file=self.file.name, extension=self.format
#         )

#         def conversion_func() -> CommandExecutionResult:
#             # Phase 1: Extract source archive
#             if not self.extractor.extract_archive():
#                 # Check if this was due to cancellation
#                 if self.progress_tracker._cancelled:
#                     return CommandExecutionResult(
#                         success=False,
#                         error_message="Archive extraction cancelled",
#                         cancelled=True,
#                     )
#                 return CommandExecutionResult(
#                     success=False,
#                     error_message="Archive extraction failed",
#                     cancelled=False,
#                 )

#             # Check for cancellation before proceeding to creation
#             if self.progress_tracker._cancelled:
#                 return CommandExecutionResult(
#                     success=False,
#                     error_message="Archive conversion cancelled before creation",
#                     cancelled=True,
#                 )

#             # Phase 2: Create target archive
#             if not self.creator.create_archive():
#                 # Check if this was due to cancellation
#                 if self.progress_tracker._cancelled:
#                     return CommandExecutionResult(
#                         success=False,
#                         error_message="Archive creation cancelled",
#                         cancelled=True,
#                     )
#                 return CommandExecutionResult(
#                     success=False,
#                     error_message="Archive creation failed",
#                     cancelled=False,
#                 )

#             return CommandExecutionResult(success=True)

#         return progress_manager.execute_with_progress(
#             conversion_func, message, timeout_ms=100
#         )

#     def _cleanup_temp_directory(self) -> None:
#         """Clean up temporary directory if it exists."""
#         if self.temp_dir_manager:
#             self.temp_dir_manager.__exit__(None, None, None)
#             self.temp_dir_manager = None
#             self.temp_dir = None

#     def _handle_missing_tool(self, tool_name: str, command_str: str) -> bool:
#         """Handle missing tool dependency with consistent error reporting.

#         Provides unified missing tool handling for both extraction and creation phases,
#         ensuring consistent error messages and dialog behavior.

#         Args:
#             tool_name: Name of the missing tool.
#             command_str: The command string that requires the tool.

#         Returns:
#             bool: Always returns False to indicate failure.
#         """
#         install_cmd = dependency_manager.get_install_instructions(tool_name)
#         if install_cmd:
#             if self.batch_mode:
#                 self.error_manager.set_error(
#                     text.Errors.MISSING_TOOL_ERROR_DETAILS.format(
#                         tool=tool_name,
#                         install_command=install_cmd,
#                     ),
#                     command_str,
#                 )
#             else:
#                 # Store missing tool info for later dialog display (after progress dialog closes)
#                 self._missing_tool_info = (tool_name, install_cmd, command_str)
#         else:
#             # Fallback error message when no install instructions available
#             error_msg = text.Errors.MISSING_TOOL_MESSAGE.format(tool=tool_name)
#             if self.batch_mode:
#                 self.error_manager.set_error(error_msg, command_str)
#             else:
#                 self.error_manager.show_error_dialog(
#                     error_msg,
#                     self.file,
#                     self.file.suffix[1:].upper() if self.file.suffix else "UNKNOWN",
#                     self.format,
#                     command=[command_str] if command_str else None,
#                     last_command=command_str,
#                 )
#         return False
