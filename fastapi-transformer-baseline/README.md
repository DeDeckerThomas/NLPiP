# FastAPI baseline scenario

Simple prediction API for [sentiment analysis](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment) on CPU.
This transformer is loaded into memory using the transformers and PyTorch libraries.

## 💾 Installation

### Manual deploy on Cloud Run (GCP)

To deploy this image to GCP, you need the [Cloud SDK](https://cloud.google.com/sdk). You can find more information on how to install it here: https://cloud.google.com/sdk/docs/install.

Navigate to the FastAPI-transformer-baseline directory.

```bash
cd FastAPI-transformer-baseline
```

Run gcloud init to update your information and select the necessary project.

```bash
gcloud init
```

Once this is done, you can start building the image with [Google Cloud Build](https://cloud.google.com/build). For more information, check the documentation: https://cloud.google.com/build/docs

First make a cloudbuild.yaml file (For the content see below 👇)

> ⚠️ Replace `{project_id}` with your [GCP Project ID](https://cloud.google.com/resource-manager/docs/creating-managing-projects). Otherwise this snippit won't work.

```yaml
steps:
  - id: "build-image"
    name: "gcr.io/cloud-builders/docker"
    args:
      [
        "build",
        "--tag",
        "gcr.io/{project_id}/fastapi_transformer_baseline:latest",
        ".",
      ]
  - id: "push-image"
    name: "gcr.io/cloud-builders/docker"
    args:
      [
        "push",
        "gcr.io/{project_id}/fastapi_transformer_baseline:latest",
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
        "gcr.io/{project_id}/fastapi_transformer_baseline:latest",
        "--region",
        "your_region",
        "--port",
        "80"
        "--set-env-vars",
        "APP_NAME=Sentiment-Analysis,API_TASK=sentiment-analysis,API_TASK_MODEL=distilbert-base-uncased-finetuned-sst-2-english",
        "--memory",
        "4Gi",
        "--cpu",
        "2"
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
