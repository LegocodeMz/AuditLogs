"""
AuditLogs - A Python package for structured audit logging with daily file rotation
"""

__version__ = "0.1.0"

from .core import (
    AuditLogger,
    log,
    log_info,
    log_warning,
    log_error,
    log_debug,
    initialize_logger
)
from .config import LogLevel, LOG_DIR, DEFAULT_LOG_DIR, MACHINE_NAME, get_machine_name

__all__ = [
    'AuditLogger',
    'log',
    'log_info',
    'log_warning',
    'log_error',
    'log_debug',
    'initialize_logger',
    'LogLevel',
    'LOG_DIR',
    'DEFAULT_LOG_DIR',
    'MACHINE_NAME',
    'get_machine_name'
]

# Initialize the global logger on import
initialize_logger()