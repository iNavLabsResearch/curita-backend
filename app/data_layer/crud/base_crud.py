from datetime import datetime
from typing import Any, Dict, List, Optional, Union, Tuple
from supabase.client import AsyncClient
from app.data_layer.supabase_client import SupabaseClient


class BaseCrud:
    def __init__(self, supabase: SupabaseClient, table_name: str, model_class):
        self.supabase: AsyncClient = supabase.get_client()
        self.table_name = table_name
        self.model_class = model_class

    async def create(self, data: Any) -> Any:
        """Create a new record"""
        from app.telemetries.logger import logger
        from dataclasses import is_dataclass

        logger.info(f"Creating record in {self.table_name} 📝")
        logger.info(f"Input data: {data}")
        logger.info(f"Model class: {self.model_class}")

        # Verify the model class is a dataclass
        if not is_dataclass(self.model_class):
            logger.error(f"{self.model_class.__name__} is not a dataclass!")
            raise TypeError(f"{self.model_class.__name__} must be a dataclass")

        response = await self.supabase.table(self.table_name).insert(data).execute()
        if not response.data:
            logger.error(f"No data in response: {response}")
            raise Exception(f"Failed to create record: {response}")

        try:
            logger.info(f"Response data: {response.data[0]}")
            # Create a new instance of the model class with the response data
            db_data = response.data[0]
            logger.info(f"Creating {self.model_class.__name__} with data: {db_data}")

            # Filter out any extra fields that aren't in the dataclass
            valid_fields = {f.name for f in self.model_class.__dataclass_fields__.values()}
            filtered_data = {k: v for k, v in db_data.items() if k in valid_fields}

            # Deserialize JSON fields
            for field_name, field_value in filtered_data.items():
                if isinstance(field_value, str) and field_name in ['tool_schema', 'headers_schema', 'payload_schema']:
                    try:
                        import json
                        filtered_data[field_name] = json.loads(field_value)
                    except (json.JSONDecodeError, TypeError):
                        # Keep as string if JSON parsing fails
                        pass

            # Create the instance
            instance = self.model_class(**filtered_data)
            logger.info(f"Successfully created {self.model_class.__name__} ✅")
            return instance

        except Exception as e:
            error_msg = f"Failed to convert response to {self.model_class.__name__}: {str(e)}"
            logger.error(error_msg)
            logger.error(f"Exception details: {str(e)}")
            raise TypeError(error_msg)

    async def get_by_id(self, id: str) -> Optional[Any]:
        """Get a record by ID"""
        response = await self.supabase.table(self.table_name).select("*").eq("id", id).execute()
        if response.data:
            db_data = response.data[0]
            return self.model_class(**db_data)
        return None

    async def get_all(self) -> List[Any]:
        """Get all records"""
        response = await self.supabase.table(self.table_name).select("*").execute()
        items = []
        for item in response.data:
            items.append(self.model_class(**item))
        return items

    async def update(self, id: str, data: Dict[str, Any]) -> Optional[Any]:
        """Update a record by ID"""
        # Add updated_at timestamp if the table has it
        if hasattr(self.model_class, 'updated_at'):
            data['updated_at'] = datetime.utcnow().isoformat()

        response = await self.supabase.table(self.table_name).update(data).eq("id", id).execute()
        if response.data:
            db_data = response.data[0]
            return self.model_class(**db_data)
        return None

    async def delete(self, id: str) -> bool:
        """Delete a record by ID"""
        response = await self.supabase.table(self.table_name).delete().eq("id", id).execute()
        return len(response.data) > 0

    async def filter_by(self, **filters) -> List[Any]:
        """Filter records by multiple criteria"""
        query = self.supabase.table(self.table_name).select("*")
        for key, value in filters.items():
            if value is not None:
                query = query.eq(key, value)
        response = await query.execute()
        items = []
        for item in response.data:
            items.append(self.model_class(**item))
        return items

    async def paginate(self, page: int = 1, page_size: int = 20, **filters) -> Tuple[List[Any], int]:
        """Paginate records with optional filters"""
        offset = (page - 1) * page_size

        # Get total count
        count_query = self.supabase.table(self.table_name).select("id", count="exact")
        for key, value in filters.items():
            if value is not None:
                count_query = count_query.eq(key, value)
        count_response = await count_query.execute()
        total_count = count_response.count

        # Get paginated data
        query = self.supabase.table(self.table_name).select("*").range(offset, offset + page_size - 1)
        for key, value in filters.items():
            if value is not None:
                query = query.eq(key, value)
        response = await query.execute()

        items = [self.model_class(**item) for item in response.data]
        return items, total_count

    async def get_by_agent_id(self, agent_id: str) -> List[Any]:
        """Get records by agent_id"""
        return await self.filter_by(agent_id=agent_id)

    async def search(self, column: str, search_term: str) -> List[Any]:
        """Search records by a column containing search term"""
        response = await self.supabase.table(self.table_name).select("*").ilike(column, f"%{search_term}%").execute()
        return [self.model_class(**item) for item in response.data]

    async def count(self, **filters) -> int:
        """Count records with optional filters"""
        query = self.supabase.table(self.table_name).select("id", count="exact")
        for key, value in filters.items():
            query = query.eq(key, value)
        response = await query.execute()
        return [self.model_class(**item) for item in response.data]
