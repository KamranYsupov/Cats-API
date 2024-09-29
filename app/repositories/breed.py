from app.db.models import Breed
from .base import RepositoryBase


class RepositoryBreed(RepositoryBase[Breed]):
    """Репозиторий для работы с таблицей breeds"""