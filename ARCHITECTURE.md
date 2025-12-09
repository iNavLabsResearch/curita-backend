# Curita Backend - Modular Architecture

## 📁 Updated Project Structure

```
curita-backend/
├── app/
│   ├── __init__.py
│   ├── core/                      # Core configuration
│   │   ├── __init__.py
│   │   └── config.py              # Centralized settings
│   ├── models/                    # Data models
│   │   ├── __init__.py
│   │   └── schemas.py             # Pydantic schemas
│   ├── services/                  # Business logic
│   │   ├── __init__.py
│   │   ├── base.py                # Base service classes
│   │   ├── document_processor.py  # Text extraction & chunking
│   │   ├── embedding_service.py   # Snowflake embeddings
│   │   ├── vector_storage.py      # Supabase storage
│   │   └── search_service.py      # Search functionality
│   ├── api/                       # API layer
│   │   ├── __init__.py
│   │   └── routes.py              # API endpoints
│   └── utilities/                 # Utility functions
│       ├── __init__.py
│       └── supabase_client.py     # Supabase connection
├── main.py                        # Application entry point
├── requirements.txt
├── supabase_schema.sql
├── .env.example
├── .gitignore
├── example_usage.py
├── ARCHITECTURE.md                # This file
└── README.md
```

## 🏗️ Architecture Overview

### 1. **Core Layer** (`app/core/`)

- **Purpose**: Application configuration and settings
- **Key Components**:
  - `config.py`: Centralized configuration using Pydantic Settings
  - Environment variable management
  - Application-wide constants

### 2. **Models Layer** (`app/models/`)

- **Purpose**: Data models and schemas
- **Key Components**:
  - `schemas.py`: Pydantic models for request/response validation
  - Type-safe data structures
  - Input validation

### 3. **Services Layer** (`app/services/`)

- **Purpose**: Business logic and core functionality
- **Base Classes** (`base.py`):

  - `BaseService`: Common service functionality
  - `BaseEmbeddingService`: Interface for embedding services
  - `BaseDocumentProcessor`: Interface for document processing
  - `BaseVectorStorage`: Interface for vector storage
  - `BaseSearchService`: Interface for search operations

- **Implementations**:
  - `SnowflakeEmbeddingService`: Snowflake Arctic Embed integration
  - `LangChainDocumentProcessor`: Text extraction and chunking using LangChain
  - `SupabaseVectorStorage`: Supabase pgvector storage
  - `SupabaseSearchService`: Vector similarity search

### 4. **API Layer** (`app/api/`)

- **Purpose**: HTTP endpoints and request handling
- **Key Components**:
  - `routes.py`: RESTful API endpoints
  - Request validation
  - Response formatting

### 5. **Utilities Layer** (`app/utilities/`)

- **Purpose**: Helper functions and shared utilities
- **Key Components**:
  - `supabase_client.py`: Singleton Supabase client

## 🔧 Design Patterns Used

### 1. **Dependency Injection**

- Services are injected via factory functions
- Easy to mock for testing
- Loose coupling between components

```python
# Example
embedding_service = get_embedding_service()
vector_storage = get_vector_storage_service()
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

```python
def get_embedding_service() -> SnowflakeEmbeddingService:
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = SnowflakeEmbeddingService()
    return _embedding_service
```

### 5. **Configuration Management**

- Centralized settings using Pydantic
- Type-safe configuration
- Environment-based configuration

```python
settings = get_settings()
chunk_size = settings.DEFAULT_CHUNK_SIZE
```

## 🚀 Benefits of This Architecture

### **Scalability**

- Easy to add new services
- Clear separation of concerns
- Modular components

### **Maintainability**

- Single responsibility principle
- Easy to locate and fix bugs
- Clear dependencies

### **Testability**

- Mock services easily
- Unit test individual components
- Integration test API layer

### **Flexibility**

- Swap implementations without changing API
- Example: Switch from Snowflake to OpenAI embeddings
- Add new storage backends

### **Type Safety**

- Pydantic models for validation
- Type hints throughout
- Catch errors at development time

## 🔌 Extending the System

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

2. API layer remains unchanged!

### **Adding New Endpoints**

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
