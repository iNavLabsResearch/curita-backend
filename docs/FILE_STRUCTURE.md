# Codebase File Structure Documentation

## Overview

This is a comprehensive documentation of the Pranthora Backend codebase structure - a voice agent and AI conversation platform with support for real-time speech processing, agent workflows, and multi-provider integrations.

---

## Root Directory

### Configuration Files

- **`agent_workflows_demo.json`** - Demo configuration for agent workflows
- **`agent_workflows.json`** - Production agent workflow configurations
- **`api_specification.yaml`** - OpenAPI/Swagger specification for REST APIs
- **`config.json`** - Main application configuration file
- **`voice_agents_config_demo.json`** - Demo voice agent configurations
- **`voice_agents_config.json`** - Production voice agent configurations
- **`exception_tts_prompts.json`** - Text-to-speech prompts for exception handling
- **`filler_tts_prompts.json`** - Filler TTS prompts for natural conversation flow
- **`diya_tution_prompt.md`** - Specific prompt template for Diya tuition use case

### Docker & Deployment

- **`docker-compose.yml`** - Development Docker Compose configuration
- **`docker-compose-prod.yml`** - Production Docker Compose configuration
- **`docker-compose-prod-lamda.yml`** - Lambda-specific production configuration
- **`Dockerfile`** - Main Docker image definition
- **`Dockerfile_v0`** - Legacy/alternative Dockerfile version

### Monitoring & Logging

- **`loki-config.yaml`** - Loki logging system configuration
- **`prometheus.yml`** - Prometheus metrics collection configuration

### Project Files

- **`main.py`** - Application entry point
- **`requirements.txt`** - Python package dependencies
- **`pytest.ini`** - Pytest configuration for testing
- **`README.md`** - Project documentation
- **`prod_deployment_files_copy.ps1`** - PowerShell script for deployment file copying

---

## `/app/` - Main Application Directory

### Core Files

- **`__init__.py`** - App module initialization
- **`static_memory_cache.py`** - In-memory caching implementation

---

## `/app/agents_management/` - Agent Management System

Core agent orchestration and management functionality.

### Root Files

- **`__init__.py`** - Module initialization
- **`voice_agent.py`** - Voice agent core implementation
- **`voice_agents_manager.py`** - Manager for multiple voice agents

### `/agent_utility/` - Agent Utilities

Helper utilities for agent operations:

- **`agent_precache_helper.py`** - Pre-caching optimization for agents
- **`agent_properties.py`** - Agent property definitions and handlers
- **`document_cache_loader.py`** - Document caching for RAG
- **`mcp_tool_converter.py`** - Model Context Protocol tool conversion

### `/agents/` - Base Agent Classes

Core agent abstractions:

- **`agent.py`** - Main agent implementation
- **`base_agent.py`** - Abstract base agent class

### `/agents_workflows/` - Workflow Management

Agent workflow orchestration:

- **`__init__.py`** - Module initialization
- **`agent_node.py`** - Individual workflow node implementation
- **`agent_workflow_graph.py`** - Workflow graph structure and execution

### `/domain_models/` - Agent Domain Models

Agent-specific domain models:

- **`agent_metadata.py`** - Agent metadata structures
- **`weaviate_configuration.py`** - Weaviate vector DB configuration for agents

### `/history_management/` - Conversation History

Conversation persistence and retrieval:

- **`__init__.py`** - Module initialization
- **`conversation_history.py`** - Conversation history management

### `/rag_database/` - RAG & Vector Database

Retrieval Augmented Generation infrastructure:

- **`embeddings_abstract.py`** - Abstract embedding interface
- **`embeddings_sentenceformer.py`** - Sentence Transformer embeddings implementation
- **`rag_client.py`** - RAG client for document retrieval
- **`vector_database.py`** - Vector database abstraction
- **`weaviate_adapter.py`** - Weaviate-specific adapter

### `/tools/` - Agent Tools & Integrations

External tool integration system:

