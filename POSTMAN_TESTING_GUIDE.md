# Postman Testing Guide for Curita Backend CRUD APIs

## Base URL
```
http://localhost:8000/api/v1
```

## Setup Instructions

1. **Start the server:**
   ```bash
   python main.py
   ```
   Server runs on `http://localhost:8000` by default

2. **Import to Postman:**
   - Create a new Collection named "Curita Backend CRUD APIs"
   - Set collection variable: `base_url` = `http://localhost:8000/api/v1`
   - Use `{{base_url}}` in all requests

3. **Headers:**
   - `Content-Type: application/json` (for POST/PUT requests)
   - `Accept: application/json`

---

## 1. Provider Management APIs

### 1.1 Model Providers

#### Create Model Provider
- **Method:** `POST`
- **URL:** `{{base_url}}/providers/models`
- **Body (JSON):**
```json
{
  "provider_name": "openai",
  "model_name": "gpt-4",
  "is_large_model": true,
  "default_temperature": 0.7,
  "supported_languages": ["en", "es"],
  "api_key_template": "sk-{key}",
  "api_base": "https://api.openai.com/v1",
  "api_key": "your-api-key",
  "is_default": false
}
```

#### List Model Providers
- **Method:** `GET`
- **URL:** `{{base_url}}/providers/models?limit=100&offset=0`

#### Get Default Model Provider
- **Method:** `GET`
- **URL:** `{{base_url}}/providers/models/default`

#### Get Model Provider by ID
- **Method:** `GET`
- **URL:** `{{base_url}}/providers/models/{provider_id}`
- **Example:** `{{base_url}}/providers/models/123e4567-e89b-12d3-a456-426614174000`

#### Update Model Provider
- **Method:** `PUT`
- **URL:** `{{base_url}}/providers/models/{provider_id}`
- **Body (JSON):**
```json
{
  "default_temperature": 0.8,
  "is_default": true
}
```

#### Set Default Model Provider
- **Method:** `POST`
- **URL:** `{{base_url}}/providers/models/{provider_id}/set-default`

#### Delete Model Provider
- **Method:** `DELETE`
- **URL:** `{{base_url}}/providers/models/{provider_id}`

---

### 1.2 TTS Providers

#### Create TTS Provider
- **Method:** `POST`
- **URL:** `{{base_url}}/providers/tts`
- **Body (JSON):**
```json
{
  "provider_name": "elevenlabs",
  "model_name": "eleven_multilingual_v2",
  "supported_languages": ["en", "es", "fr"],
  "requires_api_key": true,
  "default_endpoint": "https://api.elevenlabs.io/v1",
  "api_key_template": "{key}",
  "api_key": "your-api-key",
  "is_default": false,
  "default_voice": "21m00Tcm4TlvDq8ikWAM"
}
```

#### List TTS Providers
- **Method:** `GET`
- **URL:** `{{base_url}}/providers/tts?limit=100&offset=0`

#### Get TTS Provider by ID
- **Method:** `GET`
- **URL:** `{{base_url}}/providers/tts/{provider_id}`

#### Update TTS Provider
- **Method:** `PUT`
- **URL:** `{{base_url}}/providers/tts/{provider_id}`
- **Body (JSON):**
```json
{
  "default_voice": "new-voice-id",
  "is_default": true
}
```

#### Delete TTS Provider
- **Method:** `DELETE`
- **URL:** `{{base_url}}/providers/tts/{provider_id}`

---

### 1.3 Transcriber Providers

#### Create Transcriber Provider
- **Method:** `POST`
- **URL:** `{{base_url}}/providers/transcribers`
- **Body (JSON):**
```json
{
  "name": "Deepgram Whisper",
  "provider_name": "deepgram",
  "model_name": "whisper-large",
  "supported_languages": ["en", "es", "fr"],
  "requires_api_key": true,
  "default_endpoint": "https://api.deepgram.com/v1",
  "api_key_template": "{key}",
  "model_size": "large",
  "is_default": false,
  "api_key": "your-api-key"
}
```

#### List Transcriber Providers
- **Method:** `GET`
- **URL:** `{{base_url}}/providers/transcribers?limit=100&offset=0`

#### Get Transcriber Provider by ID
- **Method:** `GET`
- **URL:** `{{base_url}}/providers/transcribers/{provider_id}`

#### Update Transcriber Provider
- **Method:** `PUT`
- **URL:** `{{base_url}}/providers/transcribers/{provider_id}`
- **Body (JSON):**
```json
{
  "model_size": "medium",
  "is_default": true
}
```

#### Delete Transcriber Provider
- **Method:** `DELETE`
- **URL:** `{{base_url}}/providers/transcribers/{provider_id}`

