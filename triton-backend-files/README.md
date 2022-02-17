# Triton inference server

This directory contains everything you need to build the custom triton inference server image for the CPU and GPU scenario.

## 💾 Installation

To build and push this image to GCP, you need the [Cloud SDK](https://cloud.google.com/sdk). You can find more information on how to install it here: https://cloud.google.com/sdk/docs/install.

Navigate to the triton-backend-files directory.

```bash
cd triton-backend-files
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
  - id: 'build-image'
    name: 'gcr.io/cloud-builders/docker'
    args: ['build', '--tag', 'gcr.io/{project_id}/triton_server_for_optimized_transformers:latest', '.']
  - id: 'push-image'
    name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/{project_id}/triton_server_for_optimized_transformers:latest']
```

Run the following command to build and push this image to Google Container Registry. For this command it is necessary to pass a timeout value (The image is very large and it may take a few minutes).

```bash
gcloud builds submit --config ./cloudbuild.yaml --timeout 3600
```

Congratulations, your image is pushed 🥳. Now you can start deploying the optimized CPU and GPU scenarios. Please, go to the desired directory for more information.

## ✨ Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
