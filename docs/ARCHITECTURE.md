# Curita Backend - Talking Toy RAG System Architecture

## 📁 Project Structure

```
curita-backend/
├── app/
│   ├── __init__.py
│   ├── core/                         # Core configuration
│   │   ├── __init__.py
│   │   └── config.py                 # Centralized settings (13 table constants)
│   ├── models/                       # Data models
│   │   ├── __init__.py
│   │   └── schemas.py                # 30+ Pydantic schemas
│   ├── services/                     # Business logic (10 services)
│   │   ├── __init__.py
│   │   ├── base.py                   # Base service classes
│   │   ├── provider_service.py       # Model/TTS/Transcriber providers
│   │   ├── toy_service.py            # Toy management
│   │   ├── agent_service.py          # Agent management with providers
│   │   ├── agent_tools_service.py    # Tool registry with JSON schemas
│   │   ├── toy_memory_service.py     # Toy memory (interaction context)
│   │   ├── agent_memory_service.py   # Agent memory (knowledge base)
│   │   ├── conversation_service.py   # Conversation logging
│   │   ├── citation_service.py       # Message citations
│   │   ├── unified_memory_search.py  # Cross-memory search
│   │   ├── document_processor.py     # Text extraction & chunking
│   │   ├── embedding_service.py      # Snowflake embeddings (768-dim)
│   │   ├── vector_storage.py         # Supabase vector storage
│   │   └── search_service.py         # Search functionality (legacy)
│   ├── api/                          # API layer (41 endpoints)
│   │   ├── __init__.py
│   │   ├── routes.py                 # Legacy document endpoints
│   │   ├── routes_providers.py       # Provider management (18 endpoints)
│   │   ├── routes_toys_agents.py     # Toy/agent/tool endpoints (15)
│   │   └── routes_memory.py          # Memory/conversation endpoints (8)
│   └── utilities/                    # Utility functions
│       ├── __init__.py
│       ├── supabase_client.py        # Supabase connection
│       └── logger.py                 # Logging utilities
├── main.py                           # Application entry point (4 routers)
├── requirements.txt
├── supabase_schema.sql               # 10 tables + indexes
├── supabase_rpc_functions.sql        # 4 vector search RPC functions
├── seed_database.py                  # Database seeding script
├── .env.example
├── .gitignore
├── API_REFERENCE.md                  # Complete API documentation
├── ARCHITECTURE.md                   # This file
├── LOGGING.md
└── README.md
```

