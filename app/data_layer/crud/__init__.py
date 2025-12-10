"""
CRUD module initialization
"""
from app.data_layer.crud.base_crud import BaseCrud
from app.data_layer.crud.toy_crud import ToyCRUD
from app.data_layer.crud.agent_crud import AgentCRUD

__all__ = ["BaseCRUD", "ToyCRUD", "AgentCRUD"]
