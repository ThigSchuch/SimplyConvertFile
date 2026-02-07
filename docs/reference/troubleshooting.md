---
layout: default
title: Troubleshooting
parent: Reference
nav_order: 1
---

# Troubleshooting
{: .no_toc }

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## "Command not found" or "Missing dependency" errors

**Problem:** The required conversion tool is not installed.

**Solution:** Install the missing tool using your package manager:

```bash
# For image conversions
sudo apt install imagemagick

# For audio/video conversions
sudo apt install ffmpeg

# For document conversions
sudo apt install libreoffice pandoc calibre poppler-utils

# For archive conversions
sudo apt install p7zip-full rar genisoimage rpm2cpio cpio lzop xz-utils
```

See [Dependencies]({% link getting-started/dependencies.md %}) for the full list.

## Conversion fails with "Invalid format" error

**Problem:** The source or target format is not recognized.

**Solutions:**
1. Ensure the file has the correct extension
2. Check that the format is listed in [Supported Formats]({% link formats.md %})
3. Try a different target format from the same group
4. Check `conversion_exclusions` in settings — the conversion pair may be explicitly excluded

## LibreOffice conversions fail silently

**Problem:** LibreOffice returns success even when conversion fails, causing misleading errors.

**Solution:** This is automatically handled by the [file validation system]({% link usage/advanced.md %}#automatic-file-validation). If you see errors like "File validation failed: /tmp/file.odt", check the previous command's output shown in the error dialog for the actual LibreOffice error.

## Batch conversion stops after one file

**Problem:** An error occurred and wasn't handled properly.

**Solutions:**
1. Check the error dialog for specific information
2. Try converting files individually to identify the problematic one
3. Ensure all selected files are valid and not corrupted

## Low quality output

**Problem:** Default quality settings may not meet your needs.

**Solutions:**
1. Edit `user_settings.json` to increase quality parameters (see [Format Templates]({% link configuration/format-templates.md %}))
2. For JPEG: Increase `-quality` value (85–100)
3. For MP3: Increase bitrate `-b:a` (256k or 320k)
4. For video: Decrease `-crf` value (18–23 for high quality)

## Slow conversion speed

**Problem:** Complex conversions or large files take time.

**Solutions:**
1. For video: Use faster presets (`-preset fast` or `-preset ultrafast`)
2. Enable hardware acceleration in FFmpeg (if supported)
3. Process fewer files at once
4. Close other resource-intensive applications

See also [Performance Tips]({% link reference/performance.md %}).

## Getting Help

If you encounter issues not covered here:

1. **Check the error message** — it often contains specific information about what went wrong
2. **Enable debug mode** — create `~/.config/simplyconvertfile/DEBUG` for detailed logs (see [Debug Mode]({% link reference/debug.md %}))
3. **Verify dependencies** — run the conversion command manually in terminal to test
4. **Report bugs** — [open an issue on GitHub](https://github.com/ThigSchuch/SimplyConvertFile/issues) with:
   - Operating system and version
   - Installed tool versions (`convert --version`, `ffmpeg -version`, etc.)
   - Error message and steps to reproduce
