# FastAPI Benchmark API

Benchmark API for [Sentiment analysis](https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english) on the baseline, CPU and GPU scenario.

## 💾 Installation

### Manual deploy on Cloud Run (GCP)

> ⚠️ Make sure you have all the scenarios set up


To deploy this image to GCP, you need the [Cloud SDK](https://cloud.google.com/sdk). You can find more information on how to install it here: https://cloud.google.com/sdk/docs/install

Navigate to the FastAPI-transformer-baseline directory.

```bash
cd FastAPI-transformer-baseline
```

Run gcloud init to update your information and select the necessary project.

```bash
gcloud init
```

For the benchmark API, you need a VPC connector to access the Kubernetes cluster. Please fill in the missing parameters with your parameters. If you need more information, go check the documentation: https://cloud.google.com/vpc/docs/configure-serverless-vpc-access.

```
gcloud compute networks vpc-access connectors create vpc-connector \
--region "your preferred region" \
--subnet "your preferred subnet" \
--min-instances 2 \
--max-instances 3 \
```

You will also need a scenarios.json configuration file and Google service account credentials json file.

The scenarios file is simple and you can create it yourself. 
> ⚠️ Don't forget to fill in the endpoints! You can find the endpoints on Google Cloud.

```json
{
  "baseline": {
    "endpoint": "baseline-endpoint",
    "backend_type": "fastapi"
  },
  "fast-cpu": {
    "endpoint": "internal ip of cpu service",
    "backend_type": "triton"
  },
  "fast-gpu": {
    "endpoint": "internal ip of gpu service",
    "backend_type": "triton"
  }
}

```

For the credentials file, you will have to create a service account and add the invoker role to it.
```bash
gcloud iam service-accounts create fastapi-baseline-app
```

```bash
gcloud projects add-iam-policy-binding {project_id} \ 
--member="serviceAccount:fastapi-baseline-app@{your_project_id}.iam.gserviceaccount.com" 
--role="roles/run.invoker"
```

Then you can create a Google credentials json file with the following command.

```bash
gcloud iam service-accounts keys create creds.json --iam-account=fastapi-baseline-app@calm-flames-337807.iam.gserviceaccount.com
```

Now you have both files, you can add them as secrets. Run the following commands.

```bash
gcloud secrets create fastapi-benchmark-scenarios --data-file="path to your scenarios file"
```

```bash
gcloud secrets create fastapi-baseline-app-creds --data-file="path to your service account credentials file"
```


Once this is done, you can start building the image with [Google Cloud Build](https://cloud.google.com/build). For more information, check the documentation: https://cloud.google.com/build/docs.

First make a cloudbuild.yaml file (For the content see below 👇)

> ⚠️ Replace `{project_id}` with your [GCP Project ID](https://cloud.google.com/resource-manager/docs/creating-managing-projects). Otherwise this snippit won't work. Otherwise, all parameters are filled in.

```yaml
steps:
  - id: "build-image"
    name: "gcr.io/cloud-builders/docker"
    args:
      [
        "build",
        "--tag",
        "gcr.io/{project_id}/fastapi_benchmark:latest",
        ".",
      ]
  - id: "push-image"
    name: "gcr.io/cloud-builders/docker"
    args:
      [
        "push",
        "gcr.io/{project_id}/fastapi_benchmark:latest",
      ]
    waitFor: ["build-image"]
  - id: "deploy-image"
    name: "gcr.io/google.com/cloudsdktool/cloud-sdk"
    entrypoint: gcloud
    args:
      [
        "run",
        "deploy",
        "fastapi-baseline",
        "--image",
        "gcr.io/{project_id}/fastapi_benchmark:latest",
        "--region",
        "your_region",
        "--port",
        "80"
        "--memory",
        "4Gi",
        "--cpu",
        "2",
        "--vpc-connector",
        "vpc-connector",
        "--set-env-vars",
        "APP_NAME=Benchmark API,WARM_UP_RATE=10,BENCHMARK_RATE=100,DEFAULT_BENCHMARK_BATCH_SIZE=32,DEFAULT_BENCHMARK_INPUT_DATA=Hello everyone!,SCENARIOS_FILE=/app/scenarios/fastapi-benchmark-scenarios,GOOGLE_APPLICATION_CREDENTIALS=/app/secrets/fastapi-baseline-app-creds",
        "--set-secrets",
        "/app/scenarios/fastapi-benchmark-scenarios=fastapi-benchmark-scenarios:latest,/app/secrets/fastapi-baseline-app-creds=fastapi-baseline-app-creds:latest"
      ]
    waitFor: ["push-image"]

```

Run the following command to build and deploy this service to cloud run.

```bash
gcloud builds submit . --config cloudbuild.yaml
```

Congratulations, your service is ready 🥳.

### Automatic deploy on Cloud Run (GCP)

If you forked this repo, you can use Google Cloud Build triggers for continous deployment. If you want this, you can read the following document: https://cloud.google.com/build/docs/automating-builds/create-manage-triggers

## ✍️ Usage

This service has Swagger documentation, go to the /docs page for more information.

## ✨ Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