- **`__init__.py`** - Module initialization
- **`global_http_tools.py`** - Global HTTP tool definitions
- **`http_tool_executor.py`** - HTTP tool execution handler
- **`mcp_client_manager.py`** - Model Context Protocol client management
- **`mcp_tool_executor.py`** - MCP tool execution
- **`nango_action_executor.py`** - Nango integration action executor
- **`tool_execution_manager.py`** - Central tool execution management
- **`tool_executor.py`** - Base tool executor
- **`tool_registry.py`** - Tool registration and discovery
- **`tool_schema_generator.py`** - Dynamic tool schema generation
- **`ultravox_tool_converter.py`** - Ultravox-specific tool converter

### `/voice_agents/` - Voice Agent Implementations

Voice-specific agent implementations:

- **`__init__.py`** - Module initialization

### `/voice_agents_graph/` - Voice Agent Graphs

Voice agent workflow graphs:

- **`__init__.py`** - Module initialization

#### `/agent_graphs_functions/` - Graph Functions

Pre-built agent graph functions:

- **`office_agent_graphs_tools.py`** - Office/business agent graphs
- **`realestate_agent_graphs_tools.py`** - Real estate agent graphs

---

## `/app/api/` - API Layer

### `/v1/` - API Version 1

REST API endpoints:

- **`__init__.py`** - API module initialization
- **`agent_files_mapping_routes.py`** - Agent-file mapping endpoints
- **`agent_routes.py`** - Agent CRUD endpoints
- **`api_key_controller.py`** - API key management
- **`batch_calling_routes.py`** - Batch calling operations
- **`call_analytics_controller.py`** - Call analytics and metrics
- **`chromadb_search_routes.py`** - ChromaDB search endpoints
- **`composio_routes.py`** - Composio integration endpoints
- **`dashboard_controller.py`** - Dashboard data endpoints
- **`file_upload_routes.py`** - File upload handling
- **`incoming_call_controller.py`** - Incoming call webhook handler
- **`incoming_text_controller.py`** - Incoming text message handler
- **`n8n_workflow_controller.py`** - N8N workflow integration
- **`nango_integration_controller.py`** - Nango integration management
- **`phone_management_routes.py`** - Phone number management
- **`provider_routes.py`** - Provider configuration endpoints
- **`s2s_provider_incoming_call.py`** - Speech-to-speech provider webhooks
- **`schemas.py`** - Pydantic API schemas
- **`supabase_middleware.py`** - Supabase authentication middleware
- **`tool_endpoint_def_routes.py`** - Tool endpoint definitions
- **`tools_mcp_server_def_routes.py`** - MCP server definition endpoints
- **`ultravox_config_controller.py`** - Ultravox configuration
- **`whatsapp_config_routes.py`** - WhatsApp configuration endpoints
- **`workflow_controller.py`** - Workflow management endpoints

---

## `/app/data_layer/` - Data Access Layer

### Root Files

- **`__init__.py`** - Module initialization
- **`agent_constants.py`** - Agent-related constants
- **`agent_files_mapping_client.py`** - Agent file mapping data access
- **`agent_persistent_service.py`** - Agent persistence service
- **`api_key_providers_constant.py`** - API key provider constants
- **`database_manager.py`** - Database connection management
- **`supabase_client.py`** - Supabase client wrapper
- **`tables_name_constant.py`** - Database table name constants
- **`upload_files_client.py`** - File upload data access

### `/crud/` - CRUD Operations

Database CRUD operations for all entities:

