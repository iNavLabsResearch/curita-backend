# Curita Backend - Talking Toy RAG System

A comprehensive FastAPI backend for a Talking Toy RAG system with multi-agent architecture, provider management, dual memory types, conversation tracking, and vector search capabilities.

## 🎯 Features

### Core System

- **Talking Toy Architecture**: Multi-toy system with configurable agents
- **Multi-Agent Framework**: Each toy can have multiple specialized agents
- **Provider System**: Pluggable AI providers (model, TTS, transcriber)
- **Dual Memory System**:
  - **Toy Memory**: Short-term interaction context (768-dim vectors)
  - **Agent Memory**: Long-term knowledge base with file storage
- **Conversation Management**: Role-based message tracking with citations
- **Vector Search**: Fast similarity search using HNSW indexing and Snowflake Arctic Embed

### Document Processing

- **Document Upload**: Support for PDF, DOCX, and TXT files
- **Text Extraction**: Automatic text extraction using LangChain loaders
- **Smart Chunking**: LangChain's RecursiveCharacterTextSplitter with intelligent boundary detection
- **Local Embeddings**: Snowflake Arctic Embed (768 dimensions) running locally
- **Vector Storage**: Supabase pgvector for efficient vector storage

### API & Infrastructure

- **Modular Architecture**: Clean separation of concerns with service layer
- **41 REST Endpoints**: Complete CRUD operations for all entities
- **Comprehensive Logging**: Full request/response and operation logging
- **Database Seeding**: Pre-configured providers and example data

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Supabase

