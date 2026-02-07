---
layout: default
title: Debug Mode
parent: Reference
nav_order: 4
---

# Debug Mode

Enable verbose logging by creating the DEBUG trigger file:

```bash
mkdir -p ~/.config/simplyconvertfile
touch ~/.config/simplyconvertfile/DEBUG
```

Logs are printed to stdout with color-coded levels.

To disable debug mode, simply remove the file:

```bash
rm ~/.config/simplyconvertfile/DEBUG
```
