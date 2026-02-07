---
layout: default
title: Notifications
parent: Configuration
nav_order: 4
---

# Notification Settings

Configure desktop notifications for different conversion events.

---

## Configuration

```json
"notifications": {
    "enabled": true,
    "on_start": false,
    "on_success": true,
    "on_failure": true,
    "on_cancel": true,
    "on_batch_start": false,
    "on_batch_finish": true,
    "on_batch_cancel": true,
    "on_batch_step_start": false,
    "on_batch_step_success": false,
    "on_batch_step_failure": true,
    "on_missing_dependency": true,
    "on_settings_corrupted": true
}
```

## Notification Types

| Setting | Description |
|:--------|:------------|
| `enabled` | Master switch to enable/disable all notifications |
| `on_start` | When a single conversion begins |
| `on_success` | When a single conversion completes successfully |
| `on_failure` | When a single conversion fails |
| `on_cancel` | When the user cancels a single conversion |
| `on_batch_start` | When a batch conversion begins |
| `on_batch_finish` | When a batch conversion completes (with success/failure summary) |
| `on_batch_cancel` | When the user cancels a batch conversion |
| `on_batch_step_start` | When each file in a batch starts processing |
| `on_batch_step_success` | When each file in a batch completes successfully |
| `on_batch_step_failure` | When an individual file in a batch fails |
| `on_missing_dependency` | When a required tool is not installed |
| `on_settings_corrupted` | When a configuration file has issues |

## Example Override

To disable step-by-step notifications but keep batch summaries:

```json
{
    "notifications": {
        "on_batch_step_start": false,
        "on_batch_step_success": false,
        "on_batch_step_failure": false,
        "on_batch_finish": true
    }
}
```
