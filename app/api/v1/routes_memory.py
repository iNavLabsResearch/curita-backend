"""
API routes for Toy Memory and Agent Memory CRUD operations
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID
from app.telemetries.logger import logger
from app.data_layer.crud import get_toy_memory_crud, get_agent_memory_crud
from app.data_layer.data_classes.memory_schemas import (
    ToyMemoryCreate, ToyMemoryUpdate, ToyMemoryResponse,
    AgentMemoryCreate, AgentMemoryUpdate, AgentMemoryResponse
)

# Toy Memory Router
toy_memory_router = APIRouter(prefix="/toy-memory", tags=["Toy Memory"])
# Agent Memory Router  
agent_memory_router = APIRouter(prefix="/agent-memory", tags=["Agent Memory"])

# ===== TOY MEMORY ROUTES =====
@toy_memory_router.post("", response_model=ToyMemoryResponse, status_code=status.HTTP_201_CREATED)
async def create_toy_memory(memory: ToyMemoryCreate):
    try:
        crud = get_toy_memory_crud()
        result = await crud.create(memory)
        if not result:
            raise HTTPException(status_code=500, detail="Failed to create toy memory")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@toy_memory_router.get("/{memory_id}", response_model=ToyMemoryResponse)
async def get_toy_memory(memory_id: UUID):
    try:
        crud = get_toy_memory_crud()
        result = await crud.get_by_id(memory_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Toy memory {memory_id} not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@toy_memory_router.get("", response_model=List[ToyMemoryResponse])
async def get_all_toy_memories(limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0)):
    try:
        crud = get_toy_memory_crud()
        return await crud.get_all(limit=limit, offset=offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@toy_memory_router.get("/toy/{toy_id}/all", response_model=List[ToyMemoryResponse])
async def get_toy_memories_by_toy(toy_id: UUID):
    try:
        crud = get_toy_memory_crud()
        return await crud.get_all(filters={"toy_id": toy_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@toy_memory_router.post("/search/embedding", response_model=List[ToyMemoryResponse])
async def search_toy_memory_by_embedding(
    embedding: List[float] = Query(...), toy_id: Optional[UUID] = None, limit: int = 10):
    try:
        crud = get_toy_memory_crud()
        return await crud.search_by_embedding(embedding, toy_id, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@toy_memory_router.put("/{memory_id}", response_model=ToyMemoryResponse)
async def update_toy_memory(memory_id: UUID, memory: ToyMemoryUpdate):
    try:
        crud = get_toy_memory_crud()
        result = await crud.update(memory_id, memory)
        if not result:
            raise HTTPException(status_code=404, detail=f"Toy memory {memory_id} not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@toy_memory_router.delete("/{memory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_toy_memory(memory_id: UUID):
    try:
        crud = get_toy_memory_crud()
        success = await crud.delete(memory_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Toy memory {memory_id} not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@toy_memory_router.delete("/toy/{toy_id}/all", status_code=status.HTTP_204_NO_CONTENT)
async def delete_toy_memories_by_toy(toy_id: UUID):
    try:
        crud = get_toy_memory_crud()
        success = await crud.delete_by_toy_id(toy_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"No memories found for toy {toy_id}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== AGENT MEMORY ROUTES =====
@agent_memory_router.post("", response_model=AgentMemoryResponse, status_code=status.HTTP_201_CREATED)
async def create_agent_memory(memory: AgentMemoryCreate):
    try:
        crud = get_agent_memory_crud()
        result = await crud.create(memory)
        if not result:
            raise HTTPException(status_code=500, detail="Failed to create agent memory")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@agent_memory_router.get("/{memory_id}", response_model=AgentMemoryResponse)
async def get_agent_memory(memory_id: UUID):
    try:
        crud = get_agent_memory_crud()
        result = await crud.get_by_id(memory_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Agent memory {memory_id} not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@agent_memory_router.get("", response_model=List[AgentMemoryResponse])
async def get_all_agent_memories(limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0)):
    try:
        crud = get_agent_memory_crud()
        return await crud.get_all(limit=limit, offset=offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@agent_memory_router.get("/agent/{agent_id}/all", response_model=List[AgentMemoryResponse])
async def get_agent_memories_by_agent(agent_id: UUID):
    try:
        crud = get_agent_memory_crud()
        return await crud.get_all(filters={"agent_id": agent_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@agent_memory_router.post("/search/embedding", response_model=List[AgentMemoryResponse])
async def search_agent_memory_by_embedding(
    embedding: List[float] = Query(...), agent_id: Optional[UUID] = None, limit: int = 10):
    try:
        crud = get_agent_memory_crud()
        return await crud.search_by_embedding(embedding, agent_id, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@agent_memory_router.put("/{memory_id}", response_model=AgentMemoryResponse)
async def update_agent_memory(memory_id: UUID, memory: AgentMemoryUpdate):
    try:
        crud = get_agent_memory_crud()
        result = await crud.update(memory_id, memory)
        if not result:
            raise HTTPException(status_code=404, detail=f"Agent memory {memory_id} not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@agent_memory_router.delete("/{memory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent_memory(memory_id: UUID):
    try:
        crud = get_agent_memory_crud()
        success = await crud.delete(memory_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Agent memory {memory_id} not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@agent_memory_router.delete("/agent/{agent_id}/all", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent_memories_by_agent(agent_id: UUID):
    try:
        crud = get_agent_memory_crud()
        success = await crud.delete_by_agent_id(agent_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"No memories found for agent {agent_id}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
