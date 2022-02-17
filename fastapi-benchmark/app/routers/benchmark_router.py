from datetime import datetime
from functools import lru_cache
from fastapi import APIRouter
from core.config import settings
from models.benchmark_request import BenchmarkRequest
from datasets import load_dataset, load_metric
from core.benchmark_utils import BenchmarkUtils
import json
import requests



@lru_cache
def load_eval_dataset():
    return load_dataset("glue", "sst2")["validation"]


@lru_cache
def load_scenarios():
    with open(settings.SCENARIOS_FILE) as f:
        data = json.load(f)
    return data


@lru_cache
def load_accuracy_metric():
    return load_metric('accuracy')


router = APIRouter(prefix="/api")
labels_mapping = {"negative": 0, "positive": 1}
eval_dataset = load_eval_dataset()
scenarios = load_scenarios()
accuracy_metric = load_accuracy_metric()


@router.post("/benchmark")
def benchmark(benchmark_request: BenchmarkRequest):
    results = {"scenario": benchmark_request.scenario}
    endpoint = scenarios[benchmark_request.scenario]["endpoint"]
    backend_type = scenarios[benchmark_request.scenario]["backend_type"]
    authentication = scenarios[benchmark_request.scenario].get("authentication", None)

    if benchmark_request.batch_size is None:
        benchmark_request.batch_size = settings.DEFAULT_BENCHMARK_BATCH_SIZE

    if benchmark_request.latency_input_data is None:
        benchmark_request.latency_input_data = settings.DEFAULT_BENCHMARK_INPUT_DATA

    data_sample = benchmark_request.latency_input_data
    data = [data_sample for i in range(1)]
    results["single"] = BenchmarkUtils.benchmark_endpoint(
        endpoint, data, backend_type, authentication)

    data = [data_sample for i in range(benchmark_request.batch_size)]
    results["multiple"] = BenchmarkUtils.benchmark_endpoint(
        endpoint, data, backend_type, authentication)

    data = eval_dataset["sentence"]
    predictions = BenchmarkUtils.predict(endpoint, data, backend_type, authentication)
    if backend_type == "fastapi":
        pred_labels = [labels_mapping[prediction["label"].lower()]
                       for prediction in predictions]
    elif backend_type == "triton":
        pred_labels = [labels_mapping[prediction.lower()]
                       for prediction in predictions["outputs"][1]["data"]]
    results["accuracy"] = accuracy_metric.compute(
        predictions=pred_labels, references=eval_dataset["label"]).get("accuracy")

    results["timestamp"] = datetime.now()
    return results
