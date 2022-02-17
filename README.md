# Bachelor Thesis: NLPiP (NLP in Production)

This repository contains everything regarding the bachelor thesis: NLPiP (NLP in Production).

## ⚽ Goal

## Research question: How to deploy fast optimized transformer models in a modern, cloud-native way on GCP?

Transformers are big models, and they can be difficult to get into production. There is also a huge landscape of different optimization techniques and backend technologies that does not make this task any easier either.

This is what this research project aims to answer with an analysis of different scenarios of using transformers in production based on latency, accuracy, cost, and effort.

## Pretrained model

The pretrained model that is used in the different scenarios is the distilbert-base-uncased-finetuned-sst-2-english on the Hugging Face model hub. You can find more information on the model card: https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english.

This model is a transformer. Transformers are deep learning models that are used in the field of natural language processing.
In this case the model takes a text input and predicts the sentiment of that text input (positive or negative).

## 3 scenarios:

For comparison, benchmarking and testing the same pre-trained model is used. In some of these scenarios, it could be possible that some things need to be changed. For example: In the gpu scenario (Twitter), you will need a custom dataset with example tweets that you really want to censor. Otherwise, you will censor a lot of medium negative things like: "I don't like Facebook.".

### Baseline scenario:

A hobby developer who has a blog about programming with an average of 10.000 visitors per week. Like any other blog, this blog receives
unwanted negative comments.

This developer wants to do something about that, so he takes on the challenge of solving this problem. This basic application will label every comment, so that the developer can go through them and remove the unwanted negative comments.

Practical set-up: BERT transformer model loaded into memory on a simple FastAPI application deployed on GCP Cloud Run. This will be a baseline on how the average developer would do it.


Effect on metrics:

* Latency: Not important.
* Accuracy: As high as possible, all negative comments must be recognized.
* Hasselhoff factor (Effort): 2.
    * Basic understanding of transformers.
    * You only need to know about the simple functions in the HuggingFace library.
    * Knowledge of FastAPI and Docker.
    * Deployment process: knowledge of Cloud Run.

* Estimated Price: 35 euro/month for a 2 vCPUs, 4GB Ram Cloud Run instance. You can find lore information here: https://cloud.google.com/products/calculator/#id=f552fbc2-8afe-4d6b-9b7f-7947e1399979

### CPU optimized scenario:

A large supermarket chain that wants to start a project to get more insight about the sentiment in product reviews. They have heard that AI can be used for this and they want to see that in action. So they wish a medium budget application that can process reviews in a medium-fast manner. Latency is not crucial but important.


Practical set-up: BERT transformer model optimized with quantization. ONNX as serving framework and this will run in a CPU-enabled NVIDIA Triton container deployed on a Kubernetes cluster.


Effect on metrics:

* Latency: important, but not crucial. (Starter project)
* Accuracy: As high as possible, all positive and negative - reviews should be correctly classified.
* Hasselhoff factor (Effort): 6
    * Basic understanding of transformers.
    * You need to know more about the HuggingFace library, ONNX and optimization.
    * Deployment process: knowledge of NVIDIA Triton, Docker, Google GKE and Helm.

* Estimated Price: 160 euro/month for two node pools in a Kubernetes Cluster. A default pool for statistics and cluster management and a CPU-pool (N2-Standard-4: 16GB 4 vCPUs Intel Ice Lake) for NVIDIA Triton inference server. You can find more information here: https://cloud.google.com/products/calculator/#id=595af456-da2b-445b-8b1e-4f03c6a1e0bd

### GPU optimized scenario:

Twitter has a strict policy on cyberbullying and wants to delete negative comments as soon as possible. Negative tweets give a very bad image to the company itself. Therefore, they want an application with the lowest possible latency, no matter what the cost is.


Practical set-up: BERT transformer model optimized with quantization. ONNX as serving framework and this will run in a GPU-enabled NVIDIA Triton container deployed on a Kubernetes cluster.



Effect on metrics:

* Latency: Low latency is crucial.
* Accuracy: Very important.
* Hasselhoff factor (Effort): 8

    * Basic understanding of transformers.
    * You need to know more about the HuggingFace library, ONNX, optimization and TensorRT. If you really want to take full advantage of TensorRT, a basic knowledge of C++ is required. This has partly been made easier with a python wrapper but it is still fairly new.
    * Deployment process: knowledge of NVIDIA Triton, Docker, Google GKE and Helm.

* Estimated Price: 301 euro/month for two node pools in a Kubernetes Cluster. A default pool for statistics and cluster management and a GPU-pool (N1-Standard-4: 15GB 4 vCPUs Intel Sky Lake 1st generation and 1 NVIDIA TESLA T4 16 GB GDDR6) for NVIDIA Triton inference server. More information: https://cloud.google.com/products/calculator/#id=37ecf273-aebb-47b4-91e1-23c08dc7fbd4

