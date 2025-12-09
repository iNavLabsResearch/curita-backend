"""
Logging service for the application
"""
import logging
import sys
import json
import contextvars
from pathlib import Path
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from typing import Optional, Dict, Any
from pythonjsonlogger import jsonlogger

# Context variable for request ID
request_id_ctx_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "request_id", default=None
)


class CorrelationIdFilter(logging.Filter):
    """
    Logging filter to inject request ID into log records
    """
    def filter(self, record):
        record.request_id = request_id_ctx_var.get() or "N/A"
        return True


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """
    Custom JSON formatter with support for additional fields
    """
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        
        # Add correlation ID
        log_record['request_id'] = getattr(record, 'request_id', 'N/A')
        
        # Add timestamp if not present
        if not log_record.get('timestamp'):
            log_record['timestamp'] = self.formatTime(record, self.datefmt)
            
        # Add level
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[96m',      # Bright Cyan
        'INFO': '\033[92m',       # Bright Green
        'WARNING': '\033[93m',    # Bright Yellow
        'ERROR': '\033[91m',      # Bright Red
        'CRITICAL': '\033[95m',   # Bright Magenta
    }
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    GRAY = '\033[90m'
    
    def format(self, record):
        # Store original levelname
        original_levelname = record.levelname
        
        # Get color for level
        color = self.COLORS.get(original_levelname, '')
        
        # Ensure request_id exists
        if not hasattr(record, 'request_id'):
            record.request_id = 'N/A'
        
        # Format the message (basic)
        formatted = super().format(record)
        
        # Split into parts
        parts = formatted.split('|', 3)
        if len(parts) >= 3:
            # Reconstruct slightly differently
            timestamp = parts[0]
            level = parts[1]
            message = parts[-1]
            
            # Add icons
            icons = {
                'DEBUG': '🔍',
                'INFO': '✓',
                'WARNING': '⚠️',
                'ERROR': '❌',
                'CRITICAL': '🔥',
            }
            icon = icons.get(original_levelname, '•')
            
            # Color the level
            colored_level = f"{self.BOLD}{color}{level.strip()}{self.RESET}"
            
            # Dim the timestamp
            dim_timestamp = f"{self.GRAY}{timestamp.strip()}{self.RESET}"
            
            # Request ID
            req_id_str = f"[{record.request_id}]" if record.request_id != 'N/A' else ""
            req_id_fmt = f"{self.DIM}{req_id_str}{self.RESET}"
            
            return f"{icon}  {dim_timestamp} {req_id_fmt} {colored_level}  {message.strip()}"
        
        return formatted


class LoggerService:
    """Centralized logging service"""
    
    _loggers = {}
    _initialized = False
    
    @classmethod
    def setup_logging(cls):
        """Setup logging configuration for the application"""
        if cls._initialized:
            return
            
        # Import here to avoid circular imports
        from app.core.config import get_settings
        settings = get_settings()
        
        cls._initialized = True
        
        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, settings.LOG_LEVEL))
        
        # Remove existing handlers
        root_logger.handlers.clear()
        
        # Filter for correlation ID
        correlation_filter = CorrelationIdFilter()
        
        # --- Formatters ---
        
        # 1. Standard File Formatter
        file_formatter = logging.Formatter(
            fmt='%(asctime)s - [%(request_id)s] - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 2. JSON Formatter (if enabled)
        if settings.LOG_JSON_FORMAT:
            json_fmt = CustomJsonFormatter(
                '%(timestamp)s %(level)s %(name)s %(message)s %(request_id)s'
            )
            file_formatter = json_fmt
            
        # 3. Console Formatter
        console_formatter = ColoredFormatter(
            fmt='%(asctime)s|%(levelname)-8s|%(message)s',
            datefmt='%H:%M:%S'
        )
        
        # --- Handlers ---
        
        # 1. Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
        console_handler.setFormatter(console_formatter)
        console_handler.addFilter(correlation_filter)
        root_logger.addHandler(console_handler)
        
        # 2. File Handlers (if enabled)
        if settings.LOG_FILE_ENABLED:
            # A. App Log (All logs) - Rotating 10MB
            app_handler = RotatingFileHandler(
                filename="logs/app.log",
                maxBytes=settings.LOG_FILE_MAX_BYTES,
                backupCount=settings.LOG_FILE_BACKUP_COUNT
            )
            app_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
            app_handler.setFormatter(file_formatter)
            app_handler.addFilter(correlation_filter)
            root_logger.addHandler(app_handler)
            
            # B. Error Log (Errors only) - Rotating 10MB
            error_handler = RotatingFileHandler(
                filename="logs/error.log",
                maxBytes=settings.LOG_FILE_MAX_BYTES,
                backupCount=settings.LOG_FILE_BACKUP_COUNT
            )
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(file_formatter)
            error_handler.addFilter(correlation_filter)
            root_logger.addHandler(error_handler)
            
            # C. Access Log (API requests) - Daily Rotation
            # We create a specific handler but don't add it to root.
            # It will be used by the access logger specifically.
            access_handler = TimedRotatingFileHandler(
                filename="logs/access.log",
                when="midnight",
                interval=1,
                backupCount=7
            )
            access_handler.setFormatter(file_formatter)
            access_handler.addFilter(correlation_filter)
            access_handler.setLevel(logging.INFO)
            
            # Configure dedicated access logger
            access_logger = logging.getLogger("api.access")
            access_logger.propagate = False # Don't duplicate to app.log
            access_logger.addHandler(access_handler)
            access_logger.addHandler(console_handler) # Also show in console
        
        # Suppress third-party library logs
        logging.getLogger('tensorflow').setLevel(logging.ERROR)
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        logging.getLogger('httpx').setLevel(logging.WARNING)
        logging.getLogger('watchfiles').setLevel(logging.WARNING)
        # Apply our colored formatter to uvicorn loggers
        for logger_name in ['uvicorn', 'uvicorn.error', 'uvicorn.access']:
            uvicorn_logger = logging.getLogger(logger_name)
            uvicorn_logger.handlers.clear()
            uvicorn_logger.addHandler(console_handler)
            uvicorn_logger.propagate = False
    
    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Get or create a logger instance
        
        Args:
            name: Name of the logger (usually __name__)
            
        Returns:
            Logger instance
        """
        # Ensure logging is setup
        if not cls._initialized:
            cls.setup_logging()
            
        if name not in cls._loggers:
            logger = logging.getLogger(name)
            cls._loggers[name] = logger
        
        return cls._loggers[name]


def get_logger(name: str = __name__) -> logging.Logger:
    """
    Helper function to get a logger
    
    Args:
        name: Name of the logger (usually __name__)
        
    Returns:
        Logger instance
    """
    return LoggerService.get_logger(name)


# Logging utility functions
class LoggerMixin:
    """Mixin class to add logging capability to any class"""
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class"""
        return get_logger(self.__class__.__module__ + "." + self.__class__.__name__)
