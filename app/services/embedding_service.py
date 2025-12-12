"""
Embedding service using Snowflake Arctic Embed XS model locally
Optimized for conversational text with 384-dimensional embeddings
"""
from sentence_transformers import SentenceTransformer
from typing import List
from app.services.base import BaseEmbeddingService


class SnowflakeEmbeddingService(BaseEmbeddingService):
    """Service for generating embeddings using Snowflake Arctic Embed XS (384-dim)"""
    
    def __init__(self):
        """Initialize the embedding model"""
        super().__init__()
        self.model = None
        self.embedding_dimension = None
        self.initialize()
    
    def initialize(self):
        """Initialize service resources"""
        # Using Arctic Embed XS for faster, lighter embeddings (384-dim)
        model_name = self.settings.EMBEDDING_MODEL
        self.logger.info(f"Initializing embedding service with model: {model_name}")
        try:
            self.model = SentenceTransformer(model_name)
            self.embedding_dimension = self.model.get_sentence_embedding_dimension()
            self.logger.info(
                f"Embedding service initialized. "
                f"Model: {model_name}, Dimension: {self.embedding_dimension}"
            )
            
            # Verify dimension is 384 for Arctic XS
            if self.embedding_dimension != 384:
                self.logger.warning(
                    f"Expected 384 dimensions for Arctic XS, got {self.embedding_dimension}"
                )
        except Exception as e:
            self.logger.error(f"Failed to initialize embedding service: {str(e)}")
            raise
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        
        Args:
            text: Input text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        self.logger.debug(f"Generating embedding for text of length {len(text)}")
        embedding = self.model.encode(text, convert_to_numpy=True)
        self.logger.debug(f"Embedding generated: dimension={len(embedding)}")
        return embedding.tolist()
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch
        
        Args:
            texts: List of input texts to embed
            
        Returns:
            List of embedding vectors
        """
        self.logger.info(f"Generating embeddings for {len(texts)} texts in batch")
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        self.logger.info(f"Batch embeddings generated successfully: {len(embeddings)} vectors")
        return embeddings.tolist()
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embedding vectors"""
        return self.embedding_dimension


# Global embedding service instance
_embedding_service = None


def get_embedding_service() -> SnowflakeEmbeddingService:
    """Get or create global embedding service instance"""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = SnowflakeEmbeddingService()
    return _embedding_service
