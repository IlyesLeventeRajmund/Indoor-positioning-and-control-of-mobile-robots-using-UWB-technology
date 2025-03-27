import pytest
import asyncio
import httpx
import time

@pytest.mark.asyncio
async def test_stress_multiple_endpoints():
    endpoints = [
        ("http://localhost:5001/speed", {"speed": 50}),
        ("http://localhost:5001/move", {"direction": "up"}),
        ("http://localhost:5001/position", {"x": 10.5, "y": 20.7}),
    ]
    
    request_counts = [500, 1000, 5000, 10000]
    results = []

    async with httpx.AsyncClient() as client:
        for num_requests in request_counts:
            tasks = [client.post(url, json=data) for url, data in endpoints for _ in range(num_requests)]
            
            start_time = time.time()
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            end_time = time.time()
            
            success_count = sum(1 for r in responses if isinstance(r, httpx.Response) and r.status_code == 200)
            failure_count = len(responses) - success_count
            duration = end_time - start_time
            success_rate = (success_count / (num_requests * len(endpoints))) * 100

            results.append({
                "requests": num_requests * len(endpoints),
                "success": success_count,
                "failures": failure_count,
                "duration": duration,
                "success_rate": success_rate
            })

            print(f"\n=== Teszt {num_requests} kéréssel ===")
            print(f"Összes kérés: {num_requests * len(endpoints)}")
            print(f"Sikeres: {success_count}")
            print(f"Sikertelen: {failure_count}")
            print(f"Időtartam: {duration:.2f} másodperc")
            print(f"Sikerességi arány: {success_rate:.2f}%\n")

    assert all(r["success_rate"] >= 90 for r in results), "A sikerességi arány 90% alá esett!"
