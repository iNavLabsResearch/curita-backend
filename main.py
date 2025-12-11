"""
Curita Backend - RAG System with Supabase and pgvector
"""
import os
# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from static_memory_cache import StaticMemoryCache
from app.api.v1 import router as api_v1_router
from app.telemetries.logger import logger
from app.telemetries.request_manager import RequestIdManager
import uvicorn
import time
import uuid

# Get settings from StaticMemoryCache
settings = StaticMemoryCache


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    app_config = settings.config.get("application", {})
    logger.info(f"🚀 {app_config.get('app_name', 'Curita Backend')} v{app_config.get('app_version', '1.0.0')} starting up...")
    logger.info(f"📊 Log level: {app_config.get('log_level', 'INFO')}")
    logger.info(f"🔧 Debug mode: {app_config.get('debug', False)}")
    logger.info(f"📁 Embedding model: {settings.get_embed_model_config().get('model_name', 'snowflake-arctic-embed')}")
    logger.info(f"🔌 WebSocket support: Enabled")
    logger.info(f"✅ Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("👋 Application shutdown complete")


# Initialize FastAPI app
app_config = settings.config.get("application", {})
app = FastAPI(
    title=app_config.get("app_name", "Curita Backend"),
    description="Backend for talking toy system with multi-agent architecture, WebSocket support, and RAG capabilities",
    version=app_config.get("app_version", "1.0.0"),
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=app_config.get("cors_origins", ["*"]),
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
    RequestIdManager.set(request_id)
    
    try:
        # Log request
        logger.info(f"Request: {request.method} {request.url.path}")
        
        # Process request
        response = await call_next(request)
        
        # Add Request ID to response headers
        response.headers["X-Request-ID"] = request_id
        
        # Log response
        process_time = time.time() - start_time
        logger.info(
            f"Response: {request.method} {request.url.path} - "
            f"Status: {response.status_code} - Time: {process_time:.3f}s"
        )
        
        return response
    finally:
        # Clear request ID context
        RequestIdManager.clear()

# Include API routes
app.include_router(api_v1_router)


@app.get("/")
async def root():
    """Root endpoint"""
    app_config = settings.config.get("application", {})
    return {
        "message": f"Welcome to {app_config.get('app_name', 'Curita Backend')}",
        "version": app_config.get('app_version', '1.0.0'),
        "docs": "/docs",
        "health": "/api/v1/health"
    }


if __name__ == "__main__":
    app_config = settings.config.get("application", {})
    server_config = settings.config.get("server", {})
    
    host = server_config.get("host", "0.0.0.0")
    port = server_config.get("port", 8000)
    debug = app_config.get("debug", False)
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        reload_dirs=["app"] if debug else None,
        log_level="warning"  # Reduce uvicorn's default logging
    )
