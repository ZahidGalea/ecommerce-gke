Credentials setting

```bash
export GOOGLE_APPLICATION_CREDENTIALS="infrastructure/dev/ecommerce-dev-392819-dde10994963d.json"
gcloud auth activate-service-account "infrastructure-terraform-sa@ecommerce-dev-392819.iam.gserviceaccount.com" --key-file=$GOOGLE_APPLICATION_CREDENTIALS
gcloud auth configure-docker
```

CI/CD Dev

```bash
export GOOGLE_APPLICATION_CREDENTIALS="infrastructure/dev/ecommerce-dev-392819-dde10994963d.json"
python ci/infrastructure.py -g "$(cat $GOOGLE_APPLICATION_CREDENTIALS)" --env dev
```

```bash
export GOOGLE_APPLICATION_CREDENTIALS="secrets/ecommerce-dev-392819-dde10994963d.json"
python ci/front.py --front_version "0.0.1" --env dev --gcp_project_id ecommerce-dev-392819
```

### SAST Verification

```shell
docker run --rm -it -v ${PWD}/infrastructure:/src aquasec/tfsec /src
```