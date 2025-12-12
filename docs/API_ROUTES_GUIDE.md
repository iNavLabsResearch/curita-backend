# API Routes Documentation - Modular CRUD Endpoints

## Overview

This document provides comprehensive documentation for all modular CRUD API endpoints in the Curita Backend system. All routes follow RESTful conventions and industry best practices.

**Base URL**: `/api/v1`

**Total Tables Covered**: 11 tables with full CRUD operations
**Total Endpoints**: 120+ endpoints across all modules

---

## Table of Contents

1. [Toy Routes](#toy-routes) - `/api/v1/toys`
2. [Agent Routes](#agent-routes) - `/api/v1/agents`
3. [Agent Tool Routes](#agent-tool-routes) - `/api/v1/agent-tools`
4. [Model Provider Routes](#model-provider-routes) - `/api/v1/model-providers`
5. [TTS Provider Routes](#tts-provider-routes) - `/api/v1/tts-providers`
6. [Transcriber Provider Routes](#transcriber-provider-routes) - `/api/v1/transcriber-providers`
7. [Toy Memory Routes](#toy-memory-routes) - `/api/v1/toy-memory`
8. [Agent Memory Routes](#agent-memory-routes) - `/api/v1/agent-memory`
9. [Conversation Log Routes](#conversation-log-routes) - `/api/v1/conversations`
10. [Message Citation Routes](#message-citation-routes) - `/api/v1/message-citations`

---

## 1. Toy Routes

**Base Path**: `/api/v1/toys`
**Tag**: `Toys`
**File**: `routes_toy.py`

### Endpoints

| Method | Endpoint                         | Summary                  | Status Code |
| ------ | -------------------------------- | ------------------------ | ----------- |
| POST   | `/`                              | Create a new toy         | 201         |
| GET    | `/{toy_id}`                      | Get toy by ID            | 200         |
| GET    | `/`                              | Get all toys (paginated) | 200         |
| GET    | `/active/list`                   | Get all active toys      | 200         |
| GET    | `/search/by-name?name={pattern}` | Search toys by name      | 200         |
| PUT    | `/{toy_id}`                      | Update toy               | 200         |
| PATCH  | `/{toy_id}/activate`             | Activate toy             | 200         |
| PATCH  | `/{toy_id}/deactivate`           | Deactivate toy           | 200         |
| DELETE | `/{toy_id}`                      | Delete toy               | 204         |
| GET    | `/count/total`                   | Count toys               | 200         |
| GET    | `/exists/{toy_id}`               | Check if toy exists      | 200         |

**Total**: 11 endpoints

### Query Parameters

- `limit` (int, default=100, max=1000): Maximum records to return
- `offset` (int, default=0): Number of records to skip
- `is_active` (bool, optional): Filter by active status
- `name` (string): Search pattern for name

---

## 2. Agent Routes

**Base Path**: `/api/v1/agents`
**Tag**: `Agents`
**File**: `routes_agent.py`

### Endpoints

| Method | Endpoint                              | Summary                            | Status Code |
| ------ | ------------------------------------- | ---------------------------------- | ----------- |
| POST   | `/`                                   | Create a new agent                 | 201         |
| GET    | `/{agent_id}`                         | Get agent by ID                    | 200         |
| GET    | `/`                                   | Get all agents (paginated)         | 200         |
| GET    | `/toy/{toy_id}/all`                   | Get agents by toy ID               | 200         |
| GET    | `/toy/{toy_id}/active`                | Get active agents by toy ID        | 200         |
| GET    | `/provider/model/{provider_id}`       | Get agents by model provider       | 200         |
| GET    | `/provider/tts/{provider_id}`         | Get agents by TTS provider         | 200         |
| GET    | `/provider/transcriber/{provider_id}` | Get agents by transcriber provider | 200         |
| PUT    | `/{agent_id}`                         | Update agent                       | 200         |
| DELETE | `/{agent_id}`                         | Delete agent                       | 204         |
| GET    | `/count/total`                        | Count agents                       | 200         |
| GET    | `/exists/{agent_id}`                  | Check if agent exists              | 200         |

**Total**: 12 endpoints

---

## 3. Agent Tool Routes

**Base Path**: `/api/v1/agent-tools`
**Tag**: `Agent Tools`
**File**: `routes_agent_tool.py`

### Endpoints

| Method | Endpoint                         | Summary                         | Status Code |
| ------ | -------------------------------- | ------------------------------- | ----------- |
| POST   | `/`                              | Create a new agent tool         | 201         |
| GET    | `/{tool_id}`                     | Get agent tool by ID            | 200         |
| GET    | `/`                              | Get all agent tools (paginated) | 200         |
| GET    | `/toy/{toy_id}/all`              | Get tools by toy ID             | 200         |
| GET    | `/provider/{provider_name}`      | Get tools by provider name      | 200         |
| GET    | `/http-method/{method}`          | Get tools by HTTP method        | 200         |
| GET    | `/search/by-name?name={pattern}` | Search tools by name            | 200         |
| PUT    | `/{tool_id}`                     | Update agent tool               | 200         |
| DELETE | `/{tool_id}`                     | Delete agent tool               | 204         |
| GET    | `/count/total`                   | Count agent tools               | 200         |
| GET    | `/exists/{tool_id}`              | Check if tool exists            | 200         |

**Total**: 11 endpoints

---

## 4. Model Provider Routes

**Base Path**: `/api/v1/model-providers`
**Tag**: `Model Providers`
**File**: `routes_model_provider.py`

### Endpoints

| Method | Endpoint                     | Summary                             | Status Code |
| ------ | ---------------------------- | ----------------------------------- | ----------- |
| POST   | `/`                          | Create a new model provider         | 201         |
| GET    | `/{provider_id}`             | Get model provider by ID            | 200         |
| GET    | `/`                          | Get all model providers (paginated) | 200         |
| GET    | `/default/get`               | Get default model provider          | 200         |
| GET    | `/provider/{provider_name}`  | Get model providers by name         | 200         |
| GET    | `/large-models/list`         | Get large model providers           | 200         |
| PUT    | `/{provider_id}`             | Update model provider               | 200         |
| PATCH  | `/{provider_id}/set-default` | Set as default provider             | 200         |
| DELETE | `/{provider_id}`             | Delete model provider               | 204         |
| GET    | `/count/total`               | Count model providers               | 200         |
| GET    | `/exists/{provider_id}`      | Check if provider exists            | 200         |

**Total**: 11 endpoints

---

## 5. TTS Provider Routes

**Base Path**: `/api/v1/tts-providers`
**Tag**: `TTS Providers`
**File**: `routes_tts_provider.py`

### Endpoints

| Method | Endpoint                     | Summary                           | Status Code |
| ------ | ---------------------------- | --------------------------------- | ----------- |
| POST   | `/`                          | Create a new TTS provider         | 201         |
| GET    | `/{provider_id}`             | Get TTS provider by ID            | 200         |
| GET    | `/`                          | Get all TTS providers (paginated) | 200         |
| GET    | `/default/get`               | Get default TTS provider          | 200         |
| GET    | `/provider/{provider_name}`  | Get TTS providers by name         | 200         |
| PUT    | `/{provider_id}`             | Update TTS provider               | 200         |
| PATCH  | `/{provider_id}/set-default` | Set as default provider           | 200         |
| DELETE | `/{provider_id}`             | Delete TTS provider               | 204         |
| GET    | `/count/total`               | Count TTS providers               | 200         |
| GET    | `/exists/{provider_id}`      | Check if provider exists          | 200         |

**Total**: 10 endpoints

---

## 6. Transcriber Provider Routes

**Base Path**: `/api/v1/transcriber-providers`
**Tag**: `Transcriber Providers`
**File**: `routes_transcriber_provider.py`

### Endpoints

| Method | Endpoint                     | Summary                                   | Status Code |
| ------ | ---------------------------- | ----------------------------------------- | ----------- |
| POST   | `/`                          | Create a new transcriber provider         | 201         |
| GET    | `/{provider_id}`             | Get transcriber provider by ID            | 200         |
| GET    | `/`                          | Get all transcriber providers (paginated) | 200         |
| GET    | `/default/get`               | Get default transcriber provider          | 200         |
| GET    | `/provider/{provider_name}`  | Get transcriber providers by name         | 200         |
| GET    | `/model-size/{size}`         | Get transcribers by model size            | 200         |
| PUT    | `/{provider_id}`             | Update transcriber provider               | 200         |
| PATCH  | `/{provider_id}/set-default` | Set as default provider                   | 200         |
| DELETE | `/{provider_id}`             | Delete transcriber provider               | 204         |
| GET    | `/count/total`               | Count transcriber providers               | 200         |
| GET    | `/exists/{provider_id}`      | Check if provider exists                  | 200         |

**Total**: 11 endpoints

---

## 7. Toy Memory Routes

**Base Path**: `/api/v1/toy-memory`
**Tag**: `Toy Memory`
**File**: `routes_memory.py`

### Endpoints

| Method | Endpoint            | Summary                          | Status Code |
| ------ | ------------------- | -------------------------------- | ----------- |
| POST   | `/`                 | Create a new toy memory          | 201         |
| GET    | `/{memory_id}`      | Get toy memory by ID             | 200         |
| GET    | `/`                 | Get all toy memories (paginated) | 200         |
| GET    | `/toy/{toy_id}/all` | Get memories by toy ID           | 200         |
| POST   | `/search/embedding` | Search by embedding vector       | 200         |
| PUT    | `/{memory_id}`      | Update toy memory                | 200         |
| DELETE | `/{memory_id}`      | Delete toy memory                | 204         |
| DELETE | `/toy/{toy_id}/all` | Delete all memories for toy      | 204         |

**Total**: 8 endpoints

---

## 8. Agent Memory Routes

**Base Path**: `/api/v1/agent-memory`
**Tag**: `Agent Memory`
**File**: `routes_memory.py`

### Endpoints

| Method | Endpoint                | Summary                            | Status Code |
| ------ | ----------------------- | ---------------------------------- | ----------- |
| POST   | `/`                     | Create a new agent memory          | 201         |
| GET    | `/{memory_id}`          | Get agent memory by ID             | 200         |
| GET    | `/`                     | Get all agent memories (paginated) | 200         |
| GET    | `/agent/{agent_id}/all` | Get memories by agent ID           | 200         |
| POST   | `/search/embedding`     | Search by embedding vector         | 200         |
| PUT    | `/{memory_id}`          | Update agent memory                | 200         |
| DELETE | `/{memory_id}`          | Delete agent memory                | 204         |
| DELETE | `/agent/{agent_id}/all` | Delete all memories for agent      | 204         |

**Total**: 8 endpoints

---

## 9. Conversation Log Routes

**Base Path**: `/api/v1/conversations`
**Tag**: `Conversations`
**File**: `routes_conversation.py`

### Endpoints

| Method | Endpoint                | Summary                               | Status Code |
| ------ | ----------------------- | ------------------------------------- | ----------- |
| POST   | `/`                     | Create a new conversation log         | 201         |
| GET    | `/{log_id}`             | Get conversation log by ID            | 200         |
| GET    | `/`                     | Get all conversation logs (paginated) | 200         |
| GET    | `/toy/{toy_id}/history` | Get conversation history for toy      | 200         |
| GET    | `/toy/{toy_id}/recent`  | Get recent messages for toy           | 200         |
| DELETE | `/{log_id}`             | Delete conversation log               | 204         |
| GET    | `/count/total`          | Count conversation logs               | 200         |

**Total**: 7 endpoints

**Note**: Conversation logs are immutable by design (no UPDATE endpoint).

---

## 10. Message Citation Routes

**Base Path**: `/api/v1/message-citations`
**Tag**: `Message Citations`
**File**: `routes_conversation.py`

### Endpoints

| Method | Endpoint                             | Summary                               | Status Code |
| ------ | ------------------------------------ | ------------------------------------- | ----------- |
| POST   | `/`                                  | Create a new message citation         | 201         |
| GET    | `/{citation_id}`                     | Get message citation by ID            | 200         |
| GET    | `/`                                  | Get all message citations (paginated) | 200         |
| GET    | `/message/{conversation_log_id}/all` | Get citations for a message           | 200         |
| PUT    | `/{citation_id}`                     | Update message citation               | 200         |
| DELETE | `/{citation_id}`                     | Delete message citation               | 204         |
| DELETE | `/message/{conversation_log_id}/all` | Delete all citations for message      | 204         |
| GET    | `/count/total`                       | Count message citations               | 200         |

**Total**: 8 endpoints

---

## Common Patterns

### Pagination

All list endpoints support pagination with these query parameters:

- `limit` (int, default=100, max=1000): Maximum number of records
- `offset` (int, default=0): Number of records to skip

Example:

```
GET /api/v1/toys?limit=50&offset=100
```

### Filtering

Many endpoints support filtering via query parameters:

- `is_active`: Filter by active status (boolean)
- `toy_id`, `agent_id`: Filter by parent entity
- `provider_name`: Filter by provider name

Example:

```
GET /api/v1/agents?is_active=true&toy_id=123e4567-e89b-12d3-a456-426614174000
```

### Error Responses

All endpoints return consistent error responses:

**404 Not Found**:

```json
{
  "detail": "Resource with ID {id} not found"
}
```

**500 Internal Server Error**:

```json
{
  "detail": "Error message details"
}
```

**400 Bad Request**:

```json
{
  "detail": "Invalid input data"
}
```

---

## Summary

### Endpoints by Module

| Module                | Endpoints | File                             |
| --------------------- | --------- | -------------------------------- |
| Toys                  | 11        | `routes_toy.py`                  |
| Agents                | 12        | `routes_agent.py`                |
| Agent Tools           | 11        | `routes_agent_tool.py`           |
| Model Providers       | 11        | `routes_model_provider.py`       |
| TTS Providers         | 10        | `routes_tts_provider.py`         |
| Transcriber Providers | 11        | `routes_transcriber_provider.py` |
| Toy Memory            | 8         | `routes_memory.py`               |
| Agent Memory          | 8         | `routes_memory.py`               |
| Conversation Logs     | 7         | `routes_conversation.py`         |
| Message Citations     | 8         | `routes_conversation.py`         |
| **Total**             | **97**    | **10 files**                     |

### Architecture Benefits

✅ **Modular Design**: Each table has its own dedicated route file
✅ **Separation of Concerns**: Clear boundaries between different entities
✅ **Maintainability**: Easy to locate and update specific endpoints
✅ **Scalability**: Simple to add new routes or modify existing ones
✅ **Type Safety**: Full Pydantic schema validation
✅ **Error Handling**: Comprehensive error responses with logging
✅ **RESTful**: Follows REST conventions and HTTP standards
✅ **Documentation**: Auto-generated OpenAPI/Swagger docs at `/docs`

---

## Testing

Access interactive API documentation at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

All endpoints are automatically documented with request/response schemas, parameters, and example values.

---

## Related Documentation

- [CRUD Implementation Guide](../CRUD_IMPLEMENTATION_GUIDE.md)
- [CRUD Quick Reference](../CRUD_QUICK_REFERENCE.md)
- [Database Schema](../supabase_schema.sql)
