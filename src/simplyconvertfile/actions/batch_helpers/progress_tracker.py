#!/usr/bin/python3
"""
Progress tracking for batch conversions.

This module provides progress UI and state management for batch
file conversion operations.
"""

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List, Optional

from simplyconvertfile.config import settings_manager
from simplyconvertfile.ui import Gtk, ProgressbarDialogWindow
from simplyconvertfile.utils import text


@dataclass
class BatchConversionState:
    """Consolidated state for batch conversion tracking."""

    current_index: int = 0
    successful_conversions: int = 0
    cancelled: bool = False
    cancelling: bool = False
    running: bool = False

    def reset(self) -> None:
        """Reset state for new conversion."""
        self.current_index = 0
        self.successful_conversions = 0
        self.cancelled = False
        self.cancelling = False
        self.running = False


class BatchProgressTracker:
    """
    Handles progress UI and state management for batch conversions.

    Provides progress dialog management, cancellation handling, and
    state tracking for batch file conversion operations.
    """

    CANCELLING_TIMEOUT_COUNTER = 0
    MAX_CANCELLING_TIMEOUTS = 50
    PROGRESS_UPDATE_TIMEOUT_MS = 10

    def __init__(self, valid_files: List[Path], target_format: str):
        self.valid_files = valid_files
        self.target_format = target_format
        self.state = BatchConversionState()
        self._progress_window: Optional[ProgressbarDialogWindow] = None
        self._cancelling_timeout_counter = self.CANCELLING_TIMEOUT_COUNTER
        self._max_cancelling_timeouts = self.MAX_CANCELLING_TIMEOUTS
        self._progress_update_timeout_ms = self.PROGRESS_UPDATE_TIMEOUT_MS

        # Callbacks
        self._on_cancel_callback: Optional[Callable[[], None]] = None
        self._on_progress_update_callback: Optional[Callable[[], None]] = None

    def set_cancel_callback(self, callback: Callable[[], None]) -> None:
        """Set callback to be called when conversion is cancelled."""
        self._on_cancel_callback = callback

    def set_progress_update_callback(self, callback: Callable[[], None]) -> None:
        """Set callback to be called on progress updates."""
        self._on_progress_update_callback = callback

    def create_progress_dialog(self) -> None:
        """Create and configure the progress dialog."""
        self._progress_window = ProgressbarDialogWindow(
            message=text.BATCH_CONVERSION_PROGRESS_MESSAGE.format(
                file=self.valid_files[0].name,
                extension=self.target_format,
                current=1,
                total=len(self.valid_files),
            ),
            timeout_callback=self._handle_progress_timeout,
            timeout_ms=self._progress_update_timeout_ms,
        )

        if self._progress_window:
            self._progress_window.progressbar.set_fraction(0.0)
            self._setup_dialog_event_handlers()

    def _setup_dialog_event_handlers(self) -> None:
        """Set up event handlers for the progress dialog."""
        if not self._progress_window:
            return

        # Connect to the dialog's response signal to detect cancellation
        def on_response(dialog, response_id):
            if response_id in (
                Gtk.ResponseType.CANCEL,
                Gtk.ResponseType.DELETE_EVENT,
            ):
                self.state.cancelled = True
                self.state.cancelling = True
                self.state.running = False

                if self._on_cancel_callback:
                    self._on_cancel_callback()

                self._handle_cancellation_ui()

        self._progress_window.dialog.connect("response", on_response)

        # Also connect to delete-event for window close button
        def on_delete_event(dialog, event):
            self.state.cancelled = True
            self.state.cancelling = True
            self.state.running = False

            if self._on_cancel_callback:
                self._on_cancel_callback()

            self._handle_cancellation_ui()
            return False  # Allow the dialog to close

        self._progress_window.dialog.connect("delete-event", on_delete_event)

    def run_progress_dialog(self) -> None:
        """Run the progress dialog and handle completion."""
        if self._progress_window:
            self._progress_window.run()
            self._progress_window.destroy()

    def _handle_progress_timeout(self, _, progress_window) -> bool:
        """
        Handle progress timeout callback.

        Returns:
            bool: True to continue, False to stop
        """
        # If cancelling, wait for any running conversion to finish
        if self.state.cancelling:
            return self._handle_cancellation_timeout()

        # Check for cancellation first
        if self.state.cancelled:
            self.state.running = False
            return False

        if not self.state.running or not self.target_format:
            return False

        if self.state.current_index < len(self.valid_files):
            return self._handle_active_conversion(progress_window)
        else:
            return self._handle_all_files_completed(progress_window)

    def _handle_cancellation_timeout(self) -> bool:
        """Handle timeout during cancellation. Returns True to continue waiting."""
        # Check if we should continue waiting or force cleanup
        self._cancelling_timeout_counter += 1

        if self._cancelling_timeout_counter >= self._max_cancelling_timeouts:
            # Force cleanup and close
            if self._progress_window:
                self._progress_window.dialog.emit("response", Gtk.ResponseType.CANCEL)
            return False

        # Keep waiting - pulse the progress bar
        if self._progress_window:
            self._progress_window.progressbar.pulse()
        return True

    def _handle_active_conversion(self, progress_window) -> bool:
        """Handle active conversion progress. Returns True to continue."""
        self._update_progress_display(progress_window)

        # Pulse the progress bar if a conversion is running
        if (
            hasattr(self, "_on_progress_update_callback")
            and self._on_progress_update_callback
        ):
            progress_window.progressbar.pulse()

        if self._on_progress_update_callback:
            self._on_progress_update_callback()

        return True

    def _handle_all_files_completed(self, progress_window) -> bool:
        """Handle completion of all files. Returns False to stop progress updates."""
        self.state.running = False
        progress_window.dialog.emit("response", Gtk.ResponseType.OK)
        return False

    def _update_progress_display(self, progress_window) -> None:
        """Update progress bar and message."""
        progress_fraction = self.state.current_index / len(self.valid_files)
        progress_window.progressbar.set_fraction(progress_fraction)
        progress_window.set_message(
            text.BATCH_CONVERSION_PROGRESS_MESSAGE.format(
                file=self.valid_files[self.state.current_index].name,
                extension=self.target_format,
                current=self.state.current_index + 1,
                total=len(self.valid_files),
            )
        )

        # Process UI events
        while Gtk.events_pending():
            Gtk.main_iteration()
        time.sleep(0.1)  # Small delay for visibility

        # Check for cancellation after UI update
        if self.state.cancelled:
            raise Exception(text.BATCH_CONVERSION_CANCELLED_MESSAGE)

    def _handle_cancellation_ui(self) -> None:
        """Update UI to show cancellation is in progress."""
        if not self._progress_window:
            return

        # Update cancel button text to "Cancelling..."
        action_area = self._progress_window.dialog.get_action_area()
        if action_area:
            buttons = action_area.get_children()
            for button in buttons:
                if isinstance(button, Gtk.Button):
                    # Check if this is the cancel button by looking at its label
                    label = button.get_label()
                    if label == text.CANCEL_BUTTON_LABEL:
                        button.set_label(text.CANCELLING_BUTTON_LABEL)
                        button.set_sensitive(False)  # Disable the button
                        break

        # Process pending GTK events to keep UI responsive
        while Gtk.events_pending():
            Gtk.main_iteration()

    def is_cancelled(self) -> bool:
        """Check if the conversion has been cancelled."""
        return self.state.cancelled

    def increment_success_count(self) -> None:
        """Increment the successful conversions counter."""
        self.state.successful_conversions += 1

    def move_to_next_file(self) -> None:
        """Move to the next file in the batch."""
        self.state.current_index += 1

    def get_current_file(self) -> Optional[Path]:
        """Get the current file being processed."""
        if self.state.current_index < len(self.valid_files):
            return self.valid_files[self.state.current_index]
        return None

    def is_complete(self) -> bool:
        """Check if all files have been processed."""
        return self.state.current_index >= len(self.valid_files)
