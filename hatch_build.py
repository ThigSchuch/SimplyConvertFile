"""Hatch build hook to compile .po translation files into .mo files."""

import subprocess
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class TranslationBuildHook(BuildHookInterface):
    """Compile .po files to .mo during wheel/sdist build."""

    PLUGIN_NAME = "translation-compiler"

    def initialize(self, version, build_data):
        """Compile all .po files to .mo in the correct directory structure."""
        po_dir = Path(self.root) / "src" / "simplyconvertfile" / "po"
        if not po_dir.exists():
            return

        for po_file in po_dir.glob("*.po"):
            lang = po_file.stem
            out_dir = po_dir / lang / "LC_MESSAGES"
            out_dir.mkdir(parents=True, exist_ok=True)
            mo_file = out_dir / "simplyconvertfile.mo"

            # Skip if .mo is newer than .po
            if mo_file.exists() and mo_file.stat().st_mtime >= po_file.stat().st_mtime:
                continue

            try:
                subprocess.run(
                    ["msgfmt", "-o", str(mo_file), str(po_file)],
                    check=True,
                    capture_output=True,
                )
            except (subprocess.CalledProcessError, FileNotFoundError):
                # msgfmt not available — skip silently
                pass
