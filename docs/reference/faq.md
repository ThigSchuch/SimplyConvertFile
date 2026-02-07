---
layout: default
title: FAQ
parent: Reference
nav_order: 2
---

# Frequently Asked Questions

---

**Q: Can I convert multiple different file types at once?**
: Yes, batch conversion supports files from different format groups, but the target format dropdown will only show formats that work for all selected files.

**Q: Does it preserve metadata (EXIF, ID3 tags)?**
: Depends on the format and conversion. Some converters preserve metadata, others strip it. You can customize this in `user_settings.json`.

**Q: Can I convert entire folders?**
: Select all files within a folder for batch conversion. Recursive folder conversion is not currently supported.

**Q: Is there a size limit for conversions?**
: No built-in limit, but very large files (>1GB) may take significant time. Monitor system resources during conversion.

**Q: Can I use this on other desktop environments?**
: Yes! Unlike the original Nemo action, SimplyConvertFile is a standalone application that works on any Linux desktop environment with GTK 3 support.

**Q: Does it support drag-and-drop?**
: Not currently. Use the file picker or pass files as command line arguments.

**Q: How is this related to the convert-file Nemo action?**
: SimplyConvertFile was originally developed as a Cinnamon Nemo action (`convert-file@thigschuch`). It has been refactored into a standalone application that works independently of any file manager, while retaining all the original functionality and adding new features like the GUI file picker and expanded format support.