- **`__init__.py`** - Module initialization
- **`agent_crud.py`** - Agent CRUD operations
- **`agent_files_mapping_crud.py`** - Agent-file mapping CRUD
- **`agent_full_config_func.py`** - Agent full configuration retrieval
- **`agent_model_config_crud.py`** - Agent model configuration CRUD
- **`agent_phone_mapping_crud.py`** - Agent-phone mapping CRUD
- **`agent_tool_crud.py`** - Agent tool association CRUD
- **`agent_transcriber_config_crud.py`** - Transcriber configuration CRUD
- **`agent_tts_config_crud.py`** - TTS configuration CRUD
- **`agent_tts_config_crud_new.py`** - Updated TTS configuration CRUD
- **`agent_vad_config_crud.py`** - Voice Activity Detection config CRUD
- **`agent_workflow_crud.py`** - Agent workflow CRUD
- **`analytics_crud.py`** - Analytics data CRUD
- **`api_key_crud.py`** - API key CRUD
- **`base_crud.py`** - Base CRUD class with common operations
- **`call_session_crud.py`** - Call session CRUD
- **`cascading_operations.py`** - Cascading delete/update operations
- **`configuration_validation_crud.py`** - Configuration validation
- **`default_providers_func.py`** - Default provider setup functions
- **`external_integration_crud.py`** - External integration CRUD
- **`inferencing_config_crud.py`** - Inferencing configuration CRUD
- **`mcp_user_mapping_crud.py`** - MCP user mapping CRUD
- **`model_provider_crud.py`** - Model provider CRUD
- **`n8n_workflow_integration_crud.py`** - N8N workflow integration CRUD
- **`nango_integration_endpoint_crud.py`** - Nango endpoint CRUD
- **`post_call_analysis_crud.py`** - Post-call analysis CRUD
- **`tool_endpoint_def_crud.py`** - Tool endpoint definition CRUD
- **`tools_mcp_server_def_crud.py`** - MCP server definition CRUD
- **`transcriber_provider_crud.py`** - Transcriber provider CRUD
- **`tts_provider_crud.py`** - TTS provider CRUD
- **`twilio_phone_crud.py`** - Twilio phone number CRUD
- **`ultravox_agent_mapping_crud.py`** - Ultravox agent mapping CRUD
- **`ultravox_agent_tool_crud.py`** - Ultravox agent tool CRUD
- **`upload_file_crud.py`** - Uploaded file CRUD
- **`vad_provider_crud.py`** - VAD provider CRUD
- **`whatsapp_config_crud.py`** - WhatsApp configuration CRUD
- **`workflow_data_service.py`** - Workflow data service
- **`workflow_full_config_func.py`** - Workflow full configuration
- **`workflow_model_config_crud.py`** - Workflow model config CRUD
- **`workflow_node_crud.py`** - Workflow node CRUD
- **`workflow_transcriber_config_crud.py`** - Workflow transcriber config CRUD
- **`workflow_transition_crud.py`** - Workflow transition CRUD
- **`workflow_tts_config_crud.py`** - Workflow TTS config CRUD

### `/data_classes/` - Data Classes & Models

#### Root Files

- **`__init__.py`** - Module initialization
- **`agent_config.py`** - Agent configuration model
- **`agent_files_mapping.py`** - Agent-file mapping model
- **`agent_model_config.py`** - Agent model configuration
- **`agent_phone_mapping.py`** - Agent-phone mapping model
- **`agent_stt_config.py`** - Speech-to-text configuration
- **`agent_tool.py`** - Agent tool model
- **`agent_tts_config.py`** - Text-to-speech configuration
- **`agent_vad_config.py`** - Voice activity detection configuration
- **`agent_with_providers.py`** - Agent with provider details
- **`agent_workflow.py`** - Agent workflow model
- **`api_key.py`** - API key model
- **`call_session.py`** - Call session model
- **`external_integration.py`** - External integration model
- **`inferencing_config.py`** - Inferencing configuration model
- **`mcp_user_mapping.py`** - MCP user mapping model
- **`model_provider.py`** - Model provider model
- **`n8n_workflow_integration.py`** - N8N workflow integration model
- **`nango_integration_endpoint.py`** - Nango integration endpoint model
- **`nango_integration_provider.py`** - Nango provider model
- **`providers.py`** - Provider models
- **`tool_endpoint_def.py`** - Tool endpoint definition model
- **`tools_def.py`** - Tool definition model
- **`tools_mcp_server_def.py`** - MCP server definition model
- **`transcriber_provider.py`** - Transcriber provider model
- **`tts_provider.py`** - TTS provider model
- **`twilio_phone_number.py`** - Twilio phone number model
- **`upload_file.py`** - Upload file model
- **`vad_providers.py`** - VAD provider model
- **`whatsapp_config.py`** - WhatsApp configuration model
- **`whatsapp_service_config.py`** - WhatsApp service config model
- **`workflow_full_config.py`** - Workflow full configuration model
- **`workflow_model_config.py`** - Workflow model config
- **`workflow_node.py`** - Workflow node model
- **`workflow_node_dto.py`** - Workflow node DTO
- **`workflow_transcribe_config.py`** - Workflow transcriber config
- **`workflow_transition.py`** - Workflow transition model
- **`workflow_tts_config.py`** - Workflow TTS config

