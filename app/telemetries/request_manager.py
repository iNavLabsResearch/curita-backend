"""
Request ID Manager for Curita Toy Backend

Manages request correlation IDs for tracking toy-child interactions,
WebSocket sessions, and API requests across the entire system.
"""
import contextvars
import uuid

# Context variable to hold the request ID for the current execution context
_request_id_ctx_var = contextvars.ContextVar("request_id", default=None)


class RequestIdManager:
    """
    Manages request IDs for distributed tracing and logging correlation.
    
    Used to track:
    - HTTP API requests
    - WebSocket sessions
    - Toy-child interactions
    - Agent processing flows
    """
    
    @staticmethod
    def set(request_id: str = None):
        """
        Set a request ID in the context. Generate a new one if not provided.
        
        Args:
            request_id: Optional request ID. If None, generates a new UUID.
        """
        if request_id is None:
            request_id = str(uuid.uuid4())
        _request_id_ctx_var.set(request_id)

    @staticmethod
    def get() -> str:
        """
        Get the current request ID from context.
        
        Returns:
            Current request ID or None if not set.
        """
        return _request_id_ctx_var.get()

    @staticmethod
    def clear():
        """Clear the request ID from context."""
        _request_id_ctx_var.set(None)
