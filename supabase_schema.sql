-- =================================================================================
-- TALKING TOY RAG SYSTEM
-- =================================================================================

-- 1. EXTENSIONS
-- =================================================================================
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- =================================================================================
-- 2. PROVIDER TABLES
-- =================================================================================

-- 2.1 Model Providers
CREATE TABLE IF NOT EXISTS public.model_providers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_name TEXT NOT NULL,
    model_name TEXT NOT NULL,
    is_large_model BOOLEAN DEFAULT FALSE,
    default_temperature FLOAT4 DEFAULT 0.7,
    supported_languages JSONB DEFAULT '["en"]',
    api_key_template TEXT,
    api_base TEXT,
    api_key TEXT,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2.2 TTS Providers
CREATE TABLE IF NOT EXISTS public.tts_providers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_name TEXT NOT NULL,
    model_name TEXT NOT NULL,
    supported_languages JSONB DEFAULT '["en"]',
    requires_api_key BOOLEAN DEFAULT TRUE,
    default_endpoint TEXT,
    api_key_template TEXT,
    api_key TEXT,
    is_default BOOLEAN DEFAULT FALSE,
    default_voice TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2.3 Transcriber Providers
CREATE TABLE IF NOT EXISTS public.transcriber_providers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT,
    provider_name TEXT NOT NULL,
    model_name TEXT NOT NULL,
    supported_languages JSONB DEFAULT '["en"]',
    requires_api_key BOOLEAN DEFAULT TRUE,
    default_endpoint TEXT,
    api_key_template TEXT,
    model_size TEXT,
    is_default BOOLEAN DEFAULT FALSE,
    api_key TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- =================================================================================
-- 3. THE TOY (Root Entity)
-- =================================================================================

CREATE TABLE IF NOT EXISTS public.toys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    description TEXT,
    avatar_url TEXT,
    user_custom_instruction TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- =================================================================================
-- 4. AGENTS & TOOLS
-- =================================================================================

CREATE TABLE IF NOT EXISTS public.agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    toy_id UUID NOT NULL REFERENCES public.toys(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    system_prompt TEXT NOT NULL,
    
    -- Provider Links
    model_provider_id UUID REFERENCES public.model_providers(id),
    tts_provider_id UUID REFERENCES public.tts_providers(id),
    transcriber_provider_id UUID REFERENCES public.transcriber_providers(id),
    
    voice_id TEXT,
    language_code TEXT DEFAULT 'en-US',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.agent_tools (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    toy_id UUID NOT NULL REFERENCES public.toys(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    headers_schema JSONB DEFAULT '{}',
    payload_schema JSONB,
    tool_schema JSONB NOT NULL,
    http_method TEXT DEFAULT 'POST',
    provider_name TEXT,
    output_schema JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- =================================================================================
-- 5. MEMORY TABLES
-- =================================================================================

-- 5.1 Toy Memory (Interaction Context)
CREATE TABLE IF NOT EXISTS public.toy_memory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    toy_id UUID NOT NULL REFERENCES public.toys(id) ON DELETE CASCADE,
    content_type TEXT,
    chunk_text TEXT, -- The text content for context
    embedding_vector vector(768),
    chunk_index INT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for vector search
CREATE INDEX IF NOT EXISTS idx_toy_memory_embedding ON public.toy_memory
USING hnsw (embedding_vector vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- 5.2 Agent Memory (Knowledge Base)
CREATE TABLE IF NOT EXISTS public.agent_memory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    toy_id UUID NOT NULL REFERENCES public.toys(id) ON DELETE CASCADE,
    agent_id UUID NOT NULL REFERENCES public.agents(id) ON DELETE CASCADE,
    original_filename TEXT,
    storage_file_id TEXT,
    file_size BIGINT,
    content_type TEXT,
    chunk_text TEXT, -- The text content for context
    embedding_vector vector(768),
    chunk_index INT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for vector search
CREATE INDEX IF NOT EXISTS idx_agent_memory_embedding ON public.agent_memory
USING hnsw (embedding_vector vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- =================================================================================
-- 6. CONVERSATION LOGS
-- =================================================================================

CREATE TABLE IF NOT EXISTS public.conversation_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES public.agents(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system', 'tool')),
    content TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- =================================================================================
-- 7. MESSAGE CITATIONS (The Context Bridge)
-- =================================================================================

CREATE TABLE IF NOT EXISTS public.message_citations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    log_id UUID NOT NULL REFERENCES public.conversation_logs(id) ON DELETE CASCADE,
    toy_memory_id UUID REFERENCES public.toy_memory(id) ON DELETE SET NULL,
    agent_memory_id UUID REFERENCES public.agent_memory(id) ON DELETE SET NULL,
    similarity_score FLOAT4,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- =================================================================================
-- 8. ROW LEVEL SECURITY (RLS)
-- =================================================================================

-- Enable RLS on all tables
ALTER TABLE public.toys ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agent_tools ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.toy_memory ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agent_memory ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.conversation_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.message_citations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.model_providers ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.tts_providers ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.transcriber_providers ENABLE ROW LEVEL SECURITY;

-- Provider Policies (Public Read)
CREATE POLICY "Public read model providers" ON public.model_providers FOR SELECT USING (true);
CREATE POLICY "Public read tts providers" ON public.tts_providers FOR SELECT USING (true);
CREATE POLICY "Public read transcriber providers" ON public.transcriber_providers FOR SELECT USING (true);

-- NOTE: Since `user_id` was removed from the `toys` table in your diagram,
-- strict ownership RLS cannot be applied. Below is a placeholder policy that
-- allows access. You will need to add `user_id` back to `toys` if you want
-- private user data.

CREATE POLICY "Allow all access for now" ON public.toys USING (true) WITH CHECK (true);
CREATE POLICY "Allow all access agents" ON public.agents USING (true) WITH CHECK (true);
CREATE POLICY "Allow all access tools" ON public.agent_tools USING (true) WITH CHECK (true);
CREATE POLICY "Allow all access toy_memory" ON public.toy_memory USING (true) WITH CHECK (true);
CREATE POLICY "Allow all access agent_memory" ON public.agent_memory USING (true) WITH CHECK (true);
CREATE POLICY "Allow all access logs" ON public.conversation_logs USING (true) WITH CHECK (true);
CREATE POLICY "Allow all access citations" ON public.message_citations USING (true) WITH CHECK (true);