---

## 2. Toy Management APIs

#### Create Toy
- **Method:** `POST`
- **URL:** `{{base_url}}/toys`
- **Body (JSON):**
```json
{
  "name": "My Talking Toy",
  "description": "A smart interactive toy",
  "avatar_url": "https://example.com/avatar.png",
  "user_custom_instruction": "Be friendly and helpful",
  "is_active": true
}
```

#### List Toys
- **Method:** `GET`
- **URL:** `{{base_url}}/toys?limit=100&offset=0&is_active=true`
- **Query Params:**
  - `limit` (optional, default: 100)
  - `offset` (optional, default: 0)
  - `is_active` (optional, true/false)

#### Get Toy by ID
- **Method:** `GET`
- **URL:** `{{base_url}}/toys/{toy_id}`

#### Update Toy
- **Method:** `PUT`
- **URL:** `{{base_url}}/toys/{toy_id}`
- **Body (JSON):**
```json
{
  "name": "Updated Toy Name",
  "description": "Updated description",
  "is_active": false
}
```

#### Activate/Deactivate Toy
- **Method:** `POST`
- **URL:** `{{base_url}}/toys/{toy_id}/activate?is_active=true`
- **Query Params:**
  - `is_active` (true/false)

#### Delete Toy
- **Method:** `DELETE`
- **URL:** `{{base_url}}/toys/{toy_id}`
- **Note:** Cascades to agents, tools, and memories

---

## 3. Agent Management APIs

#### Create Agent
- **Method:** `POST`
- **URL:** `{{base_url}}/agents`
- **Body (JSON):**
```json
{
  "toy_id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Assistant Agent",
  "system_prompt": "You are a helpful assistant",
  "model_provider_id": "123e4567-e89b-12d3-a456-426614174001",
  "tts_provider_id": "123e4567-e89b-12d3-a456-426614174002",
  "transcriber_provider_id": "123e4567-e89b-12d3-a456-426614174003",
  "voice_id": "voice-123",
  "language_code": "en-US",
  "is_active": true
}
```

#### List Agents by Toy
- **Method:** `GET`
- **URL:** `{{base_url}}/toys/{toy_id}/agents?is_active=true`
- **Query Params:**
  - `is_active` (optional, true/false)

#### Get Agent by ID
- **Method:** `GET`
- **URL:** `{{base_url}}/agents/{agent_id}?with_providers=false`
- **Query Params:**
  - `with_providers` (optional, true/false) - Include provider details

#### Update Agent
- **Method:** `PUT`
- **URL:** `{{base_url}}/agents/{agent_id}`
- **Body (JSON):**
```json
{
  "name": "Updated Agent Name",
  "system_prompt": "Updated system prompt",
  "is_active": false
}
```

#### Delete Agent
- **Method:** `DELETE`
- **URL:** `{{base_url}}/agents/{agent_id}`
- **Note:** Cascades to memories and conversations

---

## 4. Agent Tools APIs

#### Create Agent Tool
- **Method:** `POST`
- **URL:** `{{base_url}}/tools`
- **Body (JSON):**
```json
{
  "toy_id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Weather Tool",
  "url": "https://api.weather.com/v1/forecast",
  "headers_schema": {
    "Authorization": "Bearer {token}",
    "Content-Type": "application/json"
  },
  "payload_schema": {
    "location": "string",
    "units": "metric"
  },
  "tool_schema": {
    "type": "function",
    "function": {
      "name": "get_weather",
      "description": "Get weather forecast",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {"type": "string"},
          "units": {"type": "string"}
        }
      }
    }
  },
  "http_method": "POST",
  "provider_name": "weather_api",
  "output_schema": {
    "temperature": "number",
    "condition": "string"
  }
}
```

#### List Tools by Toy
- **Method:** `GET`
- **URL:** `{{base_url}}/toys/{toy_id}/tools`

#### Get Tool by ID
- **Method:** `GET`
- **URL:** `{{base_url}}/tools/{tool_id}`

#### Update Tool
- **Method:** `PUT`
- **URL:** `{{base_url}}/tools/{tool_id}`
- **Body (JSON):**
```json
{
  "name": "Updated Tool Name",
  "url": "https://new-api-url.com"
}
```

#### Delete Tool
- **Method:** `DELETE`
- **URL:** `{{base_url}}/tools/{tool_id}`

---

## 5. Memory Management APIs

### 5.1 Memory Search

