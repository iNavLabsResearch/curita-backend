class MetricsConstants:
    """
    Metrics constants for Curita toy backend
    
    Tracks:
    - Toy-child interactions and communication
    - Agent processing and responses
    - WebSocket real-time connections
    - Memory search and retrieval operations
    """
    
    COUNTER_METRICS = "COUNTER"
    HISTOGRAM_METRICS = "HISTOGRAM"
    GAUGE_METRICS = "GAUGE"
    
    # Toy-Child Interaction Metrics
    TOY_INTERACTION_COUNT = "curita_toy_interaction_total"
    TOY_SESSION_DURATION = "curita_toy_session_duration_seconds"
    TOY_RESPONSE_TIME = "curita_toy_response_time_seconds"
    TOY_AUDIO_PROCESSED = "curita_toy_audio_processed_total"
    TOY_TEXT_MESSAGES = "curita_toy_text_messages_total"
    TOY_ACTIVE_SESSIONS = "curita_toy_active_sessions"
    TOY_MEMORY_SEARCHES = "curita_toy_memory_searches_total"
    TOY_CONVERSATION_LENGTH = "curita_toy_conversation_length"
    
    # Agent Processing Metrics
    AGENT_INVOCATIONS = "curita_agent_invocations_total"
    AGENT_ERRORS = "curita_agent_errors_total"
    AGENT_RESPONSE_TIME = "curita_agent_response_time_seconds"
    AGENT_TOKEN_USAGE = "curita_agent_token_usage_total"
    
    # WebSocket Communication Metrics
    WEBSOCKET_CONNECTIONS = "curita_websocket_connections_total"
    WEBSOCKET_DISCONNECTIONS = "curita_websocket_disconnections_total"
    WEBSOCKET_ACTIVE = "curita_websocket_active_connections"
    WEBSOCKET_MESSAGE_SIZE = "curita_websocket_message_size_bytes"
    WEBSOCKET_MESSAGE_RATE = "curita_websocket_messages_per_second"
    
    # Memory & Embedding Metrics
    MEMORY_SEARCH_TIME = "curita_memory_search_time_seconds"
    EMBEDDING_GENERATION_TIME = "curita_embedding_generation_time_seconds"
    VECTOR_STORE_OPERATIONS = "curita_vector_store_operations_total"
    
    # Provider Metrics
    PROVIDER_API_CALLS = "curita_provider_api_calls_total"
    PROVIDER_API_ERRORS = "curita_provider_api_errors_total"
    PROVIDER_RESPONSE_TIME = "curita_provider_response_time_seconds"