## 🏗️ Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         FastAPI App                          │
├─────────────────────────────────────────────────────────────┤
│  API Layer (4 route modules, 41 endpoints)                  │
│  ├── routes_providers.py      (18 endpoints)                │
│  ├── routes_toys_agents.py    (15 endpoints)                │
│  ├── routes_memory.py         (8 endpoints)                 │
│  └── routes.py                (legacy endpoints)            │
├─────────────────────────────────────────────────────────────┤
│  Service Layer (10 specialized services)                    │
│  ├── Provider Services        (Model/TTS/Transcriber)       │
│  ├── Entity Services          (Toy/Agent/Tools)             │
│  ├── Memory Services          (Toy/Agent memory)            │
│  ├── Conversation Services    (Logs/Citations)              │
│  └── Search Services          (Unified memory search)       │
├─────────────────────────────────────────────────────────────┤
│  Core Services (Document/Embedding/Vector)                  │
│  ├── Document Processor       (LangChain)                   │
│  ├── Embedding Service        (Snowflake Arctic 768-dim)    │
│  └── Vector Storage           (Supabase pgvector)           │
├─────────────────────────────────────────────────────────────┤
│  Data Layer (Supabase PostgreSQL + pgvector)                │
│  ├── 10 Tables                (Providers/Toys/Memory/etc)   │
│  ├── 4 RPC Functions          (Vector similarity search)    │
│  └── HNSW Indexes             (Fast vector search)          │
└─────────────────────────────────────────────────────────────┘
```

### 1. **Core Layer** (`app/core/`)

- **Purpose**: Application configuration and settings
- **Key Components**:
  - `config.py`: Centralized configuration using Pydantic Settings
  - Environment variable management
  - 13 table name constants for new schema
  - Embedding model configuration (768 dimensions)
  - Application-wide constants

### 2. **Models Layer** (`app/models/`)

- **Purpose**: Data models and schemas
- **Key Components**:
  - `schemas.py`: 30+ Pydantic models for type-safe data
  - Provider schemas (Create/Update/Response for 3 provider types)
  - Entity schemas (Toy/Agent/Tool)
  - Memory schemas (ToyMemory/AgentMemory with embedding support)
  - Conversation schemas (Logs/Citations)
  - Search request/response schemas
  - Input validation and type safety

### 3. **Services Layer** (`app/services/`)

- **Purpose**: Business logic and core functionality

#### 3.1 **Base Classes** (`base.py`):

- `BaseService`: Common service functionality
- `BaseEmbeddingService`: Interface for embedding services
- `BaseDocumentProcessor`: Interface for document processing
- `BaseVectorStorage`: Interface for vector storage
- `BaseSearchService`: Interface for search operations

#### 3.2 **Provider Services** (`provider_service.py`):

- `ProviderService`: Base class for all provider types
- `ModelProviderService`: AI model providers (GPT-4, Claude, etc.)
- `TTSProviderService`: Text-to-speech providers
- `TranscriberProviderService`: Speech-to-text providers
- Default provider management
- Factory functions for dependency injection

#### 3.3 **Entity Services**:

- `ToyService`: Toy CRUD operations, activation management
- `AgentService`: Agent lifecycle, provider linking, activation
- `AgentToolsService`: Tool registry with JSON schema validation

#### 3.4 **Memory Services**:

- `ToyMemoryService`: Interaction context with 768-dim vectors
- `AgentMemoryService`: Knowledge base with file storage metadata
- `UnifiedMemorySearchService`: Cross-memory search aggregation

#### 3.5 **Conversation Services**:

- `ConversationService`: Role-based message logging (user/assistant/system/tool)
- `CitationService`: Links messages to memory sources (toy/agent memory)

#### 3.6 **Core Processing Services**:

- `SnowflakeEmbeddingService`: Snowflake Arctic Embed M (768-dim)
- `LangChainDocumentProcessor`: Text extraction and chunking using LangChain
- `SupabaseVectorStorage`: Supabase pgvector storage
- `SupabaseSearchService`: Vector similarity search (legacy)

### 4. **API Layer** (`app/api/`)

- **Purpose**: HTTP endpoints and request handling
- **Modular Structure**: 4 separate route files for clean organization

#### 4.1 **Provider Routes** (`routes_providers.py` - 18 endpoints):

- Model provider CRUD + default management (6 endpoints)
- TTS provider CRUD (5 endpoints)
- Transcriber provider CRUD (5 endpoints)
- Set default provider endpoints (2 endpoints)

#### 4.2 **Toy & Agent Routes** (`routes_toys_agents.py` - 15 endpoints):

- Toy CRUD + activation (6 endpoints)
- Agent CRUD + list by toy (5 endpoints)
- Agent tool CRUD + list by toy (4 endpoints)

#### 4.3 **Memory Routes** (`routes_memory.py` - 8 endpoints):

- Memory search (1 endpoint)
- Toy memory upload/get/delete (3 endpoints)
- Agent memory upload/get/delete (3 endpoints)
- Conversation add/get/delete (1 endpoint combines all)

#### 4.4 **Legacy Routes** (`routes.py` - backward compatible):

- Document upload, search, CRUD operations
- Maintains compatibility with old document system

### 5. **Utilities Layer** (`app/utilities/`)

- **Purpose**: Helper functions and shared utilities
- **Key Components**:
  - `supabase_client.py`: Singleton Supabase client
  - `logger.py`: Comprehensive logging with rotation

## 🔧 Design Patterns Used

### 1. **Dependency Injection**

- Services are injected via factory functions
- Easy to mock for testing
- Loose coupling between components

```python
# Example
model_provider_service = get_model_provider_service()
toy_service = get_toy_service()
```

### 2. **Singleton Pattern**

- Single instance for expensive resources
- Used for: Supabase client, embedding models

```python
class SupabaseClient:
    _instance: Client = None

    @classmethod
    def get_client(cls) -> Client:
        if cls._instance is None:
            cls._instance = create_client(...)
        return cls._instance
```

### 3. **Abstract Base Classes**

- Define interfaces for services
- Enable easy swapping of implementations
- Example: Switch from Supabase to another vector DB

```python
class BaseVectorStorage(BaseService):
    @abstractmethod
    async def store_document_chunks(...):
        pass
```

### 4. **Factory Pattern**

- Services created via factory functions
- Centralized instantiation logic
- Used for all provider services and entity services

```python
def get_model_provider_service() -> ModelProviderService:
    global _model_provider_service
    if _model_provider_service is None:
        _model_provider_service = ModelProviderService()
    return _model_provider_service
