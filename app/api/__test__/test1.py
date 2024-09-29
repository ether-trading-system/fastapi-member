from fastapi import FastAPI
from httpx import AsyncClient
import pytest
from httpx import ASGITransport

app = FastAPI()

@app.get("/test/hello-test")
def test_hello():
    return {"msg": "Hello Test!"}

@pytest.mark.asyncio
async def test_hello_test():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/test/hello-test")
        assert response.status_code == 200
        assert response.json() == {"msg": "Hello Test!"}