#### Search Memory
- **Method:** `POST`
- **URL:** `{{base_url}}/memory/memory/search`
- **Body (JSON):**
```json
{
  "query": "What is the weather today?",
  "top_k": 5,
  "similarity_threshold": 0.7,
  "memory_type": "both",
  "toy_id": "123e4567-e89b-12d3-a456-426614174000",
  "agent_id": "123e4567-e89b-12d3-a456-426614174001"
}
```
- **memory_type options:** `"toy"`, `"agent"`, `"both"`

---

### 5.2 Toy Memory

#### Upload to Toy Memory
- **Method:** `POST`
- **URL:** `{{base_url}}/memory/toys/{toy_id}/memory`
- **Content-Type:** `multipart/form-data`
- **Body (form-data):**
  - `file`: (File) - Upload document (PDF, DOCX, TXT)
  - `content_type`: (Text, optional) - e.g., "text", "document"
  - `chunk_size`: (Number, optional, default: 1000)
  - `chunk_overlap`: (Number, optional, default: 200)

#### Get Toy Memory
- **Method:** `GET`
- **URL:** `{{base_url}}/memory/toys/{toy_id}/memory?limit=100`
- **Query Params:**
  - `limit` (optional, default: 100)

#### Delete Toy Memory
- **Method:** `DELETE`
- **URL:** `{{base_url}}/memory/toys/{toy_id}/memory`

---

### 5.3 Agent Memory

#### Upload to Agent Memory
- **Method:** `POST`
- **URL:** `{{base_url}}/memory/agents/{agent_id}/memory?toy_id={toy_id}`
- **Content-Type:** `multipart/form-data`
- **Query Params:**
  - `toy_id` (required) - UUID of the toy
- **Body (form-data):**
  - `file`: (File) - Upload document
  - `content_type`: (Text, optional)
  - `chunk_size`: (Number, optional, default: 1000)
  - `chunk_overlap`: (Number, optional, default: 200)

#### Get Agent Memory
- **Method:** `GET`
- **URL:** `{{base_url}}/memory/agents/{agent_id}/memory?limit=100`
- **Query Params:**
  - `limit` (optional, default: 100)

#### Delete Agent Memory
- **Method:** `DELETE`
- **URL:** `{{base_url}}/memory/agents/{agent_id}/memory`

---

## 6. Conversation Management APIs

#### Add Message to Conversation
- **Method:** `POST`
- **URL:** `{{base_url}}/memory/agents/{agent_id}/conversation`
- **Body (JSON):**
```json
{
  "agent_id": "123e4567-e89b-12d3-a456-426614174001",
  "role": "user",
  "content": "Hello, how are you?"
}
```
- **role options:** `"user"`, `"assistant"`, `"system"`, `"tool"`

#### Get Conversation History
- **Method:** `GET`
- **URL:** `{{base_url}}/memory/agents/{agent_id}/conversation?limit=100&offset=0&include_citations=false`
- **Query Params:**
  - `limit` (optional, default: 100)
  - `offset` (optional, default: 0)
  - `include_citations` (optional, default: false)

#### Clear Conversation
- **Method:** `DELETE`
- **URL:** `{{base_url}}/memory/agents/{agent_id}/conversation?keep_system=true`
- **Query Params:**
  - `keep_system` (optional, default: true) - Keep system messages

---

## 7. Health Check

#### Health Check
- **Method:** `GET`
- **URL:** `{{base_url}}/health`

---

## Postman Collection Structure

### Recommended Folder Structure:

```
Curita Backend CRUD APIs
├── 1. Providers
│   ├── Model Providers
│   │   ├── Create Model Provider
│   │   ├── List Model Providers
│   │   ├── Get Default Model Provider
│   │   ├── Get Model Provider by ID
│   │   ├── Update Model Provider
│   │   ├── Set Default Model Provider
│   │   └── Delete Model Provider
│   ├── TTS Providers
│   │   ├── Create TTS Provider
│   │   ├── List TTS Providers
│   │   ├── Get TTS Provider by ID
│   │   ├── Update TTS Provider
│   │   └── Delete TTS Provider
│   └── Transcriber Providers
│       ├── Create Transcriber Provider
│       ├── List Transcriber Providers
│       ├── Get Transcriber Provider by ID
│       ├── Update Transcriber Provider
│       └── Delete Transcriber Provider
├── 2. Toys
│   ├── Create Toy
│   ├── List Toys
│   ├── Get Toy by ID
│   ├── Update Toy
│   ├── Activate/Deactivate Toy
│   └── Delete Toy
├── 3. Agents
│   ├── Create Agent
│   ├── List Agents by Toy
│   ├── Get Agent by ID
│   ├── Update Agent
│   └── Delete Agent
├── 4. Agent Tools
│   ├── Create Tool
│   ├── List Tools by Toy
│   ├── Get Tool by ID
│   ├── Update Tool
│   └── Delete Tool
├── 5. Memory
│   ├── Search Memory
│   ├── Toy Memory
│   │   ├── Upload to Toy Memory
│   │   ├── Get Toy Memory
│   │   └── Delete Toy Memory
│   ├── Agent Memory
│   │   ├── Upload to Agent Memory
│   │   ├── Get Agent Memory
│   │   └── Delete Agent Memory
│   └── Conversations
│       ├── Add Message
│       ├── Get Conversation History
│       └── Clear Conversation
└── 6. Health Check
    └── Health Check
```

