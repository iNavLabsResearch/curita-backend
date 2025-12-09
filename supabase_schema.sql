-- =================================================================================
-- TALKING TOY RAG SYSTEM - COMPLETE SCHEMA FOR SUPABASE
-- Deploy all commands in Supabase SQL Editor
-- =================================================================================

-- =================================================================================
-- 1. EXTENSIONS
-- =================================================================================

CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- =================================================================================
-- 2. PROVIDER TABLES
-- =================================================================================

CREATE TABLE IF NOT EXISTS public.model_providers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  provider_name TEXT NOT NULL,
  model_name TEXT NOT NULL,
  api_base_url TEXT,
  api_key_env_var TEXT NOT NULL,
  config_schema JSONB DEFAULT '{}',
  embedding_model_name TEXT,
  embedding_dimension INT DEFAULT 1024,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_model_providers_active ON public.model_providers(is_active);

CREATE TABLE IF NOT EXISTS public.tts_providers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  provider_name TEXT NOT NULL,
  model_name TEXT,
  base_url TEXT NOT NULL,
  api_key_env_var TEXT NOT NULL,
  quality_tier TEXT DEFAULT 'high',
  supports_streaming BOOLEAN DEFAULT TRUE,
  latency_target_ms INT DEFAULT 1000,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tts_providers_active ON public.tts_providers(is_active);

CREATE TABLE IF NOT EXISTS public.transcriber_providers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  provider_name TEXT NOT NULL,
  model_name TEXT NOT NULL,
  api_key_env_var TEXT NOT NULL,
  language_support TEXT[] DEFAULT '{"en"}',
  is_default BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_transcriber_providers_default ON public.transcriber_providers(is_default);

-- =================================================================================
-- 3. AGENT TABLES
-- =================================================================================

CREATE TABLE IF NOT EXISTS public.agents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  transcriber_provider_id UUID REFERENCES public.transcriber_providers(id) ON DELETE SET NULL,
  name TEXT NOT NULL,
  description TEXT,
  system_prompt TEXT NOT NULL,
  first_response TEXT NOT NULL,
  personality_traits JSONB DEFAULT '{}',
  language_code TEXT DEFAULT 'en-US',
  supported_languages TEXT[] DEFAULT '{"en-US"}',
  avatar_url TEXT,
  theme_color TEXT,
  client_state JSONB DEFAULT '{}',
  knowledge_base_id UUID,
  is_active BOOLEAN DEFAULT TRUE,
  is_public BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_agents_user_id ON public.agents(user_id);
CREATE INDEX IF NOT EXISTS idx_agents_active ON public.agents(is_active);

CREATE TABLE IF NOT EXISTS public.agent_model_settings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id UUID NOT NULL UNIQUE REFERENCES public.agents(id) ON DELETE CASCADE,
  model_provider_id UUID NOT NULL REFERENCES public.model_providers(id) ON DELETE RESTRICT,
  temperature FLOAT4 DEFAULT 0.7,
  top_p FLOAT4 DEFAULT 0.9,
  frequency_penalty FLOAT4 DEFAULT 0.5,
  presence_penalty FLOAT4 DEFAULT 0.0,
  max_tokens INT DEFAULT 300,
  max_context_window INT DEFAULT 8000,
  use_knowledge_base BOOLEAN DEFAULT TRUE,
  max_rag_chunks INT DEFAULT 5,
  rag_similarity_threshold FLOAT4 DEFAULT 0.70,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_agent_model_settings_agent_id ON public.agent_model_settings(agent_id);

CREATE TABLE IF NOT EXISTS public.agent_voice_settings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id UUID NOT NULL UNIQUE REFERENCES public.agents(id) ON DELETE CASCADE,
  tts_provider_id UUID NOT NULL REFERENCES public.tts_providers(id) ON DELETE RESTRICT,
  external_voice_id TEXT NOT NULL,
  voice_name TEXT,
  voice_gender TEXT,
  stability FLOAT4 DEFAULT 0.5,
  similarity_boost FLOAT4 DEFAULT 0.75,
  speaking_rate FLOAT4 DEFAULT 1.0,
  add_background_sound BOOLEAN DEFAULT FALSE,
  background_sound_url TEXT,
  background_sound_volume FLOAT4 DEFAULT 0.3,
  enable_filler_words BOOLEAN DEFAULT TRUE,
  filler_word_probability FLOAT4 DEFAULT 0.3,
  enable_interruption BOOLEAN DEFAULT TRUE,
  interrupt_sensitivity FLOAT4 DEFAULT 0.6,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_agent_voice_settings_agent_id ON public.agent_voice_settings(agent_id);

