#!/usr/bin/python3
"""
Subprocess execution utilities for converters.

Provides utilities for executing subprocesses with common patterns.
"""

import contextlib
import shlex
import subprocess
import time
from pathlib import Path
from typing import Callable, List, Optional, Tuple, Union

from simplyconvertfile.utils import text


class SubprocessResult:
    """Result of subprocess execution."""

    def __init__(
        self,
        returncode: int,
        stdout: str = "",
        stderr: str = "",
        command: str = "",
    ):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.command = command
        self.success = returncode == 0

    @property
    def error_output(self) -> str:
        """Get error output (stderr or stdout if stderr is empty)."""
        return self.stderr or self.stdout or text.OPERATION_FAILED_MESSAGE


class SubprocessExecutor:
    """Executes subprocesses with common patterns."""

    @staticmethod
    def run_command(
        command: Union[str, List[str]],
        shell: bool = False,
        cwd: Optional[Path] = None,
        timeout: Optional[int] = None,
    ) -> SubprocessResult:
        """
        Run a command and return result.

        Args:
            command: Command to run (string for shell, list otherwise)
            shell: Whether to use shell execution
            cwd: Working directory
            timeout: Timeout in seconds

        Returns:
            SubprocessResult: Result of command execution
        """
        cmd_str = command if isinstance(command, str) else " ".join(command)

        try:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                cwd=str(cwd) if cwd else None,
                timeout=timeout,
            )

            return SubprocessResult(
                returncode=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                command=cmd_str,
            )

        except subprocess.TimeoutExpired:
            return SubprocessResult(
                returncode=-1,
                stderr="Command timed out",
                command=cmd_str,
            )
        except Exception as e:
            return SubprocessResult(
                returncode=-1,
                stderr=str(e),
                command=cmd_str,
            )

    @staticmethod
    def run_shell_command(
        command: str, cwd: Optional[Path] = None, timeout: Optional[int] = None
    ) -> SubprocessResult:
        """
        Run a shell command.

        Args:
            command: Shell command string
            cwd: Working directory
            timeout: Timeout in seconds

        Returns:
            SubprocessResult: Result of command execution
        """
        return SubprocessExecutor.run_command(
            command, shell=True, cwd=cwd, timeout=timeout
        )

    @staticmethod
    def run_regular_command(
        command: Union[str, List[str]],
        cwd: Optional[Path] = None,
        timeout: Optional[int] = None,
    ) -> SubprocessResult:
        """
        Run a regular (non-shell) command.

        Args:
            command: Command string or list
            cwd: Working directory
            timeout: Timeout in seconds

        Returns:
            SubprocessResult: Result of command execution
        """
        cmd_list = shlex.split(command) if isinstance(command, str) else command
        return SubprocessExecutor.run_command(
            cmd_list, shell=False, cwd=cwd, timeout=timeout
        )

    @staticmethod
    def run_chained_commands(
        commands: List[List[str]],
        cwd: Optional[Path] = None,
        shell_builtins: Optional[set] = None,
    ) -> Tuple[bool, Optional[str], int]:
        """
        Run chained commands sequentially.

        Args:
            commands: List of command lists
            cwd: Working directory
            shell_builtins: Set of shell builtin commands

        Returns:
            Tuple[bool, Optional[str], int]: (success, error_message, failed_step_index)
        """
        if not commands:
            return False, "No commands to execute", -1

        shell_builtins = shell_builtins or set()

        # Check if any command needs shell execution
        needs_shell = any(
            cmd[0] in shell_builtins if cmd else False for cmd in commands
        )

        if needs_shell:
            # Execute all commands in shell
            command_str = " && ".join(" ".join(cmd) for cmd in commands)
            result = SubprocessExecutor.run_shell_command(command_str, cwd=cwd)

            return (
                (True, None, -1) if result.success else (False, result.error_output, 0)
            )
        # Execute commands sequentially without shell
        for i, cmd in enumerate(commands):
            result = SubprocessExecutor.run_regular_command(cmd, cwd=cwd)

            if not result.success:
                error_msg = text.CHAINED_COMMAND_STEP_FAILED_MESSAGE.format(
                    step=i + 1,
                    total=len(commands),
                    error=result.error_output,
                    command=" ".join(cmd),
                )
                return False, error_msg, i

        return True, None, -1

    @staticmethod
    def run_cancellable_command(
        command: Union[str, List[str]],
        shell: bool = False,
        cwd: Optional[Path] = None,
        cancel_check: Optional[Callable[[], bool]] = None,
        poll_interval: float = 0.05,
    ) -> SubprocessResult:
        """
        Run a command with cancellation support.

        Args:
            command: Command to run (string for shell, list otherwise)
            shell: Whether to use shell execution
            cwd: Working directory
            cancel_check: Callable that returns True if cancellation requested
            poll_interval: How often to check for cancellation (seconds)

        Returns:
            SubprocessResult: Result of command execution
        """
        cmd_str = command if isinstance(command, str) else " ".join(command)

        # Check for cancellation before starting the subprocess
        if cancel_check and cancel_check():
            return SubprocessResult(
                returncode=-1,
                stderr=text.OPERATION_CANCELLED_BY_USER_MESSAGE,
                command=cmd_str,
            )

        try:
            process = subprocess.Popen(
                command,
                shell=shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.DEVNULL,
                text=True,
                cwd=str(cwd) if cwd else None,
            )

            # Drain stdout/stderr in background threads to prevent
            # pipe buffer deadlock (OS pipe buffer is ~64KB on Linux;
            # ffmpeg can easily fill it with progress output on stderr,
            # causing the process to block on write() and appear hung).
            import threading

            stdout_chunks = []
            stderr_chunks = []

            def _drain_stdout():
                try:
                    for line in process.stdout:
                        stdout_chunks.append(line)
                except Exception:
                    pass

            def _drain_stderr():
                try:
                    for line in process.stderr:
                        stderr_chunks.append(line)
                except Exception:
                    pass

            stdout_thread = threading.Thread(target=_drain_stdout, daemon=True)
            stderr_thread = threading.Thread(target=_drain_stderr, daemon=True)
            stdout_thread.start()
            stderr_thread.start()

            # Poll for completion or cancellation
            while process.poll() is None:
                # Check for cancellation more frequently
                for _ in range(5):  # Check 5 times per poll_interval
                    if cancel_check and cancel_check():
                        # Send SIGKILL immediately to ensure process termination
                        with contextlib.suppress(Exception):
                            process.kill()
                        # Wait for drain threads to finish after kill
                        stdout_thread.join(timeout=2)
                        stderr_thread.join(timeout=2)
                        return SubprocessResult(
                            returncode=-1,
                            stderr=text.OPERATION_CANCELLED_BY_USER_MESSAGE,
                            command=cmd_str,
                        )
                    time.sleep(
                        poll_interval / 5
                    )  # Sleep for 0.01 seconds between checks

            # Wait for drain threads to finish
            stdout_thread.join(timeout=5)
            stderr_thread.join(timeout=5)

            stdout = "".join(stdout_chunks)
            stderr = "".join(stderr_chunks)

            return SubprocessResult(
                returncode=process.returncode,
                stdout=stdout,
                stderr=stderr,
                command=cmd_str,
            )

        except Exception as e:
            return SubprocessResult(
                returncode=-1,
                stderr=str(e),
                command=cmd_str,
            )


