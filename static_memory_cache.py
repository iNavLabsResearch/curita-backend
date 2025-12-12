import json
import torch
import os

class StaticMemoryCache:
    # Static class variables to store config and models in memory
    config = {}
    models = {}
    noise_reduction_pipeline = None
    vad_model = None

    @classmethod
    def initialize(cls, config_file: str = "config.json"):
        """Load config and models into memory at startup."""
        if not os.path.exists(config_file):
            print(f"Warning: Config file '{config_file}' not found. Using empty configuration.")
            cls.config = {}
            return
        
        try:
            with open(config_file, "r") as f:
                cls.config = json.load(f)
            print(f"Configuration loaded successfully from {config_file}")
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in config file: {e}")
            cls.config = {}
            return
        except Exception as e:
            print(f"Error loading config file: {e}")
            cls.config = {}
            return
        
        cls._initialize_noise_reduction_pipeline()
        cls._initalize_vad_model()
        
        # Load database table names from config
        db_tables = cls.config.get("database_tables", {})
        cls.TOYS_TABLE = db_tables.get("toys", "toys")
        cls.AGENTS_TABLE = db_tables.get("agents", "agents")
        cls.AGENT_TOOLS_TABLE = db_tables.get("agent_tools", "agent_tools")
        cls.MODEL_PROVIDERS_TABLE = db_tables.get("model_providers", "model_providers")
        cls.TTS_PROVIDERS_TABLE = db_tables.get("tts_providers", "tts_providers")
        cls.TRANSCRIBER_PROVIDERS_TABLE = db_tables.get("transcriber_providers", "transcriber_providers")
        cls.TOY_MEMORY_TABLE = db_tables.get("toy_memory", "toy_memory")
        cls.AGENT_MEMORY_TABLE = db_tables.get("agent_memory", "agent_memory")
        cls.CONVERSATION_LOGS_TABLE = db_tables.get("conversation_logs", "conversation_logs")
        cls.MESSAGE_CITATIONS_TABLE = db_tables.get("message_citations", "message_citations")
        
        # Load chunking settings from config
        chunking_config = cls.config.get("chunking", {})
        cls.DEFAULT_CHUNK_SIZE = chunking_config.get("default_chunk_size", 1000)
        cls.DEFAULT_CHUNK_OVERLAP = chunking_config.get("default_chunk_overlap", 200)
        
        # Load embedding settings from config
        embed_config = cls.config.get("models", {}).get("embed_model", {})
        cls.EMBEDDING_MODEL = embed_config.get("model_id", "Snowflake/snowflake-arctic-embed-xs")
        cls.EMBEDDING_DIMENSION = cls.config.get("chromadb", {}).get("embedding_dimension", 384)

    @classmethod
    def _initialize_noise_reduction_pipeline(cls):
        """Initialize noise reduction pipeline and store it in memory."""
        noise_reduction_config = cls.config.get("noise_reduction", {})
        if noise_reduction_config and noise_reduction_config.get("should_use_noise_reduction"):
            from app.services.noise_reduction.noise_reduction_pipeline import NoiseReductionPipeline
            from app.services.noise_reduction.deep_filter_noise_reduction_stage import DeepFilterStage
            from app.services.noise_reduction.rn_noise_reduction_stage import RNNoiseStage
        
            noise_reduction_pipeline = NoiseReductionPipeline()
            if noise_reduction_config.get("rnnoise_reduction_enabled"):
                noise_reduction_pipeline.add_stage(RNNoiseStage())
            if noise_reduction_config.get("deep_filter_reduction_enabled"):
                noise_reduction_pipeline.add_stage(DeepFilterStage())
            cls.noise_reduction_pipeline = noise_reduction_pipeline
        else:
            cls.noise_reduction_pipeline = None

    @classmethod
    def get_config(cls, section: str, key: str):
        """Retrieve configuration value from the static memory cache."""
        return cls.config.get(section, {}).get(key)

    @classmethod
    def get_model(cls, model_name: str):
        """Retrieve model from the static memory cache."""
        return cls.models.get(model_name)

    @classmethod
    def _initalize_vad_model(cls):
        """Initialize VAD model from config (disabled - torchaudio not required)."""
        # VAD model disabled to avoid torchaudio dependency
        cls.vad_model = None

    @classmethod
    def get_vad_model(cls):
        return cls.vad_model

    @classmethod
    def get_noise_reduction_pipeline(cls):
        """Retrieve noise cancellation pipeline."""
        return cls.noise_reduction_pipeline

    @classmethod
    def get_vector_db_credentials(cls) -> dict:
        """Retrieve RAG credentials from the static memory cache.
        
        Returns:
            dict: Dictionary containing weaviate_url and weaviate_api_key
        """
        return {
            "weaviate_url": cls.config.get("vector_db", {}).get("weaviate_url"),
            "weaviate_api_key": cls.config.get("vector_db", {}).get("weaviate_api_key")
        }

    @classmethod
    def get_embed_model_config(cls) -> dict:
        """Retrieve embedding model configuration from the static memory cache.
        
        Returns:
            dict: Dictionary containing api_base, api_key, model_id, and model_name
        """
        return cls.config.get("models", {}).get("embed_model", {})
      
    @classmethod
    def get_server_base_url(cls) -> str:
        """Get the server's base URL from config.
        
        Returns:
            str: The server's base URL
        """
        return cls.config.get("server", {}).get("base_url")

    @classmethod
    def get_composio_api_key(cls) -> str:
        """Get Composio API key from config.
        
        Returns:
            str: The Composio API key
        """
        return cls.config.get("composio", {}).get("api_key")

    @classmethod
    def get_composio_org_key(cls) -> str:
        """Get Composio organization key from config.
        
        Returns:
            str: The Composio organization key
        """
        return cls.config.get("composio", {}).get("organization_key")

    @classmethod
    def get_composio_base_url(cls) -> str:
        """Get Composio base URL from config.
        
        Returns:
            str: The Composio base URL
        """
        return cls.config.get("composio", {}).get("base_url")

    @classmethod
    def get_composio_config(cls) -> dict:
        """Get complete Composio configuration from config.
        
        Returns:
            dict: Dictionary containing api_key, organization_key, and base_url
        """
        return cls.config.get("composio", {})

    @classmethod
    def get_chromadb_config(cls) -> dict:
        """Get ChromaDB configuration from config.
        
        Returns:
            dict: Dictionary containing api_key, tenant, database, collection_id, collection_name, embedding_dimension
        """
        return cls.config.get("chromadb", {})

StaticMemoryCache.initialize()
