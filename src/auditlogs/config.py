import os
import socket
from pathlib import Path
from enum import Enum

class LogLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"

# Get machine name
def get_machine_name():
    """Get the current machine hostname"""
    try:
        return socket.gethostname()
    except:
        return "unknown-machine"

MACHINE_NAME = get_machine_name()

# Default paths
DEFAULT_LOG_DIR = Path.home() / "auditlogs"

# Get log directory from environment variable or use default
LOG_DIR = Path(os.environ.get("AUDIT_LOGS_DIR", DEFAULT_LOG_DIR))

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)