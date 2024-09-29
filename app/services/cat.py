import uuid
from typing import Sequence, List, Optional

from app.db.models import Cat
from .mixins import CRUDServiceMixin
from app.repositories import RepositoryCat


class CatService(CRUDServiceMixin):
    def __init__(
        self,
        repository_cat: RepositoryCat,
        unique_fields: Optional[Sequence[str]] = None,
    ):
        self._repository_cat = repository_cat
        super().__init__(
            repository=repository_cat,
            unique_fields=unique_fields,
        )
        
    async def list(
        self,
        *args,
        limit: Optional[int] = None,
        skip: Optional[int] = None,
        load_breed: bool = False,
        **kwargs
    ) -> List[Cat]:
        return await super().list(
            *args,
            load_breed=load_breed,
            limit=limit,
            skip=skip,
            **kwargs
        )
        
    async def get(
        self,
        load_breed: bool = False,
        **kwargs
    ) -> Cat:
        return await super().get(
            load_breed=load_breed,
            **kwargs
        )
        