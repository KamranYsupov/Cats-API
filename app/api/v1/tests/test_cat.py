import pytest
from httpx import AsyncClient


async def test_create_cat(
    async_client: AsyncClient, 
    created_cat: dict,
):
    assert isinstance(created_cat, dict)


async def test_get_cats(
    async_client: AsyncClient, 
):
    response = await async_client.get('/cats/')
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_cat(
    async_client: AsyncClient, 
    created_cat: dict,
):
    cat_id = created_cat['id']
    
    response = await async_client.get(f'/cats/{cat_id}')
    assert response.status_code == 200
    assert response.json()['id'] == cat_id


async def test_get_cats_by_breed(
    async_client: AsyncClient, 
    created_breed: dict,
):
    breed_id = created_breed['id']

    response = await async_client.get(f'/cats/breed/{breed_id}')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_update_cat(
    async_client: AsyncClient, 
    created_cat: dict,
    created_breed: dict,
):
    cat_update_data =  {
        'name': 'Updated Fluffy',
        'color': 'Updated white',
        'age_months': 20,
        'description': 'Updated Very anxious',
        'breed_id': created_breed['id']
    }
    cat_id = created_cat['id']

    response = await async_client.put(f'/cats/{cat_id}', json=cat_update_data)
    assert response.status_code == 200
    assert response.json()['name'] == cat_update_data['name']


async def test_delete_cat(
    async_client: AsyncClient, 
    created_cat: dict,
):
    cat_id = created_cat['id']

    delete_response = await async_client.delete(f'/cats/{cat_id}')
    assert delete_response.status_code == 200
    assert delete_response.json()['message'] == 'Кошка успешно удалена'

    get_response = await async_client.get(f'/cats/{cat_id}')
    assert get_response.status_code == 404  
