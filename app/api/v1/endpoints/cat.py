from uuid import UUID
from typing import Dict, List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.core.container import Container
from app.db.models import Cat
from app.schemas.cat import CatCreateSchema, CatSchema, CatUpdateSchema
from app.schemas.breed import BreedSchema
from app.services import CatService, BreedService


router = APIRouter(tags=['Cat'], prefix='/cats')


@router.post(
    '/', 
    status_code=status.HTTP_201_CREATED, 
    response_model=CatSchema,
)
@inject
async def create_cat(
    create_cat_schema: CatCreateSchema,
    cat_service: CatService = Depends(
        Provide[Container.cat_service]
    ),
    breed_service: BreedService = Depends(
        Provide[Container.breed_service]
    ),
) -> CatSchema:
    create_cat_schema.breed_id = UUID(create_cat_schema.breed_id)
    cat = await cat_service.create(
        obj_in=create_cat_schema
    ) 
    breed = await breed_service.get(
        id=create_cat_schema.breed_id,
    )
    cat_schema = cat.serialize(
        schema_class=CatSchema,
        exclude_fields=('breed', )
    )
    cat_schema['breed'] = breed.serialize(
        schema_class=BreedSchema,
    )
    
    return cat_schema


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[CatSchema])
@inject
async def get_cats(
    limit: int = 10, 
    skip: int = 0, 
    cat_service: CatService = Depends(
        Provide[Container.cat_service]
    ),
) -> List[CatSchema]:
    cats = await cat_service.list(
        load_breed=True,
        limit=limit,
        skip=skip
    )
    cats_schemas = [cat.serialize(schema_class=CatSchema) for cat in cats]
    
    return cats_schemas


@router.get(
    '/{cat_id}', 
    status_code=status.HTTP_200_OK,
    response_model=CatSchema
)
@inject
async def get_cat(
    cat_id: UUID,
    cat_service: CatService = Depends(
        Provide[Container.cat_service]
    ),
) -> CatSchema:
    cat = await cat_service.get(load_breed=True, id=cat_id)    
    return cat.serialize(schema_class=CatSchema)


@router.get(
    '/breed/{breed_id}',
    status_code=status.HTTP_200_OK,
    response_model=List[CatSchema],
    response_model_exclude_none=True,
)
@inject
async def get_cats_by_breed(
    breed_id: UUID, 
    limit: int = 10, 
    skip: int = 0, 
    cat_service: CatService = Depends(
        Provide[Container.cat_service]
    ),
) -> List[CatSchema]:
    cats = await cat_service.list(
        breed_id=breed_id,
        limit=limit,
        skip=skip
    )
    cats_schemas = [
        cat.serialize(
            schema_class=CatSchema,
            exclude_fields=('breed', )
        )
        for cat in cats
    ]
    return cats_schemas


@router.put('/{cat_id}', status_code=status.HTTP_200_OK)
@inject
async def update_cat(
    cat_id: UUID,
    cat_update_schema: CatUpdateSchema,
    cat_service: CatService = Depends(
        Provide[Container.cat_service]
    ),
) -> CatSchema:
    cat_update_schema.breed_id = UUID(cat_update_schema.breed_id)
    cat = await cat_service.update(
        obj_id=cat_id,
        obj_in=cat_update_schema
    )
    
    return cat.serialize(schema_class=CatSchema)


@router.delete('/{cat_id}', status_code=status.HTTP_200_OK)
@inject
async def delete_cat(
    cat_id: UUID,
    cat_service: CatService = Depends(
        Provide[Container.cat_service]
    ),
) -> dict:
    await cat_service.delete(obj_id=cat_id)

    return {'message': 'Кошка успешно удалена'}