class ProcessManager:
    """Manages long-running subprocess execution."""

    def __init__(
        self,
        command: Union[str, List[str]],
        shell: bool = False,
        capture_output: bool = True,
        cwd: Optional[Path] = None,
    ):
        """
        Initialize process manager.

        Args:
            command: Command to execute
            shell: Whether to use shell execution
            capture_output: Whether to capture stdout/stderr
            cwd: Working directory for the process
        """
        self.command = command
        self.shell = shell
        self.capture_output = capture_output
        self.cwd = cwd
        self.process: Optional[subprocess.Popen] = None

    def start(self) -> subprocess.Popen:
        """
        Start the process.

        Returns:
            subprocess.Popen: The running process
        """
        stdout = subprocess.PIPE if self.capture_output else None
        stderr = subprocess.PIPE if self.capture_output else None

        self.process = subprocess.Popen(
            self.command,
            shell=self.shell,
            stdout=stdout,
            stderr=stderr,
            universal_newlines=self.capture_output,
            cwd=str(self.cwd) if self.cwd else None,
        )
        return self.process

    def terminate(self, timeout: int = 1) -> None:
        """
        Terminate the process gracefully.

        Args:
            timeout: Seconds to wait before killing
        """
        if not self.process:
            return

        try:
            self.process.terminate()
            self.process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            self.process.kill()
            with contextlib.suppress(subprocess.TimeoutExpired):
                self.process.wait(timeout=timeout)
        except Exception:
            pass

    def get_result(self, timeout: int = 1) -> SubprocessResult:
        """
        Get process result.

        Args:
            timeout: Timeout for communicate

        Returns:
            SubprocessResult: Process execution result
        """
        if not self.process:
            return SubprocessResult(-1, stderr=text.PROCESS_NOT_STARTED_MESSAGE)

        try:
            if self.capture_output:
                stdout, stderr = self.process.communicate(timeout=timeout)
            else:
                self.process.wait(timeout=timeout)
                stdout, stderr = "", ""

            cmd_str = (
                self.command
                if isinstance(self.command, str)
                else " ".join(self.command)
            )

            return SubprocessResult(
                returncode=self.process.returncode,
                stdout=stdout,
                stderr=stderr,
                command=cmd_str,
            )
        except subprocess.TimeoutExpired:
            return SubprocessResult(
                returncode=-1,
                stderr="Timeout waiting for process output",
            )
