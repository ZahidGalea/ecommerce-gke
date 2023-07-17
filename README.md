### Credentials setting

```bash
export GOOGLE_APPLICATION_CREDENTIALS="infrastructure/dev/ecommerce-dev-392819-dde10994963d.json"
gcloud auth activate-service-account "infrastructure-terraform-sa@ecommerce-dev-392819.iam.gserviceaccount.com" --key-file=$GOOGLE_APPLICATION_CREDENTIALS
gcloud auth configure-docker us-east1-docker.pkg.dev
```

### Build ecommerce app and push up

```bash
docker build -t us-east1-docker.pkg.dev/ecommerce-dev-392819/front-app/flutter-app:0.0.4 .
docker push us-east1-docker.pkg.dev/ecommerce-dev-392819/front-app/flutter-app:0.0.4
```

Run it locally

```bash
docker run -p 80:80 us-east1-docker.pkg.dev/ecommerce-dev-392819/front-app/flutter-app:0.0.1
```

### Run ecommerce app in GKE

Authenticate with the cluster

```bash
gcloud auth login
gcloud config set project "ecommerce-dev-392819"
gcloud container clusters get-credentials ecommerce-gke --zone us-east1
```

App Installation with helm

```bash 
kubectl config set-context --current --namespace ecommerce
helm install dev . --namespace ecommerce --create-namespace --dependency-update --wait --debug
``` 

```bash 
helm upgrade dev . --namespace ecommerce --create-namespace --dependency-update --wait --debug
```

### Infrastructure

```bash
terraform plan -out=plan.tfplan
```

```bash
terraform apply "plan.tfplan"
```

### SAST Verification

```shell
docker run --rm -it -v ${PWD}/infrastructure:/src aquasec/tfsec /src
```