#### `/domain_models/` - Domain Models

Domain-specific models:

- **`__init__.py`** - Module initialization
- **`agent_workflow_node_type.py`** - Workflow node type enum
- **`exception_type.py`** - Exception type definitions
- **`global_tool_action_type.py`** - Global tool action types
- **`llm_providers.py`** - LLM provider enums
- **`model_streaming_response.py`** - Model streaming response structure
- **`phone_config_source.py`** - Phone configuration source enum
- **`prompt.py`** - Prompt model
- **`stt_providers.py`** - STT provider enums
- **`supported_model_providers.py`** - Supported model providers
- **`tool_call.py`** - Tool call model
- **`tool_type.py`** - Tool type definitions
- **`tts_providers.py`** - TTS provider enums
- **`user_input_source.py`** - User input source enum
- **`voice_output_message.py`** - Voice output message model

#### `/dto/` - Data Transfer Objects (v1)

- **`__init__.py`** - Module initialization
- **`workflow_dto.py`** - Workflow DTO

#### `/dtos/` - Data Transfer Objects (v2)

Request/response DTOs:

- **`api_key_request.py`** - API key request DTO
- **`batch_calling_dtos.py`** - Batch calling DTOs
- **`call_models.py`** - Call-related models
- **`create_workflow_request.py`** - Workflow creation request
- **`create_workflow_response.py`** - Workflow creation response
- **`n8n_user_request.py`** - N8N user request DTO
- **`nango_auth_webhook.py`** - Nango auth webhook payload
- **`nango_session_create_request.py`** - Nango session creation request
- **`phone_management_dtos.py`** - Phone management DTOs
- **`post_call_analysis_dto.py`** - Post-call analysis DTO
- **`ultravox_agent_mapping_dto.py`** - Ultravox agent mapping DTO
- **`ultravox_agent_request.py`** - Ultravox agent request DTO
- **`ultravox_tool_dto.py`** - Ultravox tool DTO
- **`ultravox_tool_mapping_request.py`** - Ultravox tool mapping request
- **`whatsapp_config_dtos.py`** - WhatsApp config DTOs
- **`whatsapp_message_dto.py`** - WhatsApp message DTO
- **`whatsapp_webhook_payload.py`** - WhatsApp webhook payload
- **`workflow_update_request.py`** - Workflow update request

---

## `/app/factories/` - Factory Patterns

- **`__init__.py`** - Module initialization
- **`agent_graph_builder.py`** - Agent graph builder factory
- **`agent_handler_factory.py`** - Agent handler factory
- **`configuration_factory.py`** - Configuration factory
- **`inferencing_handler_factory.py`** - Inferencing handler factory

---

## `/app/media_stream_handler/` - Media Stream Handling

Real-time media stream processing:

- **`__init__.py`** - Module initialization
- **`base_call_session_handler.py`** - Base call session handler
- **`icall_session_handler.py`** - Call session handler interface
- **`twilio_call_session_handler.py`** - Twilio-specific call handler
- **`web_call_session_handler.py`** - Web-based call handler
- **`websocket_stream_handler.py`** - WebSocket stream handler

---

## `/app/middleware/` - Middleware

Middleware components (currently empty directory with `__pycache__` only)

---