## 💾 Benchmarks

Benchmarking was done with the provided benchmark API. This API helps to provide a picture of how well transformers can be improved in production under different scenarios.

Local benchmark for testing (Docker-compose)

```json
{
    "scenario": "baseline",
    "single": {
        "average_latency": 13.07956,
        "std_latency": 0.578751057364045,
        "95p_latency": 14.1686,
        "batch_size": 1
    },
    "multiple": {
        "average_latency": 352.45041000000003,
        "std_latency": 5.132505337737118,
        "95p_latency": 361.82115,
        "batch_size": 32
    },
    "accuracy": 0.9105504587155964,
    "timestamp": "2022-01-28T08:36:42.949526"
}

{
    "scenario": "fast-cpu",
    "single": {
        "average_latency": 3.07945,
        "std_latency": 0.2900197019169559,
        "95p_latency": 3.5978,
        "batch_size": 1
    },
    "multiple": {
        "average_latency": 22.740130000000008,
        "std_latency": 0.8172525271297727,
        "95p_latency": 24.0126,
        "batch_size": 32
    },
    "accuracy": 0.9048165137614679,
    "timestamp": "2022-01-28T08:37:33.047886"
}

{
    "scenario": "fast-gpu",
    "single": {
        "average_latency": 2.90327,
        "std_latency": 0.18527573262572736,
        "95p_latency": 3.27105,
        "batch_size": 1
    },
    "multiple": {
        "average_latency": 6.315669999999998,
        "std_latency": 0.44793611274377065,
        "95p_latency": 7.01595,
        "batch_size": 32
    },
    "accuracy": 0.9071100917431193,
    "timestamp": "2022-01-28T08:38:42.802653"
}
```

Google Cloud benchmark where every scenario is deployed on GCP.

```json
{
    "scenario": "baseline",
    "single": {
        "average_latency": 60.280870000000014,
        "std_latency": 6.982528636038667,
        "95p_latency": 72.34775,
        "batch_size": 1
    },
    "multiple": {
        "average_latency": 1223.4084900000003,
        "std_latency": 54.914856587174114,
        "95p_latency": 1331.5587,
        "batch_size": 32
    },
    "accuracy": 0.9105504587155964,
    "timestamp": "2022-01-30T13:42:54.749054"
}

{
    "scenario": "fast-cpu",
    "single": {
        "average_latency": 7.774379999999999,
        "std_latency": 0.47211705709495394,
        "95p_latency": 8.55275,
        "batch_size": 1
    },
    "multiple": {
        "average_latency": 48.17986,
        "std_latency": 3.664230628713209,
        "95p_latency": 55.75265,
        "batch_size": 32
    },
    "accuracy": 0.9048165137614679,
    "timestamp": "2022-01-30T13:44:01.131298"
}

{
    "scenario": "fast-gpu",
    "single": {
        "average_latency": 5.495990000000001,
        "std_latency": 1.1793932465043202,
        "95p_latency": 6.254199999999998,
        "batch_size": 1
    },
    "multiple": {
        "average_latency": 9.062449999999998,
        "std_latency": 0.5076055629127798,
        "95p_latency": 9.9628,
        "batch_size": 32
    },
    "accuracy": 0.9071100917431193,
    "timestamp": "2022-01-30T13:45:13.687763"
}
```

### Conclusions
Calculations based on GCP benchmark.

* Batch size 1
    * The CPU scenario inference is more than 7x faster than the baseline scenario.
    * The GPU scenario inference is more than 10x faster than the baseline scenario.
    * The GPU scenario inference is more than 1.4x faster than the CPU scenario.

* Batch size 32
    * The CPU scenario inference is more than 25x faster than the baseline scenario.
    * The GPU scenario inference is more than 135x faster than the baseline scenario.
    * The GPU scenario inference is more than 5x faster than the CPU scenario.

* There is a accuracy drop < 1%.
* NVIDIA Triton is more interesting for bigger batches than single samples.

## 💾 Installation

For the installation of a specific scenario, you will find a guide in the corresponding directory.
In addition to the scenarios, a simple benchmark API is provided to test these scenarios.

## 📋 Interesting resources

This section contains interesting resources where you can read more about this topic in general.

- https://github.com/ELS-RD/transformer-deploy
- https://towardsdatascience.com/hugging-face-transformer-inference-under-1-millisecond-latency-e1be0057a51c
- https://huggingface.co/infinity
- https://www.youtube.com/watch?v=jiftCAhOYQA
- Recent: https://www.youtube.com/watch?v=5E0nlHWgMMU

## ❓ Questions

If you have any question, feel free to contact Thomas De Decker.

## ✨ Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