1. Create a new project in [Supabase](https://supabase.com)
2. Run the SQL script in `supabase_schema.sql` in your Supabase SQL Editor
3. Run the RPC functions script in `supabase_rpc_functions.sql`
4. Copy your project URL and API key

### 3. Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Update the values:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key

# Embedding Model (768 dimensions)
EMBEDDING_MODEL=Snowflake/snowflake-arctic-embed-m
EMBEDDING_DIMENSION=768

# Logging Configuration (optional)
LOG_LEVEL=INFO
LOG_FILE_ENABLED=true
LOG_FILE_MAX_BYTES=10485760
LOG_FILE_BACKUP_COUNT=5
```

### 4. Seed Database (Optional)

Populate with default providers and example toy/agent:

```bash
python seed_database.py
```

This creates:

- Model providers (OpenAI GPT-4, GPT-3.5, Anthropic Claude)
- TTS providers (OpenAI, Google, ElevenLabs)
- Transcriber providers (OpenAI Whisper, Google)
- Example "Curita" toy with Storyteller agent

### 5. Run the Server

```bash
python main.py
```

Or with uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Logging

The application includes comprehensive logging:

- **Console Output**: Real-time logs for development
- **File Logging**: Rotating log files (10MB max, 5 backups)
  - `logs/app.log`: All application logs
  - `logs/error.log`: Error-level logs only
  - `logs/access.log`: API request/response logs with timing

See [LOGGING.md](LOGGING.md) for detailed documentation, configuration options, and best practices.

## API Endpoints

### 📚 Full API Documentation

See **[API_REFERENCE.md](API_REFERENCE.md)** for complete endpoint documentation with examples.

### Quick Overview (41 Endpoints)

#### 🔌 Provider Management (18 endpoints)

- **Model Providers**: CRUD operations for AI model providers (OpenAI, Anthropic, etc.)
- **TTS Providers**: Text-to-speech provider management
- **Transcriber Providers**: Speech-to-text provider management

#### 🧸 Toy & Agent Management (15 endpoints)

- **Toys**: Create/read/update/delete toys, activation management
- **Agents**: Agent lifecycle with provider linking
- **Agent Tools**: Tool registry with JSON schema support

#### 🧠 Memory & Conversation (8 endpoints)

- **Memory Search**: Unified search across toy and agent memory
- **Toy Memory**: Upload/retrieve/delete interaction context
- **Agent Memory**: Upload/retrieve/delete knowledge base with file storage
- **Conversations**: Add messages, get history, manage citations

#### 📄 Legacy Document Endpoints (backward compatible)

- Upload, search, list, get, delete documents
- Update chunks, health check

### Interactive API Docs

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Architecture

### Upload Flow

1. Extract text from document
2. Perform recursive chunking
3. Generate embeddings using Snowflake Arctic Embed (locally)
4. Store chunks and embeddings in Supabase pgvector

### Search Flow

1. Convert query text to embedding using Snowflake Arctic Embed (locally)
2. Pass embedding to Supabase RPC function
3. Perform vector similarity search in pgvector
4. Return ranked results

## Project Structure

```
curita-backend/
├── app/
│   ├── core/
│   │   └── config.py                    # Centralized configuration
│   ├── models/
│   │   └── schemas.py                   # 30+ Pydantic schemas
│   ├── api/
│   │   ├── routes.py                    # Legacy document endpoints
│   │   ├── routes_providers.py          # Provider management (18 endpoints)
│   │   ├── routes_toys_agents.py        # Toy/agent/tool endpoints (15)
│   │   └── routes_memory.py             # Memory/conversation endpoints (8)
│   ├── services/
│   │   ├── base.py                      # Base service classes
│   │   ├── provider_service.py          # Model/TTS/Transcriber providers
│   │   ├── toy_service.py               # Toy management
│   │   ├── agent_service.py             # Agent management
│   │   ├── agent_tools_service.py       # Tool registry
│   │   ├── toy_memory_service.py        # Toy memory (context)
│   │   ├── agent_memory_service.py      # Agent memory (knowledge base)
│   │   ├── conversation_service.py      # Conversation logging
│   │   ├── citation_service.py          # Message citations
│   │   ├── unified_memory_search.py     # Cross-memory search
│   │   ├── document_processor.py        # LangChain text extraction
│   │   ├── embedding_service.py         # Snowflake embeddings (768-dim)
│   │   ├── vector_storage.py            # Supabase vector storage
│   │   └── search_service.py            # Search functionality
│   └── utilities/
│       ├── supabase_client.py           # Supabase client
│       └── logger.py                    # Logging utilities
├── main.py                              # FastAPI application
├── requirements.txt                     # Python dependencies
├── supabase_schema.sql                  # Database schema (10 tables)
├── supabase_rpc_functions.sql          # Vector search RPC functions
├── seed_database.py                     # Database seeding script
├── .env.example                         # Environment template
├── API_REFERENCE.md                     # Complete API documentation
├── ARCHITECTURE.md                      # Detailed architecture guide
├── LOGGING.md                           # Logging documentation
└── README.md                            # This file
```

## Architecture

This project uses a **modular, layered architecture** with:

- **Core Layer**: Configuration management with 13 table constants
- **Models Layer**: 30+ Pydantic schemas for type-safe data
- **Services Layer**: 10 specialized services with abstract base classes
- **API Layer**: 4 modular route files with 41 RESTful endpoints
- **Utilities Layer**: Shared helper functions

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed documentation.

## Database Schema

**10 Main Tables:**

1. `model_providers` - AI model providers (GPT-4, Claude, etc.)
2. `tts_providers` - Text-to-speech providers
3. `transcriber_providers` - Speech-to-text providers
4. `toys` - Toy entities (root level)
5. `agents` - Agents with provider links
6. `agent_tools` - Tool registry with JSON schemas
7. `toy_memory` - Interaction context with 768-dim vectors
8. `agent_memory` - Knowledge base with file storage
9. `conversation_logs` - Role-based messages
10. `message_citations` - Links messages to memory sources

**RPC Functions**: 4 vector similarity search functions with HNSW indexing

## Embedding Model

**Snowflake Arctic Embed M** (768 dimensions)teraction context (user preferences, recent interactions)

- **Agent Memory**: Long-term knowledge base (documents, facts) with file storage

**Unified Search**: Search across both memory types with single API call

### Vector Search Flow

1. Convert query text to embedding using Snowflake Arctic Embed (768-dim, locally)
2. Pass embedding to Supabase RPC function
3. Perform vector similarity search in pgvector using HNSW indexing
4. Return ranked results with similarity scores
   See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed documentation.

## Snowflake Arctic Embed Model

This system uses `Snowflake/snowflake-arctic-embed-xs` (109M params, 384 dimensions) for optimal performance and speed.

## Development

Access the interactive API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

MIT