## `/app/models/` - AI Models

### `/language_models/` - Language Model Integrations

#### Root Files

- **`__init__.py`** - Module initialization
- **`model_factory.py`** - LLM model factory

#### `/offline_serving/` - Local Model Serving

- **`__init__.py`** - Module initialization
- **`end_of_turn_model.py`** - End-of-turn detection model

#### `/online_serving/` - Cloud Model Serving

- **`__init__.py`** - Module initialization
- **`base_prediction_client.py`** - Base prediction client abstraction

##### `/clients/` - Model Provider Clients

- **`__init__.py`** - Module initialization
- **`llm_model_client.py`** - Generic LLM client
- **`qwen_online_prediction_client.py`** - Qwen model client
- **`ultravox_online_prediction_client.py`** - Ultravox model client

### `/stt_models/` - Speech-to-Text Models

- **`__init__.py`** - Module initialization
- **`assembly_ai_rest_stt.py`** - AssemblyAI REST STT
- **`async_base_realtime_stt.py`** - Async base realtime STT
- **`base_realtime_stt.py`** - Base realtime STT
- **`base_stt.py`** - Base STT abstraction
- **`cartesia_realtime_stt.py`** - Cartesia realtime STT
- **`deepgram_realtime_stt.py`** - Deepgram realtime STT
- **`faster_whisper.py`** - Faster Whisper implementation
- **`sarvam_rest_stt.py`** - Sarvam REST STT
- **`soniox_realtime_stt.py`** - Soniox realtime STT
- **`whisper.py`** - Whisper implementation

---

## `/app/nlp/` - Natural Language Processing

### `/search_engine/` - Search Engine

- **`__init__.py`** - Module initialization
- **`elastic_search_engine.py`** - Elasticsearch implementation
- **`search_engine.py`** - Search engine abstraction

---

## `/app/prompts/` - Prompt Templates

### `/mcp/` - MCP Prompts

(Empty directory)

### `/tools/` - Tool Prompts

(Empty directory)

---

## `/app/services/` - Business Logic Services

### Root Files

- **`__init__.py`** - Module initialization
- **`agent_configuration_service.py`** - Agent configuration service
- **`agent_files_mapping_service.py`** - Agent file mapping service
- **`api_key_service.py`** - API key management service
- **`batch_calling_service.py`** - Batch calling service
- **`call_analytics_service.py`** - Call analytics service
- **`chromadb_service.py`** - ChromaDB service
- **`composio_service.py`** - Composio integration service
- **`dashboard_service.py`** - Dashboard data service
- **`embedding_service.py`** - Embedding generation service
- **`exception_tts_prompter.py`** - Exception TTS prompt handler
- **`file_upload_service.py`** - File upload service
- **`filler_tts_prompter.py`** - Filler TTS prompt handler
- **`mcp_tools_service.py`** - MCP tools service
- **`model_provider_service.py`** - Model provider service
- **`n8n_workflow_service.py`** - N8N workflow service
- **`nango_integration_endpoint_service.py`** - Nango endpoint service
- **`nango_service.py`** - Nango integration service
- **`openai_speech_processor.py`** - OpenAI speech processing
- **`phone_management_service.py`** - Phone management service
- **`post_call_analysis_crud_service.py`** - Post-call analysis CRUD service
- **`post_call_analysis_intelligence_service.py`** - Post-call analysis AI service
- **`tool_persistent_service.py`** - Tool persistence service
- **`transcript_collector.py`** - Transcript collection service
- **`twilio_call_service.py`** - Twilio call service
- **`twilio_session_config_manager.py`** - Twilio session configuration
- **`twilio_twiml_app_service.py`** - Twilio TwiML app service
- **`twilio_verification_service.py`** - Twilio verification service
- **`ultravox_call_service.py`** - Ultravox call service
- **`whatsapp_config_service.py`** - WhatsApp configuration service
- **`whatsapp_service.py`** - WhatsApp service
- **`workflow_service.py`** - Workflow service

### `/billing_components/` - Billing

