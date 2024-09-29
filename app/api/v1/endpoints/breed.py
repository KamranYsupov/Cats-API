from typing import Dict, List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Header, HTTPException
from starlette import status

from app.core.container import Container
from app.db.models import Breed
from app.schemas.breed import BreedCreateSchema, BreedSchema
from app.services import BreedService, BreedService


router = APIRouter(tags=['Breed'], prefix='/breeds')


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=BreedSchema,
    response_model_exclude_none=True,
)
@inject
async def create_breed(
    breed_create_schema: BreedCreateSchema,
    breed_service: BreedService = Depends(
        Provide[Container.breed_service]
    ),
) -> BreedSchema:
    breed = await breed_service.create(breed_create_schema)    
    return breed.serialize(
        schema_class=BreedSchema,
    )


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[BreedSchema])
@inject
async def get_breeds(
    limit: int = 10, 
    skip: int = 0, 
    breed_service: BreedService = Depends(
        Provide[Container.breed_service]
    ),
) -> List[BreedSchema]:
    breeds = await breed_service.list(
        limit=limit,
        skip=skip
    )
    breeds_schemas = [
        breed.serialize(schema_class=BreedSchema) for breed in breeds
    ]
    
    return breeds_schemas