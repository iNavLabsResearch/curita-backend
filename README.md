# Curita Backend - RAG System

A FastAPI backend for document processing, embedding generation, and semantic search using Supabase pgvector and Snowflake Arctic Embed models.

## Features

- **Document Upload**: Support for PDF, DOCX, and TXT files
- **Text Extraction**: Automatic text extraction using LangChain loaders
- **Smart Chunking**: LangChain's RecursiveCharacterTextSplitter with intelligent boundary detection
- **Local Embeddings**: Snowflake Arctic Embed models running locally
- **Vector Storage**: Supabase pgvector for efficient vector storage
- **Semantic Search**: Fast similarity search using RPC functions
- **CRUD Operations**: Complete document and chunk management
- **Comprehensive Logging**: Full request/response and operation logging

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Supabase

1. Create a new project in [Supabase](https://supabase.com)
2. Run the SQL script in `supabase_schema.sql` in your Supabase SQL Editor
3. Copy your project URL and API key

### 3. Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Update the values:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key

# Logging Configuration (optional)
LOG_LEVEL=INFO
LOG_FILE_ENABLED=true
LOG_FILE_MAX_BYTES=10485760
LOG_FILE_BACKUP_COUNT=5
```

### 4. Run the Server

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

### Upload Document

```bash
POST /api/v1/upload
- file: Document file (PDF, DOCX, TXT)
- chunk_size: Size of each chunk (default: 1000)
- chunk_overlap: Overlap between chunks (default: 200)
- metadata: Additional metadata (optional JSON string)
```

### Search Documents

```bash
POST /api/v1/search
{
  "query": "your search query",
  "top_k": 5,
  "similarity_threshold": 0.5,
  "filter_metadata": {}
}
```

### Search by Document ID

```bash
POST /api/v1/search/document
{
  "query": "your search query",
  "document_id": "uuid",
  "top_k": 5
}
```

### List Documents

```bash
GET /api/v1/documents?limit=100&offset=0
```

### Get Document

```bash
GET /api/v1/documents/{document_id}
```

### Delete Document

```bash
DELETE /api/v1/documents/{document_id}
```

### Update Chunk

```bash
PUT /api/v1/chunks/{chunk_id}
{
  "chunk_text": "updated text",
  "metadata": {}
}
```

### Health Check

```bash
GET /api/v1/health
```

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
│   │   └── config.py          # Centralized configuration
│   ├── models/
│   │   └── schemas.py         # Pydantic request/response models
│   ├── api/
│   │   └── routes.py          # API endpoints
│   ├── services/
│   │   ├── base.py            # Base service classes
│   │   ├── document_processor.py  # LangChain text extraction & chunking
│   │   ├── embedding_service.py   # Snowflake embeddings
│   │   ├── vector_storage.py      # Supabase storage
│   │   └── search_service.py      # Search functionality
│   └── utilities/
│       └── supabase_client.py     # Supabase client
├── main.py                    # FastAPI application
├── requirements.txt           # Python dependencies
├── supabase_schema.sql       # Database schema & RPC functions
├── .env.example              # Environment template
├── ARCHITECTURE.md           # Detailed architecture guide
└── README.md                 # Documentation
```

## Architecture

This project uses a **modular, layered architecture** with:

- **Core Layer**: Configuration management
- **Models Layer**: Pydantic schemas for type-safe data
- **Services Layer**: Business logic with abstract base classes
- **API Layer**: RESTful endpoints
- **Utilities Layer**: Shared helper functions

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed documentation.

## Snowflake Arctic Embed Model

This system uses `Snowflake/snowflake-arctic-embed-xs` (109M params, 384 dimensions) for optimal performance and speed.

## Development

Access the interactive API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

MIT
