### Credentials setting

```bash
export GOOGLE_APPLICATION_CREDENTIALS="ecommerce-dev-392819-dde10994963d.json"
```

## Presentation to GCR deployment.

Dev

```bash
export GOOGLE_APPLICATION_CREDENTIALS="infrastructure/dev/ecommerce-dev-392819-dde10994963d.json"
gcloud auth activate-service-account "infrastructure-terraform-sa@ecommerce-dev-392819.iam.gserviceaccount.com" --key-file=$GOOGLE_APPLICATION_CREDENTIALS
gcloud auth configure-docker us-east1-docker.pkg.dev

gcloud config set project "ecommerce-dev-392819"
gcloud container clusters get-credentials ecommerce-gke --zone us-east1

python ci/presentation.py --gcp_project_id "ecommerce-dev-392819" --env dev

```

Prod

```bash
python ci/presentation.py --gcp_project_id "xxxx" --env prod
```