(Empty directory with `__pycache__` only)

### `/handlers/` - Service Handlers

Real-time voice/text handlers:

- **`base_realtime_voice_handler.py`** - Base realtime voice handler
- **`realtime_text_handler.py`** - Realtime text handler
- **`realtime_voice_handler.py`** - Standard realtime voice handler
- **`realtime_voice_handler_with_deepgram_flux.py`** - Deepgram Flux integration
- **`realtime_voice_handler_with_sarvam.py`** - Sarvam integration
- **`realtime_voice_handler_with_stt.py`** - STT-integrated voice handler

### `/inferencing_handlers/` - Inferencing

AI inferencing handlers:

- **`__init__.py`** - Module initialization
- **`audio_inference_handler.py`** - Audio inference handler
- **`base_speech_inferencing_handler.py`** - Base speech inferencing
- **`inference_handler.py`** - Generic inference handler
- **`speech_to_speech_handler.py`** - Speech-to-speech handler
- **`speech_to_text_inference_handler.py`** - Speech-to-text inference handler

### `/noise_reduction/` - Noise Reduction

Audio noise reduction pipeline:

- **`__init__.py`** - Module initialization
- **`deep_filter_noise_reduction_stage.py`** - Deep filter noise reduction
- **`noise_reduction_pipeline.py`** - Noise reduction pipeline
- **`pipeline_stage.py`** - Pipeline stage abstraction
- **`rn_noise_reduction_stage.py`** - RN noise reduction stage

### `/speech_processor/` - Speech Processing

#### Root Files

- **`__init__.py`** - Module initialization
- **`eos_processor.py`** - End-of-speech processor

#### `/vad/` - Voice Activity Detection

- **`__init__.py`** - Module initialization
- **`silero_vad_processor.py`** - Silero VAD implementation
- **`vad_processor.py`** - VAD processor abstraction

### `/speech_to_text/` - Speech-to-Text Services

- **`__init__.py`** - Module initialization
- **`base_stt.py`** - Base STT service
- **`faster_whisper.py`** - Faster Whisper service
- **`transcription_handler.py`** - Transcription handler
- **`whisper.py`** - Whisper service

### `/text_to_speech/` - Text-to-Speech Services

- **`__init__.py`** - Module initialization
- **`azure_tts_processor.py`** - Azure TTS processor
- **`cartesia_tts_processor.py`** - Cartesia TTS processor
- **`deepgram_tts_processor.py`** - Deepgram TTS processor
- **`elevenlabs_tts_processor.py`** - ElevenLabs TTS processor
- **`google_tts_processor.py`** - Google TTS processor
- **`inworld_tts_processor.py`** - Inworld TTS processor
- **`sarvam_rest_tts_processor.py`** - Sarvam REST TTS processor
- **`sarvam_tts_processor.py`** - Sarvam TTS processor
- **`text_to_speech_processor.py`** - TTS processor abstraction

---

## `/app/telemetries/` - Telemetry & Monitoring

- **`__init__.py`** - Module initialization
- **`logger.py`** - Custom logger implementation
- **`metrics_constants.py`** - Metrics constants
- **`prometheus_metrics.py`** - Prometheus metrics collector
- **`request_manager.py`** - Request tracking manager

---

## `/app/utilities/` - Utility Functions

