# Curita Backend - Talking Toy RAG System API

## Overview

Complete boilerplate code for a Talking Toy RAG System with modular architecture, provider management, dual memory types (toy & agent), conversation tracking, and citation management.

## Architecture

### Service Layer (app/services/)

- **provider_service.py** - Manage model, TTS, and transcriber providers
- **toy_service.py** - Toy CRUD operations
- **agent_service.py** - Agent management with provider links
- **agent_tools_service.py** - Tool registry with JSON schemas
- **toy_memory_service.py** - Toy memory (interaction context) with 768-dim vectors
- **agent_memory_service.py** - Agent memory (knowledge base) with file storage
- **conversation_service.py** - Conversation logs with role-based messages
- **citation_service.py** - Message citations linking to memory
- **unified_memory_search.py** - Search across both memory types

### API Layer (app/api/)

- **routes_providers.py** - Provider endpoints
- **routes_toys_agents.py** - Toy, agent, and tool endpoints
- **routes_memory.py** - Memory and conversation endpoints
- **routes.py** - Legacy document endpoints (backward compatible)

## API Endpoints

### 1. Provider Management (`/api/v1/providers`)

#### Model Providers

```
POST   /providers/models              # Create model provider
GET    /providers/models              # List model providers
GET    /providers/models/default      # Get default model provider
GET    /providers/models/{id}         # Get model provider by ID
PUT    /providers/models/{id}         # Update model provider
POST   /providers/models/{id}/set-default  # Set as default
DELETE /providers/models/{id}         # Delete model provider
```

#### TTS Providers

```
POST   /providers/tts                 # Create TTS provider
GET    /providers/tts                 # List TTS providers
GET    /providers/tts/{id}            # Get TTS provider by ID
PUT    /providers/tts/{id}            # Update TTS provider
DELETE /providers/tts/{id}            # Delete TTS provider
```

#### Transcriber Providers

```
POST   /providers/transcribers        # Create transcriber provider
GET    /providers/transcribers        # List transcriber providers
GET    /providers/transcribers/{id}  # Get transcriber provider by ID
PUT    /providers/transcribers/{id}  # Update transcriber provider
DELETE /providers/transcribers/{id}  # Delete transcriber provider
```

### 2. Toy Management (`/api/v1/toys`)

```
POST   /toys                          # Create toy
GET    /toys                          # List toys (filter by is_active)
GET    /toys/{toy_id}                 # Get toy by ID
PUT    /toys/{toy_id}                 # Update toy
POST   /toys/{toy_id}/activate       # Activate/deactivate toy
DELETE /toys/{toy_id}                 # Delete toy (cascades)
```

### 3. Agent Management (`/api/v1/agents`)

```
POST   /agents                        # Create agent
GET    /toys/{toy_id}/agents          # List agents for toy
GET    /agents/{agent_id}             # Get agent by ID
PUT    /agents/{agent_id}             # Update agent
DELETE /agents/{agent_id}             # Delete agent (cascades)
```

### 4. Agent Tools (`/api/v1/tools`)

```
POST   /tools                         # Create agent tool
GET    /toys/{toy_id}/tools           # List tools for toy
GET    /tools/{tool_id}               # Get tool by ID
PUT    /tools/{tool_id}               # Update tool
DELETE /tools/{tool_id}               # Delete tool
```

### 5. Memory Management (`/api/v1`)

#### Memory Search

```
POST   /memory/search                 # Search across toy/agent memory
```

#### Toy Memory

```
POST   /toys/{toy_id}/memory          # Upload to toy memory
GET    /toys/{toy_id}/memory          # Get toy memory chunks
DELETE /toys/{toy_id}/memory          # Delete toy memory
```

#### Agent Memory

```
POST   /agents/{agent_id}/memory      # Upload to agent memory
GET    /agents/{agent_id}/memory      # Get agent memory chunks
DELETE /agents/{agent_id}/memory      # Delete agent memory
```

### 6. Conversations (`/api/v1/agents/{agent_id}/conversation`)

```
POST   /agents/{agent_id}/conversation    # Add message
GET    /agents/{agent_id}/conversation    # Get conversation history
DELETE /agents/{agent_id}/conversation    # Clear conversation
```

## Setup Instructions

