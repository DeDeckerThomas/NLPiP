from pydantic import BaseModel


class TweetPredictionResult(BaseModel):
    label: str
    score: float
