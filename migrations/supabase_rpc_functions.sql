-- =================================================================================
-- SUPABASE RPC FUNCTIONS FOR VECTOR SEARCH (384-dimensional vectors)
-- Updated for Snowflake Arctic Embed XS
-- =================================================================================

-- =================================================================================
-- 1. TOY MEMORY VECTOR SEARCH
-- =================================================================================

-- Drop existing function if it exists (for clean updates)
DROP FUNCTION IF EXISTS match_toy_memory;

CREATE OR REPLACE FUNCTION match_toy_memory(
    query_embedding vector(384),
    match_count int DEFAULT 5,
    filter_toy_id uuid DEFAULT NULL,
    similarity_threshold float DEFAULT 0.0,
    match_offset int DEFAULT 0
)
RETURNS TABLE (
    id uuid,
    toy_id uuid,
    content_type text,
    chunk_text text,
    chunk_index int,
    similarity float,
    created_at timestamptz
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        tm.id,
        tm.toy_id,
        tm.content_type,
        tm.chunk_text,
        tm.chunk_index,
        1 - (tm.embedding_vector <=> query_embedding) AS similarity,
        tm.created_at
    FROM public.toy_memory tm
    WHERE 
        (filter_toy_id IS NULL OR tm.toy_id = filter_toy_id)
        AND tm.embedding_vector IS NOT NULL
        AND (1 - (tm.embedding_vector <=> query_embedding)) >= similarity_threshold
    ORDER BY tm.embedding_vector <=> query_embedding
    LIMIT match_count
    OFFSET match_offset;
END;
$$;

-- Add comment
COMMENT ON FUNCTION match_toy_memory IS 'Vector similarity search in toy_memory using 384-dim embeddings (cosine distance) with pagination';


-- =================================================================================
-- 2. AGENT MEMORY VECTOR SEARCH
-- =================================================================================

-- Drop existing function if it exists
DROP FUNCTION IF EXISTS match_agent_memory;

CREATE OR REPLACE FUNCTION match_agent_memory(
    query_embedding vector(384),
    match_count int DEFAULT 5,
    filter_agent_id uuid DEFAULT NULL,
    filter_toy_id uuid DEFAULT NULL,
    similarity_threshold float DEFAULT 0.0,
    match_offset int DEFAULT 0
)
RETURNS TABLE (
    id uuid,
    toy_id uuid,
    agent_id uuid,
    original_filename text,
    storage_file_id text,
    content_type text,
    chunk_text text,
    chunk_index int,
    similarity float,
    created_at timestamptz
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        am.id,
        am.toy_id,
        am.agent_id,
        am.original_filename,
        am.storage_file_id,
        am.content_type,
        am.chunk_text,
        am.chunk_index,
        1 - (am.embedding_vector <=> query_embedding) AS similarity,
        am.created_at
    FROM public.agent_memory am
    WHERE 
        (filter_agent_id IS NULL OR am.agent_id = filter_agent_id)
        AND (filter_toy_id IS NULL OR am.toy_id = filter_toy_id)
        AND am.embedding_vector IS NOT NULL
        AND (1 - (am.embedding_vector <=> query_embedding)) >= similarity_threshold
    ORDER BY am.embedding_vector <=> query_embedding
    LIMIT match_count
    OFFSET match_offset;
END;
$$;

-- Add comment
COMMENT ON FUNCTION match_agent_memory IS 'Vector similarity search in agent_memory using 384-dim embeddings (cosine distance) with pagination';


-- =================================================================================
-- 3. UNIFIED MEMORY SEARCH (Both Toy and Agent Memory)
-- =================================================================================

-- Drop existing function if it exists
DROP FUNCTION IF EXISTS match_all_memory;

CREATE OR REPLACE FUNCTION match_all_memory(
    query_embedding vector(384),
    match_count int DEFAULT 5,
    filter_toy_id uuid DEFAULT NULL,
    filter_agent_id uuid DEFAULT NULL,
    similarity_threshold float DEFAULT 0.0,
    match_offset int DEFAULT 0
)
RETURNS TABLE (
    id uuid,
    memory_type text,
    toy_id uuid,
    agent_id uuid,
    chunk_text text,
    chunk_index int,
    similarity float,
    metadata jsonb,
    created_at timestamptz
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    (
        -- Toy Memory Results
        SELECT
            tm.id,
            'toy'::text AS memory_type,
            tm.toy_id,
            NULL::uuid AS agent_id,
            tm.chunk_text,
            tm.chunk_index,
            1 - (tm.embedding_vector <=> query_embedding) AS similarity,
            jsonb_build_object(
                'content_type', tm.content_type
            ) AS metadata,
            tm.created_at
        FROM public.toy_memory tm
        WHERE 
            (filter_toy_id IS NULL OR tm.toy_id = filter_toy_id)
            AND tm.embedding_vector IS NOT NULL
            AND (1 - (tm.embedding_vector <=> query_embedding)) >= similarity_threshold
        
        UNION ALL
        
        -- Agent Memory Results
        SELECT
            am.id,
            'agent'::text AS memory_type,
            am.toy_id,
            am.agent_id,
            am.chunk_text,
            am.chunk_index,
            1 - (am.embedding_vector <=> query_embedding) AS similarity,
            jsonb_build_object(
                'content_type', am.content_type,
                'original_filename', am.original_filename,
                'storage_file_id', am.storage_file_id
            ) AS metadata,
            am.created_at
        FROM public.agent_memory am
        WHERE 
            (filter_toy_id IS NULL OR am.toy_id = filter_toy_id)
            AND (filter_agent_id IS NULL OR am.agent_id = filter_agent_id)
            AND am.embedding_vector IS NOT NULL
            AND (1 - (am.embedding_vector <=> query_embedding)) >= similarity_threshold
    )
    ORDER BY similarity DESC
    LIMIT match_count
    OFFSET match_offset;
END;
$$;

-- Add comment
COMMENT ON FUNCTION match_all_memory IS 'Unified vector search across toy_memory and agent_memory using 384-dim embeddings with pagination';


-- =================================================================================
-- 4. CONVERSATION CONTEXT SEARCH
-- =================================================================================

-- Drop existing function if it exists
DROP FUNCTION IF EXISTS search_conversation_context;

CREATE OR REPLACE FUNCTION search_conversation_context(
    query_embedding vector(384),
    p_agent_id uuid,
    match_count int DEFAULT 5,
    similarity_threshold float DEFAULT 0.0
)
RETURNS TABLE (
    memory_id uuid,
    memory_type text,
    chunk_text text,
    similarity float,
    conversation_log_id uuid,
    conversation_role text,
    conversation_content text,
    conversation_created_at timestamptz
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        tm.id AS memory_id,
        'toy'::text AS memory_type,
        tm.chunk_text,
        1 - (tm.embedding_vector <=> query_embedding) AS similarity,
        cl.id AS conversation_log_id,
        cl.role AS conversation_role,
        cl.content AS conversation_content,
        cl.created_at AS conversation_created_at
    FROM public.toy_memory tm
    INNER JOIN public.toys t ON tm.toy_id = t.id
    INNER JOIN public.agents a ON t.id = a.toy_id
    LEFT JOIN public.conversation_logs cl ON a.id = cl.agent_id
    WHERE 
        a.id = p_agent_id
        AND tm.embedding_vector IS NOT NULL
        AND (1 - (tm.embedding_vector <=> query_embedding)) >= similarity_threshold
    ORDER BY tm.embedding_vector <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Add comment
COMMENT ON FUNCTION search_conversation_context IS 'Search toy memory with conversation context for a specific agent';


-- =================================================================================
-- USAGE EXAMPLES
-- =================================================================================

-- Example 1: Search toy memory
-- SELECT * FROM match_toy_memory(
--     query_embedding := '[0.1, 0.2, ..., 0.384]'::vector(384),
--     match_count := 10,
--     filter_toy_id := 'uuid-here',
--     similarity_threshold := 0.7
-- );

-- Example 2: Search agent memory
-- SELECT * FROM match_agent_memory(
--     query_embedding := '[0.1, 0.2, ..., 0.384]'::vector(384),
--     match_count := 10,
--     filter_agent_id := 'uuid-here',
--     similarity_threshold := 0.7
-- );

-- Example 3: Unified search across all memory
-- SELECT * FROM match_all_memory(
--     query_embedding := '[0.1, 0.2, ..., 0.384]'::vector(384),
--     match_count := 10,
--     filter_toy_id := 'uuid-here',
--     similarity_threshold := 0.7
-- );

-- Example 4: Search with conversation context
-- SELECT * FROM search_conversation_context(
--     query_embedding := '[0.1, 0.2, ..., 0.384]'::vector(384),
--     p_agent_id := 'uuid-here',
--     match_count := 10,
--     similarity_threshold := 0.7
-- );
