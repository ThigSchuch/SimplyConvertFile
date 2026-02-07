---
layout: default
title: Command Security
parent: Configuration
nav_order: 5
---

# Command Security
{: .no_toc }

Protection against dangerous commands in conversion templates.

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Overview

Since conversion commands are defined in JSON templates and executed via shell, a malicious or accidental template could run destructive operations on your system. The command security system inspects every command **before execution** and blocks anything deemed dangerous.

This protection applies to all commands — from default `settings.json`, user overrides in `user_settings.json`, and special rules.

## How It Works

Every command passes through a single execution chokepoint (`CommandExecutor`). Before any command runs, the sanitizer:

1. Splits the command string on shell operators (`&&`, `||`, `|`, `;`)
2. Extracts the executable name from each sub-command
3. Strips path prefixes (e.g., `/usr/bin/rm` → `rm`)
4. Checks against the blocked commands list

If a dangerous command is detected, execution is **blocked** and an error is shown.

## Blocked Commands

| Category | Commands | Reason |
|:---------|:---------|:-------|
| Privilege escalation | `sudo`, `su`, `pkexec`, `doas` | No conversion needs root access |
| File deletion | `rm`, `rmdir`, `shred`, `unlink`, `truncate` | Could destroy user files |
| Disk operations | `dd`, `mkfs`, `fdisk`, `parted`, `wipefs`, `blkdiscard` | Could damage disks/partitions |
| System control | `shutdown`, `reboot`, `poweroff`, `halt`, `init`, `systemctl` | Could disrupt the system |
| Network access | `curl`, `wget`, `nc`, `ncat`, `netcat`, `ssh`, `scp`, `rsync`, `ftp` | Could exfiltrate data |
| Permission changes | `chmod`, `chown`, `chgrp` | Could alter file permissions |
| Shell execution | `eval`, `exec` | Could run arbitrary code |

## Allowed Commands

Common tools used in legitimate conversion templates are **not** blocked:

- `ffmpeg`, `convert`, `pandoc`, `libreoffice` — conversion tools
- `python3`, `perl`, `ruby` — scripting interpreters used in templates
- `mv`, `cp`, `cat`, `cd` — file operations used in multi-step conversions
- `bash`, `sh`, `test` — shell utilities

These pass through with zero overhead.

## Configuration

### Default Behavior

By default, dangerous commands are **hard-blocked** with no option to proceed:

```json
"allow_dangerous_commands": false
```

The conversion fails and an error message is shown explaining which command was blocked and why.

### Allowing with Confirmation

If you have a legitimate need for a blocked command in a custom template, you can enable confirmation mode:

```json
"allow_dangerous_commands": true
```

Add this to your `user_settings.json`:

```bash
nano ~/.config/simplyconvertfile/user_settings.json
```

```json
{
    "allow_dangerous_commands": true
}
```

With this enabled, dangerous commands trigger a **confirmation dialog** instead of a hard block. You must explicitly click "Continue Anyway" to proceed. The Cancel button is the default action.

{: .warning }
> Only enable this if you fully understand the commands in your custom templates. A malicious template could still cause damage if you confirm execution.

## Examples

### Blocked Command

A template containing `rm` would be blocked:

```json
{
    "from": "MP4",
    "to": "MP3",
    "command": "ffmpeg -i '{input}' '{output}' && rm '{input}'"
}
```

Error: `Blocked command 'rm' detected (file deletion)`

### Safe Command

A template using only conversion tools passes through normally:

```json
{
    "from": "JSON",
    "to": "YAML",
    "command": "python3 -c \"import json, yaml; yaml.dump(json.load(open('{input}')), open('{output}', 'w'))\""
}
```

### Path-Prefixed Commands

Full paths are also detected — `/usr/bin/sudo`, `/bin/rm`, etc. are stripped to their base name before checking.