- **`__init__.py`** - Module initialization
- **`audio_utils.py`** - Audio processing utilities
- **`auth_utility.py`** - Authentication utilities
- **`call_operations_constant.py`** - Call operation constants
- **`crypto_utils.py`** - Cryptography utilities
- **`document_processor.py`** - Document processing utilities
- **`error_messages.py`** - Error message constants
- **`exception_tts_prompt_loader.py`** - Exception TTS prompt loader
- **`filler_tts_loader.py`** - Filler TTS loader
- **`lemmatizer.py`** - Text lemmatization
- **`model_utils.py`** - Model utilities
- **`openai_output_schema_parser.py`** - OpenAI output parser
- **`openai_utils.py`** - OpenAI utilities
- **`origin_validator.py`** - Origin validation
- **`response_filter.py`** - Response filtering
- **`retry_manager.py`** - Retry logic manager
- **`sentence_boundary.py`** - Sentence boundary detection
- **`sse_event_broadcaster.py`** - Server-sent events broadcaster
- **`stop_watch.py`** - Performance timing utility
- **`text_transformation.py`** - Text transformation utilities
- **`text_utils.py`** - Text utilities
- **`tool_formatter.py`** - Tool formatting utilities
- **`tool_utils.py`** - Tool utilities
- **`twilio_utils.py`** - Twilio utilities
- **`usage_controller.py`** - Usage tracking controller
- **`utility.py`** - General utilities
- **`workflow_prompt_generator.py`** - Workflow prompt generator
- **`workflow_prompt_templetes.py`** - Workflow prompt templates
- **`workflow_response_convertor.py`** - Workflow response converter

---

## `/deployment/` - Deployment Documentation

- **`build_and_deploy.md`** - Build and deployment guide
- **`deploy-script.sh`** - Deployment shell script
- **`lambda.md`** - AWS Lambda deployment guide
- **`pranthora_nginx`** - Nginx configuration
- **`run_pod.md`** - RunPod deployment guide

---

## `/env_creds/` - Environment Credentials

- **`credentials.json`** - Application credentials (⚠️ sensitive)
- **`weaviate_cred.json`** - Weaviate credentials (⚠️ sensitive)

---

## `/metrics/` - Metrics & Dashboards

- **`Voice Assistant Platform-1747614615498.json`** - Grafana/monitoring dashboard configuration

---

## `/tests/` - Test Suite

### Root Test Files

- **`__init__.py`** - Test module initialization
- **`chromadb_setup.py`** - ChromaDB test setup
- **`test_call_transfer.py`** - Call transfer tests
- **`test_cleaner.py`** - Cleaner utility tests
- **`test_composio_openai_tools.py`** - Composio-OpenAI integration tests
- **`test_conversation_history.py`** - Conversation history tests
- **`test_crud_integration.py`** - CRUD integration tests
- **`test_crud_operations.py`** - CRUD operation tests
- **`test_llm_geneation.py`** - LLM generation tests
- **`test_nango_proxy_slack.py`** - Nango Slack proxy tests
- **`test_openai_output_schema_parser.py`** - OpenAI parser tests
- **`test_provider_routes.py`** - Provider route tests
- **`test_qand_a.py`** - Q&A tests
- **`test_rag_client.py`** - RAG client tests
- **`test_real_time_handler.py`** - Real-time handler tests
- **`test_response_filter.py`** - Response filter tests
- **`test_sarvam.py`** - Sarvam integration tests
- **`test_should_allow_fxn.py`** - Function allowance tests
- **`test_tool_calling.py`** - Tool calling tests
- **`test_whatsapp_webhook_sse.py`** - WhatsApp webhook SSE tests
- **`twilio_conference_call_test.py`** - Twilio conference call tests

### `/assets/` - Test Assets

Test audio files and utilities:

- **`expose_ngrok.py`** - Ngrok exposure utility
- **`generate_filler_text.py`** - Filler text generator
- **`simple_canadian_history_question.mp3`** - Test audio file
- **`simplified_expose_ngrok.py`** - Simplified ngrok utility
- **`twilio_create_call.py`** - Twilio call creation utility
- **`twilio_create_call_gradio_app.py`** - Gradio app for call creation
- **`two_questions_with_interupt.mp3`** - Test audio file
- **`vllm_model_run.ipynb`** - VLLM model testing notebook

#### `/load_test/` - Load Testing

- **`transcription_load_test.py`** - Transcription load tests
- **`vllm_load_test.py`** - VLLM load tests

### `/evaluations/` - Model Evaluations

- **`tool_calling_evaluation.ipynb`** - Tool calling evaluation notebook

### `/integration/` - Integration Tests

Audio streaming integration tests:

