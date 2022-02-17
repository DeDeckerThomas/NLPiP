from fastapi import APIRouter

from routers import benchmark_router

api_router = APIRouter()
api_router.include_router(benchmark_router.router)


@api_router.get("/")
def main_endpoint():
    return {"status": "The API is working correctly! 🙌"}
