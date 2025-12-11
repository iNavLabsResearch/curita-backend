"""
Curita Backend - RAG System with Supabase and pgvector
"""
import os
import warnings
# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Suppress FutureWarning from transformers
warnings.filterwarnings('ignore', category=FutureWarning)

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.api.routes import router as legacy_router
from app.api.documents_routes import router as documents_router
from app.api.rag_routes import router as rag_router
from app.api.routes_providers import router as providers_router
from app.api.routes_toys_agents import router as toys_agents_router
from app.api.routes_memory import router as memory_router
from app.utilities.logger import LoggerService, get_logger
import uvicorn
import time
import uuid
from app.utilities.logger import request_id_ctx_var

# Initialize logging
LoggerService.setup_logging()
logger = get_logger(__name__)

# Get settings
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} starting up...")
    logger.info(f"📊 Log level: {settings.LOG_LEVEL}")
    logger.info(f"🔧 Debug mode: {settings.DEBUG}")
    logger.info(f"📁 Embedding model: {settings.EMBEDDING_MODEL}")
    logger.info(f"✅ Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down application...")
    logger.info("👋 Application shutdown complete")


# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Backend for document processing, embedding generation, and semantic search using Supabase pgvector",
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests with correlation ID"""
    start_time = time.time()
    
    # Generate or get request ID
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    
    # Set correlation ID context
    token = request_id_ctx_var.set(request_id)
    
    try:
        # Log request
        access_logger = get_logger("api.access")
        access_logger.info(f"Request: {request.method} {request.url.path}")
        
        # Process request
        response = await call_next(request)
        
        # Add Request ID to response headers
        response.headers["X-Request-ID"] = request_id
        
        # Log response
        process_time = time.time() - start_time
        access_logger.info(
            f"Response: {request.method} {request.url.path} - "
            f"Status: {response.status_code} - Time: {process_time:.3f}s"
        )
        
        return response
    finally:
        # Reset context variable
        request_id_ctx_var.reset(token)

# Include API routes
app.include_router(providers_router)    # Provider management
app.include_router(toys_agents_router)  # Toys, agents, and tools
app.include_router(memory_router)       # Memory and conversations
app.include_router(legacy_router)       # Legacy document routes
app.include_router(documents_router)    # New RAG document ingestion
app.include_router(rag_router)          # RAG search


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/api/v1/health"
    }


if __name__ == "__main__":
    logger.info(f"Starting server on {settings.HOST}:{settings.PORT}")
    
    # Only reload in development and without watch directories (Windows issue)
    reload = settings.DEBUG and os.getenv("UVICORN_RELOAD", "false").lower() == "true"
    
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=reload,
        reload_dirs=None  # Disable watch dirs to prevent Windows buffer overflow
    )
