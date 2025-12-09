# Logging System Documentation

## Overview

The application now includes a comprehensive logging system that tracks all operations, errors, and API requests across the entire codebase.

## Features

### 1. **Centralized Logging Service**

- Single configuration point for all logging
- Automatic logger creation for each module
- Consistent formatting across the application

### 2. **Multiple Log Outputs**

- **Console**: INFO level and above (DEBUG in dev mode)
- **app.log**: All logs (DEBUG and above) with rotation
- **error.log**: Only ERROR and CRITICAL logs
- **access.log**: HTTP request/response logs with timing

### 3. **Log Rotation**

- Automatic file rotation when size exceeds 10MB
- Keeps last 5 backup files
- Access logs rotate daily

### 4. **Structured Logging**

- Timestamp
- Logger name (module path)
- Log level
- Function name and line number
- Message

## Configuration

Add to your `.env` file:

```env
# Logging Configuration
LOG_LEVEL=INFO                    # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE_ENABLED=true             # Enable/disable file logging
LOG_FILE_MAX_BYTES=10485760       # 10MB per file
LOG_FILE_BACKUP_COUNT=5           # Keep 5 old files
LOG_JSON_FORMAT=false             # Future: JSON structured logs
```

## Usage

### In Services (Automatic)

All services inheriting from `BaseService` automatically get a logger:

```python
class MyService(BaseService):
    def my_method(self):
        self.logger.info("Processing started")
        self.logger.debug("Debug details here")
        self.logger.error("Error occurred")
```

### In Other Modules

```python
from app.utilities.logger import get_logger

logger = get_logger(__name__)

def my_function():
    logger.info("Function called")
    logger.warning("Warning message")
    logger.error("Error message")
```

### Using LoggerMixin

```python
from app.utilities.logger import LoggerMixin

class MyClass(LoggerMixin):
    def process(self):
        self.logger.info("Processing...")
```

## Log Levels

- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages
- **WARNING**: Warning messages for potentially harmful situations
- **ERROR**: Error messages for serious problems
- **CRITICAL**: Critical messages for very serious errors

## Log Files Location

All logs are stored in the `logs/` directory:

```
logs/
├── app.log          # All application logs
├── error.log        # Error logs only
└── access.log       # API access logs
```

## Examples

### Logged Operations

1. **Service Initialization**

   ```
   2024-12-09 10:30:15 - INFO - Initializing embedding service with model: Snowflake/snowflake-arctic-embed-xs
   ```

2. **Document Processing**

   ```
   2024-12-09 10:31:20 - INFO - Processing document: example.pdf (type: pdf)
   2024-12-09 10:31:22 - INFO - Split document into 45 chunks
   ```

3. **API Requests**

   ```
   2024-12-09 10:32:10 - INFO - Request: POST /api/v1/upload
   2024-12-09 10:32:15 - INFO - Response: POST /api/v1/upload - Status: 200 - Time: 5.234s
   ```

4. **Search Operations**

   ```
   2024-12-09 10:33:00 - INFO - Performing search: query='what is machine learning...', top_k=5
   2024-12-09 10:33:01 - INFO - Search completed: found 5 results
   ```

5. **Errors**
   ```
   2024-12-09 10:34:00 - ERROR - Error processing document example.pdf: Unsupported file type
   ```

## Best Practices

1. **Use Appropriate Levels**

   - DEBUG: Detailed flow information
   - INFO: Normal operations
   - WARNING: Unexpected but handled situations
   - ERROR: Errors that need attention

2. **Include Context**

   ```python
   self.logger.info(f"Processing document: {filename}")
   self.logger.error(f"Failed to process {filename}: {str(e)}")
   ```

3. **Log Important Operations**

   - Service initialization
   - Data processing start/end
   - External API calls
   - Database operations
   - Errors and exceptions

4. **Don't Log Sensitive Data**
   - Avoid logging passwords, API keys, tokens
   - Sanitize user data before logging

## Monitoring

### View Real-time Logs

```bash
# All logs
tail -f logs/app.log

# Errors only
tail -f logs/error.log

# API access
tail -f logs/access.log
```

### Filter Logs

```bash
# Show only ERROR logs
grep "ERROR" logs/app.log

# Show logs from specific module
grep "embedding_service" logs/app.log

# Show today's logs
grep "2024-12-09" logs/app.log
```

## Integration with Services

The logging system is fully integrated:

- ✅ **EmbeddingService**: Model loading, embedding generation
- ✅ **DocumentProcessor**: File processing, chunking
- ✅ **VectorStorage**: Database operations, chunk storage
- ✅ **SearchService**: Search operations, result counts
- ✅ **API Routes**: Request/response logging with timing
- ✅ **Main App**: Application startup, server info

## Future Enhancements

- [ ] JSON structured logging
- [ ] Log aggregation (ELK, Splunk)
- [ ] Async logging for better performance
- [ ] Log correlation IDs for request tracking
- [ ] Metrics and alerts based on logs
