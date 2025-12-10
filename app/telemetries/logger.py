import inspect
import json
import logging
import os
import sys
import threading
import time
from datetime import datetime

from loki_logger_handler.loki_logger_handler import LokiLoggerHandler

from app.telemetries.request_manager import RequestIdManager

grafana_loki_user = os.getenv("GRAFANA_LOKI_USER_ID")
grafana_loki_passowrd = os.getenv("GRAFANA_LOKI_PASSWORD")


# ANSI color codes for terminal output
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    # Level colors
    DEBUG = "\033[36m"      # Cyan
    INFO = "\033[32m"       # Green
    WARNING = "\033[33m"    # Yellow
    ERROR = "\033[31m"      # Red
    CRITICAL = "\033[35m"   # Magenta
    
    # Component colors
    TIMESTAMP = "\033[90m"  # Dark gray
    MESSAGE = "\033[97m"    # White
    TAG = "\033[96m"        # Bright cyan
    REQUEST_ID = "\033[93m" # Bright yellow


class StructuredLogger:
    def __init__(self, name: str, loki_url: str = None, labels: dict = None, loki_enabled: bool = False):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.logger.handlers.clear()

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(self._get_console_formatter())
        self.logger.addHandler(console_handler)

        # Loki handler
        if loki_enabled and loki_url:
            try:
                loki_handler = LokiLoggerHandler(
                    url=loki_url,
                    labels=labels or {"application": "curita_toy_backend"},
                    timeout=10,
                    enable_self_errors=True,
                    compressed=True,
                    auth=(grafana_loki_user, grafana_loki_passowrd),
                )
                loki_handler.setLevel(logging.INFO)
                loki_handler.setFormatter(self._get_loki_formatter())
                self.logger.addHandler(loki_handler)
                self.loki_connected = True
            except Exception as e:
                self.logger.warning(f"Failed to connect to Loki: {str(e)}. Continuing with console logging only.")
                self.loki_connected = False
        else:
            self.loki_connected = False

    def _get_console_formatter(self):
        """Formatter for console output with colors and better readability"""

        class ConsoleFormatter(logging.Formatter):
            def format(self, record):
                # Get level-specific color
                level_colors = {
                    "DEBUG": Colors.DEBUG,
                    "INFO": Colors.INFO,
                    "WARNING": Colors.WARNING,
                    "ERROR": Colors.ERROR,
                    "CRITICAL": Colors.CRITICAL,
                }
                level_color = level_colors.get(record.levelname, Colors.RESET)
                
                # Format timestamp
                timestamp = datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                
                # Get optional fields
                request_id = getattr(record, "request_id", RequestIdManager.get())
                tag = getattr(record, "tag", None)
                
                # Build the log line with colors
                parts = [
                    f"{Colors.TIMESTAMP}{timestamp}{Colors.RESET}",
                    f"{level_color}{Colors.BOLD}[{record.levelname:^8}]{Colors.RESET}",
                ]
                
                # Add request ID if present
                if request_id:
                    parts.append(f"{Colors.REQUEST_ID}[{request_id[:8]}]{Colors.RESET}")
                
                # Add tag if present
                if tag:
                    parts.append(f"{Colors.TAG}[{tag}]{Colors.RESET}")
                
                # Add message
                parts.append(f"{Colors.MESSAGE}{record.getMessage()}{Colors.RESET}")
                
                return " ".join(parts)

        return ConsoleFormatter()

    def _get_loki_formatter(self):
        """Formatter for Loki that returns properly structured data"""

        class LokiFormatter(logging.Formatter):
            def format(self, record):
                log_data = {
                    "timestamp": time.time(),
                    "message": record.getMessage(),
                    "level": record.levelname,
                    "process_id": os.getpid(),
                    "thread_id": threading.get_ident(),
                    "request_id": getattr(record, "request_id", RequestIdManager.get()),
                    # "caller_module": getattr(record, 'caller_module', 'unknown'),
                    # "caller_lineno": getattr(record, 'caller_lineno', 0),
                    # "caller_funcName": getattr(record, 'caller_funcName', 'unknown'),
                    "tag": getattr(record, "tag", None),
                }
                # Return tuple: (message_dict, metadata_dict)
                return (log_data, {"level": record.levelname})

        return LokiFormatter()

    def _get_caller_context(self):
        frame = inspect.currentframe().f_back.f_back
        return {
            "funcName": frame.f_code.co_name,
            "lineno": frame.f_lineno,
            "module": inspect.getmodule(frame).__name__ if inspect.getmodule(frame) else "unknown",
        }

    def _prepare_log_message(self, level, *args, **kwargs):
        if args and "message" in kwargs:
            tag = args[0]
            message = kwargs["message"]
        elif args:
            tag = None
            message = args[0]
        else:
            tag = kwargs.get("tag")
            message = kwargs.get("message", "")

        context = self._get_caller_context()
        extra = {"tag": tag, "caller_funcName": context["funcName"], "caller_lineno": context["lineno"], "caller_module": context["module"]}
        return message, extra

    def info(self, *args, **kwargs):
        message, extra = self._prepare_log_message(logging.INFO, *args, **kwargs)
        self.logger.info(message, extra=extra)

    def debug(self, *args, **kwargs):
        message, extra = self._prepare_log_message(logging.DEBUG, *args, **kwargs)
        self.logger.debug(message, extra=extra)

    def warning(self, *args, **kwargs):
        message, extra = self._prepare_log_message(logging.WARNING, *args, **kwargs)
        self.logger.warning(message, extra=extra)

    def error(self, *args, **kwargs):
        message, extra = self._prepare_log_message(logging.ERROR, *args, **kwargs)
        self.logger.error(message, extra=extra)

    def critical(self, *args, **kwargs):
        message, extra = self._prepare_log_message(logging.CRITICAL, *args, **kwargs)
        self.logger.critical(message, extra=extra)


# Initialize logger
logger = StructuredLogger(
    name="curita_toy_backend",
    loki_url=os.getenv("GRAFANA_LOKI_URL", "http://localhost:3100/loki/api/v1/push"),
    labels={"application": "curita_toy_backend", "service": "toy_communication"},
    loki_enabled=os.getenv("LOKI_ENABLED", "false") == "true",
)
