
import pytest
import tempfile
import os
from pathlib import Path
from datetime import datetime, timedelta
from auditlogs import AuditLogger, LogLevel, log_info, log_error

class TestAuditLogs:
    def test_audit_logger_creation(self):
        """Test AuditLogger creation with custom directory and machine name"""
        with tempfile.TemporaryDirectory() as temp_dir:
            logger = AuditLogger(temp_dir, "test-machine")
            assert logger.log_dir == Path(temp_dir)
            assert logger.machine_name == "test-machine"
            assert (Path(temp_dir) / "log.txt").exists()
    
    def test_log_creation(self):
        """Test log writing functionality with machine name"""
        with tempfile.TemporaryDirectory() as temp_dir:
            logger = AuditLogger(temp_dir, "test-server")
            logger.log("Test message", LogLevel.INFO)
            
            # Check if log file was created and contains message and machine name
            log_file = Path(temp_dir) / "log.txt"
            assert log_file.exists()
            
            with open(log_file, 'r') as f:
                content = f.read()
                assert "Test message" in content
                assert "test-server" in content
                assert "[INFO]" in content
    
    def test_daily_rotation(self):
        """Test daily log file rotation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            logger = AuditLogger(temp_dir)
            
            # Create a log file with yesterday's timestamp
            log_file = Path(temp_dir) / "log.txt"
            log_file.touch()
            
            # Set modification time to yesterday
            yesterday = datetime.now() - timedelta(days=1)
            os.utime(log_file, (yesterday.timestamp(), yesterday.timestamp()))
            
            # Initialize new logger which should trigger rotation
            new_logger = AuditLogger(temp_dir)
            new_logger.log("New message", LogLevel.INFO)
            
            # Check if yesterday's file was renamed
            yesterday_files = list(Path(temp_dir).glob("*_log.txt"))
            assert len(yesterday_files) >= 1
    
    def test_global_functions(self):
        """Test global convenience functions"""
        with tempfile.TemporaryDirectory() as temp_dir:
            from auditlogs import initialize_logger
            initialize_logger(temp_dir, "global-test")
            
            # These should work without raising exceptions
            log_info("Global info test")
            log_error("Global error test")
            
            log_file = Path(temp_dir) / "log.txt"
            assert log_file.exists()

def test_machine_name_detection():
    """Test machine name detection works"""
    from auditlogs import get_machine_name
    machine_name = get_machine_name()
    assert isinstance(machine_name, str)
    assert len(machine_name) > 0