---

## Testing Workflow

### Recommended Testing Order:

1. **Health Check** - Verify server is running
2. **Create Providers** - Create model, TTS, and transcriber providers
3. **Create Toy** - Create a toy
4. **Create Agent** - Create an agent linked to the toy and providers
5. **Create Tools** - Create agent tools
6. **Upload Memory** - Upload content to toy/agent memory
7. **Search Memory** - Test memory search
8. **Conversations** - Add messages and retrieve history
9. **Update Operations** - Test updates
10. **Delete Operations** - Test deletions (in reverse order)

---

## Common Response Codes

- `200 OK` - Success
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Tips

1. **Save IDs:** After creating resources, save the returned IDs as Postman variables for use in subsequent requests
2. **Use Pre-request Scripts:** Automatically extract IDs from responses
3. **Environment Variables:** Create different environments for dev/staging/prod
4. **Tests:** Add assertions to validate responses
5. **Documentation:** Use Postman's documentation feature to generate API docs

---

## Example Pre-request Script (Save Toy ID)

```javascript
// In "Create Toy" request, add this to Tests tab:
if (pm.response.code === 201) {
    const response = pm.response.json();
    pm.environment.set("toy_id", response.id);
    console.log("Toy ID saved:", response.id);
}
```

## Example Test Script (Validate Response)

```javascript
// Add to Tests tab in any request:
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has success field", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('id');
});
```

---

## Quick Reference: All Endpoints

### Providers (18 endpoints)
- `POST /api/v1/providers/models`
- `GET /api/v1/providers/models`
- `GET /api/v1/providers/models/default`
- `GET /api/v1/providers/models/{id}`
- `PUT /api/v1/providers/models/{id}`
- `POST /api/v1/providers/models/{id}/set-default`
- `DELETE /api/v1/providers/models/{id}`
- `POST /api/v1/providers/tts`
- `GET /api/v1/providers/tts`
- `GET /api/v1/providers/tts/{id}`
- `PUT /api/v1/providers/tts/{id}`
- `DELETE /api/v1/providers/tts/{id}`
- `POST /api/v1/providers/transcribers`
- `GET /api/v1/providers/transcribers`
- `GET /api/v1/providers/transcribers/{id}`
- `PUT /api/v1/providers/transcribers/{id}`
- `DELETE /api/v1/providers/transcribers/{id}`

### Toys (6 endpoints)
- `POST /api/v1/toys`
- `GET /api/v1/toys`
- `GET /api/v1/toys/{toy_id}`
- `PUT /api/v1/toys/{toy_id}`
- `POST /api/v1/toys/{toy_id}/activate`
- `DELETE /api/v1/toys/{toy_id}`

### Agents (5 endpoints)
- `POST /api/v1/agents`
- `GET /api/v1/toys/{toy_id}/agents`
- `GET /api/v1/agents/{agent_id}`
- `PUT /api/v1/agents/{agent_id}`
- `DELETE /api/v1/agents/{agent_id}`

### Tools (5 endpoints)
- `POST /api/v1/tools`
- `GET /api/v1/toys/{toy_id}/tools`
- `GET /api/v1/tools/{tool_id}`
- `PUT /api/v1/tools/{tool_id}`
- `DELETE /api/v1/tools/{tool_id}`

### Memory (8 endpoints)
- `POST /api/v1/memory/memory/search`
- `POST /api/v1/memory/toys/{toy_id}/memory`
- `GET /api/v1/memory/toys/{toy_id}/memory`
- `DELETE /api/v1/memory/toys/{toy_id}/memory`
- `POST /api/v1/memory/agents/{agent_id}/memory`
- `GET /api/v1/memory/agents/{agent_id}/memory`
- `DELETE /api/v1/memory/agents/{agent_id}/memory`
- `POST /api/v1/memory/agents/{agent_id}/conversation`
- `GET /api/v1/memory/agents/{agent_id}/conversation`
- `DELETE /api/v1/memory/agents/{agent_id}/conversation`

### Health (1 endpoint)
- `GET /api/v1/health`

**Total: 43+ CRUD endpoints**

