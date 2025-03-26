import pytest
import asyncio
import httpx

@pytest.mark.asyncio
async def test_stress_multiple_endpoints():
    endpoints = [
        ("http://localhost:5001/speed", {"speed": 50}),
        ("http://localhost:5001/move", {"direction": "up"}),
        ("http://localhost:5001/position", {"x": 10.5, "y": 20.7}),
    ]
    num_requests = 500

    async with httpx.AsyncClient() as client:
        tasks = [
            client.post(url, json=data) for url, data in endpoints for _ in range(num_requests)
        ]
        responses = await asyncio.gather(*tasks)

    assert all(response.status_code == 200 for response in responses)
