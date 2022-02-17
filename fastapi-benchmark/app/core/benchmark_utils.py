import requests
from datetime import timedelta
import numpy as np
from core.config import settings
import zlib
import json
import google.auth.transport.requests
import google.oauth2.id_token


class BenchmarkUtils:

    @staticmethod
    def benchmark_endpoint(endpoint, data, backend_type, authentication):
        session = requests.Session()

        headers, request_data = BenchmarkUtils.get_request_for_backend_type(
            backend_type, endpoint, data, authentication)

        latencies = []
        for _ in range(settings.WARM_UP_RATE):
            response = session.post(
                endpoint, headers=headers, **request_data)

        for _ in range(settings.BENCHMARK_RATE):
            response = session.post(
                endpoint, headers=headers, **request_data)
            latencies.append(response.elapsed / timedelta(milliseconds=1))

        latencies = np.array(latencies)
        return {"average_latency": np.mean(latencies), "std_latency": np.std(latencies), "95p_latency": np.percentile(latencies, 95), "batch_size": len(data)}

    @staticmethod
    def predict(endpoint, data, backend_type, authentication):
        session = requests.Session()

        headers, request_data = BenchmarkUtils.get_request_for_backend_type(
            backend_type, endpoint, data, authentication)

        response = session.post(endpoint, headers=headers, **request_data)
        return response.json()

    @staticmethod
    def get_request_for_backend_type(backend_type, endpoint, data, authentication):
        headers = {}
        if backend_type == "fastapi":
            headers.update({"Content-Type": "application/json",
                           "Accept": "application/json"})
            request_data = {"json": data}
        elif backend_type == "triton":
            request_body = {
                "inputs": [
                    {
                        "name": "text",
                        "shape": (len(data),),
                        "datatype": "BYTES",
                        "data": data,
                    }
                ],
                "outputs": [
                    {
                        "name": "label",
                        "parameters": {"binary_data": False},
                    },
                    {
                        "name": "score",
                        "parameters": {"binary_data": False},
                    }
                ],
            }
            bytes_message = bytes(json.dumps(request_body),
                                  encoding="raw_unicode_escape")
            request_body = zlib.compress(bytes_message)
            headers.update({
                "Content-Encoding": "gzip",
                "Accept-Encoding": "gzip",
                "Inference-Header-Content-Length": str(len(bytes_message))
            })
            request_data = {"data": request_body}
        if authentication == "google":
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(
                auth_req, endpoint)
            headers.update({"Authorization": f"Bearer {id_token}"})
        return headers, request_data
