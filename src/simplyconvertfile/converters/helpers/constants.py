from simplyconvertfile.utils.text import text

Security = text.Security

SHELL_OPERATORS = ["|", "&&", "||", ">", ">>", "<", "<<"]

# Commands that are blocked from execution due to security risks.
# These are grouped by category for clarity and maintainability.
DANGEROUS_COMMANDS = {
    # Privilege escalation
    "sudo",
    "su",
    "pkexec",
    "doas",
    # File deletion / destruction
    "rm",
    "rmdir",
    "shred",
    "unlink",
    "truncate",
    # Disk / partition operations
    "dd",
    "mkfs",
    "fdisk",
    "parted",
    "wipefs",
    "blkdiscard",
    # System control
    "shutdown",
    "reboot",
    "poweroff",
    "halt",
    "init",
    "systemctl",
    # Network exfiltration
    "curl",
    "wget",
    "nc",
    "ncat",
    "netcat",
    "ssh",
    "scp",
    "rsync",
    "ftp",
    # Permission / ownership changes
    "chmod",
    "chown",
    "chgrp",
    # Shell code execution primitives
    "eval",
    "exec",
}

# Human-readable category labels for dangerous commands.
DANGEROUS_COMMAND_CATEGORIES = {
    "sudo": Security.CATEGORY_PRIVILEGE_ESCALATION,
    "su": Security.CATEGORY_PRIVILEGE_ESCALATION,
    "pkexec": Security.CATEGORY_PRIVILEGE_ESCALATION,
    "doas": Security.CATEGORY_PRIVILEGE_ESCALATION,
    "rm": Security.CATEGORY_FILE_DELETION,
    "rmdir": Security.CATEGORY_DIRECTORY_DELETION,
    "shred": Security.CATEGORY_FILE_DESTRUCTION,
    "unlink": Security.CATEGORY_FILE_DELETION,
    "truncate": Security.CATEGORY_FILE_TRUNCATION,
    "dd": Security.CATEGORY_RAW_DISK_OPERATION,
    "mkfs": Security.CATEGORY_FILESYSTEM_CREATION,
    "fdisk": Security.CATEGORY_DISK_PARTITIONING,
    "parted": Security.CATEGORY_DISK_PARTITIONING,
    "wipefs": Security.CATEGORY_FILESYSTEM_SIGNATURE_REMOVAL,
    "blkdiscard": Security.CATEGORY_BLOCK_DEVICE_DISCARD,
    "shutdown": Security.CATEGORY_SYSTEM_SHUTDOWN,
    "reboot": Security.CATEGORY_SYSTEM_REBOOT,
    "poweroff": Security.CATEGORY_SYSTEM_POWER_OFF,
    "halt": Security.CATEGORY_SYSTEM_HALT,
    "init": Security.CATEGORY_SYSTEM_INIT_CONTROL,
    "systemctl": Security.CATEGORY_SYSTEM_SERVICE_CONTROL,
    "curl": Security.CATEGORY_NETWORK_ACCESS,
    "wget": Security.CATEGORY_NETWORK_DOWNLOAD,
    "nc": Security.CATEGORY_NETWORK_CONNECTION,
    "ncat": Security.CATEGORY_NETWORK_CONNECTION,
    "netcat": Security.CATEGORY_NETWORK_CONNECTION,
    "ssh": Security.CATEGORY_REMOTE_SHELL_ACCESS,
    "scp": Security.CATEGORY_REMOTE_FILE_COPY,
    "rsync": Security.CATEGORY_REMOTE_FILE_SYNC,
    "ftp": Security.CATEGORY_FILE_TRANSFER,
    "chmod": Security.CATEGORY_PERMISSION_CHANGE,
    "chown": Security.CATEGORY_OWNERSHIP_CHANGE,
    "chgrp": Security.CATEGORY_GROUP_OWNERSHIP_CHANGE,
    "eval": Security.CATEGORY_SHELL_CODE_EXECUTION,
    "exec": Security.CATEGORY_SHELL_CODE_EXECUTION,
}