```

### 5. **Template Method Pattern**

- Base ProviderService class defines common CRUD operations
- Specialized services (Model/TTS/Transcriber) inherit and customize
- Reduces code duplication

```python
class ProviderService:
    def __init__(self, table_name: str):
        self.table_name = table_name

    async def create(self, data): ...
    async def get_by_id(self, id): ...
    async def list(self): ...

class ModelProviderService(ProviderService):
    def __init__(self):
        super().__init__(settings.MODEL_PROVIDERS_TABLE)
```

### 6. **Configuration Management**

- Centralized settings using Pydantic
- Type-safe configuration
- Environment-based configuration
- 13 table constants for new schema

```python
settings = get_settings()
table_name = settings.TOYS_TABLE
embedding_dim = settings.EMBEDDING_DIMENSION  # 768
```

## 🔄 Data Flow Patterns

### 1. **Toy-Agent-Memory System Flow**

```
User Request → API Route → Service Layer → Supabase
                              ↓
                     Memory Search ← Vector Search RPC
                              ↓
                     Unified Results (Toy + Agent Memory)
                              ↓
                     Conversation Log + Citations
```

### 2. **Provider Integration Flow**

```
1. Create Providers (Model/TTS/Transcriber)
   ↓
2. Set Default Provider (per type)
   ↓
3. Create Agent with provider_id references
   ↓
4. Agent uses providers for AI operations
```

### 3. **Memory Storage Flow**

```
Document Upload → Document Processor (LangChain)
                        ↓
                  Text Chunking (RecursiveCharacterTextSplitter)
                        ↓
                  Embedding Generation (Snowflake Arctic 768-dim)
                        ↓
                  Store in Memory (Toy/Agent memory tables)
                        ↓
                  HNSW Index for Fast Search
```

### 4. **Conversation Flow with Citations**

```
1. User sends message → ConversationService.add_message()
                              ↓
2. Search memory → UnifiedMemorySearchService.search()
                              ↓
3. Generate response (external AI)
                              ↓
4. Store assistant message → ConversationService.add_message()
                              ↓
5. Link to memory sources → CitationService.add_citations_batch()
```

## 🚀 Benefits of This Architecture

### **Scalability**

- Easy to add new services
- Clear separation of concerns
- Modular components
- Support for multi-toy, multi-agent deployments

### **Maintainability**

- Single responsibility principle
- Easy to locate and fix bugs
- Clear dependencies
- 4 modular route files (vs monolithic routes)

### **Testability**

- Mock services easily
- Unit test individual components
- Integration test API layer
- Service layer isolated from API layer

### **Flexibility**

- Swap implementations without changing API
- Example: Switch from Snowflake to OpenAI embeddings
- Add new storage backends
- Add new provider types easily

### **Type Safety**

- 30+ Pydantic models for validation
- Type hints throughout
- Catch errors at development time
- Request/response schema validation

### **Extensibility**

- Provider system allows adding new AI services
- Dual memory system supports different use cases
- Tool registry enables agent capabilities expansion
- Citation system tracks information provenance

## 🔌 Extending the System

### **Adding a New Provider Type**

Example: Adding a Translation Provider

1. Add table constant to `config.py`:

```python
TRANSLATION_PROVIDERS_TABLE: str = "translation_providers"
```

2. Create Pydantic schemas in `schemas.py`:

```python
class TranslationProviderCreate(BaseModel):
    provider_name: str
    provider_type: str  # "google_translate", "deepl", etc.
    api_endpoint: Optional[str] = None
```

3. Create service in `provider_service.py`:

```python
class TranslationProviderService(ProviderService):
    def __init__(self):
        super().__init__(settings.TRANSLATION_PROVIDERS_TABLE)
```

4. Add routes to `routes_providers.py` - following existing pattern

### **Adding a New Memory Type**

Example: Adding a Session Memory for dialogue context

1. Create table in `supabase_schema.sql`
2. Add schema to `schemas.py`
3. Create service class inheriting from base patterns
4. Add vector search RPC function if needed
5. Update `UnifiedMemorySearchService` to include new type

### **Adding a New Embedding Service**

1. Create a new class inheriting from `BaseEmbeddingService`:

```python
class OpenAIEmbeddingService(BaseEmbeddingService):
    def initialize(self):
        # Setup OpenAI client
        pass

    def generate_embedding(self, text: str) -> List[float]:
        # Call OpenAI API
        pass
```

2. Update factory function to return new service:

```python
def get_embedding_service() -> BaseEmbeddingService:
    if settings.EMBEDDING_PROVIDER == "openai":
        return OpenAIEmbeddingService()
    return SnowflakeEmbeddingService()
