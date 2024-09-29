import uuid

import pytest
from httpx import AsyncClient, ASGITransport

from app.core.config import settings
from app.schemas.cat import CatCreateSchema
from app.schemas.breed import BreedCreateSchema
from app.utils.http import post_request
from app.db import db_manager, Base
from app.main import app


@pytest.fixture(scope='session', autouse=True)
async def setup_db():
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    yield
    
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        
        
@pytest.fixture
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=f'{settings.base_url}{settings.api_v1_prefix}'
    ) as client:
        yield client
         
         
@pytest.fixture
async def created_breed(async_client: AsyncClient) -> dict:
    data = {'name': f'breed_{uuid.uuid4()}'}
    schema = BreedCreateSchema(**data)
    
    return await post_request(
        async_client,
        post_url_prefix='/breeds/',
        data=schema.model_dump()
    )
    

@pytest.fixture
async def created_cat(
    async_client: AsyncClient,
    created_breed: dict,
) -> dict:
    data = {
        'name': 'Fluffy',
        'color': 'white',
        'age_months': 20,
        'description': 'Very anxious',
        'breed_id': created_breed['id']
    }
    schema = CatCreateSchema(**data)
    
    return await post_request(
        async_client,
        post_url_prefix='/cats/',
        data=schema.model_dump()
    )
    


