from typing import Sequence, Optional

from app.db.models import Breed
from .mixins import CRUDServiceMixin
from app.repositories import RepositoryBreed


class BreedService(CRUDServiceMixin):
    def __init__(
        self,
        repository_breed: RepositoryBreed,
        unique_fields: Optional[Sequence[str]] = None,
    ):
        self._repository_breed = repository_breed
        super().__init__(
            repository=repository_breed,
            unique_fields=unique_fields,
        )
        