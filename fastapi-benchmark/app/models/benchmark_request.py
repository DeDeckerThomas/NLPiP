from typing import Optional
from pydantic import BaseModel

class BenchmarkRequest(BaseModel):
    scenario: str
    latency_input_data: Optional[str]
    batch_size: Optional[int]