CREATE TABLE IF NOT EXISTS public.agent_tools (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id UUID NOT NULL REFERENCES public.agents(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT NOT NULL,
  tool_type TEXT NOT NULL,
  webhook_url TEXT NOT NULL,
  http_method TEXT DEFAULT 'POST',
  custom_headers JSONB DEFAULT '{}',
  parameters_schema JSONB NOT NULL,
  required_parameters TEXT[],
  expected_response_schema JSONB,
  response_timeout_ms INT DEFAULT 5000,
  is_enabled BOOLEAN DEFAULT TRUE,
  allow_auto_invoke BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_agent_tools_agent_id ON public.agent_tools(agent_id);

-- =================================================================================
-- 4. RAG SYSTEM TABLES
-- =================================================================================

CREATE TABLE IF NOT EXISTS public.knowledge_bases (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id UUID NOT NULL REFERENCES public.agents(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  chunk_size INT DEFAULT 500,
  chunk_overlap INT DEFAULT 100,
  chunking_strategy TEXT DEFAULT 'recursive',
  embedding_model_name TEXT NOT NULL,
  embedding_dimension INT DEFAULT 1024,
  total_chunks INT DEFAULT 0,
  total_tokens_stored INT DEFAULT 0,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_knowledge_bases_agent_id ON public.knowledge_bases(agent_id);

CREATE TABLE IF NOT EXISTS public.kb_files (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  knowledge_base_id UUID NOT NULL REFERENCES public.knowledge_bases(id) ON DELETE CASCADE,
  original_filename TEXT NOT NULL,
  file_type TEXT NOT NULL,
  file_size_bytes BIGINT,
  storage_path TEXT NOT NULL,
  processing_status TEXT DEFAULT 'pending' CHECK (processing_status IN ('pending', 'processing', 'completed', 'failed')),
  error_message TEXT,
  pages_extracted INT,
  chunks_created INT DEFAULT 0,
  extraction_model TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_kb_files_kb_id ON public.kb_files(knowledge_base_id);
CREATE INDEX IF NOT EXISTS idx_kb_files_status ON public.kb_files(processing_status);

CREATE TABLE IF NOT EXISTS public.kb_chunks (
  id BIGSERIAL PRIMARY KEY,
  knowledge_base_id UUID NOT NULL REFERENCES public.knowledge_bases(id) ON DELETE CASCADE,
  file_id UUID REFERENCES public.kb_files(id) ON DELETE CASCADE,
  chunk_text TEXT NOT NULL,
  chunk_index INT NOT NULL,
  metadata JSONB NOT NULL DEFAULT '{}',
  embedding vector(1024) NOT NULL,
  token_count INT,
  confidence_score FLOAT4,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_kb_chunks_embedding ON public.kb_chunks
USING hnsw (embedding vector_cosine_ops)
WITH (m = 24, ef_construction = 128);

CREATE INDEX IF NOT EXISTS idx_kb_chunks_kb_id ON public.kb_chunks(knowledge_base_id);
CREATE INDEX IF NOT EXISTS idx_kb_chunks_file_id ON public.kb_chunks(file_id);

CREATE TABLE IF NOT EXISTS public.agent_conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id UUID NOT NULL REFERENCES public.agents(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  session_id TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_conversations_agent_user ON public.agent_conversations(agent_id, user_id);
CREATE INDEX IF NOT EXISTS idx_conversations_session_id ON public.agent_conversations(session_id);

CREATE TABLE IF NOT EXISTS public.conversation_messages (
  id BIGSERIAL PRIMARY KEY,
  conversation_id UUID NOT NULL REFERENCES public.agent_conversations(id) ON DELETE CASCADE,
  role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
  content TEXT NOT NULL,
  used_knowledge_base BOOLEAN DEFAULT FALSE,
  referenced_chunk_ids BIGINT[] DEFAULT '{}',
  latency_ms INT,
  tokens_used INT,
  model_used TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON public.conversation_messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON public.conversation_messages(created_at);

-- =================================================================================
-- 5. OBSERVABILITY TABLE
-- =================================================================================

CREATE TABLE IF NOT EXISTS public.embedding_jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  knowledge_base_id UUID NOT NULL REFERENCES public.knowledge_bases(id) ON DELETE CASCADE,
  file_id UUID REFERENCES public.kb_files(id) ON DELETE SET NULL,
  job_status TEXT DEFAULT 'pending' CHECK (job_status IN ('pending', 'running', 'completed', 'failed')),
  chunks_processed INT DEFAULT 0,
  chunks_total INT,
  error_details JSONB,
  duration_seconds INT,
  started_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_embedding_jobs_kb_id ON public.embedding_jobs(knowledge_base_id);
CREATE INDEX IF NOT EXISTS idx_embedding_jobs_status ON public.embedding_jobs(job_status);

-- =================================================================================
-- 6. ROW-LEVEL SECURITY (RLS)
-- =================================================================================

ALTER TABLE public.agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agent_model_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agent_voice_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agent_tools ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.knowledge_bases ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.kb_files ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.kb_chunks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agent_conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.conversation_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.embedding_jobs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage their own agents" ON public.agents
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Agent model settings access" ON public.agent_model_settings
  USING (
      EXISTS (
          SELECT 1 FROM public.agents
          WHERE agents.id = agent_model_settings.agent_id
          AND agents.user_id = auth.uid()
      )
  );

CREATE POLICY "Agent voice settings access" ON public.agent_voice_settings
  USING (
      EXISTS (
          SELECT 1 FROM public.agents
          WHERE agents.id = agent_voice_settings.agent_id
          AND agents.user_id = auth.uid()
      )
  );

CREATE POLICY "Agent tools access" ON public.agent_tools
  USING (
      EXISTS (
          SELECT 1 FROM public.agents
          WHERE agents.id = agent_tools.agent_id
          AND agents.user_id = auth.uid()
      )
  );

CREATE POLICY "Knowledge base access" ON public.knowledge_bases
  USING (
      EXISTS (
          SELECT 1 FROM public.agents
          WHERE agents.id = knowledge_bases.agent_id
          AND agents.user_id = auth.uid()
      )
  );

CREATE POLICY "KB files access" ON public.kb_files
  USING (
      EXISTS (
          SELECT 1 FROM public.knowledge_bases kb
          WHERE kb.id = kb_files.knowledge_base_id
          AND EXISTS (
              SELECT 1 FROM public.agents a
              WHERE a.id = kb.agent_id
              AND a.user_id = auth.uid()
          )
      )
  );

CREATE POLICY "KB chunks access" ON public.kb_chunks
  USING (
      EXISTS (
          SELECT 1 FROM public.knowledge_bases kb
          WHERE kb.id = kb_chunks.knowledge_base_id
          AND EXISTS (
              SELECT 1 FROM public.agents a
              WHERE a.id = kb.agent_id
              AND a.user_id = auth.uid()
          )
      )
  );

CREATE POLICY "User conversations" ON public.agent_conversations
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Conversation messages access" ON public.conversation_messages
  USING (
      EXISTS (
          SELECT 1 FROM public.agent_conversations ac
          WHERE ac.id = conversation_messages.conversation_id
          AND ac.user_id = auth.uid()
      )
  );

CREATE POLICY "Embedding jobs access" ON public.embedding_jobs
  USING (
      EXISTS (
          SELECT 1 FROM public.knowledge_bases kb
          WHERE kb.id = embedding_jobs.knowledge_base_id
          AND EXISTS (
              SELECT 1 FROM public.agents a
              WHERE a.id = kb.agent_id
              AND a.user_id = auth.uid()
          )
      )
  );

-- =================================================================================
-- 7. RPC FUNCTIONS
-- =================================================================================

CREATE OR REPLACE FUNCTION public.search_knowledge_base(
  p_query_embedding vector(1024),
  p_knowledge_base_id UUID,
  p_match_threshold FLOAT4 DEFAULT 0.70,
  p_match_count INT DEFAULT 5
)
RETURNS TABLE (
  chunk_id BIGINT,
  chunk_text TEXT,
  similarity FLOAT4,
  metadata JSONB,
  file_name TEXT,
  page_number INT
)
LANGUAGE plpgsql
STABLE
AS $$
BEGIN
  RETURN QUERY
  SELECT
      kc.id,
      kc.chunk_text,
      (1 - (kc.embedding <=> p_query_embedding))::FLOAT4 AS similarity,
      kc.metadata,
      (kc.metadata->>'file_name')::TEXT,
      (kc.metadata->>'page_number')::INT
  FROM public.kb_chunks kc
  WHERE
      kc.knowledge_base_id = p_knowledge_base_id
      AND (1 - (kc.embedding <=> p_query_embedding)) > p_match_threshold
  ORDER BY kc.embedding <=> p_query_embedding ASC
  LIMIT p_match_count;
END;
$$;

CREATE OR REPLACE FUNCTION public.search_knowledge_base_filtered(
  p_query_embedding vector(1024),
  p_knowledge_base_id UUID,
  p_file_names TEXT[] DEFAULT NULL,
  p_match_threshold FLOAT4 DEFAULT 0.70,
  p_match_count INT DEFAULT 5
)
RETURNS TABLE (
  chunk_id BIGINT,
  chunk_text TEXT,
  similarity FLOAT4,
  metadata JSONB,
  file_name TEXT,
  page_number INT
)
LANGUAGE plpgsql
STABLE
AS $$
BEGIN
  RETURN QUERY
  SELECT
      kc.id,
      kc.chunk_text,
      (1 - (kc.embedding <=> p_query_embedding))::FLOAT4 AS similarity,
      kc.metadata,
      (kc.metadata->>'file_name')::TEXT,
      (kc.metadata->>'page_number')::INT
  FROM public.kb_chunks kc
  WHERE
      kc.knowledge_base_id = p_knowledge_base_id
      AND (1 - (kc.embedding <=> p_query_embedding)) > p_match_threshold
      AND (
          p_file_names IS NULL 
          OR (kc.metadata->>'file_name')::TEXT = ANY(p_file_names)
      )
  ORDER BY kc.embedding <=> p_query_embedding ASC
  LIMIT p_match_count;
END;
$$;

CREATE OR REPLACE FUNCTION public.search_by_agent(
  p_agent_id UUID,
  p_query_embedding vector(1024),
  p_match_threshold FLOAT4 DEFAULT 0.70,
  p_match_count INT DEFAULT 5
)
RETURNS TABLE (
  chunk_id BIGINT,
  chunk_text TEXT,
  similarity FLOAT4,
  metadata JSONB,
  file_name TEXT,
  page_number INT
)
LANGUAGE plpgsql
STABLE
AS $$
DECLARE
  v_kb_id UUID;
BEGIN
  SELECT agents.knowledge_base_id INTO v_kb_id
  FROM public.agents
  WHERE id = p_agent_id;
  
  IF v_kb_id IS NULL THEN
      RETURN;
  END IF;
  
  RETURN QUERY
  SELECT
      kc.id,
      kc.chunk_text,
      (1 - (kc.embedding <=> p_query_embedding))::FLOAT4 AS similarity,
      kc.metadata,
      (kc.metadata->>'file_name')::TEXT,
      (kc.metadata->>'page_number')::INT
  FROM public.kb_chunks kc
  WHERE
      kc.knowledge_base_id = v_kb_id
      AND (1 - (kc.embedding <=> p_query_embedding)) > p_match_threshold
  ORDER BY kc.embedding <=> p_query_embedding ASC
  LIMIT p_match_count;
END;
$$;

-- =================================================================================
-- 8. HELPER FUNCTIONS & TRIGGERS
-- =================================================================================

CREATE OR REPLACE FUNCTION public.update_agents_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_agents_updated_at ON public.agents;
CREATE TRIGGER update_agents_updated_at
BEFORE UPDATE ON public.agents
FOR EACH ROW
EXECUTE FUNCTION update_agents_timestamp();

CREATE OR REPLACE FUNCTION public.get_agent_stats(p_agent_id UUID)
RETURNS TABLE (
  total_conversations BIGINT,
  total_messages BIGINT,
  knowledge_base_chunks BIGINT,
  avg_latency_ms NUMERIC
)
LANGUAGE plpgsql
STABLE
AS $$
BEGIN
  RETURN QUERY
  SELECT
      COUNT(DISTINCT ac.id)::BIGINT as total_conversations,
      COUNT(cm.id)::BIGINT as total_messages,
      COUNT(kc.id)::BIGINT as knowledge_base_chunks,
      AVG(cm.latency_ms)::NUMERIC as avg_latency_ms
  FROM (SELECT 1) t
  LEFT JOIN public.agent_conversations ac ON ac.agent_id = p_agent_id
  LEFT JOIN public.conversation_messages cm ON cm.conversation_id = ac.id
  LEFT JOIN public.kb_chunks kc ON kc.knowledge_base_id = (
      SELECT knowledge_base_id FROM public.agents WHERE id = p_agent_id
  );
END;
$$;

-- =================================================================================
-- DEPLOYMENT COMPLETE
-- =================================================================================
