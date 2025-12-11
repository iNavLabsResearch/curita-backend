-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.agent_memory (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  toy_id uuid NOT NULL,
  agent_id uuid NOT NULL,
  original_filename text,
  storage_file_id text,
  file_size bigint,
  content_type text,
  chunk_text text,
  chunk_index integer,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  embedding_vector USER-DEFINED,
  CONSTRAINT agent_memory_pkey PRIMARY KEY (id),
  CONSTRAINT agent_memory_toy_id_fkey FOREIGN KEY (toy_id) REFERENCES public.toys(id),
  CONSTRAINT agent_memory_agent_id_fkey FOREIGN KEY (agent_id) REFERENCES public.agents(id)
);
CREATE TABLE public.agent_tools (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  toy_id uuid NOT NULL,
  name text NOT NULL,
  url text NOT NULL,
  headers_schema jsonb DEFAULT '{}'::jsonb,
  payload_schema jsonb,
  tool_schema jsonb NOT NULL,
  http_method text DEFAULT 'POST'::text,
  provider_name text,
  output_schema jsonb,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT agent_tools_pkey PRIMARY KEY (id),
  CONSTRAINT agent_tools_toy_id_fkey FOREIGN KEY (toy_id) REFERENCES public.toys(id)
);
CREATE TABLE public.agents (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  toy_id uuid NOT NULL,
  name text NOT NULL,
  system_prompt text NOT NULL,
  model_provider_id uuid,
  tts_provider_id uuid,
  transcriber_provider_id uuid,
  voice_id text,
  language_code text DEFAULT 'en-US'::text,
  is_active boolean DEFAULT true,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT agents_pkey PRIMARY KEY (id),
  CONSTRAINT agents_toy_id_fkey FOREIGN KEY (toy_id) REFERENCES public.toys(id),
  CONSTRAINT agents_model_provider_id_fkey FOREIGN KEY (model_provider_id) REFERENCES public.model_providers(id),
  CONSTRAINT agents_tts_provider_id_fkey FOREIGN KEY (tts_provider_id) REFERENCES public.tts_providers(id),
  CONSTRAINT agents_transcriber_provider_id_fkey FOREIGN KEY (transcriber_provider_id) REFERENCES public.transcriber_providers(id)
);
CREATE TABLE public.conversation_logs (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  agent_id uuid NOT NULL,
  role text NOT NULL CHECK (role = ANY (ARRAY['user'::text, 'assistant'::text, 'system'::text, 'tool'::text])),
  content text,
  created_at timestamp with time zone DEFAULT now(),
  CONSTRAINT conversation_logs_pkey PRIMARY KEY (id),
  CONSTRAINT conversation_logs_agent_id_fkey FOREIGN KEY (agent_id) REFERENCES public.agents(id)
);
CREATE TABLE public.message_citations (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  log_id uuid NOT NULL,
  toy_memory_id uuid,
  agent_memory_id uuid,
  similarity_score real,
  created_at timestamp with time zone DEFAULT now(),
  CONSTRAINT message_citations_pkey PRIMARY KEY (id),
  CONSTRAINT message_citations_log_id_fkey FOREIGN KEY (log_id) REFERENCES public.conversation_logs(id),
  CONSTRAINT message_citations_toy_memory_id_fkey FOREIGN KEY (toy_memory_id) REFERENCES public.toy_memory(id),
  CONSTRAINT message_citations_agent_memory_id_fkey FOREIGN KEY (agent_memory_id) REFERENCES public.agent_memory(id)
);
CREATE TABLE public.model_providers (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  provider_name text NOT NULL,
  model_name text NOT NULL,
  is_large_model boolean DEFAULT false,
  default_temperature real DEFAULT 0.7,
  supported_languages jsonb DEFAULT '["en"]'::jsonb,
  api_key_template text,
  api_base text,
  api_key text,
  is_default boolean DEFAULT false,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT model_providers_pkey PRIMARY KEY (id)
);
CREATE TABLE public.toy_memory (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  toy_id uuid NOT NULL,
  content_type text,
  chunk_text text,
  chunk_index integer,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  embedding_vector USER-DEFINED,
  CONSTRAINT toy_memory_pkey PRIMARY KEY (id),
  CONSTRAINT toy_memory_toy_id_fkey FOREIGN KEY (toy_id) REFERENCES public.toys(id)
);
CREATE TABLE public.toys (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  name text NOT NULL,
  description text,
  avatar_url text,
  user_custom_instruction text,
  is_active boolean DEFAULT true,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT toys_pkey PRIMARY KEY (id)
);
CREATE TABLE public.transcriber_providers (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  name text,
  provider_name text NOT NULL,
  model_name text NOT NULL,
  supported_languages jsonb DEFAULT '["en"]'::jsonb,
  requires_api_key boolean DEFAULT true,
  default_endpoint text,
  api_key_template text,
  model_size text,
  is_default boolean DEFAULT false,
  api_key text,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT transcriber_providers_pkey PRIMARY KEY (id)
);
CREATE TABLE public.tts_providers (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  provider_name text NOT NULL,
  model_name text NOT NULL,
  supported_languages jsonb DEFAULT '["en"]'::jsonb,
  requires_api_key boolean DEFAULT true,
  default_endpoint text,
  api_key_template text,
  api_key text,
  is_default boolean DEFAULT false,
  default_voice text,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT tts_providers_pkey PRIMARY KEY (id)
);