```

### **Adding a New Storage Backend**

1. Create a new class inheriting from `BaseVectorStorage`:

```python
class PineconeVectorStorage(BaseVectorStorage):
    def initialize(self):
        # Setup Pinecone client
        pass

    async def store_document_chunks(...):
        # Store in Pinecone
        pass
```

2. API layer remains unchanged due to abstraction!

### **Adding New Endpoints**

Example: Adding bulk operations

1. Add schemas to `schemas.py`:

```python
class BulkAgentCreate(BaseModel):
    agents: List[AgentCreate]
```

2. Add service method to `agent_service.py`:

```python
async def create_bulk(self, agents: List[AgentCreate]):
    # Bulk insert logic
```

3. Add route to appropriate route file:

```python
@router.post("/agents/bulk")
async def create_agents_bulk(data: BulkAgentCreate):
    return await agent_service.create_bulk(data.agents)
```

## 🗄️ Database Schema Details

### **Core Tables (10)**

1. **model_providers**: AI model providers (GPT-4, Claude, etc.)

   - Columns: id, provider_name, provider_type, api_endpoint, api_key, model_name, max_tokens, temperature, is_default
   - Relations: Referenced by agents.model_provider_id

2. **tts_providers**: Text-to-speech providers

   - Columns: id, provider_name, provider_type, api_endpoint, api_key, voice_id, language_code, speed, is_default
   - Relations: Referenced by agents.tts_provider_id

3. **transcriber_providers**: Speech-to-text providers

   - Columns: id, provider_name, provider_type, api_endpoint, api_key, model_name, language_code, is_default
   - Relations: Referenced by agents.transcriber_provider_id

4. **toys**: Root entity for the system

   - Columns: id, name, description, is_active, created_at, updated_at
   - Relations: Parent to agents, toy_memory

5. **agents**: AI agents with provider links

   - Columns: id, toy_id, name, description, system_prompt, model_provider_id, tts_provider_id, transcriber_provider_id, is_active, language_code
   - Relations: Belongs to toy, has many agent_tools, agent_memory, conversation_logs

6. **agent_tools**: Tool registry with JSON schemas

   - Columns: id, toy_id, provider_name, tool_name, tool_description, tool_schema (JSONB)
   - Relations: Belongs to toy

7. **toy_memory**: Interaction context with vectors

   - Columns: id, toy_id, chunk_text, embedding (vector(768)), metadata (JSONB)
   - Relations: Belongs to toy, referenced by message_citations
   - Indexes: HNSW index on embedding

8. **agent_memory**: Knowledge base with file metadata

   - Columns: id, agent_id, toy_id, chunk_text, embedding (vector(768)), file_storage_path, file_name, page_number, metadata (JSONB)
   - Relations: Belongs to agent and toy, referenced by message_citations
   - Indexes: HNSW index on embedding

9. **conversation_logs**: Role-based message history

   - Columns: id, agent_id, toy_id, role (user/assistant/system/tool), content, timestamp
   - Relations: Belongs to agent and toy, parent to message_citations

10. **message_citations**: Links messages to memory sources
    - Columns: id, log_id, toy_memory_id, agent_memory_id, relevance_score
    - Relations: Belongs to conversation_log, references toy_memory OR agent_memory

### **RPC Functions (4)**

1. **match_toy_memory**: Search toy memory by vector similarity
2. **match_agent_memory**: Search agent memory by vector similarity
3. **match_documents**: Legacy document search (384-dim vectors)
4. **match_documents_by_id**: Legacy document search filtered by ID

All RPC functions use cosine similarity (1 - <=> operator) with HNSW indexing.

## 📊 Service Dependencies

```
┌─────────────────────────────────────────────────────────────┐
│                      API Routes Layer                        │
│  routes_providers.py ──┐                                     │
│  routes_toys_agents.py │                                     │
│  routes_memory.py      │                                     │
│  routes.py (legacy)    │                                     │
└────────────────────────┼─────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                    Service Layer                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Provider Services                                    │   │
│  │ ├── ModelProviderService                            │   │
│  │ ├── TTSProviderService                              │   │
│  │ └── TranscriberProviderService                      │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Entity Services                                      │   │
│  │ ├── ToyService                                       │   │
│  │ ├── AgentService ───► ModelProviderService          │   │
│  │ └── AgentToolsService                               │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Memory Services                                      │   │
│  │ ├── ToyMemoryService ───► EmbeddingService          │   │
│  │ ├── AgentMemoryService ─► EmbeddingService          │   │
│  │ └── UnifiedMemorySearchService                      │   │
│  │     ├── ToyMemoryService                            │   │
│  │     └── AgentMemoryService                          │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Conversation Services                                │   │
│  │ ├── ConversationService                             │   │
│  │ └── CitationService ──► ConversationService         │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              Core Infrastructure Services                    │
│  ├── EmbeddingService (Snowflake Arctic 768-dim)           │
│  ├── DocumentProcessor (LangChain)                         │
│  ├── VectorStorage (Supabase pgvector)                     │
│  └── SupabaseClient (Singleton)                            │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Key Architectural Decisions

