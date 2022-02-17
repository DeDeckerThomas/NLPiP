from functools import lru_cache
from typing import List
from fastapi import APIRouter, HTTPException
from transformers import Pipeline, pipeline, AutoModelForSequenceClassification, AutoTokenizer
from core.config import settings
from models.TweetPredictionResult import TweetPredictionResult
from fastapi.logger import logger


@lru_cache()
def load_model() -> Pipeline:
    model: AutoModelForSequenceClassification = AutoModelForSequenceClassification.from_pretrained(
        settings.API_TASK_MODEL
    )
    tokenizer: AutoTokenizer = AutoTokenizer.from_pretrained(
        settings.API_TASK_MODEL
    )
    return pipeline(task=settings.API_TASK, model=model, tokenizer=tokenizer)


router: APIRouter = APIRouter(prefix="/api")
classifier: Pipeline = load_model()


@router.post("/predict")
def predict_tweet(prediction_requests: List[str]) -> List[TweetPredictionResult]:
    if not(prediction_requests):
        raise HTTPException(
            status_code=400,
            detail="There is are no tweets to classify 🐦. Please provide at least one valid tweet."
        )
    if len(prediction_requests) > settings.TWEET_LIMIT:
        raise HTTPException(
            status_code=400,
            detail=f"You can only classify a maximum of {settings.TWEET_LIMIT} tweets per request 🐦."
        )
    try:
        results: List[TweetPredictionResult] = classifier(prediction_requests)
        return results
    except Exception as exception:
        logger.error(exception)
        raise HTTPException(
            status_code=500,
            detail="Something went wrong on our end 🔧. Please try again later!"
        )
