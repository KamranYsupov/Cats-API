from dependency_injector import containers, providers

from app.repositories import (
    RepositoryCat,
    RepositoryBreed,
)
from app.services import (
    CatService,
    BreedService,
)
from app.db import DataBaseManager
from app.db.models import (
    Cat,
    Breed,
)
from app.core.config import settings


class Container(containers.DeclarativeContainer):
    db_manager = providers.Singleton(DataBaseManager, db_url=settings.db_url)
    session = providers.Resource(db_manager().get_async_session)

    # region repository
    repository_cat = providers.Singleton(
        RepositoryCat,  
        model=Cat,
        session=session
    )
    repository_breed = providers.Singleton(
        RepositoryBreed,
        model=Breed,
        session=session
    )
    # endregion

    # region services
    cat_service = providers.Singleton(
        CatService, repository_cat=repository_cat
    )
    breed_service = providers.Singleton(
        BreedService, repository_breed=repository_breed
    )
    # endregion



