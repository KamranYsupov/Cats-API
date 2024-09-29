from httpx import AsyncClient

async def post_request(
    async_client: AsyncClient,
    post_url_prefix: str,
    data: dict,
    expected_status_code: int = 201
):
    response = await async_client.post(post_url_prefix, json=data)

    if response.status_code == expected_status_code:
        print(response.text)
        return response.json()
    else:
        raise Exception(str(response.json()))