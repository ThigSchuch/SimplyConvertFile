---
layout: default
title: Performance Tips
parent: Reference
nav_order: 3
---

# Performance Tips

---

## Optimizing Conversion Speed

1. **Video conversions** — Use hardware acceleration if available:
   ```json
   "MP4": "ffmpeg -hwaccel auto -i '{input}' -c:v h264_nvenc '{output}'"
   ```

2. **Batch conversions** — Process in smaller groups if memory is limited.

3. **Image conversions** — For large batches, reduce quality slightly for faster processing.

## Quality vs. Size Trade-offs

| Format Type | Best Compression | Notes |
|:------------|:-----------------|:------|
| **Images** | WEBP | Best compression with good quality |
| **Audio** | AAC 128k or Opus | Good quality at lower bitrates than MP3 |
| **Video** | H.265 (HEVC) | Better compression than H.264, but slower encoding |
| **Documents** | PDF/A for archival | Regular PDF for sharing |