- **`twilio_audio_streamer.py`** - Twilio audio streaming test
- **`web_audio_streamer.py`** - Web audio streaming test

### `/playground/` - Development Playground

Testing and development playground:

- **`agent_and_ai_interaction_playground.py`** - Agent-AI interaction tests
- **`agent_and_ai_interaction_workflow_playground.py`** - Workflow interaction tests
- **`agent_interaction_playground.py`** - Agent interaction playground
- **`agent_testing_with_llm.py`** - LLM agent testing
- **`agent_workflow_playground.py`** - Workflow playground
- **`realtimeTTS_test.py`** - Real-time TTS tests
- **`test_scenarios.json`** - Test scenario definitions
- **`tts_test.py`** - TTS testing
- **`vllm_script.txt`** - VLLM script
- **`website.html`** - Test website

#### `/voice_agent_auto_test/` - Voice Agent Automated Tests

- **`question_1_file.wav`** - Test audio file 1
- **`question_2_file.wav`** - Test audio file 2
- **`twilio_agents_stt_tts_tester.py`** - Twilio agent STT/TTS tester
- **`user_prompt_updator.py`** - User prompt updater
- **`voice2voice_test_web.py`** - Voice-to-voice web test
- **`web_agents_stt_tts_tester.py`** - Web agent STT/TTS tester

### `/tool_tester/` - Tool Testing

(Empty directory with `__pycache__` only)

---

## Architecture Overview

### Key Components

1. **Agent Management System** (`/app/agents_management/`)

   - Core voice agent orchestration
   - Workflow graph execution
   - RAG and vector database integration
   - Tool execution and integration

2. **API Layer** (`/app/api/v1/`)

   - REST API endpoints
   - Webhook handlers (Twilio, WhatsApp, N8N, Nango)
   - Provider configurations

3. **Data Layer** (`/app/data_layer/`)

   - Comprehensive CRUD operations
   - Data models and DTOs
   - Database management (Supabase)

4. **Services** (`/app/services/`)

   - Business logic
   - Speech processing (STT/TTS)
   - Real-time voice handlers
   - Integration services

5. **AI Models** (`/app/models/`)

   - Language model integrations
   - STT model implementations
   - Online and offline serving

6. **Media Streaming** (`/app/media_stream_handler/`)

   - Real-time audio streaming
   - Twilio and Web call handling
   - WebSocket management

7. **Utilities & Infrastructure**
   - Telemetry and monitoring (`/app/telemetries/`)
   - Utility functions (`/app/utilities/`)
   - Middleware (`/app/middleware/`)

### Technology Stack

- **Framework**: FastAPI (Python)
- **Database**: Supabase (PostgreSQL)
- **Vector DB**: Weaviate, ChromaDB
- **Voice Services**: Twilio, Ultravox, Deepgram, ElevenLabs, Sarvam, Cartesia
- **LLM Providers**: OpenAI, Qwen, Ultravox
- **Integrations**: Composio, Nango, N8N, MCP (Model Context Protocol)
- **Monitoring**: Prometheus, Loki, Grafana
- **Containerization**: Docker, Docker Compose
- **Testing**: Pytest

### Key Features

- Multi-provider voice agent platform
- Real-time speech-to-speech conversations
- RAG-enabled knowledge retrieval
- Workflow-based agent orchestration
- Tool calling and external integrations
- WhatsApp and Twilio telephony support
- Post-call analytics and intelligence
- Batch calling capabilities
- Multi-tenancy with API key management

---

## Notes

- **Security**: Credentials stored in `/env_creds/` should be secured and not committed to version control
- **Python Cache**: `__pycache__` directories throughout the project contain compiled Python bytecode
- **Configuration**: Multiple config files support demo and production environments
- **Scalability**: Docker Compose configurations for development and production deployments
- **Monitoring**: Comprehensive telemetry with Prometheus and Loki integration

---

**Document Version**: 1.0  
**Last Updated**: Based on current repository state  
**Repository**: pranthora_backend  
**Branch**: main
