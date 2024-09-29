from typing import List, Type, Optional

from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Cat
from .base import RepositoryBase, ModelType


class RepositoryCat(RepositoryBase[Cat]):
    """Репозиторий для работы с таблицей cats"""
    
    def __init__(
        self, 
        model: Type[ModelType], 
        session: AsyncSession
    ):
        self._session = session
        super().__init__(
            model=Cat,
            session=session,
        )

    async def list(
        self,
        *args,
        limit: Optional[int] = None,
        skip: Optional[int] = None,
        load_breed: bool = False,
        **kwargs
    ) -> List[Cat]:
        options = self._get_query_options(load_breed)
                
        return await super().list(
            *args, 
            limit=limit, 
            skip=skip,
            options=options,
            **kwargs,
        )
    
    async def get(
        self,
        load_breed: bool = False,
        **kwargs
    ) -> Cat:
        options = self._get_query_options(load_breed)
        
        return await super().get(options=options, **kwargs)
    
    @staticmethod
    def _get_query_options(
        load_breed: bool = False
    ) -> List:
        query_options = []
        if load_breed:
            print('load')
            query_options.append(
                joinedload(Cat.breed)
            )
            
        return query_options