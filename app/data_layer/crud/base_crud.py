"""
Base CRUD operations for all database entities.
Provides generic CRUD operations that can be inherited by specific CRUD classes.
"""
from typing import TypeVar, Generic, Optional, List, Dict, Any, Type
from pydantic import BaseModel
from uuid import UUID
from app.data_layer.supabase_client import SupabaseClient, get_supabase
from app.telemetries.logger import logger


# Type variables for generic CRUD operations
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseModel)


class BaseCRUD(Generic[CreateSchemaType, UpdateSchemaType, ResponseSchemaType]):
    """
    Base CRUD class providing generic database operations.
    
    This class implements the Repository pattern for database operations,
    providing a clean separation between business logic and data access.
    
    Type Parameters:
        CreateSchemaType: Pydantic model for creation operations
        UpdateSchemaType: Pydantic model for update operations
        ResponseSchemaType: Pydantic model for response operations
    """
    
    def __init__(
        self,
        table_name: str,
        response_model: Type[ResponseSchemaType],
        supabase_client: Optional[SupabaseClient] = None
    ):
        """
        Initialize the CRUD instance.
        
        Args:
            table_name: Name of the database table
            response_model: Pydantic model class for responses
            supabase_client: Optional Supabase client instance
        """
        self.table_name = table_name
        self.response_model = response_model
        self.supabase = supabase_client or get_supabase()
        logger.info(f"Initialized {self.__class__.__name__} for table '{table_name}'")
    
    async def create(self, data: CreateSchemaType) -> Optional[ResponseSchemaType]:
        """
        Create a new record in the database.
        
        Args:
            data: Pydantic model containing data to create
            
        Returns:
            Created record as response model, or None if failed
        """
        try:
            data_dict = data.model_dump(exclude_unset=True)
            logger.debug(f"Creating new record in {self.table_name}: {data_dict}")
            
            result = await self.supabase.insert(self.table_name, data_dict)
            
            if result and len(result) > 0:
                logger.info(f"Successfully created record in {self.table_name} with id: {result[0].get('id')}")
                return self.response_model(**result[0])
            
            logger.warning(f"Failed to create record in {self.table_name}")
            return None
            
        except Exception as e:
            logger.error(f"Error creating record in {self.table_name}: {str(e)}", exc_info=True)
            return None
    
    async def get_by_id(self, id: UUID) -> Optional[ResponseSchemaType]:
        """
        Retrieve a single record by its ID.
        
        Args:
            id: UUID of the record to retrieve
            
        Returns:
            Record as response model, or None if not found
        """
        try:
            logger.debug(f"Fetching record from {self.table_name} with id: {id}")
            
            result = await self.supabase.select(
                self.table_name,
                filters={"id": str(id)},
                limit=1
            )
            
            if result and len(result) > 0:
                logger.info(f"Successfully retrieved record from {self.table_name} with id: {id}")
                return self.response_model(**result[0])
            
            logger.warning(f"Record not found in {self.table_name} with id: {id}")
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving record from {self.table_name} with id {id}: {str(e)}", exc_info=True)
            return None
    
    async def get_all(
        self,
        limit: int = 100,
        offset: int = 0,
        order_by: str = "created_at",
        order_desc: bool = True,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ResponseSchemaType]:
        """
        Retrieve all records with optional filtering and pagination.
        
        Args:
            limit: Maximum number of records to return (default: 100)
            offset: Number of records to skip (default: 0)
            order_by: Column to order by (default: "created_at")
            order_desc: Whether to order descending (default: True)
            filters: Optional dictionary of filters to apply
            
        Returns:
            List of records as response models
        """
        try:
            logger.debug(f"Fetching records from {self.table_name} with filters: {filters}")
            
            result = await self.supabase.select(
                self.table_name,
                filters=filters or {},
                limit=limit,
                offset=offset,
                order_by=order_by,
                order_desc=order_desc
            )
            
            if result:
                records = [self.response_model(**record) for record in result]
                logger.info(f"Successfully retrieved {len(records)} records from {self.table_name}")
                return records
            
            logger.info(f"No records found in {self.table_name}")
            return []
            
        except Exception as e:
            logger.error(f"Error retrieving records from {self.table_name}: {str(e)}", exc_info=True)
            return []
    
    async def update(
        self,
        id: UUID,
        data: UpdateSchemaType
    ) -> Optional[ResponseSchemaType]:
        """
        Update an existing record by its ID.
        
        Args:
            id: UUID of the record to update
            data: Pydantic model containing fields to update
            
        Returns:
            Updated record as response model, or None if failed
        """
        try:
            # Only include fields that are explicitly set (not None)
            update_data = data.model_dump(exclude_unset=True, exclude_none=True)
            
            if not update_data:
                logger.warning(f"No data provided for update in {self.table_name}")
                return await self.get_by_id(id)
            
            logger.debug(f"Updating record in {self.table_name} with id {id}: {update_data}")
            
            result = await self.supabase.update(
                self.table_name,
                filters={"id": str(id)},
                data=update_data
            )
            
            if result and len(result) > 0:
                logger.info(f"Successfully updated record in {self.table_name} with id: {id}")
                return self.response_model(**result[0])
            
            logger.warning(f"Failed to update record in {self.table_name} with id: {id}")
            return None
            
        except Exception as e:
            logger.error(f"Error updating record in {self.table_name} with id {id}: {str(e)}", exc_info=True)
            return None
    
    async def delete(self, id: UUID) -> bool:
        """
        Delete a record by its ID.
        
        Args:
            id: UUID of the record to delete
            
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            logger.debug(f"Deleting record from {self.table_name} with id: {id}")
            
            result = await self.supabase.delete(
                self.table_name,
                filters={"id": str(id)}
            )
            
            if result:
                logger.info(f"Successfully deleted record from {self.table_name} with id: {id}")
                return True
            
            logger.warning(f"Failed to delete record from {self.table_name} with id: {id}")
            return False
            
        except Exception as e:
            logger.error(f"Error deleting record from {self.table_name} with id {id}: {str(e)}", exc_info=True)
            return False
    
    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Count records in the table with optional filtering.
        
        Args:
            filters: Optional dictionary of filters to apply
            
        Returns:
            Number of records matching the filters
        """
        try:
            logger.debug(f"Counting records in {self.table_name} with filters: {filters}")
            
            result = await self.supabase.select(
                self.table_name,
                filters=filters or {}
            )
            
            count = len(result) if result else 0
            logger.info(f"Count for {self.table_name}: {count}")
            return count
            
        except Exception as e:
            logger.error(f"Error counting records in {self.table_name}: {str(e)}", exc_info=True)
            return 0
    
    async def exists(self, id: UUID) -> bool:
        """
        Check if a record exists by its ID.
        
        Args:
            id: UUID of the record to check
            
        Returns:
            True if record exists, False otherwise
        """
        try:
            result = await self.get_by_id(id)
            return result is not None
        except Exception as e:
            logger.error(f"Error checking existence in {self.table_name} with id {id}: {str(e)}", exc_info=True)
            return False
