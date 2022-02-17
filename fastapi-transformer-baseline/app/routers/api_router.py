from typing import Dict
from fastapi import APIRouter
from routers import twitter_sentiment_analysis_router


api_router: APIRouter = APIRouter()
api_router.include_router(twitter_sentiment_analysis_router.router)


@api_router.get("/")
def main_endpoint() -> Dict[str, str]:
    return {"status": "The API is working correctly! 🙌"}
