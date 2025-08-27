import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Union
from .config import LOG_DIR, LogLevel, MACHINE_NAME

class AuditLogger:
    """Main audit logging class with daily file rotation"""
    
    def __init__(self, log_dir: Optional[Union[str, Path]] = None, 
                 machine_name: Optional[str] = None):
        """
        Initialize audit logger
        
        Args:
            log_dir: Directory to store audit logs. If None, uses default from config
            machine_name: Custom machine name for logging. If None, uses system hostname
        """
        self.log_dir = Path(log_dir) if log_dir else LOG_DIR
        self.machine_name = machine_name if machine_name else MACHINE_NAME
        self.today_log_file = self.log_dir / "log.txt"
        
        os.makedirs(self.log_dir, exist_ok=True)
        self._rotate_daily_logs()
    
    def _rotate_daily_logs(self):
        """Rotate logs based on date - rename yesterday's log file"""
        if self.today_log_file.exists():
            last_modified = datetime.fromtimestamp(self.today_log_file.stat().st_mtime)
            if last_modified.date() < datetime.now().date():
                # Rename yesterday's log file
                yesterday_file = self.log_dir / f"{last_modified.strftime('%Y%m%d')}_log.txt"
                
                # Handle case where yesterday file already exists
                counter = 1
                original_yesterday_file = yesterday_file
                while yesterday_file.exists():
                    yesterday_file = self.log_dir / f"{last_modified.strftime('%Y%m%d')}_log_{counter}.txt"
                    counter += 1
                
                try:
                    self.today_log_file.rename(yesterday_file)
                except Exception as e:
                    # If rename fails, we'll just continue with the current file
                    pass
    
    def log(self, message: str, level: LogLevel = LogLevel.INFO):
        """
        Write formatted log message
        
        Args:
            message: The log message to write
            level: Log level (INFO, WARNING, ERROR, DEBUG)
        """
        try:
            with open(self.today_log_file, "a", encoding="utf-8") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = f"{timestamp} [{level.value}] - {self.machine_name} | {message}\n"
                f.write(log_entry)
                
                # Also print to console for immediate feedback
                print(log_entry.strip())
                
        except Exception as e:
            print(f"Failed to write log: {e}")
    
    def info(self, message: str):
        """Log info message"""
        self.log(message, LogLevel.INFO)
    
    def warning(self, message: str):
        """Log warning message"""
        self.log(message, LogLevel.WARNING)
    
    def error(self, message: str):
        """Log error message"""
        self.log(message, LogLevel.ERROR)
    
    def debug(self, message: str):
        """Log debug message"""
        self.log(message, LogLevel.DEBUG)
    
    def get_log_files(self):
        """Get list of all log files in the directory"""
        return sorted(self.log_dir.glob("*.txt"), key=os.path.getmtime, reverse=True)
    
    def clear_logs(self, keep_last_n: int = 10):
        """Clear old log files, keeping only the most recent ones"""
        log_files = self.get_log_files()
        if len(log_files) > keep_last_n:
            for old_file in log_files[keep_last_n:]:
                try:
                    old_file.unlink()
                except Exception as e:
                    print(f"Failed to delete log file {old_file}: {e}")

# Global instance for easy import
_audit_logger = AuditLogger()

# Convenience functions
def log(message: str, level: LogLevel = LogLevel.INFO):
    """Write formatted log message using global logger"""
    _audit_logger.log(message, level)

def log_info(message: str):
    """Log info message"""
    _audit_logger.info(message)

def log_warning(message: str):
    """Log warning message"""
    _audit_logger.warning(message)

def log_error(message: str):
    """Log error message"""
    _audit_logger.error(message)

def log_debug(message: str):
    """Log debug message"""
    _audit_logger.debug(message)

def initialize_logger(log_dir: Optional[Union[str, Path]] = None, 
                     machine_name: Optional[str] = None):
    """
    Initialize the global logger with custom settings
    
    Args:
        log_dir: Custom log directory
        machine_name: Custom machine name
    """
    global _audit_logger
    _audit_logger = AuditLogger(log_dir, machine_name)