### 1. Database Setup

1. Run `supabase_schema.sql` in Supabase SQL Editor
2. Run `supabase_rpc_functions.sql` for vector search functions

### 2. Environment Variables

Update `.env`:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Embedding Model (updated to support 768 dimensions)
EMBEDDING_MODEL=Snowflake/snowflake-arctic-embed-m
EMBEDDING_DIMENSION=768
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Seed Database (Optional)

```bash
python seed_database.py
```

This creates:

- Default model providers (OpenAI GPT-4, GPT-3.5, Anthropic Claude)
- Default TTS providers (OpenAI, Google, ElevenLabs)
- Default transcriber providers (OpenAI Whisper, Google)
- Example toy and agent

### 5. Run Server

```bash
python main.py
```

Or:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Key Features

### ✅ Modular Architecture

- Clean separation of concerns
- Dependency injection pattern
- Base service classes for consistency

### ✅ Provider System

- Pluggable model, TTS, and transcriber providers
- Default provider management
- Multi-language support

### ✅ Dual Memory System

- **Toy Memory**: Interaction context (768-dim vectors)
- **Agent Memory**: Knowledge base with file storage
- Unified search across both types

### ✅ Conversation Tracking

- Role-based messages (user, assistant, system, tool)
- Message citations linking to memory sources
- Conversation history management

### ✅ Vector Search

- HNSW indexing for fast similarity search
- Snowflake Arctic Embed (768 dimensions)
- Similarity threshold filtering

### ✅ Comprehensive Logging

- Request/response logging
- Operation tracking
- Error handling with context

## Data Flow

```
1. Create Toy → 2. Create Agent → 3. Link Providers → 4. Add Tools
                        ↓
5. Upload to Agent Memory (Knowledge Base)
                        ↓
6. Upload to Toy Memory (Context)
                        ↓
7. Start Conversation → 8. Search Memory → 9. Generate Response with Citations
```

## Example Usage

### 1. Create a Toy

```python
POST /api/v1/toys
{
  "name": "Curita",
  "description": "Learning companion",
  "is_active": true
}
```

### 2. Create an Agent

```python
POST /api/v1/agents
{
  "toy_id": "<toy_uuid>",
  "name": "Storyteller",
  "system_prompt": "You are a creative storyteller...",
  "language_code": "en-US"
}
```

### 3. Upload Knowledge

```python
POST /api/v1/agents/{agent_id}/memory?toy_id={toy_id}
FormData: file=document.pdf
```

### 4. Search Memory

```python
POST /api/v1/memory/search
{
  "query": "What is photosynthesis?",
  "memory_type": "both",
  "agent_id": "<agent_uuid>",
  "top_k": 5
}
```

### 5. Add Conversation Message

```python
POST /api/v1/agents/{agent_id}/conversation
{
  "role": "user",
  "content": "Tell me a story about space"
}
```

## File Structure

```
curita-backend/
├── app/
│   ├── api/
│   │   ├── routes.py (legacy)
│   │   ├── routes_providers.py
│   │   ├── routes_toys_agents.py
│   │   └── routes_memory.py
│   ├── core/
│   │   └── config.py (updated)
│   ├── models/
│   │   └── schemas.py (complete schemas)
│   ├── services/
│   │   ├── provider_service.py
│   │   ├── toy_service.py
│   │   ├── agent_service.py
│   │   ├── agent_tools_service.py
│   │   ├── toy_memory_service.py
│   │   ├── agent_memory_service.py
│   │   ├── conversation_service.py
│   │   ├── citation_service.py
│   │   └── unified_memory_search.py
│   └── utilities/
├── main.py (updated)
├── supabase_schema.sql
├── supabase_rpc_functions.sql (NEW)
├── seed_database.py (NEW)
└── API_REFERENCE.md (NEW)
```

## Next Steps

1. ✅ All service layers implemented
2. ✅ All API routes created
3. ✅ Database schema and RPC functions ready
4. ✅ Seed script for initial data
5. 📝 Update README.md with new documentation
6. 📝 Update ARCHITECTURE.md with new patterns
7. 🧪 Test all endpoints
8. 🚀 Deploy!

## Testing

Access the interactive API documentation at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

All endpoints are fully documented with request/response schemas!