### **Why Dual Memory System?**

- **Toy Memory**: Stores interaction patterns, user preferences, contextual information
  - Short-lived, frequently updated
  - Specific to toy-user interaction
- **Agent Memory**: Stores factual knowledge, documents, reference material
  - Long-lived, rarely modified
  - Tied to file storage for traceability

### **Why Separate Provider Tables?**

- Different provider types have different configuration needs
- Clear separation of concerns
- Easy to add new provider types
- Default provider per type (not global default)

### **Why Citation System?**

- Tracks information provenance
- Links AI responses to source material
- Enables "show me where this came from" features
- Supports explainable AI requirements

### **Why Modular Route Files?**

- Reduces cognitive load (4 files vs 1 monolithic)
- Clear ownership and responsibility
- Easier to navigate and maintain
- Independent versioning possible

### **Why 768-Dimension Vectors?**

- Upgraded from 384-dim for better semantic understanding
- Snowflake Arctic Embed M provides excellent quality
- Runs locally (no API costs)
- HNSW indexing keeps search fast despite higher dimensions

## 📈 Performance Considerations

### **Vector Search Optimization**

- HNSW indexes for O(log n) search time
- Separate indexes for toy_memory and agent_memory
- Similarity threshold filtering reduces result set
- RPC functions execute server-side (no data transfer overhead)

### **Caching Strategy**

- Singleton pattern for expensive resources (embedding models)
- Default provider lookup can be cached
- Conversation history pagination for large conversations

### **Connection Pooling**

- Supabase client uses connection pooling
- Single client instance shared across requests

## 🧪 Testing Strategy

### **Unit Tests**

- Test each service independently
- Mock Supabase client
- Test Pydantic schema validation

### **Integration Tests**

- Test API endpoints with real database (test schema)
- Verify vector search accuracy
- Test provider linking logic

### **End-to-End Tests**

- Create toy → agent → upload knowledge → search → conversation flow
- Test citation linking
- Verify memory isolation between toys

1. Add schema to `app/models/schemas.py`:

```python
class NewFeatureRequest(BaseModel):
    field1: str
    field2: int
```

2. Add endpoint to `app/api/routes.py`:

```python
@router.post("/new-feature", response_model=NewFeatureResponse)
async def new_feature(request: NewFeatureRequest):
    # Implementation
    pass
```

## 📊 Data Flow

```
User Request
    ↓
FastAPI (main.py)
    ↓
API Routes (routes.py)
    ↓
Pydantic Validation (schemas.py)
    ↓
Service Layer (services/)
    ↓
Database/External APIs
    ↓
Response (schemas.py)
    ↓
User
```

## 🧪 Testing Strategy

### **Unit Tests**

- Test individual services
- Mock dependencies
- Fast execution

### **Integration Tests**

- Test API endpoints
- Use test database
- Validate full flow

### **End-to-End Tests**

- Test complete user workflows
- Upload → Store → Search
- Verify results

## 🔒 Security Considerations

- Environment variables for secrets
- API key validation
- Input sanitization via Pydantic
- CORS configuration
- Rate limiting (future enhancement)

## 📈 Performance Optimization

- Singleton pattern for expensive resources
- Batch embedding generation
- Database indexing (pgvector)
- Caching (future enhancement)

## 🎯 Best Practices

1. **Always use base classes** when defining new services
2. **Type hints** on all functions
3. **Pydantic models** for data validation
4. **Factory functions** for service instantiation
5. **Centralized configuration** in `config.py`
6. **Async/await** for I/O operations
7. **Error handling** at API layer
8. **Logging** (future enhancement)

## 🚀 Future Enhancements

- [ ] Add logging service
- [ ] Implement caching layer
- [ ] Add rate limiting
- [ ] Create admin dashboard
- [ ] Add metrics/monitoring
- [ ] Implement batch processing
- [ ] Add webhooks
- [ ] Create CLI tools
